# Use Cases — High Availability and Scalability

## Case 1: Multi-Tier E-commerce with ALB and ASG

**Context:**  
An e-commerce site needs high availability (99.9% SLA) with the ability to scale from 50 to 2,000 req/s during peak hours (Black Friday), separating API and frontend traffic.

**Architecture:**

```
Route 53 (DNS Failover + Health Check)
         │
         ▼
 Internet Gateway  (public VPC)
         │
         ▼
  ALB (multi-AZ, listener 443)
  ├── Rule 1: /api/* → TG-API (EC2 c5.xlarge, Target Tracking CPU 60%)
  ├── Rule 2: /static/* → TG-Static (S3 via redirect or EC2)
  └── Rule 3: default → TG-Web (EC2 t3.large, Target Tracking CPU 50%)

TG-API:
  └── ASG: min=2, max=50, desired=4
        ├── Scaling: Target Tracking (CPUUtilization = 60)
        └── Health check: ELB (/health, HTTP 200, interval 15s)

TG-Web:
  └── ASG: min=2, max=30, desired=4
        ├── Scaling: Target Tracking + Scheduled (Black Friday pre-scale)
        └── AZ: us-east-1a, us-east-1b, us-east-1c

ElastiCache (Session)     RDS Multi-AZ (DB)
us-east-1a               us-east-1a (primary)
us-east-1b               us-east-1b (standby AZ)

Backup /static:
  CloudFront → S3 (static assets, global CDN)
```

**Design decisions:**
- Path-based routing on ALB separates API from frontend without two ALBs
- ELB health check on ASG ensures automatic replacement of instances with application failure
- Scheduled scaling pre-provisions instances before Black Friday

**Concepts covered:** ALB path-based routing, ASG Target Tracking, ELB health check, multi-AZ, horizontal scalability

---

## Case 2: Internal API with PrivateLink and NLB

**Context:**  
A fintech exposes a payments API for external partners. Partners have their own VPCs and need to access the API securely, without internet traffic, without VPC Peering (regulatory requirement prohibiting CIDR overlap).

**Architecture:**

```
Fintech Account (Provider):                  Partner A Account:
┌──────────────────────────────┐             ┌─────────────────────┐
│  VPC: 10.0.0.0/16            │             │  VPC: 10.0.0.0/16   │
│                              │             │  (same CIDR — ok!)  │
│  EC2 (API Payment)           │             │                     │
│    └── Port 8443             │             │  EC2 (Consumer)     │
│         ↓                    │             │    └── Interface VPC │
│  NLB (internal)              │ PrivateLink │       Endpoint       │
│  └── TG: port 8443           │◀───────────▶│    IP: 10.0.x.x     │
│  └── Listener: 443           │             │    (ENI in VPC)      │
│  └── TLS: ACM cert           │             │                     │
│         ↓                    │             └─────────────────────┘
│  VPC Endpoint Service        │
│  (with account whitelist)    │             Partner B Account:
│                              │             ┌─────────────────────┐
└──────────────────────────────┘             │  Same pattern ↑     │
                                             └─────────────────────┘

Traffic: 100% within AWS network (never internet)
No Peering: no route between VPCs, no CIDR overlap issues
```

**Endpoint Service Configuration:**
```bash
# Create the service from the NLB
aws ec2 create-vpc-endpoint-service-configuration \
  --network-load-balancer-arns arn:aws:elasticloadbalancing:... \
  --acceptance-required  # requires manual approval for new consumers

# Add permission for the partner account to create an endpoint
aws ec2 modify-vpc-endpoint-service-permissions \
  --service-id vpce-svc-xxxxxxxxxxxxxxxx \
  --add-allowed-principals "arn:aws:iam::PARTNER_ACCOUNT_ID:root"
```

**Concepts covered:** PrivateLink, NLB as VPC Endpoint Service backend, Interface VPC Endpoint, cross-account security without internet

---

## Case 3: Blue/Green Deployment Without Downtime

**Context:**  
A DevOps team needs to deploy new application versions with zero downtime, with immediate rollback capability if the new version has errors.

**Architecture with ALB Weighted Target Groups:**

```
ALB Listener (:443)
│
└── Rule: /* → Forward (weighted)
      ├── TG-Blue (version 1.2.0): weight 90% → 9 instances (m5.large)
      └── TG-Green (version 2.0.0): weight 10% → 1 instance (m5.large)

Gradual deploy:
  Phase 1: Blue 100%, Green 0%    (new version available but no traffic)
  Phase 2: Blue 95%, Green 5%     (canary: monitoring)
  Phase 3: Blue 80%, Green 20%    (validation)
  Phase 4: Blue 50%, Green 50%    (50/50)
  Phase 5: Blue 0%, Green 100%    (full deploy)

Instant rollback:
  Any phase: change weights → Blue 100%, Green 0%
  API: aws elbv2 modify-rule (< 1 second propagation)

Monitoring (CloudWatch):
  ├── ALB: HTTPCode_Target_5XX_Count per TG
  ├── ALB: TargetResponseTime per TG
  └── Alarm → SNS → Lambda (automatic rollback if error rate > 1%)
```

**Concepts covered:** ALB weighted target groups, blue/green zero-downtime, canary release, automated rollback

---

## Case 4: Worker Fleet with Lifecycle Hooks and SQS

**Context:**  
A video processing system uses EC2 to transcode files received from an SQS queue. Each job takes up to 30 minutes. On scale-in, it is critical that the current job completes before the instance is terminated.

**Architecture:**

```
SQS Queue (video-jobs)
    │ Long polling
    ▼
ASG Worker Fleet
  ├── Scale-out Trigger: ApproximateNumberOfMessages > 10 (Custom CloudWatch Metric)
  ├── Scale-in Trigger: ApproximateNumberOfMessages = 0 for 5 min
  │
  └── Lifecycle Hook: EC2_INSTANCE_TERMINATING
          └── Timeout: 3600s (1 hour)
          └── Notification: EventBridge Rule

EventBridge Rule (lifecycle hook event)
  └── Lambda: LifecycleHookTerminating
        ├── Queries job status on the instance (SSM Parameter Store)
        │     └── /workers/{instance-id}/job-status
        ├── If job running: waits (polls every 60s)
        ├── If job complete: CompleteLifecycleAction(CONTINUE)
        └── If timeout (safety): CompleteLifecycleAction(CONTINUE)

Full flow:
  ASG decides to terminate instance-X
    → instance-X transitions to Terminating:Wait
    → EventBridge triggers Lambda
    → Lambda checks: job in progress
    → Lambda waits 20 minutes
    → Lambda confirms job completed
    → CompleteLifecycleAction(CONTINUE)
    → instance-X terminates normally
```

**Concepts covered:** Lifecycle Hooks, Terminating:Wait, EventBridge, Lambda for lifecycle automation, custom CloudWatch metrics for ASG scaling

---

## Case 5: Traffic Inspection with GWLB and Security Appliance

**Context:**  
A financial services company needs to inspect all inbound and outbound application traffic with a third-party IDS/IPS (Palo Alto Networks) before it reaches the application servers.

**Architecture:**

```
Internet Gateway
      │
      ▼
VPC Provider Account (Centralized Security Hub):
┌──────────────────────────────────────────┐
│  GWLB Endpoint (in consumer VPC)         │
│       │                                  │
│  GWLB (Layer 3, GENEVE)                  │
│  └── Target Group: Firewall EC2s         │
│        ├── Palo Alto VM-Series (AZ-a)    │
│        └── Palo Alto VM-Series (AZ-b)    │
└──────────────────────────────────────────┘
      │ Inspected packets returned
      ▼
VPC Consumer (Application Account):
┌──────────────────────────────────────────┐
│  Ingress Routing (VPC Route Table)       │
│  Destination: 0.0.0.0/0 → GWLB Endpoint │
│  (All internet traffic goes to GWLB)     │
│                                          │
│  ALB → ASG (App Servers)                 │
└──────────────────────────────────────────┘

Flow:
  Internet → IGW → GWLB Endpoint → GWLB → Palo Alto
    → (if OK) returned to GWLB → GWLB Endpoint → ALB → App
  If blocked by IDS/IPS → dropped

Benefit: Appliances centrally managed in Security Hub Account,
         isolated from the application, scalable via ASG
```

**Concepts covered:** GWLB, GENEVE protocol, VPC Ingress Routing, Centralized Security Hub, transparent appliance

---

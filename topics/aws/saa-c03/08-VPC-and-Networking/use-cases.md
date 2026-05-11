# Use Cases — Module 07: VPC and Networking

## Case 1: Multi-Tier VPC with Public and Private Subnets

**Scenario:** 3-tier web application: Web (public), App (private), DB (isolated private).

**Architecture:**
```
VPC: 10.0.0.0/16
  │
  ├── Public Subnet us-east-1a (10.0.1.0/24)
  │     ├── ALB (Internet-facing)
  │     └── NAT Gateway (1a) ← route to Internet Gateway
  │
  ├── Public Subnet us-east-1b (10.0.2.0/24)
  │     ├── ALB (second AZ)
  │     └── NAT Gateway (1b)
  │
  ├── Private App Subnet us-east-1a (10.0.10.0/24)
  │     └── EC2 App Servers → route 0.0.0.0/0 → NAT GW (1a)
  │
  ├── Private App Subnet us-east-1b (10.0.11.0/24)
  │     └── EC2 App Servers → route 0.0.0.0/0 → NAT GW (1b)
  │
  ├── DB Subnet us-east-1a (10.0.20.0/24)
  │     └── RDS Primary (no outbound internet route)
  │
  └── DB Subnet us-east-1b (10.0.21.0/24)
        └── RDS Standby (Multi-AZ)

VPC Endpoints:
  Gateway Endpoint: S3 and DynamoDB → added to private route tables
  Interface Endpoint: Secrets Manager, CloudWatch (for private subnet)
```

---

## Case 2: Hybrid Connectivity with Direct Connect + VPN Backup

**Scenario:** Company with on-premises datacenter needs high-speed private connectivity to AWS with automatic failover.

**Architecture:**
```
                    Direct Connect (10 Gbps) ← primary
On-Premises ──────────────────────────────────── AWS (VGW)
                                │                    │
                                │                    └── VPC (Private VIF)
                    Site-to-Site VPN ← backup via internet
                    (automatic failover via BGP)

DX Gateway:
  On-premises → DX Connection → DX Gateway → VGW (VPC us-east-1)
                                           → VGW (VPC us-west-2)
  [A single DX accesses multiple VPCs in multiple regions]
```

**BGP failover configuration:**
- DX uses shorter BGP AS Path prepending (preferred)
- VPN uses longer AS Path (used only if DX goes down)
- BFD (Bidirectional Forwarding Detection) detects failures in sub-second

---

## Case 3: Connecting 50 VPCs with Transit Gateway

**Scenario:** Company with 50 VPCs (dev, staging, prod per service) + on-premises VPN. Requirement: Prod VPCs do not communicate with Dev.

**Architecture with TGW Route Tables:**
```
Transit Gateway
  ├── Attachment: VPC-Prod-1 → Route Table: PROD
  ├── Attachment: VPC-Prod-2 → Route Table: PROD
  ├── Attachment: VPC-Dev-1  → Route Table: DEV
  ├── Attachment: VPC-Dev-2  → Route Table: DEV
  ├── Attachment: VPC-Shared → Route Table: SHARED (propagated to PROD and DEV)
  └── Attachment: VPN (on-prem) → Route Table: HYBRID

Route Table PROD: routes to VPC-Prod-* and VPC-Shared
Route Table DEV:  routes to VPC-Dev-* and VPC-Shared
[No cross routes → Prod and Dev automatically isolated]
```

---

## Case 4: SaaS Service Exposure via PrivateLink

**Scenario:** Company A wants to sell an API to Company B without using the public internet and without VPC Peering (to avoid CIDR conflicts).

**Architecture:**
```
Company A (Provider)                    Company B (Consumer)
  VPC: 10.0.0.0/16                        VPC: 10.0.0.0/16 (same CIDR is ok!)
    └── NLB (Service Endpoint)                └── Interface VPC Endpoint
          └── API Service (EC2/ECS)                 └── DNS: api.xxxxx.vpce.amazonaws.com
                                                          → Private IP in Company B's VPC
Endpoint Service:
  com.amazonaws.vpce.us-east-1.xxxxxxxx
  [Company A accepts the connection; Company B creates the Interface Endpoint]
```

**PrivateLink vs VPC Peering:**
- PrivateLink: only the specific service is accessible; unidirectional traffic (consumer → provider)
- No CIDR conflict possible: each company uses its own IP space

---

## Case 5: VPC Flow Logs for Security Analysis

**Scenario:** Security team needs to investigate suspicious traffic and detect communication with malicious IPs.

**Architecture:**
```
VPC Flow Logs → CloudWatch Log Group "/vpc/flow-logs"
                    └── CloudWatch Insights Queries:
                          - By IP: fields srcAddr | filter srcAddr like "1.2.3.4"
                          - REJECT analysis: filter action = "REJECT" | stats count by dstPort
                          - Top talkers: stats sum(bytes) by srcAddr | sort by sum desc

VPC Flow Logs → S3 Bucket (for historical analysis)
    └── Amazon Athena → SQL queries over date-partitioned logs
          └── QuickSight → Security dashboards

GuardDuty: uses VPC Flow Logs + DNS Logs automatically for ML-based threat detection
```

**Typical analysis with Athena:**
```sql
SELECT srcaddr, dstaddr, dstport, action, sum(bytes) as bytes
FROM vpc_flow_logs
WHERE action = 'REJECT' AND day >= '2024-01-01'
GROUP BY 1, 2, 3, 4
ORDER BY bytes DESC LIMIT 10
```

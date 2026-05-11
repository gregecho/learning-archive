# Real Use Cases — Well-Architected Framework (Module 26)

## Case 1 — Well-Architected Review of a Growing Startup

**Context:** Healthtech startup with 150K active users grew from 5 to 150 employees in 2 years. Original architecture was built quickly and never reviewed. Investors require a technical maturity report before the next funding round.

**Well-Architected Review Process:**
```
SETUP:
AWS Well-Architected Tool (enabled in console)
├── Create Workload: "Main Healthtech Platform"
├── Define: owner, environment, technologies
└── Invite APN partner (optional, for facilitated review)

PILLAR REVIEW (interviews with teams):

Pillar 1 — Operational Excellence:
├── Question: "Do you use IaC for all resources?"
│   Answer: "No, many resources created manually in console"
│   → HIGH RISK: Create Terraform/CDK for all resources
└── Question: "Do you practice runbooks for common operations?"
    Answer: "We only have outdated Word documents"
    → MEDIUM RISK: Create runbooks in SSM + playbooks

Pillar 2 — Security:
├── "Root credentials used regularly?" → YES → CRITICAL
├── "MFA enabled for all users?" → NO → HIGH
└── "Patient data encrypted at rest?" → PARTIALLY → HIGH

Pillar 3 — Reliability:
├── "RDS has Multi-AZ?" → NO → HIGH
├── "Auto Scaling configured?" → NO → HIGH
└── "DR tested?" → NEVER → HIGH

Pillar 4 — Performance:
├── "Cache implemented?" → NO → MEDIUM
└── "p99 latency metrics monitored?" → NO → MEDIUM

Pillar 5 — Cost Optimization:
├── "Idle instances?" → 40% with CPU < 5% → HIGH
└── "Reserved Instances for stable workloads?" → NO → MEDIUM

Pillar 6 — Sustainability:
└── "Regions chosen consider % of renewable energy?" → NO → LOW
```

**Prioritized Remediation Plan:**
| Priority | Item | Pillar | Effort |
|-----------|------|-------|---------|
| CRITICAL | Disable root usage, enable MFA | Security | 1 day |
| CRITICAL | Enable RDS Multi-AZ | Reliability | 4h |
| HIGH | Migrate resources to IaC | Op. Excellence | 3 weeks |
| HIGH | Encrypt PHI data (KMS) | Security | 1 week |
| HIGH | Auto Scaling for EC2 | Reliability | 2 days |
| MEDIUM | Implement ElastiCache | Performance | 3 days |
| MEDIUM | Reserved Instances (1 year) | Cost | 1 hour |

---

## Case 2 — Multi-Region DR Implementation

**Context:** Digital bank needs to guarantee continuity of operations even in case of complete failure of an AWS region. Regulation requires RPO <= 15 minutes and RTO <= 1 hour.

**DR Strategy Analysis:**

| Strategy | RPO | RTO | Cost/month | Adequate? |
|------------|-----|-----|-----------|----------|
| Backup & Restore | Hours | 24h | $1K | NO - RTO not met |
| Pilot Light | 15 min | 1-2h | $5K | Marginally meets RTO |
| Warm Standby | 5 min | 15 min | $25K | YES |
| Active-Active | ~0 | ~0 | $60K | YES Overkill (cost) |

**Chosen Warm Standby Architecture:**
```
PRIMARY REGION (us-east-1):
ALB → EC2 Auto Scaling (min:4, max:20)
         └── Aurora MySQL (multi-AZ, writer)
         └── ElastiCache Redis (cluster mode)
Route 53 Health Check → ALB us-east-1

SECONDARY REGION (us-west-2) — Warm Standby:
ALB → EC2 Auto Scaling (min:1, max:20) ← always-on instances
         └── Aurora Global Database (read replica us-west-2)
         └── ElastiCache Redis (small standby)
Route 53 Health Check → ALB us-west-2

REPLICATION:
Aurora Global Database → lag < 1s between regions
S3 Cross-Region Replication (user files)
DynamoDB Global Tables (session data)

AUTOMATIC FAILOVER:
Route 53 Failover Policy:
├── Primary: ALB us-east-1 (health check every 10s)
└── Secondary: ALB us-west-2 (activated automatically if primary fails)

Recovery Steps (RTO: 15-30 min):
1. Route 53 detects failure (30-60s)
2. DNS propagates to us-west-2 (30-60s) 
3. Aurora Global: promote secondary to writer (< 1 min)
4. ASG us-west-2: scale out to full capacity (5-10 min)
5. App fully restored (~15 min total)
```

---

## Case 3 — Cost Optimization: From $80K to $35K/month

**Context:** B2B SaaS with predictable workload (intense usage 8am-6pm, low at night and weekends) was paying $80K/month. Audit identified significant opportunities.

**Before Analysis (problems identified):**
```
ORIGINAL INFRA:
50x EC2 m5.xlarge On-Demand (24/7): $5,400/month
5x RDS db.r5.2xlarge On-Demand: $6,000/month
10x NAT Gateways (excessive redundancy): $4,500/month
S3: 200 TB in Standard (rarely accessed data after 30 days): $4,600/month
EBS: 500 gp2 volumes not in use: $2,500/month
Data Transfer: $8,000/month (processing in multiple regions)
CloudFront not used (direct traffic to EC2): $0 → $8K potential savings
```

**Optimization Plan:**
```
ACTION 1 — Reserved Instances EC2 (1 year):
Before: 50 x m5.xlarge On-Demand = $10,800/month
After: 30 x m5.xlarge Reserved (1 yr, no upfront) = $4,800/month
        20 x m5.xlarge Spot (fault-tolerant tasks) = $1,200/month
Savings: $4,800/month

ACTION 2 — Savings Plans RDS:
Before: 5 x db.r5.2xlarge On-Demand = $6,000/month  
After: Compute Savings Plans (1 yr) + right-size db.r5.xlarge = $2,800/month
Savings: $3,200/month

ACTION 3 — S3 Lifecycle Policies:
Before: 200 TB all in S3 Standard = $4,600/month
After:
  0-30 days: Standard ($0.023/GB) = $460/month
  30-90 days: Standard-IA ($0.0125/GB) = $250/month
  > 90 days: Glacier Flexible ($0.004/GB) = $820/month
Savings: $3,070/month

ACTION 4 — Consolidate NAT Gateways:
Before: 10 NAT GWs x $0.045/h = $4,500/month + data
After: 2 NAT GWs (1 per AZ in use) = $900/month
Savings: $3,600/month

ACTION 5 — Clean up unused EBS:
Before: 500 unattached gp2 volumes = $2,500/month
After: Lambda automation + AWS Config rule = $0
Savings: $2,500/month

RESULT:
Before: $80,000/month
After: $35,000/month
Savings: $45,000/month (56%)
```

---

## Case 4 — High Availability Architecture for Multi-AZ E-commerce

**Context:** Online retailer expects $90 million in sales during Black Friday. One hour of downtime = ~$500K in lost revenue. They need fault-tolerant architecture.

**Resilient Multi-AZ Architecture:**
```
                    Route 53 (Health Checks)
                           │
                    CloudFront (global CDN)
                           │
                    WAF + Shield Advanced
                           │
                    ALB (Multi-AZ automatic)
                    ├─────────────────────────┐
                    │                         │
              AZ us-east-1a             AZ us-east-1b
              EC2 Auto Scaling          EC2 Auto Scaling
              (min:10, des:20, max:50)  (min:10, des:20, max:50)
                    │                         │
              ElastiCache Redis         ElastiCache Redis
              (node cache AZ-a)         (node cache AZ-b)
                    │                         │
              Aurora MySQL             Aurora MySQL  
              (Writer)                 (Reader — automatic failover)

S3 + CloudFront (static assets — images, CSS, JS)
SQS → Lambda (async order processing — decouples from main flow)
EventBridge → Lambda (real-time inventory monitoring)

Auto Scaling Policies:
├── Target Tracking: CPU 60% → scale
├── Step Scaling: SQS > 500 msgs → +5 EC2
└── Schedule: 8am-12am on BF = min:20

Circuit Breaker Pattern:
└── If external payment fails: accept order + process async
    → Better UX than 500 error
```

---

## Case 5 — Sustainability: Reducing Workload Carbon Footprint

**Context:** Tech company with ESG commitment needs to quantify and reduce carbon emissions from AWS workloads. Goal: 30% reduction in 12 months.

**Analysis with Customer Carbon Footprint Tool:**
```
DIAGNOSIS (AWS Console → Billing → Carbon Footprint):
Region us-east-1: 45% of emissions (datacenter coal-heavy)
Idle instances (CPU < 5%): 30% of the fleet
On-Demand vs Serverless: 70% EC2, 30% serverless

SUSTAINABILITY ACTIONS:

1. Migrate workloads to regions with more renewable energy:
   us-east-1 (43% renewable) → eu-west-1 Ireland (96% renewable)
   us-east-1 → us-west-2 Oregon (62% renewable)
   Impact: direct reduction in carbon intensity

2. Serverless > EC2 (resources used only when needed):
   API Gateway + Lambda: zero consumption when no traffic
   EC2 24/7: consumes even when idle
   
3. Graviton3 instead of x86:
   Graviton3 (40% more energy efficient than x86)
   c7g vs c6i: same cost, lower emissions

4. Aggressive Auto Scaling (scale to zero where possible):
   Schedule: shut down dev/staging at night and weekends
   70% of dev instances idle 16h/day = unnecessary waste

5. S3 Intelligent-Tiering (less reprocessing of cold data):
   Cold data in Glacier = lower active storage energy

ESTIMATED RESULT:
Before: 100 tons CO2e/year
After: 65 tons CO2e/year
Reduction: 35% (exceeds 30% target)
Financial ROI: -$15K/month in operational costs (Graviton is cheaper)
```

# Use Cases — EC2 Compute

## Case 1: HPC Cluster with Placement Group and EFA

**Context:**  
An engineering company runs CFD (Computational Fluid Dynamics) simulations that require ultra-fast MPI communication between instances. Any network latency above 1ms significantly degrades performance.

**Architecture:**

```
Cluster Placement Group (same AZ, same rack)
┌──────────────────────────────────────────────────────┐
│                                                      │
│  hpc6a.48xlarge  ←──EFA──→  hpc6a.48xlarge           │
│       │                          │                   │
│       └──────────────────────────┘                   │
│              10 Gbps / <100μs latency                │
│                                                      │
│  hpc6a.48xlarge  ←──EFA──→  hpc6a.48xlarge           │
│                                                      │
└──────────────────────────────────────────────────────┘
     ↑
EFA (Elastic Fabric Adapter) = RDMA-capable network interface
Bypasses the kernel networking stack for minimal latency

Storage: Lustre (FSx) mounted on all instances
Orchestration: AWS ParallelCluster
```

**Placement Group Configuration:**
```bash
aws ec2 create-placement-group \
  --group-name hpc-cluster \
  --strategy cluster

aws ec2 run-instances \
  --instance-type hpc6a.48xlarge \
  --placement "GroupName=hpc-cluster" \
  --network-interfaces '[{"InterfaceType":"efa"}]' \
  --count 8
```

**Trade-off:** Cluster PG → all in the same rack → if the rack fails, all instances go down. For HPC, latency takes priority over availability.

**Concepts covered:** Cluster Placement Group, EFA, HPC, hpc6a instances

---

## Case 2: Batch Processing with Spot Fleet and Fault Tolerance

**Context:**  
A data science company runs machine learning jobs that take between 2 and 6 hours. Cost is critical. Jobs can be restarted from a checkpoint if the instance is interrupted.

**Architecture:**

```
SQS Queue (1000 jobs)
       │
       ▼
Spot Fleet (ASG with Mixed Instance Policy)
┌─────────────────────────────────────────────────────┐
│  Strategy: capacityOptimized                        │
│  Types: m5.4xlarge, m5a.4xlarge, m4.4xlarge         │
│         c5.4xlarge, r5.2xlarge                      │
│                                                     │
│  [m5.4xl] [c5.4xl] [m5a.4xl] [r5.2xl] [m5.4xl]    │
│     ↑         ↑        ↑                            │
│  Job.py  Job.py   Job.py                            │
│  (SQS msg visibility timeout = job duration + 10%)  │
└─────────────────────────────────────────────────────┘
       │
       ▼
S3 (Checkpoint every hour + final result)

If instance is interrupted:
  → Job returns to SQS queue (visibility timeout expires)
  → Another instance picks up the job
  → Resumes from last checkpoint in S3
```

**ASG Configuration with Mixed Instance:**
```json
{
  "MixedInstancesPolicy": {
    "InstancesDistribution": {
      "OnDemandPercentageAboveBaseCapacity": 0,
      "SpotAllocationStrategy": "capacity-optimized"
    },
    "LaunchTemplate": {
      "Overrides": [
        {"InstanceType": "m5.4xlarge"},
        {"InstanceType": "m5a.4xlarge"},
        {"InstanceType": "m4.4xlarge"},
        {"InstanceType": "c5.4xlarge"}
      ]
    }
  }
}
```

**Concepts covered:** Spot Fleet, capacityOptimized, checkpointing, SQS for job distribution, interruption tolerance

---

## Case 3: OLTP Database Server with io2 and Placement Group

**Context:**  
A company migrates an Oracle database to EC2. The database requires 50,000 guaranteed IOPS, backup via snapshots, and Oracle BYO-L licensing (per socket).

**Architecture:**

```
Dedicated Host (r6i.16xlarge)
  ├── Oracle License: 2 sockets × 16 cores = 32 cores BYO-L
  ├── RAM: 512 GB (memory-optimized instance)
  └── Storage:
        ├── EBS io2 Block Express (500 GB, 50,000 provisioned IOPS)
        │     └── Multi-attach for standby? → Not in this case
        └── EBS gp3 (redo/archive logs: 2 TB)

Backup:
  └── Automatic EBS Snapshots via Data Lifecycle Manager
        └── Retention: 7 days, schedule: 02:00 UTC
        └── Cross-region copy for DR

Monitoring:
  └── CloudWatch enhanced monitoring (1s granularity)
  └── CloudWatch Alarm → SNS → PagerDuty if IOPS > 45,000
```

**Why Dedicated Host vs Dedicated Instance:**
- Dedicated Host: socket/core visibility → required for Oracle license compliance
- Dedicated Instance: exclusive hardware but no socket counting → does not count for Oracle BYO-L

**Concepts covered:** io2 Block Express, Dedicated Host for BYO-L, EBS snapshots, enhanced monitoring

---

## Case 4: Web Environment with ASG, Spot and Launch Template

**Context:**  
An e-commerce company wants to reduce EC2 costs by 60% using Spot for stateless web instances (session in ElastiCache), maintaining an On-Demand base for minimum availability.

**Architecture:**

```
ALB (us-east-1)
  │
  ├── Target Group: Web-TG
  │
ASG (mixed instances policy)
├── Base: 2 On-Demand (m5.large) — guaranteed minimum availability
├── Spot: up to 10 instances (m5.large, m5a.large, m4.large, t3.xlarge)
│     └── Strategy: capacityOptimized
│
├── Launch Template v2:
│     ├── AMI: ami-prod-web (golden AMI)
│     ├── UserData: starts app, registers in service discovery
│     ├── Spot interruption handler (SSM parameter)
│     └── IMDSv2: HttpTokens=required
│
├── Scale-out: CPU > 70% for 2 minutes → +2 instances
├── Scale-in: CPU < 30% for 5 minutes → -1 instance
└── Scheduled: +4 instances at 6pm-10pm (peak hours)

ElastiCache Redis
  └── User sessions (TTL 30min)
  └── When Spot instance is interrupted, session persists in Redis
```

**Concepts covered:** ASG Mixed Instances, Spot with On-Demand base, Launch Template, stateless app, Target Tracking + Scheduled scaling

---

## Case 5: Hibernate for Stateful Analysis Workloads

**Context:**  
A data scientist runs Jupyter notebooks on EC2 with large datasets loaded in RAM (150 GB). At the end of the day, she shuts down the instance but wants to resume exactly where she left off the next day without reloading data.

**Solution with Hibernate:**

```
r6i.4xlarge (128 vCPU, 128 GB RAM)
  ├── EBS root (gp3, 500 GB) — encrypted with CMK ⚠️
  │     └── Stores: OS + data + RAM contents when hibernating
  └── EBS data (gp3, 2 TB) — datasets

Flow:
  18:00: hibernate-instance
    → RAM (150 GB) written to EBS root
    → Instance stops billing (only EBS charged)
  08:00: start-instance
    → RAM restored from EBS root
    → Jupyter continues exactly where it left off
    → In-memory datasets preserved

Hibernate requirements:
  ✅ RAM ≤ 150 GB (hibernate limit)
  ✅ Root EBS encrypted
  ✅ Root EBS size ≥ RAM size
  ✅ Instance cannot be on Instance Store
  ✅ Maximum duration: 60 days hibernated
```

**Cost comparison:**
- Stop: stops EC2 billing, but loses RAM data → reloading = hours of data scientist time
- Hibernate: stops EC2 billing, RAM preserved → productivity maintained

**Concepts covered:** EC2 Hibernate, EBS encryption requirement, cost optimization, memory-optimized instances

---

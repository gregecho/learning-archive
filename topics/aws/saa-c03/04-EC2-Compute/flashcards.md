# Flashcards — EC2 Compute

> Review one card at a time. Try to answer before revealing the response.

---

**Q:** What are the main EC2 instance families and their use cases?  
**A:** M (general purpose, balanced CPU/RAM), C (compute-optimized: HPC, batch, ML inference), R (memory-optimized: in-memory DB, cache), I (storage-optimized: NVMe local, high IOPS DB), P/G (GPU: ML training, rendering), T (burstable: apps that rarely need peak CPU but have a low baseline).

---

**Q:** What is the CPU credits mechanism in T instances?  
**A:** T instances accumulate credits when CPU is below baseline and spend them when above. T3/T3a with Unlimited mode can use CPU beyond accumulated credits by paying for extra credits. In Standard mode with zero credits, CPU is throttled to baseline.

---

**Q:** What is the difference between On-Demand and Reserved Instance?  
**A:** On-Demand: pay per hour/second, no commitment, more expensive. Reserved Instance: 1 or 3 year commitment, up to 72% discount. Standard RI cannot change type, region, or OS. Convertible RI can change attributes, lower discount (~54%). Both can be paid upfront, partial, or monthly.

---

**Q:** What is the difference between Compute Savings Plans and EC2 Instance Savings Plans?  
**A:** Compute Savings Plans: up to 66% discount, applies to any family, region, OS and size, also covers Lambda and Fargate. EC2 Instance Savings Plans: up to 72%, locked to specific family + region (e.g., m5 in us-east-1), more discount, less flexibility.

---

**Q:** What is a Spot Instance and when to use it?  
**A:** Spot Instances use AWS spare capacity at up to 90% discount. They can be interrupted with 2 minutes notice. Ideal for: fault-tolerant batch jobs, distributed ML training, rendering, testing. Do NOT use for: primary database, stateful web sessions.

---

**Q:** What is Spot Fleet and how does it work?  
**A:** Spot Fleet manages a set of Spot instances (and optionally On-Demand). You define a pool of types/regions and the strategy: `lowestPrice` (chooses the cheapest), `capacityOptimized` (chooses the pool with most available capacity — recommended to reduce interruptions), `diversified` (distributes across all pools).

---

**Q:** What is the difference between Dedicated Host and Dedicated Instance?  
**A:** Dedicated Host: you rent a specific physical server, have socket/core visibility, can use BYO-L licenses (per socket/core such as SQL Server, Windows Server). Dedicated Instance: instance on dedicated hardware for your account but without physical host control. Host is more expensive but required for license compliance.

---

**Q:** What is IMDSv2 and why is it preferred over IMDSv1?  
**A:** IMDSv2 (Instance Metadata Service v2) uses a token-based model: first make a PUT to obtain a token with TTL, then use the token in the `X-aws-ec2-metadata-token` header. Protects against SSRF attacks where a process on the instance could capture metadata without the token. To disable IMDSv1, configure `HttpTokens: required`.

---

**Q:** What is the difference between gp2 and gp3 in EBS?  
**A:** gp2: IOPS tied to size (3 IOPS/GB, max 16,000), burst. gp3: baseline of 3,000 IOPS and 125 MB/s regardless of size, can independently provision up to 16,000 IOPS and 1,000 MB/s. gp3 is cheaper (~20%) and more flexible — use by default.

---

**Q:** When to use io1/io2 vs gp3?  
**A:** io2: up to 64,000 IOPS per volume, io2 Block Express up to 256,000 IOPS, 99.999% durability (vs 99.8-99.9% for gp). Use for high-performance databases (Oracle, SQL Server, workloads needing >16,000 guaranteed IOPS). io1: previous version, 99.8% durability.

---

**Q:** What is Instance Store and what are its characteristics?  
**A:** Ephemeral NVMe storage directly on the physical host of the instance. Very high IOPS (e.g., i3.large has ~100K IOPS). Data LOST on: stop, terminate, or hardware failure. Persists on: restart. Ideal for high-performance cache, temporary buffer, scratch disk.

---

**Q:** What are the three types of Placement Groups?  
**A:** Cluster: all instances in the same rack and AZ, <1ms latency between instances, ideal for HPC and MPI. Spread: each instance on a separate rack, max 7 per AZ, for critical high availability. Partition: groups of instances per partition (each partition = separate rack), up to 7 partitions per AZ, for HDFS/Cassandra/Kafka.

---

**Q:** What happens to an EC2 instance when we Stop it (vs Hibernate)?  
**A:** Stop: instance stops, RAM is lost, EBS root preserved, charged for EBS not instance. Hibernate: RAM is written to EBS root volume (must have space and be encrypted), on start the OS resumes from where it stopped. Hibernate limit: 60 days.

---

**Q:** What are AMIs and what are the virtualization categories?  
**A:** Amazon Machine Image is an instance template (OS, data, configurations). HVM (Hardware Virtual Machine): full hardware emulation — the only type supported by modern instances. PV (Paravirtual): legacy. AMIs can be shared between accounts, copied between regions. To copy an unencrypted AMI to encrypted, specify a CMK in the copy.

---

**Q:** What is EC2 User Data?  
**A:** Script (shell or cloud-init) executed once on the first boot of the instance with root privileges. Accessible at `http://169.254.169.254/latest/user-data`. Useful for installing software, configuring applications. Not re-executed on reboots (unless explicitly configured).

---

**Q:** How to query EC2 instance metadata from within it using IMDSv2?  
**A:**
```bash
TOKEN=$(curl -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 21600")
curl -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/instance-id
```
Without the token (IMDSv1), just: `curl http://169.254.169.254/latest/meta-data/instance-id`

---

**Q:** What is Capacity Reservation and when to use it?  
**A:** Reserves capacity in a specific AZ with no price discount (pay On-Demand). Guarantees capacity will be available when needed. Can combine with Savings Plans or Regional RI for discount. Useful for DR, compliance, or critical workloads that cannot be left without capacity.

---

**Q:** What is the maximum IOPS of io2 Block Express and st1 vs sc1?  
**A:** io2 Block Express: up to 256,000 IOPS, 4,000 MB/s. st1 (throughput): 40 MB/s per TB baseline, 250 MB/s per TB burst, max 500 MB/s — sequential access (logs, Kafka, data warehouse). sc1 (cold HDD): 12 MB/s per TB baseline, cheaper — rarely accessed data.

---

**Q:** What is an Elastic IP and when should it be avoided?  
**A:** Elastic IP is a static IPv4 that can be associated/reassociated to instances or ENIs. Charged when NOT in use ($0.005/hour). Avoid in scalable architectures — use DNS (Route 53) instead of depending on a fixed IP. Use only when a client needs an IP on an allowlist.

---

**Q:** What is AWS Systems Manager Session Manager?  
**A:** Allows interactive access to EC2 instances without opening port 22 (SSH) or 3389 (RDP). The instance needs the SSM Agent installed and an IAM role with `AmazonSSMManagedInstanceCore`. Access via Console or CLI. Audited by CloudTrail and sessions can be logged to S3/CloudWatch Logs.

---

# Questions — EC2 Compute

## Question 1
**Domain:** Design High-Performing Architectures  
**Difficulty:** Medium

A company needs to run a machine learning job with GPU-intensive matrix calculations. Which EC2 instance family is most suitable?

- A) M5 — General Purpose
- B) R6g — Memory Optimized
- C) P4de — Accelerated Computing
- D) T3 — Burstable

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

P instances are accelerated with NVIDIA GPUs, designed for machine learning training and HPC. The other families do not have GPUs. M5 is balanced CPU/RAM without GPU. R6g is Memory Optimized for in-memory databases. T3 is burstable for intermittent light workloads.

**Key concept:** P family (GPU) for ML/HPC
</details>

## Question 2
**Domain:** Design Cost-Optimized Architectures  
**Difficulty:** Medium

An analytics team runs batch data processing for 6 hours daily, with tolerable failures and the ability to restart from a checkpoint. Which purchasing model offers the greatest discount?

- A) On-Demand
- B) Reserved Instance Standard 1 year
- C) Spot Instances
- D) Dedicated Host

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

Spot Instances offer up to 90% discount for interruption-tolerant workloads. The batch workload with checkpointing exactly fits this profile: it can be interrupted and resumed. Reserved and Dedicated Host are for continuous or compliance workloads. On-Demand is more expensive without commitment.

**Key concept:** Spot Instances for interruption-tolerant batch
</details>

## Question 3
**Domain:** Design Cost-Optimized Architectures  
**Difficulty:** Medium

A company uses an ERP database that runs 24/7 without interruptions for two years and needs to stay active for the next 3 years. Which purchasing model offers the greatest discount with the least need for instance type changes?

- A) Spot Instances
- B) On-Demand
- C) Reserved Instance Standard 3 years All Upfront
- D) Savings Plans Compute 1 year

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

Standard Reserved Instance 3 years All Upfront offers the maximum possible discount (~72%). The workload is stable and predictable, with no need for type flexibility. All Upfront maximizes the discount compared to Partial or No Upfront. Savings Plans would be suitable if the company wanted type/region flexibility, but have a slightly lower discount.

**Key concept:** Standard RI 3 years All Upfront for stable long-term workload
</details>

## Question 4
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Medium

An EC2 instance running an API needs to retrieve the instance ID, region, and associated role ARN. Where can it obtain this information securely without accessing external services?

- A) User Data
- B) Parameter Store
- C) Instance Metadata Service (IMDSv2)
- D) Secrets Manager

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

IMDS provides instance information at 169.254.169.254. With IMDSv2 (session-oriented), you first obtain a token and use it in subsequent requests. This includes instance-id, region, ami-id, IAM role credentials, and much more. User Data only executes a script on initialization. Parameter Store and Secrets Manager store external data, not instance metadata.

**Key concept:** IMDSv2 for instance self-discovery
</details>

## Question 5
**Domain:** Design High-Performing Architectures  
**Difficulty:** Medium

An HPC application distributes calculations across nodes that need sub-millisecond network latency and 100 Gbps throughput between them. Which EC2 configuration optimizes this?

- A) Spread Placement Group across multiple AZs
- B) Partition Placement Group in the same AZ
- C) Cluster Placement Group in the same AZ with Enhanced Networking instances
- D) Instances in different AZs without placement group

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

Cluster Placement Group places instances physically close, minimizing latency and maximizing bandwidth between them (up to 10 Gbps with Enhanced Networking / EFA instances). Must be in the same AZ. Spread PG maximizes availability but disperses physically, degrading inter-node latency. Partition PG differentiates racks but does not minimize intra-group latency. Different AZs introduce regional network latency.

**Key concept:** Cluster Placement Group for low-latency HPC
</details>

## Question 6
**Domain:** Design Resilient Architectures  
**Difficulty:** Easy

A critical application uses EC2 with an in-memory database. The team needs to ensure that if the instance is replaced, the database returns with the previous state quickly instead of reloading everything from scratch. Which EC2 feature solves this?

- A) Instance Store
- B) Hibernation
- C) EC2 Auto Recovery
- D) Elastic IP

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

Hibernation saves the RAM contents to the EBS root volume, allowing the instance to resume with the exact state. The in-memory database would be at the same point upon waking from hibernation. Instance Store loses data on stop. Auto Recovery replaces the instance on new hardware but does not preserve memory state. Elastic IP is about fixed IP addresses.

**Key concept:** Hibernation saves RAM to EBS for state resumption
</details>

## Question 7
**Domain:** Design High-Performing Architectures  
**Difficulty:** Medium

A video streaming system needs EBS volumes with 40,000 consistent IOPS, very low latency, and 99.999% durability to store video chunks during processing. Which EBS type should be used?

- A) gp3
- B) st1
- C) io2 Block Express
- D) sc1

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

io2 Block Express offers up to 256,000 IOPS with 99.999% durability and consistent sub-millisecond latency. For 40,000 IOPS, gp3 only reaches 16,000. st1 and sc1 are HDDs with very low IOPS, unsuitable for high-performance streaming.

**Key concept:** io2 Block Express for very high IOPS and maximum durability
</details>

## Question 8
**Domain:** Design Cost-Optimized Architectures  
**Difficulty:** Medium

A company uses T3 instances to host monitoring microservices that recently started performing continuous intensive calculations. Customers are complaining about slowness. What is the most likely cause?

- A) The T3 instance has no Elastic IP
- B) Burstable CPU credits have been exhausted and the instance operates at baseline
- C) The EBS volume is full
- D) Instance metadata is disabled

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

T3 instances accumulate CPU credits when below baseline and consume them in bursts. Continuously intensive workloads exhaust the credits and performance drops to baseline, which can be very low (e.g., t3.micro has a 10% vCPU baseline). The solution is to migrate to a non-burst family (M, C) or enable T3 Unlimited with additional cost.

**Key concept:** T3 burst credits exhausted in continuous workload
</details>

## Question 9
**Domain:** Design Resilient Architectures  
**Difficulty:** Hard

A company needs to deploy a Cassandra database on 18 EC2 instances, organized so that rack failures affect the smallest possible number of nodes, but Cassandra can use partition information for intelligent replication. Which placement group should be used?

- A) Cluster Placement Group
- B) Spread Placement Group
- C) Partition Placement Group
- D) No placement group, using multiple AZs

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

Partition Placement Group was designed exactly for systems like Cassandra, HDFS, and Kafka. Each partition represents a distinct rack. Cassandra can use the partition as a virtual availability zone for replication awareness. With 18 instances across 6 partitions (3 per partition), a rack failure affects only 3 nodes. Spread limits to 7 instances/AZ. Cluster is unsuitable for Cassandra because it concentrates hardware.

**Key concept:** Partition PG for distributed databases with rack awareness
</details>

## Question 10
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Medium

A company needs production EC2 instances to be accessible for troubleshooting without opening port 22 to the world and without a bastion host. Which solution eliminates the exposed SSH attack vector?

- A) Open port 22 in the security group only for the administrator's IP
- B) Use AWS Systems Manager Session Manager for portless access
- C) Configure site-to-site VPN for the administrator's laptop
- D) Create an EC2 Key Pair and share it among admins

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

Session Manager allows access to the instance shell via the AWS Console or CLI without opening any inbound ports in the security group, without key pairs, and with automatic auditing in CloudTrail and session logging in S3/CloudWatch. Alternative A still exposes port 22. Alternative C partially resolves it but does not eliminate SSH. Alternative D shares a key pair, a terrible practice.

**Key concept:** Session Manager for access without open ports
</details>

## Question 11
**Domain:** Design Cost-Optimized Architectures  
**Difficulty:** Medium

A startup uses multiple EC2 types and also Lambda and Fargate. They want a single flexible discount plan that covers all of these compute services. What is the best option?

- A) Standard Reserved Instances for each instance type individually
- B) Compute Savings Plans covering EC2, Lambda, and Fargate
- C) EC2 Savings Plans restricted to family and region
- D) Dedicated Hosts with 3-year RI

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

Compute Savings Plans is the most flexible: applies discount to any EC2 type, family, region, OS, Lambda (above 0.5 GB), and Fargate, without specific type commitment. EC2 Savings Plans have a slightly higher discount but are restricted to family and region. Reserved Instances require specification by type. Dedicated Hosts serve a different purpose.

**Key concept:** Compute Savings Plans for flexible multi-service coverage
</details>

## Question 12
**Domain:** Design High-Performing Architectures  
**Difficulty:** Medium

A self-managed MySQL database on EC2 needs an EBS volume with high sequential throughput for binary log writes. Which EBS type offers the best cost-benefit for this access pattern?

- A) io2 Block Express
- B) gp3 with extra IOPS
- C) st1 — Throughput Optimized HDD
- D) sc1 — Cold HDD

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

st1 is optimized for large-block sequential access with throughput up to 500 MBps and is much cheaper than SSD for this use case. Binary logs are large sequential writes — an ideal profile for st1. io2 would be wasteful for sequential logging. sc1 is even slower and for cold data. gp3 is a general-purpose SSD, good but more expensive and with lower throughput for massive sequential workloads.

**Key concept:** st1 for high-throughput sequential I/O at low cost
</details>

## Question 13
**Domain:** Design Resilient Architectures  
**Difficulty:** Easy

A company wants to copy an AMI that uses a customer-managed KMS CMK to another region. Which prerequisite is mandatory?

- A) The AMI must be public before the copy
- B) The destination account must have access to the original CMK or an equivalent CMK must be used in the copy
- C) The AMI needs to be decrypted before the copy
- D) It is not possible to copy encrypted AMIs between regions

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

When copying an encrypted AMI between regions, you must specify a CMK in the destination region. The AMI's EBS snapshots are re-encrypted with the destination region key. The requesting account needs permission on both the source CMK (to decrypt) and the destination CMK (to re-encrypt). It is not possible to copy without access to the keys, but alternative D is wrong because the copy is possible with the correct CMKs.

**Key concept:** Destination CMK required when copying encrypted AMI cross-region
</details>

## Question 14
**Domain:** Design Cost-Optimized Architectures  
**Difficulty:** Hard

A company has 100 On-Demand instances and wants to reduce costs. The usage pattern shows a constant load of 60 instances throughout the day with peaks of 40 additional during business hours. Which purchasing strategy best balances cost and availability?

- A) 100 Spot Instances
- B) 60 Reserved Instances for the base + 40 On-Demand or Spot for peaks
- C) 100 Reserved Instances Standard 3 years
- D) Savings Plans Compute covering only 20% of the commitment

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

The ideal architecture is to cover the consistent base with RI or Savings Plans (greater discount) and use On-Demand or Spot for the variable capacity. 100 Spot would be risky for a critical base load. 100 RI covering 40 instances that are sometimes idle wastes the commitment. Savings Plans with 20% commitment leaves 80% of the base at On-Demand rates.

**Key concept:** stable base with RI + burst with On-Demand/Spot
</details>

## Question 15
**Domain:** Design Resilient Architectures  
**Difficulty:** Medium

A production environment uses an EC2 instance as an application server. After a stop/start, the instance's public IP changed and existing connections failed. What is the most direct solution to ensure a permanent public IP?

- A) Enable Enhanced Networking
- B) Associate an Elastic IP with the instance
- C) Create a new AMI with an embedded fixed IP
- D) Migrate to an instance with Instance Store

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

Elastic IP is a static public IP that remains associated with the account even after stop/start or instance failure. It can be quickly remapped to a replacement instance in case of failure. Enhanced Networking is about network performance. AMI does not define IP. Instance Store has no relation to IP.

**Key concept:** Elastic IP for permanent public IP on EC2
</details>

---

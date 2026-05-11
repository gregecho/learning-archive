# Questions — Module 29: Practice Exams and Questions

> Exam study strategy

---

**About the practice exam questions**

This module's README.md contains the full Practice Exam 1 with 65 questions in SAA-C03 style. This file gathers complementary exam strategy questions and meta-questions about the exam format.

---

**1.** In the SAA-C03 exam, a question asks you to choose the "most cost-effective" solution. Which elimination approach should you use?

- A) Always choose the option with Lambda (serverless is always cheaper)
- B) Eliminate options with idle resources (always-on EC2, over-provisioned instances), then compare remaining costs
- C) Always choose Reserved Instances (highest discount)
- D) Choose the option with the fewest AWS services (fewer services = lower cost)

<details><summary>Answer</summary>

**B** — "Most cost-effective" varies by context: for intermittent workloads, Lambda/Fargate/Spot are cheaper. For stable 24/7 workloads, Reserved Instances. First eliminate: (1) over-provisioning, (2) idle resources, (3) unnecessary redundancy. Then compare remaining services by pricing model.

</details>

---

**2.** An exam question asks you to choose 2 correct answers from 5 options. What is the best strategy?

- A) Mark the first 2 options that seem correct
- B) Identify the 2 most obviously incorrect, eliminate, and from the 3 remaining choose the 2 most correct
- C) Mark as uncertain and come back later
- D) Look for keywords like "serverless" or "managed" in options

<details><summary>Answer</summary>

**B** — Elimination strategy: first remove clearly wrong options (wrong service for context, violates obvious security principle). From the remaining, choose the 2 that best meet ALL question requirements. In multiple-select questions, all correct options must be chosen to score.

</details>

---

**3.** The exam asks for a "highly available" architecture. What is the minimum criterion the answer must meet?

- A) Use the newest AWS service
- B) Have resources in at least 2 Availability Zones with automatic failover
- C) Use Reserved Instances in 3 regions
- D) Have daily data backup

<details><summary>Answer</summary>

**B** — High availability = tolerance to an AZ failure. Minimum: resources in 2+ AZs with automatic failover (ELB + multi-AZ ASG, RDS Multi-AZ, etc.). Backup is for recovery (not HA). Multi-region is for disaster recovery or global reach (different from simple HA).

</details>

---

**4.** A question describes an application that "sometimes has unpredictable traffic spikes" and needs a compute solution. Which service is the most likely answer?

- A) Fixed EC2 On-Demand
- B) EC2 Reserved Instances
- C) Lambda or ECS Fargate with Auto Scaling
- D) EC2 Spot Instances

<details><summary>Answer</summary>

**C** — "Unpredictable" and "spikes" = serverless/auto-scaling. Lambda scales to zero when no load and to thousands when spiking, without manual configuration. Fargate with metric-based ASG also works. Reserved Instances are for predictable load; Spot can be interrupted during spikes.

</details>

---

**5.** In the exam, when a question mentions "least change to existing application" (lift-and-shift), which category of answer is most likely?

- A) Lambda and DynamoDB (cloud-native serverless)
- B) EC2 + RDS (VM equivalent + relational database)
- C) EKS + S3 (containers + storage)
- D) CloudFormation + CodePipeline (automation)

<details><summary>Answer</summary>

**B** — "Least possible change" = lift-and-shift = EC2 (VM equivalent), RDS (managed database, same engine), ELB (load balancer). The application does not need to be rewritten. Lambda/DynamoDB require refactoring. EKS requires containerization. The question tests recognizing the "Rehost" pattern from the 7Rs.

</details>

---

**6.** What is the most important tip when reading an SAA-C03 exam question?

- A) Read the last sentence of the question first to understand what is being asked
- B) Identify all requirements (availability, cost, security, performance) explicitly mentioned before looking at the options
- C) Eliminate the longest options (generally unnecessary complexity)
- D) Always choose the option with the most managed service

<details><summary>Answer</summary>

**B** — Read the full scenario and note the explicit requirements (e.g., "RTO < 1 hour", "no custom code", "lowest cost"). Each requirement can eliminate options. Some questions have distractors that meet some requirements but violate others. Identifying ALL requirements before evaluating answers is the most effective strategy.

</details>

---

**7.** On exam day, how much time should you dedicate to the first pass through the 65 questions?

- A) Solve all questions meticulously on the first pass (no skipping)
- B) ~1.5 minutes per question on first pass (~97 min); mark difficult questions; use remaining time to review
- C) Skip the first 20 questions (usually harder)
- D) Answer the easiest ones first (last 30 questions)

<details><summary>Answer</summary>

**B** — Time management: 130 minutes / 65 questions = 2 min/question. Reserve ~97 min for first pass (~1.5 min/question). Questions you are confident about: answer and move on. Difficult questions: mark and skip. With the remaining 33 min, review the marked ones. Never get stuck on a single question for 10 minutes.

</details>

---

**8.** An exam question has the following options and asks for the "most secure" answer:
- A) Use hardcoded IAM access keys in application code
- B) Use IAM Role associated with EC2 instance profile
- C) Store access keys in EC2 environment variables
- D) Use a ~/.aws/credentials file on the server

<details><summary>Answer</summary>

**B** — IAM Role via Instance Profile: temporary credentials automatically rotated by STS; never exposed in code, env vars, or files. Hardcoded access keys (A), env vars (C), and credentials file (D) are all leakage risks. The general rule: never use long-lived credentials when IAM Roles are possible.

</details>

---

**9.** Which SAA-C03 exam domain has the highest weight?

- A) Design Resilient Architectures (26%)
- B) Design High-Performing Architectures (24%)
- C) Design Secure Applications (30%)
- D) Design Cost-Optimized Architectures (20%)

<details><summary>Answer</summary>

**C** — Design Secure Applications has 30% of the exam — it is the heaviest domain. Focus on: IAM (roles, policies, conditions), KMS, VPC security (SG vs NACL), S3 (Block Public Access, OAC, pre-signed), Cognito, Secrets Manager, GuardDuty, Shield, WAF. 30% of questions are about security.

</details>

---

**10.** What is the minimum passing score for SAA-C03?

- A) 65% (700/1000)
- B) 72% (720/1000)
- C) 75% (750/1000)
- D) 80% (800/1000)

<details><summary>Answer</summary>

**B** — Minimum score: **720/1000** (on a 100-1000 scale). It is not 72% of questions correct — the score uses a psychometric model (pruning questions don't score). In practice, you need to get roughly 43-47 of the 65 scored questions correct (there are unscored test questions that appear randomly).

</details>

---

**11.** A question describes: "the company needs a solution that processes data **in batch** once per day." Which service/combination is a candidate for the correct answer?

- A) Kinesis Data Streams + Lambda
- B) EventBridge Scheduler + Lambda (or ECS/Batch)
- C) SQS FIFO + Lambda
- D) Kinesis Data Firehose

<details><summary>Answer</summary>

**B** — "Once per day" = scheduled processing. EventBridge Scheduler (or Rule of type `schedule`) + Lambda/ECS Fargate/AWS Batch is the pattern. Kinesis is for continuous real-time streaming, not daily batch. AWS Batch is excellent for heavy computing batch jobs.

</details>

---

**12.** You're in the exam and a question asks you to choose between RDS Multi-AZ and Read Replicas. The requirement says "high availability for writes." What do you choose?

- A) Read Replicas (can be promoted to primary in case of failure)
- B) RDS Multi-AZ (automatic synchronous failover to standby; no write data loss)
- C) Both, with Read Replicas pointing to the Multi-AZ standby
- D) Aurora instead of standard RDS

<details><summary>Answer</summary>

**B** — Multi-AZ: **synchronous** replication to standby in another AZ. Automatic failover in 1-2 minutes. No loss of writes (synchronous). Read Replicas: **asynchronous** replication — may have lag; if primary fails, requires manual promotion (not automatic for RDS — only Aurora promotes automatically).

</details>

---

**13.** A question mentions "data transfer out cost." What is the architectural impact of this?

- A) Data transferred between AWS regions is free
- B) Upload to S3 is free; S3 → internet transfer has cost (~$0.09/GB); using CloudFront reduces transfer cost
- C) VPC Peering never has data transfer cost
- D) Lambda has no data transfer cost

<details><summary>Answer</summary>

**B** — Data transfer pricing: UPLOAD to AWS = free. Download from AWS to internet = ~$0.09/GB. CloudFront has lower cost per GB than direct S3 + includes edge caching. Intra-region transfer (same AZ) = generally free between services. AZ to AZ in same region = has cost ($0.01/GB). Cross-region = always has cost.

</details>

---

**14.** In the exam, when a question mentions a "startup with limited budget" needing high availability, which approach does the exam generally favor?

- A) Multi-region active-active for maximum HA
- B) Multi-AZ with smaller instances + Auto Scaling (HA without over-provisioning)
- C) On-Demand instances in a single AZ (cheapest)
- D) 3-year Reserved Instances immediately

<details><summary>Answer</summary>

**B** — The exam frequently tests: cost-effective high availability. Multi-AZ is sufficient for most HA cases. Smaller instances + Auto Scaling avoid expensive and unnecessary on-demand. Multi-region is for DR (different from HA) and costs much more. Reserve only after growth stabilizes.

</details>

---

**15.** What is the purpose of "unscored" questions in the SAA-C03 exam?

- A) There are no unscored questions in SAA-C03
- B) They are piloting questions (testing new questions for future exam versions), randomly distributed among the 65
- C) They are the 5 easiest questions to guarantee minimum score
- D) They are questions about recently announced new services

<details><summary>Answer</summary>

**B** — AWS includes "field trial" or "pre-operational" questions — new questions being tested for calibration. You don't know which are scored and which are not. Implication: do not skip any question (even those that seem very difficult may be unscored; even easy ones are scored). Answer all of them.

</details>

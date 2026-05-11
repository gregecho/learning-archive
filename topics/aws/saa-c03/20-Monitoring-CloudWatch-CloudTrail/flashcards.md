# Flashcards — Module 14: Monitoring, CloudWatch and CloudTrail

> **Format:** Q = Question | A = Answer
> **Total:** 25 flashcards

---

**Q:** How does the CloudWatch Agent enable memory and disk monitoring on EC2?
**A:** By default, CloudWatch does **not** collect RAM memory, disk usage, or process metrics. Installing the **CloudWatch Agent** on the instance allows sending custom metrics to CloudWatch (e.g., `mem_used_percent`, `disk_used_percent`). The Agent also collects logs and sends them to CloudWatch Logs.

---

**Q:** What is CloudWatch Logs Insights?
**A:** **Interactive query** engine for CloudWatch Logs. Custom syntax (SQL-like). Allows: filtering, aggregating, visualizing logs. Ex: `fields @timestamp, @message | filter @message like /ERROR/ | sort @timestamp desc | limit 20`. Pay per data scanned. Visual results (tables, time series graphs).

---

**Q:** What is CloudTrail and what events does it record?
**A:** **API call auditing** service on AWS. Records: who called which API, when, from which IP, with what result. Types: **Management Events** (create/delete resources — CloudFormation, IAM, EC2 start/stop), **Data Events** (operations on data — S3 GetObject, Lambda Invoke; disabled by default), **Insights Events** (unusual API activity).

---

**Q:** What is the difference between CloudTrail and AWS Config?
**A:** **CloudTrail:** "who did what and when?" — history of API calls. Action auditing. **AWS Config:** "how is it configured now and how did it change?" — history of resource configurations. Compliance: evaluate resources against rules. CloudTrail records events; Config records configuration states.

---

**Q:** What are AWS Config Rules and how do they work?
**A:** Rules that evaluate whether AWS resources comply with policies. **Managed Rules:** pre-built by AWS (e.g., `s3-bucket-public-read-prohibited`). **Custom Rules:** Lambda code that evaluates compliance. Evaluation: triggered by changes or periodic. Status: COMPLIANT / NON_COMPLIANT. Automatic remediations via SSM.

---

**Q:** What is AWS X-Ray and what are the central concepts?
**A:** **Distributed tracing** service for applications. Concepts: **Trace** = end-to-end request; **Segment** = work done by a service; **Subsegment** = granular sub-work; **Annotations** = key-value for filtering traces; **Sampling** = % of requests to trace (default: 5%). Service Map: visualization of dependencies and latencies.

---

**Q:** What is CloudWatch Anomaly Detection?
**A:** Uses ML to create an expected behavior model for a metric (based on history). Creates a dynamic "normal" band. Alerts when the metric falls outside the band. Adapts to seasonality (days of the week, times). More sophisticated than a static threshold alarm.

---

**Q:** What is AWS Systems Manager Session Manager and why is it more secure than SSH?
**A:** Access to EC2 instances (and managed on-premises) via browser or CLI **without opening port 22 (SSH) and without SSH keys**. Auditable: all sessions are logged in CloudWatch/S3. Works on instances in private subnets without a bastion host. Requires SSM Agent on the instance + IAM Role with `ssm:StartSession` permission.

---

**Q:** What are the two tiers of SSM Parameter Store?
**A:** **Standard:** free, up to 10,000 parameters, value up to 4 KB, no Advanced Policies, no TTL. **Advanced:** paid ($0.05/month per parameter), up to 100,000 parameters, value up to 8 KB, supports Parameter Policies (automatic TTL, expiration notifications). For rotating secrets: use Secrets Manager.

---

**Q:** What is CloudWatch Contributor Insights?
**A:** Analyzes logs and metrics to identify the **top contributors** of latency, error, or cost. Ex: "which 10 IPs generate the most 5XX errors?" or "which customers have the highest API latency?". Creates rules with log patterns. Useful for: security (detecting suspicious IPs), performance (identifying users/resources degrading the system).

---

**Q:** How to make CloudTrail logs tamper-proof?
**A:** Enable **Log File Validation** on the trail: CloudTrail generates a Digest file (SHA-256 hash) per hour. Any modification to the log file is detectable by comparing with the digest. Store logs in an S3 bucket with **Object Lock (Compliance mode)** + MFA Delete + restrictive policies. CloudTrail Lake for immutable analysis.

---

**Q:** What is AWS Config Aggregator?
**A:** Collects compliance data from AWS Config across multiple accounts and regions into a **central account**. Two source types: individual accounts (list of account IDs) or Organization (all accounts in AWS Org automatically). Allows centralized view of multi-account compliance. The central account needs permission from sources via delegated administrator.

---

**Q:** What is SSM Patch Manager?
**A:** Automates patching of EC2 instances (and on-premises). **Patch Baselines:** defines which patches to install (severity, classification). **Maintenance Windows:** time windows to apply patches. **Compliance Reporting:** reports in Config which instance is up to date. Can use Run Command to apply patches on-demand.

---

**Q:** What is the default retention of CloudWatch Logs?
**A:** By default: **indefinite** (logs never expire). Configurable per Log Group: 1 day to 10 years, or "Never Expire". To reduce cost: configure retention policy. For compliance: configure appropriate retention. For long term: export to S3 (CloudWatch Logs Subscription Filters → Kinesis Firehose → S3).

---

**Q:** What is AWS Trusted Advisor?
**A:** Advisor that analyzes the AWS account in 5 categories: **Cost Optimization** (idle instances, unused Reserved), **Performance** (EBS throughput, EC2 type), **Security** (open SGs, root MFA, public S3), **Fault Tolerance** (RDS backups, ELB health checks), **Service Limits** (alerts when approaching limits). Basic checks free; full with Business/Enterprise Support.

---

**Q:** How does CloudWatch Alarm monitor EC2 instance health and trigger recovery?
**A:** Alarm on `StatusCheckFailed_System` metric (failure in underlying hardware). Alarm action: **EC2 Instance Recovery** — moves the instance to healthy hardware keeping the same private IP, Elastic IP, metadata, and EBS volumes. (vs. Reboot which only restarts on the same hardware).

---

**Q:** What is CloudWatch Synthetics Canary?
**A:** Scripts (Node.js or Python) that emulate user behavior on web apps/APIs at configurable intervals. Monitors: availability, latency, user flows (login → checkout). Detects problems before real users are affected. Metrics sent to CloudWatch. Different from Real User Monitoring.

---

**Q:** What is EventBridge (formerly CloudWatch Events)?
**A:** Serverless event bus. Connects AWS services and SaaS. Sources: EC2 state changes, CodePipeline stages, Scheduled events (cron), S3 events, custom events. Targets: Lambda, SQS, SNS, Step Functions, Kinesis, ECS, API Gateway. Rules with event pattern matching (JSON filters). EventBridge Pipes for point-to-point transformation.

---

**Q:** What is CloudWatch Logs Subscription Filter?
**A:** In real time, filters and delivers logs from a Log Group to: **Kinesis Data Streams**, **Kinesis Firehose**, **Lambda**. Use cases: real-time log analysis (KDS → Lambda), long-term storage (KDF → S3), multi-account aggregation (cross-account subscription destinations).

---

**Q:** How does AWS Config detect non-compliant resources automatically and remediate?
**A:** **Detection:** Config Rule evaluated continuously or on change. NON_COMPLIANT status alerted in console and via EventBridge. **Automatic remediation:** SSM Automation Document executed automatically when rule detects non-compliance. Ex: public S3 bucket → remediation executes SSM that applies Block Public Access.

---

**Q:** What is CloudTrail Insights?
**A:** Detects anomalous API call activity. Analyzes normal pattern of write management events and alerts when there is significant deviation (e.g., unusual spike of `TerminateInstances`, `DeleteSecurityGroup`). Use cases: detect compromised credentials, automation errors, attacks. Insights events are charged separately.

---

**Q:** What is the difference between CloudWatch Metrics and CloudWatch Custom Metrics?
**A:** **Built-in Metrics:** automatically collected by AWS services (EC2 CPU, ELB latency, Lambda InvocationDuration). Default granularity: 5 minutes (1 min with "detailed monitoring"). **Custom Metrics:** sent via PutMetricData API or CloudWatch Agent from custom applications. Granularity: 1 second (High Resolution). Examples: business metrics, application memory.

---

**Q:** What is AWS Security Hub?
**A:** Centralizer of **security findings** from multiple services (GuardDuty, Inspector, Macie, IAM Analyzer, Config, Firewall Manager, 3rd party). Unified dashboard. Security posture scoring against standards (CIS AWS Benchmarks, AWS Foundational Security Best Practices). Automates remediations via EventBridge. Multi-account via Organization.

---

**Q:** What is SSM Run Command?
**A:** Executes scripts (Shell, PowerShell, etc.) on EC2 instances and managed on-premises servers at scale. No SSH required. Targets: instances by tag, by instance ID, all managed instances. Auditable: output sent to S3/CloudWatch. Rate control for gradual application. Basis of Patch Manager and other SSM automation.

---

**Q:** What is the difference between CloudWatch Logs and CloudTrail for security auditing?
**A:** **CloudTrail:** auditing of AWS actions (API calls, console logins, IAM changes). Answers: "was it deleted/modified? By whom? When?". **CloudWatch Logs:** application, OS, and AWS service logs (VPC Flow Logs, ALB access logs). Answers: "what happened inside the application?". For complete auditing: CloudTrail (who did what) + CloudWatch Logs (what happened in the system).

---

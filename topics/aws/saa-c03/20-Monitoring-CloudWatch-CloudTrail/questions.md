# Questions — Module 14: CloudWatch, CloudTrail and Config Monitoring

> **SAA-C03 Domain**: Design Secure Applications | Operational Excellence
> **Difficulty**: Medium

---

**1.** A company notices that their EC2 instances have CPU and network metrics in CloudWatch, but they cannot monitor RAM memory usage. What do they need to configure?

- A) Enable Detailed Monitoring on EC2 instances
- B) Install the CloudWatch Agent on instances and configure OS metric collection
- C) Use AWS Trusted Advisor for memory metrics
- D) Create custom metrics via CloudWatch API in instance user data

<details><summary>Answer</summary>

**B** — Standard EC2 metrics do not include RAM memory, disk usage, and processes (these are OS metrics, not hypervisor). The CloudWatch Agent installed on instances collects these operating system metrics and publishes them as Custom Metrics in CloudWatch. Detailed Monitoring (A) increases granularity from 5 min to 1 min, but still without memory.

</details>

---

**2.** A security audit discovered that AWS resources were deleted without authorization. The analyst needs to identify who deleted them, when, and from which IP. Which service has this information?

- A) Amazon CloudWatch Logs
- B) AWS CloudTrail (Management Events)
- C) AWS Config (Configuration History)
- D) Amazon GuardDuty

<details><summary>Answer</summary>

**B** — CloudTrail records all API calls including: who (userIdentity), when (eventTime), from where (sourceIPAddress), what action (eventName such as DeleteInstance, DeleteBucket). It is the "audit log" of AWS. CloudWatch Logs has application logs, not API calls.

</details>

---

**3.** A company needs to be alerted when any S3 bucket in the account becomes publicly accessible. What is the most efficient solution?

- A) Lambda that checks all bucket ACLs every hour
- B) AWS Config Rule `s3-bucket-public-read-prohibited` with SNS notification on non-compliance detection
- C) CloudWatch Alarm monitoring S3 access metrics
- D) Amazon Macie scanning all buckets

<details><summary>Answer</summary>

**B** — AWS Config Rule `s3-bucket-public-read-prohibited`: continuously evaluates whether buckets have public read permission. When a bucket becomes public, Config marks it as NON_COMPLIANT and can notify via SNS or execute automatic remediation via SSM. Proactive and without custom code.

</details>

---

**4.** A DevOps team wants to track how their Security Group configurations have changed over time (who added a rule, which rule, when). Which service provides this view?

- A) VPC Flow Logs
- B) AWS Config with resource Configuration Timeline
- C) CloudTrail with filter for `AuthorizeSecurityGroupIngress`
- D) B and C provide complementary views

<details><summary>Answer</summary>

**D** — AWS Config: shows the Security Group configuration history (state before and after each change). CloudTrail: shows which user/role made the change via API. Together: "what changed" (Config) + "who changed" (CloudTrail). On the exam, Config is for "what" and CloudTrail is for "who/when".

</details>

---

**5.** A microservices application has intermittent high latency. The team wants to identify which specific service (Lambda, DynamoDB, API Gateway) is causing the delay. Which observability service should be used?

- A) CloudWatch Logs with manual timestamp parsing
- B) AWS X-Ray with distributed tracing
- C) CloudWatch Metrics with dashboards
- D) CloudTrail to track API calls

<details><summary>Answer</summary>

**B** — X-Ray: instruments the application to create end-to-end traces. The Service Map visualizes time spent in each component (API GW → Lambda → DynamoDB). Subsegments show exactly where latency occurs. Identifies bottlenecks in complex distributed systems.

</details>

---

**6.** A company needs to retain CloudTrail logs for 7 years due to regulatory requirements, but storage cost must be minimized. What is the ideal configuration?

- A) CloudTrail → CloudWatch Logs with 7-year retention (2,555 days)
- B) CloudTrail → S3 with lifecycle policy: Standard (90 days) → Glacier (90-365 days) → Glacier Deep Archive (after 1 year)
- C) CloudTrail Lake with 7-year Event Data Store
- D) CloudTrail → S3 with Intelligent-Tiering

<details><summary>Answer</summary>

**B** — For long-term storage with minimal cost: CloudTrail delivers logs to S3, lifecycle policy moves to cheaper tiers over time. Glacier Deep Archive ($0.00099/GB/month) is the cheapest option for rarely accessed data. CloudTrail Lake (C) is excellent for queries but costs more.

</details>

---

**7.** A company wants to automatically detect suspicious activities on AWS such as: instance reconnaissance, unusual API calls at 3am, access from IPs in unknown countries. Which service should be used?

- A) AWS Config
- B) Amazon GuardDuty
- C) CloudTrail Insights
- D) AWS Security Hub

<details><summary>Answer</summary>

**B** — GuardDuty: Machine Learning analysis on CloudTrail, VPC Flow Logs, and DNS Logs. Detects threats such as reconnaissance, credential compromise, cryptocurrency mining activity, access from C&C (Command & Control) IPs. No manual rule configuration needed.

</details>

---

**8.** A developer needs to run commands on EC2 instances in a private subnet without opening SSH ports (port 22). Which solution should be implemented?

- A) Add a rule in the SG for the dev's IP
- B) Create a Bastion Host in the public subnet
- C) Use AWS Systems Manager Session Manager
- D) Use AWS Client VPN

<details><summary>Answer</summary>

**C** — SSM Session Manager: access to the instance shell via AWS console or CLI without open ports, without key pairs, without bastion host. The SSM Agent on the instance + IAM role with `AmazonSSMManagedInstanceCore` are the only requirements. Sessions are audited (CloudTrail) and can be recorded (S3/CloudWatch).

</details>

---

**9.** A company receives a notification that their EC2 instances are missing the mandatory `CostCenter` tag. They want instances without this tag to be automatically stopped. Which configuration implements this?

- A) CloudWatch Alarm → SNS → Email to the operations team
- B) AWS Config Rule for `required-tags` + Remediation Action via SSM Automation (StopInstances)
- C) Lambda scheduled by EventBridge checking tags via API
- D) Trusted Advisor to check for missing tags

<details><summary>Answer</summary>

**B** — AWS Config `required-tags` rule detects resources without mandatory tags. Config Remediation with SSM Automation document for StopInstances executes the action automatically when the rule detects Non-Compliant. Fully managed solution without custom Lambda code.

</details>

---

**10.** A company has 50 AWS accounts in its organization. The security team needs centralized visibility of all findings from GuardDuty, Inspector, Macie, and Config. Which service consolidates this view?

- A) AWS CloudTrail with multi-account trail
- B) AWS Security Hub with centralized aggregation in the management account
- C) Amazon Detective for consolidated investigation
- D) VPC Flow Logs centralized in S3

<details><summary>Answer</summary>

**B** — AWS Security Hub: consolidates security findings from GuardDuty, Inspector, Macie, Config, IAM Access Analyzer, and third-party tools in a single dashboard. With Organizations, automatically delegates to the management account or designated security account. Prioritizes findings with severity score.

</details>

---

**11.** A Lambda application generates JSON structured logs. The team wants to monitor the error rate and create an alarm when it exceeds 1% of invocations. What is the solution?

- A) Use the standard Lambda metrics `Errors` and `Invocations` in CloudWatch
- B) CloudWatch Logs Metric Filter to extract errors from logs → CloudWatch Metric → Alarm
- C) CloudWatch Logs Insights with alerts
- D) X-Ray with fault detection

<details><summary>Answer</summary>

**A** — Standard Lambda metrics (`Errors`, `Invocations`) in CloudWatch already record execution errors. Create an Alarm with the metric `sum(Errors)/sum(Invocations) * 100 > 1`. Metric Filter (B) is only needed for custom errors in application logs that are not captured by the standard Lambda metrics.

</details>

---

**12.** A company needs to maintain a record of all AWS resource configuration changes for 2 years for compliance auditing. Which configuration should be implemented?

- A) CloudTrail enabled in all regions with delivery to S3 with Object Lock Compliance
- B) AWS Config with delivery channel to S3 + 2-year configuration history retention
- C) CloudWatch Logs with 730-day retention for all service logs
- D) A and B are complementary and both are needed for complete auditing

<details><summary>Answer</summary>

**D** — Config records "what was configured" (resource snapshots); CloudTrail records "what changed via API call". For complete compliance auditing, both are needed. Config → S3 for long-term retention + CloudTrail → S3 with Object Lock for immutability.

</details>

---

**13.** A company uses Systems Manager Parameter Store to store database connection strings. They need to ensure these parameters are encrypted with a specific KMS key and that only the application can decrypt. How to implement?

- A) Use `String` type parameters encrypted with SHA256
- B) Use `SecureString` type parameters with a specific KMS CMK; application IAM role has `kms:Decrypt` only for that key
- C) Store in S3 encrypted with KMS
- D) Use Secrets Manager instead of Parameter Store

<details><summary>Answer</summary>

**B** — SecureString in Parameter Store uses KMS to encrypt the value. With CMK (Customer Managed Key), you control the key policy: only the application IAM role has `kms:Decrypt` for that specific key. Other services/users cannot read the value even with `ssm:GetParameter`.

</details>

---

**14.** An operations team wants to know when any EC2 instance enters the "impaired" state (status check failure) and automatically restart the instance. Which configuration should be implemented?

- A) CloudWatch Alarm on `StatusCheckFailed_System` metric → Action: EC2 Instance Recovery
- B) Auto Scaling Group with health check that replaces failed instances
- C) Scheduled Lambda checking instance status
- D) A for single instances; B for instances in ASG

<details><summary>Answer</summary>

**D** — For single instances outside ASG: EC2 Instance Recovery (via CloudWatch Alarm) moves the instance to healthy hardware keeping the same IP, EIP, and instance ID. For instances in ASG: the ASG itself replaces unhealthy instances automatically (health checks). The choice depends on the architecture.

</details>

---

**15.** A financial security company needs to ensure that all CloudTrail logs are immutable (no one can delete or modify, not even the root account). Which configuration should be implemented?

- A) CloudTrail → S3 with S3 Object Lock in Compliance mode + Bucket Policy denying delete
- B) CloudTrail with CloudWatch Logs (logs stay in CloudWatch which has automatic retention)
- C) CloudTrail with MFA Delete on the S3 bucket
- D) S3 Versioning on the CloudTrail logs bucket

<details><summary>Answer</summary>

**A** — S3 Object Lock in Compliance mode with retention period: **not even the root account** can delete or overwrite objects during the retention period. It is the only way to guarantee absolute immutability. MFA Delete (C) and Versioning (D) still allow deletion by authorized admins.

</details>

---

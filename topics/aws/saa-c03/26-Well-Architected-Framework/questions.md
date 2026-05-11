# Questions — Module 26: Well-Architected Framework

> **SAA-C03 Domain**: All domains (cross-cutting framework)  
> **Difficulty**: Medium-High

---

**1.** A company wants to implement the Reliability pillar principles of the Well-Architected Framework. Which of the following actions is NOT a principle of this pillar?

- A) Scale horizontally to increase system availability
- B) Automatically recover from failures
- C) Minimize the environmental impact of workloads
- D) Stop guessing capacity by using Auto Scaling

<details><summary>Answer</summary>

**C** — Minimizing environmental impact belongs to the **Sustainability** pillar (6th pillar). The Reliability pillar principles are: automatically recover from failures, test recovery procedures, scale horizontally, stop guessing capacity, and manage change through automation.

</details>

---

**2.** A company has a critical application with RPO of 1 hour and RTO of 30 minutes. Which DR strategy is the most cost-effective for these requirements?

- A) Backup & Restore (hourly snapshots)
- B) Pilot Light with critical components running in second region
- C) Warm Standby with reduced capacity in second region
- D) Multi-site Active-Active

<details><summary>Answer</summary>

**B** — Pilot Light: keeps the DB replicated (via Aurora Global DB or DMS CDC → RPO ~seconds) and AMIs ready in the second region. In case of disaster, components can be provisioned and DNS redirected (Route 53 failover) in ~10-15 minutes. RTO 30 min and RPO 1h are achievable at lower cost than Warm Standby.

</details>

---

**3.** A company is reviewing its workload with the AWS Well-Architected Tool and identified that it does not have logging for all API calls. Under which pillar does this risk fall?

- A) Performance Efficiency
- B) Cost Optimization
- C) Security
- D) Operational Excellence

<details><summary>Answer</summary>

**C** — The Security pillar requires "enabling traceability" — CloudTrail for APIs, CloudWatch Logs, Config for configurations. Lack of logging is a High Risk Item for security (prevents incident detection and investigation).

</details>

---

**4.** A startup uses EC2 On-Demand to run its production workloads that run 24/7 and have been running for 18 months. The CTO wants to reduce costs immediately. What is the primary recommendation of the Cost Optimization pillar?

- A) Purchase 1-year Reserved Instances or Savings Plans for the stable workload
- B) Migrate everything to Lambda (serverless)
- C) Move to Spot Instances
- D) Reduce the number of Availability Zones

<details><summary>Answer</summary>

**A** — Stable 24/7 workloads are ideal for Reserved Instances or Savings Plans. 1-year RI/SP offer ~40% discount vs On-Demand. Spot (C) is interruptible (inadequate for production 24/7 without fault tolerance). Lambda is not always cheaper for long-running workloads.

</details>

---

**5.** A company is developing a new application and wants to apply the principle of "implement a strong identity foundation" from the Security pillar. Which practices represent this? (Select 2)

- A) Use IAM roles for all applications (no hardcoded access keys)
- B) Enable MFA for human users accessing the AWS Console
- C) Configure CloudFront for all endpoints
- D) Use instances with higher memory capacity

<details><summary>Answer</summary>

**A and B** — IAM roles (no long-lived credentials) and MFA are the foundations of "strong identity foundation" from the Security pillar. CloudFront is Performance Efficiency/Reliability. Higher memory is Performance Efficiency.

</details>

---

**6.** A company suffered a security incident. After investigation, they realized they did not have sufficient logs to identify the root cause. Which Well-Architected Framework principle was neglected and which pillar?

- A) "Automate security best practices" — Pillar: Security
- B) "Enable traceability" — Pillar: Security
- C) "Refine operations procedures frequently" — Pillar: Operational Excellence
- D) "Anticipate failure" — Pillar: Reliability

<details><summary>Answer</summary>

**B** — "Enable traceability" is a design principle of the Security pillar. Traceability = CloudTrail logs (APIs), VPC Flow Logs (network), CloudWatch Logs (application), Config (configuration). Without these logs, forensic investigation is impossible.

</details>

---

**7.** A company has a development environment that runs 8 hours per day, 5 days per week. Currently it uses On-Demand instances and spends $500/month. What does the Cost Optimization pillar recommend?

- A) Convert to 1-year Reserved Instances
- B) Use Spot Instances for development
- C) Create automation (Lambda + EventBridge) to start/stop instances outside working hours
- D) Migrate the development environment to containers on Fargate

<details><summary>Answer</summary>

**C** — Non-production environments should only run when needed. Start/stop (8h x 5 days = 40h/week) vs 168h/week On-Demand → ~76% cost reduction. EventBridge Rules (schedule) → Lambda (start/stop EC2). Cost Optimization: adopt consumption model (pay for what you use).

</details>

---

**8.** A company uses a database server with very high specification (64 vCPUs) but average CPU usage is only 5%. What do the Performance Efficiency and Cost Optimization pillars recommend?

- A) Keep the high specification to ensure headroom
- B) Use AWS Compute Optimizer to identify the appropriate RDS instance type (rightsizing)
- C) Migrate to Lambda
- D) Add Read Replicas to distribute the load

<details><summary>Answer</summary>

**B** — Compute Optimizer analyzes historical metrics (CPU, memory — with CloudWatch agent, network) and recommends the ideal instance type. Over-provisioned = unnecessary cost without performance benefit. Rightsizing is a central principle of Cost Optimization.

</details>

---

**9.** A company realizes that its manual deployment process (SSH + rsync of code) is slow and error-prone, causing frequent incidents. Which Well-Architected pillar addresses this and which AWS technology?

- A) Reliability — use Multi-AZ to avoid downtime during deploys
- B) Operational Excellence — implement CI/CD with CodePipeline + CodeDeploy (perform operations as code)
- C) Performance Efficiency — use Elastic Beanstalk for automatic deployment
- D) Security — use IAM to control who can deploy

<details><summary>Answer</summary>

**B** — Operational Excellence: "perform operations as code" and "make frequent, small, reversible changes". CI/CD automates deployments, reduces human error and enables fast rollback. CodePipeline + CodeDeploy implements this principle directly.

</details>

---

**10.** A global application needs to serve content with minimum latency to users worldwide without maintaining multiple application clusters in each region. Which Performance Efficiency pillar principle is applied?

- A) Use the right technology for each task
- B) Go global in minutes using CloudFront, Global Accelerator and S3
- C) Stop guessing capacity
- D) Democratize advanced technologies

<details><summary>Answer</summary>

**B** — "Go global in minutes": CloudFront distributes content to 400+ edge locations without needing infrastructure in each region. Global Accelerator routes traffic through the private AWS network to reduce latency. Performance without horizontally scaling the application per region.

</details>

---

**11.** A company wants to measure whether its AWS workloads are aligned with Well-Architected Framework principles in a formal, documented way. What is the correct process?

- A) Manually compare architecture with whitepapers
- B) Use the AWS Well-Architected Tool (WAT) to perform a formal review per workload
- C) Hire AWS Professional Services for an audit
- D) Use Trusted Advisor to check the 5 categories

<details><summary>Answer</summary>

**B** — AWS Well-Architected Tool: defines the workload, answers questions about each pillar, generates risk report (HRI and MRI — High/Medium Risk Items), creates Improvement Plan and tracks progress. Free and can be performed by the architecture team itself.

</details>

---

**12.** From the Sustainability pillar perspective, which of the following architectures has the lowest environmental impact for an intermittent workload?

- A) EC2 On-Demand always on (24/7) with high utilization
- B) AWS Lambda (serverless) for intermittent loads and Fargate for containers
- C) EC2 Reserved Instances to guarantee availability
- D) EC2 with Auto Scaling with minimum of 5 instances

<details><summary>Answer</summary>

**B** — Sustainability: maximize resource utilization. Lambda and Fargate charge only when executing (zero idle consumption). Less hardware being used = lower carbon footprint. Serverless aligns resources precisely with demand, eliminating idle resources.

</details>

---

**13.** A company has different environments (dev, staging, prod) and wants to implement the "use IaC" principle from the Operational Excellence pillar. What direct benefit does this bring?

- A) Dev/staging/prod environments become identical, eliminating "works on my machine" bugs
- B) Automatically reduces EC2 cost
- C) Increases EC2 instance security
- D) Improves RDS query performance

<details><summary>Answer</summary>

**A** — IaC (CloudFormation, CDK, Terraform) allows creating identical environments reproducibly. The same template provisions dev, staging and prod with the same configurations, eliminating configuration drift and the famous "works in dev but not in prod" problem.

</details>

---

**14.** The security team wants to ensure that no SSH port (22) is open to 0.0.0.0/0 in any Security Group in the company. What is the most robust preventive approach from the Security pillar?

- A) Audit SGs manually every week
- B) Config Rule `restricted-ssh` + automatic Remediation that removes the violating rule
- C) CloudTrail alert when someone adds a rule to an SG
- D) IAM Permission denying `AuthorizeSecurityGroupIngress` for all users

<details><summary>Answer</summary>

**B** — Config Rule continuously detects SGs with port 22 open to 0.0.0.0/0. With Remediation configured, Config executes an SSM Automation that removes the violating rule automatically (or notifies for manual action). Automates security best practices — principle of the Security pillar.

</details>

---

**15.** A company is evaluating the total cost of operation (TCO) for a workload that consumes 1,000 hours of EC2 m5.large per month, consistently for 2 years. Which purchase model does the Cost Optimization pillar recommend?

- A) On-Demand (no commitment, maximum flexibility)
- B) Spot Instances (maximum discount)
- C) 1-year Compute Savings Plans ($X per hour committed)
- D) 3-year Convertible Reserved Instances (maximum discount)

<details><summary>Answer</summary>

**C** — 1-year Compute Savings Plans: ~66% discount vs On-Demand, more flexible than RI (can change instance type, OS, region within Compute SP). For predictable workload over 2 years, some commitment is clearly the way. 3 years (D) gives more discount but less flexibility; 1 year is the typical recommended sweet spot.

</details>

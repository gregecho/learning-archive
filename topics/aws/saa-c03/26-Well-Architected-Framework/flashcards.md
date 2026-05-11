# Flashcards — Module 26: Well-Architected Framework

> **Format:** Q = Question | A = Answer  
> **Total:** 25 flashcards

---

**Q:** What are the 6 pillars of the AWS Well-Architected Framework?  
**A:** **(1) Operational Excellence** — operate and monitor systems. **(2) Security** — protect data and systems. **(3) Reliability** — recover from failures, scale. **(4) Performance Efficiency** — use resources efficiently. **(5) Cost Optimization** — avoid unnecessary costs. **(6) Sustainability** — minimize environmental impact.

---

**Q:** What are the 4 Disaster Recovery strategies in order from lowest to highest cost/capability?  
**A:** **(1) Backup & Restore** (RPO/RTO: hours) → **(2) Pilot Light** (minimum core always running, RPO/RTO: tens of minutes) → **(3) Warm Standby** (scaled-down version always active, RTO: minutes) → **(4) Active-Active Multi-Site** (traffic in multiple regions simultaneously, RTO: seconds/zero).

---

**Q:** What is RPO vs RTO and how do they affect DR strategy choice?  
**A:** **RPO** (Recovery Point Objective): how much data can I lose. **RTO** (Recovery Time Objective): how long can I be unavailable. Lower RPO/RTO = more expensive strategy: Backup&Restore (RPO/RTO hours) → Pilot Light → Warm Standby → Active-Active (RPO/RTO ~0, most expensive).

---

**Q:** What is the Operational Excellence pillar and its design principles?  
**A:** Focus on operating and improving processes continuously. Principles: **Perform operations as code** (IaC), **Annotate documentation** (auto-generated), **Make frequent, small, reversible changes** (no big-bang deployments), **Refine operations procedures frequently** (Game Days), **Anticipate failure** (pre-mortem), **Learn from failures** (blameless post-mortems).

---

**Q:** What is the Security pillar and its "base of identity" principle?  
**A:** **Identity is the foundation of security.** Everything starts with "who can do what". Principles: Strong identity foundation (IAM, Organizations SCP), Enable traceability (CloudTrail, CloudWatch), Apply security at all layers (SG, WAF, KMS, encryption), Protect data in transit and at rest, Keep people away from data, Prepare for security events.

---

**Q:** What is the Reliability pillar and how does Auto Scaling contribute?  
**A:** Reliability = ability to recover from failures and grow. Auto Scaling contributes via: scaling horizontally (more instances, not bigger), automatically recovering from failures (replacing unhealthy instances), distributing across multiple AZs. Principles: Test recovery procedures, Stop guessing capacity, Manage change with automation.

---

**Q:** What is the Performance Efficiency pillar?  
**A:** Use computing resources efficiently. Principles: **Democratize advanced technologies** (use managed services instead of building), **Go global in minutes** (regions, CloudFront), **Use serverless architectures** (no server management), **Experiment more often** (ease of testing instance types), **Consider mechanical sympathy** (use the right service for the workload).

---

**Q:** What are the principles of the Cost Optimization pillar?  
**A:** Avoid unnecessary spending. Principles: **Implement cloud financial management** (organizational process), **Adopt a consumption model** (pay for what you use, shut down idle), **Measure overall efficiency** (output per cost), **Stop spending on undifferentiated heavy lifting** (use managed services), **Analyze and attribute expenditure** (tags, cost allocation).

---

**Q:** What is the Sustainability pillar and how to reduce environmental impact?  
**A:** Minimize environmental impact of workloads. Practices: use regions with lower carbon footprint, optimize utilization (non-idle instances), use managed services (AWS optimizes shared hardware), serverless (on-demand resources), scaling down during low-usage periods, modernize hardware via new services (Graviton — better energy efficiency).

---

**Q:** What is the AWS Well-Architected Tool (WAT)?  
**A:** Tool in the AWS console to review workloads against the 6 pillars. Process: create review → answer questions by pillar → receive "High Risk Issues" (HRI) and "Medium Risk Issues" (MRI) with recommendations. Creates improvement plan. Free. Can be created by AWS partners via the Well-Architected Partner Program.

---

**Q:** What does "Pilot Light" mean in DR strategy?  
**A:** Keep the **minimum core** of the application always running in the DR region. The core: database (replicated) and basic configurations. In case of disaster: "light the pilot" = scale the remaining components (EC2, ELB) in the DR region. RTO: minutes to tens of minutes. Lower cost than Warm Standby (only the essential runs continuously).

---

**Q:** What is "Warm Standby" and how does it differ from "Pilot Light"?  
**A:** **Warm Standby:** full (but reduced/sub-capacity) version of the application running in the DR region. **Pilot Light:** only the minimum core. Difference: Warm Standby has all components ready (small EC2, RDS replica), only scales on failover. Pilot Light needs to provision EC2 etc on failover. Warm Standby = lower RTO, higher cost.

---

**Q:** What is the availability table for 99%, 99.9%, 99.99%, 99.999%?  
**A:** **99%** = ~87.6h downtime/year (~7.3h/month). **99.9%** = ~8.7h/year (~43.8 min/month). **99.99%** = ~52 min/year (~4.4 min/month). **99.999% (Five Nines)** = ~5.26 min/year (~26 sec/month). Five Nines requires active-active architecture with zero tolerance for single point of failure.

---

**Q:** How to compare On-Demand vs Reserved vs Savings Plans in the Cost Optimization context?  
**A:** **On-Demand:** maximum flexibility, maximum price. Use for: unpredictable workloads, spikes. **Reserved (1 or 3 years):** up to 72% discount. Use for: stable and predictable 24/7 workload. **Savings Plans:** $ per hour commitment (Compute or EC2/Fargate/Lambda). More flexible than Reserved. **Spot:** up to 90% off, interruptible. Use for: batch, fault-tolerant.

---

**Q:** What is the Well-Architected Framework Lens?  
**A:** Extension of WAF for specific domains. Available: **Serverless Lens**, **SaaS Lens**, **Machine Learning Lens**, **Data Analytics Lens**, **Games Industry Lens**, **SAP Lens**, **High Performance Computing Lens** etc. Each Lens has specific questions and best practices for that domain beyond the 6 base pillars.

---

**Q:** Which Well-Architected principle says "design for failure"?  
**A:** **Reliability** pillar: "Test recovery procedures" and "Design for failure". AWS: design assuming components WILL fail. Everything should have redundancy. Avoid SPOFs (Single Points of Failure). Multi-AZ, Auto Scaling, circuit breakers, dead letter queues — resilient architecture assumes failures as expected, not exceptional.

---

**Q:** How does the "Infrastructure as Code" principle fit into Well-Architected?  
**A:** **Operational Excellence** pillar: "Perform operations as code". IaC (CloudFormation, Terraform, CDK): (1) reproducible — same state every time; (2) auditable — changes in version control; (3) reversible — rollback to previous version; (4) testable — validate before production. Eliminates inconsistent manual configuration.

---

**Q:** What is the "Loose Coupling" principle in Well-Architected?  
**A:** **Reliability** pillar: components with weak dependencies fail in isolation. Implementation: SQS between services (buffered messages if downstream fails), SNS for fan-out, API Gateway decouples clients from backends, ELB decouples clients from instances. Opposite: tight coupling (services call directly → failure in one cascades).

---

**Q:** What are Game Days in the Operational Excellence context?  
**A:** Planned simulations of failures and incidents to test response procedures. "Pre-mortems": imagining the system failed and identifying causes. Goal: discover vulnerabilities and gaps in runbooks before they happen in production. Culture of learning through simulation. Related to Chaos Engineering (Netflix Chaos Monkey).

---

**Q:** What is the difference between "vertical scaling" and "horizontal scaling" in Well-Architected?  
**A:** **Vertical (Scale Up):** increase instance size (m5.large → m5.xlarge). Physical limit. Requires downtime (generally). SPOF. **Horizontal (Scale Out):** add more instances of the same type. No practical limit. No downtime (gradual). Eliminates SPOF. Well-Architected favors horizontal: "Scale horizontally to increase aggregate system availability."

---

**Q:** What is the "consumption model" in the Cost Optimization pillar?  
**A:** Pay only for what you use — opposite of the on-premises model (pay for peak capacity, even when idle). AWS: scale down when demand drops. Shut down dev environments at night/weekends. Lambda/Fargate/DynamoDB On-Demand: pay only for actual execution. Goal: cost proportional to actual usage, not theoretical peak.

---

**Q:** What are the 3 types of security controls according to Well-Architected?  
**A:** **(1) Preventive:** prevents problems before they happen (IAM policies, SCP, SGs, encryption). **(2) Detective:** detects when something happens (CloudTrail, Config Rules, GuardDuty, Security Hub). **(3) Responsive:** responds after detection (runbooks, SNS/Lambda automation, incident response plans). Secure architecture needs all 3 types.

---

**Q:** What is "blast radius reduction" in the Security pillar?  
**A:** Limit the potential impact of a security failure. Techniques: **Least privilege** (compromised account has minimal access), **Accounts separation** (AWS Organizations — workloads in separate accounts, failure in one does not affect others), **Network segmentation** (separate VPCs, private subnets), **Encryption per-resource** (compromised key only affects data under that key).

---

**Q:** How does the Sustainability pillar apply practically on AWS?  
**A:** Practices: **(1)** Choose region with lower carbon emission factor. **(2)** Use Graviton instances (ARM — better performance/watt). **(3)** Optimize utilization: avoid over-provisioning (Compute Optimizer). **(4)** Serverless: resources freed when not used. **(5)** S3 Lifecycle: move cold data to Glacier (less energy). **(6)** Eliminate unnecessary workloads.

---

**Q:** What are Shared Responsibility Areas in Well-Architected?  
**A:** Well-Architected recognizes that some responsibilities are shared between teams: Dev, Ops, Security and Cloud Center of Excellence (CCoE). WAT reviews ideally involve: solutions architect + security engineer + business representative. It is not the responsibility of ops alone or dev alone. Shared architecture culture.

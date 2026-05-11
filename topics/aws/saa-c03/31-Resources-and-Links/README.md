# Module 21 — Study Resources and Links

## Official AWS Documentation

### Essential User Guides

| Service | Link |
|---|---|
| **EC2 User Guide** | https://docs.aws.amazon.com/ec2/latest/userguide/ |
| **S3 User Guide** | https://docs.aws.amazon.com/AmazonS3/latest/userguide/ |
| **VPC User Guide** | https://docs.aws.amazon.com/vpc/latest/userguide/ |
| **RDS User Guide** | https://docs.aws.amazon.com/AmazonRDS/latest/UserGuide/ |
| **DynamoDB Developer Guide** | https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/ |
| **Lambda Developer Guide** | https://docs.aws.amazon.com/lambda/latest/dg/ |
| **IAM User Guide** | https://docs.aws.amazon.com/IAM/latest/UserGuide/ |
| **CloudFormation User Guide** | https://docs.aws.amazon.com/AWSCloudFormation/latest/UserGuide/ |
| **ECS Developer Guide** | https://docs.aws.amazon.com/AmazonECS/latest/developerguide/ |
| **EKS User Guide** | https://docs.aws.amazon.com/eks/latest/userguide/ |

---

## Official AWS Whitepapers (Essential for the Exam)

| Document | Relevance |
|---|---|
| **AWS Well-Architected Framework** | HIGH — entire module 16 is based on this |
| **Architecting for the Cloud: Best Practices** | HIGH — architectural patterns |
| **AWS Security Best Practices** | HIGH — security domain (30%) |
| **Running Containerized Microservices on AWS** | MEDIUM — ECS, EKS, microservices |
| **Practicing Continuous Integration and Delivery on AWS** | MEDIUM — CodePipeline, CodeBuild, deploy |
| **AWS Storage Services Overview** | HIGH — S3, EBS, EFS, FSx, Storage Gateway |
| **Building Big Data Storage Solutions (Data Lakes) for Maximum Flexibility** | MEDIUM — S3, Glue, Athena, Lake Formation |
| **Overview of Deployment Options on AWS** | MEDIUM — Blue/green, canary, rolling |

Portal: https://aws.amazon.com/whitepapers/

---

## Important AWS Service FAQs

FAQs contain questions that frequently appear on the exam:

| Service | FAQ URL |
|---|---|
| **Amazon EC2** | https://aws.amazon.com/ec2/faqs/ |
| **Amazon S3** | https://aws.amazon.com/s3/faqs/ |
| **Amazon RDS** | https://aws.amazon.com/rds/faqs/ |
| **Amazon DynamoDB** | https://aws.amazon.com/dynamodb/faqs/ |
| **Amazon VPC** | https://aws.amazon.com/vpc/faqs/ |
| **Amazon Route 53** | https://aws.amazon.com/route53/faqs/ |
| **AWS Lambda** | https://aws.amazon.com/lambda/faqs/ |
| **Amazon SQS** | https://aws.amazon.com/sqs/faqs/ |
| **Amazon SNS** | https://aws.amazon.com/sns/faqs/ |
| **Amazon CloudFront** | https://aws.amazon.com/cloudfront/faqs/ |

---

## Courses and Training

### Official AWS Courses (AWS Training & Certification)
- **AWS Cloud Practitioner Essentials** — Fundamentals (free): https://explore.skillbuilder.aws
- **Architecting on AWS** — 3-day AWS in-person/virtual course
- **AWS Solutions Architect - Associate (Learning Path)** — SkillBuilder: https://skillbuilder.aws/learning_plan/view/78/solutions-architect-associate-learning-plan

### Recommended Third-Party Courses

| Platform | Instructor | Notes |
|---|---|---|
| Udemy | **Stephane Maarek** (SAA-C03) | Most popular, updated, EN |
| Udemy | **Neal Davis** (Adrian Cantrill material) | Very technical, EN |
| CloudGuru / Pluralsight | Various | Hands-on labs |
| YouTube | **FreeCodeCamp** | Free crash courses |

---

## Practice Exams and Question Banks

| Platform | Type | Notes |
|---|---|---|
| **Tutorials Dojo** (Jon Bonso) | SAA-C03 Practice Exams | Best practice exam bank for the exam; detailed explanations |
| **AWS Skill Builder** (Official Practice) | Official exams | Official practice exam: 20 questions ($0 with subscription) |
| **ExamPro** | Neal Davis practice exams | High quality, explanations |
| **Whizlabs** | Question bank | Additional option |
| **Udemy Practice Tests** | Maarek / Neal Davis | Usually comes with the course |

---

## Study Tools

| Tool | Use |
|---|---|
| **AWS Free Tier** | Free account for labs: https://aws.amazon.com/free/ |
| **AWS Architecture Center** | Architecture diagrams and references: https://aws.amazon.com/architecture/ |
| **AWS This Is My Architecture** | Videos of real AWS customer architectures: https://aws.amazon.com/this-is-my-architecture/ |
| **AWS Blog** | News and technical deep dives: https://aws.amazon.com/blogs/aws/ |
| **AWS re:Invent YouTube** | Free technical talks: https://youtube.com/@AWSEventsChannel |
| **AWS Calculator** | Cost estimation: https://calculator.aws/ |
| **AWS Exam Guide** | Official SAA-C03 exam guide: https://d1.awsstatic.com/training-and-certification/docs-sa-assoc/AWS-Certified-Solutions-Architect-Associate_Exam-Guide.pdf |

---

## Resources by Exam Domain

### Domain 1 — Resilient Architectures (26%)
- [AWS Fault Isolation Boundaries](https://docs.aws.amazon.com/whitepapers/latest/aws-fault-isolation-boundaries/abstract-and-introduction.html)
- [Disaster Recovery of Workloads on AWS: Recovery in the Cloud](https://docs.aws.amazon.com/whitepapers/latest/disaster-recovery-workloads-on-aws/disaster-recovery-workloads-on-aws.html)
- [Amazon RDS Multi-AZ](https://aws.amazon.com/rds/features/multi-az/)
- [SQS Developer Guide — Dead Letter Queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)

### Domain 2 — High-Performance Architectures (24%)
- [Amazon EC2 Instance Types](https://aws.amazon.com/ec2/instance-types/)
- [Caching Overview (ElastiCache)](https://aws.amazon.com/caching/aws-caching/)
- [DynamoDB Best Practices](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/best-practices.html)
- [Amazon Aurora Features](https://aws.amazon.com/rds/aurora/features/)

### Domain 3 — Secure Applications (30%)
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html)
- [AWS Security Best Practices (Whitepaper)](https://docs.aws.amazon.com/whitepapers/latest/aws-security-best-practices/aws-security-best-practices.html)
- [VPC Security Groups and NACLs](https://docs.aws.amazon.com/vpc/latest/userguide/infrastructure-security.html)
- [KMS Key Policies](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html)

### Domain 4 — Cost-Optimized Architectures (20%)
- [AWS Cost Optimization Pillar](https://docs.aws.amazon.com/wellarchitected/latest/cost-optimization-pillar/welcome.html)
- [Spot Instances](https://aws.amazon.com/ec2/spot/)
- [AWS Savings Plans](https://aws.amazon.com/savingsplans/)
- [S3 Storage Classes](https://aws.amazon.com/s3/storage-classes/)

---

## Recommended YouTube Channels

| Channel | Content |
|---|---|
| **AWS Events** | re:Invent, re:Inforce talks |
| **TechWorld with Nana** | Kubernetes, Docker, DevOps (EN) |
| **AWS Online Tech Talks** | Technical demos of specific services |
| **Rampup programs (AWS)** | Structured learning series |

---

## Suggested Study Timeline

```
Week 1-2:  Modules 01-04 (Cloud, EC2, IAM, S3, Storage)
Week 3-4:  Modules 05-07 (Advanced S3, Databases, VPC/Networks)
Week 5-6:  Modules 08-10 (Route53/CloudFront, SQS/SNS, Containers)
Week 7-8:  Modules 11-13 (Lambda/API GW, Analytics, ML/AI)
Week 9:    Modules 14-16 (Monitoring, Migration, Well-Architected)
Week 10:   Practice exams (Module 19) + review of weak points
Week 11:   Intensive flashcards + Cheatsheets from all modules
Week 12:   Full practice exams + final review + schedule exam
```

---

## Exam Registration

1. Visit: https://aws.amazon.com/certification/certified-solutions-architect-associate/
2. Create account at: https://www.aws.training/ or https://home.pearsonvue.com/aws
3. Choose format: In-person (test center) or Online Proctored
4. Cost: USD $150
5. Validity: 3 years (renew with recertification exam or higher-level exam)

**Exam ID**: SAA-C03

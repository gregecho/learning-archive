# Real Use Cases — Study Resources in Action (Module 21)

## Case 1 — Study Plan for Someone with 8 Weeks

**Context:** IT professional with on-premises infrastructure experience (no prior AWS experience) plans to obtain SAA-C03 in 8 weeks, studying 2 hours per day.

**Week-by-Week Plan:**
```
WEEK 1 — BASICS AND COMPUTE (14h):
Resources:
  ├── Udemy Course Stephane Maarek: Sections 1-5 (EC2, ELB, ASG)
  ├── AWS Free Tier: create account + explore console
  └── Skill Builder: "AWS Cloud Practitioner Essentials" (free)
  
Practice:
  └── Create EC2 t3.micro, connect via SSH, install nginx, access via browser
  
Goal: understand EC2, instance types, pricing, ELB, Auto Scaling

WEEK 2 — STORAGE AND DATABASE (14h):
Resources:
  ├── Maarek Course: Sections 6-10 (EBS, EFS, S3, RDS, DynamoDB)
  └── AWS Docs: S3 FAQ + RDS FAQ (30min each)
  
Practice:
  └── Create S3 bucket, versioning, lifecycle policy
  └── Create RDS Free Tier, connect via DBeaver

WEEK 3 — NETWORK AND SECURITY (14h):
Resources:
  ├── Maarek Course: Sections 11-14 (VPC, Route 53, CloudFront, WAF)
  └── Whitepaper: "AWS Security Best Practices" (1h)
  
Practice:
  └── Create VPC with 2 subnets (public+private), NAT GW, bastion host

WEEK 4 — SERVERLESS AND INTEGRATION (14h):
Resources:
  ├── Maarek Course: Sections 15-19 (Lambda, SQS, SNS, API GW, Kinesis)
  └── Tutorial: "Build a Serverless App" (free AWS Labs)
  
Practice:
  └── Lambda + API GW + DynamoDB (complete todo app)

WEEK 5 — MICROSERVICES, MONITORING AND ANALYTICS (14h):
Resources:
  ├── Maarek Course: Sections 20-24 (ECS, CloudWatch, CloudTrail, Athena)
  └── AWS Architecture Center: Well-Architected examples

WEEK 6 — MIGRATION, COST, BEST PRACTICES (14h):
Resources:
  ├── Maarek Course: Final sections
  └── Whitepaper: "AWS Well-Architected Framework"
  
WEEK 7 — FIRST PRACTICE EXAM (14h):
Resources:
  ├── Tutorials Dojo: 1 full practice exam (65 questions)
  └── Review ALL wrong questions (read explanations carefully)
  
Goal: score > 65% on first practice exam

WEEK 8 — INTENSIVE REVIEW + EXAM (14h):
Resources:
  ├── Tutorials Dojo: second full practice exam
  ├── Review cheatsheets for the most missed services
  └── Flashcards in the days before the exam
  
SCHEDULE EXAM: at the beginning of week 7 (motivation to study!)
```

---

## Case 2 — Using Skill Builder for Hands-On Labs

**Context:** Candidate knows theory but has never operated on AWS. Skill Builder offers hands-on labs with included credits.

**Skill Builder Lab Plan:**
```
AWS Skill Builder Individual ($29/month or $299/year): 
  Access to real sandbox labs (never pay AWS costs in labs)
  
PRIORITY LABS FOR SAA-C03:
├── "Introduction to Amazon EC2" (free on basic Skill Builder)
├── "Introduction to Amazon S3" 
├── "Creating an Amazon Virtual Private Cloud (VPC)"
├── "Introduction to Amazon RDS"
├── "Introduction to AWS Lambda"
├── "Introduction to Amazon DynamoDB"
├── "Introduction to Amazon CloudWatch"
├── "Introduction to AWS IAM"
└── "AWS Well-Architected Best Practices" (not a lab, theoretical module)

EXAM READINESS: "AWS Certified Solutions Architect - Associate" 
  (free official course, 3h, covers all exam domains)
  Available at: skillbuilder.aws → search "SAA Exam Readiness"

FREE ON BASIC SKILL BUILDER (no payment):
├── Cloud Practitioner Essentials
├── AWS Technical Essentials  
├── Exam Readiness SAA-C03
└── Several introductory-level labs
```

---

## Case 3 — Strategy for Architecture Diagram Questions

**Context:** The SAA-C03 exam presents complex multi-service scenarios. How to structure reasoning.

**Analysis Framework:**
```
4-STEP METHOD:

STEP 1 — READ THE LAST PARAGRAPH FIRST:
(usually contains the main constraint)
"The company needs the LOWEST COST solution that meets the requirements."
→ This immediately eliminates all more expensive solutions

STEP 2 — IDENTIFY KEYWORDS:
┌─────────────────────────────────────────────────────────┐
│ "serverless"       → Lambda, Fargate, Aurora Serverless  │
│ "lowest overhead"  → Managed services                    │
│ "real-time"        → Kinesis, EventBridge                │
│ "decouple"         → SQS, SNS                            │
│ "global"           → CloudFront, Route 53, DynamoDB GT   │
│ "auto failover"    → Multi-AZ, Route 53 Failover         │
│ "scale reads"      → Read Replica (NOT Multi-AZ)         │
│ "no data loss"     → Multi-AZ, synchronous               │
│ "compliance/audit" → CloudTrail + S3 + Object Lock       │
│ "sensitive data"   → Macie, KMS, Secrets Manager         │
└─────────────────────────────────────────────────────────┘

STEP 3 — ELIMINATE CLEARLY WRONG OPTIONS:
"Install software on EC2 instances" → red flag (more overhead)
"Manually manage" in an HA question → almost always wrong
"Share root credentials" → always wrong

STEP 4 — CHOOSE BETWEEN THE 2 REMAINING:
Apply the question's criteria (cost? performance? availability?)
If still in doubt: managed service > self-managed on AWS
```

---

## Case 4 — Using Tutorials Dojo vs Real Exam

**Context:** Candidate has a 78% score on Tutorials Dojo. Are they ready for the real exam?

**Practice Exam Calibration:**
```
PRACTICE SCORE × REAL EXAM CORRELATION (empirical):
Tutorials Dojo 75% → Real exam likely 70-75% (passing: 72%)
Tutorials Dojo 80% → Real exam likely 75-82% (comfortable pass)
Tutorials Dojo 85% → Real exam likely 80-88% (good pass)

WHY PRACTICE EXAMS MAY BE HARDER:
Tutorials Dojo and ExamTopics have more technical/detailed questions
The real exam has more scenario-based questions than purely technical ones
Real exam: 50 scored + 15 experimental (new questions don't count)

INTERPRETING SCORE BY DOMAIN:
Domain 1 (Security 30%): score < 70% → review IAM, KMS, VPC
Domain 2 (Resilience 26%): score < 70% → review Multi-AZ, Auto Scaling, DR
Domain 3 (Performance 24%): score < 70% → review ElastiCache, Kinesis, CloudFront
Domain 4 (Cost 20%): score < 70% → review S3 tiers, Reserved, Spot

RECOMMENDED TARGET:
Take 2-3 full 65-question practice exams
Average score > 78% on the last 2 practice exams → schedule exam
Do not take a practice exam the day before the real exam (anxiety)
```

---

## Case 5 — Post-Certification: Next Career Steps

**Context:** Candidate just passed SAA-C03. What to do next to maximize return on investment.

**Career Plan:**
```
IMMEDIATE (first 7 days):
├── Update LinkedIn:
│   Licenses & Certifications section:
│   Name: "AWS Certified Solutions Architect - Associate"
│   Issuer: Amazon Web Services (AWS)
│   Verification link: Credly badge
├── Accept badge on Credly (email from AWS)
└── Update resume/profile on job boards

NEXT CERTIFICATIONS (recommended order):
OPTION A — Broaden (other Associate before Professional):
SAA-C03 → DVA-C02 (Developer) → SOA-C02 (SysOps) → SAP-C02 (Pro)

OPTION B — Go deeper directly:
SAA-C03 → SAP-C02 (Professional — maximum Architect level)
           (SAA automatically renews when passing SAP)

OPTION C — Specialization:
SAA-C03 → DOP-C02 (DevOps Pro) or ANS-C01 (Advanced Network)
           or SCS-C02 (Security Specialty)

FOR JOB SEEKERS:
AWS Partner Network (register free account) → find jobs
LinkedIn: "AWS Solutions Architect" → job alerts
GitHub: create repository with AWS projects (practical evidence)
Blog: write about what you learned → visibility

FOR FREELANCERS:
Upwork/Toptal: certification increases hourly rate
AWS Marketplace: companies seek certified SAs for consulting
AWS Partner: company can become a partner with 2+ certified SAs

MAINTAIN RELEVANCE:
AWS re:Invent (November): main conference, yearly news
AWS Blogs (aws.amazon.com/blogs): weekly service news
re:Post: answer community questions (solidify knowledge)
```

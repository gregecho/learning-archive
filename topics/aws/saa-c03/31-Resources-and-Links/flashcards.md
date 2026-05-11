# Flashcards — Module 21: Resources and Links

> **Format:** Q = Question | A = Answer  
> **Total:** 20 flashcards — resources, strategies, and study guidance

---

**Q:** What is the official AWS website for all certifications and where to schedule the exam?  
**A:** **aws.amazon.com/certification/** — main certifications page. To schedule: "Schedule Exam" button → redirects to **Pearson VUE** (in-person test centers or online proctored). Alternative: register through the SAA-C03 certification page itself. Remember: valid ID required (government-issued photo ID or passport for online proctored).

---

**Q:** What are the 3 main paid courses recommended for SAA-C03?  
**A:** **(1) Stephane Maarek (Udemy):** Ultimate AWS Certified Solutions Architect Associate — most popular, 30h+, updated, exam-focused. **(2) Neal Davis (Digital Cloud Training):** AWS SAA-C03 — clear explanations, good for beginners. **(3) Adrian Cantrill:** superior technical depth, more difficult, for those who want to truly understand. All available on Udemy frequently on sale.

---

**Q:** What is the most important official AWS resource for real practice questions?  
**A:** **AWS Skill Builder** (skillbuilder.aws): **(1)** "AWS Certified Solutions Architect – Associate Official Practice Question Set" — 20 free official questions. **(2)** "Exam Prep Official Practice Exam: AWS SAA-C03" — 65 paid questions, with detailed feedback. Credentials: free account on Skill Builder. Official questions give the real exam difficulty level.

---

**Q:** What is Tutorials Dojo and why is it highly recommended?  
**A:** **tutorialsdojo.com** — practice exam platform created by Jon Bonso. Highlights: explanations for EVERY option of each question (why correct + why each wrong answer is wrong); cheat sheets by service; timed and review modes; high correlation with real exam. Cost: ~$15-30 per practice exam. Widely cited as the best practice resource beyond the official one.

---

**Q:** Which AWS whitepaper is most important for SAA-C03 and where to find it?  
**A:** **"AWS Well-Architected Framework"** — aws.amazon.com/architecture/well-architected. Describes the 6 pillars with design principles. Other essentials: **(1)** "Architecting for the Cloud: AWS Best Practices". **(2)** "AWS Security Best Practices". **(3)** "Disaster Recovery of Workloads on AWS". All free at aws.amazon.com/whitepapers.

---

**Q:** How to use the AWS Architecture Center for studying?  
**A:** **aws.amazon.com/architecture** — library of Reference Architectures by use case (web apps, serverless, data lake, microservices) and industry. For studying: open architecture diagrams relevant to the exam (3-tier web app, serverless API, data lake), understand which services are combined and why. Official AWS reference architectures.

---

**Q:** What is the official tool for estimating costs of an AWS architecture?  
**A:** **AWS Pricing Calculator** (calculator.aws) — free. Select services, configure parameters (region, instance type, expected usage in hours/GB/requests), add to estimate, share estimate via URL. Different from Cost Explorer (for already incurred costs). In the exam: "estimate costs before implementing" → Pricing Calculator.

---

**Q:** Where to find AWS service FAQs and how to use them for studying?  
**A:** On each AWS service page: `aws.amazon.com/[service]/faqs/`. E.g.: `aws.amazon.com/s3/faqs/`, `aws.amazon.com/ec2/faqs/`. FAQs explain limits, edge cases, and specific behaviors that appear on the exam. Reading priority: EC2, S3, RDS, IAM, VPC, Lambda, DynamoDB — services with the greatest exam weight.

---

**Q:** What is the difference between Pearson VUE and PSI for scheduling the AWS exam?  
**A:** Both are AWS-approved exam providers. **Pearson VUE:** more popular, more test centers, online proctored option (OnVUE). **PSI:** alternative, fewer centers, also has online proctored. For online proctored: requires webcam, microphone, quiet environment with no other people, nothing on the desk. Exam in English available; some localized versions may be available.

---

**Q:** What to study in the final week before the SAA-C03 exam?  
**A:** Last week: **(1)** Review practice exam mistakes (focus on what you got wrong, not what you already know). **(2)** Cheatsheets by service (numerical limits, comparisons). **(3)** Domain 1 (Security, 30%) — IAM conditions, encryption, network security. **(4)** Full practice exam (65q) to measure readiness. **(5)** Do not study anything new in the last 2 days — review + rest. Score 75%+ on practice exams = ready for the exam.

---

**Q:** Which YouTube channel has the best free AWS service summaries for the exam?  
**A:** **(1) Be a Better Dev** — practical and conceptual demos. **(2) Stephane Maarek** — course snippets. **(3) Digital Cloud Training (Neal Davis)** — detailed tutorials. **(4) AWS Events** — technical re:Invent talks (advanced). **(5) TechWorld with Nana** — complementary Docker/K8s. For English content: search "SAA-C03 preparation".

---

**Q:** What is the AWS Free Tier for in hands-on study?  
**A:** Practicing labs at no cost. Essential Always Free resources: Lambda 1M req/month, DynamoDB 25GB, CloudFront 1TB/month, SNS 1M req, API Gateway 1M req/month. 12-month free: EC2 t2/t3.micro 750h/month, S3 5GB, RDS db.t2.micro 750h/month. **ALWAYS:** set up Budget Alert in the Billing Console to alert if cost > $1. Clean up after labs (stop/delete resources).

---

**Q:** How to use AWS Skill Builder for free for preparation?  
**A:** Create a free account at skillbuilder.aws. Access: **(1)** "AWS Cloud Practitioner Essentials" (free basic course). **(2)** "Architecting on AWS" (concepts). **(3)** "AWS Certified Solutions Architect - Associate" learning path (free). **(4)** "Official Practice Question Set SAA-C03" (20 free questions). Paid subscription ($29/month) gives access to full practice exams and labs.

---

**Q:** What is the AWS Certification Discord and how to benefit from it?  
**A:** Online communities where candidates share exam experiences, resources, and tips. AWS: join servers like "AWS Study Group", "r/AWSCertifications" (Reddit), "Discord AWS Brasil" (or regional equivalents). Benefits: exam update tips, notifications when questions change, sharing of free resources, support from people who recently passed.

---

**Q:** How to set up a local study environment for labs (AWS CLI + Terraform)?  
**A:** **(1)** Install AWS CLI v2: `winget install Amazon.AWSCLI` (Windows) or `brew install awscli` (Mac). **(2)** Configure: `aws configure` (access key + secret + region + format). **(3)** Install Terraform: `winget install Hashicorp.Terraform`. **(4)** Verify: `aws sts get-caller-identity` returns account info. Use AWS Cloud9 as alternative — browser-based environment with no local setup.

---

**Q:** Which book is recommended to complement SAA-C03 study?  
**A:** **"AWS Certified Solutions Architect Study Guide" by Ben Piper and David Clinton** (Sybex/Wiley) — updated for SAA-C03, methodical approach, good pre-exam supplement. **"AWS Cookbook" by John Culkin** — more hands-on, practical recipes. Books are complementary (not substitutes) to practice exams. Priority: practice exams > books.

---

**Q:** What is the AWS "Exam Readiness" and how to interpret it?  
**A:** AWS Skill Builder has "Exam Readiness: SAA-C03" courses that map domains, explain question types, and elimination strategies. Additionally: a score of 80%+ on Tutorials Dojo practice exams in timed mode is generally considered sufficient readiness. Below 72% (80% equivalent on practice exams): continue studying identified weak points.

---

**Q:** Where to read about new AWS services and updates that may appear on the exam?  
**A:** **(1) AWS What's New:** aws.amazon.com/new — update feed. **(2) AWS Blog:** aws.amazon.com/blogs/aws — technical posts. **(3) re:Invent announcements:** YouTube/AWS Events. **(4) AWS Certification changelog:** AWS notifies when exam versions change with 6 months' notice. Focus: services listed in the official Exam Guide. Do not study out-of-scope services.

---

**Q:** How to create a 6-week study plan for SAA-C03?  
**A:** **Week 1:** Fundamental modules (EC2, S3, IAM, VPC). **Week 2:** Databases + Advanced Networking (RDS, DynamoDB, Route 53, CloudFront). **Week 3:** Serverless + Decoupling (Lambda, API GW, SQS, SNS, EventBridge). **Week 4:** Analytics + Migration + Well-Architected. **Week 5:** Full practice exams (2-3 full exams) + review mistakes. **Week 6:** Focus on weak points + final practice exam + rest.

---

**Q:** How to use Tutorials Dojo cheat sheets for final review?  
**A:** Tutorialsdojo.com/aws-cheat-sheets/ — available by service, free. Format: comparison tables, important numerical limits, differences between similar services. For review: print or save offline the cheat sheets for core services (EC2, S3, RDS/Aurora, VPC, IAM, Lambda, DynamoDB). Especially review comparison tables that the exam frequently tests (e.g., SQS vs SNS vs EventBridge).

---

**Q:** After obtaining SAA-C03 certification, how to keep it valid?  
**A:** Validity: **3 years**. To recertify: **(1)** Re-take SAA-C03 before expiration. **(2)** Obtain a higher-level certification (SAP-C02 Professional) — automatically recertifies SAA. **(3)** Obtain another Associate or specialty (does not automatically recertify). In the AWS Certification profile: you can download the digital certificate and Credly badge. Share on LinkedIn.

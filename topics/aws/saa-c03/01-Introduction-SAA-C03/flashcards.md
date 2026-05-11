# Flashcards — Introduction SAA-C03

---
**Q:** Which domain has the highest weight in SAA-C03?  
**A:** Design Resilient Architectures, at 30%.

---
**Q:** Which domain has the lowest formal weight?  
**A:** Design Cost-Optimized Architectures, at 18%.

---
**Q:** Does SAA-C03 test more service catalog knowledge or architectural decision-making?  
**A:** Architectural decision-making with context and trade-offs.

---
**Q:** What most differentiates SAA-C03 from CLF-C02?  
**A:** The depth of technical choices and justification between plausible alternatives.

---
**Q:** "Least operational overhead" typically points to what?  
**A:** Managed services, if they meet the requirement.

---
**Q:** Does Multi-AZ replace Multi-Region?  
**A:** No. Multi-AZ handles AZ failures; Multi-Region handles regional disasters.

---
**Q:** CloudFront vs Global Accelerator in one sentence?  
**A:** CloudFront is a CDN with cache; Global Accelerator accelerates global traffic without being an edge cache.

---
**Q:** RDS vs DynamoDB in initial reasoning?  
**A:** RDS for relational/transactional; DynamoDB for key-value/document with horizontal scale.

---
**Q:** SQS vs SNS in one sentence?  
**A:** SQS decouples with a queue; SNS distributes messages to multiple subscribers.

---
**Q:** Secrets Manager vs Parameter Store?  
**A:** Secrets Manager is stronger for secrets with native rotation.

---
**Q:** What does CloudTrail record?  
**A:** API calls and audit events in the AWS account.

---
**Q:** Which service group appears in a large portion of the exam?  
**A:** EC2, ELB, ASG, S3, VPC, IAM, RDS, DynamoDB, Lambda, Route 53, and KMS.

---
**Q:** "Minimal changes to the application" indicates what?  
**A:** Avoid alternatives that require major refactoring.

---
**Q:** Near real-time analytics tends to point to what?  
**A:** Streaming or event-driven processing, not late batch.

---
**Q:** Does the exam prefer more control or less operation?  
**A:** Less operation, as long as the functional and non-functional requirements are met.

---
**Q:** What does the exam measure beyond technical knowledge?  
**A:** The ability to read context and prioritize the correct trade-offs.

---
**Q:** What is the recommended default region for labs in this repository?  
**A:** us-east-1.

---
**Q:** What does "cost-effective" mean in an AWS question?  
**A:** Best balance between total cost and requirement, not just the lowest raw price.

---
**Q:** What is a common SAA-C03 preparation mistake?  
**A:** Studying too many rare services and neglecting the core blocks.

---
**Q:** How to best review over 8 weeks?  
**A:** Alternate dense theory, questions, short review, and practice exams in the final stretch.

---
**Q:** What to do when two alternatives seem correct?  
**A:** Re-read the main requirement, constraints, and qualifying words in the question.


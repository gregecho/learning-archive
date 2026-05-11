# Cheatsheet — Introduction SAA-C03

## 📌 Exam Weights

| Domain | Weight | Practical Focus |
|---|---:|---|
| Design Resilient Architectures | 30% | HA, DR, decoupling, fault tolerance |
| Design High-Performing Architectures | 28% | Compute, storage performance, database, cache, network |
| Design Secure Applications and Architectures | 24% | IAM, KMS, isolation, auditing, encryption |
| Design Cost-Optimized Architectures | 18% | Rightsizing, managed services, storage classes and purchase models |

## 🧠 Question Keywords

| Term | What it typically signals |
|---|---|
| least operational overhead | managed service |
| cost-effective | lowest total cost consistent with the requirement |
| highly available | multi-AZ, redundancy, failover |
| fault tolerant | failure tolerance without perceived downtime |
| near real-time | streaming, event, low latency |
| minimal changes | avoid major refactoring |
| securely | IAM, KMS, private endpoint, least privilege |
| global users | CloudFront, Route 53, Global Accelerator |

## 🧱 Most Frequent Services

| Group | Services |
|---|---|
| Compute | EC2, Auto Scaling, ELB, Lambda |
| Storage | S3, EBS, EFS |
| Database | RDS, Aurora, DynamoDB, ElastiCache |
| Network | VPC, Route 53, CloudFront, Transit Gateway |
| Security | IAM, KMS, Secrets Manager, Security Groups |
| Messaging | SQS, SNS, EventBridge |
| Observability | CloudWatch, CloudTrail, Config |

## ⚖️ Most Common Comparisons

| Comparison | Quick rule |
|---|---|
| CloudFront vs Global Accelerator | HTTP cache vs global traffic acceleration |
| RDS vs DynamoDB | relational/transactional vs highly scalable NoSQL |
| SQS vs SNS | decoupled queue vs pub/sub fan-out |
| Secrets Manager vs Parameter Store | secret rotation vs simple config/secret |
| Lambda vs EC2 | elastic serverless vs granular control |
| Multi-AZ vs Multi-Region | regional HA vs full regional DR |

## ⏱️ Exam Time Management

| Item | Reference |
|---|---|
| Questions | 65 |
| Total time | 130 minutes |
| Average target per question | ~2 minutes |
| Long questions | flag, move on, and return |
| Final review | reserve 10 to 15 minutes |

## 🚫 Common Pitfalls

| Pitfall | Correction |
|---|---|
| choosing the most complex solution | choose the one most aligned with the requirement |
| ignoring operations | include administrative effort in the decision |
| confusing HA with DR | HA does not replace a multi-region plan |
| overestimating rare services | focus on the exam core |
| memorizing without context | practice complete scenarios |


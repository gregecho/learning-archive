# Links and Resources — IAM and Security (Module 09)

## Official AWS Documentation

- [AWS IAM — Official Documentation](https://docs.aws.amazon.com/IAM/latest/UserGuide/introduction.html)
- [IAM — Policy Evaluation Logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html)
- [IAM — Permissions Boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html)
- [IAM — Service Control Policies (SCP)](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html)
- [IAM — ABAC with Tags](https://docs.aws.amazon.com/IAM/latest/UserGuide/tutorial_attribute-based-access-control.html)
- [AWS STS — AssumeRole](https://docs.aws.amazon.com/STS/latest/APIReference/API_AssumeRole.html)
- [IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html)
- [Amazon GuardDuty](https://docs.aws.amazon.com/guardduty/latest/ug/what-is-guardduty.html)
- [AWS Security Hub](https://docs.aws.amazon.com/securityhub/latest/userguide/what-is-securityhub.html)
- [Amazon Macie](https://docs.aws.amazon.com/macie/latest/user/what-is-macie.html)
- [AWS WAF](https://docs.aws.amazon.com/waf/latest/developerguide/waf-chapter.html)
- [AWS Shield](https://docs.aws.amazon.com/waf/latest/developerguide/shield-chapter.html)

## FAQs

- [AWS IAM FAQ](https://aws.amazon.com/iam/faqs/)
- [Amazon GuardDuty FAQ](https://aws.amazon.com/guardduty/faqs/)

## Whitepapers

- [AWS Security Best Practices](https://docs.aws.amazon.com/whitepapers/latest/aws-security-best-practices/aws-security-best-practices.html)
- [Security Pillar — Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)

## AWS Blog Articles

- [IAM least privilege: patterns and practices](https://aws.amazon.com/blogs/security/techniques-for-writing-least-privilege-iam-policies/)
- [ABAC with AWS IAM and resource tags](https://aws.amazon.com/blogs/security/attribute-based-access-control-with-aws-services/)
- [How to use STS AssumeRole with ExternalId](https://aws.amazon.com/blogs/security/how-to-use-external-id-when-granting-access-to-your-aws-resources/)

## Study Tools

- [Tutorials Dojo — AWS IAM Cheat Sheet](https://tutorialsdojo.com/aws-identity-and-access-management-iam/)
- [AWS IAM Policy Simulator](https://policysim.aws.amazon.com/)

## Security Services Comparison

| Service | What it detects / protects | Type |
|---------|---------------------------|------|
| GuardDuty | Suspicious behavior (accounts, workloads, data) | Threat detection |
| Macie | Sensitive data (PII) in S3 | Data discovery |
| Inspector | Vulnerabilities in EC2/ECR/Lambda | Vulnerability assessment |
| WAF | Malicious HTTP requests (SQL inj, XSS) | Application protection |
| Shield Standard | Automatic DDoS L3/L4 | DDoS protection |
| Shield Advanced | Advanced DDoS + 24/7 support | Premium DDoS protection |
| Config | Configuration compliance | Configuration auditing |
| Security Hub | Security findings aggregator | Consolidated view |

---

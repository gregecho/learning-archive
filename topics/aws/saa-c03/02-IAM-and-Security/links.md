# Reference Links — IAM and Security

## Official AWS Documentation

### IAM
- [IAM User Guide](https://docs.aws.amazon.com/IAM/latest/UserGuide/) — Complete Identity and Access Management guide
- [IAM Policy Reference](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies.html) — Complete JSON policy grammar
- [IAM Policy Evaluation Logic](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_evaluation-logic.html) — How IAM evaluates permissions
- [Permission Boundaries](https://docs.aws.amazon.com/IAM/latest/UserGuide/access_policies_boundaries.html) — Permission Boundaries guide
- [IAM Condition Keys](https://docs.aws.amazon.com/IAM/latest/UserGuide/reference_policies_condition-keys.html) — Complete list of global condition keys

### IAM Identity Center
- [IAM Identity Center User Guide](https://docs.aws.amazon.com/singlesignon/latest/userguide/) — AWS SSO / Identity Center
- [Permission Sets Reference](https://docs.aws.amazon.com/singlesignon/latest/userguide/permissionsetsconcept.html) — Permission Sets concept

### AWS Organizations + SCPs
- [AWS Organizations User Guide](https://docs.aws.amazon.com/organizations/latest/userguide/) — Organizations and SCPs
- [Service Control Policies](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps.html) — SCPs in detail
- [SCP Examples](https://docs.aws.amazon.com/organizations/latest/userguide/orgs_manage_policies_scps_examples.html) — Practical SCP examples

### KMS
- [KMS Developer Guide](https://docs.aws.amazon.com/kms/latest/developerguide/) — Complete KMS guide
- [KMS Key Policy](https://docs.aws.amazon.com/kms/latest/developerguide/key-policies.html) — How key policies work
- [Envelope Encryption](https://docs.aws.amazon.com/kms/latest/developerguide/concepts.html#enveloping) — Envelope encryption concept
- [KMS Grants](https://docs.aws.amazon.com/kms/latest/developerguide/grants.html) — Grants vs Key Policies
- [Multi-Region Keys](https://docs.aws.amazon.com/kms/latest/developerguide/multi-region-keys-overview.html) — Multi-region keys

### Secrets Manager
- [Secrets Manager User Guide](https://docs.aws.amazon.com/secretsmanager/latest/userguide/) — Complete guide
- [Rotating Secrets](https://docs.aws.amazon.com/secretsmanager/latest/userguide/rotating-secrets.html) — How rotation works
- [Secrets Manager vs Parameter Store](https://docs.aws.amazon.com/systems-manager/latest/userguide/integration-ps-secretsmanager.html) — Official comparison

### Parameter Store
- [Parameter Store User Guide](https://docs.aws.amazon.com/systems-manager/latest/userguide/systems-manager-parameter-store.html)
- [Working with SecureString](https://docs.aws.amazon.com/systems-manager/latest/userguide/sysman-paramstore-securestring.html)

### ACM
- [ACM User Guide](https://docs.aws.amazon.com/acm/latest/userguide/) — Certificate Manager
- [ACM Private CA](https://docs.aws.amazon.com/privateca/latest/userguide/) — Managed private CA

---

## Whitepapers and Best Practices

- [Security Pillar — AWS Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/) — Security pillar of WAFR
- [IAM Best Practices](https://docs.aws.amazon.com/IAM/latest/UserGuide/best-practices.html) — Official AWS best practices
- [Security Best Practices in IAM](https://aws.amazon.com/architecture/security-identity-compliance/) — Security architecture
- [Organizing Your AWS Environment Using Multiple Accounts](https://docs.aws.amazon.com/whitepapers/latest/organizing-your-aws-environment/) — Multi-account whitepaper

---

## AWS re:Invent and Technical Talks

- [IAM Policy Evaluation Deep Dive (re:Invent)](https://www.youtube.com/results?search_query=aws+reinvent+iam+policy+evaluation) — Search on YouTube: "AWS re:Invent IAM policy evaluation"
- [Delegating Access to KMS Keys](https://aws.amazon.com/blogs/security/how-to-restrict-amazon-sns-topic-access-to-only-allow-specific-aws-services/) — AWS Security Blog

---

## Important FAQs for the Exam

- [IAM FAQ](https://aws.amazon.com/iam/faqs/)
- [KMS FAQ](https://aws.amazon.com/kms/faqs/)
- [Secrets Manager FAQ](https://aws.amazon.com/secrets-manager/faqs/)

---

## Useful Tools

- [AWS Policy Simulator](https://policysim.aws.amazon.com/) — Test IAM policies without real effect
- [AWS Policy Generator](https://awspolicygen.s3.amazonaws.com/policygen.html) — Generate policies visually
- [IAM Access Analyzer](https://docs.aws.amazon.com/IAM/latest/UserGuide/what-is-access-analyzer.html) — Detect unintended external access

---

## Key SAA-C03 Concepts in This Module

| Concept | Exam Frequency |
|---|---|
| Policy evaluation order (explicit deny priority) | High |
| Permission Boundary for delegating role creation | High |
| SCPs do not affect management account | High |
| KMS envelope encryption | High |
| Secrets Manager vs Parameter Store | Medium |
| ACM + CloudFront requires us-east-1 | High |
| aws:PrincipalOrgID for bucket policies | Medium |
| KMS Multi-Region Keys | Medium |


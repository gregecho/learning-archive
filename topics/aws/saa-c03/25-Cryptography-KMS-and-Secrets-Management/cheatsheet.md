# Cheatsheet - Cryptography, KMS and Secrets Management

## Quick map

| Need | Best choice | Note |
|---|---|---|
| Key with policy control and auditing | KMS customer-managed key | More control for compliance |
| Automatic secret rotation | Secrets Manager | Strong RDS integration |
| App parameters at low cost | Parameter Store | SecureString uses KMS |
| TLS certificate for ALB/CloudFront/API Gateway | ACM | Free public cert |
| Cryptographic control in dedicated HSM | CloudHSM | Greater operational complexity |

## Exam rules

- key policy is essential for KMS permissions
- explicit deny always prevails
- use IAM role for apps instead of static keys
- CloudFront + ACM public => certificate in us-east-1

## Pitfalls

- confusing Secrets Manager with Parameter Store in automatic rotation scenario
- forgetting kms:Decrypt permission on the consumer principal
- assuming that encrypting in the service eliminates access management
- ignoring KMS call costs at high throughput

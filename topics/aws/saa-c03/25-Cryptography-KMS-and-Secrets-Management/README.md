# 25 Cryptography, KMS and Secrets Management

## Module objectives

- master encryption at rest and in transit in the SAA-C03 context
- differentiate AWS KMS, CloudHSM, Secrets Manager, Parameter Store, and ACM
- decide between AWS-managed and customer-managed keys based on compliance
- apply security patterns with lower operational overhead

## Fundamental concepts

The SAA-C03 exam covers applied security: it is not enough to know the service name, you need to choose the best combination of encryption, access control and secret rotation.

## KMS in practice

- KMS manages keys and auditable cryptographic operations.
- Customer managed keys allow policy control, rotation and grants.
- Key policy is mandatory for correct access.
- Envelope encryption is standard for data at scale.

Summary flow of envelope encryption:
1. application requests data key from KMS (GenerateDataKey)
2. KMS returns plaintext and encrypted data key
3. application encrypts data with the plaintext key
4. stores encrypted data + encrypted data key

## Secrets and certificates

- Secrets Manager: secrets with automatic rotation (strong for database credentials).
- Parameter Store SecureString: configurations and simple secrets, lower cost.
- ACM: TLS certificates for ALB, CloudFront and API Gateway.
- ACM Private CA: issuance of internal private certificates.

## Exam tips

- if there is a requirement for automatic credential rotation, the answer tends to be Secrets Manager.
- if the exam asks for "full control over encryption keys", use customer managed KMS key.
- if a dedicated HSM and specialized cryptographic control is needed, consider CloudHSM.
- for CloudFront with ACM, the public certificate must be in us-east-1.
- encryption without permission control does not address risk; IAM + key policy matter.

## Related links

- [Cheatsheet](./cheatsheet.md)
- [Use cases](./use-cases.md)
- [Questions](./questions.md)
- [Flashcards](./flashcards.md)
- [Lab](./lab.md)
- [Official links](./links.md)

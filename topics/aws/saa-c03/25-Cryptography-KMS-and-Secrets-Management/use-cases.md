# Use Cases - Cryptography, KMS and Secrets Management

## Case 1: Relational database with password rotation

Scenario:
- ECS application accesses Aurora
- audit requires automatic rotation

Architecture:
- Secrets Manager with rotation
- ECS task role to read secret
- KMS customer-managed key for secret encryption

## Case 2: Public API with managed TLS

Scenario:
- API Gateway + CloudFront
- no manual certificate management

Architecture:
- ACM public with automatic renewal
- certificate in us-east-1 for CloudFront

## Case 3: Company with strict key control requirements

Scenario:
- compliance requires segregation of key access

Architecture:
- customer-managed keys in KMS
- minimal key policy + grants for applications
- audit trail via CloudTrail

## Case 4: Legacy application with secret in file

Scenario:
- hardcoded password in code

Architecture:
- migrate to Parameter Store/Secrets Manager
- remove credential from repository
- use IAM role at runtime

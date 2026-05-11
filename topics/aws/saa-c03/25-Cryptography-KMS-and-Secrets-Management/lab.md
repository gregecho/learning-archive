# Lab - KMS + Secrets Manager + IAM Role

## Objective
Protect application credentials using rotatable secret and role-based access.

## Steps

1. Create a KMS customer-managed key for secrets.
2. Create a secret in Secrets Manager (test username/password) using the key.
3. Create IAM role for workload (EC2/Lambda) with permissions `secretsmanager:GetSecretValue` and `kms:Decrypt`.
4. Associate the role to the compute resource.
5. Read the secret via SDK/CLI without static credentials.
6. Enable automatic rotation (when applicable).

## Validation

- workload reads secret with role
- access denied for principal without permission
- access events appear in CloudTrail

## Cleanup

- remove lab secret
- remove role/policies and created key

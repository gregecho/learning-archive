# Flashcards — IAM and Security

> Review one card at a time. Try to answer before revealing the answer.

---

**Q:** What is the difference between IAM User and IAM Role?  
**A:** User has permanent credentials (password + access key). Role provides temporary credentials via STS, assumed by AWS services, other accounts, or federated identities. It never has its own password or access key.

---

**Q:** What is a Permission Boundary and what is it used for?  
**A:** It is a managed IAM policy that defines the maximum permissions a user or role can have — even if the identity policy grants more. Used to delegate role creation without privilege escalation.

---

**Q:** What is the difference between AWS-managed policy, Customer-managed policy, and Inline policy?  
**A:** AWS-managed: maintained by AWS, reusable, not editable. Customer-managed: you create and control it, reusable across multiple identities. Inline: embedded in the identity, 1:1, deleted with it — avoid except for exclusive permissions.

---

**Q:** In IAM policy evaluation, what comes first: SCP, Permission Boundary, or identity policy?  
**A:** Explicit Deny (any source) → SCP blocks? → Permission Boundary blocks? → Identity policy or resource policy allows? For cross-account access: both identity AND resource policy must allow.

---

**Q:** What does the `aws:PrincipalOrgID` condition do?  
**A:** Restricts access to a resource only to principals belonging to a specific AWS Organization. Useful in bucket policies to ensure only company accounts access the bucket, without listing each account ID.

---

**Q:** What is an SCP and who does it affect?  
**A:** Service Control Policy — maximum permission guardrail in AWS Organizations. Applies to all member accounts and OUs, but NEVER to the management account. An explicit allow in the SCP does not grant permission on its own — the identity policy still needs to allow it.

---

**Q:** What is the difference between `aws:SourceVpc` and `aws:SourceVpce`?  
**A:** `aws:SourceVpc` restricts to the VPC ID. `aws:SourceVpce` restricts to the specific VPC Endpoint ID. Use `aws:SourceVpce` when you want to ensure only access via a specific endpoint is allowed.

---

**Q:** What is IAM Identity Center (formerly AWS SSO) used for?  
**A:** Centralized single sign-on for multiple AWS accounts and SaaS applications. Allows creating permission sets (collection of policies) and assigning them to users/groups per account. Integrates with AD, Okta, and other identity providers via SAML 2.0/SCIM.

---

**Q:** What are the three types of KMS CMKs?  
**A:** 1) AWS-owned: managed by AWS, no visibility for the customer, no additional cost (e.g.: S3 SSE with aws/s3). 2) AWS-managed CMK: created by the service in your account (aws/ebs), visible, automatic annual rotation, cannot edit key policy. 3) Customer-managed CMK: you create it, pay per month, edit key policy, define rotation, can disable.

---

**Q:** What is envelope encryption?  
**A:** A pattern where: (1) KMS generates a Data Key (plaintext + encrypted with the CMK); (2) the client uses the plaintext data key to encrypt the data; (3) discards the plaintext key and stores the encrypted data key with the data; (4) to decrypt, sends the encrypted data key to KMS and uses the returned plaintext key.

---

**Q:** What is the purpose of the KMS key policy?  
**A:** Defines who can manage and use the CMK. It is mandatory — every CMK needs a key policy. The policy includes the root account as administrator (ensures recovery), key administrators, and key users. It is a resource-based policy, therefore allows cross-account without role assumption.

---

**Q:** What are KMS Grants and when to use them?  
**A:** Grants provide temporary and programmatic permission to use a CMK without changing the key policy. They are created via `CreateGrant` and the grant token is passed in API calls (`kms:decrypt --grant-tokens`). Used by AWS services internally (e.g.: EBS when creating a snapshot of an encrypted volume).

---

**Q:** What are KMS Multi-Region Keys?  
**A:** Keys that have the same key material replicated across multiple regions. They allow encrypting in us-east-1 and decrypting in eu-west-1 without re-encrypting. Key ARNs are different but the material is the same. Useful for cross-region DR with encrypted data.

---

**Q:** What is the main difference between Secrets Manager and Parameter Store?  
**A:** Secrets Manager: native automatic rotation (integrates with RDS, Redshift, DocumentDB), charges per secret per month. Parameter Store: no native rotation, Standard free (max 4KB), SecureString uses KMS. Secrets Manager is preferable for credentials with rotation; Parameter Store for application configs.

---

**Q:** What is ACM and what are its limitations?  
**A:** AWS Certificate Manager manages SSL/TLS certificates. Public certificates are free and automatically renewed. They can only be used with integrated AWS services (ALB, CloudFront, API Gateway) — they cannot be exported. For CloudFront, the certificate must be in us-east-1.

---

**Q:** What is ACM Private CA?  
**A:** A private Certificate Authority managed by AWS. Issues private certificates for internal services (mTLS, microservices). Has a monthly cost per CA + per certificate. Certificates issued ARE exportable, unlike public ACM certificates.

---

**Q:** How does cross-account role assumption work?  
**A:** Account A creates a role with a trust policy allowing account B to assume it (sts:AssumeRole). Account B creates a policy allowing sts:AssumeRole on the ARN of account A's role. The user in account B calls AssumeRole and receives temporary credentials from account A.

---

**Q:** Which IAM condition requires MFA in an API call?  
**A:** `"Condition": {"Bool": {"aws:MultiFactorAuthPresent": "true"}}` — ensures the operation only occurs when the principal authenticated with MFA. Useful for protecting sensitive actions like deleting S3 objects or disabling a CMK.

---

**Q:** What is the difference between identity-based policy and resource-based policy for cross-account access?  
**A:** With resource-based policy (e.g.: S3 bucket policy, KMS key policy) that explicitly allows the principal from another account: direct access without role assumption. With identity-based policy only: need to assume a role. Resource-based policies allow cross-account without a role hop — considered more direct for services that support it.

---

**Q:** What is Parameter Store SecureString and what are its KMS key options?  
**A:** SecureString encrypts the value using KMS. It can use the aws/ssm CMK (no CMK cost, but no key policy control) or a customer-managed CMK (full control, auditing, can revoke access). For cross-account use, customer-managed CMK is required.

---

**Q:** What does `"Effect": "Deny"` mean in an IAM policy vs SCP?  
**A:** In both cases, explicit Deny overrides any Allow in any other policy. In IAM: if any applicable policy has Deny for the action, the call is denied. In SCP: Deny blocks the entire account/OU, even if identity policies allow it.


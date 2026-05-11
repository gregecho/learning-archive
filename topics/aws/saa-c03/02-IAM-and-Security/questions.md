# Questions — IAM and Security

## Question 1
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Medium

A security team wants to ensure that developers can create IAM roles for their applications, but that these roles can never have permission to access the AWS billing service or export KMS keys. Which IAM mechanism should be configured?

- A) AWS Organizations SCP applied to the developers' OU
- B) IAM Permission Boundary applied to roles created by developers
- C) IAM Group with Explicit Deny for Billing and KMS
- D) S3 Bucket Policy with PrincipalOrgID condition

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

Permission Boundaries define the ceiling of effective permissions for a role or user. Even if a developer creates a role with full access permission, if the boundary does not include Billing or KMS:ExportKey, those accesses are blocked. Option A would be correct for restricting an entire account, but does not solve the problem of roles created by the developers themselves within the account. Option C blocks the dev group, but not the roles they create. Option D is an S3 resource-based policy, which does not solve this case.

**Key concept:** Permission Boundary as a ceiling for controlled delegation
</details>

## Question 2
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Hard

A company has multiple AWS accounts in an organization. The security team wants to ensure that no account, regardless of any local admin, can disable CloudTrail. Which solution resolves this?

- A) Create IAM Permission Boundary with Deny for cloudtrail:StopLogging in each account
- B) Create an SCP in the organization with Deny for cloudtrail:StopLogging and apply to the root
- C) Create IAM Policy with Deny for CloudTrail at the account level
- D) Configure a bucket policy on the CloudTrail bucket

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

SCPs applied to the organization root affect all accounts (except the management account) and no local administrator can override an explicit SCP deny. Option A requires configuration in each account individually and can be removed by a local admin. Option C is an IAM policy that can also be modified by an account admin. Option D protects the bucket, but does not prevent StopLogging or DeleteTrail before logs reach the bucket.

**Key concept:** SCP as an immutable organizational guardrail for local admins
</details>

## Question 3
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Medium

A Flask application running on EC2 needs to read database secrets with automatic rotation every 30 days. The compliance requirement states that credentials must never be stored in code or configuration files. What is the most appropriate solution?

- A) Store credentials in environment variables on the instance
- B) Use AWS Secrets Manager with IAM role on EC2 and configured automatic rotation
- C) Store credentials in Parameter Store Standard and read in cloud-init
- D) Embed credentials in the instance User Data

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

Secrets Manager is the preferred solution for rotatable credentials. EC2 uses an IAM role (Instance Profile) to call the Secrets Manager API without exposing credentials. Automatic rotation is native for RDS, Redshift, and other databases. Option A stores in plaintext in environment variables. Option C has no native rotation. Option D exposes credentials in User Data, visible via metadata.

**Key concept:** Secrets Manager + Instance Profile for rotatable credentials
</details>

## Question 4
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Hard

A team wants calls to Amazon S3 from a specific VPC to be allowed only for objects with the prefix `/reports/`. Via bucket policy, which combination of elements correctly implements this?

- A) Condition: aws:SourceIp pointing to the VPC CIDR + resource with prefix /reports/*
- B) Condition: aws:SourceVpce pointing to the VPC Endpoint ID + resource with prefix /reports/*
- C) Permission Boundary with s3:prefix = /reports/
- D) SCP with Condition: aws:SourceVpc and bucket resource

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

`aws:SourceVpce` identifies traffic passing through a specific VPC Endpoint, being more precise than the VPC IP (which can change). Combined with the resource `arn:aws:s3:::bucket/reports/*`, it restricts access to the correct prefix. Option A uses IP, which is not the recommended way for VPC restriction. Option C applies Permission Boundary, which does not solve the prefix restriction in bucket policy. Option D: SCPs do not operate on resource policies of specific services.

**Key concept:** aws:SourceVpce in bucket policy for access via VPC Endpoint
</details>

## Question 5
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Medium

A company encrypts data in Amazon RDS using KMS. An auditor wants to verify which type of CMK was used to ensure the company controls the entire key lifecycle. Which type of CMK meets this requirement?

- A) AWS-owned CMK
- B) AWS-managed CMK (aws/rds)
- C) Customer-managed CMK created by the customer
- D) Data key generated by RDS

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: C**

Only the customer-managed CMK gives the customer full control: key policy definition, enable/disable, controlled rotation, and audit via CloudTrail with detail level. AWS-owned CMK is not visible in the account. AWS-managed CMK is visible, but the customer does not manage it. Data key is derived from a CMK and is not what the auditor is asking about.

**Key concept:** customer-managed CMK for cryptographic lifecycle control
</details>

## Question 6
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Medium

A new feature needs to request objects from S3 in account B from a Lambda in account A. The team prefers to avoid creating a role in account B for simplicity. Which approach works?

- A) Add an SCP in account B that allows the Lambda ARN
- B) Add account A as a principal in the bucket policy of the bucket in account B
- C) Create an IAM user in account B and use the credentials in account A's Lambda
- D) Configure VPC Peering between the accounts

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

A resource-based policy (bucket policy) can specify a principal from another account without needing to create a role. The Lambda in account A needs permission for s3:GetObject in its execution role, and the bucket in account B needs the bucket policy that allows that ARN. This is the simplest form of cross-account without role assumption. Option A: SCP does not grant permission, only restricts. Option C shares long-term credentials, a bad practice. Option D does not resolve IAM; VPC Peering is about networking.

**Key concept:** cross-account via resource-based policy without role assumption
</details>

## Question 7
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Hard

An architect needs to implement envelope encryption for sensitive data stored in S3. What is the correct sequence of operations?

- A) Encrypt the data with the CMK directly, store in S3
- B) Generate a data key via KMS, encrypt the data with it in plaintext, encrypt the data key with the CMK, store encrypted data + encrypted data key
- C) Store the data key in plaintext along with the encrypted data
- D) Use only the data key without any CMK

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

Envelope encryption works: (1) GenerateDataKey call to KMS returns data key in plaintext and ciphertext; (2) encrypt the data with the plaintext data key; (3) discard the plaintext data key from memory; (4) store the encrypted data along with the ciphertext data key. To decrypt, send the ciphertext data key to KMS (Decrypt) to get the plaintext back. Option A encrypts directly with CMK, which is inefficient for large volumes and does not scale. Option C exposes the data key. Option D does not protect the data key.

**Key concept:** correct sequence of envelope encryption with KMS
</details>

## Question 8
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Medium

A multinational company wants all employees from different subsidiaries to access multiple AWS accounts with single sign-on (SSO) via the existing corporate Active Directory. Which service is most appropriate?

- A) Create IAM Users in each AWS account
- B) IAM Identity Center integrated with Active Directory via SAML or SCIM
- C) AWS Cognito User Pools
- D) IAM Roles with ADFS as IdP per account individually

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

IAM Identity Center offers centralized access management for multiple accounts, native AD integration via AWS Managed AD or AD Connector (also supports SAML/SCIM with other IDPs like Okta), and permission sets that map access level per account. Eliminates the need to manage IAM users in each account. Option A is the highest-effort and least secure approach. Option C is for customer/application user authentication, not internal employees. Option D is operationally complex to maintain at scale.

**Key concept:** IAM Identity Center for centralized multi-account SSO
</details>

## Question 9
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Medium

A developer inadvertently deleted a customer-managed CMK from KMS that was being used to encrypt data in EBS. What is the state of the CMK after the delete action?

- A) The CMK is deleted immediately and the data is unrecoverable
- B) The CMK enters a waiting period of 7 to 30 days before effective deletion, which can be cancelled
- C) The CMK is disabled but remains available indefinitely
- D) The CMK is automatically archived in S3

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

KMS implements a waiting period of 7 to 30 days (configurable, default 30 days) before the effective deletion of a CMK. During this period, the deletion can be cancelled. No cryptographic operations can be performed with the key during the waiting period. This protects against accidental deletion. If deletion occurs, data encrypted exclusively by that key becomes unrecoverable.

**Key concept:** CMK deletion waiting period in KMS
</details>

## Question 10
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Medium

An application with multiple microservices uses a VPC with private subnets. Each microservice needs access to S3 without exposing traffic to the public internet. Which solution is most efficient and secure?

- A) Configure NAT Gateway for S3 traffic
- B) Create a VPC Gateway Endpoint for S3
- C) Create a VPC Interface Endpoint for S3
- D) Use Direct Connect to access S3

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

The Gateway Endpoint for S3 (and DynamoDB) is free and accessed via route table. Traffic stays within the AWS network without needing a NAT Gateway. It is the most economical solution. Option A involves NAT Gateway processing and transfer costs in addition to routing to the internet. Option C: Interface Endpoint for S3 (PrivateLink) also works, but has an hourly and per-GB cost — preferable when S3 needs to be accessed from on-premises via Direct Connect. Option D is for on-premises connectivity.

**Key concept:** Gateway Endpoint for S3 without data cost vs Interface Endpoint with cost
</details>

## Question 11
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Easy

An IAM policy has the following statements: an Allow for s3:GetObject on any bucket, and an explicit Deny for s3:GetObject on the `confidential-logs` bucket. What happens when the user tries to access an object in `confidential-logs`?

- A) The Allow from the first statement prevails
- B) The explicit Deny prevails and access is denied
- C) It depends on the order of statements in the JSON
- D) Another Allow policy is needed to resolve the conflict

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

The fundamental rule of IAM evaluation is: an explicit Deny always overrides any Allow, regardless of the order of statements or how many policies allow it. There is no way for an Allow to overcome an explicit Deny in the same account.

**Key concept:** explicit Deny has absolute priority over Allow
</details>

## Question 12
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Hard

A company wants TLS certificates for APIs exposed via ALB to be centrally managed, with automatic renewal without manual intervention. Which combination of services resolves this?

- A) CloudFront with a self-signed certificate created by the team
- B) ACM with a public certificate for the domain, DNS validation, integrated with ALB
- C) Generate certificate with OpenSSL, import into IAM, and attach to ALB
- D) EC2 with Nginx managing certificates manually

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

ACM provisions and renews public certificates automatically. DNS validation is the preferred method because it is automated via CNAME record. The certificate is integrated directly with ALB without needing to export the private key. Option A is not centralized management and self-signed is not for production. Option C requires manual deletion and recreation on renewal. Option D unnecessarily increases operational effort.

**Key concept:** ACM with DNS validation for zero-touch renewal
</details>

## Question 13
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Medium

A team needs to differentiate Parameter Store from Secrets Manager when choosing where to store a boolean feature flag without sensitive value and a rotatable database password. Which allocation is correct?

- A) Both in Secrets Manager for standardization
- B) Feature flag in Parameter Store Standard; database password in Secrets Manager
- C) Both in Parameter Store Advanced
- D) Feature flag in Secrets Manager; database password in EC2 Systems Manager agent

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

Parameter Store Standard is free and ideal for non-sensitive configuration or simple secrets without rotation. Secrets Manager is most appropriate for credentials requiring automatic rotation. Using Secrets Manager for feature flags pays for something that did not need it. Option C uses Advanced without need. Option D mixes concepts incorrectly.

**Key concept:** Parameter Store for config/simple secrets; Secrets Manager for rotation
</details>

## Question 14
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Hard

An organization needs a KMS key to be used in both us-east-1 and eu-west-1 to encrypt and decrypt data without needing re-encryption when moving data between regions. Which KMS feature meets this requirement?

- A) Cross-region replication of CMK via S3
- B) KMS Multi-Region Keys with replica in eu-west-1
- C) Use the same exported data key in both regions
- D) Create independent CMKs in each region and use AWS DataSync to synchronize

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

Multi-Region Keys share the same key material between different regions, using the same key ID (with mrk- prefix). Data encrypted in us-east-1 can be decrypted in eu-west-1 without re-encryption, as the keys are cryptographically equivalent. Option A does not exist. Option C: exported data key exposes the material outside KMS — breaks the security model. Option D creates keys with different materials, preventing direct cross-region decrypt.

**Key concept:** KMS Multi-Region Keys for cross-region encrypt/decrypt
</details>

## Question 15
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Medium

An EC2 in a production environment needs only permissions to put metrics in CloudWatch and nothing else. What is the best least-privilege approach?

- A) Create an IAM User with the AmazonCloudWatchFullAccess policy
- B) Create an IAM Role with a customer-managed policy granting only cloudwatch:PutMetricData and associate with the instance via Instance Profile
- C) Create an IAM Group with CloudWatch permission and add the instance to the group
- D) Use the admin access key in the AWS_ACCESS_KEY_ID environment variable

<details>
<summary>✅ Answer and Explanation</summary>

**Correct answer: B**

IAM Roles with Instance Profile provide automatically rotated temporary credentials. The policy should be minimal: only `cloudwatch:PutMetricData` on resource `*`. Avoids use of long-term credentials. Option A uses a user (long-term credentials) and Full Access permissions — violates least privilege. Option C: instances cannot be members of IAM groups. Option D is the worst practice: hardcoded credentials in the environment.

**Key concept:** Instance Profile + least privilege policy for EC2
</details>


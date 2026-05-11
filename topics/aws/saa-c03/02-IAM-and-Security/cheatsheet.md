# Cheatsheet — IAM and Security

## IAM Policy Types

| Type | Managed by | Reusable | Coexists with identity | Binding |
|---|---|---|---|---|
| AWS Managed Policy | AWS | Yes | Yes | 1:N |
| Customer Managed Policy | You | Yes | Yes | 1:N |
| Inline Policy | You | No | Yes | 1:1 (deleted with identity) |
| Resource-Based Policy | You | N/A | N/A | On the resource |
| Permission Boundary | You | Yes | Limits identity | Max permissions |
| SCP | Org admin | Yes | Limits account | Guardrail per OU/account |

---

## Permission Evaluation Logic

```
1. Explicit DENY in any policy?                → DENY (end)
2. Organization SCP allows the action?         → no? DENY
3. Permission Boundary allows the action?      → no? DENY
4. Identity Policy allows?                     → yes? ALLOW (same account)
   └── Resource Policy allows?                 → yes? ALLOW (cross-account without role assumption)
5. None of the options allowed?                → implicit DENY
```

> **Cross-account without Resource Policy:** BOTH identity policy AND resource policy must allow.  
> **Cross-account WITH Resource Policy (e.g.: S3, KMS):** Resource policy can allow on its own (but boundary and SCP still apply).

---

## Most Tested IAM Conditions

| Condition | Example use |
|---|---|
| `aws:RequestedRegion` | Restrict actions to `us-east-1` and `sa-east-1` |
| `aws:MultiFactorAuthPresent: true` | Require MFA for sensitive actions |
| `aws:PrincipalOrgID` | Limit S3 bucket access to the entire Org |
| `aws:SourceVpc` / `aws:SourceVpce` | Restrict access only from VPC/endpoint |
| `aws:CurrentTime` | Time window for access |
| `s3:prefix` | Restrict ListBucket to a specific prefix |
| `iam:PassedToService` | Control which services a role can be delegated to |

---

## KMS — CMK Types

| Type | Managed by | Cost | Rotation | Editable | Visible |
|---|---|---|---|---|---|
| AWS-owned | AWS (internal) | No cost | Automatic by AWS | No | No |
| AWS-managed | AWS (your account) | No cost per CMK | Annual automatic | No | Yes |
| Customer-managed | You | $1/month + $0.03/10K API | Optional annual | Yes | Yes |

**Key Material Origin:** `AWS_KMS` (default) | `EXTERNAL` (import) | `AWS_CLOUDHSM`

---

## KMS — Envelope Encryption (Sequence)

```
Encrypt:
  1. GenerateDataKey(CMK ARN)
     → receives: Plaintext data key + Encrypted data key
  2. Use Plaintext key to encrypt data (AES-256-GCM)
  3. Erase Plaintext key from memory
  4. Store: Encrypted data + Encrypted data key

Decrypt:
  1. Decrypt(Encrypted data key, CMK ARN)
     → receives: Plaintext data key
  2. Use Plaintext key to decrypt data
  3. Erase Plaintext key from memory
```

---

## Secrets Manager vs Parameter Store

| Feature | Secrets Manager | Parameter Store |
|---|---|---|
| Automatic rotation | ✅ Native (Lambda) | ❌ (external trigger) |
| RDS/Redshift/DocDB integration | ✅ Native | ❌ |
| Cost | $0.40/secret/month + API | Standard: free; Advanced: $0.05/param/month |
| Maximum size | 64 KB | 4 KB (standard), 8 KB (advanced) |
| Versioning | ✅ (staging labels) | ✅ |
| Cross-account | ✅ (resource policy) | With customer CMK |
| Hierarchical paths | Limited | ✅ (`/app/prod/db`) |
| Best for | DB credentials with rotation | App configurations, parameters |

---

## ACM — Summary

| Feature | Public ACM | ACM Private CA |
|---|---|---|
| Cost | Free | ~$400/month per CA + $0.75/cert |
| Exportable | ❌ No | ✅ Yes |
| Renewal | Automatic | Automatic |
| Validation | DNS (preferred) or Email | No external validation |
| Use | ALB, CloudFront, API GW | Internal microservices, mTLS |
| CloudFront region | ⚠️ Certificate must be in us-east-1 | — |

---

## Cross-Account Access Patterns

| Scenario | Mechanism |
|---|---|
| S3 access from another account | Bucket policy + (role or user with identity policy) |
| KMS CMK access from another account | Key policy on CMK + identity policy on caller |
| Assume role in another account | Trust policy on role + iam:AssumeRole on caller |
| Share RDS snapshot | Share snapshot with destination account ID |
| Access via PrivateLink | VPC Endpoint + NLB + VPC Endpoint Service policy |

---

## IAM Identity Center — Concepts

```
AWS Organizations
  └── IAM Identity Center (SSO)
        ├── Identity Source: Built-in / AD / External IdP (SAML/SCIM)
        ├── Users & Groups
        ├── Permission Sets (= Collection of IAM policies)
        └── Account Assignments
              ├── Account A → User X → Permission Set Admin
              ├── Account B → Group Y → Permission Set ReadOnly
              └── Application assignments (SaaS via SAML)
```

---

## Exam Tips (IAM)

- **Explicit DENY always wins**, regardless of any Allow
- Permission Boundary ≠ SCP: boundary limits the *identity*, SCP limits the *account*
- Management Account is **never** affected by SCPs
- For cross-account S3/KMS without role assumption → resource-based policy with the destination account ID
- To require MFA: `Bool: aws:MultiFactorAuthPresent: true` (not `StringEquals`)
- CloudFront + ACM → certificate **must** be in `us-east-1`
- KMS Multi-Region Key: same material but different ARNs per region
- Secrets Manager charges per secret; Parameter Store Standard is free


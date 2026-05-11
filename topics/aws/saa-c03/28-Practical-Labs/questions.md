# Questions — Module 28: Practical Labs

> **SAA-C03 Domain**: Hands-on Verification  
> **Difficulty**: Practical

---

**1.** After creating a VPC with the command `aws ec2 create-vpc --cidr-block 10.0.0.0/16`, you try to launch an EC2 instance in the new VPC but cannot access the internet. Which step is most likely missing?

- A) Configure VPC DNS
- B) Create an Internet Gateway and attach it to the VPC, and add route 0.0.0.0/0 in the route table pointing to the IGW
- C) Enable IPv6 on the VPC
- D) Create a NAT Gateway before creating instances

<details><summary>Answer</summary>

**B** — A newly created VPC has no IGW. For internet access: (1) create IGW, (2) attach to VPC, (3) create or modify route table adding route 0.0.0.0/0 → IGW, (4) associate route table with public subnet, (5) instance needs public IP (auto-assign or EIP). All these steps are necessary.

</details>

---

**2.** You created a Lambda function that tries to connect to an RDS in a private subnet, but receives timeout. Lambda is in the same VPC. What is the first item to check?

- A) Lambda configured timeout (too low)
- B) Whether the RDS Security Group allows traffic on port 3306 from the Lambda Security Group
- C) Whether Lambda has enough memory
- D) Whether RDS is Multi-AZ

<details><summary>Answer</summary>

**B** — For Lambda in VPC to access RDS: RDS SG must have an inbound rule allowing the database port (MySQL: 3306, PostgreSQL: 5432) from the Lambda SG (referenced by Security Group ID, not by IP). Checking SGs is always the first step in connectivity problems.

</details>

---

**3.** You ran `terraform apply` and created AWS resources. When trying to destroy them with `terraform destroy`, you receive an error stating that the S3 bucket cannot be deleted because it is not empty. What is the correct solution in Terraform?

- A) Delete objects manually in the S3 console before running `terraform destroy`
- B) Add `force_destroy = true` in the `aws_s3_bucket` resource and re-apply before destroying
- C) Use `terraform state rm aws_s3_bucket.name` to remove from state
- D) Create a lifecycle rule on the bucket to expire objects

<details><summary>Answer</summary>

**B** — `force_destroy = true` in the `aws_s3_bucket` resource allows Terraform to delete the bucket even with objects. Run `terraform apply` to update the resource with this setting, then `terraform destroy`. Removing from state (C) leaves the resource orphaned in AWS (not deleted).

</details>

---

**4.** You want to test whether an IAM policy is working correctly before associating it with a user. Which AWS CLI tool should you use?

- A) `aws iam simulate-principal-policy`
- B) `aws iam get-policy`
- C) `aws iam list-attached-user-policies`
- D) `aws sts assume-role`

<details><summary>Answer</summary>

**A** — `aws iam simulate-principal-policy`: simulates the IAM authorization result for a specific principal performing specific actions on specific resources. Returns Allow or Deny without performing the action. Perfect for testing policies before applying. `simulate-custom-policy` tests a JSON policy without a specific user.

</details>

---

**5.** You are creating a Terraform module for an S3 bucket. The module should accept the bucket name as a required variable and create the bucket with versioning enabled. What is the correct syntax?

- A) 
```hcl
resource "aws_s3_bucket" "main" {
  bucket = var.bucket_name
}
resource "aws_s3_bucket_versioning" "main" {
  bucket = aws_s3_bucket.main.id
  versioning_configuration { status = "Enabled" }
}
```
- B) `aws s3api create-bucket --bucket ${var.bucket_name} --versioning Enabled`
- C) `resource "s3" "bucket" { name = var.bucket_name; versioning = true }`
- D) None of the above

<details><summary>Answer</summary>

**A** — In Terraform AWS Provider 4.x+ syntax, `aws_s3_bucket_versioning` is a separate resource (no longer a block inside `aws_s3_bucket`). The configuration in (A) is correct and modern. Option (C) has invalid syntax.

</details>

---

**6.** After deploying an ECS Fargate application, you notice that the containers keep restarting constantly. Where is the first place to investigate?

- A) VPC Flow Logs
- B) Container CloudWatch Logs (task definition should have logConfiguration with awslogs driver)
- C) AWS X-Ray traces
- D) CloudTrail for ECS service

<details><summary>Answer</summary>

**B** — Containers in restart loop generally indicate application error or misconfiguration. The container log (stdout/stderr) in CloudWatch Logs is the first place. The task definition must have `logConfiguration: awslogs` pointing to a Log Group. Without this, logs are lost and debugging is impossible.

</details>

---

**7.** You are using AWS CLI and receive the error `An error occurred (AccessDenied) when calling the DescribeInstances operation`. How do you diagnose which permission is missing?

- A) Check `aws iam list-attached-user-policies` to see user policies
- B) Use `aws iam simulate-principal-policy --action-names ec2:DescribeInstances` to simulate authorization
- C) Check `aws sts get-caller-identity` to confirm which identity is being used, then check that identity's policies
- D) C is the first step; then B to confirm the exact policy that is denying

<details><summary>Answer</summary>

**D** — Correct flow: first `aws sts get-caller-identity` to confirm you're authenticated as the correct identity (not as another role). Then `simulate-principal-policy` to understand which statement is denying the action. `list-attached-user-policies` does not show group policies or inline policies.

</details>

---

**8.** You created a MySQL RDS with `--no-publicly-accessible` in a private subnet. The application on EC2 in the same VPC cannot connect. What should you check? (Select 2)

- A) The RDS Security Group allows inbound on port 3306 from the EC2 Security Group
- B) The EC2 is in the same VPC as RDS (or VPCs connected by peering/TGW)
- C) The RDS has an Elastic IP associated
- D) The RDS subnet has a route to the Internet Gateway

<details><summary>Answer</summary>

**A and B** — For EC2 → RDS connectivity in the same VPC: (1) both in the same VPC; (2) RDS SG allows port 3306 from EC2 SG. Private RDS does not need EIP (C) or IGW route (D) — those are for public access.

</details>

---

**9.** You want to query DynamoDB returning only items where `status = "active"` and `age > 25`. The table has `userId` as partition key and `createdAt` as sort key. Which DynamoDB operation should you use?

- A) GetItem with FilterExpression
- B) Query with FilterExpression
- C) Scan with FilterExpression (reads entire table and filters)
- D) Batch GetItem

<details><summary>Answer</summary>

**C** — `status` and `age` are not table keys nor any described GSI/LSI. Query requires specifying the partition key. Scan reads the entire table and applies FilterExpression (works but expensive for large tables). The ideal solution would be to create a GSI with `status` as partition key and then do Query, but with the described indexes, Scan is the only option.

</details>

---

**10.** You created a Lambda function with code working locally, but when invoking on AWS you receive `Runtime.ImportModuleError: No module named 'boto3'`. What is the likely cause?

- A) Boto3 needs to be installed separately in Python Lambdas
- B) The deployment zip does not include dependencies correctly
- C) The selected Python runtime does not support boto3
- D) Boto3 is already included in Python Lambda runtime; the problem is another module being imported

<details><summary>Answer</summary>

**D** — Boto3 IS already included in the Python Lambda runtime (pre-installed by AWS). If the error says `No module named 'boto3'`, it is actually possible that the error is from another module listed earlier, or that the zip was incorrectly created, replacing the runtime boto3 with an incomplete local version. Check that the deployment package is correct.

</details>

---

**11.** After creating a CloudFront distribution with an S3 bucket as origin, you can still access S3 objects directly via the bucket URL, bypassing CloudFront. How to resolve this?

- A) Configure bucket policy to deny access from everyone except CloudFront OAC (Origin Access Control)
- B) Disable static website hosting on S3
- C) Configure CORS on the S3 bucket
- D) Use S3 pre-signed URLs instead of CloudFront

<details><summary>Answer</summary>

**A** — OAC (Origin Access Control): creates an identity in CloudFront. The bucket policy is updated to allow only GetObject from Principal `cloudfront.amazonaws.com` with condition `AWS:SourceArn` of the distribution. Any direct access to the S3 URL returns 403.

</details>

---

**12.** You want to monitor how many 5xx status requests your Lambda API is returning and create an alarm when it exceeds 10 in 5 minutes. Which CLI command sequence implements this?

- A) Create Metric Filter on Log Group + create Alarm on custom metric
- B) Use standard API Gateway metrics (`5XXError`) directly to create the Alarm
- C) Create CloudTrail Event Rule for status 500
- D) Use X-Ray with error threshold

<details><summary>Answer</summary>

**B** — API Gateway automatically publishes the `5XXError` metric in CloudWatch (namespace `AWS/ApiGateway`). Create the Alarm directly on this metric: `aws cloudwatch put-metric-alarm --alarm-name api-5xx --namespace AWS/ApiGateway --metric-name 5XXError --dimensions Name=ApiName,Value=my-api --period 300 --evaluation-periods 1 --threshold 10 --comparison-operator GreaterThanThreshold --statistic Sum`.

</details>

---

**13.** You ran `terraform apply` but the `aws_iam_role_policy_attachment` resource is not in your code. Terraform is showing this resource in state (`terraform state list`). What happens if you run `terraform apply` again?

- A) Terraform will delete the role policy attachment because it is not in the code
- B) Terraform does nothing with resources not in code (only manages what is in code)
- C) You would need `terraform state rm` to remove the resource from state
- D) Terraform will show an error about orphaned resource

<details><summary>Answer</summary>

**A** — Terraform manages resources declaratively: the desired state = what is in the code. If a resource is in state but not in code, the next `terraform apply` will delete that resource to align state with code. To remove from state without deleting the real resource: `terraform state rm resource.name`.

</details>

---

**14.** An S3 bucket event notification is configured to invoke a Lambda when objects are created. But when testing, the Lambda is not invoked. Which two items should you check?

- A) Lambda Resource Policy allowing S3 to invoke (Principal: s3.amazonaws.com) + Notification configured on the correct bucket
- B) Lambda IAM Role with s3:GetObject + Lambda SG
- C) Bucket versioning enabled + Lambda in same region as bucket
- D) CloudWatch Logs enabled on Lambda + S3 Access Logging

<details><summary>Answer</summary>

**A** — For S3 to invoke Lambda: (1) Resource-based policy on Lambda (`aws lambda add-permission`) allowing `lambda:InvokeFunction` with Principal `s3.amazonaws.com` and condition `ArnEquals` on the bucket ARN; (2) Notification configuration on the bucket pointing to the correct Lambda ARN. Without the resource policy, S3 receives access denied when trying to invoke.

</details>

---

**15.** You are using `aws s3 sync` to backup files from a server to S3. The command includes unnecessary files (node_modules, .git). How to exclude these directories?

- A) `aws s3 sync . s3://my-bucket --exclude "node_modules/*" --exclude ".git/*"`
- B) `aws s3 sync . s3://my-bucket --ignore node_modules .git`
- C) Create a .s3ignore file
- D) `aws s3 sync . s3://my-bucket --filter "node_modules"`

<details><summary>Answer</summary>

**A** — `--exclude` with glob pattern: `aws s3 sync . s3://my-bucket --exclude "node_modules/*" --exclude ".git/*"`. Each exclusion is a separate `--exclude`. The pattern uses glob (* and **). Note: if you want to include only certain types, use `--exclude "*" --include "*.js"`. S3 does not have a .s3ignore file.

</details>

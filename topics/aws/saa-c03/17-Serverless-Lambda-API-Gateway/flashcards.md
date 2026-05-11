# Flashcards — Module 11: Serverless, Lambda and API Gateway

> **Format:** Q = Question | A = Answer  
> **Total:** 25 flashcards

---

**Q:** What are the 3 Lambda invocation types?  
**A:** **Synchronous** (waits for response — API GW, ALB, SDK); **Asynchronous** (does not wait — S3 Events, SNS, EventBridge); **Event Source Mapping** (Lambda polls — SQS, Kinesis, DynamoDB Streams)

---

**Q:** What is Lambda concurrency and what is the default limit per region?  
**A:** Number of Lambda instances executing simultaneously. Default: **1,000 concurrent executions per region** (can be increased via support). Each synchronous invocation consumes 1 concurrency unit while executing.

---

**Q:** What is Provisioned Concurrency in Lambda?  
**A:** Pre-warms Lambda instances, eliminating cold starts. Instances remain "warm" and ready to respond immediately. Has additional cost (paid per hour of provisioned concurrency). Useful for latency-sensitive applications.

---

**Q:** What happens to SQS messages when Lambda returns an error in Event Source Mapping?  
**A:** Lambda automatically retries. After exhausting attempts (configurable maxReceiveCount on the SQS DLQ), the message goes to the **Dead Letter Queue (DLQ)**. Lambda does not directly handle the SQS DLQ — the DLQ is configured on SQS itself.

---

**Q:** What is a Lambda Layer?  
**A:** ZIP file containing dependencies (libraries, custom runtime) shared across multiple functions. Up to 5 layers per function. Maximum total size (code + layers): 250 MB uncompressed. Avoids repeating dependencies in each deployment package.

---

**Q:** What is the difference between Lambda Proxy Integration and Custom Integration in API Gateway?  
**A:** **Proxy Integration:** API GW passes the full HTTP request to Lambda (headers, body, query params) as an `event` object. Lambda returns the complete response (statusCode, headers, body). **Custom Integration:** API GW transforms the request/response via mapping templates (VTL). Proxy is simpler; custom offers more control.

---

**Q:** What is Lambda SnapStart and which runtime is it applicable to?  
**A:** Feature to reduce cold start in Java 11+. When publishing a new version, AWS initializes the function and takes a snapshot of the state. New invocations restore the snapshot instead of initializing from scratch — reduces cold start from seconds to milliseconds.

---

**Q:** How does Lambda access resources in a private VPC?  
**A:** By configuring Lambda with **VPC Configuration** (VPC ID, subnets, security group). AWS creates an ENI (Elastic Network Interface) in the specified subnet. Lambda gets a private VPC IP and can access RDS, ElastiCache, etc. Requires: NAT Gateway for Lambda to have internet access.

---

**Q:** What are the 3 API types in API Gateway?  
**A:** **REST API** (full functionality, staging, caching, throttling per stage); **HTTP API** (simpler, cheaper, lower latency, supports native JWT/OAuth); **WebSocket API** (persistent bidirectional connections, for chat, real-time notifications).

---

**Q:** What is throttling in API Gateway and how does it work?  
**A:** Limiting requests to protect the backend. Limits: **10,000 requests/second** per account (default) + **5,000 burst** concurrent. Per stage/method can be configured separately. When exceeded: HTTP 429 (Too Many Requests). Account limit can be increased via support.

---

**Q:** What type of Lambda authorizer does API Gateway verify?  
**A:** **Token-based:** receives token (JWT, OAuth) in the Authorization header and returns IAM policy (Allow/Deny). **Request-based:** receives headers, query params and can use any authentication logic. Result is cached by TTL (up to 3600s) for performance.

---

**Q:** What is a Lambda Alias and how does it differ from a Version?  
**A:** **Version:** immutable snapshot of code + configuration with unique ARN (e.g., `function:1`). **Alias:** named pointer (e.g., `PROD`) that points to one or two versions. Aliases support **canary deployment** (aliasName:weight to split traffic — e.g., 90% v1, 10% v2).

---

**Q:** What is the maximum Lambda execution time?  
**A:** **15 minutes** (900 seconds). For longer processes: use Step Functions (workflow orchestration), ECS/Fargate, or EC2.

---

**Q:** How does API Gateway support CORS?  
**A:** By configuring CORS in API Gateway to respond to pre-flight OPTIONS requests with headers `Access-Control-Allow-Origin`, `Access-Control-Allow-Headers`, `Access-Control-Allow-Methods`. For Proxy Integration, Lambda must also return CORS headers in responses.

---

**Q:** What is AWS SAM (Serverless Application Model)?  
**A:** Framework that simplifies deployment of serverless applications. Simplified CloudFormation syntax: `AWS::Serverless::Function`, `AWS::Serverless::Api`. Commands: `sam build`, `sam deploy`, `sam local invoke` (local testing with Docker). Generates a CloudFormation stack underneath.

---

**Q:** What is the Lambda Execution Role?  
**A:** IAM Role assumed by the Lambda function during execution. Defines which AWS APIs the function can call (e.g., `dynamodb:PutItem`, `s3:GetObject`). The function assumes the Role automatically — no explicit credentials needed in the code.

---

**Q:** What happens during a Lambda cold start?  
**A:** First invocation (or after period without use): AWS needs to allocate infrastructure, download code, initialize runtime, run code outside the handler. Adds latency (milliseconds to seconds, higher for Java). Solutions: Provisioned Concurrency, SnapStart (Java), keep initialization code outside the handler.

---

**Q:** What are the native API Gateway integrators besides Lambda?  
**A:** HTTP Integration (forwards to external HTTP endpoint), AWS Service Integration (directly calls AWS services — e.g., SQS, DynamoDB without intermediate Lambda), Mock Integration (returns static response), VPC Link (integrates with resources in private VPC via NLB).

---

**Q:** What is the API Gateway Deployment Stage and what is it for?  
**A:** Deployed snapshot of the API with a unique URL (e.g., `https://api-id.execute-api.us-east-1.amazonaws.com/prod`). Allows multiple environments: dev, staging, prod. Each stage has independent configurations: throttling, caching, stage variables (passed to Lambda/integration), logging.

---

**Q:** How does Lambda process multiple SQS messages simultaneously?  
**A:** Event Source Mapping processes messages in **batches** (up to 10,000). Lambda receives a batch of messages (configurable batch size). An error in any message in the batch may cause all to be returned to the queue. Solution: **Partial Batch Response** (individually report which messages failed).

---

**Q:** What is Lambda Destinations and when to use it instead of DLQ?  
**A:** For **asynchronous** invocations: configures success and failure destinations (SQS, SNS, EventBridge, another Lambda). More expressive than DLQ (includes invocation context + original input + output/error). DLQ only captures failed messages without result. Lambda Destinations is the modern standard.

---

**Q:** What is the Lambda invocation payload size limit?  
**A:** **Synchronous:** 6 MB (request payload) + 6 MB (response payload). **Asynchronous:** 256 KB (event payload). For larger payloads: save data in S3 and pass the S3 key as the event.

---

**Q:** What is the API Gateway Usage Plan?  
**A:** Defines usage limits per API key: throttling (requests/second, burst) and quota (requests/day or week or month). Allows monetizing APIs (different plans for different client tiers), controlling usage per client, and preventing abuse.

---

**Q:** What is Lambda@Edge?  
**A:** Runs Lambda code at CloudFront Points of Presence (edge locations) — close to the user. Use cases: URL rewrite, A/B testing, edge authentication, customizing headers. Limitations vs regular Lambda: shorter timeout (5s viewer, 30s origin), lower max memory, no VPC access, limited regions.

---

**Q:** How does Lambda Function URL differ from API Gateway?  
**A:** Function URL: dedicated HTTPS endpoint directly to the function (no API Gateway). Simpler, lower latency, no API Gateway cost. Limitations: no advanced throttling, no caching, no multi-stage usage, no native WAF integration (except via CloudFront). Use for simple webhooks or functions with occasional traffic.

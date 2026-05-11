# Flashcards — Module 10: Containers (ECS, EKS, Fargate)

---

**Q:** What is the object hierarchy in ECS?
**A:** Cluster → Service → Task → Container. Task Definition defines the blueprint (image, CPU, RAM, vars, volumes, IAM). Service maintains N tasks running. Cluster is the logical grouping of resources

---

**Q:** What is Task Role vs Task Execution Role in ECS?
**A:** Task Role: IAM role for the **application** inside the container (permission to access S3, DynamoDB, etc.). Task Execution Role: IAM role for the **ECS Agent** (pull image from ECR, push logs to CloudWatch, read Secrets Manager/SSM)

---

**Q:** What is the only network mode supported by Fargate?
**A:** **awsvpc mode**. Each Fargate task receives a dedicated ENI with a private VPC IP. Allows individual Security Groups per task. Bridge and host modes only work with EC2 Launch Type

---

**Q:** What is the advantage of awsvpc mode in ECS EC2?
**A:** Each task receives its own ENI with a VPC IP → can have individual SG per task (not per instance). Facilitates granular access control and compatibility with ALB target type "ip". Disadvantage: limit of ENIs per EC2 instance

---

**Q:** What is the CPU and RAM limit that can be configured in a Fargate task?
**A:** CPU: 0.25 vCPU to 16 vCPU. RAM: proportional to CPU (e.g., 0.25 vCPU → 0.5-2 GB; 16 vCPU → 32-120 GB). Charged per vCPU-second and GB-second while the task is active

---

**Q:** What are the 3 Launch Types available in ECS?
**A:** EC2 (you manage the cluster's EC2 instances), Fargate (serverless, AWS manages the host), External/ECS Anywhere (on-premises or edge servers registered as an ECS cluster)

---

**Q:** What is ECS Capacity Provider?
**A:** Automatically manages the Auto Scaling Group of the cluster's EC2 instances based on pending tasks, optimizing bin packing. With "Managed Scaling" enabled, ECS scales instances up/down automatically before tasks become queued

---

**Q:** What is the cost of the control plane for an EKS cluster?
**A:** $0.10/hour per EKS cluster (~$72/month). ECS does not charge for the cluster (only for compute: EC2 or Fargate). Consider this fixed cost for small workloads on EKS

---

**Q:** What are EKS Managed Node Groups?
**A:** AWS manages the lifecycle of EC2 worker nodes (provisioning, patching, updates with zero downtime, draining). You choose the instance type and AMI. Different from Fargate (no nodes) and Self-managed nodes (you manage everything manually)

---

**Q:** What is IRSA (IAM Roles for Service Accounts) in EKS?
**A:** Allows associating IAM Roles with Kubernetes Service Accounts. Pods using the Service Account receive temporary AWS credentials via OIDC (no hardcoding). Equivalent to ECS Task Role but for Kubernetes pods — per-pod/deployment granularity

---

**Q:** What is Amazon VPC CNI in EKS?
**A:** Default EKS network plugin. Allocates IPs directly from the VPC for each pod (does not use overlay network). Result: pods have native VPC IPs, communicate directly with other AWS resources, can have SGs applied directly (EKS Security Groups for Pods)

---

**Q:** What is the ECR Lifecycle Policy and how does it work?
**A:** Rules that automatically delete images based on criteria: age (days), count (keep N most recent), tag status (tagged/untagged). Examples: "delete untagged images older than 7 days" or "keep only the 5 most recent images per tag prefix"

---

**Q:** What is the difference between ECR Image Scanning Basic and Enhanced?
**A:** Basic (Clair): checks OS CVEs (OS packages). Enhanced (Amazon Inspector): checks CVEs in the OS AND in programming languages (Python, Node.js, Java packages). Enhanced = more detailed. Results available in Inspector Console + EventBridge events

---

**Q:** How do ECS containers securely access secrets (DB credentials)?
**A:** In Task Definition, `secrets` field: reference the Secrets Manager ARN or SSM Parameter Store. The ECS Agent (via Task Execution Role) fetches the secret at launch time and injects it as an environment variable or file. No hardcoded credentials

---

**Q:** What is AWS App Runner?
**A:** Serverless PaaS for web containers. You provide an ECR image or source code → App Runner automatically creates load balancer, HTTPS, auto-scaling, custom domain. Zero ECS/Fargate/ALB configuration. Simpler than ECS, less control

---

**Q:** What is ECS Service Connect?
**A:** AWS-managed Service Mesh for service-to-service communication within an ECS cluster. Offers service discovery, routing, retries, timeouts, and observability (metrics, tracing) without manually configuring App Mesh or Envoy

---

**Q:** What is the scaling mode in EKS for pods and for nodes?
**A:** Pods: **HPA** (Horizontal Pod Autoscaler) — scales number of pods based on CPU/RAM/custom metrics. Nodes: **Cluster Autoscaler** (scales node groups) or **Karpenter** (faster and more efficient node provisioning, AWS-native). Fargate nodes: scale automatically per pod

---

**Q:** What is EKS Fargate Profile?
**A:** Selector that defines which pods run on Fargate (by namespace and labels). A pod matching the profile is automatically scheduled on Fargate (no EC2 instances). Pods that do not match go to node groups. Each Fargate pod = isolated micro-VM

---

**Q:** How does authentication work on Amazon ECR for Docker pull?
**A:** Uses the AWS CLI: `aws ecr get-login-password --region ... | docker login --username AWS --password-stdin <account>.dkr.ecr.<region>.amazonaws.com`. Token valid for 12 hours. Kubernetes/EKS: uses ECR credential helper or IRSA for automatic renewal

---

**Q:** What is AWS Copilot CLI?
**A:** CLI that automates deployment of containerized applications on ECS/Fargate following best practices. Automatically creates: ECR, Task Definition, ECS Service, ALB, VPC, CodePipeline, SSM/Secrets. Abstracts complexity without removing control like App Runner does

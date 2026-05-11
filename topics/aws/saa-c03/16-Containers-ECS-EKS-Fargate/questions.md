# Exam Questions — Module 10: Containers (ECS, EKS, Fargate)

<!-- SAA-C03 Domain: Design High-Performing Architectures / Design Resilient Architectures -->

---

**1.** A team wants to run containers on AWS without managing EC2 servers. Which combination enables this with ECS?

- A) ECS with EC2 Launch Type
- B) ECS with Fargate Launch Type
- C) ECS with External Launch Type
- D) ECS with manually configured Auto Scaling Groups

<details>
<summary>Answer</summary>
**B — ECS with Fargate**
Fargate is serverless: you define the task (CPU, RAM, image), and AWS manages all underlying hosts. No EC2 to provision, patch, or scale. EC2 Launch Type requires you to register EC2 instances in the cluster (you manage the fleet). External is for on-premises servers (ECS Anywhere).
</details>

---

**2.** What is the difference between Task Role and Task Execution Role in ECS?

- A) Task Role is for the ECS agent; Execution Role is for the container
- B) Task Role is for the application inside the container; Execution Role is for ECS to manage the task (pull ECR image, push logs)
- C) Both are equivalent — distinction is only nomenclature
- D) Task Role applies to EC2 Launch Type; Execution Role to Fargate

<details>
<summary>Answer</summary>
**B — Correct**
**Task Role**: IAM policies for what the **application** can do (e.g., read S3, write DynamoDB). Obtained via Task Metadata Endpoint (task IMDS). **Task Execution Role**: for the ECS and Fargate agent: pull image from ECR, send logs to CloudWatch, read Secrets Manager/SSM Parameter Store. Both are needed when the application accesses AWS and uses ECR.
</details>

---

**3.** A container in ECS with Fargate launch type needs each task to have its own Security Group for granular network control. Which network mode should be enabled?

- A) bridge mode
- B) host mode
- C) awsvpc mode
- D) none mode

<details>
<summary>Answer</summary>
**C — awsvpc mode**
With `awsvpc`, each task receives **a dedicated ENI (Elastic Network Interface)** with a private VPC IP. This allows associating individual Security Groups per task. It is the **only mode supported by Fargate**. `bridge` uses dynamic ports of the EC2 host. `host` uses the host network directly.
</details>

---

**4.** A company uses ECS EC2 launch type and wants to distribute traffic across multiple containers on the same EC2 instance, with different dynamically assigned ports. Which ALB configuration?

- A) Application Load Balancer with target type "instance" and dynamic port mapping
- B) Network Load Balancer with fixed IP targets
- C) Application Load Balancer with target type "ip" in awsvpc mode
- D) Classic Load Balancer with sticky sessions

<details>
<summary>Answer</summary>
**A — ALB with dynamic port mapping (bridge mode)**
In ECS EC2 with bridge mode, no fixed port is defined (or uses hostPort=0) — ECS assigns dynamic ports on the host. The ALB with target type "instance" uses the ECS service to automatically register the (instance, dynamic port) pairs. With awsvpc, target type "ip" is used (each task has its own unique IP).
</details>

---

**5.** Which ECS component defines the containers (Docker image, CPU, RAM, environment variables, volumes, IAM) of a task?

- A) ECS Service
- B) ECS Cluster
- C) Task Definition
- D) Capacity Provider

<details>
<summary>Answer</summary>
**C — Task Definition**
Task Definition is the JSON blueprint that defines: Docker image(s), allocated CPU/RAM, port mappings, mounted volumes, environment variables, Task Role, Task Execution Role, log driver, etc. It is versioned. ECS Service uses the Task Definition to launch and maintain N running tasks.
</details>

---

**6.** A company uses Amazon EKS and wants to run pods without managing worker nodes (serverless). Which configuration should be used?

- A) EKS Managed Node Groups with Auto Scaling
- B) EKS Self-managed Nodes with Spot instances
- C) EKS with Fargate Profiles
- D) EKS with AWS Batch integration

<details>
<summary>Answer</summary>
**C — EKS Fargate Profiles**
Fargate Profiles in EKS define which pods (by namespace/labels) should run on Fargate. AWS provisions and manages the compute; you do not see or manage EC2 nodes. Managed Node Groups manage EC2 nodes automatically but you still choose types, AMIs, etc. Fargate = zero node management.
</details>

---

**7.** What is the approximate cost of the control plane for an EKS cluster per hour?

- A) Free — only worker nodes are charged
- B) $0.10/hour per EKS cluster (~$72/month)
- C) $0.50/hour per cluster
- D) Charged per number of running pods

<details>
<summary>Answer</summary>
**B — $0.10/hour per cluster (~$72/month)**
EKS charges $0.10 per hour for the managed control plane (API server, etcd, etc.) — this is fixed regardless of the number of nodes/pods. ECS has no cluster cost; only compute (EC2 or Fargate). This is an important differentiator when choosing ECS vs EKS for small workloads.
</details>

---

**8.** A Docker image was pushed to ECR. How to ensure only the 10 most recent images per repository are retained (automatically delete old images)?

- A) S3 Lifecycle Policy integrated with ECR
- B) ECR Lifecycle Policy with image count rule
- C) Lambda with CloudWatch Events cleaning images weekly
- D) ECR Image Scanning with auto-delete of old images

<details>
<summary>Answer</summary>
**B — ECR Lifecycle Policy**
ECR Lifecycle Policies allow creating rules such as: keep only the N most recent images per tag prefix, delete untagged images after X days, etc. Applied automatically by ECR without additional computation. Image Scanning detects vulnerabilities (CVEs) — does not manage retention.
</details>

---

**9.** What is IRSA (IAM Roles for Service Accounts) in EKS?

- A) Allows EKS pods to use IAM roles without needing hardcoded credentials
- B) Service to federate IAM identities across multiple EKS clusters
- C) Authentication mechanism for EKS nodes with the control plane
- D) Allows cross-account access between EKS clusters

<details>
<summary>Answer</summary>
**A — IAM Roles for individual pods**
IRSA allows associating an IAM Role with a Kubernetes Service Account. Pods using that Service Account receive temporary AWS credentials automatically (via OIDC). This is equivalent to the Task Role in ECS — without putting credentials in environment variables or using the entire node's role for the pod.
</details>

---

**10.** A company wants to use ECS or EKS. The team has little experience but needs to integrate with third-party Kubernetes Helm Charts. Which to choose?

- A) ECS — simpler and no cluster cost
- B) EKS — native Kubernetes support and ecosystem (Helm, Operators, etc.)
- C) App Runner — eliminates orchestration needs
- D) EC2 with Docker Compose

<details>
<summary>Answer</summary>
**B — EKS**
If the explicit requirement is Kubernetes compatibility (Helm Charts, Operators, kubectl, native RBAC), EKS is the choice. ECS is not Kubernetes and does not support Helm. If the priority were simplicity without Kubernetes, ECS (especially + Fargate) would be better. The presence of Helm Charts as a requirement determines EKS.
</details>

---

**11.** How does automatic scaling of tasks in ECS work based on SQS queue metrics?

- A) ECS Service Auto Scaling with Target Tracking Policy based on ApproximateNumberOfMessagesVisible
- B) Lambda function that invokes ECS RunTask as the queue grows
- C) SQS Auto Scaling Group trigger for ECS Cluster
- D) CloudWatch Alarm → SNS → ECS TaskSet update

<details>
<summary>Answer</summary>
**A — ECS Service Auto Scaling with Target Tracking**
ECS Service Auto Scaling supports Target Tracking, Step Scaling, and Scheduled Scaling. For SQS: create a CloudWatch Custom Metric with `ApproximateNumberOfMessagesVisible / number_of_tasks`, configure Target Tracking to keep this ratio at a target (e.g., 10 messages per task). ECS scales tasks automatically based on queue load.
</details>

---

**12.** Which AWS service is most suitable for quickly deploying a containerized web application with zero infrastructure configuration (no ECS, ALB, etc.)?

- A) ECS + Fargate + ALB (manual)
- B) AWS Copilot CLI
- C) AWS App Runner
- D) Elastic Beanstalk with Docker

<details>
<summary>Answer</summary>
**C — AWS App Runner**
App Runner is PaaS for web containers: you provide the ECR image (or source code) and App Runner creates and manages all infrastructure (load balancer, auto-scaling, HTTPS, custom domain). Zero ECS/ALB configuration. Elastic Beanstalk with Docker is more flexible but more complex. Copilot automates ECS/Fargate but still exposes the components.
</details>

---

**13.** What is the recommended secure mechanism for an ECS container to access database credentials stored in Secrets Manager?

- A) Inject the credential as a hardcoded environment variable in the Task Definition
- B) Mount an EFS volume with the credential file
- C) Reference the Secrets Manager ARN in the Task Definition — ECS automatically injects as env var or file
- D) Lambda sidecar container that fetches the credential and passes via shared volume

<details>
<summary>Answer</summary>
**C — Secrets Manager reference in Task Definition**
ECS supports secret injection directly from the Task Definition: in the `secrets` field, reference the Secrets Manager ARN (or SSM Parameter Store). The ECS Execution Role pulls the value at task launch time and injects it as an environment variable. No hardcoded credentials. C is the recommended AWS standard.
</details>

---

**14.** What differentiates ECS Capacity Provider from simply using Auto Scaling Groups manually in ECS EC2 Launch Type?

- A) Capacity Provider automatically manages EC2 instance scaling based on pending tasks, without manual intervention
- B) Capacity Provider is exclusive to Fargate, does not work with EC2
- C) There is no difference — Capacity Provider is just an alias for ASG
- D) Capacity Provider eliminates the need for Task Definitions

<details>
<summary>Answer</summary>
**A — Automatic cluster scaling management**
Capacity Provider with Managed Scaling: automatically scales the cluster's EC2 Auto Scaling Group based on pending tasks (optimized bin packing). Without CP, you manage manually or configure simple scaling policies. With CP, ECS "knows" how many instances are needed to accommodate all tasks and scales proactively before tasks become pending.
</details>

---

**15.** A company wants to check for CVE vulnerabilities in Docker images in ECR before they are deployed. Which configuration?

- A) SonarQube integrated with ECR
- B) ECR Image Scanning (Basic via Clair or Enhanced via Amazon Inspector)
- C) GuardDuty with ECR integration
- D) CodeBuild step that manually runs Trivy

<details>
<summary>Answer</summary>
**B — ECR Image Scanning**
ECR offers two types of scanning: **Basic** (uses open-source Clair, checks OS CVEs) enabled on-push or manual. **Enhanced Scanning** (via Amazon Inspector) checks CVEs in the OS and in programming languages (Python packages, Node.js modules, etc.) with results in the Inspector Console and EventBridge events for automation. Amazon Inspector → ECR = continuous image scanning.
</details>

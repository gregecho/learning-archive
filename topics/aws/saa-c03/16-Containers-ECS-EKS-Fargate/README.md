# Module 10 — Containers: ECS, EKS, Fargate

## Why Containers on AWS?

Containers offer consistency between environments (dev/staging/prod), dependency isolation, and workload density. AWS offers two main orchestrators: **ECS** (proprietary, simplicity) and **EKS** (Kubernetes, portability).

---

## Amazon ECS (Elastic Container Service)

### Core Concepts
```
ECS Cluster
  └── Service (defines how many Tasks to run + where)
        └── Task (1-N containers running together)
              └── Task Definition (blueprint: image, CPU, RAM, ports, volumes, IAM role)
```

- **Task Definition**: versioned JSON file that defines containers (like a Dockerfile but for ECS)
- **Task**: running instance of a Task Definition (1 task = 1 or more co-located containers)
- **Service**: ensures N tasks are always running; integrates with ALB/NLB; rolling updates
- **Cluster**: logical grouping of resources (can be EC2 instances or Fargate)

### Launch Types

| Launch Type | Infrastructure | Management | Control |
|---|---|---|---|
| **EC2** | EC2 instances you register in the cluster | You manage the instances (AMI, patches, scaling) | Full over host |
| **Fargate** | Serverless — AWS manages the host | No instances to manage | Task-level only |
| **External (ECS Anywhere)** | Your on-premises servers | You manage | Hybrid |

### ECS Network Modes

| Mode | Description | When to use |
|---|---|---|
| **bridge** | Container ports mapped to dynamic host IPs | EC2, multiple containers on same host |
| **host** | Container uses host network directly | EC2, high performance, no NAT |
| **awsvpc** | Each task gets its own ENI with a private VPC IP | **Recommended** — Fargate mandatory; SG isolation per task |
| **none** | No network | Offline tasks |

With `awsvpc`, each task has its own Security Group — maximum granularity of network isolation.

### IAM in ECS
| IAM Role | For | Who uses it |
|---|---|---|
| **Task Role** | What the container can do (S3, DynamoDB, etc.) | The application inside the container |
| **Task Execution Role** | What ECS can do to launch the task (pull ECR, push CloudWatch Logs, Secrets Manager) | The ECS agent |

> **Never embed credentials in the container** — use Task Role with `awsvpc` mode. Credentials are obtained via IMDS from the task metadata endpoint.

### ECS + ALB: Service Discovery and Load Balancing
- **ALB with dynamic port mapping** (EC2 launch type): containers register dynamic ports on the TG
- **NLB** for high throughput or non-HTTP traffic
- **Service Connect**: managed Service Mesh for service-to-service communication within ECS (mTLS, observability)
- **Cloud Map**: DNS-based service discovery for inter-container communication

### ECS Auto Scaling
- Scales the number of **tasks** (not instances — for EC2 Launch Type, scaling instances is separate)
- Policies: Target Tracking, Step Scaling, Scheduled
- **ECS Capacity Provider**: automatically manages the underlying EC2 cluster scaling based on pending tasks

---

## AWS Fargate

Serverless compute engine for ECS and EKS. You do not manage servers:

- Define: CPU (0.25 vCPU to 16 vCPU) + RAM (proportional to CPU)
- Charged per vCPU-hour and GB-hour while the task is running
- Each task on Fargate mandatorily uses `awsvpc` (own ENI)
- **Spot Fargate**: up to 70% discount for interruptible tasks
- **Fargate Savings Plans**: usage commitment for discount

---

## Amazon EKS (Elastic Kubernetes Service)

Managed Kubernetes on AWS. AWS manages the control plane (API server, etcd); you manage the worker nodes.

### Worker Node Modes

| Mode | Description | Flexibility |
|---|---|---|
| **Managed Node Groups** | AWS manages the lifecycle of EC2 nodes (launch, update, terminate) | High — can customize AMI, type, etc. |
| **Self-managed Nodes** | You manage completely (launch template, userdata) | Total |
| **Fargate Profiles** | Pods run on Fargate (serverless) | No node management |

### EKS Components
- **Control Plane**: managed by AWS (multi-AZ by default, highly available)
- **Worker Nodes**: EC2 or Fargate where Pods run
- **Add-ons**: AWS manages components like CoreDNS, kube-proxy, Amazon VPC CNI, AWS Load Balancer Controller
- **Amazon VPC CNI**: pods receive IPs directly from the VPC (same as ECS awsvpc — each pod = VPC IP)

### EKS Storage
- **EBS**: persistent volumes for pods (node-specific, no multi-attach)
- **EFS**: shared volumes across multiple pods/nodes
- **Amazon FSx for Lustre**: high-performance for ML/HPC workloads

### EKS vs ECS

| Aspect | ECS | EKS |
|---|---|---|
| Orchestrator | AWS Proprietary | Kubernetes (open source) |
| Learning curve | Lower | Higher |
| Portability | AWS only | Any Kubernetes (on-prem, GKE, AKS) |
| Ecosystem | AWS natively integrated | Helm charts, Kubernetes operators |
| Multi-cloud/on-prem | ECS Anywhere (limited) | EKS Anywhere, Kubernetes anywhere |
| Control plane cost | No cluster cost | $0.10/hour per EKS cluster |

---

## Amazon ECR (Elastic Container Registry)

Private (and public) Docker/OCI image registry:

- **Private repositories**: images accessible only within the account (or cross-account via resource policy)
- **Public repositories** (ECR Public): public images (similar to Docker Hub)
- **Image Scanning**: enhanced scanning via Amazon Inspector (CVEs, malware) or basic
- **Lifecycle Policies**: automatically discards old images (e.g., keep only the 10 most recent)
- **Replication**: cross-region or cross-account for DR and global distribution

---

## Other Container Services

### AWS App Runner
- PaaS for web containers: you provide the code or image, App Runner manages everything
- Auto-scaling, HTTPS, load balancing — no ECS/Fargate/ALB configuration
- Simpler, less control

### AWS Copilot
- CLI to deploy containerized applications on ECS/Fargate with built-in best practices
- Automatically creates: ECR, ECS Service, ALB, SSM Parameters, etc.

### AWS App Mesh
- Service Mesh based on **Envoy proxy** for ECS and EKS
- Observability (tracing, metrics) and mTLS for service-to-service communication
- AWS-native alternative to Istio

---

## Reference Architecture: Microservices with ECS Fargate

```
Route 53 → ALB (public)
              ├── /api/users/* → ECS Service: UserService (Fargate)
              │                       └── Task Role → DynamoDB (Users table)
              ├── /api/orders/* → ECS Service: OrderService (Fargate)
              │                       └── Task Role → RDS Aurora (Orders DB)
              └── /api/notify/* → ECS Service: NotifyService (Fargate)
                                      └── Task Role → SNS/SES

Internal communication:
  OrderService → SNS "order-placed" → SQS → NotifyService
  (fan-out via EventBridge for auditing to S3)

ECR → Task Definition (versioned image)
CloudWatch Logs → Container logs (awslogs driver)
AWS X-Ray → Distributed tracing
```

---

## When to Use What

| Need | Service |
|---|---|
| Maximum simplicity, containerized web app | App Runner |
| AWS-native containers without managing infra | ECS + Fargate |
| AWS-native containers with host control | ECS + EC2 |
| Kubernetes for portability | EKS |
| Kubernetes serverless | EKS + Fargate |
| Kubernetes on-premises | EKS Anywhere |

---

## Exam Tips

- **Task Role** = application permissions; **Task Execution Role** = ECS permissions to manage the task
- **awsvpc mode** = each task has its own ENI and SG — network isolation per task (mandatory for Fargate)
- **ECS EC2** still needs EC2 instances in the cluster; **Fargate** = zero infra to manage
- **Managed Node Groups** on EKS != Fargate — they are still EC2 nodes but managed by AWS
- **ECR Lifecycle Policy** prevents accumulation of old images; use for cost control
- EKS has a fixed cluster cost ($0.10/hour ≈ $72/month); ECS does not charge for the cluster
- For multi-cloud portability: EKS (Kubernetes) is more suitable than ECS
- **VPC CNI on EKS** = pods with VPC IPs (like awsvpc on ECS) — important for security and routing
- ECS Auto Scaling scales **tasks**; Capacity Provider automatically scales the underlying **EC2 cluster**
- **Service Connect** = new alternative to App Mesh for service-to-service communication on ECS

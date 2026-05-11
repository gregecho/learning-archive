# Cheatsheet — Module 10: Containers (ECS, EKS, Fargate)

## ECS Launch Types

| | EC2 Launch Type | Fargate Launch Type | External (ECS Anywhere) |
|---|---|---|---|
| Manage instances? | YES (you) | NO (AWS) | YES (on-prem/edge) |
| Cost | EC2 + ECS (free cluster) | vCPU/hour + GB/hour | EC2-like per node |
| Control | Full over host | Task level only | Full over hardware |
| Available network | bridge, host, awsvpc | Only **awsvpc** | bridge, host, awsvpc |

## ECS Task Definition — Critical Parameters

```json
{
  "family": "my-app",
  "taskRoleArn": "arn:aws:iam::...:role/TaskRole",
  "executionRoleArn": "arn:aws:iam::...:role/TaskExecutionRole",
  "networkMode": "awsvpc",
  "requiresCompatibilities": ["FARGATE"],
  "cpu": "512",
  "memory": "1024",
  "containerDefinitions": [{
    "name": "app",
    "image": "account.dkr.ecr.region.amazonaws.com/app:v1.0",
    "portMappings": [{"containerPort": 8080}],
    "secrets": [{"name": "DB_PASSWORD", "valueFrom": "arn:aws:secretsmanager:..."}],
    "logConfiguration": {"logDriver": "awslogs", "options": {"awslogs-group": "/ecs/app"}}
  }]
}
```

## ECS IAM Roles

| Role | Who uses it | What for |
|---|---|---|
| Task Role | Application in the container | Access AWS services (S3, DynamoDB, SQS) |
| Task Execution Role | ECS Agent / Fargate | Pull ECR image, push CloudWatch Logs, read Secrets Manager |
| Instance Profile | EC2 node (EC2 Launch Type) | ECS Agent registers with the cluster |

## ECS Network Modes

| Mode | Works with | Task IP | SG per Task | Notes |
|---|---|---|---|---|
| bridge | EC2 | Host IP + dynamic port | No (host SG) | Dynamic port mapping with ALB |
| host | EC2 | Host IP | No | No NAT, high performance |
| **awsvpc** | EC2 and **Fargate** | **Own VPC IP** | **YES** | Recommended; ENI per task |
| none | EC2 | None | No | Offline tasks |

## ECS vs EKS — When to Use

| Criterion | ECS | EKS |
|---|---|---|
| Simple + AWS-native | ✅ Best | Can use |
| Kubernetes compatible | ❌ | ✅ Required |
| Helm Charts / Operators | ❌ | ✅ |
| Multi-cloud / portability | ❌ | ✅ |
| Control plane cost | Free | $0.10/hour ≈ $72/month |
| Learning curve | Low | High |

## EKS — Worker Node Types

| Type | Management | Flexibility |
|---|---|---|
| Managed Node Groups | AWS (managed EC2 lifecycle) | AMI, types, size chosen by you |
| Self-managed Nodes | You (launch template, userdata) | Total |
| Fargate Profiles | AWS (serverless) | Zero node management (per pod) |

## ECR — Important Configurations

| Feature | Description |
|---|---|
| Lifecycle Policy | Automates image deletion by count or age |
| Image Scanning | Basic (Clair, OS CVEs) or Enhanced (Inspector, OS + languages) |
| Replication | Cross-region and/or cross-account (for DR, global distribution) |
| Immutable Tags | Prevents overwriting existing tags (e.g., `latest` immutable) |
| Pull Through Cache | Proxy cache from public registries (DockerHub, ECR Public) |

## Fargate CPU/RAM Combinations

| vCPU | RAM (GB) |
|---|---|
| 0.25 | 0.5, 1, 2 |
| 0.5 | 1 to 4 |
| 1 | 2 to 8 |
| 2 | 4 to 16 |
| 4 | 8 to 30 |
| 8 | 16 to 60 |
| 16 | 32 to 120 |

## Container Services Comparison

| Service | Management | Kubernetes? | Best for |
|---|---|---|---|
| ECS + EC2 | Medium (EC2 nodes) | No | Control + AWS native |
| ECS + Fargate | Low (serverless) | No | Simplicity without infra |
| EKS + Node Groups | Medium | **Yes** | Managed K8s |
| EKS + Fargate | Low | **Yes** | K8s + serverless |
| App Runner | Zero | No | Ultra-fast deploy |
| Elastic Beanstalk | Low-medium | No | Traditional web apps |

## Quick Exam Tips
- **Task Role** = what the app does; **Execution Role** = what ECS does to launch the task
- **awsvpc** = only option on Fargate; gives dedicated ENI + IP + SG per task
- **ECS costs**: EC2 cluster is free, Fargate charges per vCPU-hour and GB-hour
- **EKS costs**: $0.10/hour for the control plane (regardless of nodes/pods)
- **IRSA (IAM Roles for Service Accounts)**: EKS equivalent of ECS Task Role — role per pod via OIDC
- **Managed Node Groups**: AWS manages EC2 (rolling update, drain) but you choose type/AMI
- **Fargate Profile on EKS**: defines which pods (namespace/label) go to Fargate
- Dynamic port mapping (ECS EC2 bridge mode): ALB target type = "instance"; with awsvpc = target type "ip"
- For secrets in tasks: reference Secrets Manager/SSM in Task Definition (Execution Role with permission)
- **ECR + VPC Endpoint**: instances in private subnet pull ECR images without NAT/internet

# Hands-on Lab — VPC: Private Networks, NAT Gateway and Security (Module 05)

> **Region:** us-east-1 | **Estimated cost:** ~$0.05 (NAT Gateway $0.045/h — destroy in < 1h)  
> **Prerequisites:** AWS CLI configured, Terraform >= 1.5

---

## Objective

Create a complete VPC with public and private subnets, NAT Gateway, bastion host, Security Groups, and NACLs — replicating a typical production architecture.

---

## Part 1 — Terraform: Complete VPC

```hcl
# main.tf
terraform {
  required_version = ">= 1.5"
  required_providers {
    aws = {
      source  = "hashicorp/aws"
      version = "~> 5.0"
    }
  }
}

provider "aws" { region = "us-east-1" }

locals {
  prefix = "lab-vpc"
}

# Main VPC
resource "aws_vpc" "lab" {
  cidr_block           = "10.0.0.0/16"
  enable_dns_support   = true
  enable_dns_hostnames = true
  tags = { Name = "${local.prefix}" }
}

# Public subnets (2 AZs for HA)
resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.lab.id
  cidr_block              = "10.0.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  tags = { Name = "${local.prefix}-public-a", Tier = "public" }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.lab.id
  cidr_block              = "10.0.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
  tags = { Name = "${local.prefix}-public-b", Tier = "public" }
}

# Private subnets (2 AZs)
resource "aws_subnet" "private_a" {
  vpc_id            = aws_vpc.lab.id
  cidr_block        = "10.0.10.0/24"
  availability_zone = "us-east-1a"
  tags = { Name = "${local.prefix}-private-a", Tier = "private" }
}

resource "aws_subnet" "private_b" {
  vpc_id            = aws_vpc.lab.id
  cidr_block        = "10.0.11.0/24"
  availability_zone = "us-east-1b"
  tags = { Name = "${local.prefix}-private-b", Tier = "private" }
}

# Internet Gateway
resource "aws_internet_gateway" "lab" {
  vpc_id = aws_vpc.lab.id
  tags   = { Name = "${local.prefix}-igw" }
}

# Elastic IP for NAT Gateway
resource "aws_eip" "nat" {
  domain = "vpc"
  tags   = { Name = "${local.prefix}-nat-eip" }
}

# NAT Gateway in public subnet a
resource "aws_nat_gateway" "lab" {
  allocation_id = aws_eip.nat.id
  subnet_id     = aws_subnet.public_a.id
  tags          = { Name = "${local.prefix}-natgw" }
  depends_on    = [aws_internet_gateway.lab]
}

# Public route table
resource "aws_route_table" "public" {
  vpc_id = aws_vpc.lab.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.lab.id
  }
  tags = { Name = "${local.prefix}-rt-public" }
}

resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

# Private route table → NAT
resource "aws_route_table" "private" {
  vpc_id = aws_vpc.lab.id
  route {
    cidr_block     = "0.0.0.0/0"
    nat_gateway_id = aws_nat_gateway.lab.id
  }
  tags = { Name = "${local.prefix}-rt-private" }
}

resource "aws_route_table_association" "private_a" {
  subnet_id      = aws_subnet.private_a.id
  route_table_id = aws_route_table.private.id
}

resource "aws_route_table_association" "private_b" {
  subnet_id      = aws_subnet.private_b.id
  route_table_id = aws_route_table.private.id
}

# Security Group: Bastion Host
resource "aws_security_group" "bastion" {
  name   = "${local.prefix}-bastion-sg"
  vpc_id = aws_vpc.lab.id

  ingress {
    from_port   = 22
    to_port     = 22
    protocol    = "tcp"
    cidr_blocks = ["0.0.0.0/0"]  # In production: specific IP
    description = "SSH access"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# Security Group: Private instances — only accept SSH from Bastion
resource "aws_security_group" "private_app" {
  name   = "${local.prefix}-app-sg"
  vpc_id = aws_vpc.lab.id

  ingress {
    from_port       = 22
    to_port         = 22
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
    description     = "SSH only via bastion"
  }

  ingress {
    from_port       = 8080
    to_port         = 8080
    protocol        = "tcp"
    security_groups = [aws_security_group.bastion.id]
    description     = "App port"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# NACL for private subnet
resource "aws_network_acl" "private" {
  vpc_id     = aws_vpc.lab.id
  subnet_ids = [aws_subnet.private_a.id, aws_subnet.private_b.id]

  # Allow SSH from VPC (10.0.0.0/16)
  ingress {
    rule_no    = 100
    action     = "allow"
    protocol   = "tcp"
    cidr_block = "10.0.0.0/16"
    from_port  = 22
    to_port    = 22
  }

  # Allow ephemeral ports (HTTP/HTTPS responses)
  ingress {
    rule_no    = 200
    action     = "allow"
    protocol   = "tcp"
    cidr_block = "0.0.0.0/0"
    from_port  = 1024
    to_port    = 65535
  }

  # Block direct HTTP access from outside the VPC
  ingress {
    rule_no    = 300
    action     = "deny"
    protocol   = "tcp"
    cidr_block = "0.0.0.0/0"
    from_port  = 80
    to_port    = 80
  }

  egress {
    rule_no    = 100
    action     = "allow"
    protocol   = "-1"
    cidr_block = "0.0.0.0/0"
    from_port  = 0
    to_port    = 0
  }

  tags = { Name = "${local.prefix}-private-nacl" }
}

output "vpc_id"         { value = aws_vpc.lab.id }
output "public_a_id"    { value = aws_subnet.public_a.id }
output "private_a_id"   { value = aws_subnet.private_a.id }
output "nat_eip"        { value = aws_eip.nat.public_ip }
```

---

## Part 2 — Verify and Test the Network

```bash
terraform init && terraform apply -auto-approve

VPC_ID=$(terraform output -raw vpc_id)
PUB_SUBNET=$(terraform output -raw public_a_id)
PRIV_SUBNET=$(terraform output -raw private_a_id)
NAT_IP=$(terraform output -raw nat_eip)

echo "VPC: $VPC_ID"
echo "NAT EIP: $NAT_IP"

# Check route tables
aws ec2 describe-route-tables \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'RouteTables[*].[RouteTableId, Routes[*].[DestinationCidrBlock, GatewayId, NatGatewayId]]' \
  --output json | python3 -m json.tool | head -60

# Check NACLs
aws ec2 describe-network-acls \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'NetworkAcls[*].[NetworkAclId, Entries[*].[RuleNumber, RuleAction, CidrBlock]]' \
  --output table

# Check Security Groups
aws ec2 describe-security-groups \
  --filters "Name=vpc-id,Values=$VPC_ID" \
  --query 'SecurityGroups[*].[GroupName, IpPermissions[*].[IpProtocol, FromPort, IpRanges[0].CidrIp]]' \
  --output json | python3 -m json.tool

# VPC Flow Logs (recommended in prod)
FLOW_LOG_BUCKET="lab-vpc-logs-$(aws sts get-caller-identity --query Account --output text)"
aws s3api create-bucket --bucket "$FLOW_LOG_BUCKET"

aws ec2 create-flow-logs \
  --resource-type VPC \
  --resource-ids "$VPC_ID" \
  --traffic-type ALL \
  --log-destination-type s3 \
  --log-destination "arn:aws:s3:::${FLOW_LOG_BUCKET}"

echo "Flow Logs enabled for VPC $VPC_ID"
```

---

## Cleanup

```bash
# Disable and delete Flow Logs
FLOW_LOG_ID=$(aws ec2 describe-flow-logs \
  --filter "Name=resource-id,Values=$VPC_ID" \
  --query 'FlowLogs[0].FlowLogId' --output text)
aws ec2 delete-flow-logs --flow-log-ids "$FLOW_LOG_ID"
aws s3 rm "s3://${FLOW_LOG_BUCKET}" --recursive
aws s3api delete-bucket --bucket "$FLOW_LOG_BUCKET"

# Destroy Terraform infrastructure
terraform destroy -auto-approve
```

---

## What You Learned

- Default VPC: `10.0.0.0/16` → `/24` subnets = 251 usable hosts per subnet
- NAT Gateway: PAID per hour and per GB. Cheap alternative: NAT Instance (EC2 t3.micro)
- Security Group vs NACL: SG stateful (ALLOW only); NACL stateless (ALLOW and DENY, requires return rule)
- Bastion Host: single SSH entry point in the public subnet; Session Manager is an alternative without bastion
- VPC Flow Logs: network traffic auditing; essential for troubleshooting and compliance

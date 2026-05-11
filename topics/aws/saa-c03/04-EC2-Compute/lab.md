# Lab — EC2 Compute

> **Region:** us-east-1  
> **Estimated cost:** ~$0.05–$0.20/hour during the lab (EC2 t3.micro + EBS)  
> **Prerequisite:** AWS CLI configured, Terraform >= 1.5, VPC and default subnet available

## Lab Objectives
1. Create a Launch Template with mandatory IMDSv2 and User Data
2. Create a Spot Fleet with type diversification
3. Compare gp2 vs gp3 in practice with IOPS benchmarking
4. Create and use a Partition Placement Group

---

## Part 1: Launch Template with IMDSv2 via AWS CLI

```bash
# Variables
REGION="us-east-1"
VPC_ID=$(aws ec2 describe-vpcs --filters "Name=isDefault,Values=true" \
  --query "Vpcs[0].VpcId" --output text --region $REGION)
SUBNET_ID=$(aws ec2 describe-subnets --filters "Name=vpc-id,Values=$VPC_ID" \
  --query "Subnets[0].SubnetId" --output text --region $REGION)
AMI_ID=$(aws ssm get-parameters --names /aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64 \
  --region $REGION --query "Parameters[0].Value" --output text)

echo "VPC: $VPC_ID | Subnet: $SUBNET_ID | AMI: $AMI_ID"

# Create Security Group
SG_ID=$(aws ec2 create-security-group \
  --group-name "lab-ec2-sg" \
  --description "Lab EC2 SAA-C03" \
  --vpc-id $VPC_ID \
  --region $REGION \
  --query GroupId --output text)

# Allow SSH (for testing only — restrict to your IP in production)
MY_IP=$(curl -s https://checkip.amazonaws.com)
aws ec2 authorize-security-group-ingress \
  --group-id $SG_ID \
  --protocol tcp --port 22 \
  --cidr "${MY_IP}/32" \
  --region $REGION

# Key pair (if you don't have one)
aws ec2 create-key-pair \
  --key-name lab-ec2-keypair \
  --query KeyMaterial --output text \
  --region $REGION > ~/.ssh/lab-ec2-keypair.pem
chmod 400 ~/.ssh/lab-ec2-keypair.pem

# USER DATA script base64 encoded
USER_DATA=$(cat <<'EOF' | base64
#!/bin/bash
yum update -y
# Install SSM Agent (already included in AL2023 but ensure)
yum install -y amazon-ssm-agent
systemctl enable --now amazon-ssm-agent

# Simple disk benchmark
yum install -y fio
echo "Lab EC2 ready" > /var/www/html/index.html
yum install -y httpd
systemctl enable --now httpd
EOF
)

# Create Launch Template with mandatory IMDSv2
LT_ID=$(aws ec2 create-launch-template \
  --launch-template-name "lab-saa-c03-lt" \
  --version-description "v1 - IMDSv2 required" \
  --launch-template-data "{
    \"ImageId\": \"$AMI_ID\",
    \"InstanceType\": \"t3.micro\",
    \"KeyName\": \"lab-ec2-keypair\",
    \"SecurityGroupIds\": [\"$SG_ID\"],
    \"MetadataOptions\": {
      \"HttpTokens\": \"required\",
      \"HttpEndpoint\": \"enabled\",
      \"HttpPutResponseHopLimit\": 1
    },
    \"UserData\": \"$USER_DATA\",
    \"TagSpecifications\": [{
      \"ResourceType\": \"instance\",
      \"Tags\": [{\"Key\": \"Name\", \"Value\": \"lab-ec2-imdsv2\"}]
    }]
  }" \
  --region $REGION \
  --query LaunchTemplate.LaunchTemplateId --output text)

echo "Launch Template created: $LT_ID"
```

---

## Part 2: Test IMDSv2

```bash
# Launch instance from Launch Template
INSTANCE_ID=$(aws ec2 run-instances \
  --launch-template LaunchTemplateId=$LT_ID,Version='$Latest' \
  --subnet-id $SUBNET_ID \
  --associate-public-ip-address \
  --region $REGION \
  --query "Instances[0].InstanceId" --output text)

echo "Instance: $INSTANCE_ID"
aws ec2 wait instance-running --instance-ids $INSTANCE_ID --region $REGION

PUBLIC_IP=$(aws ec2 describe-instances --instance-ids $INSTANCE_ID \
  --query "Reservations[0].Instances[0].PublicIpAddress" --output text --region $REGION)

# SSH into the instance and test IMDSv2
ssh -i ~/.ssh/lab-ec2-keypair.pem ec2-user@$PUBLIC_IP

# Inside the instance:
# Try IMDSv1 (should fail with 401)
curl -s http://169.254.169.254/latest/meta-data/instance-id
# Expected: 401 Unauthorized

# IMDSv2 (correct)
TOKEN=$(curl -s -X PUT "http://169.254.169.254/latest/api/token" \
  -H "X-aws-ec2-metadata-token-ttl-seconds: 300")
curl -s -H "X-aws-ec2-metadata-token: $TOKEN" \
  http://169.254.169.254/latest/meta-data/instance-id
# Expected: i-0xxxxxxxxxxxx
```

---

## Part 3: Terraform — Placement Group + gp3 EBS

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

provider "aws" {
  region = "us-east-1"
}

data "aws_vpc" "default" {
  default = true
}

data "aws_subnets" "available" {
  filter {
    name   = "vpc-id"
    values = [data.aws_vpc.default.id]
  }
}

data "aws_ssm_parameter" "al2023" {
  name = "/aws/service/ami-amazon-linux-latest/al2023-ami-kernel-6.1-x86_64"
}

# ──────────────────────────────────────────────────────
# 1. Partition Placement Group (for Kafka/Cassandra)
# ──────────────────────────────────────────────────────

resource "aws_placement_group" "partition_pg" {
  name            = "lab-partition-pg"
  strategy        = "partition"
  partition_count = 3 # 3 partitions = 3 separate racks
}

# ──────────────────────────────────────────────────────
# 2. Security Group
# ──────────────────────────────────────────────────────

resource "aws_security_group" "lab_sg" {
  name        = "lab-ec2-terraform-sg"
  description = "Lab EC2 Terraform"
  vpc_id      = data.aws_vpc.default.id

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# ──────────────────────────────────────────────────────
# 3. Launch Template with gp3 and IMDSv2
# ──────────────────────────────────────────────────────

resource "aws_launch_template" "lab_lt" {
  name_prefix            = "lab-ec2-"
  image_id               = data.aws_ssm_parameter.al2023.value
  instance_type          = "t3.micro"
  vpc_security_group_ids = [aws_security_group.lab_sg.id]

  # Mandatory IMDSv2
  metadata_options {
    http_endpoint               = "enabled"
    http_tokens                 = "required"
    http_put_response_hop_limit = 1
  }

  # EBS gp3 as root volume
  block_device_mappings {
    device_name = "/dev/xvda"
    ebs {
      volume_size           = 20
      volume_type           = "gp3"
      iops                  = 3000 # baseline gp3
      throughput            = 125  # MB/s baseline gp3
      delete_on_termination = true
      encrypted             = true
    }
  }

  # Additional EBS gp3 for data (custom IOPS)
  block_device_mappings {
    device_name = "/dev/xvdb"
    ebs {
      volume_size           = 50
      volume_type           = "gp3"
      iops                  = 6000  # above baseline, no extra cost per volume
      throughput            = 250   # MB/s
      delete_on_termination = true
      encrypted             = true
    }
  }

  user_data = base64encode(<<-EOF
    #!/bin/bash
    yum update -y
    yum install -y fio lsblk

    # Format and mount /dev/nvme1n1 (second EBS volume)
    mkfs.xfs /dev/nvme1n1
    mkdir -p /data
    mount /dev/nvme1n1 /data
    echo "/dev/nvme1n1 /data xfs defaults 0 2" >> /etc/fstab

    # IOPS benchmark on gp3 (report to CloudWatch Logs)
    fio --name=iops_test --ioengine=libaio --rw=randread \
      --bs=4k --numjobs=4 --size=1G --runtime=30 \
      --directory=/data --output=/tmp/fio_results.txt
    cat /tmp/fio_results.txt
  EOF
  )

  tag_specifications {
    resource_type = "instance"
    tags = {
      Name   = "lab-ec2-gp3-pg"
      Module = "03-EC2-Compute"
    }
  }

  lifecycle {
    create_before_destroy = true
  }
}

# ──────────────────────────────────────────────────────
# 4. Instances in Placement Group (simulating Kafka brokers)
# ──────────────────────────────────────────────────────

resource "aws_instance" "kafka_broker" {
  count = 3

  launch_template {
    id      = aws_launch_template.lab_lt.id
    version = "$Latest"
  }

  placement_group         = aws_placement_group.partition_pg.id
  placement_partition_number = count.index + 1
  subnet_id               = data.aws_subnets.available.ids[0]

  tags = {
    Name      = "lab-kafka-broker-${count.index + 1}"
    Partition = count.index + 1
  }
}

# ──────────────────────────────────────────────────────
# Outputs
# ──────────────────────────────────────────────────────

output "placement_group_name" {
  value = aws_placement_group.partition_pg.name
}

output "broker_instance_ids" {
  value = aws_instance.kafka_broker[*].id
}

output "launch_template_id" {
  value = aws_launch_template.lab_lt.id
}
```

---

## Part 4: Compare gp2 vs gp3 via CLI

```bash
# Create gp2 volume (legacy)
VOL_GP2=$(aws ec2 create-volume \
  --size 100 \
  --volume-type gp2 \
  --availability-zone us-east-1a \
  --region us-east-1 \
  --query VolumeId --output text)

# Create gp3 volume with same IOPS as gp2 (3 IOPS/GB = 300 IOPS for 100GB)
# but with configurable throughput
VOL_GP3=$(aws ec2 create-volume \
  --size 100 \
  --volume-type gp3 \
  --iops 3000 \
  --throughput 125 \
  --availability-zone us-east-1a \
  --region us-east-1 \
  --query VolumeId --output text)

echo "gp2: $VOL_GP2 | gp3: $VOL_GP3"

# Verify prices via describe
aws ec2 describe-volumes \
  --volume-ids $VOL_GP2 $VOL_GP3 \
  --query "Volumes[*].{ID:VolumeId,Type:VolumeType,IOPS:Iops,Throughput:Throughput}" \
  --output table --region us-east-1
```

---

## Cleanup

```bash
# Terraform
terraform destroy -auto-approve

# CLI — terminate instances
aws ec2 terminate-instances --instance-ids $INSTANCE_ID --region us-east-1

# Delete volumes
aws ec2 delete-volume --volume-id $VOL_GP2 --region us-east-1
aws ec2 delete-volume --volume-id $VOL_GP3 --region us-east-1

# Delete launch template
aws ec2 delete-launch-template \
  --launch-template-id $LT_ID --region us-east-1

# Delete key pair
aws ec2 delete-key-pair \
  --key-name lab-ec2-keypair --region us-east-1
rm ~/.ssh/lab-ec2-keypair.pem

# Delete security group (after instances terminated)
aws ec2 delete-security-group --group-id $SG_ID --region us-east-1

echo "Cleanup completed!"
```

---

## Review Points

- [ ] What is the difference between `HttpPutResponseHopLimit: 1` vs `2` in IMDSv2?
- [ ] Why can the gp3 volume have more IOPS than gp2 for the same size?
- [ ] In a Partition Placement Group, do instances from different partitions share hardware?
- [ ] Why use `launch_template` instead of `launch_configuration` in Terraform?
- [ ] What happens to gp3 volume data when `delete_on_termination = true`?

---

# Hands-On Lab — Migration and Transfer: DMS + S3 Transfer (Module 15)

> **Region:** us-east-1 | **Estimated cost:** ~$0.50 (DMS replication instance t3.micro, < 1 hour of use)
> **Prerequisites:** AWS CLI configured, Terraform >= 1.5, MySQL client

---

## Objective

Simulate a MySQL database migration from on-premises to RDS using DMS, and practice data transfer between S3 buckets (simulating storage migration).

---

## Part 1 — Base Infrastructure with Terraform

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

data "aws_caller_identity" "current" {}

locals {
  prefix     = "lab-migration"
  account_id = data.aws_caller_identity.current.account_id
}

# VPC for the lab
resource "aws_vpc" "lab" {
  cidr_block           = "10.10.0.0/16"
  enable_dns_hostnames = true
  enable_dns_support   = true
  tags = { Name = "${local.prefix}-vpc" }
}

resource "aws_internet_gateway" "lab" {
  vpc_id = aws_vpc.lab.id
  tags   = { Name = "${local.prefix}-igw" }
}

# Public subnet (for access to source MySQL)
resource "aws_subnet" "public_a" {
  vpc_id                  = aws_vpc.lab.id
  cidr_block              = "10.10.1.0/24"
  availability_zone       = "us-east-1a"
  map_public_ip_on_launch = true
  tags = { Name = "${local.prefix}-public-a" }
}

resource "aws_subnet" "public_b" {
  vpc_id                  = aws_vpc.lab.id
  cidr_block              = "10.10.2.0/24"
  availability_zone       = "us-east-1b"
  map_public_ip_on_launch = true
  tags = { Name = "${local.prefix}-public-b" }
}

resource "aws_route_table" "public" {
  vpc_id = aws_vpc.lab.id
  route {
    cidr_block = "0.0.0.0/0"
    gateway_id = aws_internet_gateway.lab.id
  }
}

resource "aws_route_table_association" "public_a" {
  subnet_id      = aws_subnet.public_a.id
  route_table_id = aws_route_table.public.id
}

resource "aws_route_table_association" "public_b" {
  subnet_id      = aws_subnet.public_b.id
  route_table_id = aws_route_table.public.id
}

# Security Group for RDS
resource "aws_security_group" "rds" {
  name   = "${local.prefix}-rds-sg"
  vpc_id = aws_vpc.lab.id

  ingress {
    from_port   = 3306
    to_port     = 3306
    protocol    = "tcp"
    cidr_blocks = ["10.10.0.0/16"]
    description = "MySQL within VPC"
  }

  egress {
    from_port   = 0
    to_port     = 0
    protocol    = "-1"
    cidr_blocks = ["0.0.0.0/0"]
  }
}

# RDS MySQL — DESTINATION database
resource "aws_db_subnet_group" "lab" {
  name       = "${local.prefix}-subnet-group"
  subnet_ids = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

resource "aws_db_instance" "destination" {
  identifier        = "${local.prefix}-destination"
  engine            = "mysql"
  engine_version    = "8.0"
  instance_class    = "db.t3.micro"
  allocated_storage = 20
  storage_type      = "gp2"

  db_name  = "store_destination"
  username = "admin"
  password = "Lab@12345!"  # Use Secrets Manager in production

  db_subnet_group_name   = aws_db_subnet_group.lab.name
  vpc_security_group_ids = [aws_security_group.rds.id]

  skip_final_snapshot = true
  publicly_accessible = false

  tags = { Environment = "lab", Module = "15-migration" }
}

# IAM Role for DMS
resource "aws_iam_role" "dms" {
  name = "${local.prefix}-dms-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "dms.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "dms_vpc" {
  role       = aws_iam_role.dms.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AmazonDMSVPCManagementRole"
}

# DMS Subnet Group
resource "aws_dms_replication_subnet_group" "lab" {
  replication_subnet_group_description = "Lab DMS subnet group"
  replication_subnet_group_id          = "${local.prefix}-dms-subnet"
  subnet_ids                           = [aws_subnet.public_a.id, aws_subnet.public_b.id]
}

# DMS Replication Instance
resource "aws_dms_replication_instance" "lab" {
  replication_instance_class  = "dms.t3.micro"
  replication_instance_id     = "${local.prefix}-replication"
  replication_subnet_group_id = aws_dms_replication_subnet_group.lab.id
  vpc_security_group_ids      = [aws_security_group.rds.id]
  publicly_accessible         = false
  allocated_storage           = 20
}

output "rds_endpoint" {
  value = aws_db_instance.destination.endpoint
}

output "dms_instance_arn" {
  value = aws_dms_replication_instance.lab.replication_instance_arn
}
```

---

## Part 2 — Source MySQL Database (simulated locally)

```bash
# Option A: Use Docker to simulate on-premises database
docker run -d \
  --name mysql-source \
  -e MYSQL_ROOT_PASSWORD=Lab@12345! \
  -e MYSQL_DATABASE=store_source \
  -p 3306:3306 \
  mysql:8.0

sleep 20  # wait for MySQL to start

# Populate source database with test data
docker exec -i mysql-source mysql -uroot -pLab@12345! store_source << 'SQL'
CREATE TABLE customers (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  email VARCHAR(150) UNIQUE NOT NULL,
  ssn CHAR(14) NOT NULL,
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

CREATE TABLE products (
  id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(200) NOT NULL,
  price DECIMAL(10,2) NOT NULL,
  stock INT DEFAULT 0
);

CREATE TABLE orders (
  id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT REFERENCES customers(id),
  product_id INT REFERENCES products(id),
  quantity INT NOT NULL,
  total DECIMAL(10,2),
  status ENUM('pending','approved','shipped','delivered') DEFAULT 'pending',
  created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
);

-- Sample data
INSERT INTO customers (name, email, ssn) VALUES
  ('John Silva', 'john@example.com', '000.000.000-00'),
  ('Mary Santos', 'mary@example.com', '111.111.111-11'),
  ('Carlos Oliveira', 'carlos@example.com', '222.222.222-22');

INSERT INTO products (name, price, stock) VALUES
  ('Notebook Pro', 2500.00, 10),
  ('Wireless Mouse', 89.90, 50),
  ('27" Monitor', 1200.00, 5);

INSERT INTO orders (customer_id, product_id, quantity, total, status) VALUES
  (1, 1, 1, 2500.00, 'approved'),
  (2, 2, 3, 269.70, 'delivered'),
  (3, 3, 2, 2400.00, 'pending'),
  (1, 2, 1, 89.90, 'shipped');

SELECT 'Data inserted successfully' AS status;
SQL
```

---

## Part 3 — Configure DMS

```bash
# Deploy infrastructure
terraform init && terraform apply -auto-approve

RDS_ENDPOINT=$(terraform output -raw rds_endpoint)
DMS_ARN=$(terraform output -raw dms_instance_arn)

echo "RDS Destination: $RDS_ENDPOINT"
echo "DMS Instance: $DMS_ARN"

# Create SOURCE endpoint (local MySQL via machine's public IP)
MY_IP=$(curl -s ifconfig.me)

SOURCE_ARN=$(aws dms create-endpoint \
  --endpoint-identifier "lab-source-mysql" \
  --endpoint-type source \
  --engine-name mysql \
  --server-name "$MY_IP" \
  --port 3306 \
  --database-name store_source \
  --username root \
  --password "Lab@12345!" \
  --query 'Endpoint.EndpointArn' --output text)

# Create DESTINATION endpoint (RDS)
TARGET_ARN=$(aws dms create-endpoint \
  --endpoint-identifier "lab-target-rds" \
  --endpoint-type target \
  --engine-name mysql \
  --server-name "${RDS_ENDPOINT%:*}" \
  --port 3306 \
  --database-name store_destination \
  --username admin \
  --password "Lab@12345!" \
  --query 'Endpoint.EndpointArn' --output text)

# Test connection to endpoints
aws dms test-connection \
  --replication-instance-arn "$DMS_ARN" \
  --endpoint-arn "$SOURCE_ARN"

aws dms test-connection \
  --replication-instance-arn "$DMS_ARN" \
  --endpoint-arn "$TARGET_ARN"

# Create Full Load task
TASK_ARN=$(aws dms create-replication-task \
  --replication-task-identifier "lab-full-load" \
  --source-endpoint-arn "$SOURCE_ARN" \
  --target-endpoint-arn "$TARGET_ARN" \
  --replication-instance-arn "$DMS_ARN" \
  --migration-type full-load \
  --table-mappings '{
    "rules": [{
      "rule-type": "selection",
      "rule-id": "1",
      "rule-name": "1",
      "object-locator": {
        "schema-name": "store_source",
        "table-name": "%"
      },
      "rule-action": "include"
    }]
  }' \
  --query 'ReplicationTask.ReplicationTaskArn' --output text)

# Start task
aws dms start-replication-task \
  --replication-task-arn "$TASK_ARN" \
  --start-replication-task-type start-replication

# Monitor progress
watch -n 10 'aws dms describe-replication-tasks \
  --filters Name=replication-task-arn,Values='"$TASK_ARN"' \
  --query "ReplicationTasks[0].[Status, ReplicationTaskStats.TablesLoaded, ReplicationTaskStats.TablesLoading]" \
  --output table'
```

---

## Part 4 — Validate Migration and S3 Transfer

```bash
# Check data in destination RDS
mysql -h "${RDS_ENDPOINT%:*}" -u admin -p"Lab@12345!" store_destination << 'SQL'
SELECT 'Customers:' AS table_name, COUNT(*) AS records FROM customers
UNION ALL
SELECT 'Products:', COUNT(*) FROM products
UNION ALL
SELECT 'Orders:', COUNT(*) FROM orders;
SQL

# Simulate S3 data migration (Cross-Region or Cross-Account)
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
SOURCE_BUCKET="lab-migration-source-${ACCOUNT_ID}"
DEST_BUCKET="lab-migration-dest-${ACCOUNT_ID}"

# Create buckets
aws s3api create-bucket --bucket "$SOURCE_BUCKET"
aws s3api create-bucket --bucket "$DEST_BUCKET"

# Create test data
for i in $(seq 1 20); do
  echo "Data file ${i}: $(date) - migration data" > /tmp/file_${i}.txt
  aws s3 cp /tmp/file_${i}.txt "s3://${SOURCE_BUCKET}/data/file_${i}.txt"
done

echo "20 files created in source bucket."

# Migrate using S3 Sync
aws s3 sync "s3://${SOURCE_BUCKET}/" "s3://${DEST_BUCKET}/" \
  --metadata-directive COPY \
  --sse aws:kms

# Verify integrity
SOURCE_COUNT=$(aws s3 ls "s3://${SOURCE_BUCKET}/data/" --recursive | wc -l)
DEST_COUNT=$(aws s3 ls "s3://${DEST_BUCKET}/data/" --recursive | wc -l)
echo "Source files: $SOURCE_COUNT | Destination files: $DEST_COUNT"

# Enable S3 replication (CRR - Cross-Region Replication)
# Requires bucket in different region
echo "For CRR: create bucket in us-west-2 and configure replication rule"
```

---

## Cleanup

```bash
# Stop and delete DMS
aws dms stop-replication-task --replication-task-arn "$TASK_ARN"
sleep 30
aws dms delete-replication-task --replication-task-arn "$TASK_ARN"
aws dms delete-endpoint --endpoint-arn "$SOURCE_ARN"
aws dms delete-endpoint --endpoint-arn "$TARGET_ARN"

# Destroy Terraform (RDS, DMS instance, VPC)
terraform destroy -auto-approve

# Clean S3
aws s3 rm "s3://${SOURCE_BUCKET}" --recursive
aws s3 rm "s3://${DEST_BUCKET}" --recursive
aws s3api delete-bucket --bucket "$SOURCE_BUCKET"
aws s3api delete-bucket --bucket "$DEST_BUCKET"

# Stop Docker
docker stop mysql-source && docker rm mysql-source

# Clean temporary files
rm -f /tmp/file_*.txt
```

---

## What You Learned

- DMS requires: replication instance + source endpoint + target endpoint + task
- Full Load migration type: complete snapshot, no continuous replication
- Full Load + CDC type: initial Full Load + real-time change capture
- DMS supports homogeneous and heterogeneous migrations (SCT needed for heterogeneous)
- `aws s3 sync` is idempotent — only transfers new or modified files
- Replication instance is charged per hour even without running tasks — destroy after use

---

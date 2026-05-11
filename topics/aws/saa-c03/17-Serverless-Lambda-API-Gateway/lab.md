# Practical Lab — Serverless: Lambda + API Gateway + DynamoDB (Module 11)

> **Region:** us-east-1 | **Estimated cost:** < $0.10 (Free Tier covers all Lambda/DynamoDB portions)  
> **Prerequisites:** AWS CLI configured, SAM CLI installed, Python 3.12

---

## Objective

Create a complete serverless REST API with authentication, allowing **creation** and **querying** of orders using Lambda + API Gateway + DynamoDB + Cognito.

---

## Part 1 — Infrastructure with Terraform

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

# DynamoDB — orders table
resource "aws_dynamodb_table" "orders" {
  name         = "lab-orders"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "orderId"

  attribute {
    name = "orderId"
    type = "S"
  }

  ttl {
    attribute_name = "expiration"
    enabled        = true
  }

  tags = {
    Environment = "lab"
    Module      = "11-serverless"
  }
}

# IAM Role for Lambda
resource "aws_iam_role" "lambda_role" {
  name = "lab-lambda-orders-role"

  assume_role_policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Action    = "sts:AssumeRole"
      Effect    = "Allow"
      Principal = { Service = "lambda.amazonaws.com" }
    }]
  })
}

resource "aws_iam_role_policy_attachment" "lambda_basic" {
  role       = aws_iam_role.lambda_role.name
  policy_arn = "arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole"
}

resource "aws_iam_role_policy" "lambda_dynamo" {
  name = "lab-lambda-dynamo-policy"
  role = aws_iam_role.lambda_role.id

  policy = jsonencode({
    Version = "2012-10-17"
    Statement = [{
      Effect = "Allow"
      Action = [
        "dynamodb:PutItem",
        "dynamodb:GetItem",
        "dynamodb:Query",
        "dynamodb:Scan"
      ]
      Resource = aws_dynamodb_table.orders.arn
    }]
  })
}

# Lambda — create order
resource "aws_lambda_function" "create_order" {
  function_name = "lab-create-order"
  role          = aws_iam_role.lambda_role.arn
  handler       = "create_order.lambda_handler"
  runtime       = "python3.12"
  timeout       = 30
  memory_size   = 256
  filename      = "lambda_package.zip"

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.orders.name
    }
  }
}

# Lambda — query order
resource "aws_lambda_function" "query_order" {
  function_name = "lab-query-order"
  role          = aws_iam_role.lambda_role.arn
  handler       = "query_order.lambda_handler"
  runtime       = "python3.12"
  timeout       = 30
  memory_size   = 128
  filename      = "lambda_package.zip"

  environment {
    variables = {
      TABLE_NAME = aws_dynamodb_table.orders.name
    }
  }
}

# API Gateway
resource "aws_apigatewayv2_api" "orders_api" {
  name          = "lab-orders-api"
  protocol_type = "HTTP"

  cors_configuration {
    allow_origins = ["*"]
    allow_methods = ["GET", "POST"]
    allow_headers = ["Content-Type", "Authorization"]
  }
}

resource "aws_apigatewayv2_stage" "default" {
  api_id      = aws_apigatewayv2_api.orders_api.id
  name        = "$default"
  auto_deploy = true
}

# Lambda ↔ API GW Integrations
resource "aws_apigatewayv2_integration" "create" {
  api_id             = aws_apigatewayv2_api.orders_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.create_order.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_integration" "query" {
  api_id             = aws_apigatewayv2_api.orders_api.id
  integration_type   = "AWS_PROXY"
  integration_uri    = aws_lambda_function.query_order.invoke_arn
  integration_method = "POST"
}

resource "aws_apigatewayv2_route" "create_route" {
  api_id    = aws_apigatewayv2_api.orders_api.id
  route_key = "POST /orders"
  target    = "integrations/${aws_apigatewayv2_integration.create.id}"
}

resource "aws_apigatewayv2_route" "query_route" {
  api_id    = aws_apigatewayv2_api.orders_api.id
  route_key = "GET /orders/{orderId}"
  target    = "integrations/${aws_apigatewayv2_integration.query.id}"
}

# Lambda permission for API GW to invoke
resource "aws_lambda_permission" "create_apigw" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.create_order.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.orders_api.execution_arn}/*/*"
}

resource "aws_lambda_permission" "query_apigw" {
  action        = "lambda:InvokeFunction"
  function_name = aws_lambda_function.query_order.function_name
  principal     = "apigateway.amazonaws.com"
  source_arn    = "${aws_apigatewayv2_api.orders_api.execution_arn}/*/*"
}

output "api_url" {
  value = aws_apigatewayv2_api.orders_api.api_endpoint
}
```

---

## Part 2 — Lambda Code

```python
# create_order.py
import json
import boto3
import uuid
import os
from datetime import datetime, timezone, timedelta

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    body = json.loads(event.get('body', '{}'))
    
    if not body.get('product') or not body.get('quantity'):
        return {
            'statusCode': 400,
            'body': json.dumps({'error': 'product and quantity are required'})
        }
    
    order_id = str(uuid.uuid4())
    expiration = int((datetime.now(timezone.utc) + timedelta(days=30)).timestamp())
    
    item = {
        'orderId': order_id,
        'product': body['product'],
        'quantity': int(body['quantity']),
        'status': 'pending',
        'createdAt': datetime.now(timezone.utc).isoformat(),
        'expiration': expiration
    }
    
    table.put_item(Item=item)
    
    return {
        'statusCode': 201,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps({'orderId': order_id, 'status': 'pending'})
    }
```

```python
# query_order.py
import json
import boto3
import os

dynamodb = boto3.resource('dynamodb')
table = dynamodb.Table(os.environ['TABLE_NAME'])

def lambda_handler(event, context):
    order_id = event['pathParameters']['orderId']
    
    response = table.get_item(Key={'orderId': order_id})
    
    if 'Item' not in response:
        return {
            'statusCode': 404,
            'body': json.dumps({'error': 'order not found'})
        }
    
    return {
        'statusCode': 200,
        'headers': {'Content-Type': 'application/json'},
        'body': json.dumps(response['Item'], default=str)
    }
```

---

## Part 3 — Deploy and Test

```bash
# 1. Package Lambda
zip -j lambda_package.zip create_order.py query_order.py

# 2. Deploy infrastructure
terraform init
terraform plan
terraform apply -auto-approve

# 3. Capture API URL
API_URL=$(terraform output -raw api_url)

# 4. Create order
curl -X POST "${API_URL}/orders" \
  -H "Content-Type: application/json" \
  -d '{"product": "Notebook", "quantity": 2}'

# Expected: {"orderId": "uuid-xxx", "status": "pending"}

# 5. Query order
ORDER_ID="uuid-from-previous-step"
curl "${API_URL}/orders/${ORDER_ID}"

# 6. Check logs
aws logs tail /aws/lambda/lab-create-order --since 5m

# 7. Check DynamoDB
aws dynamodb scan --table-name lab-orders \
  --query 'Items[*].[orderId.S, product.S, status.S]' \
  --output table
```

---

## Part 4 — Concurrency and Scaling Test

```bash
# Send 100 simultaneous orders (requires 'ab' or wrk)
# Using curl in a loop:
for i in $(seq 1 20); do
  curl -s -X POST "${API_URL}/orders" \
    -H "Content-Type: application/json" \
    -d "{\"product\": \"Item-${i}\", \"quantity\": ${i}}" &
done
wait

# View Lambda concurrency metrics in CloudWatch
aws cloudwatch get-metric-statistics \
  --namespace AWS/Lambda \
  --metric-name ConcurrentExecutions \
  --dimensions Name=FunctionName,Value=lab-create-order \
  --start-time $(date -u -d '5 minutes ago' +%Y-%m-%dT%H:%M:%SZ) \
  --end-time $(date -u +%Y-%m-%dT%H:%M:%SZ) \
  --period 60 \
  --statistics Maximum
```

---

## Cleanup

```bash
# Destroy ALL resources (avoids costs)
terraform destroy -auto-approve

# Verify DynamoDB was removed
aws dynamodb list-tables --query 'TableNames[?contains(@, `lab`)]'

# Verify Lambdas were removed
aws lambda list-functions --query 'Functions[?contains(FunctionName, `lab`)].FunctionName'
```

---

## What You Learned

- Lambda runs code without servers, charging only per invocation
- API Gateway HTTP API is cheaper and simpler than REST API for Lambda
- DynamoDB PAY_PER_REQUEST: no provisioned capacity, pay per request
- Lambda IAM Role must be explicitly authorized (principle of least privilege)
- DynamoDB TTL expires items automatically (free, no extra charge)
- `terraform destroy` removes everything — always run at the end of the lab

# Hands-On Lab — Well-Architected Framework: WAT + Trusted Advisor + Cost Explorer (Module 26)

> **Region:** us-east-1 | **Estimated cost:** ~$0 (Well-Architected Tool, Trusted Advisor and Cost Explorer are free)  
> **Prerequisites:** AWS CLI configured, account with console access

---

## Objective

Use native AWS tools to evaluate the architecture according to the Well-Architected Framework, check Trusted Advisor recommendations, and analyze costs with Cost Explorer.

---

## Part 1 — AWS Well-Architected Tool

```bash
# List available lenses
aws wellarchitected list-lenses \
  --query 'LenseSummaries[*].[LensAlias, LensName]' \
  --output table

# Create a workload for evaluation
WORKLOAD_ID=$(aws wellarchitected create-workload \
  --workload-name "Lab-Ecommerce-Platform" \
  --description "Evaluation of the e-commerce platform for lab purposes" \
  --environment PRODUCTION \
  --aws-regions "us-east-1" \
  --lenses "wellarchitected" \
  --review-owner "devops-team@company.com" \
  --query 'WorkloadId' --output text)

echo "Workload created: $WORKLOAD_ID"

# View workload details
aws wellarchitected get-workload \
  --workload-id "$WORKLOAD_ID" \
  --query 'Workload.[WorkloadName, Environment, RiskCounts]' \
  --output table

# List milestone (initial state)
aws wellarchitected list-milestones \
  --workload-id "$WORKLOAD_ID"

# Explore questions by pillar
PILLARS=("operationalExcellence" "security" "reliability" "performance" "costOptimization" "sustainability")

for PILLAR in "${PILLARS[@]}"; do
  echo ""
  echo "=== Pillar: $PILLAR ==="
  aws wellarchitected list-answers \
    --workload-id "$WORKLOAD_ID" \
    --lens-alias "wellarchitected" \
    --pillar-id "$PILLAR" \
    --query 'AnswerSummaries[*].[QuestionId, QuestionTitle, Risk]' \
    --output table 2>/dev/null | head -30
done

# Answer a question (security pillar — SEC 1)
aws wellarchitected update-answer \
  --workload-id "$WORKLOAD_ID" \
  --lens-alias "wellarchitected" \
  --question-id "sec_securely_operate" \
  --selected-choices "sec_securely_operate_aws_account" "sec_securely_operate_multi_accounts" \
  --notes "We use AWS Organizations with SCPs for centralized governance"

# Generate milestone after answering questions
MILESTONE_NUMBER=$(aws wellarchitected create-milestone \
  --workload-id "$WORKLOAD_ID" \
  --milestone-name "Sprint-Review-2025-Q1" \
  --query 'MilestoneNumber' --output text)

echo "Milestone created: Sprint-Review-2025-Q1 (Number: $MILESTONE_NUMBER)"

# View lens review with risks
aws wellarchitected get-lens-review \
  --workload-id "$WORKLOAD_ID" \
  --lens-alias "wellarchitected" \
  --query 'LensReview.[LensName, RiskCounts]' \
  --output json
```

---

## Part 2 — Trusted Advisor

```bash
# List all available checks
aws trustedadvisor list-checks \
  --query 'checks[*].[id, name, category, status]' \
  --output table 2>/dev/null | head -50

# Checks by category
CATEGORIES=("cost_optimizing" "security" "fault_tolerance" "performance" "service_limits")

for CAT in "${CATEGORIES[@]}"; do
  echo ""
  echo "=== Category: $CAT ==="
  aws trustedadvisor list-checks \
    --query "checks[?category=='${CAT}'].[id, name]" \
    --output table 2>/dev/null | head -20
done

# Security check — Security Groups open ports
OPEN_PORTS_CHECK="HCP4007jHTy"  # SG check ID for open ports

aws trustedadvisor get-check-result \
  --check-id "$OPEN_PORTS_CHECK" \
  --query 'result.[status, timestamp, flaggedResources[*].[region, status]]' \
  --output json 2>/dev/null

# MFA check on root account
MFA_CHECK="7DAFEmoDos"

aws trustedadvisor get-check-result \
  --check-id "$MFA_CHECK" \
  --query 'result.[status, checkId]' \
  --output json 2>/dev/null

# Underutilized instances check (Cost)
UNDERUTIL_CHECK="Qch7DwouX1"

aws trustedadvisor get-check-result \
  --check-id "$UNDERUTIL_CHECK" \
  --query 'result.[status, flaggedResources]' \
  --output json 2>/dev/null

# Refresh checks (force update)
aws trustedadvisor refresh-check --check-id "$OPEN_PORTS_CHECK"
echo "Check refreshed. Wait ~2-3 min for results."

# Summary of all results
aws trustedadvisor describe-checks-result-summary \
  --query 'result.[status, categorySpecificSummary]' \
  --output json 2>/dev/null
```

---

## Part 3 — AWS Compute Optimizer

```bash
# Check if Compute Optimizer is enabled
aws compute-optimizer get-enrollment-status \
  --query 'status' --output text

# Enable if needed
aws compute-optimizer update-enrollment-status --status Active

# Wait 24h to generate recommendations — list what is available
aws compute-optimizer get-ec2-instance-recommendations \
  --query 'instanceRecommendations[*].[instanceArn, finding, findingReasonCodes]' \
  --output table 2>/dev/null

# Recommendations for Auto Scaling Groups
aws compute-optimizer get-auto-scaling-group-recommendations \
  --query 'autoScalingGroupRecommendations[*].[autoScalingGroupArn, finding]' \
  --output table 2>/dev/null

# Recommendations for EBS volumes
aws compute-optimizer get-ebs-volume-recommendations \
  --query 'volumeRecommendations[*].[volumeArn, finding]' \
  --output table 2>/dev/null

# Export recommendations to S3 (for mass analysis)
ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
REPORT_BUCKET="lab-compute-optimizer-${ACCOUNT_ID}"

aws s3api create-bucket --bucket "$REPORT_BUCKET"

aws compute-optimizer export-ec2-instance-recommendations \
  --s3-destination-config bucket="$REPORT_BUCKET",keyPrefix="recommendations/" \
  --query 'jobId' --output text
```

---

## Part 4 — Cost Explorer

```bash
# Total cost last 30 days by service
START=$(date -d "-30 days" +%Y-%m-%d 2>/dev/null || date -v-30d +%Y-%m-%d)
END=$(date +%Y-%m-%d)

aws ce get-cost-and-usage \
  --time-period "Start=${START},End=${END}" \
  --granularity MONTHLY \
  --metrics BlendedCost UnblendedCost UsageQuantity \
  --group-by "Type=DIMENSION,Key=SERVICE" \
  --query 'ResultsByTime[0].Groups[*].[Keys[0], Metrics.BlendedCost.Amount]' \
  --output table

# Top 5 most expensive services
aws ce get-cost-and-usage \
  --time-period "Start=${START},End=${END}" \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by "Type=DIMENSION,Key=SERVICE" \
  --query 'sort_by(ResultsByTime[0].Groups, &Metrics.BlendedCost.Amount)[-5:][*].[Keys[0], Metrics.BlendedCost.Amount]' \
  --output table

# Cost by tag (example: Environment)
aws ce get-cost-and-usage \
  --time-period "Start=${START},End=${END}" \
  --granularity MONTHLY \
  --metrics BlendedCost \
  --group-by "Type=TAG,Key=Environment" \
  --query 'ResultsByTime[0].Groups[*].[Keys[0], Metrics.BlendedCost.Amount]' \
  --output table

# Forecast for the next 30 days
FORECAST_START=$(date +%Y-%m-%d)
FORECAST_END=$(date -d "+30 days" +%Y-%m-%d 2>/dev/null || date -v+30d +%Y-%m-%d)

aws ce get-cost-forecast \
  --time-period "Start=${FORECAST_START},End=${FORECAST_END}" \
  --granularity MONTHLY \
  --metric BLENDED_COST \
  --query '[Total.Amount, Total.Unit]' \
  --output text

# Daily cost (useful for detecting anomalies)
aws ce get-cost-and-usage \
  --time-period "Start=${START},End=${END}" \
  --granularity DAILY \
  --metrics BlendedCost \
  --query 'ResultsByTime[*].[TimePeriod.Start, Total.BlendedCost.Amount]' \
  --output table | tail -10
```

---

## Part 5 — Savings Plans Analysis

```bash
# View already purchased Savings Plans
aws savingsplans describe-savings-plans \
  --query 'savingsPlans[*].[savingsPlanId, offeringId, state, commitment, end]' \
  --output table

# Savings Plans recommendations
aws ce get-savings-plans-purchase-recommendation \
  --savings-plans-type COMPUTE_SP \
  --term-in-years ONE_YEAR \
  --payment-option NO_UPFRONT \
  --lookback-period-in-days SIXTY_DAYS \
  --query 'SavingsPlansPurchaseRecommendation.[SavingsPlansType, LookbackPeriodInDays, SavingsPlansPurchaseRecommendationDetails[0].EstimatedSavingsSavingsPlansEligibleCosts]' \
  --output json

# Compare On-Demand vs Savings Plans vs Reserved Instances
echo ""
echo "=== Pricing Model Comparison ==="
echo "On-Demand: no commitment, full price"
echo "Compute Savings Plan 1yr No Upfront: ~17% discount"
echo "EC2 Savings Plan 1yr No Upfront: ~up to 40% discount"
echo "RI 1yr No Upfront: up to 40% for specific type"
echo "RI 1yr All Upfront: up to 56% for specific type"
echo "RI 3yr All Upfront: up to 72% for specific type"
echo "Spot Instances: up to 90% discount (interruptible)"

# Cost Anomaly Detection — create monitor
aws ce create-anomaly-monitor \
  --anomaly-monitor '{
    "MonitorName": "lab-monitor-service",
    "MonitorType": "DIMENSIONAL",
    "MonitorDimension": "SERVICE"
  }' \
  --query 'MonitorArn' --output text
```

---

## Part 6 — IAM Access Analyzer (Security Pillar)

```bash
# Create analyzer at account level
ANALYZER_ARN=$(aws accessanalyzer create-analyzer \
  --analyzer-name "lab-account-analyzer" \
  --type ACCOUNT \
  --query 'arn' --output text)

echo "Analyzer created: $ANALYZER_ARN"

# Wait for analysis (~1-2 min) and list findings
sleep 60

aws accessanalyzer list-findings \
  --analyzer-arn "$ANALYZER_ARN" \
  --query 'findings[*].[id, resourceType, resource, status]' \
  --output table

# View finding details (if any exist)
FIRST_FINDING=$(aws accessanalyzer list-findings \
  --analyzer-arn "$ANALYZER_ARN" \
  --query 'findings[0].id' --output text 2>/dev/null)

if [ "$FIRST_FINDING" != "None" ] && [ -n "$FIRST_FINDING" ]; then
  aws accessanalyzer get-finding \
    --analyzer-arn "$ANALYZER_ARN" \
    --id "$FIRST_FINDING" \
    --output json
fi
```

---

## Cleanup

```bash
# Delete Well-Architected Tool workload
aws wellarchitected delete-workload --workload-id "$WORKLOAD_ID"

# Delete IAM Access Analyzer
aws accessanalyzer delete-analyzer --analyzer-name "lab-account-analyzer"

# Delete anomaly monitor
MONITOR_ARN=$(aws ce list-cost-category-definitions --query 'CostCategoryReferences[0]' 2>/dev/null)
# Manual listing of monitors:
aws ce get-anomaly-monitors --query 'AnomalyMonitors[*].[MonitorArn, MonitorName]' --output table

# Clean up Compute Optimizer bucket
aws s3 rm "s3://${REPORT_BUCKET}" --recursive
aws s3api delete-bucket --bucket "$REPORT_BUCKET" 2>/dev/null

echo "Cleanup complete. Well-Architected Tool, Access Analyzer deleted."
```

---

## What You Learned

- **WAT (Well-Architected Tool):** create workloads, answer questions by pillar, generate milestones, track HIGH/MEDIUM/NONE risks
- **Trusted Advisor:** automatic checks in 5 categories; manual refresh available via CLI
- **Compute Optimizer:** right-sizing recommendations based on CloudWatch metrics (requires 14+ days of data)
- **Cost Explorer:** analysis by service, tag, daily/monthly granularity, forecasting
- **Savings Plans:** choose between COMPUTE_SP (more flexible) and EC2_SP (cheaper for fixed type)
- **IAM Access Analyzer:** detects resources with unintended external access (S3, SQS, Lambda, etc.)

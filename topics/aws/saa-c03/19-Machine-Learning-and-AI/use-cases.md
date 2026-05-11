# Real Use Cases — Machine Learning and AI (Module 13)

## Case 1 — Product Recommendation System

**Context:** E-commerce with 10 million users needs personalized recommendations in real time on the product page ("customers who bought X also bought Y") and in personalized email campaigns by segment.

**Requirements:**
- Real-time recommendations (< 200ms per request)
- Model retrained daily with new behavioral data
- No dedicated ML team required — use managed service
- Segmentation for batch marketing campaigns

**Architecture:**
```
INPUT DATA:
Clickstream → Kinesis → S3 (user-product interactions)
Orders      → S3 (purchase history)

TRAINING (daily — batch):
S3 (interactions) → Amazon Personalize
                    ├── Dataset Group
                    ├── Solution (USER_PERSONALIZATION algorithm)
                    └── Campaign (inference endpoint)

INFERENCE (real time):
App → Amazon Personalize Campaign → JSON Recommendations
App → ElastiCache (cache result by user_id, TTL 1h)

BATCH (email campaigns):
EventBridge (daily) → Lambda → Personalize Batch Inference
                                  └── S3 (recommendations by segment)
                                            └── SES (personalized emails)
```

**Personalize vs SageMaker for this case:**
| Criterion | Personalize | SageMaker |
|---------|-------------|-----------|
| ML team required | No | Yes |
| Available algorithms | Recommendation/ranking | Any |
| Setup time | Hours | Days/weeks |
| Flexibility | Low | High |
| Cost | Per TPS + training hours | Per instance |

---

## Case 2 — Financial Document Analysis with Textract + Comprehend

**Context:** Insurance company needs to process 5,000 documents/day (claim forms, medical reports, invoices) to accelerate policy analysis. Manual process takes 3 days per claim.

**Requirements:**
- Extract structured data from forms (fields, tables)
- Detect PII information (SSN, name, date of birth) for protection
- Classify document type (claim/report/invoice)
- Verify consistency of extracted data

**Architecture:**
```
Documents (PDF/image) → S3 (incoming-claims)
                              │ S3 Event Notification
                              ▼
                         Lambda (orchestrator)
                         ├── Textract StartDocumentAnalysis (async)
                         │     (extracts forms + tables)
                         │     └── SNS callback → Lambda (result)
                         ├── Comprehend DetectPiiEntities
                         │     (detects SSN, name, date)
                         ├── Comprehend ClassifyDocument
                         │     (type: claim/report/invoice)
                         └── Comprehend DetectSentiment
                               (customer urgency in free text)
                              │
                         DynamoDB (metadata + extracted fields)
                         S3 (structured JSON result)
                         Step Functions (human approval flow if confidence < 80%)

A2I (Augmented AI) → Human review when Textract has low confidence
```

**Time Reduction:**
- Before: 3 days (manual) → After: 2 hours (automated)
- Automation rate: 85% of documents without human review
- A2I covers the 15% with low confidence

---

## Case 3 — Customer Service Chatbot with Lex v2 + Lambda

**Context:** Telecommunications company wants to reduce call volume (200,000/month) to customer support by offering a chatbot that resolves the 5 most common issues: check bill, duplicate invoice, cancel services, check data balance, change plan.

**Requirements:**
- Understand natural language in Portuguese
- Authenticate user before sensitive operations
- Escalate complex calls to human agent
- Integrate with existing CRM system (REST API)

**Architecture:**
```
User (WhatsApp / App / Web)
       │
       ▼
Amazon Lex v2 (Bot in Portuguese)
  Intents:
  ├── CheckBill     → Lambda (queries CRM API)
  ├── GenerateInvoice → Lambda (generates PDF invoice → S3 → URL)
  ├── CancelService → Lambda (checks contract + calls CRM)
  ├── CheckData     → Lambda (queries telemetry system)
  └── ChangePlan    → Lambda (plan options + Step Functions workflow)

  Authentication:
  ├── Slot: SSN + date of birth
  └── Lambda validator → queries DynamoDB (authenticated session)

  Fallback:
  └── Intent: TransferToAgent → Amazon Connect (transfer)

Amazon Connect (integrated call center)
CloudWatch (metrics: intent recognition rate, transfer rate)
```

**Success Metrics:**
| KPI | Before | After |
|-----|--------|-------|
| Resolution without agent | 0% | 65% |
| Average resolution time | 8 min | 90 sec |
| Cost per interaction | $15 | $0.12 |
| Satisfaction (CSAT) | 3.2/5 | 4.1/5 |

---

## Case 4 — Content Moderation with Rekognition

**Context:** UGC (User Generated Content) platform with 500,000 image/video uploads per day needs to automatically remove inappropriate content (violence, nudity, drugs) before publishing.

**Requirements:**
- Analyze 100% of content before publishing
- False positives < 5% (valid content blocked)
- Human review for borderline cases (confidence 50-80%)
- Audit trail of decisions (legal compliance)

**Architecture:**
```
User upload → S3 (content-pending)
                    │ Lambda trigger
                    ▼
               Lambda (moderator)
               ├── Rekognition DetectModerationLabels
               │     (nudity, violence, drugs, etc.)
               │
               ├── If score > 80% (inappropriate):
               │     └── Move to S3 (content-blocked)
               │         DynamoDB (log: blocked + reason)
               │         SNS → User email (notification)
               │
               ├── If score 20-80% (uncertain):
               │     └── A2I (Augmented AI) → Human review queue
               │         Step Functions awaits human decision
               │
               └── If score < 20% (approved):
                     └── S3 (content-approved) → CloudFront

Audit: DynamoDB Streams → Lambda → S3 (immutable compliance log)
```

**Rekognition for Video:**
```
Video upload → S3 → Lambda → Rekognition StartContentModeration (async)
                                  │ SNS callback when complete
                                  ▼
                             Lambda (process result)
                             ├── Timestamps of inappropriate scenes
                             └── Decision: approve/reject/segment
```

---

## Case 5 — Demand Forecasting for Inventory Management

**Context:** Supermarket chain needs to forecast demand for 50,000 SKUs over the next 4 weeks to optimize replenishment orders and reduce waste.

**Requirements:**
- Forecast per SKU + store + week
- Consider seasonality, holidays, promotions
- Retrain model monthly with new data
- Integrate forecasts with ERP purchasing system

**Architecture:**
```
HISTORICAL DATA:
S3 (daily sales for last 3 years, per SKU/store)
S3 (external data: holidays, promotions, weather)

AMAZON FORECAST:
├── Dataset Group (sales + metadata + related items)
├── Predictor (algorithm: AutoML selects the best)
│     (options: DeepAR+, Prophet, NPTS, CNN-QR)
└── Forecast (generates P10/P50/P90 for 28 days)

INFERENCE + INTEGRATION:
EventBridge (1x/week) → Lambda
     │
     ├── CreateForecastExportJob → S3 (forecasts.csv)
     ├── Lambda processes CSV → DynamoDB (suggested_orders table)
     └── REST API ERP → reads DynamoDB → generates purchase orders

QuickSight (dashboard: forecast vs actual, MAPE accuracy)
SNS → Alert if MAPE > 15% (model degrading)
```

**Accuracy Metrics:**
| Metric | Typical Value | What it means |
|---------|-------------|----------------|
| MAPE | < 15% | Mean Absolute Percentage Error |
| WAPE | < 10% | Weighted APE (considers volume) |
| P50 | median forecast | 50% confidence |
| P90 | optimistic limit | For safety stock |

---

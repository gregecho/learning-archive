# Cheatsheet — Module 13: Machine Learning and AI

## The 3 Layers of the AWS AI/ML Framework

```
┌─────────────────────────────────────────────────────────────────────┐
│       Level 1: AI Services (no ML knowledge required)               │
│  Rekognition | Comprehend | Polly | Transcribe | Translate | Lex    │
│  Textract | Kendra | Bedrock | Fraud Detector | Personalize          │
│  Forecast | Lookout for Metrics | Lookout for Vision                 │
├─────────────────────────────────────────────────────────────────────┤
│       Level 2: ML Services (build/train/deploy your models)          │
│  SageMaker Studio | Ground Truth | Experiments | Model Monitor      │
│  Training Jobs | Hyperparameter Tuning | Feature Store | Pipelines  │
├─────────────────────────────────────────────────────────────────────┤
│       Level 3: Infrastructure (specialized hardware)                 │
│  EC2 GPU (p3, p4, g4) | AWS Trainium | AWS Inferentia               │
└─────────────────────────────────────────────────────────────────────┘
```

---

## Comparison — Natural Language Services (NLP)

| Service | Direction | Input | Output |
|---|---|---|---|
| **Amazon Transcribe** | Audio → Text (STT) | Audio (MP3, WAV, FLAC) | Text + timestamps |
| **Amazon Polly** | Text → Audio (TTS) | Text / SSML | Audio (MP3, PCM) |
| **Amazon Translate** | Text → Text | Text in language X | Text in language Y |
| **Amazon Comprehend** | Text → Analysis | Text | Entities, Sentiment, PII, Topics |
| **Amazon Lex v2** | Conversation → Intent | Text or Audio | Intent + Filled Slots |
| **Amazon Kendra** | Question → Answer | Natural language question | Answer from documents |

---

## Comparison — Computer Vision and Documents

| Service | Input | Output |
|---|---|---|
| **Rekognition Image** | Image | Objects, faces, text, moderation labels |
| **Rekognition Video** | Video (S3 or stream) | Person tracking, activity, labels over time |
| **Textract** | Document image/PDF | Text + Tables + Forms + Keys-Values |
| **Lookout for Vision** | Product images (factory) | Anomaly detected: NORMAL/ANOMALY |

---

## SageMaker — ML Pipeline

| Phase | Service/Feature |
|---|---|
| **Data Labeling** | Ground Truth |
| **Data Preparation** | Data Wrangler, Processing Jobs |
| **Feature Engineering** | Feature Store |
| **Model Training** | Training Jobs (EC2) |
| **Hyperparameter Tuning** | Automatic Model Tuning (HPO) |
| **Model Evaluation** | Experiments |
| **Model Registry** | Model Registry (versioning) |
| **Deployment Online** | Endpoint (real-time inference) |
| **Deployment Batch** | Batch Transform |
| **Model Monitoring** | Model Monitor (drift detection) |
| **No-Code** | Canvas (business users) |

---

## Amazon Bedrock — Available Foundation Models

| Provider | Models |
|---|---|
| **Amazon** | Titan Text, Titan Embeddings, Titan Image Generator |
| **Anthropic** | Claude 3 (Haiku, Sonnet, Opus) |
| **Meta** | Llama 3 |
| **Cohere** | Command R, Embed |
| **Mistral AI** | Mistral, Mixtral |
| **Stability AI** | Stable Diffusion (images) |

**RAG:** Bedrock Knowledge Bases → OpenSearch Serverless (vector store) → contextualized LLM.

---

## Comparison — Recommendation and Forecasting Services

| Service | Use Case | Input | Output |
|---|---|---|---|
| **Personalize** | Personalized recommendations | User-item interactions + metadata | Top-N items per userId |
| **Forecast** | Time series forecasting | Historical data + metadata | Future values + intervals |
| **Fraud Detector** | Fraud detection | Transaction events | Fraud score |
| **Lookout for Metrics** | Anomalies in business metrics | Metrics from S3/RDS/Redshift | Anomaly alerts |

---

## Comprehend — Available Analyses

| Analysis | Description | Example |
|---|---|---|
| **Entity Recognition** | People, places, orgs, dates | "John works at Amazon in New York" |
| **Sentiment Analysis** | Positive/Negative/Neutral/Mixed | Product review |
| **Key Phrases** | Main expressions in text | "aws certification", "cloud computing" |
| **Language Detection** | Identifies the language | en-US, pt-BR, es |
| **PII Detection** | SSN, email, phone, etc. | Redaction of personal data |
| **Topic Modeling** | Groups documents by theme | Support ticket analysis |
| **Targeted Sentiment** | Sentiment per mentioned entity | "camera" → positive, "battery" → negative |

**Comprehend Medical:** specialized in clinical text (diagnoses, medications, procedures).

---

## Rekognition — Features by Type

| Feature | Image | Video |
|---|---|---|
| Object/scene detection | Yes | Yes (with timestamps) |
| Facial recognition | Yes (compare, search) | Yes (person tracking) |
| Text detection (OCR) | Yes | Yes |
| Content moderation | Yes | Yes |
| PPE detection | Yes | Yes |
| Celebrity detection | Yes | Yes |
| Activity analysis | No | Yes |

---

## SageMaker Deployment Options

| Option | Latency | Use |
|---|---|---|
| **Real-time Endpoint** | Milliseconds | Online inference, one request at a time |
| **Serverless Inference** | Seconds (cold start) | Intermittent traffic, no idle cost |
| **Async Inference** | Minutes | Large payload, queues |
| **Batch Transform** | Hours | Batch inference (S3 input → S3 output) |
| **Multi-Model Endpoint** | Low | Host multiple models on 1 endpoint |

---

## Exam Tips — Which AI Service to Use

| Scenario | AWS Service |
|---|---|
| "Transcribe call center calls" | Amazon Transcribe (+ Call Analytics) |
| "Generate synthetic voice for IVR" | Amazon Polly (NTTS) |
| "Detect adult content in user photos" | Amazon Rekognition Content Moderation |
| "Extract fields from scanned forms" | Amazon Textract |
| "Sentiment analysis of reviews" | Amazon Comprehend |
| "Natural language chatbot" | Amazon Lex v2 |
| "Intelligent search in Word/PDF documents" | Amazon Kendra |
| "Personalized product recommendations" | Amazon Personalize |
| "Inventory demand forecasting" | Amazon Forecast |
| "Detect fraud in transactions" | Amazon Fraud Detector |
| "Detect anomalies in revenue metrics" | Amazon Lookout for Metrics |
| "Use LLM models via API without training" | Amazon Bedrock |
| "Train custom ML model" | Amazon SageMaker |
| "Label image data for training" | SageMaker Ground Truth |
| "NLP on clinical medical text" | Amazon Comprehend Medical |
| "Product quality scanner on factory floor" | Amazon Lookout for Vision |

---

# Module 13 — Machine Learning and Artificial Intelligence

## Overview of AWS ML/AI Services

AWS offers 3 layers of ML services:
```
Layer 1 — AI Services (ready to use, no ML expertise)
  Rekognition, Comprehend, Polly, Transcribe, Translate, Lex, Textract,
  Forecast, Personalize, Kendra, CodeWhisperer, Bedrock

Layer 2 — ML Services (managed platform)
  Amazon SageMaker (train, optimize, deploy custom models)

Layer 3 — ML Frameworks + Infrastructure
  EC2 (GPU instances p3/p4), EKS + Karpenter, Deep Learning AMIs
```

---

## Amazon SageMaker

Complete managed ML platform:

### ML Flow with SageMaker

```
Data (S3) → SageMaker Studio (web IDE)
              ├── Data Wrangler: visual data preparation
              ├── Experiments: experiment tracking
              ├── Training Job: trains model on managed instances
              │     ├── Built-in algorithms (XGBoost, Linear Learner, etc.)
              │     ├── Custom container (your Docker code)
              │     └── Spot instances (up to 90% discount, Managed Spot Training)
              ├── Hyperparameter Tuning: automatically optimizes hyperparameters
              ├── Model Registry: versions and governs models
              └── Deployment:
                    ├── Real-time Endpoint (ms latency, auto-scaling)
                    ├── Serverless Inference (no active instance to maintain)
                    ├── Batch Transform (batch inference on S3)
                    └── Async Inference (long jobs, result in S3)
```

### SageMaker — Important Features

| Feature | Description |
|---|---|
| **SageMaker Studio** | Jupyter-based IDE for the entire ML cycle |
| **Autopilot** | AutoML — automatically finds the best model |
| **Canvas** | AutoML with no-code interface (no Python code) |
| **Ground Truth** | Data labeling with humans (public + private workforce) |
| **Clarify** | Detects bias in data and model explainability |
| **Feature Store** | Shared feature database between training and inference |
| **Pipelines** | CI/CD for ML (MLOps) |
| **JumpStart** | Pre-trained models and ready-made ML solutions |

---

## Amazon Rekognition

Managed computer vision (images and videos):
- **Object/Scene Detection**: identifies objects, activities, scenes
- **Facial Analysis**: detection, attribute analysis, comparison, recognition
- **Text Detection**: OCR in images (license plates, documents)
- **Content Moderation**: detects inappropriate content (violence, nudity)
- **PPE Detection**: Personal Protective Equipment (helmet, mask)
- **Celebrity Recognition**: identifies celebrities in images
- **Video Analysis**: real-time video stream analysis via Kinesis Video Streams

---

## Amazon Comprehend

Managed NLP (Natural Language Processing):
- **Entity/Sentiment Analysis**: detects entities (people, places, organizations) and sentiment (positive, negative, neutral, mixed)
- **Topic Modeling**: discovers topics in document collections
- **Key Phrase Extraction**: key phrases from text
- **Language Detection**: identifies text language
- **PII Detection/Redaction**: detects and redacts Personally Identifiable Information (SSN, email, phone)
- **Custom Models**: trains custom classifiers and entity recognizers

---

## Amazon Polly

Text-to-Speech (TTS):
- Converts text to natural speech in multiple languages and voices
- **Neural TTS (NTTS)**: more natural and expressive voices
- **SSML** (Speech Synthesis Markup Language): fine control of pronunciation, pauses, emphasis
- **Speech Marks**: metadata with word/phrase timestamps (useful for karaoke or synchronized subtitles)
- **Lexicon**: specializes pronunciation of specific words (acronyms, technical terms)

---

## Amazon Transcribe

Speech-to-Text (STT):
- Average accuracy with domain-specific custom models
- **Custom Vocabulary**: adds specific terms (product names, jargon)
- **Custom Language Model**: custom language model for specific domain
- **Speaker Diarization**: identifies who is speaking in each segment
- **Medical Transcribe**: specialized medical vocabulary (HIPAA eligible)
- **Call Analytics**: call center call analysis (sentiment, silences, interruptions)
- **Streaming**: real-time transcription

---

## Amazon Translate

Neural machine translation:
- High-quality translation in 75+ languages
- **Custom Terminology**: glossary of terms that should not be translated or have specific translation
- **Active Custom Translation**: adapts the model with provided translation examples
- **Parallel Data**: trains with original and translated sentence pairs
- Integrates with S3 for batch document translation

---

## Amazon Lex

Conversational chatbots (same engine as Alexa):
- **Intents**: actions the user wants to perform (e.g., `BookFlight`, `CheckBalance`)
- **Slots**: variables to collect (e.g., `travel_date`, `destination`)
- **Utterances**: phrases that trigger the intent
- **Fulfillment**: Lambda processes the intent and returns a response
- **Channels**: integrates with Facebook, Slack, Twitch, Kik
- **Amazon Connect**: Lex can be the call center bot

---

## Amazon Bedrock

Foundation Models (FM) via API — Generative AI:
- Models from: Anthropic (Claude), Amazon (Titan), Stability AI, Cohere, AI21, Meta (Llama)
- **Serverless**: no infrastructure to manage; pay per token
- **RAG with Knowledge Bases**: manages embeddings (OpenSearch Serverless) + retrieval automatically
- **Agents**: defines actions and Lambda functions that the model can execute autonomously
- **Fine-tuning**: adapts base models with your own data (S3)
- **Model Evaluation**: compares outputs of different models with automatic and human metrics
- **Guardrails**: applies content filters, PII redaction, topic denial to model responses

---

## Other AI Services

| Service | Function |
|---|---|
| **Amazon Textract** | Advanced OCR: extracts text, tables, and forms from PDF/image documents |
| **Amazon Kendra** | Enterprise search with NLP (finds answers in corporate documents) |
| **Amazon Forecast** | Time series forecasting (demand, sales, resource usage) |
| **Amazon Personalize** | Personalized recommendations (like Netflix/Amazon.com) — no ML expertise |
| **Amazon Fraud Detector** | Fraud detection (purchases, fake accounts) with ML |
| **Amazon Lookout for Metrics** | Automatically detects anomalies in business metrics |
| **Amazon CodeWhisperer** | AI code generation in the IDE (based on Bedrock) |

---

## Exam Tips

- **Rekognition**: vision (image/video) → Transcribe: speech→text → Polly: text→speech
- **Comprehend**: text analysis (sentiment, entities) → different from Rekognition (images)
- **Kendra**: enterprise search (answering questions in documents) → different from OpenSearch (analytics)
- **Forecast vs Personalize**: Forecast = time series forecasting (demand, inventory); Personalize = user-item recommendations
- SageMaker Ground Truth: human labeling → **Rekognition Custom Labels** also trains with labeled images (simpler)
- **Textract** recognizes **tables and forms** (not just simple text like traditional OCR)
- Bedrock: **Foundation Models via API** without training a model from scratch — different from SageMaker (train custom model)
- SageMaker Managed Spot Training: uses Spot instances for training jobs → up to 90% cost reduction; checkpointing required to resume after interruption
- **Comprehend PII**: detects/redacts sensitive data in text (e.g., GDPR compliance)
- **Amazon Connect + Lex**: automated call center; no telephony infrastructure to manage

---

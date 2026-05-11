# Flashcards — Module 13: Machine Learning and AI

> **Format:** Q = Question | A = Answer
> **Total:** 25 flashcards

---

**Q:** What are the 3 layers of the AWS AI/ML framework?
**A:** **(1) AI Services (top):** Ready-to-use APIs without ML knowledge — Rekognition, Comprehend, Polly, Transcribe, Translate, Lex, Textract, Kendra, Bedrock. **(2) ML Services (middle):** SageMaker (custom build-train-deploy). **(3) Infrastructure (base):** EC2 GPU, Trainium, Inferentia for training/inference at scale.

---

**Q:** What is Amazon Bedrock and how does it differ from SageMaker?
**A:** **Bedrock:** access to Foundation Models (LLMs) from third parties via API (Anthropic Claude, Amazon Titan, Meta Llama, Mistral, Cohere, Stability AI) without training models. **SageMaker:** platform for training, tuning, and deploying custom ML models. Bedrock = use ready-made models; SageMaker = build custom models.

---

**Q:** What is RAG in the context of Amazon Bedrock?
**A:** Retrieval Augmented Generation: technique that connects LLMs to an external knowledge base. Flow: user asks → system retrieves relevant context from the base → sends context + question to the LLM → LLM generates an answer grounded in current data. Bedrock Knowledge Bases implements RAG with Amazon OpenSearch Serverless as a vector store.

---

**Q:** For which use case should Amazon Rekognition be used?
**A:** **Image and video analysis:** object/scene/text detection, facial recognition (comparison, collection search), inappropriate content detection (moderation), PPE analysis, celebrity detection, video analysis in streaming or batch. No ML knowledge required.

---

**Q:** What is the difference between Amazon Transcribe and Amazon Polly?
**A:** **Transcribe:** Speech-to-Text (STT) — converts audio to text. Features: diarization (identifying who is speaking), custom vocabulary, PII redaction, automatic language identification. **Polly:** Text-to-Speech (TTS) — converts text to audio. Features: neural voices (NTTS), SSML for pronunciation control, custom lexicons.

---

**Q:** What is Amazon Comprehend and what are its main analyses?
**A:** NLP service for text analysis without ML code. Analyses: **Entities** (people, organizations, places), **Key Phrases** (key expressions), **Sentiment** (positive/negative/neutral/mixed), **Language Detection**, **PII Detection/Redaction**, **Topic Modeling** (group documents by latent themes). Comprehend Medical: specialized version for clinical texts.

---

**Q:** What is Amazon Lex v2 and what is it used for?
**A:** Managed service for creating **chatbots and virtual assistants** for voice and text. Uses ASR (Automatic Speech Recognition) + NLU (Natural Language Understanding). Intents = actions; Slots = parameters to collect. Basis of Alexa. Use case: IVR, customer service bots, help desk assistants. No ML knowledge required.

---

**Q:** What is the difference between Amazon Kendra and Amazon OpenSearch?
**A:** **Kendra:** intelligent search for corporate documents using ML and NLP. Understands natural language, semantic search, answers questions directly. Input: PDFs, Word, SharePoint, Salesforce, S3. **OpenSearch:** technical search and analytics (logs, metrics, e-commerce search, full-text search). Kendra = intelligent for humans; OpenSearch = technical/full-text.

---

**Q:** For which scenario should Amazon SageMaker Ground Truth be used?
**A:** **Data labeling** for ML model training. Flow: humans (crowdworkers via Amazon Mechanical Turk or private workforce) annotate/label images, texts, videos. Active Learning: partially trained models automatically label high-confidence data, reducing human labeling cost by up to 70%.

---

**Q:** What is Amazon Textract and how does it differ from simple OCR?
**A:** **Textract:** extracts text + **structure** from scanned documents. Goes beyond OCR: detects Tables (extracts headers and cells), Forms (extracts field:value from forms), Queries (answers specific questions about the document). Supports multi-page PDFs, IDs (passports, driver's licenses), medical documents.

---

**Q:** What is Amazon Fraud Detector?
**A:** Managed fraud detection service using ML. Models pre-trained on AWS fraud data + customer historical data. Detection events: new account registrations, online payments, guest checkout. Returns a fraud score. No ML expertise required.

---

**Q:** What are the stages of the SageMaker ML pipeline?
**A:** **(1) Data prep:** SageMaker Data Wrangler / Processing Jobs. **(2) Training:** Training Jobs (EC2 instances). **(3) Tuning:** Hyperparameter Optimization (HPO). **(4) Evaluation:** Experiments. **(5) Registry:** Model Registry. **(6) Deploy:** SageMaker Endpoints (online) / Batch Transform (offline). **(7) Monitor:** Model Monitor.

---

**Q:** What is Amazon SageMaker Feature Store?
**A:** Centralized repository of features (input variables) for ML models. Allows: sharing features across teams and models, reusing computed features, consistency between training and inference (same calculation). **Online Store:** low latency for real-time inference. **Offline Store:** history via S3 for training.

---

**Q:** What is Amazon Forecast and what problem does it solve?
**A:** Managed **time series forecasting** service using DeepAR+ (Amazon proprietary algorithm). Input: historical time series data (sales, demand, traffic) + metadata (promotions, holidays). Output: future forecasts with confidence intervals. Use cases: demand planning, supply chain, capacity planning.

---

**Q:** What is Amazon Personalize and what type of recommendation does it serve?
**A:** Managed **personalized recommendations** service (same used by Amazon.com/Prime Video). Input: user-item interaction data (clicks, purchases, plays), item/user metadata. Output: real-time recommendations by userId. Use cases: "other users also bought", "continue watching", "recommended products".

---

**Q:** What is Amazon Lookout for Metrics?
**A:** Automatic **time series anomaly detection** using ML. Input: business metrics (revenue, DAUs, conversion rate) from S3, RDS, Redshift, Salesforce, etc. Automatically detects significant deviations. Sends alerts via SNS. No ML knowledge required. Different from CloudWatch Anomaly Detection (technical infrastructure metrics).

---

**Q:** What is Amazon SageMaker Jumpstart?
**A:** Hub of pre-trained models and ready-to-deploy ML solutions in one click. Contains: Foundation Models (Llama, Mistral, Falcon), vision models (ResNet, EfficientNet), NLP (BERT, RoBERTa), industry solutions (demand forecast, fraud). Accelerates ML project start without starting from scratch.

---

**Q:** What are Amazon Bedrock Guardrails?
**A:** Security controls for applications with Foundation Models. Features: content filters (violence, hate speech, sexual), topic denial (block prohibited topics — e.g., competitors), PII redaction, word filters. Automatically applied to user input AND model response.

---

**Q:** For which scenario should Amazon Translate with Custom Terminology be used?
**A:** When there are company/product-specific terms that should not be automatically translated (product names, corporate jargon, acronyms). Custom Terminology: CSV with source→target pair. Ex: "Amazon Aurora" → "Amazon Aurora" (do not translate), "order" → "pedido" (specific translation). Maintains terminological consistency in translations.

---

**Q:** What is Amazon SageMaker Canvas?
**A:** **No-code** interface for ML. Business professionals without programming experience can train ML models (classification, regression, time series forecasting, image analysis) via visual interface. Input: CSV uploads, S3. Uses AutoML under the hood. Shares models with data scientists in SageMaker Studio.

---

**Q:** What is Amazon Rekognition Content Moderation?
**A:** API that detects inappropriate or adult content in images and videos. Returns hierarchical labels with confidence score (e.g., "Explicit Nudity" > "Nudity", confidence: 99.5%). Use cases: UGC (User Generated Content) platforms, social networks, marketplaces. Companies define confidence threshold for automatic moderation.

---

**Q:** What is Amazon Transcribe Call Analytics?
**A:** Specialized version of Transcribe for call center call analysis. Beyond transcription: detects **sentiment** of each conversation turn (customer vs. agent), identifies custom categories (complaint, cancellation), extracts entities (account numbers, dates), measures silence time and interruptions.

---

**Q:** When should Amazon Comprehend Medical be used?
**A:** Extracts medical entities from clinical text: **diagnoses** (ICD-10 codes), **medications** (dosage, frequency, route of administration), **medical procedures**, **anatomy**, **vital signs**. Detects relationships (medication → dosage). HIPAA eligible. Use cases: NLP of electronic health records, medical coding, clinical research.

---

**Q:** What is Amazon Polly Neural Text-to-Speech (NTTS)?
**A:** Ultra-high-quality synthetic voices using deep learning — practically indistinguishable from human voice. More natural than standard voices (concatenation synthesis). Supports **SSML** (Speech Synthesis Markup Language) to control pauses, emphasis, pronunciation. Use cases: IVR, audiobooks, accessibility, e-learning.

---

**Q:** What is the responsibility model in Amazon Bedrock (Security)?
**A:** **AWS responsible for:** infrastructure, base model, FM training data. **Customer responsible for:** data sent to the model (prompts/context), fine-tuning data, application and generated responses. Prompts and responses **are not used to train AWS models** (customer private data). Bedrock is HIPAA/SOC/ISO eligible.

---

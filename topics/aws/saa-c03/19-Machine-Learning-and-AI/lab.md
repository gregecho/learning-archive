# Hands-On Lab — Machine Learning: Comprehend + Rekognition + Textract (Module 13)

> **Region:** us-east-1 | **Estimated cost:** < $1.00 (Free Tier includes 5K units/month Comprehend, 5K images Rekognition)
> **Prerequisites:** AWS CLI configured, Python 3.12, boto3

---

## Objective

Explore the three main "pre-trained" AI services from AWS — without training models, just consuming APIs.

---

## Part 1 — Comprehend: Text Analysis

```python
#!/usr/bin/env python3
# comprehend_demo.py

import boto3
import json

client = boto3.client('comprehend', region_name='us-east-1')

texts = [
    "The product arrived quickly and the quality is excellent! Highly recommend.",
    "Terrible service, took 30 days to deliver and arrived broken.",
    "Normal delivery, product as described. Nothing special.",
    "The customer's SSN is 123-45-6789 and email is john@example.com",
    "Amazon Web Services launched new artificial intelligence services in New York.",
]

print("=" * 60)
print("SENTIMENT ANALYSIS")
print("=" * 60)

for text in texts[:3]:
    response = client.detect_sentiment(
        Text=text,
        LanguageCode='en'
    )
    sentiment = response['Sentiment']
    scores = response['SentimentScore']
    print(f"\nText: {text[:50]}...")
    print(f"Sentiment: {sentiment}")
    print(f"Confidence: POSITIVE={scores['Positive']:.2%}, NEGATIVE={scores['Negative']:.2%}")

print("\n" + "=" * 60)
print("PII DETECTION (Personal Data)")
print("=" * 60)

response = client.detect_pii_entities(
    Text=texts[3],
    LanguageCode='en'
)

print(f"\nText: {texts[3]}")
print("PII Entities found:")
for entity in response['Entities']:
    start = entity['BeginOffset']
    end = entity['EndOffset']
    value = texts[3][start:end]
    print(f"  Type: {entity['Type']} | Value detected: {value} | Score: {entity['Score']:.2%}")

print("\n" + "=" * 60)
print("ENTITY EXTRACTION")
print("=" * 60)

response = client.detect_entities(
    Text=texts[4],
    LanguageCode='en'
)

print(f"\nText: {texts[4]}")
print("Entities found:")
for entity in response['Entities']:
    print(f"  {entity['Type']}: {entity['Text']} (score: {entity['Score']:.2%})")

print("\n" + "=" * 60)
print("LANGUAGE DETECTION")
print("=" * 60)

language_texts = [
    "This is an English sentence about cloud computing.",
    "Esta frase esta em portugues sobre computacao em nuvem.",
    "Este es un texto en espanol sobre servicios en la nube.",
]

for text in language_texts:
    response = client.detect_dominant_language(Text=text)
    lang = response['Languages'][0]
    print(f"  '{text[:40]}...' → {lang['LanguageCode']} ({lang['Score']:.2%})")
```

```bash
# Run
python3 comprehend_demo.py
```

---

## Part 2 — Rekognition: Image Analysis

```python
#!/usr/bin/env python3
# rekognition_demo.py

import boto3
import urllib.request
import json

client = boto3.client('rekognition', region_name='us-east-1')
s3 = boto3.client('s3', region_name='us-east-1')

# Use public image via URL (Rekognition can receive bytes directly)
# For the lab, let's create a test image via S3

import boto3, os

ACCOUNT_ID = boto3.client('sts').get_caller_identity()['Account']
BUCKET = f"lab-rekognition-{ACCOUNT_ID}"

# Create temporary bucket
s3_resource = boto3.resource('s3', region_name='us-east-1')
try:
    s3_resource.create_bucket(Bucket=BUCKET)
except Exception as e:
    print(f"Bucket already exists or error: {e}")

# Download public test image (photo of people in landscape)
test_image_url = "https://upload.wikimedia.org/wikipedia/commons/thumb/4/43/Cute_dog.jpg/320px-Cute_dog.jpg"
urllib.request.urlretrieve(test_image_url, "/tmp/test_image.jpg")

# Upload to S3
s3.upload_file("/tmp/test_image.jpg", BUCKET, "test_image.jpg")

print("=" * 60)
print("LABEL DETECTION (objects/scenes)")
print("=" * 60)

response = client.detect_labels(
    Image={'S3Object': {'Bucket': BUCKET, 'Name': 'test_image.jpg'}},
    MaxLabels=10,
    MinConfidence=80.0
)

for label in response['Labels']:
    print(f"  {label['Name']:30} Confidence: {label['Confidence']:.1f}%")

print("\n" + "=" * 60)
print("CONTENT MODERATION")
print("=" * 60)

response = client.detect_moderation_labels(
    Image={'S3Object': {'Bucket': BUCKET, 'Name': 'test_image.jpg'}},
    MinConfidence=50.0
)

if response['ModerationLabels']:
    for label in response['ModerationLabels']:
        print(f"  ALERT: {label['Name']} (Parent: {label['ParentName']}) — {label['Confidence']:.1f}%")
else:
    print("  No inappropriate content detected ✓")

print("\n" + "=" * 60)
print("FACE COMPARISON (simulation with same image)")
print("=" * 60)

# Simulate with same image (same face)
response = client.compare_faces(
    SourceImage={'S3Object': {'Bucket': BUCKET, 'Name': 'test_image.jpg'}},
    TargetImage={'S3Object': {'Bucket': BUCKET, 'Name': 'test_image.jpg'}},
    SimilarityThreshold=80
)

print(f"  Faces found in source: {len(response.get('SourceImageFace', {})) > 0}")
print(f"  Comparisons: {len(response.get('FaceMatches', []))} matches found")

# S3 Cleanup
s3.delete_object(Bucket=BUCKET, Key='test_image.jpg')
s3.delete_bucket(Bucket=BUCKET)
print("\nTest bucket removed.")
```

```bash
python3 rekognition_demo.py
```

---

## Part 3 — Textract: Document Extraction

```python
#!/usr/bin/env python3
# textract_demo.py

import boto3
import json

client = boto3.client('textract', region_name='us-east-1')

# Create a simple PDF document for Textract to analyze
# (Textract accepts PNG/JPEG/PDF/TIFF)
# For the lab, we create a PNG image with text

from PIL import Image, ImageDraw, ImageFont
import io

# Create image with text simulating a form
img = Image.new('RGB', (600, 400), color='white')
draw = ImageDraw.Draw(img)

draw.text((50, 30), "REGISTRATION FORM", fill='black')
draw.text((50, 80), "Name: John Silva Santos", fill='black')
draw.text((50, 120), "SSN: 000-00-0000", fill='black')
draw.text((50, 160), "Date of Birth: 06/15/1985", fill='black')
draw.text((50, 200), "Email: john.silva@company.com", fill='black')
draw.text((50, 240), "Phone: (11) 99999-0000", fill='black')
draw.text((50, 300), "Total Amount: $1,500.00", fill='black')
draw.text((50, 340), "Status: Approved", fill='black')

img_bytes = io.BytesIO()
img.save(img_bytes, format='PNG')
img_bytes.seek(0)

print("=" * 60)
print("TEXT EXTRACTION (DetectDocumentText)")
print("=" * 60)

response = client.detect_document_text(
    Document={'Bytes': img_bytes.getvalue()}
)

print("Text extracted line by line:")
for block in response['Blocks']:
    if block['BlockType'] == 'LINE':
        print(f"  [{block['Confidence']:.1f}%] {block['Text']}")

print("\n" + "=" * 60)
print("FORM ANALYSIS (AnalyzeDocument FORMS)")
print("=" * 60)

img_bytes.seek(0)
response = client.analyze_document(
    Document={'Bytes': img_bytes.getvalue()},
    FeatureTypes=['FORMS']
)

key_blocks = {}
value_blocks = {}

for block in response['Blocks']:
    if block['BlockType'] == 'KEY_VALUE_SET':
        if 'KEY' in block['EntityTypes']:
            key_blocks[block['Id']] = block
        else:
            value_blocks[block['Id']] = block

print("Key-value pairs detected:")
for key_id, key_block in key_blocks.items():
    # Extract key text
    key_text = ' '.join([
        w['Text'] for w in [
            next((b for b in response['Blocks'] if b['Id'] == rel['Ids'][0]), None)
            for rel in key_block.get('Relationships', []) if rel['Type'] == 'CHILD'
        ] if w and w.get('BlockType') == 'WORD'
    ])

    # Extract value text
    value_text = ''
    for rel in key_block.get('Relationships', []):
        if rel['Type'] == 'VALUE':
            value_block = value_blocks.get(rel['Ids'][0])
            if value_block:
                for vrel in value_block.get('Relationships', []):
                    if vrel['Type'] == 'CHILD':
                        for word_id in vrel['Ids']:
                            word = next((b for b in response['Blocks'] if b['Id'] == word_id), None)
                            if word and word['BlockType'] == 'WORD':
                                value_text += word['Text'] + ' '

    if key_text and value_text:
        print(f"  {key_text.strip()}: {value_text.strip()}")
```

```bash
# Install dependencies
pip3 install boto3 Pillow

python3 textract_demo.py
```

---

## Part 4 — Complete Pipeline: Automatic Moderation with Lambda

```bash
# Create Lambda that automatically moderates images
cat > moderation_lambda.py << 'EOF'
import boto3
import json
import os

rekognition = boto3.client('rekognition')
s3 = boto3.client('s3')

def lambda_handler(event, context):
    for record in event['Records']:
        bucket = record['s3']['bucket']['name']
        key = record['s3']['object']['key']

        response = rekognition.detect_moderation_labels(
            Image={'S3Object': {'Bucket': bucket, 'Name': key}},
            MinConfidence=75
        )

        labels = response['ModerationLabels']

        if labels:
            print(f"INAPPROPRIATE CONTENT in s3://{bucket}/{key}")
            for label in labels:
                print(f"  - {label['Name']}: {label['Confidence']:.1f}%")

            # Move to quarantine bucket
            quarantine_bucket = os.environ.get('QUARANTINE_BUCKET', bucket + '-quarantine')
            s3.copy_object(
                Bucket=quarantine_bucket,
                CopySource={'Bucket': bucket, 'Key': key},
                Key=f"quarantine/{key}"
            )
            s3.delete_object(Bucket=bucket, Key=key)
            return {'status': 'blocked', 'labels': [l['Name'] for l in labels]}
        else:
            print(f"Content approved: s3://{bucket}/{key}")
            return {'status': 'approved'}
EOF

zip moderation_lambda.zip moderation_lambda.py

# Deploy via CLI
aws lambda create-function \
  --function-name lab-image-moderation \
  --runtime python3.12 \
  --role arn:aws:iam::$(aws sts get-caller-identity --query Account --output text):role/lab-lambda-rekognition-role \
  --handler moderation_lambda.lambda_handler \
  --zip-file fileb://moderation_lambda.zip \
  --timeout 30
```

---

## Cleanup

```bash
# Remove Lambda
aws lambda delete-function --function-name lab-image-moderation

# Remove local files
rm -f *.zip *.py /tmp/test_image.jpg
```

---

## What You Learned

- Comprehend detects sentiment, PII, entities, and language without training models
- Rekognition detects objects, faces, celebrities, and inappropriate content
- Textract extracts text and key-value pairs from forms (far beyond simple OCR)
- All 3 services: pay-per-use, no provisioning, natively integrate with S3
- Free Tier allows experimenting at no cost: Comprehend 5K units/month, Rekognition 5K images

---

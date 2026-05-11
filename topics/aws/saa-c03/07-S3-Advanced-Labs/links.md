# Links and Resources — S3 Advanced (Module 08)

## Official AWS Documentation

- [Amazon S3 — Official Documentation](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Welcome.html)
- [S3 — Versioning](https://docs.aws.amazon.com/AmazonS3/latest/userguide/Versioning.html)
- [S3 — Lifecycle Policies](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lifecycle-mgmt.html)
- [S3 — Cross-Region Replication (CRR)](https://docs.aws.amazon.com/AmazonS3/latest/userguide/replication.html)
- [S3 — Presigned URLs](https://docs.aws.amazon.com/AmazonS3/latest/userguide/ShareObjectPreSignedURL.html)
- [S3 — Event Notifications](https://docs.aws.amazon.com/AmazonS3/latest/userguide/NotificationHowTo.html)
- [S3 — Multipart Upload](https://docs.aws.amazon.com/AmazonS3/latest/userguide/mpuoverview.html)
- [S3 Transfer Acceleration](https://docs.aws.amazon.com/AmazonS3/latest/userguide/transfer-acceleration.html)
- [S3 — Block Public Access](https://docs.aws.amazon.com/AmazonS3/latest/userguide/access-control-block-public-access.html)
- [S3 Object Lock and WORM](https://docs.aws.amazon.com/AmazonS3/latest/userguide/object-lock.html)

## FAQs

- [Amazon S3 FAQ](https://aws.amazon.com/s3/faqs/)

## Whitepapers

- [Security Best Practices for Amazon S3](https://docs.aws.amazon.com/AmazonS3/latest/userguide/security-best-practices.html)

## AWS Blog Articles

- [Optimizing S3 costs with lifecycle policies](https://aws.amazon.com/blogs/storage/optimizing-amazon-s3-with-storage-class-analysis/)
- [How to use presigned URLs for accessing S3](https://aws.amazon.com/blogs/developer/generating-amazon-s3-presigned-urls-with-sse-kms/)
- [S3 Cross-Region Replication use cases](https://aws.amazon.com/blogs/storage/use-amazon-s3-replication-to-help-improve-data-resiliency/)

## Study Tools

- [Tutorials Dojo — Amazon S3 Cheat Sheet](https://tutorialsdojo.com/amazon-s3/)
- [AWS S3 Storage Classes Calculator](https://aws.amazon.com/s3/storage-classes/)

## S3 Storage Classes Comparison

| Class | Access | Availability | Durability | Min. Duration | Cost |
|--------|--------|-----------------|-------------|--------------|-------|
| S3 Standard | Frequent | 99.99% | 11 9s | None | High |
| S3 Standard-IA | Infrequent | 99.9% | 11 9s | 30 days | Medium |
| S3 One Zone-IA | Infrequent | 99.5% | 11 9s (1 AZ) | 30 days | Low |
| S3 Glacier IR | Archive | 99.9% | 11 9s | 90 days | Very low |
| S3 Glacier Flexible | Archive | 99.99% | 11 9s | 90 days | Extremely low |
| S3 Glacier Deep | Cold archive | 99.99% | 11 9s | 180 days | Minimal |
| S3 Intelligent | Variable | 99.9% | 11 9s | None | Variable |

# Links and Resources — SQS, SNS and Messaging (Module 10)

## Official AWS Documentation

- [Amazon SQS — Official Documentation](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/welcome.html)
- [SQS — Standard vs FIFO Queues](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/standard-queues.html)
- [SQS — Dead-Letter Queues (DLQ)](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-dead-letter-queues.html)
- [SQS — Visibility Timeout](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-visibility-timeout.html)
- [SQS — Long Polling](https://docs.aws.amazon.com/AWSSimpleQueueService/latest/SQSDeveloperGuide/sqs-short-and-long-polling.html)
- [Amazon SNS — Official Documentation](https://docs.aws.amazon.com/sns/latest/dg/welcome.html)
- [SNS — Filter Policies](https://docs.aws.amazon.com/sns/latest/dg/sns-message-filtering.html)
- [SNS — Fan-out Pattern](https://docs.aws.amazon.com/sns/latest/dg/sns-common-scenarios.html)
- [Amazon EventBridge — Documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
- [Amazon MQ — Documentation](https://docs.aws.amazon.com/amazon-mq/latest/developer-guide/welcome.html)

## FAQs

- [Amazon SQS FAQ](https://aws.amazon.com/sqs/faqs/)
- [Amazon SNS FAQ](https://aws.amazon.com/sns/faqs/)

## Whitepapers

- [Messaging Patterns on AWS](https://docs.aws.amazon.com/whitepapers/latest/develop-deploy-low-latency-applications/messaging.html)

## AWS Blog Articles

- [Standard vs FIFO: choosing the right queue](https://aws.amazon.com/blogs/compute/building-a-messaging-platform-using-sqs-and-sns/)
- [SQS DLQ best practices](https://aws.amazon.com/blogs/compute/handling-failures-with-sqs-dead-letter-queues/)
- [SNS to SQS fan-out pattern](https://aws.amazon.com/blogs/compute/exploring-the-amazon-sns-message-filtering-feature/)

## Study Tools

- [Tutorials Dojo — Amazon SQS Cheat Sheet](https://tutorialsdojo.com/amazon-sqs/)
- [Tutorials Dojo — Amazon SNS Cheat Sheet](https://tutorialsdojo.com/amazon-sns/)

## Messaging Services Comparison

| Criterion | SQS Standard | SQS FIFO | SNS | EventBridge |
|---------|-------------|----------|-----|-------------|
| Ordering | Not guaranteed | Guaranteed | N/A | N/A |
| Throughput | Unlimited | 300 msg/s (3000 w/batching) | Unlimited | 10k events/s |
| Deduplication | No | Yes (ID) | No | No |
| Delivery | At-least-once | Exactly-once | Push (fan-out) | Push (targets) |
| Consumers | Pull | Pull | Push (subscriptions) | Push (rules) |
| Typical use | Decoupling | Payments, orders | Notifications, fan-out | AWS service events |
| Message retention | 1 min–14 days | 1 min–14 days | N/A | N/A |

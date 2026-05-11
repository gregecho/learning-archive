# Links and Resources — DynamoDB (Module 07)

## Official AWS Documentation

- [Amazon DynamoDB — Official Documentation](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Introduction.html)
- [DynamoDB — Global Secondary Indexes (GSI)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/GSI.html)
- [DynamoDB — Local Secondary Indexes (LSI)](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/LSI.html)
- [DynamoDB Streams](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Streams.html)
- [DynamoDB TTL — Time to Live](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/TTL.html)
- [DynamoDB Auto Scaling](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/AutoScaling.html)
- [DynamoDB On-Demand vs Provisioned](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/HowItWorks.ReadWriteCapacityMode.html)
- [DAX — DynamoDB Accelerator](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/DAX.html)
- [DynamoDB Transactions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/transaction-apis.html)
- [DynamoDB Condition Expressions](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/Expressions.ConditionExpressions.html)

## FAQs

- [Amazon DynamoDB FAQ](https://aws.amazon.com/dynamodb/faqs/)

## Whitepapers

- [Best Practices for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/BestPractices.html)
- [DynamoDB — NoSQL Design Patterns](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/bp-general-nosql-design.html)

## AWS Blog Articles

- [NoSQL Design Patterns for DynamoDB](https://aws.amazon.com/blogs/database/nosql-design-patterns-for-dynamodb/)
- [GSI Overloading - advanced indexing](https://aws.amazon.com/blogs/database/using-global-secondary-indexes-for-dynamic-queries/)
- [Single-table design with DynamoDB](https://aws.amazon.com/blogs/compute/creating-a-single-table-design-with-amazon-dynamodb/)

## Study Tools

- [Tutorials Dojo — Amazon DynamoDB Cheat Sheet](https://tutorialsdojo.com/amazon-dynamodb/)
- [NoSQL Workbench for DynamoDB](https://docs.aws.amazon.com/amazondynamodb/latest/developerguide/workbench.html)

## DynamoDB Comparison Table

| Criterion | On-Demand | Provisioned |
|---------|-----------|-------------|
| Capacity planning | No | Yes (RCU/WCU) |
| Scaling | Automatic | Manual or Auto Scaling |
| Cost per req | Higher | Lower (predictable usage) |
| Ideal for | Unpredictable traffic | Stable traffic |
| Free tier | No | Yes (25 WCU/RCU) |

| Read Mode | Definition |
|----------------|-----------|
| Eventually Consistent | Default — 1/2 the RCU cost |
| Strongly Consistent | Most recent data — 1 RCU per 4KB |
| Transactional Read | 2x RCU — guarantees atomicity |

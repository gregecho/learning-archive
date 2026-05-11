# Links and Resources — Monitoring: CloudWatch and CloudTrail (Module 14)

## Official AWS Documentation

- [Amazon CloudWatch — Official Documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/WhatIsCloudWatch.html)
- [CloudWatch Logs — Documentation](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/WhatIsCloudWatchLogs.html)
- [CloudWatch Logs Insights — Query Syntax](https://docs.aws.amazon.com/AmazonCloudWatch/latest/logs/CWL_QuerySyntax.html)
- [CloudWatch Alarms — Configuration](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/AlarmThatSendsEmail.html)
- [CloudWatch Metrics — Available Namespaces and Metrics](https://docs.aws.amazon.com/AmazonCloudWatch/latest/monitoring/aws-services-cloudwatch-metrics.html)
- [AWS CloudTrail — Documentation](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-user-guide.html)
- [CloudTrail — What is Logged](https://docs.aws.amazon.com/awscloudtrail/latest/userguide/cloudtrail-concepts.html)
- [AWS Config — Documentation](https://docs.aws.amazon.com/config/latest/developerguide/WhatIsConfig.html)
- [AWS Config — Managed Rules](https://docs.aws.amazon.com/config/latest/developerguide/managed-rules-by-aws-config.html)
- [Amazon EventBridge — Documentation](https://docs.aws.amazon.com/eventbridge/latest/userguide/eb-what-is.html)
- [AWS X-Ray — Documentation](https://docs.aws.amazon.com/xray/latest/devguide/aws-xray.html)

## FAQs

- [Amazon CloudWatch FAQ](https://aws.amazon.com/cloudwatch/faqs/)
- [AWS CloudTrail FAQ](https://aws.amazon.com/cloudtrail/faqs/)
- [AWS Config FAQ](https://aws.amazon.com/config/faqs/)

## Whitepapers

- [AWS Security Logging and Monitoring Whitepaper](https://docs.aws.amazon.com/whitepapers/latest/aws-security-incident-response-guide/detection.html)
- [Security Pillar — Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/security-pillar/welcome.html)
- [AWS Compliance Framework and GDPR — Logging requirements](https://aws.amazon.com/compliance/gdpr-center/)

## AWS Blog Articles

- [Operational visibility with Amazon CloudWatch](https://aws.amazon.com/blogs/mt/operational-visibility-with-amazon-cloudwatch/)
- [Using CloudWatch Logs Insights for advanced log analysis](https://aws.amazon.com/blogs/mt/using-amazon-cloudwatch-logs-insights-for-advanced-log-analysis/)
- [Automate security response with AWS Config and Lambda](https://aws.amazon.com/blogs/security/how-to-auto-remediate-internet-accessible-ports-with-aws-config-and-aws-security-hub/)
- [Best practices for AWS CloudTrail](https://aws.amazon.com/blogs/mt/aws-cloudtrail-best-practices/)

## re:Invent Videos

- [Centralized observability with CloudWatch (COP323)](https://www.youtube.com/results?search_query=aws+reinvent+cloudwatch+centralized+observability)
- [Threat detection with GuardDuty and CloudTrail](https://www.youtube.com/results?search_query=aws+reinvent+guardduty+cloudtrail+threat+detection)
- [AWS X-Ray distributed tracing in practice](https://www.youtube.com/results?search_query=aws+reinvent+x-ray+distributed+tracing)

## Study Tools

- [Tutorials Dojo — CloudWatch Cheat Sheet](https://tutorialsdojo.com/amazon-cloudwatch/)
- [Tutorials Dojo — CloudTrail Cheat Sheet](https://tutorialsdojo.com/aws-cloudtrail/)
- [Tutorials Dojo — AWS Config Cheat Sheet](https://tutorialsdojo.com/aws-config/)
- [AWS Skill Builder — Monitoring, Logging, and Remediation](https://explore.skillbuilder.aws/learn/course/external/view/elearning/1499/aws-cloud-operations)

## Monitoring Services Comparison

| Service | What it monitors | Default retention |
|---------|---------------|-----------------|
| CloudWatch Metrics | AWS resource metrics | 15 months |
| CloudWatch Logs | Application/service logs | Configurable (default: never expire) |
| CloudTrail | API calls (who did what) | 90 days (free management events) |
| Config | Resource configuration state | 7 years (configurable) |
| GuardDuty | Security threats (VPC Flow, DNS, CloudTrail) | 90 days |
| X-Ray | Distributed request tracing | 30 days |

---

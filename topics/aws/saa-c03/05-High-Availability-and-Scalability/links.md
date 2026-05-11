# Reference Links — High Availability and Scalability

## Official AWS Documentation

### Elastic Load Balancing
- [ELB User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/userguide/) — Overview and type comparison
- [ALB User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/) — Application Load Balancer
- [NLB User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/) — Network Load Balancer
- [GWLB User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/) — Gateway Load Balancer
- [CLB User Guide](https://docs.aws.amazon.com/elasticloadbalancing/latest/classic/) — Classic (legacy)

### ALB — Routing and Features
- [ALB Listener Rules](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/listener-update-rules.html) — Conditions and actions
- [Weighted Target Groups (ALB)](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-target-groups.html) — Canary/Blue-Green
- [ALB Sticky Sessions](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/sticky-sessions.html) — Duration and Application-based
- [ALB Lambda Targets](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/lambda-functions.html) — Using Lambda as a target

### NLB
- [NLB Static IP Addresses](https://docs.aws.amazon.com/elasticloadbalancing/latest/network/network-load-balancers.html) — Static IP and Elastic IP
- [NLB with PrivateLink](https://docs.aws.amazon.com/vpc/latest/privatelink/create-endpoint-service.html) — VPC Endpoint Service

### GWLB
- [GWLB and Appliances](https://docs.aws.amazon.com/elasticloadbalancing/latest/gateway/introduction.html) — GENEVE and appliances
- [VPC Ingress Routing with GWLB](https://docs.aws.amazon.com/vpc/latest/userguide/VPC_Route_Tables.html#ingress-routing) — Ingress routing with GWLB

### Auto Scaling
- [EC2 Auto Scaling User Guide](https://docs.aws.amazon.com/autoscaling/ec2/userguide/) — Complete guide
- [Launch Templates](https://docs.aws.amazon.com/AWSEC2/latest/UserGuide/ec2-launch-templates.html) — Replacement for Launch Configurations
- [Scaling Policies](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-scale-based-on-demand.html) — Target Tracking, Step, Simple
- [Predictive Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-predictive-scaling.html) — ML-based scaling
- [Scheduled Scaling](https://docs.aws.amazon.com/autoscaling/ec2/userguide/schedule_time.html)
- [Lifecycle Hooks](https://docs.aws.amazon.com/autoscaling/ec2/userguide/lifecycle-hooks.html) — Pending:Wait and Terminating:Wait
- [Termination Policies](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-termination-policies.html)
- [Mixed Instance Policy](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-mixed-instances-groups.html) — Spot + On-Demand mix
- [Health Check Types](https://docs.aws.amazon.com/autoscaling/ec2/userguide/ec2-auto-scaling-health-checks.html) — EC2 vs ELB vs Custom

---

## Whitepapers

- [Reliability Pillar — Well-Architected Framework](https://docs.aws.amazon.com/wellarchitected/latest/reliability-pillar/) — Reliability pillar
- [Performance Efficiency Pillar](https://docs.aws.amazon.com/wellarchitected/latest/performance-efficiency-pillar/) — Scaling and elasticity
- [AWS Architecture Center — High Availability](https://aws.amazon.com/architecture/high-availability/) — HA patterns

---

## AWS Technical Blog Posts

- [Building a Scalable and Highly Available Application](https://aws.amazon.com/blogs/architecture/) — AWS Architecture Blog
- [Introducing GWLB](https://aws.amazon.com/blogs/networking-and-content-delivery/introducing-aws-gateway-load-balancer/) — Gateway Load Balancer launch blog
- [Blue/Green Deployments with ALB Weighted Target Groups](https://aws.amazon.com/blogs/devops/use-aws-codedeploy-to-implement-blue-green-deployments-for-aws-lambda-functions/) — Zero-downtime deployment

---

## FAQs for the Exam

- [Elastic Load Balancing FAQ](https://aws.amazon.com/elasticloadbalancing/faqs/)
- [EC2 Auto Scaling FAQ](https://aws.amazon.com/ec2/autoscaling/faqs/)

---

## Useful Tools

- [ELB Access Logs](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html) — For routing debug
- [ASG Activity History](https://docs.aws.amazon.com/autoscaling/ec2/userguide/as-verify-scaling-activity.html) — View scaling history

---

## Key SAA-C03 Concepts in This Module

| Concept | Exam Frequency |
|---|---|
| ALB vs NLB: when to use each (static IP → NLB) | High |
| GWLB for security appliance insertion | High |
| ALB weighted target groups for canary/blue-green | High |
| ELB health check on ASG (not just EC2 health) | High |
| Target Tracking creates alarms automatically | High |
| Lifecycle Hooks for custom initialization/draining | High |
| Cross-zone LB: default/cost by ELB type | Medium |
| Launch Template > Launch Configuration | Medium |
| PrivateLink requires NLB as backend | High |
| Predictive Scaling requires 14 days of history | Medium |

---

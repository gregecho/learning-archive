# Flashcards — High Availability and Scalability

> Review one card at a time. Try to answer before revealing the response.

---

**Q:** What is the fundamental difference between ALB and NLB?  
**A:** ALB operates at layer 7 (HTTP/HTTPS/HTTP2/gRPC), routing by content (path, host, header, query string). NLB operates at layer 4 (TCP/UDP/TLS), ultra-low latency, static IP per AZ, preserves client source IP by default.

---

**Q:** What is GWLB (Gateway Load Balancer) and when to use it?  
**A:** Layer 3, GENEVE protocol, designed for transparent insertion of security appliances (next-gen firewalls, IDS/IPS, deep packet inspection). Encapsulates traffic and sends it to appliances (EC2 with NVA) in the target group. Use with VPC Routing and GWLB Endpoints.

---

**Q:** What is cross-zone load balancing and what is the default for each ELB type?  
**A:** Distributes traffic equally among all registered instances, regardless of AZ. ALB: enabled by default, no extra charge. NLB/GWLB: disabled by default, enabling charges for inter-AZ traffic. CLB: enabled by default via console, no charge.

---

**Q:** What is Connection Draining (Deregistration Delay)?  
**A:** Period (default 300s, 0–3600s) during which the ELB waits for in-progress connections to complete before deregistering/stopping an instance. During this period, the ALB stops sending new requests to the instance but maintains existing ones. Reduce for applications with short requests; increase for long uploads.

---

**Q:** What types of targets does ALB support?  
**A:** EC2 instances (by instance ID), IP addresses (on-premises resources, other services with IP), Lambda functions (for serverless backends), and other ALBs (for chained microservice architectures).

---

**Q:** Does ALB preserve the client's source IP?  
**A:** ALB does NOT preserve the source IP directly — it terminates the TCP connection and makes a new request to the target. The original client IP is in the `X-Forwarded-For` header. NLB DOES preserve the source IP (layer 4 pass-through).

---

**Q:** What is Launch Template vs Launch Configuration?  
**A:** Launch Configuration: legacy, immutable (cannot edit, only create new), does not support multiple instance types, does not support spot with on-demand mix. Launch Template: recommended, has versions ($Latest, $Default), supports mixed instances policy, spot fleet, placement groups, T2/T3 unlimited.

---

**Q:** What are the 4 Auto Scaling policies?  
**A:** 1) Target Tracking: keeps a metric at a target value (e.g., CPU 50%), creates alarms automatically. 2) Step Scaling: scales in steps based on metric ranges, requires CloudWatch alarm. 3) Scheduled Scaling: based on date/time, for predictable patterns. 4) Predictive Scaling: uses ML to forecast load and pre-provisions.

---

**Q:** What is the cooldown period in Auto Scaling?  
**A:** Period (default 300s) after a scaling activity during which the ASG does not initiate another scaling action. Purpose: let the new instance start absorbing load before deciding to scale further. Target Tracking has a separate warmup period that replaces cooldown for scale-out.

---

**Q:** What is a Lifecycle Hook in ASG?  
**A:** Allows pausing the ASG during instance lifecycle transitions: `Pending:Wait` (before entering service) and `Terminating:Wait` (before being terminated). The hook can trigger Lambda, SNS, SQS, or EventBridge. Default timeout: 3600s. To continue: `CompleteLifecycleAction(CONTINUE)` or `ABANDON`.

---

**Q:** What is the default ASG termination policy?  
**A:** 1) Selects AZ with most instances (rebalance); 2) Instance with oldest Launch Configuration/Template; 3) Instance closest to next billing hour; 4) Random if tie. Also available policies: `OldestInstance`, `NewestInstance`, `ClosestToNextInstanceHour`, `AllocationStrategy`.

---

**Q:** What is Predictive Scaling and what is the requirement?  
**A:** Uses ML to analyze metric history and pre-provision capacity before the expected peak. Requires at least 14 days of metric history to generate forecasts. Can be used combined with Target Tracking for proactive and reactive coverage.

---

**Q:** What is PrivateLink and how does NLB relate to it?  
**A:** AWS PrivateLink allows exposing a service from one VPC to consumers in other VPCs/accounts without peering, via Interface Endpoints. NLB is the prerequisite: the service must be behind an NLB to be registered as a VPC Endpoint Service. Consumers create Interface VPC Endpoints pointing to the service.

---

**Q:** How does ALB health check work vs ASG health check?  
**A:** ALB checks instance health in the target group (HTTP path, response code, interval). ASG can use two types: EC2 (system status) or ELB (delegated to ELB). In production, ALWAYS configure the ASG to use ELB health check, as it detects application failures that EC2 health check does not.

---

**Q:** What is the warm-up period in ASG Target Tracking?  
**A:** Period (in seconds) during which a new instance is not considered in scaling metrics, giving it time to initialize. Prevents the ASG from interpreting a "warming" instance as low performance and scaling further unnecessarily.

---

**Q:** How to implement blue/green deployment with ALB and ASG?  
**A:** Create two target groups: `tg-blue` (current version) and `tg-green` (new version). Configure a listener rule with weighted target groups (e.g., 95% blue, 5% green). Gradually increase green weight. If successful, redirect 100% to green. If failure, return to 100% blue immediately.

---

**Q:** What are Sticky Sessions on ALB?  
**A:** Ensures requests from the same client go to the same instance for a period. Uses cookies: `AWSALB` (generated by ALB, duration 1s–7 days) or application-defined cookie. Useful for stateful sessions. Can cause imbalance if one instance receives many long sessions.

---

**Q:** What is NLB Zonal DNS and static IP?  
**A:** Every NLB receives a DNS hostname (e.g., `my-nlb-xxxx.elb.amazonaws.com`). Each enabled AZ has an NLB node with a static IP that can be assigned as an Elastic IP. For client IP whitelisting, use the NLB's Elastic IP. DNS resolves to all nodes; for fixed IP per AZ, use the IP directly.

---

**Q:** What is the difference between Step Scaling and Simple Scaling?  
**A:** Simple Scaling (legacy): triggers one action and waits for cooldown before any other action. All or nothing. Step Scaling: allows multiple steps based on metric ranges without cooldown between different steps — reacts faster to gradual or sudden load changes.

---

**Q:** How does the Mixed Instance Policy work in ASG with Spot?  
**A:** Defines a pool of instance types and the On-Demand vs Spot percentage. The ASG attempts to launch Spot from the cheapest available type. If interrupted, it tries another type from the pool. The `capacityOptimized` strategy minimizes interruptions by choosing pools with more available capacity.

---

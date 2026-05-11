# Questions — High Availability and Scalability

## Question 1
**Domain:** Design Resilient Architectures  
**Difficulty:** Medium

A company has a REST API using EC2 with Auto Scaling. Corporate clients need to add the API IPs to their firewall whitelist. Which type of load balancer solves this with a fixed IP?

- A) ALB with static IP
- B) NLB with Elastic IP per AZ
- C) CLB with static IP
- D) ALB with wildcard SSL

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

NLB allows associating an Elastic IP per Availability Zone, providing static and predictable IP addresses. ALB uses DNS and the IP can change. CLB is legacy and does not have a reliable static IP. Wildcard SSL does not solve the IP problem.

**Key concept:** NLB with Elastic IP for client IP allowlisting
</details>

## Question 2
**Domain:** Design Resilient Architectures  
**Difficulty:** Medium

A multi-tenant SaaS platform routes traffic to different target groups based on the request hostname: `tenant-a.app.com` goes to TG-A and `tenant-b.app.com` goes to TG-B. Which ALB feature implements this?

- A) Path-based routing
- B) Host-based routing
- C) IP-based routing
- D) Weighted target groups

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

Host-based routing uses the HTTP Host header to select the target group according to the request hostname. Path-based uses the URL path (/api, /admin). IP-based routing does not exist as an ALB listener rule. Weighted target groups split traffic proportionally between groups, not by hostname.

**Key concept:** host-based routing on ALB for multi-tenant by hostname
</details>

## Question 3
**Domain:** Design High-Performing Architectures  
**Difficulty:** Medium

A team wants to use ALB for a canary release, sending 5% of traffic to the new version and 95% to the current version. Which ALB feature enables this?

- A) Host-based routing with two listeners
- B) Weighted target groups in the same listener rule
- C) NLB with cross-zone balancing
- D) Auto Scaling Group with weighted Launch Template

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

ALB supports weighted target groups in a listener rule, distributing traffic proportionally between two or more target groups in the same action. This is the standard mechanism for gradual canary and blue/green deployments. Host-based routing routes by hostname, not by weight. NLB does not have this feature. ASG does not control traffic proportion at the load balancer level.

**Key concept:** weighted target groups on ALB for canary release
</details>

## Question 4
**Domain:** Design Secure Applications and Architectures  
**Difficulty:** Hard

A company wants to inspect all inbound internet traffic before it reaches the application, using a third-party next-gen firewall running on EC2. Which type of load balancer supports this transparent appliance insertion model?

- A) ALB with Lambda authorizer
- B) NLB with TLS pass-through
- C) GWLB with VPC routing to appliances in the target group
- D) CLB with proxy protocol

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

GWLB operates at layer 3 with the GENEVE protocol, enabling transparent insertion of security appliances in the traffic path. Packets are sent to the GWLB endpoint, processed by appliances in the target group, and returned to the GWLB, which redirects them to the destination. ALB, NLB, and CLB do not support this IP packet encapsulation model.

**Key concept:** GWLB for transparent security appliance insertion
</details>

## Question 5
**Domain:** Design Resilient Architectures  
**Difficulty:** Medium

An ASG is configured with EC2-type health check only. One instance is running but the application process has crashed and returns HTTP 500 for every request. Will the ASG replace it automatically?

- A) Yes, EC2 health check detects any application failure
- B) No, EC2 health check validates only instance status, not the application
- C) Yes, ALB notifies ASG automatically without additional configuration
- D) No, the instance must be restarted manually

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

The EC2 health check only detects hardware/OS status failures (instance status check and system status check). A crashed application returning HTTP 500 is still in the "running" state for EC2. For the ASG to replace instances with application failure, you must enable ELB health check on the ASG, which evaluates health at the ALB target group level.

**Key concept:** ELB health check on ASG to detect application failures
</details>

## Question 6
**Domain:** Design High-Performing Architectures  
**Difficulty:** Medium

An application receives predictable peaks every Monday at 8am when employees arrive at work. The team wants to ensure instances are already available before the peak, avoiding scale-out latency. Which scaling policy is most appropriate?

- A) Target Tracking with CPUUtilization
- B) Scheduled Scaling increasing capacity at 7:45am every Monday
- C) Step Scaling with alarm on CPU > 70%
- D) Manual scaling every Monday morning

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

Scheduled Scaling anticipates the capacity increase before the expected peak, avoiding the inherent lag of reactive policies. Target Tracking and Step Scaling are reactive: they wait for the metric to rise before acting — arriving late for abrupt peaks. Manual scaling depends on human intervention. For predictable peaks, Scheduled (or Predictive with history) is the answer.

**Key concept:** Scheduled Scaling to provision before predictable peaks
</details>

## Question 7
**Domain:** Design Resilient Architectures  
**Difficulty:** Medium

A company wants to ensure that when adding new EC2 instances via ASG, the monitoring agent is installed and configured before the instance begins receiving traffic from the load balancer. Which mechanism should be used?

- A) User Data with installation script
- B) Lifecycle Hook on EC2_INSTANCE_LAUNCHING with Lambda that installs the agent
- C) Golden AMI with pre-installed agent
- D) AWS Config rule to verify the agent

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

Lifecycle Hook on `Pending:Wait` keeps the instance out of the ELB target group while automation runs. A Lambda (triggered via SNS/SQS/EventBridge) installs and configures the agent and then calls `CompleteLifecycleAction(CONTINUE)`. User Data runs on boot but does not guarantee the instance only enters the load balancer afterward — the hook does. Golden AMI is good for a pre-installed agent but not for dynamic configurations.

**Key concept:** Lifecycle Hook Pending:Wait for custom initialization before ELB
</details>

## Question 8
**Domain:** Design Cost-Optimized Architectures  
**Difficulty:** Medium

An ALB has two target groups in two AZs: TG-A with 10 instances in AZ1 and TG-B with 2 instances in AZ2. With cross-zone load balancing enabled on the ALB, how is traffic distributed?

- A) 50% to AZ1 and 50% to AZ2
- B) Evenly across all 12 instances (~8.3% each)
- C) 83% to TG-A and 17% to TG-B
- D) 100% to TG-A because it has more instances

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

With cross-zone load balancing enabled, each ALB node distributes traffic equally among all healthy instances in all AZs, regardless of how many are per AZ. 12 instances = ~8.3% each. Without cross-zone, each node distributes only to instances in its AZ (50% to each AZ, so AZ1 with 10 instances each gets 5% and AZ2 with 2 instances each gets 25%).

**Key concept:** cross-zone load balancing distributes evenly across all instances
</details>

## Question 9
**Domain:** Design Resilient Architectures  
**Difficulty:** Hard

An ASG is executing scale-in. The termination policy is set to default. AZ1 has 4 instances and AZ2 has 2. Which instance is selected for termination first?

- A) The newest instance in any AZ
- B) An instance from AZ2, because it has fewer and is imbalanced
- C) An instance from AZ1, because it is the AZ with more instances, followed by the oldest by launch template
- D) Random among all instances

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

The default ASG termination policy: (1) selects the AZ with more instances to rebalance; (2) within that AZ, selects the instance with the oldest launch template or configuration; (3) if tied, the closest to the next chargeable hour. AZ1 with 4 instances is selected first. The oldest by template would be terminated.

**Key concept:** default termination policy: AZ with more instances → oldest by template
</details>

## Question 10
**Domain:** Design High-Performing Architectures  
**Difficulty:** Medium

A service needs access to an internal API running in another account's VPC, without exposing traffic to the internet and without creating VPC Peering. Which architecture meets this requirement?

- A) Internet Gateway with restricted security group
- B) NLB with VPC Endpoint Service (PrivateLink) in the producer account
- C) Multi-region ALB with CloudFront
- D) Site-to-site VPN between accounts

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

AWS PrivateLink uses an NLB as the backend of a VPC Endpoint Service. The consumer creates an Interface Endpoint (VPC Endpoint) that appears as an ENI in their VPC with a private IP. Traffic never leaves the AWS network and does not require peering, routing, or internet exposure. VPN is more complex and does not elegantly solve the issue.

**Key concept:** NLB + PrivateLink for private cross-account service exposure without peering
</details>

## Question 11
**Domain:** Design Resilient Architectures  
**Difficulty:** Medium

An ASG EC2 instance is processing a long task when scale-in is triggered. Which mechanism ensures the task completes before the instance is terminated?

- A) Cooldown period of 3600 seconds
- B) Connection Draining on ELB
- C) Lifecycle Hook on EC2_INSTANCE_TERMINATING
- D) Suspended scaling for scale-in

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

Lifecycle Hook on `Terminating:Wait` keeps the instance in a waiting state before effective termination. Automation can monitor task completion and call `CompleteLifecycleAction(CONTINUE)` when finished. Connection Draining only drains active HTTP connections from the ELB, it does not wait for background tasks. Cooldown affects when the next scaling occurs, not the timing of one already started. Suspend would stop scaling entirely.

**Key concept:** Lifecycle Hook Terminating:Wait for long-running tasks on scale-in
</details>

## Question 12
**Domain:** Design High-Performing Architectures  
**Difficulty:** Medium

An architect needs to create a fleet of EC2 instances using multiple types (m5.large, m5.xlarge, m6i.large) with an On-Demand and Spot mix to reduce cost. Which feature enables this?

- A) Launch Configuration with multiple types
- B) Launch Template with type overrides + Mixed Instance Policy in ASG
- C) Multiple ASGs separated by type
- D) Dedicated Host with type multiplexing

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

Launch Template supports instance type overrides. In ASG, the Mixed Instance Policy allows defining multiple types and the On-Demand/Spot distribution. The ASG chooses the cheapest available from the pool of defined types. Launch Configuration does not support multiple types. Multiple ASGs increase operational complexity. Dedicated Host is unrelated to Spot type diversification.

**Key concept:** Launch Template with Mixed Instance Policy for diversified fleet
</details>

## Question 13
**Domain:** Design Resilient Architectures  
**Difficulty:** Easy

A company wants to ensure that even if an ASG instance appears healthy to EC2, it will be replaced if the application does not return HTTP 200 on health check requests. Which configuration implements this?

- A) Create a CloudWatch alarm for response code
- B) Enable ELB health check on ASG and configure health check on the target group
- C) Use enhanced monitoring on EC2
- D) Configure CloudTrail to detect HTTP errors

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

For ASG to consider application health checks, you need to: (1) configure the health check on the ALB target group with the expected path and success code; (2) enable ELB health check on the ASG. This way, instances that fail the ALB health check are marked as unhealthy in ASG and replaced. CloudWatch alarm does not automatically act on ASG this way. Enhanced monitoring provides metrics but does not replace instances.

**Key concept:** enable ELB health check on ASG + configure TG health check
</details>

## Question 14
**Domain:** Design Cost-Optimized Architectures  
**Difficulty:** Medium

A team wants to scale ASG based on the number of visible messages in an SQS queue (ApproximateNumberOfMessagesVisible). Which scaling policy supports custom CloudWatch metrics directly?

- A) Scheduled Scaling
- B) Predictive Scaling
- C) Target Tracking Scaling with custom CloudWatch metric
- D) EC2 Auto Recovery

<details>
<summary>Answer and Explanation</summary>

**Correct answer: C**

Target Tracking supports custom CloudWatch metrics in addition to predefined metrics. You can set ApproximateNumberOfMessagesVisible/number-of-instances as a target to maintain a constant message load per instance. Scheduled is time-based. Predictive uses standard metric history. Auto Recovery is for hardware failures, not scaling.

**Key concept:** Target Tracking with custom CloudWatch metric to scale by SQS
</details>

## Question 15
**Domain:** Design Resilient Architectures  
**Difficulty:** Hard

A company has an ALB with an HTTPS listener on port 443. The SSL certificate is configured on the listener. The backend application runs HTTP on port 8080. An architect needs to ensure ALB → EC2 communication is also encrypted. Which configuration implements this?

- A) ALB cannot establish HTTPS to targets, only HTTP
- B) Configure the target group protocol as HTTPS on port 443 and install certificates on the instances
- C) Use NLB with TLS pass-through
- D) Configure SSL policy on ALB to automatically encrypt the backend

<details>
<summary>Answer and Explanation</summary>

**Correct answer: B**

ALB supports HTTPS as a target group protocol. Configure the target group with HTTPS protocol and install certificates on the instances (self-signed or ACM via Private CA). The ALB establishes HTTPS to each instance. Alternative A is wrong — ALB does support HTTPS backend. NLB with TLS pass-through is a different solution. SSL policy on the listener controls only TLS negotiation from client to ALB.

**Key concept:** target group HTTPS for end-to-end encryption on ALB
</details>

---

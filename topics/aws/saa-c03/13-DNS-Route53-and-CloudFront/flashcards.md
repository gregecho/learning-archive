# Flashcards — Module 08: DNS, Route 53 and CloudFront

---

**Q:** Why can't CNAME be used at the root domain (apex)?
**A:** RFC 1034 prohibits CNAME at the zone apex (cannot coexist with other records like SOA/NS). AWS created the **Alias record** as a proprietary extension that works at the apex and points to AWS resources at no additional query cost

---

**Q:** What is the default TTL for Route 53 records and what happens during failover?
**A:** Configurable TTL (e.g., 300s = 5 min). During failover, the TTL determines how long DNS resolvers around the world will cache the old address. Low TTL = faster failover, more queries (cost). High TTL = slower failover, fewer queries

---

**Q:** What are the 8 Route 53 routing types?
**A:** Simple, Weighted, Latency, Failover, Geolocation, Geoproximity (Traffic Flow), Multi-Value Answer, IP-based routing

---

**Q:** Which routing policy uses traffic flow with configurable bias?
**A:** **Geoproximity routing** (Traffic Flow). Routes based on geographic distance. The "bias" increases or decreases a resource's region of influence (positive bias → attracts more traffic; negative → repels). Requires Route 53 Traffic Flow

---

**Q:** What is the difference between Geolocation and Latency routing?
**A:** Geolocation: routes based on client country/continent (e.g., users from Brazil → BR server). Latency: routes based on MEASURED latency between client and AWS regions (e.g., user in Brazil → server in us-east-1 if faster than sa-east-1)

---

**Q:** What is a Calculated Health Check in Route 53?
**A:** Combines results of multiple individual Health Checks using AND, OR, or NOT. Allows creating logic such as: "consider healthy if at least 2 of 3 endpoints are UP." Useful for being more resilient to false positives

---

**Q:** How to monitor private resources (without public IP) with Route 53 Health Checks?
**A:** Route 53 Health Checkers operate from the internet. For private resources: create a CloudWatch Metric Alarm based on resource metrics → Health Check of type "CloudWatch Alarm." When Alarm → ALARM: Health Check fails

---

**Q:** What is the difference between OAI and OAC in CloudFront?
**A:** OAI (Origin Access Identity): legacy, works with standard S3. OAC (Origin Access Control): new standard, supports all S3 regions, SSE-KMS, S3 Object Lambda, more HTTP methods. For new projects: always use OAC

---

**Q:** What is Cache Policy vs Origin Request Policy in CloudFront?
**A:** Cache Policy: defines what goes into the cache key (headers, cookies, query strings) and TTL. Origin Request Policy: defines what is sent to the origin (headers, cookies, query strings) BEYOND what is in the cache key. Origin can receive more information than the cache considers

---

**Q:** How much does a CloudFront Cache Invalidation cost?
**A:** First **1,000 paths** of invalidation per month: free. Above: $0.005 per path. Wildcard `/*` counts as 1 path. Best practice: use asset versioning (file name hashing) to avoid invalidations

---

**Q:** What is CloudFront Functions vs Lambda@Edge? Which is faster?
**A:** CloudFront Functions: sub-millisecond, JavaScript, only Viewer Request/Response, cheaper. Lambda@Edge: up to 30s (Origin), Node.js/Python, 4 events including Origin. CF Functions is faster and cheaper; Lambda@Edge is more powerful

---

**Q:** What is AWS Global Accelerator used for?
**A:** Improves performance and availability for global applications using 2 static Anycast IPs. Traffic enters the nearest AWS edge and travels through the private AWS backbone network. Ideal for: fixed IPs (firewall), non-HTTP traffic (generic UDP/TCP), failover in seconds (no DNS TTL)

---

**Q:** What is the difference between Route 53 and Global Accelerator for failover?
**A:** Route 53: DNS-based failover with TTL → may take minutes to propagate. Global Accelerator: failover in seconds (no TTL, Anycast routing), but only covers AWS endpoints. For ultra-fast failover and static IPs: GA. For simplicity and flexibility: Route 53

---

**Q:** What is Route 53 Resolver Inbound vs Outbound Endpoint?
**A:** Inbound: allows on-premises to resolve DNS names of AWS resources (queries arrive from outside into the VPC). Outbound: allows resources in the VPC to resolve on-premises DNS names (forwarding rules to on-prem DNS servers via DX/VPN)

---

**Q:** Which AWS resources are valid Alias record targets in Route 53?
**A:** ALB/NLB/CLB, CloudFront, API Gateway, Elastic Beanstalk, VPC Interface Endpoints, Global Accelerator, S3 website endpoint, other zones in Route 53. Alias resolves at the DNS server — no extra query cost

---

**Q:** What is a WAF Rate-based rule?
**A:** Limits the number of requests from the same IP within a time window (5 minutes). E.g., block IP that makes more than 1,000 requests in 5 minutes. Protects against brute force and layer 7 DDoS (volumetric)

---

**Q:** What is AWS Shield Standard vs Advanced?
**A:** Standard: free, automatic for all, protects against layer 3/4 DDoS (SYN floods, UDP reflection). Advanced: paid (~$3,000/month), protection for layer 7 as well, DRT (DDoS Response Team) 24/7, cost credits for DDoS, detailed reports

---

**Q:** How to configure mandatory HTTPS in CloudFront?
**A:** In Behavior: "Viewer Protocol Policy" = "Redirect HTTP to HTTPS" or "HTTPS Only". Use ACM certificate (us-east-1 region for CloudFront). For S3 origin: OAC does not require HTTPS but it is recommended. For custom origins: configure Origin Protocol Policy

---

**Q:** What is Multi-Value Answer routing in Route 53?
**A:** Returns multiple IPs (up to 8) for the same DNS name, each with Health Check. Different from Simple (returns all without health check). Clients generally use the first functional IP. It is NOT a load balancer (does not replace ALB) — only returns multiple healthy records

---

**Q:** How does CloudFront Geo Restriction work and what is the more granular alternative?
**A:** Geo Restriction: blocks/allows countries via MaxMind GeoIP (returns 403). Entire distribution or by behavior. More granular alternative: integrate Lambda@Edge that checks the `CloudFront-Viewer-Country` header and applies custom logic (e.g., redirect to localized version, not just block)

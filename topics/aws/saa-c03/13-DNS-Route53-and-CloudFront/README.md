# Module 08 — DNS, Route 53 and CloudFront

## Amazon Route 53

AWS managed DNS service and domain registrar. The name comes from the DNS port (53) and the American Route 66.

### Hosted Zone Types
- **Public Hosted Zone**: resolves names on the public internet
- **Private Hosted Zone**: resolves names within one or more VPCs (not publicly accessible)

### Record Types
| Type | Description | AWS-specific |
|---|---|---|
| A | IPv4 address | — |
| AAAA | IPv6 address | — |
| CNAME | Points to another hostname | Cannot be created at the apex (root domain) |
| **Alias** | Points to AWS resource (ELB, CloudFront, S3, etc.) | Yes — responds as A/AAAA, free for AWS resources |
| NS | Name Servers of the hosted zone | — |
| SOA | Start of Authority | — |
| MX | Mail servers | — |
| TXT | Text (SPF, DKIM, ACM validation) | — |
| PTR | Reverse DNS | — |
| SRV, CAA | Services, certificate authority | — |

> **Alias vs CNAME**: Alias can be created at the apex (example.com), CNAME cannot. Alias does not charge for query. Alias resolves to the actual IP (no CNAME chain). **Cannot create Alias for EC2 DNS name.**

### Routing Policies

| Policy | Behavior | When to use |
|---|---|---|
| **Simple** | Returns 1 or multiple random values | Single resource, no mandatory health check |
| **Weighted** | Distributes by weight (0–255) | A/B testing, gradual migration |
| **Latency** | Routes to the region with lowest latency to the user | Multi-region, low latency |
| **Failover** | Primary → Secondary if primary fails | Active-passive DR |
| **Geolocation** | By country/continent/state (US) | Localized content, compliance |
| **Geoproximity** | By location + bias (expand/reduce region) | Traffic redistribution by coordinates |
| **Multivalue Answer** | Returns up to 8 values, with health check | Load distribution without ELB (client-side) |
| **IP-based** | By client CIDR | ISP-specific routing, network optimization |

> Geoproximity requires **Traffic Flow** and **Traffic Policy** — not configurable via the simple console.

### Health Checks
- Check HTTP/HTTPS/TCP endpoints every 10s (Fast HCs) or 30s
- Calculated by at least 18 global checkers (configurable threshold of 1–10)
- **Calculated Health Checks**: combines multiple health checks (AND/OR)
- **CloudWatch Alarm Health Check**: for private resources (without public IP) — HC checks the alarm, not the resource directly
- Can be associated with Weighted, Failover, Latency, Geolocation records

---

## Amazon CloudFront

Global CDN (Content Delivery Network) with 450+ PoPs (Edge Locations) and 13 Regional Edge Caches.

### Components
- **Distribution**: CloudFront configuration unit (domain: `xxxx.cloudfront.net`)
- **Origin**: backend (S3, ALB, EC2, API Gateway, any HTTP address)
- **Behavior (Cache Behavior)**: rule by path pattern (e.g., `/api/*` → no cache; `/*.jpg` → cache 1 day)
- **Cache Policy**: TTL (min/max/default), headers/cookies/query strings to include in cache key
- **Origin Request Policy**: what to send to the origin beyond what is in the cache key
- **Edge Location**: where files are cached

### CloudFront + S3

| Method | Description | For new content? |
|---|---|---|
| **OAC (Origin Access Control)** | Policy on S3 bucket that only accepts requests signed by CloudFront | Recommended |
| **OAI (Origin Access Identity)** | Virtual IAM identity for CF to access private S3 | Legacy (still works) |

With OAC, the S3 bucket must have:
```json
{
  "Principal": {"Service": "cloudfront.amazonaws.com"},
  "Condition": {"StringEquals": {"AWS:SourceArn": "arn:aws:cloudfront::ACCOUNT:distribution/DIST_ID"}}
}
```

### CloudFront Cache Invalidation
- Removes objects from cache before TTL expires: `/*` (all) or specific path
- Charged per invalidation path after the first 1,000/month
- Alternative: use file versioning (e.g., `app.v2.js`) — no invalidation cost

### Geo Restriction
- **Allowlist**: only listed countries can access
- **Blocklist**: listed countries are blocked
- Based on GeoIP database (not infallible — VPNs can bypass)

### Lambda@Edge vs CloudFront Functions

| Feature | Lambda@Edge | CloudFront Functions |
|---|---|---|
| Runtime | Node.js, Python | JavaScript (ECMAScript 5.1) |
| Latency | Moderate (~1–10ms) | Very low (<1ms) |
| Memory | Up to 10 GB (L@E viewer), 128MB request | Max 2 MB memory |
| Requests/s | No rate limit | 10 million+ req/s |
| Duration | Up to 30s (origin), 5s (viewer) | Maximum 1ms |
| Network access | Yes (can call external APIs) | No |
| Events | Viewer Request/Response, Origin Request/Response | Viewer Request/Response only |
| Typical use | Complex URL rewrite, cookie-based A/B, authentication | Header manipulation, simple URL rewrite, redirect |

---

## AWS Global Accelerator

Uses the AWS global network to route user traffic to the nearest endpoint with the lowest latency:

- Provides **2 Static Anycast IPs** globally (do not change — excellent for whitelisting)
- Routes to the nearest healthy endpoint via the AWS backbone network
- Supports endpoints: ALB, NLB, EC2, Elastic IP addresses
- **Health checks** detect failover and reroute automatically
- **Difference from CloudFront**: CloudFront delivers cached content (CDN); Global Accelerator is a TCP/UDP proxy, better for non-HTTP applications (gaming, IoT, VoIP)

### Route 53 vs Global Accelerator

| Aspect | Route 53 | Global Accelerator |
|---|---|---|
| Static IP | No (DNS) | Yes (2 Anycast IPs) |
| Failover | DNS propagation (~60s) | Nearly instant |
| Generic TCP/UDP | No (DNS only) | Yes |
| Cached content | No | No |
| Cost | Per query | Hourly fee + per GB |

---

## AWS WAF (Web Application Firewall)

Protects web applications against OWASP exploits:

- Deploy: **CloudFront, ALB, API Gateway, AppSync, Cognito User Pool**
- **Web ACL**: contains rules and rule groups
- Rules inspect: IP, headers, body (up to 8 KB), URI string, query string, HTTP method
- **Managed Rule Groups**: preconfigured sets (OWASP Top 10, bots, AWS Managed Intelligence)
- **Rate-based Rules**: limit per IP (e.g., max 100 req/5min)
- Action: Allow, Block, Count (monitoring without blocking), CAPTCHA, Challenge

---

## Exam Tips

- **Alias record** = free + can be at apex; CNAME = charges per query + cannot be at apex
- **Geoproximity** needs Traffic Policy (Traffic Flow); Geolocation does not
- **Failover**: primary health check fails → routes to secondary (passive DR)
- CloudFront + S3: OAC is the new standard (replaced OAI)
- **Lambda@Edge** = complex processing with external calls; **CF Functions** = transformations in < 1ms
- **Global Accelerator** = static IPs + AWS backbone network; good for gaming, IoT, VoIP, and TCP/UDP apps
- **Route 53 Multivalue** != ELB: only distributes, does not actually load balance; client chooses arbitrarily
- Resolve DNS from Private Hosted Zone of another VPC: enable **VPC Association** or use **Route 53 Resolver** (Inbound/Outbound Endpoints) for on-prem
- CloudFront can have multiple origins in the same distribution (path-based routing between origins)
- WAF can go on ALB **or** on CloudFront — for protection closer to the edge, use CloudFront + WAF

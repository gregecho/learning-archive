# Cheatsheet — Module 08: DNS, Route 53 and CloudFront

## Route 53 — Record Types

| Record | Usage | Apex? | Query Cost |
|---|---|---|---|
| A | IPv4 address | Yes | Standard |
| AAAA | IPv6 address | Yes | Standard |
| CNAME | Alias to another hostname | **NO** | Standard |
| **Alias** | AWS resources (ALB, CF, S3) | **YES** | Free |
| MX | Email servers | Yes | Standard |
| TXT | Verification, SPF, DKIM | Yes | Standard |
| NS | Zone nameservers | Yes | Standard |

## Route 53 Routing Policies

| Policy | Use Case | Health Check? |
|---|---|---|
| Simple | Single resource, no HA | No |
| Weighted | A/B testing, gradual migration | Optional |
| Latency | Lowest latency for user | Optional |
| Failover | Active-Passive DR | **Required** for primary |
| Geolocation | Content by country/region | Optional |
| Geoproximity | By geographic distance with bias | Optional |
| Multi-Value | Multiple healthy IPs (pseudo LB) | Recommended |
| IP-based | Routing by source CIDR | No |

## CloudFront — Components and Configuration

| Component | Description |
|---|---|
| Distribution | Entry point — defines origins, behaviors, certificate |
| Origin | Content source: S3, ALB, EC2, API GW, custom HTTP |
| Behavior | Cache rule associated with a path pattern (e.g., `/api/*`) |
| Cache Policy | Defines cache key (query strings, headers, cookies) and TTLs |
| Origin Request Policy | What to send to origin beyond the cache key |
| OAC | Replaces OAI — authenticates CF with S3 origin via SigV4 |

## CloudFront TTLs
- `Cache-Control: max-age=<seconds>` in origin response → defines edge TTL
- Default TTL: **86,400s** (24h) if origin doesn't define one
- Minimum TTL and Maximum TTL in behavior override the origin header if lower/higher
- Invalidation: forces immediate cache miss (1,000 paths/month = free)

## Lambda@Edge vs CloudFront Functions

| | CloudFront Functions | Lambda@Edge |
|---|---|---|
| Runtime | JavaScript (ES5.1) | Node.js, Python |
| Triggers | Viewer Request, Viewer Response | Viewer Req/Res + Origin Req/Res |
| Max time | < 1ms | 5s (Viewer), 30s (Origin) |
| Memory | 2 MB | 128 MB (Viewer), 10 GB (Origin) |
| Request body | NO (on Viewer Req) | YES (with size limits) |
| Price | $0.0000001 per invocation | $0.00000625 per 100ms |
| Use cases | Headers, redirects, simple URL rewrites | Auth, A/B test, JWT validation, body inspection |

## Global Accelerator vs Route 53 vs CloudFront

| | Route 53 | Global Accelerator | CloudFront |
|---|---|---|---|
| Type | DNS | Anycast network proxy | CDN |
| IPs | DNS (changes) | 2 Static Anycast IPs | CF IPs (change) |
| Protocol | HTTP/S, TCP, UDP | TCP, UDP, HTTP/S | HTTP/S |
| Failover speed | Minutes (TTL) | < 1 minute | Varies |
| Caching | No | No | **Yes** |
| Main case | DNS routing | Global TCP apps, fixed IPs, non-HTTP | Global static/dynamic content |

## CloudFront + WAF Protection and Security

| Service | Protects against |
|---|---|
| AWS WAF | OWASP Top 10 (SQL injection, XSS), rate limiting, IP reputation, custom rules |
| Shield Standard | DDoS L3/L4 (free, automatic) |
| Shield Advanced | DDoS L7, DRT 24/7, cost credit (~$3K/month) |
| Geo Restriction | Block/allow countries (MaxMind GeoIP) |
| Signed URLs/Cookies | Paid/private content with expiration |

## Quick Exam Tips
- **CNAME does not work at apex** (company.com); use Alias
- Alias records are **free** for Route 53 → AWS resources
- CloudFront caching: `Cache-Control: no-cache` forces revalidation; TTL=0 never caches
- OAC > OAI for new projects (SSE-KMS, all S3 regions, more HTTP methods)
- Route 53 Health Check for private resources: via **CloudWatch Alarm** (HCs cannot reach resources without public IP)
- Calculated Health Check: combine multiple HCs with AND/OR/NOT
- WAF can be associated with: **CloudFront, ALB, API Gateway, AppSync**
- Global Accelerator: ideal when you need a **fixed IP** for firewall whitelisting
- Lambda@Edge runs in **edge locations** (specific regions); CloudFront Functions in **all PoPs**
- Route 53 low TTL before DNS migration → accelerates propagation of changes

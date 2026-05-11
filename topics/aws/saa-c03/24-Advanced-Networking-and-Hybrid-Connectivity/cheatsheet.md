# Cheatsheet - Advanced Networking and Hybrid Connectivity

## Quick pick

| Scenario | Recommended solution |
|---|---|
| 2 VPCs with simple traffic exchange | VPC Peering |
| dozens of VPCs and accounts | Transit Gateway |
| publish internal service to multiple accounts | PrivateLink |
| connect branch office quickly | Site-to-Site VPN |
| high throughput and predictable latency | Direct Connect |

## Important rules

- VPC Peering: no transitive routing
- TGW: centralized routing with separate route tables
- PrivateLink: connects consumer to private service endpoint
- DX: use redundant link and VPN as contingency
- Resolver inbound/outbound endpoints: hybrid DNS

## Exam pitfalls

- using full mesh peering (does not scale)
- forgetting overlapping CIDR (blocks peering/TGW)
- assuming Security Group filters internet traffic from public subnet without correct route
- confusing NACL as stateful (it is actually stateless)

## Trigger phrases

- "multiple VPCs across accounts" => Transit Gateway
- "privately access service" => PrivateLink
- "consistent network performance" => Direct Connect
- "encrypted connection over internet" => VPN

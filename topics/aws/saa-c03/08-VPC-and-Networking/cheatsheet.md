# Cheatsheet — Module 07: VPC and Networking

## Security Groups vs NACLs

| | Security Group | NACL |
|---|---|---|
| Level | Instance/ENI | Subnet |
| State | **Stateful** (automatic response) | **Stateless** (separate inbound AND outbound rules) |
| Rules | Allow only | Allow and **Deny** |
| Processing | All rules evaluated | Numeric order; stops at first match |
| Default | Blocks all inbound; allows all outbound | Allow all (inbound and outbound) |
| Association | N SGs per ENI, 1 SG across multiple ENIs | 1 NACL per subnet; 1 subnet per NACL |

## VPC Network Components

| Component | Function |
|---|---|
| Internet Gateway (IGW) | Outbound + inbound internet for public subnet (IPv4/IPv6) |
| NAT Gateway | Outbound internet for private subnet (IPv4 only); zonal |
| Egress-Only IGW | Outbound internet for private subnet (IPv6 only) |
| Virtual Private Gateway (VGW) | AWS endpoint for Site-to-Site VPN and DX Private VIF |
| Customer Gateway (CGW) | Represents on-prem device in VPN configuration |
| Transit Gateway (TGW) | Central hub for multiple VPCs and on-prem connections (transitive) |

## VPC Endpoints

| | Gateway Endpoint | Interface Endpoint (PrivateLink) |
|---|---|---|
| Services | S3, DynamoDB (only) | ~200+ AWS services + custom |
| How it works | Entry in route table | ENI with private VPC IP |
| Cost | Free | Charged ($/hour + $/GB) |
| On-premises | Not accessible | Accessible via DX/VPN |
| DNS | Does not change DNS | Private DNS option → resolves to ENI IP |

## Direct Connect (DX)

| Type | Capacity | Provisioning | Via |
|---|---|---|---|
| Dedicated Connection | 1/10/100 Gbps | Weeks | Direct with AWS |
| Hosted Connection | 50 Mbps to 10 Gbps | Faster | Via APN partner |

**Virtual Interfaces (VIF):**
- **Private VIF** → VPC via VGW or DX Gateway
- **Public VIF** → AWS public endpoints (S3, EC2 IPs)
- **Transit VIF** → Transit Gateway (multiple VPCs)

**DX + VPN:** add IPSec VPN over DX for data-in-transit encryption (DX by itself does not encrypt)

## Site-to-Site VPN

| | Site-to-Site VPN | Accelerated VPN |
|---|---|---|
| Path | Public internet (HTTPS/IPSec) | AWS Edge → private backbone |
| Latency | Variable | Reduced |
| Cost | Lower | SGA + per hour or additional transfer |
| Throughput | ~1.25 Gbps per tunnel | ~1.25 Gbps per tunnel |

- Each VPN connection has **2 tunnels** (redundancy; HA recommended via 2 customer gateways)
- VGW = AWS side; CGW = on-premises side

## Routing: Peering vs Transit Gateway

| | VPC Peering | Transit Gateway |
|---|---|---|
| Transit | Non-transitive | **Transitive** |
| Scale | N*(N-1)/2 connections for N VPCs | N attachments per TGW |
| Cross-region | Yes (inter-region peering) | Yes (TGW Peering) |
| Cost | No connection cost | Cost per attachment + per GB |
| CIDR overlap | Prevents peering | Does not allow communication (but attachment possible) |

## IPs Reserved per AWS Subnet
```
10.0.0.0/24 (256 IPs) → 251 available:
  10.0.0.0  → Network address
  10.0.0.1  → VPC router (default gateway)
  10.0.0.2  → DNS (Amazon DNS = VPC_CIDR_base + 2)
  10.0.0.3  → Reserved by AWS (future)
  10.0.0.255 → Broadcast
```

## VPC Flow Logs — Key Fields
```
version account-id interface-id srcaddr dstaddr srcport dstport protocol packets bytes start end action log-status
```
- Destinations: CloudWatch Logs or S3
- Does NOT capture: DNS (Route 53), DHCP, IMDS (169.254.x.x), Windows license activation

## Quick Exam Tips
- NAT Gateway: create **1 per AZ** for HA; each AZ's private subnet routes to its own AZ's NAT GW
- VPC Peering: CIDRs cannot overlap; is not transitive; works cross-region
- Transit Gateway: replaces peering mesh for large topologies; supports multicast
- Gateway Endpoint: adds route in route table; no public IP needed to access S3/DynamoDB
- Interface Endpoint with Private DNS: resolves public service name to private IP in the VPC
- PrivateLink: ideal for exposing SaaS or internal services to other VPCs without peering
- Direct Connect: does NOT encrypt by default; add VPN over DX for encryption
- Egress-Only IGW: for IPv6 outbound only (NAT does not exist for IPv6)
- Route Tables: one per subnet; subnets without explicit association use the main route table

# Module 07 — VPC and Networking

## Objective

In this module, you will learn to design secure, resilient, and scalable VPC networks, choosing the correct connectivity, segmentation, routing, and private access for scenarios covered on the exam.

## Key AWS Services

- Amazon VPC
- AWS Transit Gateway
- AWS Direct Connect
- AWS Site-to-Site VPN
- AWS PrivateLink (Interface Endpoints)

## Architecture and Trade-offs

## VPC Fundamentals

A VPC (Virtual Private Cloud) is a logically isolated virtual network within AWS. Each account receives one **Default VPC** per region.

### Key Components
```
VPC (10.0.0.0/16)
├── Public Subnet (10.0.1.0/24) — AZ-a
│     ├── Internet Gateway → route 0.0.0.0/0
│     └── Instances with public IP
├── Private Subnet (10.0.2.0/24) — AZ-a
│     ├── NAT Gateway (outbound internet, no inbound)
│     └── Instances without public IP
├── Private Subnet (10.0.3.0/24) — AZ-b
│     └── (multi-AZ redundancy)
├── Route Tables (one per subnet or shared)
├── Network ACLs (stateless, subnet level)
├── Security Groups (stateful, instance/ENI level)
├── DHCP Options Set
├── Elastic IPs
└── ENIs (Elastic Network Interfaces)
```

### CIDRs
- **Primary**: assigned at creation (cannot be changed), e.g., `10.0.0.0/16`
- **Secondary**: up to 5 additional blocks can be added
- Subnet size: `/28` (minimum) to `/16` (maximum)
- AWS **reserves 5 IPs** per subnet (.0 network, .1 VPC router, .2 DNS, .3 reserved, .255 broadcast)

---

## Security Groups vs Network ACLs

| Characteristic | Security Group | Network ACL |
|---|---|---|
| Level | Instance / ENI | Subnet |
| State | **Stateful** (automatic response) | **Stateless** (independent inbound and outbound rules) |
| Rules | ALLOW only | ALLOW and DENY |
| Evaluation | All rules evaluated | Rules in numeric order (1, 100, 200...) — first match applies |
| New default | Deny all, needs rules | Allow All inbound/outbound |
| Reference | Can reference another SG | CIDR only |

**Inbound traffic evaluation order:**
1. NACL (subnet level) → 2. Security Group (instance level)

---

## NAT Gateway vs NAT Instance

| Characteristic | NAT Gateway | NAT Instance (legacy) |
|---|---|---|
| Managed | AWS managed | You manage (EC2) |
| Scale | Automatic (up to 100 Gbps) | Manual (instance type) |
| Availability | Highly available per AZ | Single point of failure |
| Cost | Per hour + per GB processed | Per EC2 hour + EIP |
| Source/Dest Check | Automatic | Must disable manually |
| Security Groups | No (uses subnet NACL) | Yes (SG on instance) |

**Important:** NAT Gateway is zonal — for real HA, **one NAT GW per AZ** with per-AZ route table pointing to the local NAT GW.

---

## VPC Peering

Private network connection between two VPCs (same or different regions/accounts).

- Traffic uses AWS private network (not the internet)
- **Non-transitive**: VPC A ↔ VPC B and VPC B ↔ VPC C does **not** imply VPC A ↔ VPC C
- CIDRs cannot overlap
- Requires route table updates in both VPCs
- Supports cross-account and cross-region

```
VPC A ←──── peering ────→ VPC B
VPC B ←──── peering ────→ VPC C
VPC A ←────────────────── VPC C  ← NEEDS separate peering
```

---

## Transit Gateway (TGW)

Central hub that allows connecting multiple VPCs and on-premises networks:

```
VPC A ──┐
VPC B ──┤
VPC C ──┼──→ Transit Gateway ←──→ VPN / Direct Connect
VPC D ──┤
VPC E ──┘
```

- **Transitive** by default (A ↔ TGW ↔ C = A ↔ C, unlike peering)
- **Route Tables** on the TGW control which VPC can communicate with which
- Supports **multicast** (only AWS service to support it)
- TGW Resource Sharing via AWS RAM (share across Org accounts)
- **TGW Peering**: connects TGWs from different regions
- Ideal for hub-and-spoke with tens/hundreds of VPCs

---

## VPC Endpoints

Allow private access to AWS services **without leaving the VPC** (no IGW, NAT, VPN, DX):

### Gateway Endpoints
- Free
- Only for **S3 and DynamoDB**
- Added as a route table entry (service prefix → endpoint ID)
- Cannot be extended to on-premises or VPC peering

### Interface Endpoints (PrivateLink)
- ENI with private IP in the VPC
- Charged per hour + per GB processed
- Supports **most AWS services** and third-party services
- Access via private DNS (Endpoint-specific DNS names or Private DNS enabled)
- Can be accessed from on-premises via VPN/DX

---

## AWS Direct Connect (DX)

Dedicated network connection between on-premises and AWS:

| Type | Speed | SLA | Provisioning |
|---|---|---|---|
| Dedicated Connection | 1, 10, 100 Gbps | AWS SLA | Direct with AWS, weeks |
| Hosted Connection | 50 Mbps – 10 Gbps | Partner | Through partner, more flexible |

### Virtual Interfaces (VIFs)
- **Public VIF**: accesses AWS public endpoints (S3, DynamoDB, KMS API)
- **Private VIF**: accesses VPC private IPs
- **Transit VIF**: accesses Transit Gateway (for multiple VPCs via DX)

### Direct Connect Gateway
- Connects a DX connection to multiple VPCs in **different regions** (same account)
- Reduced number of Private VIFs (1 connection → multiple regions/VPCs)

### High Availability with DX
- **Backup DX**: two circuits at different points of presence
- **DX + VPN as backup**: Site-to-Site VPN as failover (lower cost, higher latency)
- **LAG (Link Aggregation Group)**: multiple physical circuits aggregated as one logical link

---

## Site-to-Site VPN

Encrypted connection (IPSec) between on-premises and VPC:
- **Virtual Private Gateway (VGW)**: terminates the VPN on the VPC
- **Customer Gateway (CGW)**: physical/software device on-premises
- VPN goes over the public internet (variable latency, encrypted)
- Throughput: up to ~1.25 Gbps (limited by VGW)
- **Accelerated Site-to-Site VPN**: uses Global Accelerator to reduce latency (exits internet at nearest PoP)

---

## VPC Flow Logs

- Captures IP traffic metadata (not payload) on VPCs, subnets, or ENIs
- Destinations: **CloudWatch Logs** or **S3**
- Includes: source/dest IP, port, protocol, bytes, packets, action (ACCEPT/REJECT), ENI ID
- Does not capture: DNS queries, DHCP, metadata (169.254.x.x), AWS link-local
- Latency: ~10–15 min after capture (near-real-time)

---

## IPv6 in VPC

- `/56` block assigned to VPC (AWS chooses, no private IPv6 ranges)
- Subnets receive `/64`
- **All IPv6 addresses are public** (no NAT for IPv6)
- **Egress-Only Internet Gateway**: allows IPv6 outbound without receiving inbound traffic (equivalent to NAT GW for IPv6)

---

## Elastic Network Interface (ENI)

Virtual network interface that can be:
- Moved between instances (for failover while keeping private IP and security groups)
- Multiple ENIs per instance (multi-homed: e.g., mgmt network + app network)
- Each ENI can have multiple private IPs and one Elastic IP

---

## Common Exam Pitfalls

- **Security Group = stateful** — does not need return rule; **NACL = stateless** — needs inbound AND outbound rules
- **VPC Peering is not transitive** — each pair needs its own peering; for many VPCs, use TGW
- **NAT Gateway per AZ** for HA — if all private subnets use one NAT GW in one AZ, there is a single point of failure
- **Gateway Endpoint** (S3, DynamoDB) = free; **Interface Endpoint** = charged per hour
- **Direct Connect + VPN** = dual layer of redundancy (DX primary + VPN fallback)
- Interface Endpoints accessible from on-prem via DX/VPN; Gateway Endpoints are not
- **TGW** supports transitivity — recommended when you have many VPCs (>5) to connect
- **Egress-only IGW** = NAT for IPv6 (outbound only, no public inbound)
- **VPC Flow Logs** does not capture packet contents — only metadata (IP, port, action)
- Flow Logs with REJECT = SG or NACL blocked; Flow Logs with ACCEPT but connectivity issue = application or OS problem

## Hands-on Lab

For guided networking practice, use [09-VPC-and-Networking-Labs/lab.md](../09-VPC-and-Networking-Labs/lab.md).
Cost notes: prefer short test windows for NAT Gateway and endpoints, validate routes with few resources, and do a complete teardown when finished.

## Practice Questions

- [questions.md](./questions.md)

## Quick Review / Cheatsheet

- [cheatsheet.md](./cheatsheet.md)
- [flashcards.md](./flashcards.md)

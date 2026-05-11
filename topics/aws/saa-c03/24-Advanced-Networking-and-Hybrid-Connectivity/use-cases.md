# Use Cases - Advanced Networking and Hybrid Connectivity

## Case 1: Multi-account enterprise group

Scenario:
- 50 VPCs across multiple accounts
- need for controlled communication

Architecture:
- Central Transit Gateway
- separate route tables by domain
- traffic inspection in security VPC

## Case 2: Private SaaS for enterprise clients

Scenario:
- clients in different AWS accounts
- no public exposure

Architecture:
- NLB + Endpoint Service
- consumption via Interface VPC Endpoint (PrivateLink)

## Case 3: Data center to AWS with low latency variation

Scenario:
- workloads sensitive to network variation
- high data volume

Architecture:
- AWS Direct Connect primary
- Site-to-Site VPN as backup
- BGP for failover

## Case 4: Hybrid DNS integration

Scenario:
- on-premises applications need to resolve private zones on AWS

Architecture:
- Route 53 Resolver inbound endpoint
- conditional forwarding in on-premises DNS

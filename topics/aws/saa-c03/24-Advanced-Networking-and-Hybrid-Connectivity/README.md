# 24 Advanced Networking and Hybrid Connectivity

## Module objectives

- master connectivity between VPCs, accounts and on-premises data center
- differentiate VPC Peering, Transit Gateway, PrivateLink, VPN and Direct Connect
- design networks with resilience, security and low latency
- solve exam questions focused on routing, isolation and transfer costs

## Fundamental concepts

In SAA-C03, advanced networking appears when the scenario involves multiple VPCs, multiple accounts, hybrid connectivity and private services.

## Key components

- VPC Peering: directly connects two VPCs; does not support transitive routing.
- AWS Transit Gateway (TGW): hub-and-spoke for many VPCs and VPNs.
- AWS PrivateLink: expose/consume private service without full peering.
- Site-to-Site VPN: IPSec tunnel over the internet.
- AWS Direct Connect (DX): dedicated link with low variability for on-premises.
- Route 53 Resolver endpoints: hybrid DNS between AWS and on-premises.

## When to use each one

- few VPCs and simple topology: VPC Peering
- many VPCs/accounts with central routing: TGW
- publish internal service to other accounts with smaller surface: PrivateLink
- quick connectivity without dedicated circuit: VPN
- stable high throughput connectivity: Direct Connect (with VPN backup)

## Exam tips

- peering is not transitive; TGW solves this.
- if the question asks for private service access without opening the full CIDR, think PrivateLink.
- DX usually appears with requirements for more predictable latency and high traffic.
- for hybrid high availability, combine DX + VPN backup.
- Security Group is stateful; NACL is stateless (recurring trap).

## Related links

- [Cheatsheet](./cheatsheet.md)
- [Use cases](./use-cases.md)
- [Questions](./questions.md)
- [Flashcards](./flashcards.md)
- [Lab](./lab.md)
- [Official links](./links.md)

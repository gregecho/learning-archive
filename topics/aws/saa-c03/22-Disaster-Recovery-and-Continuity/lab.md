# Lab - Basic Multi-Region DR

## Objective
Implement a simple failover with Route 53 and data replication in S3.

## Steps

1. Create two S3 buckets in different regions.
2. Enable versioning on both.
3. Configure CRR from the primary bucket to the secondary bucket.
4. Publish a static page in two regions (S3 static website or minimal EC2).
5. Configure Route 53 Failover Record:
- Primary pointing to main workload
- Secondary pointing to secondary workload
6. Create a Health Check for the primary endpoint.
7. Simulate a failure (interrupt primary endpoint) and validate failover.
8. Document the observed RTO.

## Validation

- Objects replicate to the second region
- DNS switches to secondary endpoint after failure
- Application returns to primary after recovery

## Cleanup

- remove Route 53 records/health checks
- delete resources and buckets to avoid cost

---

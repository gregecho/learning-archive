# Use Cases — Module 06: Databases

## Case 1: E-commerce with RDS Multi-AZ and Read Replicas

**Scenario:** E-commerce with seasonal traffic spikes. Catalog is read 20x more than written. Automatic failover required.

**Architecture:**
```
                ┌─ RDS PostgreSQL Primary (us-east-1a)
                │    ├── OLTP: orders, payments
ALB → App      ─┤    └── Multi-AZ Standby (us-east-1b) ← sync replica
Servers        │
                └─ RDS Read Replica x3 (us-east-1c)
                     └── OLTP reads: catalog, search

ElastiCache Redis ← Session cache + most searched catalog
```

**Key configurations:**
- Primary endpoint: writes + critical reads (strong consistency)
- Read Replica endpoint (Reader): catalog reads (eventual consistency ok)
- ElastiCache Redis: 1-hour cache for product pages
- RDS Multi-AZ: standby in different AZ, failover ~1-2 min

---

## Case 2: Serverless Application with DynamoDB and DAX

**Scenario:** Real-time leaderboard API for a mobile game with 1 million concurrent active users.

**Architecture:**
```
Mobile App → API Gateway → Lambda
                              ├── DynamoDB Table (Players)
                              │     ├── PK: player_id
                              │     └── GSI: score-index (PK: game_id, SK: score)
                              └── DAX Cluster (cache layer)
                                    └── Latency < 1ms for top players
```

**DynamoDB Design:**
```
Table: GameLeaderboard
  PK: game_id#season
  SK: player_id
  GSI1: score-index (PK: game_id#season, SK: score) → top 100 per game

TTL: season_end_timestamp → auto-deletes previous season data
```

**Why DAX?** Lambda cold starts + 1M users → DynamoDB would have microsecond latency but DAX guarantees < 100us for any query. GSI enables efficient `query` by ranking without scanning.

---

## Case 3: Aurora Global Database for Multi-Regional Application

**Scenario:** Global SaaS with users in America (us-east-1) and Europe (eu-west-1). European regulation requires data in Europe.

**Architecture:**
```
America (us-east-1) — PRIMARY
  └── Aurora PostgreSQL Cluster
        ├── Writer Instance
        ├── Reader Instance x2
        └── US App Servers (writes + reads)

                    ↓ Replication < 1 second (Global Database)

Europe (eu-west-1) — SECONDARY
  └── Aurora PostgreSQL Cluster (read-only)
        ├── Reader Instance x2 (local reads GDPR)
        └── EU App Servers (reads only)

Failover:
  Aurora Managed Planned Failover → promotes EU to Primary in < 1 minute
  RPO < 1s | RTO < 1 minute
```

---

## Case 4: Analytics Pipeline with Redshift + Spectrum

**Scenario:** BI team needs to cross historical sales data in the DW with fresh data from an S3 data lake.

**Architecture:**
```
Historical Data (DW)              Fresh Data (Data Lake)
  └── Redshift Cluster               └── S3 (Parquet, date-partitioned)
        └── table: sales_hist              └── Glue Catalog (file schemas)

Unified query (Redshift Spectrum):
SELECT h.region, f.product, SUM(h.revenue) + SUM(f.revenue) as total
FROM sales_hist h
JOIN spectrum.sales_fresh f ON h.product_id = f.product_id  ← S3 via Spectrum
WHERE f.date >= CURRENT_DATE - 7
GROUP BY 1, 2
```

**Benefit:** No daily ETL to load S3 data into DW. Real-time joins between DW and Data Lake. Redshift MPP distributes Spectrum processing across nodes.

---

## Case 5: Fraud Prevention with DynamoDB + ElastiCache

**Scenario:** Banking system needs to verify if a card payment is being made from a suspicious IP or device in < 10ms.

**Architecture:**
```
Payment → API
  ├── ElastiCache Redis → Check: ip_blacklist, device_fingerprint (hits < 1ms)
  │         └── Cache Miss → DynamoDB → redis (write-through)
  │
  ├── DynamoDB: fraud_signals_table
  │     PK: signal_type (ip|device|account)
  │     SK: signal_value
  │     Attributes: risk_score, last_seen, blocked_until (TTL)
  │
  └── EventBridge: "fraud_detected" → SNS → Email/Lambda → Block Account
```

**Pattern used:** Write-through cache (when detecting a new fraud signal, writes to Redis AND DynamoDB simultaneously). TTL on DynamoDB to auto-expire old signals. DAX could replace Redis+DynamoDB if all logic stays in DynamoDB.

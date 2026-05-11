# Questions — Module 15: Migration and Data Transfer

> **SAA-C03 Domain**: Design Resilient Architectures
> **Difficulty**: Medium

---

**1.** A company needs to migrate 500 TB of data from a data center to AWS. The internet connection is 1 Gbps shared with the company. Internet transfer would take more than 45 days. Which service should be used?

- A) AWS DataSync with transfer scheduler
- B) AWS Direct Connect for direct transfer
- C) AWS Snowball Edge Storage Optimized (multiple devices)
- D) S3 Transfer Acceleration

<details><summary>Answer</summary>

**C** — Snowball Edge Storage Optimized: 80 TB/device. For 500 TB, ~7 devices would be needed. DataSync via internet (A) would take 45+ days with shared 1 Gbps. Direct Connect (B) requires months of provisioning and setup. Snow Family is ideal when network transfer would take weeks.

</details>

---

**2.** A company is migrating an Oracle 12c database to Amazon Aurora PostgreSQL. The team needs to convert PL/SQL stored procedures that are incompatible with PostgreSQL. Which tool should be used?

- A) AWS DMS (Database Migration Service)
- B) AWS Schema Conversion Tool (SCT)
- C) AWS Glue for data transformation
- D) Amazon RDS for Oracle instead of Aurora

<details><summary>Answer</summary>

**B** — SCT (Schema Conversion Tool): converts the schema and procedural code (stored procedures, functions, triggers, PL/SQL packages) from Oracle to the PostgreSQL dialect. Identifies objects that cannot be automatically converted and generates a report. Then, use DMS for data migration.

</details>

---

**3.** A company wants to migrate 50 on-premises Windows servers to Amazon EC2 with minimal changes. The maintenance window is only 2 hours. Which service should be used?

- A) AWS Application Migration Service (MGN) with continuous replication before cutover
- B) AWS SMS (Server Migration Service) with scheduled cutover
- C) Manually create AMIs and launch EC2 instances
- D) AWS DMS to migrate complete servers

<details><summary>Answer</summary>

**A** — MGN installs a replication agent on source servers and continuously replicates disks to AWS. When ready for cutover, the maintenance window is only for the final delta (minutes, not hours). RTO of ~30-60 minutes vs 2-hour window is achievable. SMS is the legacy service replaced by MGN.

</details>

---

**4.** A retail company has B2B partners that can only transfer files via SFTP. The company wants to receive these files directly in S3 without maintaining an SFTP server. Which service should be used?

- A) AWS DataSync with SFTP endpoint
- B) AWS Transfer Family with SFTP protocol and S3 backend
- C) AWS Storage Gateway File Gateway
- D) S3 with pre-signed URLs for upload

<details><summary>Answer</summary>

**B** — Transfer Family: creates a managed SFTP endpoint (no server to manage). Partners continue using their existing SFTP clients without changes. Files are stored directly in S3. Authentication can be via IAM, Cognito, or custom Lambda (for LDAP/AD).

</details>

---

**5.** A company wants to migrate a 2 TB MySQL database from on-premises to Amazon RDS MySQL with less than 15 minutes of downtime. What is the strategy?

- A) Export MySQL dump, upload to S3, restore in RDS (hours of downtime)
- B) DMS full load + CDC: migrate initial data, then replicate changes, cutover with minimal window
- C) Create Read Replica in RDS pointing to on-premises MySQL and promote
- D) AWS Database Migration Service with snapshot migration

<details><summary>Answer</summary>

**B** — DMS with CDC (Change Data Capture): first performs full load of the database to RDS (no impact on production). Then enables CDC to replicate changes in real time. When both databases are in sync, the cutover window is minimal (only accumulated lag, which can be seconds). Total downtime < 15 minutes.

</details>

---

**6.** A team wants to migrate data from on-premises NAS files to Amazon EFS, ensuring that Unix timestamps and permissions are preserved. Which service should be used?

- A) AWS Snowball Edge + rsync
- B) AWS DataSync with metadata preservation
- C) FTP to S3 + copy script
- D) AWS Storage Gateway File Gateway

<details><summary>Answer</summary>

**B** — DataSync: preserves file metadata (modification, access, creation timestamps; Unix uid/gid/chmod permissions). Supports NFS → EFS. Performs integrity verification (checksums) during and after transfer. More reliable and faster than manual rsync.

</details>

---

**7.** A company wants to evaluate their on-premises server fleet before migration to identify server dependencies and usage patterns. The environment is VMware. Which service and mode should be used?

- A) Application Discovery Service with Agent-based mode on each server
- B) Application Discovery Service Agentless with VMware vCenter Connector
- C) AWS Migration Hub with manual analysis
- D) AWS MGN with pre-migration analysis

<details><summary>Answer</summary>

**B** — ADS Agentless: VM appliance on VMware vCenter collects CPU, memory, storage, and network from VMs without installing agents on each server. Faster to implement for initial inventory. Agent-based (A) provides more detailed data (processes, network connections) but requires installation on each server.

</details>

---

**8.** A company discovered that 30% of their on-premises applications have low usage and will be discontinued in the next 6 months. What is the correct migration strategy for these applications?

- A) Rehost (lift-and-shift) to EC2
- B) Replatform to managed services
- C) Retire (do not migrate — eliminate)
- D) Retain (keep on-premises until discontinuation)

<details><summary>Answer</summary>

**C** — Retire: if the application will be discontinued in 6 months, there is no reason to invest in migration. Eliminating now immediately reduces operational costs. Retain (D) would be correct if there were a technical reason to keep on-premises temporarily, but knowing they will be discontinued, retire immediately.

</details>

---

**9.** A company wants to move its legacy on-premises CRM (without vendor support) to a modern SaaS CRM in the cloud. Which migration strategy would the 7 Rs classify this as?

- A) Rehost
- B) Replatform
- C) Repurchase
- D) Refactor

<details><summary>Answer</summary>

**C** — Repurchase: replace with a SaaS product (e.g., Salesforce, HubSpot, SAP). The code is not migrated; data is migrated to the new SaaS system. The company abandons the legacy system and adopts a ready-made modern solution.

</details>

---

**10.** A company needs to migrate 10 PB of data from magnetic tapes to S3 for long-term retention. Which AWS service should be used?

- A) 100 Snowball Edge devices
- B) AWS Snowmobile (truck with 100 PB capacity)
- C) Dedicated Direct Connect + DataSync
- D) 125 Snowball Edge Storage Optimized devices

<details><summary>Answer</summary>

**D** — Snowball Edge Storage Optimized: 80 TB per device. For 10 PB: 10,000 TB / 80 TB = 125 devices. Snowmobile (B) is for migrations > 100 PB (exabyte-scale). For 10 PB, multiple Snowball Edges in parallel is the practical solution.

</details>

---

**11.** A company wants to migrate its on-premises Oracle RAC database to AWS. Oracle RAC uses proprietary features not available in RDS. What is the best option?

- A) RDS Oracle Multi-AZ
- B) Amazon RDS Custom for Oracle (access to operating system and engine)
- C) Oracle on EC2 with EFS shared storage
- D) Aurora PostgreSQL with Oracle compatibility

<details><summary>Answer</summary>

**B** — RDS Custom for Oracle: managed option that still allows OS access and engine customization (for customers needing specific patches, RAC-like features via workarounds, or external dependencies). More managed than pure Oracle on EC2, but more flexible than standard RDS Oracle.

</details>

---

**12.** During a DMS migration from SQL Server to Aurora MySQL, the team notices that triggers in SQL Server are not compatible. What is the role of SCT in this scenario?

- A) SCT automatically migrates data like DMS
- B) SCT automatically converts SQL Server T-SQL triggers to MySQL SQL, identifying incompatibilities for manual adjustment
- C) SCT only verifies data type compatibility
- D) SCT is not needed for SQL Server → MySQL

<details><summary>Answer</summary>

**B** — SCT analyzes SQL Server procedural code (T-SQL: stored procedures, triggers, functions) and converts to MySQL SQL where possible. For code that cannot be automatically converted (proprietary T-SQL features), it generates a report with required manual actions and indicates conversion complexity per object.

</details>

---

**13.** A company operates a data center with 200 on-premises servers and wants to know how much it will cost to run them on AWS before committing to migration. Which tool should be used?

- A) AWS Cost Explorer with projections
- B) AWS Migration Evaluator (Agentless Collector + TCO Analysis)
- C) AWS Compute Optimizer
- D) Trusted Advisor with cost analysis

<details><summary>Answer</summary>

**B** — AWS Migration Evaluator (formerly TSO Logic): collects on-premises environment utilization data (via agentless collector or data import) and provides detailed TCO (Total Cost of Ownership) analysis comparing current costs vs AWS. Basis for migration business case.

</details>

---

**14.** A company needs to move data daily from an on-premises NFS server to an S3 bucket on a scheduled and verified basis. Which service should be used?

- A) Storage Gateway File Gateway
- B) AWS DataSync with scheduled task
- C) Direct Connect + S3 Transfer Acceleration
- D) AWS Snowcone with embedded DataSync agent

<details><summary>Answer</summary>

**B** — DataSync: install the agent on the on-premises server (or use DataSync VM agent), connect to NFS source and S3 destination, create a task with schedule (daily). Verifies integrity with checksums and only performs incremental transfer after the first full sync. Simpler than managing Storage Gateway for migration.

</details>

---

**15.** A manufacturing company has legacy IoT equipment in remote locations with limited internet connectivity. They need to collect and process data locally before sending to AWS. Which Snow device should be used?

- A) AWS Snowmobile
- B) AWS Snowball Edge Compute Optimized (edge computing + storage)
- C) AWS Snowcone with basic edge computing
- D) AWS Outposts

<details><summary>Answer</summary>

**B** — Snowball Edge Compute Optimized: 52 vCPUs, 208 GB RAM, 42 TB storage + 28 TB NVMe SSD, optional GPU. Runs EC2 instances (AMIs locally), Lambda functions, and SageMaker inference at the edge. Ideal for processing IoT data in remote locations and syncing with AWS when connectivity is available.

</details>

---

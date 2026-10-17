# ZeroTrace — Autonomous Erasure & Proof Infrastructure

> **"Stripe for Data Destruction"** — India's DPDP Act, 2023 compliant data destruction and verification infrastructure for modern enterprise lakehouses, AI memory, and semantic caches.

[![CI](https://github.com/zerotrace/zerotrace/actions/workflows/ci.yml/badge.svg)](https://github.com/zerotrace/zerotrace/actions)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)

---

## 1. Overview & Problem

Under India's **Digital Personal Data Protection Act, 2023 (DPDP Act)**, when a Data Principal withdraws consent, companies (Data Fiduciaries) must erase their personal data across all storage layers. Penalties reach up to ₹250 crore.

### The Three Traps of Modern Data Deletion
1. **The Lakehouse Time-Travel Trap**: SQL `DELETE` on Apache Iceberg, Delta Lake, or Snowflake in Merge-on-Read mode only writes positional delete files. The original Parquet data remains on disk and queryable via historical snapshots. Manifest files, column statistics (min/max bounds), and S3 versioning keep PII alive indefinitely.
2. **The AI / RAG Ghost Memory Trap**: Customer support transcripts chunked into vector databases (pgvector) remain queryable by LLMs even if the primary SQL row is deleted. Residual data lingers in Postgres dead tuples and Redis semantic cache AOF persistence files.
3. **The Audit Compliance Paradox**: Keeping an audit log that "Person X was erased" itself violates data minimisation by storing Person X's identifier in the audit log.

ZeroTrace physically destroys data across Lakehouse, Vector DB, and Semantic Cache, attacks its own work using an adversarial red-team audit, and issues a **privacy-preserving cryptographic receipt** verifiable client-side without storing a single byte of PII in the audit trail.

---

## 2. System Architecture

```text
                               +-----------------------------+
                               |     Data Principal Portal   |  (Voice / Text Intake)
                               +--------------+--------------+
                                              |
                                              v
+-----------------------------------------------------------------------------------------+
|                                    BRAIN PLANE                                          |
|                                                                                         |
|  +--------------------+    +---------------------+    +------------------------------+  |
|  |  Sarvam AI (STT)   |--->|  Gemma Intent Parser|--->|  Agentic Lineage Discovery   |  |
|  |  (kn, hi, ta, te)  |    |  (DPDP Act Sec 6/12)|    |  (Lake, Vector, Cache Graph) |  |
|  +--------------------+    +---------------------+    +--------------+---------------+  |
+----------------------------------------------------------------------|------------------+
                                                                       v
+-----------------------------------------------------------------------------------------+
|                                    DATA PLANE                                           |
|                                                                                         |
|  +----------------------------+   +-----------------------+   +----------------------+  |
|  |  Speed 1: Crypto Killswitch|   | Speed 2: Lakehouse    |   | Speed 2: pgvector    |  |
|  |  (Envelope Key Shredding)  |   | (Targeted Bloom Scan) |   | & Redis Cache Purge  |  |
|  +----------------------------+   +-----------------------+   +----------------------+  |
|                                              |                                          |
|                                              v                                          |
|  +-----------------------------------------------------------------------------------+  |
|  |                 Adversarial Red-Team Audit & Self-Healing Loop                    |  |
|  |      (Time travel, PyArrow raw scan, S3 bucket grep, Vector sweep, Collateral)    |  |
|  +-------------------------------------------+---------------------------------------+  |
+----------------------------------------------|------------------------------------------+
                                               v
+-----------------------------------------------------------------------------------------+
|                                    PROOF PLANE                                          |
|                                                                                         |
|  +------------------------------+  +-------------------------+  +--------------------+  |
|  |  Salted Merkle Tree Engine   |  | Ed25519 Receipt Signer  |  | Blockchain Anchor  |  |
|  |  (Pre-root, Post, Diff-root) |  | (No plaintext PII)      |  | (ShipRite / EVM)   |  |
|  +------------------------------+  +-------------------------+  +--------------------+  |
+-----------------------------------------------------------------------------------------+
```

---

## 3. Monorepo Structure & Ownership

- `apps/web/` — Frontend (Rohan): Data Principal Portal, DPO Console, Adversary Console, Public Verifier, Demo Director.
- `services/data-plane/` — Data Plane (Moiz): Apache Iceberg on S3, pgvector, Redis, PySpark engine, adversarial attack library.
- `services/orchestrator/` — Brain Plane & Proof Plane (Pavan): FastAPI orchestration saga, Sarvam/Gemma adapters, Merkle proof engine, Ed25519 signer, blockchain anchor.
- `contracts/` — Frozen API contracts: `openapi.orchestrator.yaml`, `openapi.dataplane.yaml`, `events.schema.json`, `receipt.schema.json`, test fixtures.
- `infra/` — Docker Compose, production compose, Caddyfile, database initialization.
- `docs/` — Proof specifications (`docs/proof-spec.md`), runbook (`docs/runbook.md`), and integration checklists (`docs/integration.md`).

---

## 4. Quick Start (One Command)

### Prerequisites
- Python 3.11+
- Docker and Docker Compose

### 1. Run Tests & Golden Path Verification
```bash
# Run 17 unit, cryptographic proof, and contract tests
pytest services/orchestrator/tests -v

# Run 10-stage headless End-to-End Golden Path validation
python scripts/e2e_golden_path.py
```

### 2. Start Full Local Development Stack
```bash
docker compose -f infra/docker-compose.yml up -d
```

### 3. Open Interactive Swagger Docs
- Orchestrator API: `http://localhost:8001/docs`
- Mock Orchestrator: `python contracts/mock_orchestrator.py` (Port 8001)
- Stub Data Plane: `python services/orchestrator/src/adapters/stub_dataplane.py` (Port 8002)

---

## 5. Technical Novelties

| Novelty | Description |
|---|---|
| **N1: Atomic Tri-Layer Synchronisation** | Coordinated, idempotent saga erasing Lakehouse, pgvector AI memory, and Redis semantic cache with a single job ID. |
| **N2: Two-Speed Erasure** | Instant cryptographic key destruction (< 1s readability cutoff) followed by verified physical Parquet & index eradication. |
| **N3: Blast-Radius Compaction** | Per-file Bloom filter Subject Locator Index targeting only 3 of 480 files, measured at ₹212 vs ₹1,046 for full-table rewrite (79.7% saving). |
| **N4: Adversarial Self-Audit & Self-Healing** | 9-vector red-team audit attacks its own work. If residue (e.g. planted ghost embedding) is detected, the engine enters remediation and re-audits. |
| **N5: Privacy-Preserving Audit Proof** | Domain-separated salted Merkle trees over pre- and post-purge states. Retains ZERO personal identifiers in audit log. |
| **N6: Trustless Browser-Side Verification** | The Public Verifier recomputes all Merkle math client-side. Altering 1 byte in the receipt causes instant verification failure. |
| **N7: Collateral Integrity Guarantee** | Cryptographic row-level checksum proof showing 49,999 non-subject records were completely untouched. |
| **N8: Statutory Retention Intelligence** | Automatically quarantines KYC and financial records into an encrypted retention vault under PMLA 2002 / RBI 5-year lock. |
| **N9: Multilingual Voice-First Intake** | Data Principals can speak Kannada, Hindi, Tamil, Telugu, or English; Sarvam AI transcribes and Gemma extracts intent. |
| **N10: Regulator-Ready Legal Artifacts** | Automatically generates Bharatiya Sakshya Adhiniyam, 2023 (Section 63) electronic evidence certificate and DPBI compliance pack. |

---

## 6. License
Apache License 2.0. Built for Hacktober Hackathon 2026.

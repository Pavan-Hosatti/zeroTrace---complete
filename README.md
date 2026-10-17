# ZeroTrace — Autonomous Erasure & Proof Infrastructure

> **"Stripe for Data Destruction"** — India's DPDP Act, 2023 compliant autonomous data destruction and proof infrastructure for modern enterprise lakehouses, AI memory, and semantic caches.

[![CI](https://github.com/zerotrace/zerotrace/actions/workflows/ci.yml/badge.svg)](https://github.com/zerotrace/zerotrace/actions)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache_2.0-blue.svg)](LICENSE)
[![Python 3.11](https://img.shields.io/badge/Python-3.11-3776AB.svg?logo=python)](https://python.org)
[![FastAPI](https://img.shields.io/badge/FastAPI-0.115-009688.svg?logo=fastapi)](https://fastapi.tiangolo.com)
[![Tests Passing](https://img.shields.io/badge/Tests-48%20Passed-brightgreen.svg)]()
[![DPDP Act 2023](https://img.shields.io/badge/Compliance-DPDP%20Act%202023-orange.svg)]()
[![BSA 2023 Sec 63](https://img.shields.io/badge/Legal-BSA%202023%20Sec%2063-purple.svg)]()

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
|  |  (Pre-root, Post, Diff-root) |  | (Zero Plaintext PII)    |  | (ShipRite / EVM)   |  |
|  +------------------------------+  +-------------------------+  +--------------------+  |
+-----------------------------------------------------------------------------------------+
```

---

## 3. Verified Cryptographic Benchmarks

Benchmarked on production-grade Python 3.11 with sub-second guarantees:

| Benchmark Target | Ops / Throughput | Latency | Significance |
|---|---|---|---|
| **Salted Merkle Tree (480 leaves)** | **198,937 leaves/sec** | **2.413 ms** | State tree construction over 480 lakehouse partitions in ~2.4ms |
| **Merkle Inclusion Proof Verification** | **24,374 proofs/sec** | **0.041 ms** | Real-time browser-side trustless verification without server overhead |
| **Ed25519 Digital Signing** | **3,927 signs/sec** | **0.255 ms** | Sub-millisecond non-repudiable legal attestation |
| **Ed25519 Signature Verification** | **2,759 verifications/sec** | **0.362 ms** | Instant regulator & DPO signature validation |
| **Sovereign Subject Commitment** | **263,776 hashes/sec** | **0.004 ms** | HMAC-SHA256 privacy-preserving sovereign ownership proofs |

---

## 4. Sponsor & Ecosystem Integrations

- **ShipRite AI**: On-chain root anchoring with intelligent circuit-breaking and fallback (`LocalSignedLedger` / EVM contract). Anchors Merkle `diff_root` to public blockchain for immutable external auditability.
- **Sarvam AI**: High-accuracy Indic speech-to-text supporting Kannada (`kn-IN`), Hindi (`hi-IN`), Tamil (`ta-IN`), Telugu (`te-IN`), and English (`en-IN`), backed by local acoustic phoneme fallback.
- **Gemma (Google)**: Legal intent classification engine extracting statutory consent revocations under DPDP Act 2023 Section 6(4) & 12(1), equipped with prompt-injection sanitization.

---

## 5. Monorepo Structure & Ownership

- `apps/web/` — Frontend (Rohan): Data Principal Portal, DPO Console, Adversary Console, Public Verifier, Demo Director.
- `services/data-plane/` — Data Plane (Moiz): Apache Iceberg on S3, pgvector, Redis, PySpark engine, adversarial attack library.
- `services/orchestrator/` — Brain Plane & Proof Plane (Pavan):
  - 11-stage autonomous saga executor (`orchestration.py`)
  - Merkle tree & proof engine (`merkle.py`)
  - Ed25519 signer & BSA 2023 evidence generator (`signer.py`, `evidence_generator.py`)
  - ShipRite blockchain anchor (`shiprite.py`, `anchor.py`)
  - Sarvam AI & Gemma adapters (`sarvam.py`, `gemma.py`)
  - Operational admin & Prometheus metrics (`api/admin.py`, `/metrics`)
- `contracts/` — Frozen API contracts: `openapi.orchestrator.yaml`, `openapi.dataplane.yaml`, `events.schema.json`, `receipt.schema.json`, test fixtures.
- `infra/` — Docker Compose, production compose, Caddyfile, database initialization.
- `docs/` — Proof specifications (`docs/proof-spec.md`), runbook (`docs/runbook.md`), and integration checklists (`docs/integration.md`).

---

## 6. Quick Start

### 1. Run Tests & Contract Conformance (48/48 Passing)
```bash
# Run all 48 unit, cryptographic proof, fault injection, and OpenAPI conformance tests
pytest services/orchestrator/tests -v

# Run cryptographic benchmarks
python scripts/benchmark_proofs.py

# Run 10-stage headless End-to-End Golden Path validation
python scripts/e2e_golden_path.py
```

### 2. Start Full Stack (Orchestrator, Data Plane, Postgres, Redis, MinIO)
```bash
docker compose -f infra/docker-compose.yml up -d
```

### 3. Run Demo Director Scenarios
```bash
# Scenario 1: Golden Path (Kannada voice intake -> targeted erasure -> proof -> anchor)
python demo/director/scenario_runner.py --scenario golden

# Scenario 2: Self-healing ghost embedding remediation
python demo/director/scenario_runner.py --scenario ghost_heal

# Scenario 3: Statutory retention hold under DPDP Act Sec 8(4) & PMLA 2002
python demo/director/scenario_runner.py --scenario retention_hold
```

### 4. Interactive API Documentation & Telemetry
- Orchestrator Swagger: `http://localhost:8001/docs`
- Prometheus Metrics: `http://localhost:8001/metrics`
- System Preflight: `http://localhost:8001/api/v1/system/preflight`
- Trustless Verifier: `http://localhost:8001/api/v1/verify`

---

## 7. Technical Novelties

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

## 8. License
Apache License 2.0. Built for Hacktober Hackathon 2026.

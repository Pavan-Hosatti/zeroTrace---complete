# ZeroTrace Monorepo Integration Checklist & Contract Guide

This document coordinates the parallel development of Rohan (Frontend, `apps/web`), Moiz (Data Plane, `services/data-plane`), and Pavan (Platform & Orchestrator, `services/orchestrator`).

---

## 1. Team Ownership Boundaries

| Owner | Directory | Responsibilities |
|---|---|---|
| **Rohan** | `apps/web` | Frontend: Portal, DPO Console, Adversary Console, Public Verifier, Demo Director. |
| **Moiz** | `services/data-plane` | Data Plane: Lakehouse (Iceberg), Vector store (pgvector), Cache (Redis), Seed generator, Attack suite. |
| **Pavan** | `services/orchestrator`, `contracts/`, `infra/`, root | Orchestrator, Proof plane, State manifests, Contracts, Platform & Deployment. |

---

## 2. Unblocking Rohan (Frontend)

Rohan does NOT need to wait for the real backend. Two options are provided:

### Option A: The Mock Orchestrator (Port 8001)
Run the high-fidelity mock server that streams pre-recorded NDJSON fixtures over SSE with `Last-Event-ID` support:
```bash
python contracts/mock_orchestrator.py
```
This serves on `http://localhost:8001/api/v1` with full CORS enabled.

### Option B: Pre-recorded Fixtures in `contracts/fixtures/`
- `contracts/fixtures/golden-job-events.ndjson`: 42-event sequence covering all 11 stages.
- `contracts/fixtures/audit-fail-self-heal.ndjson`: Sequence showing ghost embedding detection, round 1 failure, targeted remediation, and round 2 pass.
- `contracts/fixtures/retention-hold.ndjson`: Sequence showing KYC statutory hold ending in `COMPLETED_WITH_HOLDS`.
- `contracts/fixtures/sample-receipt.json`: Valid cryptographic receipt.
- `contracts/fixtures/proof-test-vectors.json`: Mathematical test vectors for in-browser client-side cryptographic verification (including tamper cases).

---

## 3. Unblocking Moiz (Data Plane)

Moiz builds against `contracts/openapi.dataplane.yaml` (Base path `http://localhost:8002`, header `X-Service-Key: dev-service-key`).
To verify conformance, Pavan has provided:
```bash
# Start stub data plane to see sample responses
python services/orchestrator/src/adapters/stub_dataplane.py
```

### Integration Checkpoints
- [x] Checkpoint 1: Contracts frozen in `contracts/` with OpenAPI 3.0 & JSON Schemas.
- [x] Checkpoint 2: Orchestrator core & proof plane mathematically verified (17/17 tests passing).
- [x] Checkpoint 3: End-to-end golden path pipeline verified headlessly.
- [ ] Checkpoint 4: Connect Rohan's frontend to real orchestrator on port 8001.
- [ ] Checkpoint 5: Connect Moiz's PySpark data plane to orchestrator on port 8002.
- [ ] Checkpoint 6: Three consecutive full demo runs under 90 seconds without manual intervention.

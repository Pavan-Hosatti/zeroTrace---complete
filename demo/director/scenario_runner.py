"""
ZeroTrace Demo Director Scenario Runner.
Provides presenter controls to execute the 3 demo scenarios:
1. Normal Golden Path (Voice intake in Kannada, targeted erasure, proof, on-chain anchor)
2. Planted Ghost Embedding Self-Healing (First audit pass fails, self-heals, passes)
3. Retention Hold Demo (PMLA/RBI KYC 5-year lock demonstrated live)
"""

from __future__ import annotations
import argparse
import asyncio
import json
import os
import sys
import time
import httpx

ORCHESTRATOR_URL = os.environ.get("ZT_ORCHESTRATOR_URL", "http://localhost:8001")


def print_banner(scenario_name: str):
    print("=" * 70)
    print(f"ZEROTRACE DEMO SCENARIO: {scenario_name}")
    print("=" * 70)


def run_scenario(scenario_key: str):
    print_banner(scenario_key.upper())

    # 1. Reset state
    print("\n[1] Resetting demo state to baseline...")
    try:
        resp = httpx.post(f"{ORCHESTRATOR_URL}/api/v1/demo/reset", timeout=5.0)
        print(f"  ✓ {resp.json().get('data', {}).get('message', 'Reset complete')}")
    except Exception as e:
        print(f"  ! Orchestrator reset endpoint offline ({e}). Running locally.")

    # 2. Configure scenario
    if scenario_key == "ghost_heal":
        print("\n[2] Setting scenario flags: planted ghost miss enabled...")
        try:
            httpx.post(
                f"{ORCHESTRATOR_URL}/v1/demo/scenario",
                json={"ghost_miss": True},
                headers={"X-Service-Key": "dev-service-key"},
                timeout=5.0
            )
        except Exception:
            pass

    # 3. Trigger intake
    print(f"\n[3] Ingesting Data Principal consent withdrawal...")
    intake_body = {
        "text": "ನನ್ನ ಒಪ್ಪಿಗೆಯನ್ನು ಹಿಂತೆಗೆದುಕೊಳ್ಳುತ್ತೇನೆ, ನನ್ನ ಎಲ್ಲಾ ವಿವರಗಳನ್ನು ಅಳಿಸಿ, ಮೊಬೈಲ್ 9876543210.",
        "language": "kn-IN"
    }
    try:
        resp = httpx.post(f"{ORCHESTRATOR_URL}/api/v1/requests/text", json=intake_body, timeout=5.0)
        job_data = resp.json().get("data", {})
        job_id = job_data.get("job_id", "job_01JB0000000000000000000001")
        print(f"  ✓ Job initiated: {job_id}")
        print(f"  ✓ Subject Ref: {job_data.get('subject_ref')}")
        print(f"  ✓ Receipt Secret: {job_data.get('receipt_secret', '')[:16]}...")
    except Exception as e:
        print(f"  ! Running against local fixture: job_01JB0000000000000000000001")
        job_id = "job_01JB0000000000000000000001"

    # 4. Stream progress
    print(f"\n[4] Streaming live events for Job {job_id}...")
    print("  -> Intake -> Parsing -> Lineage Discovery -> Retention Hold -> Targeted Erasure -> Audit -> Proof -> Anchor")

    print("\n" + "=" * 70)
    print(f"Scenario '{scenario_key}' ready for presentation.")
    print("=" * 70)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="ZeroTrace Demo Director Scenario Runner")
    parser.add_argument(
        "--scenario",
        choices=["golden", "ghost_heal", "retention_hold"],
        default="golden",
        help="Demo scenario to run"
    )
    args = parser.parse_args()
    run_scenario(args.scenario)

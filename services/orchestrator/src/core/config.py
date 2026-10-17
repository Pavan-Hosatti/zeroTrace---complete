"""
ZeroTrace Orchestrator Configuration.
Environment-driven settings with 12-factor compliance.
"""

from __future__ import annotations
import os
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_prefix="ZT_",
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

    # Server
    ENV: str = "development"
    DEBUG: bool = True
    PORT: int = 8001
    HOST: str = "0.0.0.0"
    CORS_ORIGINS: List[str] = ["http://localhost:3000", "http://localhost:5173", "http://localhost:8001", "https://app.zerotrace.dev", "*"]
    SERVICE_KEY: str = "dev-service-key"
    JWT_SECRET: str = "zerotrace-demo-jwt-secret-key-must-be-at-least-32-bytes-long"
    PEPPER_SECRET: str = "zerotrace-pseudonym-hmac-pepper-secret-key-32-bytes"

    # Databases
    DATABASE_URL: str = "sqlite+aiosqlite:///./zerotrace_app.db"
    REDIS_URL: str = "redis://localhost:6379/1"  # db1 for event bus & queue

    # Data Plane upstream
    DATAPLANE_URL: str = "http://localhost:8002"

    # AI / External Services
    SARVAM_API_KEY: str = "mock-sarvam-key"
    SARVAM_ENDPOINT: str = "https://api.sarvam.ai/speech-to-text"
    GEMMA_MODEL_ID: str = "gemma-2-9b-it"
    GEMMA_API_BASE: str = "http://localhost:11434/v1"
    ENABLE_OFFLINE_FALLBACK: bool = True

    # Cryptography & Proof
    SIGNER_PRIVATE_KEY: str = "9d61b19deffd5a60ba844af492ec2cc44449c5697b326919703bac031cae7f60"
    POLICY_VERSION: str = "dpdp-2023-v1.4"

    # Blockchain Anchor
    ANCHOR_PROVIDER: str = "local"  # "shiprite" | "evm" | "local"
    SHIPRITE_API_KEY: str = "mock-shiprite-key"
    SHIPRITE_ENDPOINT: str = "https://api.shiprite.io/v1/anchor"
    EVM_RPC_URL: str = "http://localhost:8545"
    EVM_CONTRACT_ADDRESS: str = "0x742d35Cc6634C0532925a3b844Bc454e4438f44e"


settings = Settings()

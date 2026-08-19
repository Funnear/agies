"""API Key Authentication, Tiering, and Rate-Limiting Engine."""

from datetime import datetime, timezone
import os
import secrets
import time
from typing import Dict, Optional
from fastapi import HTTPException, Security, status
from fastapi.security.api_key import APIKeyHeader
from pydantic import BaseModel

API_KEY_HEADER = APIKeyHeader(name="X-API-Key", auto_error=False)


class APIKeyInfo(BaseModel):
    """Metadata for an issued API key."""

    key: str
    owner: str
    tier: str = "standard"  # standard, pro, admin
    created_at: datetime
    is_active: bool = True
    rate_limit_rpm: int = 60  # requests per minute


class APIKeyManager:
    """In-memory and environment-backed API key manager with sliding-window rate limiting."""

    def __init__(self):
        self._keys: Dict[str, APIKeyInfo] = {}
        self._request_timestamps: Dict[str, list[float]] = {}

        # Initialize default master/admin key from env or generate a deterministic default
        master_key = os.environ.get("AGIES_MASTER_API_KEY", "agies_dev_master_key_999")
        self.register_key(
            key=master_key,
            owner="AGIES System Administrator",
            tier="admin",
            rate_limit_rpm=1000,
        )

        # Standard dev key for instant testing
        self.register_key(
            key="agies_test_key_123",
            owner="Developer Sandbox",
            tier="standard",
            rate_limit_rpm=60,
        )

    def register_key(
        self,
        key: Optional[str] = None,
        owner: str = "Anonymous User",
        tier: str = "standard",
        rate_limit_rpm: int = 60,
    ) -> APIKeyInfo:
        """Issue or register a new API key."""
        generated_key = key or f"agies_{tier}_{secrets.token_hex(16)}"
        info = APIKeyInfo(
            key=generated_key,
            owner=owner,
            tier=tier,
            created_at=datetime.now(timezone.utc),
            is_active=True,
            rate_limit_rpm=rate_limit_rpm,
        )
        self._keys[generated_key] = info
        return info

    def revoke_key(self, key: str) -> bool:
        """Revoke an existing API key."""
        if key in self._keys:
            self._keys[key].is_active = False
            return True
        return False

    def validate_key(self, api_key: str) -> Optional[APIKeyInfo]:
        """Validate key existence and active status."""
        key_info = self._keys.get(api_key)
        if key_info and key_info.is_active:
            return key_info
        return None

    def check_rate_limit(self, key_info: APIKeyInfo) -> bool:
        """Enforce rate limits per minute per API key."""
        now = time.time()
        window_start = now - 60.0
        timestamps = self._request_timestamps.setdefault(key_info.key, [])

        # Filter out timestamps older than 60 seconds
        timestamps = [t for t in timestamps if t > window_start]
        self._request_timestamps[key_info.key] = timestamps

        if len(timestamps) >= key_info.rate_limit_rpm:
            return False

        timestamps.append(now)
        return True


# Global Key Manager Singleton
key_manager = APIKeyManager()


async def get_api_key(api_key: Optional[str] = Security(API_KEY_HEADER)) -> APIKeyInfo:
    """FastAPI Dependency for authenticating requests via X-API-Key header."""
    if not api_key:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Missing API Key. Please provide the 'X-API-Key' header.",
            headers={"WWW-Authenticate": "ApiKey"},
        )

    key_info = key_manager.validate_key(api_key)
    if not key_info:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Invalid or revoked API Key.",
        )

    if not key_manager.check_rate_limit(key_info):
        raise HTTPException(
            status_code=status.HTTP_429_TOO_MANY_REQUESTS,
            detail=f"Rate limit exceeded for tier '{key_info.tier}' ({key_info.rate_limit_rpm} req/min).",
        )

    return key_info


async def require_admin(key_info: APIKeyInfo = Security(get_api_key)) -> APIKeyInfo:
    """Dependency requiring admin tier privileges."""
    if key_info.tier != "admin":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Administrative privileges required for this endpoint.",
        )
    return key_info

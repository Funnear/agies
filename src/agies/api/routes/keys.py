"""API Key Management Router (Admin Protected)."""

from typing import Optional
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel, Field

from agies.api.auth import APIKeyInfo, key_manager, require_admin

router = APIRouter(prefix="/keys", tags=["API Key Management"])


class KeyIssueRequest(BaseModel):
    owner: str = Field(..., description="Developer or organization name")
    tier: str = Field("standard", description="Access tier (standard, pro, admin)")
    rate_limit_rpm: Optional[int] = Field(
        None, description="Custom requests-per-minute limit"
    )


@router.post(
    "/issue", response_model=APIKeyInfo, summary="Issue a new API key (Admin only)"
)
async def issue_key(
    req: KeyIssueRequest,
    admin_key: APIKeyInfo = Depends(require_admin),
):
    """Issue a new API access key with custom tier and rate limits."""
    rpm = req.rate_limit_rpm or (
        300 if req.tier == "pro" else 1000 if req.tier == "admin" else 60
    )
    info = key_manager.register_key(
        owner=req.owner,
        tier=req.tier,
        rate_limit_rpm=rpm,
    )
    return info


@router.delete("/revoke/{key_to_revoke}", summary="Revoke an API key (Admin only)")
async def revoke_key(
    key_to_revoke: str,
    admin_key: APIKeyInfo = Depends(require_admin),
):
    """Revoke access for an existing API key."""
    success = key_manager.revoke_key(key_to_revoke)
    if not success:
        raise HTTPException(status_code=404, detail="API key not found.")
    return {"message": "API key successfully revoked.", "key": key_to_revoke}

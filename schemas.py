"""Pydantic schemas for GoTo Meeting Connector (GoTo REST API)."""
from __future__ import annotations
from typing import Any, Optional, List, Dict
from pydantic import BaseModel, Field

class NoParams(BaseModel):
    """Empty parameter model."""
    pass

class ConnectGoToParams(BaseModel):
    label: str = Field(default="", description="Friendly connection label, e.g. Acme GoTo.")
    access_token: str = Field(..., description="GoTo OAuth 2.0 Bearer Access Token.")

class DisconnectGoToParams(BaseModel):
    connection_id: str = Field(..., description="Connection ID to remove.")

class ListMeetingsParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")
    historical: bool = Field(default=False, description="Whether to include past/historical meetings.")

class GetMeetingParams(BaseModel):
    meeting_id: int = Field(..., description="Numeric GoTo meeting ID.")
    connection_id: str = Field(default="", description="Optional connection ID.")

class CreateMeetingParams(BaseModel):
    subject: str = Field(..., description="Meeting subject/topic.")
    start_time: str = Field(..., description="Start time (ISO 8601 UTC string, e.g. 2026-09-04T10:00:00Z).")
    end_time: str = Field(..., description="End time (ISO 8601 UTC string, e.g. 2026-09-04T11:00:00Z).")
    password_required: bool = Field(default=False, description="Require meeting password.")
    conference_call_info: str = Field(default="Hybrid", description="VoIP, Free, Hybrid, Private.")
    connection_id: str = Field(default="", description="Optional connection ID.")

class DeleteMeetingParams(BaseModel):
    meeting_id: int = Field(..., description="Numeric GoTo meeting ID.")
    connection_id: str = Field(default="", description="Optional connection ID.")

class AuditHealthParams(BaseModel):
    connection_id: str = Field(default="", description="Optional connection ID.")

# Return shape models
class GoToConnection(BaseModel):
    id: str = Field(..., description="Connection ID")
    label: str = Field(..., description="Connection label")
    created_at: str = Field(..., description="Connection timestamp")

class ConnectionList(BaseModel):
    connections: List[GoToConnection] = Field(default_factory=list)
    total: int = Field(default=0)

class ConnectResult(BaseModel):
    id: str = Field(..., description="Connection ID")
    label: str = Field(..., description="Connection label")
    status: str = Field(default="connected", description="Connection status")

class DeleteResult(BaseModel):
    status: str = Field(..., description="Status")
    meeting_id: Optional[int] = Field(default=None, description="Deleted meeting ID")

class MeetingRecord(BaseModel):
    meeting_id: int = Field(..., description="Numeric meeting ID")
    subject: str = Field(..., description="Meeting subject")
    start_time: Optional[str] = Field(default=None, description="Start time")
    end_time: Optional[str] = Field(default=None, description="End time")
    join_url: Optional[str] = Field(default=None, description="Join URL")

class MeetingList(BaseModel):
    meetings: List[Dict[str, Any]] = Field(default_factory=list)
    count: int = Field(default=0)

class HealthAuditResult(BaseModel):
    status: str = Field(..., description="Status: healthy, degraded, or error")
    user: str = Field(default="Unknown", description="GoTo user or account")
    meetings_count: int = Field(default=0, description="Active meetings count")
    summary: str = Field(..., description="Human-readable health summary")

"""Resource operation handlers for GoTo Meeting Connector."""
from __future__ import annotations
from typing import Any
from imperal_sdk import ActionResult
from app import chat
from handlers_connection import resolve_client
from schemas import (
    ListMeetingsParams, GetMeetingParams, CreateMeetingParams,
    DeleteMeetingParams, AuditHealthParams, MeetingRecord,
    MeetingList, DeleteResult, HealthAuditResult
)

@chat.function(
    "list_meetings",
    "List scheduled or historical GoTo meetings.",
    action_type="read",
    chain_callable=True,
    data_model=MeetingList
)
async def list_meetings(ctx, params: ListMeetingsParams) -> ActionResult:
    """List scheduled or historical GoTo meetings."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        meetings = await client.list_meetings(historical=params.historical)
        return ActionResult.ok({"meetings": meetings, "count": len(meetings)}, summary=f"Found {len(meetings)} GoTo meeting(s).")
    except Exception as e:
        return ActionResult.error(f"Error listing meetings: {e}")

@chat.function(
    "get_meeting",
    "Get details of a specific GoTo meeting by ID.",
    action_type="read",
    chain_callable=True,
    data_model=MeetingRecord
)
async def get_meeting(ctx, params: GetMeetingParams) -> ActionResult:
    """Get details of a specific GoTo meeting."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        meeting = await client.get_meeting(meeting_id=params.meeting_id)
        return ActionResult.ok(
            {
                "meeting_id": params.meeting_id,
                "subject": meeting.get("subject", "Meeting"),
                "start_time": meeting.get("startTime") or meeting.get("starttime"),
                "end_time": meeting.get("endTime") or meeting.get("endtime"),
                "join_url": meeting.get("joinUrl") or meeting.get("joinURL")
            },
            summary=f"Retrieved meeting {params.meeting_id}: {meeting.get('subject', 'Meeting')}."
        )
    except Exception as e:
        return ActionResult.error(f"Error fetching meeting {params.meeting_id}: {e}")

@chat.function(
    "create_meeting",
    "Schedule a new GoTo meeting.",
    action_type="write",
    chain_callable=True,
    event="goto-meeting-connector.create_meeting",
    effects=["create:meeting"],
    data_model=MeetingRecord
)
async def create_meeting(ctx, params: CreateMeetingParams) -> ActionResult:
    """Schedule a new GoTo meeting."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        meeting = await client.create_meeting(
            subject=params.subject,
            start_time=params.start_time,
            end_time=params.end_time,
            password_required=params.password_required,
            conference_call_info=params.conference_call_info
        )
        mid = meeting.get("meetingid") or meeting.get("meetingId") or 0
        return ActionResult.ok(
            {
                "meeting_id": mid,
                "subject": params.subject,
                "start_time": params.start_time,
                "end_time": params.end_time,
                "join_url": meeting.get("joinURL") or meeting.get("joinUrl")
            },
            summary=f"Scheduled GoTo meeting '{params.subject}' with ID {mid}."
        )
    except Exception as e:
        return ActionResult.error(f"Error scheduling meeting: {e}")

@chat.function(
    "delete_meeting",
    "Delete a scheduled GoTo meeting.",
    action_type="write",
    chain_callable=True,
    event="goto-meeting-connector.delete_meeting",
    effects=["delete:meeting"],
    data_model=DeleteResult
)
async def delete_meeting(ctx, params: DeleteMeetingParams) -> ActionResult:
    """Delete a scheduled GoTo meeting."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        await client.delete_meeting(meeting_id=params.meeting_id)
        return ActionResult.ok({"status": "deleted", "meeting_id": params.meeting_id}, summary=f"Deleted GoTo meeting {params.meeting_id}.")
    except Exception as e:
        return ActionResult.error(f"Error deleting meeting: {e}")

@chat.function(
    "audit_goto_health",
    "Audit GoTo Meeting connectivity and active meetings count.",
    action_type="read",
    chain_callable=True,
    data_model=HealthAuditResult
)
async def audit_goto_health(ctx, params: AuditHealthParams) -> ActionResult:
    """Audit GoTo Meeting health and connectivity."""
    client = await resolve_client(ctx, params.connection_id)
    try:
        meetings = await client.list_meetings(historical=False)
        return ActionResult.ok(
            {
                "status": "healthy",
                "user": "Connected Organizer",
                "meetings_count": len(meetings),
                "summary": f"Connection verified. {len(meetings)} active scheduled meeting(s)."
            },
            summary=f"GoTo Meeting health verified. {len(meetings)} active meetings."
        )
    except Exception as e:
        return ActionResult.ok(
            {
                "status": "degraded",
                "user": "Unknown",
                "meetings_count": 0,
                "summary": f"Health check failed: {e}"
            },
            summary=f"GoTo Meeting health audit failed: {e}"
        )

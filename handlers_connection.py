"""Connection lifecycle handlers for GoTo Meeting Connector."""
from __future__ import annotations
import json, uuid, datetime
from imperal_sdk import ActionResult
from app import chat
from schemas import (
    ConnectGoToParams, DisconnectGoToParams, NoParams,
    ConnectionList, GoToConnection, ConnectResult, DeleteResult
)
from goto_meeting_client import GoToMeetingClient

SECRET_KEY = "goto_meeting_connections"

async def _load_connections(ctx) -> list[dict]:
    raw = await ctx.secrets.get(SECRET_KEY)
    if not raw:
        return []
    try:
        return json.loads(raw)
    except Exception:
        return []

async def _save_connections(ctx, connections: list[dict]) -> None:
    await ctx.secrets.set(SECRET_KEY, json.dumps(connections))

async def resolve_client(ctx, connection_id: str = "") -> GoToMeetingClient:
    connections = await _load_connections(ctx)
    if not connections:
        raise ValueError("No GoTo Meeting connections found. Please connect an account first.")
    if connection_id:
        for c in connections:
            if c.get("id") == connection_id:
                return GoToMeetingClient(access_token=c["access_token"])
        raise ValueError(f"Connection ID {connection_id} not found.")
    c = connections[0]
    return GoToMeetingClient(access_token=c["access_token"])

@chat.function(
    "connect_goto_meeting",
    "Connect your own GoTo Meeting account by saving your OAuth Access Token.",
    action_type="write",
    chain_callable=True,
    event="goto-meeting-connector.connect_goto_meeting",
    effects=["create:connection"],
    data_model=ConnectResult
)
async def connect_goto_meeting(ctx, params: ConnectGoToParams) -> ActionResult:
    """Connect a GoTo Meeting account after verifying OAuth token."""
    client = GoToMeetingClient(access_token=params.access_token)
    try:
        await client.get_user()
    except Exception as e:
        return ActionResult.error(f"Failed to authenticate with GoTo Meeting: {e}")

    conn_id = f"goto_{uuid.uuid4().hex[:8]}"
    label = params.label.strip() or "GoTo Meeting Account"
    created_at = datetime.datetime.now(datetime.timezone.utc).isoformat()
    connections = await _load_connections(ctx)
    connections.append({
        "id": conn_id,
        "label": label,
        "access_token": params.access_token,
        "created_at": created_at
    })
    await _save_connections(ctx, connections)

    return ActionResult.ok(
        {"id": conn_id, "label": label, "status": "connected"},
        summary=f"Successfully connected GoTo Meeting account '{label}'."
    )

@chat.function(
    "list_connections",
    "List connected GoTo Meeting accounts without exposing credentials.",
    action_type="read",
    chain_callable=True,
    data_model=ConnectionList
)
async def list_connections(ctx, params: NoParams) -> ActionResult:
    """List connected GoTo Meeting accounts."""
    conns = await _load_connections(ctx)
    records = [
        {"id": c.get("id", ""), "label": c.get("label", ""), "created_at": c.get("created_at", "")}
        for c in conns
    ]
    return ActionResult.ok(
        {"connections": records, "total": len(records)},
        summary=f"Found {len(records)} connected GoTo Meeting account(s)."
    )

@chat.function(
    "disconnect_goto_meeting",
    "Disconnect a GoTo Meeting account.",
    action_type="write",
    chain_callable=True,
    event="goto-meeting-connector.disconnect_goto_meeting",
    effects=["delete:connection"],
    data_model=DeleteResult
)
async def disconnect_goto_meeting(ctx, params: DisconnectGoToParams) -> ActionResult:
    """Disconnect a GoTo Meeting connection."""
    connections = await _load_connections(ctx)
    initial_len = len(connections)
    connections = [c for c in connections if c.get("id") != params.connection_id]
    if len(connections) == initial_len:
        return ActionResult.error(f"Connection {params.connection_id} not found.")
    await _save_connections(ctx, connections)
    return ActionResult.ok(
        {"status": "disconnected", "meeting_id": None},
        summary=f"GoTo Meeting connection {params.connection_id} disconnected."
    )

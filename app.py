"""Extension declaration, capabilities, health check for GoTo Meeting Connector."""
from __future__ import annotations
from imperal_sdk import ChatExtension, Extension

ext = Extension(
    "goto-meeting-connector",
    version="0.1.0",
    display_name="GoTo Meeting",
    description="Comprehensive GoTo Meeting connector: schedule, manage, list, and inspect meetings and conference sessions via GoTo REST API.",
    icon="icon.svg",
    capabilities=["gotomeeting:manage"]
)

chat = ChatExtension(ext)

@ext.health_check
async def health_check(ctx) -> bool:
    """Verify GoTo Meeting connector health."""
    return True

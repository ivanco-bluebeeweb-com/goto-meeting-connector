"""Panel UI for GoTo Meeting Connector."""
from __future__ import annotations
from imperal_sdk import ui
from app import ext
import handlers_connection as h

def _settings_button() -> ui.UINode:
    return ui.Button(
        "App settings",
        variant="secondary",
        size="sm",
        icon="settings",
        on_click=ui.Call("__goto_meeting_settings")
    )

def _help_modal() -> ui.UINode:
    return ui.Modal(
        trigger=ui.Button("How do I set this up?", variant="ghost", size="sm"),
        title="Connecting GoTo Meeting",
        children=[
            ui.Text(
                "1. Sign in to GoTo Developer Center and create an OAuth 2.0 Client.\n"
                "2. Generate an OAuth Bearer access token with meetings permissions.\n"
                "3. Enter a label and paste your token below, then click Connect GoTo Meeting.",
                variant="body"
            )
        ]
    )

@ext.panel("goto_meeting_sidebar", slot="left")
async def goto_meeting_sidebar(ctx, **kwargs) -> ui.UINode:
    connections = await h._load_connections(ctx)
    conn_items = [
        ui.Text(c.get("label") or "GoTo Account", variant="body")
        for c in connections
    ] if connections else [ui.Text("No GoTo Meeting accounts connected yet.", variant="caption")]

    return ui.Stack(
        direction="v",
        gap=3,
        children=[
            ui.Text("GoTo Meeting", variant="heading"),
            ui.Stack(direction="v", gap=1, children=conn_items),
            ui.Divider(),
            ui.Form(
                submit_label="Connect GoTo Meeting",
                action=ui.Call("connect_goto_meeting"),
                children=[
                    ui.Stack(
                        direction="v",
                        gap=2,
                        children=[
                            ui.Stack(
                                direction="v",
                                gap=1,
                                children=[
                                    ui.Text("Connection Label", variant="caption"),
                                    ui.Input(placeholder="e.g. Sales GoTo", param_name="label")
                                ]
                            ),
                            ui.Stack(
                                direction="v",
                                gap=1,
                                children=[
                                    ui.Text("OAuth Bearer Access Token", variant="caption"),
                                    ui.Input(placeholder="OAuth Bearer Token", param_name="access_token")
                                ]
                            )
                        ]
                    )
                ]
            ),
            ui.Divider(),
            ui.Stack(
                direction="h",
                gap=2,
                children=[
                    _help_modal(),
                    _settings_button()
                ]
            )
        ]
    )

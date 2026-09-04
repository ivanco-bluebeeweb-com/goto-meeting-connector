"""GoTo Meeting REST API client."""
from __future__ import annotations
import httpx
from typing import Any, Dict, List, Optional

class GoToMeetingClient:
    def __init__(self, access_token: str):
        self.base_url = "https://api.getgo.com/G2M/rest"
        self.headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

    async def get_user(self) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.base_url}/organizers", headers=self.headers, timeout=15.0)
            res.raise_for_status()
            data = res.json()
            if isinstance(data, list) and data:
                return data[0]
            return {"status": "ok"}

    async def list_meetings(self, historical: bool = False) -> List[Dict[str, Any]]:
        endpoint = "historicalMeetings" if historical else "meetings"
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.base_url}/{endpoint}", headers=self.headers, timeout=15.0)
            res.raise_for_status()
            data = res.json()
            return data if isinstance(data, list) else []

    async def get_meeting(self, meeting_id: int) -> Dict[str, Any]:
        async with httpx.AsyncClient() as client:
            res = await client.get(f"{self.base_url}/meetings/{meeting_id}", headers=self.headers, timeout=15.0)
            res.raise_for_status()
            data = res.json()
            if isinstance(data, list) and data:
                return data[0]
            return data if isinstance(data, dict) else {}

    async def create_meeting(self, subject: str, start_time: str, end_time: str, password_required: bool = False, conference_call_info: str = "Hybrid") -> Dict[str, Any]:
        payload = {
            "subject": subject,
            "starttime": start_time,
            "endtime": end_time,
            "passwordrequired": password_required,
            "conferencecallinfo": conference_call_info,
            "meetingtype": "scheduled"
        }
        async with httpx.AsyncClient() as client:
            res = await client.post(f"{self.base_url}/meetings", headers=self.headers, json=payload, timeout=15.0)
            res.raise_for_status()
            data = res.json()
            if isinstance(data, list) and data:
                return data[0]
            return data if isinstance(data, dict) else {}

    async def delete_meeting(self, meeting_id: int) -> None:
        async with httpx.AsyncClient() as client:
            res = await client.delete(f"{self.base_url}/meetings/{meeting_id}", headers=self.headers, timeout=15.0)
            res.raise_for_status()

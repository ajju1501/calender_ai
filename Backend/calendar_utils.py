from google.oauth2 import service_account
from googleapiclient.discovery import build
import os
import json

# Load service account JSON from environment variable
service_account_info = json.loads(os.environ["GOOGLE_APPLICATION_CREDENTIALS_JSON"])

# Define calendar scope
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Calendar ID from env variable
CALENDAR_ID = os.environ["CALENDAR_ID"]

# Authenticate
credentials = service_account.Credentials.from_service_account_info(
    service_account_info, scopes=SCOPES
)

# Build service
service = build("calendar", "v3", credentials=credentials)

# Create event
def create_event(start_time, end_time, summary):
    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
    }
    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"✅ Event created: {created_event.get('htmlLink')}"

# Get available slots (customize as needed)
def get_free_slots(date_str):
    return "🕒 You can choose any time tomorrow between 10 AM to 6 PM."

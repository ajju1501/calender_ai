from google.oauth2 import service_account
from googleapiclient.discovery import build
import os

# Use your own service account credentials file path
SERVICE_ACCOUNT_FILE = "E:\Internship\Tailor_talk\Backend\peak-axiom-465016-m3-cea1d1a0f6bd.json"
SCOPES = ["https://www.googleapis.com/auth/calendar"]

# Replace with your test calendar ID (usually ends with @group.calendar.google.com)
CALENDAR_ID = "319764cd0aa45e08ac7336c45ee39c7690fc95ab0d70968cffb0ad82bf86896c@group.calendar.google.com"

credentials = service_account.Credentials.from_service_account_file(
    SERVICE_ACCOUNT_FILE, scopes=SCOPES
)

service = build("calendar", "v3", credentials=credentials)

def create_event(start_time, end_time, summary):
    event = {
        "summary": summary,
        "start": {"dateTime": start_time, "timeZone": "Asia/Kolkata"},
        "end": {"dateTime": end_time, "timeZone": "Asia/Kolkata"},
    }

    created_event = service.events().insert(calendarId=CALENDAR_ID, body=event).execute()
    return f"✅ Event created: {created_event.get('htmlLink')}"

def get_free_slots(date_str):
    # Optional: Implement availability check here
    return "🕒 You can choose any time tomorrow between 10 AM to 6 PM."

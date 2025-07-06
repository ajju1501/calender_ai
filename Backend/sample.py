from calendar_utils import create_event

# Set sample times (RFC 3339 format)
start_time = "2025-07-07T16:00:00+05:30"
end_time = "2025-07-07T17:00:00+05:30"
summary = "Test Appointment"

print(create_event(start_time, end_time, summary))
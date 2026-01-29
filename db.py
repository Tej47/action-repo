from pymongo import MongoClient, ASCENDING
from datetime import datetime, timezone
import os
from dateutil import parser

#MongoDB Connection
MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")

client = MongoClient(MONGO_URI)
db=client["github_events"]
events = db["events"]

#Indexes
#Preventing duplicate webhook events
events.create_index([("request_id", ASCENDING)], unique=True)

#Optimize timebased queries
events.create_index([("timestamp", ASCENDING)])

ALLOWED_ACTIONS = {"PUSH", "PULL_REQUEST", "MERGE"}

def validate_event_payload(payload: dict):
    required_fields = {
        "request_id": str,
        "author": str,
        "action": str,
        "from_branch": str,
        "to_branch": str,
        "timestamp": str
    }

    for field, field_type in required_fields.items():
        if field not in payload:
            raise ValueError(f"Missing required field: {field}")
        if not isinstance(payload[field], field_type):
            raise TypeError(f"{field} must be of type {field_type.__name__}")
    if payload["action"] not in ALLOWED_ACTIONS:
        raise ValueError("Invalid action type")

#Validate timestamp format
    try:
        parser.isoparse(payload["timestamp"])
    except Exception:
        raise ValueError("Invalid timestamp format (must be ISO 8601 UTC)")    
        
def get_utc_timestamp():
    """
    Returns ISO 8601 UTC timestamp string
    """
    return datetime.now(timezone.utc).isoformat()

#Insert Event
def insert_event(event_data: dict):
    validate_event_payload(event_data)
    try:
        events.insert_one(event_data)
    except Exception as e:
        raise RuntimeError(f"Database insert failed: {str(e)}")
    
def fetch_events_since(timestamp_iso: str):
    return list(events.find(
        {"timestamp": {"$gt": timestamp_iso}},
        {"_id": 0}
    ).sort("timestamp", ASCENDING))    


#xplain the process of changes in timestamp
#doubts in fetch
from datetime import datetime
# import uuid
from flask import jsonify
from db import get_utc_timestamp, events, insert_event

def handle_pull_request(payload):
    pull_request = payload.get("pull_request")

    if not pull_request:
        return jsonify({"error": "Invalid pull request payload"}), 400
    
    is_merged = pull_request.get("merged", False)

    action_type = "MERGE" if is_merged else "PULL_REQUEST"

    data = {
        "request_id": str(pull_request.get("id")),
        "author": pull_request["user"]["login"],
        "action": action_type,
        "from_branch": pull_request["head"]["ref"],
        "to_branch": pull_request["base"]["ref"],
        "timestamp": get_utc_timestamp()
    }

    if events.find_one({"request_id":data["request_id"], "action": data["action"]}):
        return jsonify({"duplicate": True}), 200
    
    insert_event(data)

    return jsonify({"stored": True, "type": action_type}), 201

#why check find one with both requestid and action but not just request id
# Why include action here?
# Because:
# Same PR ID can generate PULL_REQUEST
# Later generate MERGE
# This avoids:
# Losing valid MERGE events
# Double inserts of same event

#example for pull_request that we use get on
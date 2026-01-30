from datetime import datetime
from flask import jsonify
from db import get_utc_timestamp, events, insert_event

def handle_pull_request(payload):
    action = payload.get("action")
    pull_request = payload.get("pull_request")

    if not pull_request:
        return jsonify({"ignored": True}), 200

    # Only check for opened PRs and merged PRs
    if action not in ["opened", "closed"]:
        return jsonify({"ignored": True}), 200

    is_merged = pull_request.get("merged", False)

    if action == "closed" and not is_merged:
        return jsonify({"ignored": "pr closed without merge"}), 200

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

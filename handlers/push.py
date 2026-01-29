from flask import jsonify
from db import events, get_utc_timestamp, insert_event
from datetime import datetime
# import uuid

def handle_push(payload):
    commit_hash = payload["head_commit"]["id"]

    data = {
        "request_id": commit_hash,
        "author": payload["pusher"]["name"],
        "action": "PUSH",
        "from_branch": "",
        "to_branch": payload["ref"].split("/")[-1],
        "timestamp": get_utc_timestamp()
    }

    if events.find_one({"request_id": data["request_id"]}):
        return jsonify({"duplicate":True}), 200
    insert_event(data)
    return jsonify({"stored": True}), 201

#commit hash 
#do we need events.find_one
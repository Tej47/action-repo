from flask import Flask, jsonify, request, render_template
from flask_cors import CORS
from datetime import datetime
from db import events
from handlers.push import handle_push
from handlers.pull_request import handle_pull_request
#push2 testing

app = Flask(__name__)
CORS(app)

@app.route("/health", methods=["GET"])
def health_check():
    """
    Docstring for health_check
    """
    return jsonify({"status": "running"}), 200


@app.route("/webhook", methods=["POST"])
def github_webhook():
    event_type = request.headers.get("X-GitHub-Event")
    payload = request.json

    if not event_type or not payload:
        return jsonify({"error": "Invalid payload"}), 400
    if event_type == "push":
        return handle_push(payload)
    elif event_type == "pull_request":
        return handle_pull_request(payload)
    return jsonify({"ignored": True}), 200



@app.route("/events", methods=["GET"])
def fetch_events():
    since = request.args.get("since")
    query={}
    if since:
        try:
            query["timestamp"]={
                "$gt": since
            }
        except Exception:
            return jsonify({"error": "invalid timestamp"}), 400
    events_list= list(
        events.find(query, {"_id":0}).sort("timestamp", 1)
    )
    return jsonify(events_list), 200

#why is query empty and how do we get "timestamp"
#what is $gt
#query, {"_id":0})

@app.route("/")
def home():
    return render_template("index.html")



if __name__=="__main__":
    app.run(debug=True, port=5000)

#x-github-event
# where did we link the repo     
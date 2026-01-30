Webhook Trigger Repository
This repository exists solely to act as a data source for the webhook-repo project. It contains no production code, only dummy files used to trigger GitHub Webhook events.

Purpose
Whenever a git push or Pull Request is performed on this repository, GitHub is configured to send a POST payload to a remote Flask server.

Webhook Configuration
Payload URL: (Configured via ngrok/deployed URL)

Content type: application/json

Events: Push, Pull requests

How to Trigger Events
Edit demo1.txt or any other demo#.txt and push to main.

Create a new branch, push changes, and open a Pull Request.

Merge the Pull Request to see the 'Merge' status in the monitor UI.

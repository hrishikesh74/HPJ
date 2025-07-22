import os
from flask import Flask, request
from slack_sdk import WebClient
from slack_sdk.errors import SlackApiError
from dotenv import load_dotenv

# Load .env file
load_dotenv()

SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
PORT = int(os.getenv("PORT", 5000))

client = WebClient(token=SLACK_BOT_TOKEN)
app = Flask(__name__)

@app.route("/slack/events", methods=["POST"])
def slack_events():
    data = request.json

    # URL Verification (needed when setting up the app)
    if data.get("type") == "url_verification":
        return data.get("challenge")

    # Handle message
    if "event" in data:
        event = data["event"]
        if event.get("type") == "message" and "hello" in event.get("text", "").lower():
            try:
                client.chat_postMessage(
                    channel=event["channel"],
                    text="👋 Hello! I'm your friendly bot."
                )
            except SlackApiError as e:
                print(f"Slack API error: {e.response['error']}")

    return "", 200

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=PORT)

This is a new line

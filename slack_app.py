import os
from slack_bolt import App
from slack_bolt.adapter.socket_mode import SocketModeHandler
import logging
import requests
import json

logging.basicConfig(level=logging.DEBUG)

# Install the Slack app and get xoxb- token in advance
app = App(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("message")
def say_hello(event, say):
    logging.debug("got message")
    r = requests.post("http://localhost:5005/webhooks/rest/webhook",json={"sender":"test","message":event["text"]})
    json_data = json.loads(r.text)[0]
    say(f"{json_data['text']}")


# Add middleware / listeners here

if __name__ == "__main__":
    # export SLACK_APP_TOKEN=xapp-***
    # export SLACK_BOT_TOKEN=xoxb-***
    handler = SocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    handler.start()

import os
# from slack_bolt import App
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
import logging
import requests
import json
import aiohttp
import sqlite_db as sdb

logging.basicConfig(level=logging.DEBUG)

# Install the Slack app and get xoxb- token in advance
app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

@app.event("message")
async def say_hello(event, say):
    logging.debug("got message")
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:5005/webhooks/rest/webhook',json={"sender":event['user'],"message":event["text"]}) as response:
            
    # r = await requests.post("http://localhost:5005/webhooks/rest/webhook",json={"sender":event['user'],"message":event["text"]})
            json_data = json.loads(await response.text())[0]
            db = await sdb.get_db_object()
            await db.execute(f"insert into events values ('{event['user']}','{event['text']}','{json_data['text']}')")
            await db.commit()

            await say(f"{json_data['text']}")


# Add middleware / listeners here
async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()


if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main())

    # asyncio.run(main())

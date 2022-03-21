import os
# from slack_bolt import App
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
import logging
import requests
import json
import aiohttp
import sqlite_db as sdb
from datetime import datetime

logging.basicConfig(level=logging.ERROR)

# Install the Slack app and get xoxb- token in advance
app = AsyncApp(token=os.environ["SLACK_BOT_TOKEN"])

@app.event({
    "type":"message",
    "subtype": None
})
async def say_hello(event, say, context):
    # logging.error("\n\n\n\n\n\n\ngot message")
    async with aiohttp.ClientSession() as session:
        async with session.post('http://localhost:5005/webhooks/rest/webhook',json={"sender":event['user'],"message":event["text"]}) as response:
            
    # r = await requests.post("http://localhost:5005/webhooks/rest/webhook",json={"sender":event['user'],"message":event["text"]})
            token = context.bot_token
            channel = event['user']
            logging.error(channel)
            text = "typing... "
            resp = await app.client.chat_postMessage(
                token=token, 
                channel=channel,
                text=text
            )
            # logging.error("\n\n\n\n\n\n\n\n\n\n\n\n")
            # print(dir(resp))
            ts = resp['message']['ts']
            logging.error(ts)
            # resp = event.chat_postMessage()
            json_data = json.loads(await response.text())[0]
            db = await sdb.get_db_object()
            query="""
            insert into events values (?,?,?,?)
            """
            await db.execute(query, (event['user'],event['text'],json_data['text'],datetime.now()))
            await db.commit()

            text = json_data['text']
            channel = resp['channel']

            time_to_sleep = len(text)*0.01
            await asyncio.sleep(time_to_sleep+0.5)

            await app.client.chat_update(
                token=token,
                channel=channel,
                ts=ts,
                text=text
            )



# Add middleware / listeners here
async def main():
    handler = AsyncSocketModeHandler(app, os.environ["SLACK_APP_TOKEN"])
    await handler.start_async()


if __name__ == "__main__":
    import asyncio
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(main())

    # asyncio.run(main())

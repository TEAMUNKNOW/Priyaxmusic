from lexica import Client
from pyrogram import filters
from DAXXMUSIC import app




def main(prompt: str) -> str:
    client = Client()
    response = client.palm(prompt)
    return response["content"].strip()

@app.on_message(filters.regex(r"Yumi|yumi|baby|Baby"))
async def deepchat(app: app, message):
    if message.reply_to_message:
        query = message.text.split(' ', 1)[1]
        x = main(query)
        await message.reply(x)
    else:
        query = message.text.split(' ', 1)[1]
        x = main(query)
        await message.reply(x)

from OpsAi import Ai
from asyncio import sleep as rest 
from datetime import datetime 
from DAXXMUSIC import app
from pyrogram import filters


@app.on_message(filters.command("ask", "ai"))
async def ai_bot(_, message):
     if message.reply_to_message:
      queri = message.reply_to_message.text
      gonb = Ai(query=queri)
      await message.reply(gonb.chat())
     elif len(message.command) == 1:
      return await message.reply("ʜᴇʟʟᴏ! ɪ'ᴍ ʏᴏᴜʀ ғʀɪᴇɴᴅʟʏ ᴀɪ ᴀssɪsᴛᴀɴᴛ. \nʜᴏᴡ ᴄᴀɴ ɪ ʜᴇʟᴘ ʏᴏᴜ ᴛᴏᴅᴀʏ?")
     elif len(message.command) > 1:
      queri = message.text.split(None,1)[1]
     gonb = Ai(query=queri)
     x = Ai(query=queri)
     me = await message.reply_text("ᴘʀᴏᴄᴇssᴇs.....")
     await rest(2)
     mee = await me.edit_text("ᴀʟʟ ᴍᴏsᴛ ᴅᴏɴᴇ ʙᴀʙʏ....🖤")
     await mee.delete()
     await rest(1)
     await message.reply(gonb.chat())
     
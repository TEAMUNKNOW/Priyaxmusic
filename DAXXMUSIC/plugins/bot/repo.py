import requests
from requests import get
from DAXXMUSIC import app
from pyrogram import filters, enums 
from pyrogram.types import InputMediaPhoto
from config import BANNED_USERS
from aiohttp import ClientSession as cs
from json import loads
from bs4 import BeautifulSoup as BSP
from io import BytesIO
import re

@app.on_message(filters.command(["pic"], prefixes=["/", "!", "."]) & ~BANNED_USERS)
async def pinterest(_, message):
    chat_id = message.chat.id

    try:
        query = message.text.split(None, 1)[1]
    except:
        return await message.reply("ɢɪᴠᴇ ɪᴍᴀɢᴇ ɴᴀᴍᴇ ғᴏʀ sᴇᴀʀᴄʜ 🔍")

    try:
        images = get(f"https://pinterest-api-one.vercel.app/?q={query}").json()

        if not images or "images" not in images:
            raise Exception("No images found.")

        media_group = []
        count = 0

        msg = await message.reply(f"sᴄʀᴀᴘɪɴɢ ɪᴍᴀɢᴇs ғʀᴏᴍ ᴘɪɴᴛᴇʀᴇᴛs...")

        for url in images["images"][:6]:
            media_group.append(InputMediaPhoto(media=url))
            count += 1
            await msg.edit(f"=> ᴏᴡᴏ sᴄʀᴀᴘᴇᴅ ɪᴍᴀɢᴇs {count}")

        if media_group:
            await app.send_media_group(
                chat_id=chat_id,
                media=media_group,
                reply_to_message_id=message.id
            )
            return await msg.delete()
        else:
            raise Exception("No images found.")

    except Exception as e:
        await msg.delete()
        return await message.reply(f"ᴇʀʀᴏʀ : {e}")

        
pin_pattern = "(?:https\:\/\/pin.it\/\S\S\S\S\S\S\S\S\S)"      
async def scrap_pins(message):
    text = re.findall(pin_pattern, message.text)
    async with cs() as sess:
        msg = await message.reply("`Downloading...`", parse_mode=enums.ParseMode.MARKDOWN)
        resp = await sess.get(text[0])
        soup = BSP(await resp.text(), 'html.parser')
        try:
            data = soup.find('script', attrs={'data-test-id': 'video-snippet'})
            if data:
                tag = loads(data.string.strip())
                video = BytesIO(await (await sess.get(tag['contentUrl'])).read())
                thumb = BytesIO(await (await sess.get(tag['thumbnailUrl'])).read())
                video.name = tag['name'] if tag['name'] else "@YaaraOP"
                await msg.delete()
                await message.reply_video(video=video, caption=f"Uploaded By [{app.me.first_name}](https://t.me/{app.me.username})", thumb=thumb, supports_streaming=True, parse_mode=enums.ParseMode.MARKDOWN)
            else:
                data = soup.find('script', attrs={'data-test-id': 'leaf-snippet'})
                tag = loads(data.string.strip())
                photo = BytesIO(await (await sess.get(tag['image'])).read())
                await msg.delete()
                await message.reply_photo(photo=photo, caption=f"Uploaded By [{app.me.first_name}](https://t.me/{app.me.username})", parse_mode=enums.ParseMode.MARKDOWN)
        except KeyError:
            print("Key Error")
            
@app.on_message(filters.regex(r'\b(?:pin\.it|pinterest\.com)\b') & (filters.group | filters.private) & ~BANNED_USERS)
async def pin_download(_, message):
    await scrap_pins(message)
    
snap_pattern = "(?:https\:\/\/t.snapchat.com\/\S\S\S\S\S\S\S\S)"            
async def scrap_snaps(message):
    text = re.findall(snap_pattern, message.text)
    async with cs() as sess:
        msg = await message.reply("`Downloading...`", parse_mode=enums.ParseMode.MARKDOWN)
        resp = await sess.get(text[0])
        soup = BSP(await resp.text(), 'html.parser')
        tag = soup.findAll("script", attrs={'data-react-helmet':'true', 'type':'application/ld+json'})[0]
        data = loads(tag.string.strip())
        video = BytesIO(await (await sess.get(data['contentUrl'])).read())
        thumb = BytesIO(await (await sess.get(data['thumbnailUrl'])).read())
        video.name = data['name'] if data['name'] else "@YaaraOP"
        await msg.delete()
        await message.reply_video(video, caption=f"Uploaded By [{app.me.first_name}](https://t.me/{app.me.username})", thumb=thumb, parse_mode=enums.ParseMode.MARKDOWN)
           
@app.on_message(filters.regex("(?:https\:\/\/t.snapchat.com\/\S\S\S\S\S\S\S\S)") & (filters.group | filters.private) & ~BANNED_USERS)
async def snap_download(_, message):
    await scrap_snaps(message)

async def download_ig(query):
	url = "https://instagram-bulk-scraper-latest.p.rapidapi.com/media_download_from_url"
	payload = { "url": query}
	headers = {
	"content-type": "application/json",
	"X-RapidAPI-Key": "1852da1a0dmshb013cd0683d2903p12df7ajsnd5d070b1f894",
	"X-RapidAPI-Host": "instagram-bulk-scraper-latest.p.rapidapi.com"
	}
	response = requests.post(url, json=payload, headers=headers)
	return response.json()['data']

@app.on_message(filters.regex(r'https://www\.instagram\.com/reel/.*') & (filters.group | filters.private))
async def insta(client, message):
            			chat_id = message.chat.id
            			query = message.text
            			data = await download_ig(query)
            			if data:
            				await message.reply_video(video=data['main_media_hd'], caption=f"Download by {app.me.mention}")
            			else:
            				await message.reply("Give A Valid Url")
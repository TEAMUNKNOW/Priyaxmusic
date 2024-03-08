from pyrogram.types import InlineKeyboardButton
import config

def song_markup(_, vidid):
    buttons = [
        [
            InlineKeyboardButton(
                text="ᴀᴜᴅɪᴏ",
                callback_data=f"song_helper audio|{vidid}",
            ),
            InlineKeyboardButton(
                text="ᴠɪᴅᴇᴏ",
                callback_data=f"song_helper video|{vidid}",
            ),
        ],
        [
            InlineKeyboardButton(
                text=_["CLOSE_BUTTON"], callback_data="close"
            ),
        ],
    ]
    return buttons
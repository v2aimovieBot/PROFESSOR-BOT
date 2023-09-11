import re, os
from os import environ
import asyncio
import json
from collections import defaultdict
from typing import Dict, List, Union
from pyrogram import Client
from time import time

id_pattern = re.compile(r'^.\d+$')
def is_enabled(value, default):
    if value.strip().lower() in ["on", "true", "yes", "1", "enable", "y"]:
        return True
    elif value.strip().lower() in ["off", "false", "no", "0", "disable", "n"]:
        return False
    else:
        return default


# Bot information
PORT = environ.get("PORT", "8080")
WEBHOOK = bool(environ.get("WEBHOOK", True)) # for web support on/off
SESSION = environ.get('SESSION', 'Media_search')
API_ID = int(environ['API_ID'])
API_HASH = environ['API_HASH']
BOT_TOKEN = environ['BOT_TOKEN']

# Bot settings
CACHE_TIME = int(environ.get('CACHE_TIME', 300))
USE_CAPTION_FILTER = bool(environ.get('USE_CAPTION_FILTER', True))
PICS = (environ.get('PICS' ,'https://graph.org/file/01ddfcb1e8203879a63d7.jpg https://graph.org/file/d69995d9846fd4ad632b8.jpg https://graph.org/file/a125497b6b85a1d774394.jpg https://graph.org/file/43d26c54d37f4afb830f7.jpg https://graph.org/file/60c1adffc7cc2015f771c.jpg https://graph.org/file/d7b520240b00b7f083a24.jpg https://graph.org/file/0f336b0402db3f2a20037.jpg https://graph.org/file/39cc4e15cad4519d8e932.jpg https://graph.org/file/d59a1108b1ed1c6c6c144.jpg https://te.legra.ph/file/3a4a79f8d5955e64cbb8e.jpg https://graph.org/file/d69995d9846fd4ad632b8.jpg')).split()
BOT_START_TIME = time()

# Admins, Channels & Users
ADMINS = [int(admin) if id_pattern.search(admin) else admin for admin in environ.get('ADMINS', '').split()]
CHANNELS = [int(ch) if id_pattern.search(ch) else ch for ch in environ.get('CHANNELS', '0').split()]
auth_users = [int(user) if id_pattern.search(user) else user for user in environ.get('AUTH_USERS', '').split()]
AUTH_USERS = (auth_users + ADMINS) if auth_users else []
auth_channel = environ.get('AUTH_CHANNEL')
auth_grp = environ.get('AUTH_GROUP')
AUTH_CHANNEL = int(auth_channel) if auth_channel and id_pattern.search(auth_channel) else None
AUTH_GROUPS = [int(ch) for ch in auth_grp.split()] if auth_grp else None

# MongoDB information
DATABASE_URI = environ.get('DATABASE_URI', "")
DATABASE_NAME = environ.get('DATABASE_NAME', "Cluster0")
COLLECTION_NAME = environ.get('COLLECTION_NAME', 'Telegram_files')

#maximum search result buttos count in number#
MAX_RIST_BTNS = int(environ.get('MAX_RIST_BTNS', "10"))
START_MESSAGE = environ.get('START_MESSAGE', '👋 𝙷𝙴𝙻𝙾 {user}\n\n𝙼𝚈 𝙽𝙰𝙼𝙴 𝙸𝚂 {bot},\n𝙸 𝙲𝙰𝙽 𝙿𝚁𝙾𝚅𝙸𝙳𝙴 𝙼𝙾𝚅𝙸𝙴𝚂, 𝙹𝚄𝚂𝚃 𝙰𝙳𝙳 𝙼𝙴 𝚃𝙾 𝚈𝙾𝚄𝚁 𝙶𝚁𝙾𝚄𝙿 𝙰𝙽𝙳 𝙼𝙰𝙺𝙴 𝙼𝙴 𝙰𝙳𝙼𝙸𝙽...')
BUTTON_LOCK_TEXT = environ.get("BUTTON_LOCK_TEXT", "𝙃𝙚𝙮 {𝙦𝙪𝙚𝙧𝙮}! \n🥴 यह किसी और के द्वारा की गई मूवी रिक्वेस्ट है। कृपया खुद से मूवी रिक्वेस्ट करें। 🙏\n𝙏𝙝𝙞𝙨 𝙞𝙨 𝙣𝙤𝙩 𝙮𝙤𝙪𝙧 𝙧𝙚𝙦𝙪𝙚𝙨𝙩𝙚𝙙 𝙈𝙤𝙫𝙞𝙚 \n𝙋𝙡𝙚𝙖𝙨𝙚 𝙧𝙚𝙦𝙪𝙚𝙨𝙩 𝙮𝙤𝙪𝙧 𝙤𝙬𝙣 😎")
FORCE_SUB_TEXT = environ.get('FORCE_SUB_TEXT', '𝙅𝙤𝙞𝙣 𝙊𝙪𝙧 𝙈𝙤𝙫𝙞𝙚𝙨 𝙐𝙥𝙙𝙖𝙩𝙚 𝘾𝙝𝙖𝙣𝙣𝙚𝙡 𝙏𝙤 𝙐𝙨𝙚 𝙏𝙝𝙞𝙨 𝘽𝙤𝙩.! \n𝙏𝙝𝙚𝙣 𝘾𝙡𝙞𝙘𝙠 𝙤𝙣 🔄 𝙩𝙧𝙮 𝘼𝙜𝙖𝙞𝙣 𝘽𝙪𝙩𝙩𝙤𝙣.\nमूवीज डाउनलोड करने के लिए कृपया हमारे अपडेट चैनल को ज्वॉइन कीजिए 🙏 \nफिर 🔄 𝙩𝙧𝙮 𝙖𝙜𝙖𝙞𝙣 पर क्लिक करें और अपनी मूवीज प्राप्त करें।')
RemoveBG_API = environ.get("RemoveBG_API", "")
WELCOM_PIC = environ.get("WELCOM_PIC", "")
WELCOM_TEXT = environ.get("WELCOM_TEXT", "👋 𝙃𝙚𝙮 {user} \n𝙬𝙚𝙡𝙘𝙤𝙢𝙚 𝙩𝙤 {chat}🌹\nकिसी भी फिल्म के लिए रिक्वेस्ट करें हम इसे मुफ्त में प्रदान करेंगे 💯 बस ग्रुप में मूवी का नाम मैसेज करें और तुरंत फाइल प्रोवा इडर  द्वारा डाउनलोडिंग लिंक प्राप्त करें। \nRead pinned message for Group rules")
PMFILTER = is_enabled(environ.get('PMFILTER', "True"), True)
G_FILTER = is_enabled(environ.get("G_FILTER", "True"), True)
BUTTON_LOCK = is_enabled(environ.get("BUTTON_LOCK", "True"), True)

# url shortner
SHORT_URL = environ.get("SHORT_URL")
SHORT_API = environ.get("SHORT_API")

# Others
IMDB_DELET_TIME = int(environ.get('IMDB_DELET_TIME', "300"))
LOG_CHANNEL = int(environ.get('LOG_CHANNEL', 0))
SUPPORT_CHAT = environ.get('SUPPORT_CHAT', 'mkn_bots_updates')
P_TTI_SHOW_OFF = is_enabled(environ.get('P_TTI_SHOW_OFF', "True"), True)
PM_IMDB = is_enabled(environ.get('PM_IMDB', "True"), True)
IMDB = is_enabled(environ.get('IMDB', "True"), True)
SINGLE_BUTTON = is_enabled(environ.get('SINGLE_BUTTON', "True"), True)
CUSTOM_FILE_CAPTION = environ.get("CUSTOM_FILE_CAPTION", "▪️ 𝐅𝐢𝐥𝐞 𝐧𝐚𝐦𝐞 : {file_name}\n▪️ 𝐅𝐢𝐥𝐞 𝐒𝐢𝐳𝐞 : {file_size}\n_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳\n🔰 𝗣𝗹𝗲𝗮𝘀𝗲 𝘀𝘂𝗽𝗽𝗼𝗿𝘁 𝘂𝘀 𝗯𝘆 𝘀𝘂𝗯𝘀𝗰𝗿𝗶𝗯𝗶𝗻𝗴 𝘁𝗼 𝗼𝘂𝗿 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 𝗰𝗵𝗮𝗻𝗻𝗲𝗹 𝘁𝗼 𝗴𝗲𝘁 𝗳𝗿𝗲𝗲 𝗺𝗼𝘃𝗶𝗲𝘀. 𝗜𝘁 𝘄𝗶𝗹𝗹 𝗼𝗻𝗹𝘆 𝘁𝗮𝗸𝗲 𝘆𝗼𝘂 𝟭𝟬 𝘀𝗲𝗰𝗼𝗻𝗱𝘀 🥰\n_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳\n🔰 मुफ्त में मूवीज प्राप्त करने हेतु कृपया हमारे यूट्यूब चैनल को सब्सक्राइब कर के हमरा सपोर्ट करें । इसमें सिर्फ आपका 10 सेकंड लगेगा। 🥰\n_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳_̳\n🔰 𝗢𝘂𝗿 𝗬𝗼𝘂𝗧𝘂𝗯𝗲 𝗖𝗵𝗮𝗻𝗻𝗲𝗹 👇\n╭────────•◆•──────➤\n•❰🔥https://tapthe.link/1Z2wRI82P ❱•\n•❰🔥https://tapthe.link/1Z2wRI82P ❱•\n•❰🔥https://tapthe.link/1Z2wRI82P ❱•\n╰────────•◆•──────➤")
BATCH_FILE_CAPTION = environ.get("BATCH_FILE_CAPTION", None)
IMDB_TEMPLATE = environ.get("IMDB_TEMPLATE", "<b>Query: {query}</b> \n‌IMDb Data:\n\n🏷 Title: <a href={url}>{title}</a>\n🎭 Genres: {genres}\n📆 Year: <a href={url}/releaseinfo>{year}</a>\n🌟 Rating: <a href={url}/ratings>{rating}</a> / 10")
LONG_IMDB_DESCRIPTION = is_enabled(environ.get("LONG_IMDB_DESCRIPTION", "False"), False)
SPELL_CHECK_REPLY = is_enabled(environ.get("SPELL_CHECK_REPLY", "True"), True)
MAX_LIST_ELM = environ.get("MAX_LIST_ELM", None)
INDEX_REQ_CHANNEL = int(environ.get('INDEX_REQ_CHANNEL', LOG_CHANNEL))
FILE_STORE_CHANNEL = [int(ch) for ch in (environ.get('FILE_STORE_CHANNEL', '')).split()]
MELCOW_NEW_USERS = is_enabled(environ.get('MELCOW_NEW_USERS', "True"), True)
PROTECT_CONTENT = is_enabled(environ.get('PROTECT_CONTENT', "False"), False)
PUBLIC_FILE_STORE = is_enabled(environ.get('PUBLIC_FILE_STORE', "True"), True)




BLACKLIST_WORDS = (
    list(os.environ.get("BLACKLIST_WORDS").split(","))
    if os.environ.get("BLACKLIST_WORDS")
    else []
)

BLACKLIST_WORDS = ["@BM Links", "[BindasMovies]", "[Hezz Movies]", "www Tamilblasters rent", "E4E", "[D&O]", "[MM]", "[", "]", "[FC]", "[CF]", "LinkZz", "[DFBC]", "@New_Movie", "@Infinite_Movies2", "MM", "@R A R B G", "[F&T]", "[KMH]", "[DnO]", "[F&T]", "MLM", "@TM_LMO", "@x265_E4E", "@HEVC MoviesZ", "SSDMovies", "@MM Linkz", "[CC]", "@Mallu_Movies", "@DK Drama", "@luxmv_Linkz", "@Akw_links", "CK HEVC", "@Team_HDT", "[CP]", "www 1TamilMV men", "www TamilRockers", "@MM", "@mm", "[MW]", "@TN68 Linkzz", "@Clipmate_Movie", "[MASHOBUC]", "Official TheMoviesBoss", "www CineVez one", "www 7MovieRulz lv", "www 1TamilMV vip", "[SMM Official]"]






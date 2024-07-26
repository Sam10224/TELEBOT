# This is the main python script with all the bot functionalities

# Import all required modules
import os
import requests
import random
import openai
import wikipediaapi
from typing import Final
from datetime import datetime
from telegram import Bot, Update
from telegram.error import BadRequest
from googletrans import Translator, LANGUAGES
from telegram.ext import Application, CommandHandler, MessageHandler, filters, ContextTypes
from helper import dare, truth, insults, flirtLines, jokes

# Replace with your own API keys and URLs if necessary
TOKEN: Final = os.getenv("BOT_TOKEN")
BOT_USERNAME: Final = os.getenv("BOT_USERNAME")
CHANNEL_ID: Final = os.getenv("CHANNEL_ID")
GROUP_ID: Final = os.getenv("GROUP_ID")
OPENAI_API_KEY: Final = os.getenv("OPENAI_API_KEY")
PEXELS_API_KEY: Final = os.getenv("PEXELS_API_KEY")
TRIVIA_API_KEY: Final = os.getenv("TRIVIA_API_KEY")
YOUTUBE_API_KEY: Final = os.getenv("YOUTUBE_API_KEY")
WEATHER_API_KEY: Final = os.getenv("WEATHER_API_KEY")

WEATHER_URL: Final = "http://api.openweathermap.org/data/2.5/weather"
USER_AGENT: Final = "YourBotName/1.0 (https://yourwebsite.com/; your-email@example.com)"
wiki_wiki = wikipediaapi.Wikipedia(language="en", user_agent=USER_AGENT)
openai.api_key = OPENAI_API_KEY

async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
—————————————————————
┈╭━━━━━━━━━━━╮┈ ┈┃╭━━━╮┊╭━━━╮┃┈ ╭┫┃┈▇┈┃┊┃┈▇┈┃┣╮ ┃┃╰━━━╯┊╰━━━╯┃┃ ╰┫╭━╮╰━━━╯╭━╮┣╯ ┈┃┃┣┳┳┳┳┳┳┳┫┃┃┈ ┈┃┃╰┻┻┻┻┻┻┻╯┃┃┈ ┈╰━━━━━━━━━━━╯┈
*/menu to display the menu*
.……..… /´¯/)………....(\¯\.............
……….../….//……….. …\\….\. ........
………../….//………… ….\\….\. ......
…../´¯/…./´¯\………../¯ \….\¯`\.....
.././.../…./…./.|_……_|.\….\….\…\.\
(.(….(….(…./.)..)..(..(.\….)….)….).) 
.\…………….\/../…..\....\/…………../
""")

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return "Hey there i am TELEBOT!"
    if "how are you" in processed:
        return "I've never been better!"
    if "bot" in processed:
        return ""
    if "menu" in processed:
        return f"""
        ╭════〘 TELEBOT 〙═⊷⏣
⬡│▸ /start
⬡│▸ /menu
⬡│▸ /pexels
⬡│▸ /openai
⬡│▸ /weather
⬡│▸ /trivia
⬡│▸ /youtube
⬡│▸ /tiktok
⬡│▸ /owner
⬡│▸ /version
⬡│▸ /translate
⬡│▸ /morse
⬡│▸ /time
 └───────────────···▸
The current date and time is\n {datetime.now()}
        === [ V.1.0.0 ] ===
"""
    return ""

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"[USER]: ({update.message.chat.id}) in {message_type}: {text}")

    if message_type == "group":
        if BOT_USERNAME in text:
            new_text: str = text.replace(BOT_USERNAME, "").strip()
            response: str = handle_response(new_text)
        else:
            return ""
    else:
        response: str =  handle_response(text)

    print("[TELEBOT]:", response)
    await update.message.reply_text(response)

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[TELEBOT]: update {update}\n caused error {context.error}\n")

if __name__ == "__main__":
    print("[TELEBOT]: Starting bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))

    app.add_handler(CommandHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print("[TELEBOT]: All Systems Nominal!")
    print("\n")
    print("[TELEBOT]: Polling...")
    app.run_polling(poll_interval=3)
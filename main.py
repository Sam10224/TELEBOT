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
from helper import dareLines, truthLines, insultLines, flirtLines, jokeLines

#####################################################################################

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
translator = Translator()

##################################################################################################

# This is the start command called via the start button or /start
async def start_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
—————————————————————
┈╭━━━━━━━━━━━╮┈ ┈┃╭━━━╮┊╭━━━╮┃┈ ╭┫┃┈▇┈┃┊┃┈▇┈┃┣╮ ┃┃╰━━━╯┊╰━━━╯┃┃ ╰┫╭━╮╰━━━╯╭━╮┣╯ ┈┃┃┣┳┳┳┳┳┳┳┫┃┃┈ ┈┃┃╰┻┻┻┻┻┻┻╯┃┃┈ ┈╰━━━━━━━━━━━╯┈
            *TELEBOT => /menu*
""")

####################################################################################

# This is the add member function that automatically adds members to your group
async def add_members(update: Update, context: ContextTypes.DEFAULT_TYPE):
    members = []
    for member in update.chat_member:
        try:
            await Bot.add_chat_members(chat_id=GROUP_ID, user_ids=[member])
        except BadRequest as e:
            print(f"[TELEBOT]: Failed to add {member}: {e}")

#################################################################

# This is the version command that requests the latest version of the Bot
async def version_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("[TELEBOT]: Version => [ V.1.0.0 ]")

##############################################################################################

# This is a custom command
async def help_command(update: Update, context:ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("Type help for more information")

########################################################################################################

# This is the owner command that fetches details about the bot owner
async def owner_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    await update.message.reply_text("""
           === [ V.1.2.8 ] ===                         
[BOT]: @kenya_pentagonBot
[OWNER]: @sam_yose
[CHANNEL]: @kE_pentagon
[PROJECT]: https://github.com/Sam10224/TELEBOT.git

Use the /menu to get the full list of my commands...
""")

###########################################################################################

async def joke_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    joke = random.choice(jokeLines)
    await update.message.reply_text(joke)

async def truth_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    truth = random.choice(truthLines)
    await update.message.reply_text(truth)

async def dare_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    dare = random.choice(dareLines)
    await update.message.reply_text(dare)

async def flirt_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    flirt = random.choice(flirtLines)
    await update.message.reply_text(flirt)

async def insult_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    insult = random.choice(insultLines)
    await update.message.reply_text(insult)

##########################################################################################################

# This is the weather command
async def weather_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    city = update.message.text.split(" ", 1)[1] if len(update.message.text.split()) > 1 else "Nairobi"
    response = requests.get(f"{WEATHER_URL}?q={city}&appid={WEATHER_API_KEY}&units=metric")
    data = response.json()
    
    if response.status_code == 200:
        main = data["main"]
        weather = data['weather'][0]
        temperature = main["temp"]
        humidity = main["humidity"]
        weather_description = weather["description"]
        await update.message.reply_text(f"""
===[TELEBOT WEATHER]===\n
The weather in {city} is:\n
1. [Temperature]: {temperature}°C
2. [Humidity]: {humidity}%
3. [Description]: {weather_description}\n
===[TELEBOT WEATHER]===
""")
    else:
        await update.message.reply_text("I couldn't retrieve the weather information. Please try again.")

#################################################################################################

# Interact with chatGPT
async def openai_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    prompt = update.message.text.split(" ", 1)[1] if len(update.message.text.split()) > 1 else "Hello"
    response = openai.Completion.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user","content": prompt}],
        max_tokens=50
    )
    await update.message.reply_text(response.choices[0].text.strip())

######################################################################################################################

async def wiki_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    search_query = update.message.text.split(" ", 1)[1] if len(update.message.text.split()) > 1 else "Wikipedia"
    page = wiki_wiki.page(search_query)
    if page.exists():
        summary = page.summary[:1000]
        await update.message.reply_text(summary)
    else:
        await update.message.reply_text("I couldn't find any information about this")

##############################################################################################################################

async def pexels_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.split(" ", 1)[1] if len(update.message.text.split()) > 1 else "nature"
    headers = {
        "Authorization": PEXELS_API_KEY
    }
    params = {
        "query": query,
        "per_page": 1
    }
    response = requests.get("https://api.pexels.com/v1/search", headers=headers, params=params)
    data = response.json()

    if response.status_code == 200 and data.get("photos"):
        photo_url = data["photos"][0]["src"]["original"]
        await update.message.reply_photo(photo_url, caption=f"Here's an image for your search: {query}")
    else:
        await update.message.reply_text("Image not found")

def get_trivia_question(api_key, category=9, difficulty="medium", question_type="multiple"):
    url = "https://opentdb.com/api/php"
    params = {
        "amount": 1,
        "apikey": api_key,
        "category": category,
        "difficulty": difficulty,
        "type": question_type
    }

    response = requests.get(url, params=params)
    if response.status_code == 200:
        data = response.json()
        return data["results"][0]
    else:
        print(f"Error: Unable to retrieve data (Status Code: {response.status_code})")
        return None


async def trivia_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    question = get_trivia_question(TRIVIA_API_KEY, category=9, difficulty="medium", question_type="multiple")
    if question:
        text = f"Question: {question['question']}\n"
        if question["type"] == "multiple":
            all_answers = question["incorrect_answers"] + [question["correct_answer"]]
            random.shuffle(all_answers)
            for i, answer in enumerate(all_answers, 1):
                text += f" {i}. {answer}\n"
        elif question["type"] == "boolean":
            text += "1. True\n 2. False\n"
        await update.message.reply_text(text)
    else:
        await update.message.reply_text("I could not retrieve a trivia question. Please try again.")

############################################################################################################################

async def youtube_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    query = update.message.text.split(" ", 1)[1] if len(update.message.text.split()) > 1 else "Telegram"

    try:
        response = requests.get(f"https://www.googleapis.com/youtube/v3/search?part=snippet&q={query}&key={YOUTUBE_API_KEY}&maxResults=1")
        response.raise_for_status()
        data = response.json()

        print("Youtube API response data:", data)

        if "items" in data and data["items"]:
            item = data["items"][0]
            video_id = item["id"].get("videoId") if "id" in item else None
            if video_id:
                video_url = f"https://www.youtube.com/watch?v={video_id}"
                await update.message.reply_text(video_url)
            else:
                await update.message.reply_text("No video id found in the response.")
        else:
            await update.message.reply_text("No item found in the youtube API response.")

    except requests.RequestException as e:
        await update.message.reply_text(f"An error occurred while fetching video: {e}")
    except KeyError as e:
        await update.message.reply_text(f"Missing expected data in the response: {e}")

############################################################################################################

async def translate_command(update: Update, context: ContextTypes.DEFAULT_TYPE):
    if len(context.args) < 2:
        await update.message.reply_text("Usage: /translate <language_code> <text>")
        return
    
    target_lang = context.args[0]
    text_to_translate = " ".join(context.args[1:])

    if target_lang not in LANGUAGES:
        await update.message.reply_text(f"Language code '{target_lang}' is not supported.")
        return
    
    try:
        translated = translator.translate(text_to_translate, dest=target_lang)
        await update.message.reply_text(translated.text)
    except Exception as e:
        print(f"Translation Error: {e}")
        await update.message.reply_text("An error occured while trying to translate the text.")

def handle_response(text: str) -> str:
    processed: str = text.lower()

    if "hello" in processed:
        return "Hey there i am TELEBOT!"
    if "how are you" in processed:
        return "I've never been better!"
    if "help" in processed:
        return ""
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
⬡│▸ /flirt
⬡│▸ /joke
⬡│▸ /insult
⬡│▸ /truth
⬡│▸ /dare
 └───────────────···▸
The current date and time is\n {datetime.now()}
        === [ V.1.0.0 ] ===
"""
    return ""

#############################################################################################

async def handle_message(update: Update, context: ContextTypes.DEFAULT_TYPE):
    message_type: str = update.message.chat.type
    text: str = update.message.text

    print(f"[{update.message.chat.full_name}] in {message_type}: {text}")

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

#########################################################################################################

async def error(update: Update, context: ContextTypes.DEFAULT_TYPE):
    print(f"[TELEBOT]: update {update}\n caused error {context.error}\n")

################################################################################################################

if __name__ == "__main__":
    print("[TELEBOT]: Starting bot...")
    app = Application.builder().token(TOKEN).build()

    app.add_handler(CommandHandler("start", start_command))
    app.add_handler(CommandHandler("add", add_members))
    app.add_handler(CommandHandler("version", version_command))
    app.add_handler(CommandHandler("help", help_command))
    app.add_handler(CommandHandler("owner", owner_command))
    app.add_handler(CommandHandler("joke", joke_command))
    app.add_handler(CommandHandler("insult", insult_command))
    app.add_handler(CommandHandler("truth", truth_command))
    app.add_handler(CommandHandler("dare", dare_command))
    app.add_handler(CommandHandler("flirt", flirt_command))
    app.add_handler(CommandHandler("weather", weather_command))
    app.add_handler(CommandHandler("youtube", youtube_command))
    app.add_handler(CommandHandler("pexels", pexels_command))
    app.add_handler(CommandHandler("trivia", trivia_command))
    app.add_handler(CommandHandler("wikipedia", wiki_command))

    app.add_handler(MessageHandler(filters.TEXT, handle_message))

    app.add_error_handler(error)

    print("[TELEBOT]: All Systems Nominal!")
    print("\n")
    print("[TELEBOT]: Polling...")
    app.run_polling(poll_interval=3)
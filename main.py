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


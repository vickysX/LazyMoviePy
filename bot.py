import telebot
import requests
import os

TELEGRAM_API_KEY = os.environ.get("TELEGRAM_API_KEY")
RAPID_API_KEY = os.environ.get("RAPID_API_KEY")
bot_client = telebot.TeleBot(TELEGRAM_API_KEY)

@bot_client.message_handler(commands = ["start"])
def send_welcome_message(message):
    bot_client.send_message(chat_id = message.chat.id, text = "Hi, I'm a bot")

@bot_client.message_handler(commands = ["help"])
def send_welcome_message(message):
    bot_client.send_message(chat_id = message.chat.id, text = "Do it yourself!")

@bot_client.message_handler(regexp = "[a-z]*\s[a-z]*")
def send_data(message):
    data = message.text.split(" ")
    title = data[0]
    country = data[1]
    movieData = fetch_data(title, country)["result"][0]
    bot_client.send_message(chat_id=message.chat.id, text=f"Title: {movieData['title']}\nOverview: {movieData['overview']}\nYear: {movieData['year']}")

def fetch_data(title, country, show_type = "all", lang = "en") -> dict:
    url = "https://streaming-availability.p.rapidapi.com/v2/search/title"
    querystring = {"title":title,"country":country,"show_type":show_type,"output_language":lang}
    headers = {
        "X-RapidAPI-Key": RAPID_API_KEY,
        "X-RapidAPI-Host": "streaming-availability.p.rapidapi.com"
    }
    response = requests.get(url, headers=headers, params=querystring)
    return response.json()

bot_client.infinity_polling()
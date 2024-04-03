import os
from bot import MyBot
from dotenv import load_dotenv


#loading dotenv files
load_dotenv()

bot_token = os.getenv('BOT_TOKEN')
db_url = os.getenv('DB_URL')

def main():
    bot = MyBot(bot_token)
    bot.run()

if __name__ == '__main__':
    main()

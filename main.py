import os
from bot import MyBot
from dotenv import load_dotenv


#loading dotenv files
load_dotenv(override=True)

bot_token = os.getenv('BOT_TOKEN_PRO')

def main():
    bot = MyBot(bot_token)
    bot.run()

if __name__ == '__main__':
    main()

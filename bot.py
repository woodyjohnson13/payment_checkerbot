from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from database.db import Database
from dotenv import load_dotenv
import os

#loading dotenv files
load_dotenv()


db_url = os.getenv('DB_URL')


class MyBot:
    def __init__(self, token):
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.username="@PyamentCheckBot"
        db_session=Database(db_url)


    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Hello! I'm your bot.")
        
    def respond_to_mention(self, update, context):
        if self.username in update.message.text:
            context.bot.send_message(chat_id=update.effective_chat.id, text="You mentioned me!")



    def run(self):
        start_handler = CommandHandler('start', self.start)
        mention_handler = MessageHandler(Filters.entity('mention'), self.respond_to_mention)

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(mention_handler)


        self.updater.start_polling()
        self.updater.idle()

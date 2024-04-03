from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
from database.db import Database
from dotenv import load_dotenv
import os
import re

#loading dotenv files
load_dotenv(override=True)


db_url = os.getenv('DB_URL')

orders_approve = [[InlineKeyboardButton("Yes", callback_data='yes'),
            InlineKeyboardButton("No", callback_data='no')]]



class MyBot:
    def __init__(self, token):
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.username="@PyamentCheckBot"
        self.db_session=Database(db_url)

    def button_handers(self,update, context):
        query = update.callback_query
        
        message_sender_id = query.message.reply_to_message.from_user.id
        if query.from_user.id != message_sender_id:
            # If the button click is not from the original message sender, ignore it
            return


        if query.data == 'yes':           
            context.bot.send_message(chat_id=query.message.chat_id, text="You clicked Yes!")
        elif query.data == 'no':
            context.bot.send_message(chat_id=query.message.chat_id, text="You clicked No!")
            
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text=query.message.text,
                                      reply_markup=None)



    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Бот онлайн.")
    
    def extract_lead_ids(self, message_text):
        pattern = r'#(\d+)|[;,/](\d+)'
        matches = re.findall(pattern, message_text)
        # Extract the IDs from the matches
        lead_ids = [int(match[0]) if match[0] else int(match[1]) for match in matches]
        return lead_ids
        
    def respond_to_mention(self, update, context):
        if self.username in update.message.text:
            lead_ids = self.extract_lead_ids(update.message.text)
            print(lead_ids)
            if lead_ids:
                orders = self.db_session.get_order_by_lead_id(lead_ids)
                if orders:
                    orders_approve_message = ""
                    for order in orders:
                        orders_approve_message += f"Lead_id: {order.lead_id}, Info: {order.info}\n"
                    order_approve_markup = InlineKeyboardMarkup(orders_approve)
                    context.bot.send_message(chat_id=update.effective_chat.id, text=orders_approve_message,reply_markup=order_approve_markup,reply_to_message_id=update.message.message_id)
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text="Заказы не найдены",reply_to_message_id=update.message.message_id)
            else:
                context.bot.send_message(chat_id=update.effective_chat.id, text="Лид ID не определены",reply_to_message_id=update.message.message_id)



    def run(self):
        start_handler = CommandHandler('start', self.start)
        mention_handler = MessageHandler(Filters.entity('mention'), self.respond_to_mention)
        button_handler = CallbackQueryHandler(self.button_handers)

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(mention_handler)
        self.dispatcher.add_handler(button_handler)  



        self.updater.start_polling()
        self.updater.idle()

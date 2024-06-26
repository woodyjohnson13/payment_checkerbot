import os
from dotenv import load_dotenv
#*Telegram imports
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
#*Classes
from database.db import Database
from regex.regex_processor import RegexProcessor
from amocrm_integration.amo_integration import AmoCRM
import time

load_dotenv(override=True)

amo_client_id=os.getenv('AMO_CLIENT_ID')
amo_client_secret=os.getenv('AMO_CLIENT_SECRET')
amo_redirect_url=os.getenv('AMO_REDIRECT_URL')
amo_subdomain=os.getenv('AMO_SUBDOMAIN')




db_url = os.getenv('DB_URL')

my_regex=RegexProcessor()
my_amo=AmoCRM(amo_client_id,amo_client_secret,amo_subdomain,amo_redirect_url)

class MyBot:
    def __init__(self, token):
        self.updater = Updater(token=token, use_context=True)
        self.dispatcher = self.updater.dispatcher
        self.username="@PyamentCheckBot"
        self.db_session=Database(db_url)
    
    def button_handers(self,update, context):
        query = update.callback_query
        chat_id=query.message.chat_id
        reply_message=query.message.reply_to_message.text
        message_sender_id = query.message.reply_to_message.from_user.id
        # If the button click is not from the original message sender, ignore it
        if query.from_user.id != message_sender_id:
            return

        data = query.data.split(":")  # Splitting callback data to extract lead ID and name
        if len(data) == 6 and data[0] == 'yes':
            print(data)
            lead_id, amount,checking_account,date,payment_text_id = data[1], data[2],data[3],data[4],data[5]
            
            payment_message=self.db_session.get_payment_text(payment_text_id).text
            self.db_session.create_payment(lead_id,date,amount,checking_account,payment_message,chat_id,reply_message)
            #!Get rid of it, it throws error
            # self.db_session.delete_payment_text(payment_text_id)
            my_amo.change_payment_status_and_date(lead_id)
            #!This doesnt work for now
            # my_lead=my_amo.get_lead_by_id(lead_id)
            # my_lead.payment=1
            # my_lead.payment_date=my_amo.date_formatter(date)
            # my_lead.save()
            context.bot.send_message(chat_id=query.message.chat_id, text=f"Оплата внесена для сделки: {lead_id}\nВ размере: {amount}р\nРасчетный счет: {checking_account}\nДата: {date}") 
        if len(data)==1 and data[0]=='no':
            pass    
        context.bot.delete_message(chat_id=query.message.chat_id, message_id=query.message.message_id)

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Бот онлайн.")
    
    def respond_to_reply(self, update, context):
        #text of the message i reply to
        replied_message_text = update.message.reply_to_message.text
        #extracting payment data from message
        lead_data=my_regex.handle_text(replied_message_text.replace('\n',' '))
        #text of my rely aka lead_ids
        your_reply_text = update.message.text
        #lead ids extracted
        lead_ids = my_regex.find_lead_ids(your_reply_text)
        orders = []
        if lead_data['amount'] != "Сумма сделки не найдена" and lead_data['date'] != 'Дата не найдена' and lead_data['checking_account'] != 'Расчетный счет не найден':
            
            
            max_retries = 5
            retries = 0
            payment_text_id = None
            while retries < max_retries:
                payment_text_id = self.db_session.create_payment_text(replied_message_text)
                if payment_text_id is not None:
                    break
                retries += 1
                time.sleep(1)  # Wait for 1 second before retrying
            if payment_text_id is None:
                # Handle the case when payment_text_id is still None after max retries
                return
            
            
            if lead_ids:
                    for lead_id in lead_ids:
                        amo_lead=my_amo.get_lead_by_id(lead_id)
                        if amo_lead :
                            order = {'id': amo_lead.id, 'name': amo_lead.name}                    
                            orders.append(order)
                    if orders:
                            for order in orders:                                
                                orders_approve_message = f"Сделка: {order['id']}\n{order['name']}\n"
                                
                                callback_data_yes = f"yes:{order['id']}:{lead_data['amount']}:{lead_data['checking_account']}:{lead_data['date']}:{payment_text_id}"
                                                                
                                order_approve_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Да", callback_data=callback_data_yes),
                                                                            InlineKeyboardButton("Нет", callback_data='no')]])
                                
                                context.bot.send_message(chat_id=update.effective_chat.id, text=orders_approve_message,reply_markup=order_approve_markup,reply_to_message_id=update.message.message_id)
     
    def run(self):
        start_handler = CommandHandler('start', self.start)
        button_handler = CallbackQueryHandler(self.button_handers)
        reply_handler = MessageHandler(Filters.reply, self.respond_to_reply)

        self.dispatcher.add_handler(start_handler)
        self.dispatcher.add_handler(button_handler)  
        self.dispatcher.add_handler(reply_handler)

        self.updater.start_polling()
        self.updater.idle()

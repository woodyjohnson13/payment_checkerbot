import os
from dotenv import load_dotenv
#*Telegram imports
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters,CallbackQueryHandler
from telegram import InlineKeyboardButton, InlineKeyboardMarkup
#*Classes
from database.db import Database
from regex.regex_processor import RegexProcessor
from amocrm_integration.amo_integration import AmoCRM

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
        
        message_sender_id = query.message.reply_to_message.from_user.id
        
        # If the button click is not from the original message sender, ignore it
        if query.from_user.id != message_sender_id:
            return

        data = query.data.split(":")  # Splitting callback data to extract lead ID and name
        if len(data) == 5 and data[0] == 'yes':
            lead_id, amount,checking_account,date = data[1], data[2],data[3],data[4]
            self.db_session.create_payment(lead_id,date,amount,checking_account)
            my_lead=my_amo.get_lead_by_id(lead_id)
            my_lead.payment=True
            my_lead.payment_date=my_amo.date_formatter(date)
            my_lead.save()
            context.bot.send_message(chat_id=query.message.chat_id, text=f"Оплата внесена для сделки: {lead_id}\nВ размере: {amount}р\nРасчетный счет: {checking_account}\nДата: {date}")
        elif len(data) == 3 and data[0] == 'no':
            lead_id,lead_name=data[1],data[2]
            context.bot.send_message(chat_id=query.message.chat_id,text=f"Сделка {lead_id} \n {lead_name} \nне подошла.")
            
        context.bot.edit_message_text(chat_id=query.message.chat_id,
                                      message_id=query.message.message_id,
                                      text=query.message.text,
                                      reply_markup=None)

    def start(self, update, context):
        context.bot.send_message(chat_id=update.effective_chat.id, text="Бот онлайн.")
    
     
    def respond_to_mention(self, update, context):
        if self.username in update.message.text:
            
            lead_data=my_regex.handle_text(update.message.text)
            lead_ids = my_regex.find_lead_ids(update.message.text)
            orders = []
            if lead_ids:
                for lead_id in lead_ids:
                    amo_lead=my_amo.get_lead_by_id(lead_id)
                    if amo_lead :
                        order = {'id': amo_lead.id, 'name': amo_lead.name}                    
                        orders.append(order)
                if orders:
                    for order in orders:
                        orders_approve_message = ""
                        orders_approve_message += f"Сделка: {order['id']}\n{order['name']}\n"
                        callback_data_yes = f"yes:{order['id']}:{lead_data['amount']}:{lead_data['checking_account']}:{lead_data['date']}"
                        # callback_data_no = f"no:{order['id']}:{order['name']}"
                        order_approve_markup = InlineKeyboardMarkup([[InlineKeyboardButton("Да", callback_data=callback_data_yes),
                                                                      InlineKeyboardButton("Нет", callback_data='no')]])
                        context.bot.send_message(chat_id=update.effective_chat.id, text=orders_approve_message,reply_markup=order_approve_markup,reply_to_message_id=update.message.message_id)
                else:
                    context.bot.send_message(chat_id=update.effective_chat.id, text=f"Заказ c {lead_id} не найден",reply_to_message_id=update.message.message_id)
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

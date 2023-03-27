import datetime
import logging
import time
from datetime import datetime


import telebot
from django.http import JsonResponse
from django.views import View

from telebot import types
from telebot.storage import StateMemoryStorage

from core.settings import BOT_TOKEN, BOT_URL
import os

import email
import email.mime.application
import smtplib
import ssl
import time
from datetime import datetime
from email.mime.multipart import MIMEMultipart
from email.mime.text import MIMEText

from bs4 import BeautifulSoup as bs
from pathlib import Path
from shutil import rmtree





logger = telebot.logger
telebot.logger.setLevel(logging.DEBUG)

state_storage = StateMemoryStorage()

bot = telebot.TeleBot('6203162805:AAGNiPa8rfioozNJoFpBU_ssxw-E6bUIBIc')


class BotAPIView(View):
    def post(self, request):
        json_string = request.body.decode('UTF-8')
        update = telebot.types.Update.de_json(json_string)
        bot.process_new_updates([update])
        return JsonResponse({'code': 200})

user_dict = {}


lang_dict = {'wrong_data': {'Русский 🇷🇺': 'Неверные данные', 'Oʻzbek tili 🇺🇿': 'Notoʻgʻri maʻlumotlar'},
             'ask_name': {'Русский 🇷🇺': 'Напишите своё имя', 'Oʻzbek tili 🇺🇿': 'Ismingizni yozing'},
             'wrong_name': {'Русский 🇷🇺': 'Данные введены некорректно. Просим указать имя',
                            'Oʻzbek tili 🇺🇿': 'Maʻlumotlar notoʻgʻri kiritilgan. Iltimos, ismni koʻrsating'},
             'ask_surname': {'Русский 🇷🇺': 'Напишите свою фамилию', 'Oʻzbek tili 🇺🇿': 'Familiyangizni yozing'}, 
             'wrong_surname': {'Русский 🇷🇺': 'Данные введены некорректно. Просим указать фамилию',
                            'Oʻzbek tili 🇺🇿': 'Maʻlumotlar notoʻgʻri kiritilgan. Iltimos, familiyangizni kiriting'},              
             'ask_number': {'Русский 🇷🇺': 'Укажитe контактный номер ,чтобы мы могли связаться с вами', 'Oʻzbek tili 🇺🇿': 'Siz bilan bogʻlanishimiz uchun telefon raqamingizni kiriting'},
             'wrong_number': {'Русский 🇷🇺': 'Неверный формат номера!', 'Oʻzbek tili 🇺🇿': 'Notoʻgʻri raqam formati!'},
              
             'ask_vacancy': {'Русский 🇷🇺': 'Напишите название желаемой вакансии', 'Oʻzbek tili 🇺🇿': 'Istagan vakansiyaning nomini yozing'},
             'wrong_vacancy': {'Русский 🇷🇺': 'Данные введены некорректно. Напиши название желаемой вакансии', 'Oʻzbek tili 🇺🇿': 'Maʻlumotlar notoʻgʻri kiritilgan. Istagan vakansiyaning nomini yozing'},

             'ask_resume': {'Русский 🇷🇺': 'Пожалуйста отправьте своё резюме', 'Oʻzbek tili 🇺🇿': 'Iltimos, CV ni yuboring'},
             'wrong_resume': {'Русский 🇷🇺': 'Неверный формат данных.Пожалуйста отправьте своё резюме', 'Oʻzbek tili 🇺🇿': 'Maʻlumotlar formati notoʻgʻri.Iltimos, CV ni yuboring'},

             'accept': {'Русский 🇷🇺': 'Вы даёте согласие на обработку персональных данных?', 'Oʻzbek tili 🇺🇿': 'Shaxsiy maʻlumotlarni qayta ishlashga rozilik berasizmi?'},

             'yes': {'Русский 🇷🇺': 'Да', 'Oʻzbek tili 🇺🇿': 'Ha'},
            
             'again': {'Русский 🇷🇺': 'Если хотите пройти опрос заново, нажмите на кнопку: "/start"',
                       'Oʻzbek tili 🇺🇿': 'Soʻrovnomadan qaytadan oʻtishni istasangiz quyidagi tugmani bosing: "/start"'},
             'ne_interesuyet': {'Русский 🇷🇺': 'Не интересует', 'Oʻzbek tili 🇺🇿': 'Qiziqtirmaydi'},
             'back': {'Русский 🇷🇺': 'Назад', 'Oʻzbek tili 🇺🇿': 'Ortga'},
             'start': {'Русский 🇷🇺': 'Начать сначала', 'Oʻzbek tili 🇺🇿': 'Boshidan boshlash'},
             'sendmail': {'Русский 🇷🇺': 'Ваше резюме отправлено на рассмотрение. Спасибо за отклик!', 'Oʻzbek tili 🇺🇿': 'Sizning rezyumeingiz koʻrib chiqish uchun yuborildi. Javobingiz uchun rahmat!'},
             'i_save_it': {'Русский 🇷🇺': 'Пожалуй, я сохраню это', 'Oʻzbek tili 🇺🇿': 'Balki saqlab qolarman'}
             
             
             }


class User:
    def __init__(self, lang):
        self.lang = lang
        self.name = None
        self.surname = None
        self.number = None
        self.jobs_name = None
        self.resume = None
        



markupp = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
btn1 = types.KeyboardButton('Русский 🇷🇺')
btn2 = types.KeyboardButton('Oʻzbek tili 🇺🇿')
markupp.row(btn1, btn2)


@bot.message_handler(commands=['start'])
def process_start(message):
    markupp = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    btn1 = types.KeyboardButton('Русский 🇷🇺')
    btn2 = types.KeyboardButton('Oʻzbek tili 🇺🇿')
    markupp.row(btn1, btn2)
    bot.send_message(message.chat.id,
                     'Привет!\nПожалуйста, выбери язык\n\nAssalomu alaykum!\nIltimos, tilni tanlang',
                     reply_markup=markupp)

    bot.register_next_step_handler(message, ask_language)


@bot.message_handler(content_types=['text'])
def checker(message):
    print(message.text)
    print("checker")
    if (message.text == '/start'):
        print("in if")
        process_start(message)
        return
    elif (message.text == 'Начать сначала'):
        process_start(message)
        return
    elif (message.text == 'Boshidan boshlash'):
        process_start(message)
        return
    else:
        print("in else")
        bot.reply_to(message, "Выбери вариант кнопкой (Tugmani bosib variantni tanlang)")


@bot.message_handler(content_types=['text'])
def ask_language(message):
    try:
        chat_id = message.chat.id
        lang = message.text

        if (lang == '/start'):
            process_start(message)
            return
 
        user = User(lang)
        user_dict[chat_id] = user
        print(user)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn = types.KeyboardButton(lang_dict['start'][user.lang])
        markup.row(btn)
        between_language_and_ask_name(message)
    except KeyError:
        bot.reply_to(message,
                     "Выберите один из вариантов 'Русский' или 'Ozbek tili'\n\n 'Русский' yoki 'Ozbek tili' parametrlaridan birini tanlang ")
        bot.register_next_step_handler(message, ask_language)


def between_language_and_ask_name(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn = types.KeyboardButton(lang_dict['start'][user.lang])
    markup.row(btn)

    markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
    btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
    markup__v1.row(btn_1, btn_2)

    msg = bot.send_message(message.chat.id, lang_dict['ask_name'][user.lang], reply_markup = markup)
    bot.register_next_step_handler(msg, ask_name)        


bot.message_handler(content_types=['text'])
def ask_name(message):
    try:
        chat_id = message.chat.id
        name = message.text
        user = user_dict[chat_id]

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn = types.KeyboardButton(lang_dict['start'][user.lang])
        markup.row(btn)

        if (name == lang_dict['start'][user.lang] or name == '/start'):
            process_start(message)
            return

        if not all(x.isascii() or x.isspace() or x.isalnum() for x in name):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            msg = bot.reply_to(message, lang_dict['wrong_name'][user.lang])
            bot.register_next_step_handler(msg, ask_name)
            return
        user.name = name
        between_ask_name_and_ask_surname(message)
       

    except Exception as e:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        msg = bot.reply_to(message, lang_dict['wrong_data'][user.lang])
        bot.register_next_step_handler(msg, ask_name)


def between_ask_name_and_ask_surname(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn = types.KeyboardButton(lang_dict['start'][user.lang])
    markup.row(btn)

    markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
    btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
    markup__v1.row(btn_1, btn_2)

    msg = bot.send_message(message.chat.id, lang_dict['ask_surname'][user.lang], reply_markup = markup__v1)
    bot.register_next_step_handler(msg, ask_surname) 

def ask_surname(message):
    try:
        chat_id = message.chat.id
        surname = message.text
        user = user_dict[chat_id]

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn = types.KeyboardButton(lang_dict['start'][user.lang])
        markup.row(btn)

        if (surname == lang_dict['start'][user.lang] or surname == '/start'):
            process_start(message)
            return

        if (surname == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            between_language_and_ask_name(message)
            return

        if not all(x.isascii() or x.isspace() or x.isalnum() for x in surname):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            msg = bot.reply_to(message, lang_dict['wrong_surname'][user.lang])
            bot.register_next_step_handler(msg, ask_surname)
            return
        user.surname = surname
        between_name_and_number(message)
        
    except Exception as e:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        msg = bot.reply_to(message, lang_dict['wrong_data'][user.lang])
        bot.register_next_step_handler(msg, ask_surname)                           

def between_name_and_number(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn = types.KeyboardButton(lang_dict['start'][user.lang])
    markup.row(btn)

    markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
    btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
    markup__v1.row(btn_1, btn_2)

    msg = bot.send_message(message.chat.id, lang_dict['ask_number'][user.lang], reply_markup = markup__v1)
    bot.register_next_step_handler(msg, ask_number)  



@bot.message_handler(content_types=['text'])
def ask_number(message):
    try:
        chat_id = message.chat.id
        number = message.text
        user = user_dict[chat_id]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn = types.KeyboardButton(lang_dict['start'][user.lang])
        markup.row(btn)

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        if (number == lang_dict['start'][user.lang] or number == '/start'):
            process_start(message)
            return

        if (number == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            between_ask_name_and_ask_surname(message)
            return

        if not all(x.isascii() or x.isspace() or x.isalnum() for x in number):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            msg = bot.reply_to(message, lang_dict['wrong_number'][user.lang])
            bot.register_next_step_handler(msg, ask_number)
            return

        user.number = number
        between_number_and_vacancy(message)

    except Exception:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        msg = bot.reply_to(message, lang_dict['wrong_number'][user.lang])
        bot.register_next_step_handler(msg, ask_number)

def between_number_and_vacancy(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn = types.KeyboardButton(lang_dict['start'][user.lang])
    markup.row(btn)

    markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
    btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
    markup__v1.row(btn_1, btn_2)

    msg = bot.send_message(message.chat.id, lang_dict['ask_vacancy'][user.lang], reply_markup = markup__v1)
    bot.register_next_step_handler(msg, vacancy)  

def vacancy(message):
    try:
        chat_id = message.chat.id
        jobs_name = message.text
        user = user_dict[chat_id]

        markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn = types.KeyboardButton(lang_dict['start'][user.lang])
        markup.row(btn)

        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)

        if (jobs_name == lang_dict['start'][user.lang] or jobs_name == '/start'):
            process_start(message)
            return

        if (jobs_name == lang_dict['back'][user.lang]):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            between_name_and_number(message)
            return

        if not all(x.isascii() or x.isspace() or x.isalnum() for x in jobs_name):
            chat_id = message.chat.id
            user = user_dict[chat_id]
            msg = bot.reply_to(message, lang_dict['wrong_vacancy'][user.lang])
            bot.register_next_step_handler(msg, vacancy)
            return
        user.jobs_name = jobs_name
        between_vacancy_and_ask_resume(message)
        

    except Exception:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        msg = bot.reply_to(message, lang_dict['wrong_vacancy'][user.lang])
        bot.register_next_step_handler(msg, vacancy)

def between_vacancy_and_ask_resume(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]

    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn = types.KeyboardButton(lang_dict['start'][user.lang])
    markup.row(btn)

    markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
    btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
    markup__v1.row(btn_1, btn_2)

    msg = bot.send_message(message.chat.id, lang_dict['ask_resume'][user.lang], reply_markup = markup__v1)
    bot.register_next_step_handler(msg, ask_resume)          

@bot.message_handler(content_types=['document'])
def ask_resume(message):
    try:
        chat_id = message.chat.id
        user = user_dict[chat_id]

        file_info = bot.get_file(message.document.file_id)
        downloaded_file = bot.download_file(file_info.file_path)
    
        user.resume = message.document.file_name
        
        if (message.text == '/start'):
            process_start(message)
            return
        if (message.text == lang_dict['start'][user.lang]):
            process_start(message)
            return
        if (message.text == lang_dict['back'][user.lang]):
            between_number_and_vacancy(message)
            return
        src = 'bot/send and clear' + message.document.file_name;
        with open(src, 'wb') as new_file:
            new_file.write(downloaded_file)
        
        markup__v1 = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
        btn_1 = types.KeyboardButton(lang_dict['start'][user.lang])
        btn_2 = types.KeyboardButton(lang_dict['back'][user.lang])
        markup__v1.row(btn_1, btn_2)
        
        bot.reply_to(message, lang_dict['i_save_it'][user.lang], reply_markup = markup__v1)
        Accept(message)
        
    except Exception:
        chat_id = message.chat.id
        user = user_dict[chat_id]
        msg = bot.reply_to(message, lang_dict['wrong_resume'][user.lang])
        bot.register_next_step_handler(msg, ask_resume)

@bot.message_handler(content_types=['text'])
def Accept(message):
  
    chat_id = message.chat.id
    user = user_dict[chat_id]

    markup_accept = types.InlineKeyboardMarkup(row_width=1)
    item1 = types.InlineKeyboardButton(lang_dict['yes'][user.lang], callback_data='Да')
    item2 = types.InlineKeyboardButton(lang_dict['back'][user.lang], callback_data='Назад')
    markup_accept.add(item1, item2)
    
    bot.send_message(message.chat.id, lang_dict['accept'][user.lang], reply_markup = markup_accept)


    




@bot.callback_query_handler(func=lambda call: True)
def edu(call):
    message = call.message
    try:
        if call.data == 'Да':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            send_email(message)
            
        if call.data == 'Назад':
            chat_id = call.message.chat.id
            user = user_dict[chat_id]
            between_vacancy_and_ask_resume(message)    

    except Exception as e:
        bot.reply_to(message, "ERROR")


def send_email(message):
    chat_id = message.chat.id
    user = user_dict[chat_id]
    msg = MIMEMultipart("alternative")
    fromaddr = "bukanov1234@mail.ru"
    mypass = "6bUc5jT7is5Yvz4pYHLf"
    toaddr = "bukanov1234@mail.ru"
    msg['From'] = fromaddr
    msg['To'] = toaddr
    msg['Subject'] = user.jobs_name

    now = datetime.now()
    response_date = now.strftime("%d.%m.%Y")
   

    html = f"""
    <!DOCTYPE html>
    <html>
    <head>
    <meta http-equiv="Content-Type" content="text/html; charset=utf-8">
    </head>
    <body>
    <h1>Заявка<h1>
    <br>        
    <p>Имя: {user.name}<p>
    <p>Фамилия: {user.surname}<p>
    <p>Номер: {user.number}<p>
    


                               
    </body>
    </html>
    """
    text = bs(html, "html.parser").text
    msg.attach(MIMEText(text, 'plain'))
    msg.attach(MIMEText(html, 'html', 'utf-8'))
    src = 'bot/send and clear' + user.resume;
    fp = open(src, 'rb')
    att = email.mime.application.MIMEApplication(fp.read())
    fp.close()
    att.add_header('Content-Disposition', 'attachment', filename=user.resume)
    msg.attach(att)

    server = smtplib.SMTP_SSL('smtp.mail.ru:465')
    ssl.SSLContext(ssl.PROTOCOL_TLS)
    server.login(msg['From'], mypass)
    text = msg.as_string()
    server.sendmail(msg['From'], msg['To'], text)
    server.quit()

    print("Successfully")

    for path in Path('bot/send and clear').glob('*'):
        if path.is_dir():
            rmtree(path)
        else:
            path.unlink()

    markup_start = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=1)
    btn = types.KeyboardButton('/start')
    markup_start.row(btn)   


    bot.send_message(message.chat.id, lang_dict['sendmail'][user.lang])   
    bot.send_message(message.chat.id, lang_dict['again'][user.lang], reply_markup = markup_start) 

    if (message.text == '/start'):
        process_start(message)
        return          


bot.enable_save_next_step_handlers(delay=2)

bot.load_next_step_handlers()


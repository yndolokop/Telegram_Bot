import telebot
import time
from telebot import types
import requests
from bs4 import BeautifulSoup
import re
import os


URL = 'https://www.film.ru/a-z/serials'

bot = telebot.TeleBot('5497131074:AAEpCyP-0saGTFWbWaQAtlQAmM6oKCm4hmA')


@bot.message_handler(comannds=['admin'])
def admin(message):
    info = os.name
    print(message)
    bot.reply_to(message.chat.id, info)

@bot.message_handler(comannds=['say'])
def say(message):
    text = ' '.join(message.text.split(' ')[1:])
    print(message)
    bot.reply_to(message, f'***{text.upper()}***')


@bot.message_handler(commands=['start'])
def start(message):
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=3)
    top30_serials = types.KeyboardButton('ТОП 30 сериалов')
    top30_films = types.KeyboardButton('ТОП 30 фильмов')
    top30_rus_serials = types.KeyboardButton('ТОП 30 русских сериалов')
    markup.add(top30_films, top30_serials, top30_rus_serials)
    mess = f'Привет, <b>{message.from_user.first_name}</b>!\nЧто будем искать? Нажми на одну из кнопок ниже.'
    bot.send_message(message.chat.id, mess, parse_mode='html', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def bot_mess(message):
    if message.chat.type == 'private':
        if message.text == 'ТОП 30 сериалов':
            url = 'https://www.film.ru/a-z/serials'
            response = requests.get(url)
            time.sleep(3)
            soup = BeautifulSoup(response.content, 'html.parser')
            films = soup.find_all('div', class_='film_list')
            for film in films:
                link = url + film.find('a', class_='film_list_link').get('href')
                name_ru = film.find('a', class_='film_list_link').find('strong').text
                date = film.find('a', class_='film_list_link').find_all('span')[2].text
                name_en = film.select("span[title]")
                for name in name_en:
                    eng_name = re.findall('"([^"]*)"', str(name))  # обязательно переведем класс soup в строку
                    all_films = f'{name_ru}\n {eng_name}\n {date}\n Cсылка: {link}'
                    bot.send_message(message.chat.id, all_films, parse_mode='html')


bot.polling(none_stop=True)

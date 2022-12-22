import telebot
import wikipedia, re
from config import token
import random
bot = telebot.TeleBot(token)

# Команда старта

@bot.message_handler(commands=['start'])
def welcom(message):
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
    item1 = telebot.types.KeyboardButton('Рандомное число')
    item2 = telebot.types.KeyboardButton('Кинуть кости')
    item3 = telebot.types.KeyboardButton('Конвертация')
    item4 = telebot.types.KeyboardButton('Вики')


    markup.add(item1, item2, item3, item4)

    bot.send_message(message.chat.id, 'Привет! Выбери пункт', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'привет':
        bot.send_message(message.chat.id, 'Привет, как дела?')
    elif message.text == 'Рандомное число':
        bot.send_message(message.chat.id, str(random.randint(1,100)))
    elif message.text == 'Кинуть кости':
        bot.send_message(message.chat.id, f'Вам выпало {(random.randint(1,6))} и {(random.randint(1,6))}')
    elif message.text == 'Конвертация':
        markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard=True)
        item2_0 = telebot.types.KeyboardButton('Зашифровать')
        item2_1 = telebot.types.KeyboardButton('Расшифровать')
        markup.add(item2_1, item2_0)
        bot.send_message(message.chat.id, 'Выберите что вам надо', reply_markup=markup)
    elif message.text == 'Зашифровать':
        bot.send_message(message.chat.id, 'Введите текст формата - ABBCCC')
        bot.register_next_step_handler(message, com)
    elif message.text == 'Расшифровать':
        bot.send_message(message.chat.id, 'Введите текст формата - 3B4D2A')
        bot.register_next_step_handler(message, decom)
    elif message.text == 'Вики':
        bot.send_message(message.chat.id, 'Что найти в Википедии?')
        bot.register_next_step_handler(message, getwiki)
    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')
@bot.message_handler(content_types=['text'])
def com(message):
    x = message.text
    str_list = []
    count = 1
    for i in range(len(x) - 1):
        if x[i] == x[i + 1]:
            count += 1
        else:
            str_list.append(str(count) + x[i])
            count = 1
    if count > 1 or (x[len(x) - 2] != x[-1]):
        str_list.append(str(count) + x[i])
    bot.send_message(message.chat.id, "".join(str_list))
@bot.message_handler(content_types=['text'])
def decom(message):
    x = message.text
    new_txt = ''
    num = 0
    for i in range(len(x)):
        if x[i].isnumeric():
            num = x[i]
        else:
            new_txt =new_txt + x[i] * int(num)
    bot.send_message(message.chat.id, new_txt)

@bot.message_handler(content_types=['text'])
def getwiki(message):
    try:
        ny = wikipedia.page(message)
        # Получаем первую тысячу символов
        wikitext = ny.content[:1000]
        # Разделяем по точкам
        wikimas = wikitext.split('.')
        # Отбрасываем всЕ после последней точки
        wikimas = wikimas[:-1]
        # Создаем пустую переменную для текста
        wikitext2 = ''
        # Проходимся по строкам, где нет знаков «равно» (то есть все, кроме заголовков)
        for x in wikimas:
            if not ('==' in x):
                # Если в строке осталось больше трех символов, добавляем ее к нашей переменной и возвращаем утерянные при разделении строк точки на место
                if (len((x.strip())) > 3):
                    wikitext2 = wikitext2 + x + '.'
            else:
                break
        # Теперь при помощи регулярных выражений убираем разметку
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\([^()]*\)', '', wikitext2)
        wikitext2 = re.sub('\{[^\{\}]*\}', '', wikitext2)
        # Возвращаем текстовую строку
        bot.send_message(message.chat.id, wikitext2)
    # Обрабатываем исключение, которое мог вернуть модуль wikipedia при запросе
    except Exception as e:
        bot.send_message(message.chat.id, 'В энциклопедии нет информации об этом')

bot.polling(none_stop=True)

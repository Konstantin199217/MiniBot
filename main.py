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
    item5 = telebot.types.KeyboardButton('Угадай число')
    item6 = telebot.types.KeyboardButton('Зодиак')
    item7 = telebot.types.KeyboardButton('Шутка')

    markup.add(item1, item2, item3, item4, item5, item6, item7)

    bot.send_message(message.chat.id, 'Привет! Выбери пункт', reply_markup=markup)


@bot.message_handler(content_types=['text'])
def send_text(message):
    if message.text == 'привет':
        bot.send_message(message.chat.id, 'Привет, как дела?')
    elif message.text == 'Рандомное число':
        bot.send_message(message.chat.id, str(random.randint(1, 100)))
    elif message.text == 'Кинуть кости':
        bot.send_message(message.chat.id, f'Вам выпало {(random.randint(1, 6))} и {(random.randint(1, 6))}')
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
    elif message.text == 'Угадай число':
        bot.send_message(message.chat.id, 'Я загадал число от 1 до 10. Сможешь угадать?')
        bot.register_next_step_handler(message, LucNum)
    elif message.text == 'Зодиак':
        markup = telebot.types.InlineKeyboardMarkup(row_width=2)

        item1 = telebot.types.InlineKeyboardButton('Овен', callback_data='Овен')
        item2 = telebot.types.InlineKeyboardButton('Телец', callback_data='Телец')
        item3 = telebot.types.InlineKeyboardButton('Близнецы', callback_data='Близнецы')
        item4 = telebot.types.InlineKeyboardButton('Рак', callback_data='Рак')
        item5 = telebot.types.InlineKeyboardButton('Лев', callback_data='Лев')
        item6 = telebot.types.InlineKeyboardButton('Дева', callback_data='Дева')
        item7 = telebot.types.InlineKeyboardButton('Весы', callback_data='Весы')
        item8 = telebot.types.InlineKeyboardButton('Скорпион', callback_data='Скорпион')
        item9 = telebot.types.InlineKeyboardButton('Стрелец', callback_data='Стрелец')
        item10 = telebot.types.InlineKeyboardButton('Козерог', callback_data='Козерок')
        item11 = telebot.types.InlineKeyboardButton('Водолей', callback_data='Водолей')
        item12 = telebot.types.InlineKeyboardButton('Рыбы', callback_data='Рыбы')

        markup.add(item1, item2, item3, item4, item5, item6, item7, item8, item9, item10, item11, item12)
        bot.send_message(message.chat.id, 'Выбери свой знак', reply_markup=markup)
    elif message.text == 'Шутка':
        bot.send_message(message.chat.id, 'У семьи каннибалов умер родственник. И грустно и вкусно.')
        bot.send_sticker(message.chat.id, 'CAACAgIAAxkBAAEHBXRjqt44xktdkzaSSTSAMeVyPnSMQgACuw0AAqtwOUpPHwzDGOJ-8SwE')

    else:
        bot.send_message(message.chat.id, 'Я тебя не понимаю')
@bot.callback_query_handler(func=lambda call: True)
def callback_in(call):
    sign = call.data
    print(sign)
    ret = {}
    with open('sign.txt', 'r', encoding='utf-8') as tline:
        for i in range(12):
            str1 = tline.readline().split(':')
            print(str1)
            if str1[0] == sign:
                ret[str1[0]]= str1[1]
    bot.send_message(call.message.chat.id, str(ret))
@bot.message_handler(content_types=['text'])
def LucNum(message):
    num = random.randint(1, 11)
    print(num)
    if message.text == str(num):
        bot.send_message(message.chat.id, 'Да ты ЭКСТРАСЕНС')
    else:
        bot.send_message(message.chat.id, 'Я и не думал что ты угадаешь')


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
            new_txt = new_txt + x[i] * int(num)
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

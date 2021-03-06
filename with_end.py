pip install pyTelegramBotAPI
import telebot
from requests import get
from telebot import types

bot = telebot.TeleBot('1751134716:AAHHDwQ1SW5gTSunprNygu-Q7EQh4KSesEY')

from collections import defaultdict
scores = defaultdict(int)

keyboard = telebot.types.InlineKeyboardMarkup()
key_memes = telebot.types.InlineKeyboardButton(text='Мемы', callback_data='memes')
keyboard.add(key_memes)
key_quotes = telebot.types.InlineKeyboardButton(text='Цитаты преподавателей', callback_data='quotes')
keyboard.add(key_quotes)
key_organisation = telebot.types.InlineKeyboardButton(text='Организация учебного процесса', callback_data='organisation')
keyboard.add(key_organisation)


@bot.message_handler(commands=['start'])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Выбери раздел:', reply_markup=keyboard)
    


@bot.callback_query_handler(
    func=lambda call: call.data == 'memes' or call.data == 'quotes' or call.data == 'organisation')
def callback_worker(call):
    if call.data == 'memes':
        bot.send_message(call.message.chat.id, '''В каждом задании этого раздела вам будет показан мем, 
связанный с нашим потоком. Вам нужно будет выбрать один вариант ответа или ввести слово.''')
        bot.send_photo(call.message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/chicken.jpg?raw=true').content)  # про курицу
        mesg = bot.send_message(call.message.chat.id, 'Введите слово:')
        bot.register_next_step_handler(mesg, meme1)
    elif call.data == 'quotes':
        bot.send_message(call.message.chat.id,
                         '''В этом разделе тебе будут показаны цитаты преподавателей. Отгадай, кому они принадлежат.''')
        mesg = bot.send_message(call.message.chat.id,
                                'Чья цитата? Введи сначала имя, потом фамилию преподавателя. \n"Видите ли вы эту красивую табличку с буквами? Она вам нравится или вызывает ужас? Вы пока подумайте, а я включу «Щенячий патруль»".')
        bot.register_next_step_handler(mesg, quote1)
    elif call.data == 'organisation':
        bot.send_message(call.message.chat.id, '''В этом разделе будут вопросы, связанные с учебным процессом на фикле. 
Выберите верный вариант ответа или введите слово.''')

        keyboard_org = types.ReplyKeyboardMarkup(one_time_keyboard = True)
        key_var1 = types.KeyboardButton("фонетика")
        key_var2 = types.KeyboardButton("социолингвистика")
        key_var3 = types.KeyboardButton("академическое письмо")
        key_var4 = types.KeyboardButton("пары по языкам")
        keyboard_org.row(key_var1, key_var2)
        keyboard_org.row(key_var3, key_var4)
        r = bot.send_message(call.message.chat.id, "Какие семинары загадочно исчезают из РУЗа?", reply_markup=keyboard_org)
        bot.register_next_step_handler(r, organisation1)


        
        
def organisation1(org1): 
    if org1.text == "/end":
        bot.send_message(org1.chat.id, "Заканчиваем...") 
        end_message(org1) 
    elif org1.text == 'фонетика':
        scores[org1.from_user.id] += 1
        r = bot.send_message(org1.chat.id, 'Верно!', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(False, True)
        itembtna = types.KeyboardButton('Юрий Александрович')
        itembtnv = types.KeyboardButton('Михаил Александрович')
        itembtnc = types.KeyboardButton('Владимир Владимирович')
        itembtnd = types.KeyboardButton('Андриан Викторович')
        markup.row(itembtna, itembtnv)
        markup.row(itembtnc, itembtnd)
        r1 = bot.send_message(org1.chat.id, "Как зовут Ландера?", reply_markup=markup)
        bot.register_next_step_handler(r1, organisation2)
    elif org1.text == 'социолингвистика' or org1.text == 'академическое письмо' or org1.text == 'пары по языкам':
        r = bot.send_message(org1.chat.id, 'Нет( \nправильный ответ: фонетика', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(False, True)
        itembtna = types.KeyboardButton('Юрий Александрович')
        itembtnv = types.KeyboardButton('Михаил Александрович')
        itembtnc = types.KeyboardButton('Владимир Владимирович')
        itembtnd = types.KeyboardButton('Андриан Викторович')
        markup.row(itembtna, itembtnv)
        markup.row(itembtnc, itembtnd)
        r1 = bot.send_message(org1.chat.id, "Как зовут Ландера?", reply_markup=markup)
        bot.register_next_step_handler(r1, organisation2)

def organisation2(org2):
    if org2.text == "/end":
        bot.send_message(org2.chat.id, "Заканчиваем...") 
        end_message(org2)
    elif org2.text == 'Юрий Александрович':
        scores[org2.from_user.id] += 1
        bot.send_message(org2.chat.id, 'Верно!', reply_markup=types.ReplyKeyboardRemove())
        r2 = bot.send_message(org2.chat.id, "На каком этаже находится учебный офис ФиКЛ? Введите число")
        bot.register_next_step_handler(r2, organisation3)
    elif org2.text == 'Михаил Александрович' or org2.text == 'Владимир Владимирович' or org2.text == 'Андриан Викторович':
        bot.send_message(org2.chat.id, 'Нет( \nправильный ответ: Юрий Александрович', reply_markup=types.ReplyKeyboardRemove())
        r2 = bot.send_message(org2.chat.id, "На каком этаже находится учебный офис ФиКЛ? Введите число")
        bot.register_next_step_handler(r2, organisation3)        
        
def organisation3(org3):
    if org3.text == "/end":
        bot.send_message(org3.chat.id, "Заканчиваем...")
        end_message(org3)
    elif org3.text == '4':
        scores[org3.from_user.id] += 1
        bot.send_message(org3.chat.id, 'Да!', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(False, True)
        itembtna = types.KeyboardButton('мемы')
        itembtnv = types.KeyboardButton('музыку')
        itembtnc = types.KeyboardButton('фотографии Ландера')
        itembtnd = types.KeyboardButton('лингвистические опросы')
        itembtne = types.KeyboardButton('скрины писем из учебного офиса')
        markup.row(itembtna, itembtnv)
        markup.row(itembtnc, itembtnd)
        markup.row(itembtne)
        r3 = bot.send_message(org3.chat.id, "Что отправляют в беседу чаще всего?", reply_markup=markup)
        bot.register_next_step_handler(r3, organisation4)
    else:
        bot.send_message(org3.chat.id, 'Нет( \nправильный ответ: 4', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(False, True)
        itembtna = types.KeyboardButton('мемы')
        itembtnv = types.KeyboardButton('музыку')
        itembtnc = types.KeyboardButton('фотографии Ландера')
        itembtnd = types.KeyboardButton('лингвистические опросы')
        itembtne = types.KeyboardButton('скрины писем из учебного офиса')
        markup.row(itembtna, itembtnv)
        markup.row(itembtnc, itembtnd)
        markup.row(itembtne)
        r3 = bot.send_message(org3.chat.id, "Что отправляют в беседу чаще всего?", reply_markup=markup)
        bot.register_next_step_handler(r3, organisation4)       
                
def organisation4(org4):
    if org4.text == "/end":
        bot.send_message(org4.chat.id, "Заканчиваем...")
        end_message(org4)
    elif org4.text == 'лингвистические опросы':
        scores[org4.from_user.id] += 1
        r4 = bot.send_message(org4.chat.id, 'Да!', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(False, True)
        itembtna = types.KeyboardButton('лингвисты 2020')
        itembtnv = types.KeyboardButton('лесбисты(-ки)’20')
        itembtnc = types.KeyboardButton('лингвистки’20')
        itembtnd = types.KeyboardButton('лесбистки(-ы)’20')
        markup.row(itembtna, itembtnv)
        markup.row(itembtnc, itembtnd)
        bot.send_message(org4.chat.id, "Как называется беседа потока?", reply_markup=markup)
        bot.register_next_step_handler(r4, organisation5)
    else:
        r4 = bot.send_message(org4.chat.id, 'Нет( \nправильный ответ: лингвистические опросы', reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(selective = False)
        itembtna = types.KeyboardButton('лингвисты 2020')
        itembtnv = types.KeyboardButton('лесбисты(-ки)’20')
        itembtnc = types.KeyboardButton('лингвистки’20')
        itembtnd = types.KeyboardButton('лесбистки(-ы)’20')
        markup.row(itembtna, itembtnv)
        markup.row(itembtnc, itembtnd)
        bot.send_message(org4.chat.id, "Как называется беседа потока?", reply_markup=markup)
        bot.register_next_step_handler(r4, organisation5)   
                        
def organisation5(org5):
    if org5.text == "/end":
        bot.send_message(org5.chat.id, "Заканчиваем...")
        end_message(org5)
    elif org5.text == "лесбистки(-ы)’20":
        scores[org5.from_user.id] += 1
        bot.send_message(org5.chat.id, "Да!", reply_markup=types.ReplyKeyboardRemove())        
    else:
        bot.send_message(org5.chat.id, "Нет( \nправильный ответ: лесбистки(-ы)’20", reply_markup=types.ReplyKeyboardRemove())

       
  
        
@bot.message_handler(func=lambda message: True)
def meme1(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text.lower() == 'курица':
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/phonetics.jpg?raw=true').content)  # не успел сдать тест по фонетике
        keyboard_memes = telebot.types.ReplyKeyboardMarkup(False, True)
        keyboard_memes.row("тест по фонетике")
        keyboard_memes.row("домашку по проге")
        keyboard_memes.row("контрольную по латыни")
        mesg = bot.send_message(message.chat.id, "Не успел сдать ...", reply_markup=keyboard_memes)
        bot.register_next_step_handler(mesg, meme2)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: курица')
        bot.send_photo(message.chat.id,
                       get('https://github.com/ioiimm/drafts/blob/main/bot/img/phonetics.jpg?raw=true').content)
        keyboard_memes = telebot.types.ReplyKeyboardMarkup(False, True)
        keyboard_memes.row("тест по фонетике")
        keyboard_memes.row("домашку по проге")
        keyboard_memes.row("контрольную по латыни")
        mesg = bot.send_message(message.chat.id, "Не успел сдать ...", reply_markup=keyboard_memes)
        bot.register_next_step_handler(mesg, meme2)


def meme2(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == "тест по фонетике":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/dobrushina.jpg?raw=true').content)  # здравствуйте, Добрушина
        keyboard_memes = telebot.types.ReplyKeyboardMarkup(False, True)
        keyboard_memes.row("Добрушина, эксперимент")
        keyboard_memes.row("Зибер, тест по артикуляции")
        keyboard_memes.row("Ландер, экспедицию в Индонезию")
        keyboard_memes.row("учебный офис, РУЗ")
        mesg = bot.send_message(message.chat.id, "Здравствуйте ... одобрите ... :", reply_markup=keyboard_memes)
        bot.register_next_step_handler(mesg, meme3)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: тест по фонетике')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/dobrushina.jpg?raw=true').content)  # здравствуйте, Добрушина
        keyboard_memes = telebot.types.ReplyKeyboardMarkup(False, True)
        keyboard_memes.row("Добрушина, эксперимент")
        keyboard_memes.row("Зибер, тест по артикуляции")
        keyboard_memes.row("Ландер, экспедицию в Индонезию")
        keyboard_memes.row("учебный офис, РУЗ")
        mesg = bot.send_message(message.chat.id, "Здравствуйте ... одобрите ... :", reply_markup=keyboard_memes)
        bot.register_next_step_handler(mesg, meme3)


def meme3(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == "Добрушина, эксперимент":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/daniel.jpg?raw=true').content)  # Михаил Даниэль
        mesg = bot.send_message(message.chat.id, "Кто на картинке? Введите имя и фамилию.")
        bot.register_next_step_handler(mesg, meme4)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: Добрушина, эксперимент')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/daniel.jpg?raw=true').content)  # Михаил Даниэль
        mesg = bot.send_message(message.chat.id, "Кто на картинке? Введите имя и фамилию.")
        bot.register_next_step_handler(mesg, meme4)


def meme4(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text.lower() == "Михаил Даниэль".lower():
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
        bot.send_photo(message.chat.id,
                       get('https://github.com/ioiimm/drafts/blob/main/bot/img/lms.jpg?raw=true').content)  # лмс
        mesg = bot.send_message(message.chat.id, "Кто / что на фото? Введите одно слово:")
        bot.register_next_step_handler(mesg, meme5)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: Михаил Даниэль')
        bot.send_photo(message.chat.id,
                       get('https://github.com/ioiimm/drafts/blob/main/bot/img/lms.jpg?raw=true').content)  # лмс
        mesg = bot.send_message(message.chat.id, "Кто / что на фото? Введите одно слово:")
        bot.register_next_step_handler(mesg, meme5)


def meme5(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text.lower() == "лмс" or message.text.lower() == "lms":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/causativ.jpg?raw=true').content)  # каузация
        mesg = bot.send_message(message.chat.id, "Введите слово:")
        bot.register_next_step_handler(mesg, meme6)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: lms или лмс')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/causativ.jpg?raw=true').content)
        mesg = bot.send_message(message.chat.id, "Введите слово:")
        bot.register_next_step_handler(mesg, meme6)


def meme6(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text.lower() == "каузация" or message.text.lower() == "каузацию":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
        bot.send_photo(message.chat.id,
                       get('https://github.com/ioiimm/drafts/blob/main/bot/img/stenin.jpg?raw=true').content)  # Стенин
        mesg = bot.send_message(message.chat.id, "Кто на фото? Введите фамилию:")
        bot.register_next_step_handler(mesg, meme6_reply)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: каузация или каузацию')
        bot.send_photo(message.chat.id,
                       get('https://github.com/ioiimm/drafts/blob/main/bot/img/stenin.jpg?raw=true').content)  # Стенин
        mesg = bot.send_message(message.chat.id, "Кто на фото? Введите фамилию:")
        bot.register_next_step_handler(mesg, meme6_reply)


def meme6_reply(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text.lower() == "стенин":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: Стенин')


@bot.message_handler(func=lambda message: True)
def quote1(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
        
    elif message.text.lower() == 'инна зибер':
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id,
                         'Совершенно верно! Сразу видно, что смотришь все лекции и читаешь все письма :)')
        mesg = bot.send_message(message.chat.id,
                                'Чья цитата? Введи сначала имя, потом фамилию преподавателя. \n"Надеюсь, скоро станет попроще".')
        bot.register_next_step_handler(mesg, quote2)
    else:
        bot.send_message(message.chat.id, 'Ошибочка! Правильный ответ: Инна Зибер.')
        mesg = bot.send_message(message.chat.id,
                                'Чья цитата? Введи сначала имя, потом фамилию преподавателя. \n"Надеюсь, скоро станет попроще".')
        bot.register_next_step_handler(mesg, quote2)


def quote2(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text.lower() == 'юрий ландер':
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id,
                         'Совершенно верно! Сразу видно, что смотришь все лекции и читаешь все письма :)')
        mesg = bot.send_message(message.chat.id,
                                'Чья цитата? Введи сначала имя, потом фамилию преподавателя. \n"Будет чтение разных уровней сложности: иногда попроще, иногда полегче".')
        bot.register_next_step_handler(mesg, quote3)
    else:
        bot.send_message(message.chat.id, 'Ошибочка! Правильный ответ: Юрий Ландер.')
        mesg = bot.send_message(message.chat.id,
                                'Чья цитата? Введи сначала имя, потом фамилию преподавателя. \n"Будет чтение разных уровней сложности: иногда попроще, иногда полегче".')
        bot.register_next_step_handler(mesg, quote3)


def quote3(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text.lower() == "михаил даниэль":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id,
                         'Совершенно верно! Сразу видно, что смотришь все лекции и читаешь все письма :)')
    else:
        bot.send_message(message.chat.id, 'Ошибочка! Правильный ответ: Михаил Даниэль.')


@bot.message_handler(commands=['end'])
def end_message(end_m):
    perc = scores[end_m.from_user.id]/15*100
    if perc > 0 and perc <= 29: 
        text_res = "кажется, ты не с фикла… но можешь перевестись сюда!"
    elif perc > 29 and perc <= 54:
        text_res = "наверно, ты мало ходил на  пары. ну ничего, впереди еще три года."
    elif perc > 54 and perc <= 79:
        text_res = "есть недочеты, но ты молодец!"   
    elif perc > 79 and perc <= 100:
        text_res = "ты настоящий фиклёнок!"
    bot.send_message(end_m.chat.id, text_res)
    scores[end_m.from_user.id] = 0
        
bot.polling()

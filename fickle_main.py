import telebot
from requests import get
from telebot import types
from collections import defaultdict
import emoji

scores = defaultdict(int)
sections = defaultdict(int)
sections_lst = defaultdict(list)
sections_check = defaultdict(list)

bot = telebot.TeleBot('1751134716:AAHHDwQ1SW5gTSunprNygu-Q7EQh4KSesEY')

keyboard = telebot.types.InlineKeyboardMarkup()
key_memes = telebot.types.InlineKeyboardButton(text='Мемы', callback_data='memes')
keyboard.add(key_memes)
key_quotes = telebot.types.InlineKeyboardButton(text='Цитаты преподавателей', callback_data='quotes')
keyboard.add(key_quotes)
key_organisation = telebot.types.InlineKeyboardButton(text='Организация учебного процесса',
                                                      callback_data='organisation')
keyboard.add(key_organisation)


@bot.message_handler(commands=['start'])
def start_message(message):
    global sections, sections_lst, sections_check
    scores[message.from_user.id] = 0
    sections_lst[message.from_user.id].clear()
    sections_check[message.from_user.id].clear()
    sections[message.from_user.id] = 0
    bot.send_photo(message.chat.id, get(
        'https://github.com/ioiimm/drafts/blob/main/bot/img/beauty.jpg?raw=true').content)
    bot.send_message(message.chat.id, '''Привет!
Этот прекрасный тест команда нашего проекта создала специально для 1 курса ОП “Фундаментальная и компьютерная лингвистика” НИУ ВШЭ (если ты не с фикла, тоже можешь попробовать пройти его!). 
Ответив на все вопросы, ты узнаешь, насколько хорошо ты разбираешься в мемах, цитатах преподавателей и организации учебного процесса на нашей любимой программе!\n
Вот несколько команд, которые могут тебе помочь:\n
/start – собственно начинает игру\n
/next – если тебе наскучил какой-то раздел, можешь перейти к следующему (но осторожно, обратно вернуться не получится!)\n
/end – в любой момент заканчивает игру и подсчитывает число набранных баллов
''', reply_markup=types.ReplyKeyboardRemove())
    bot.send_message(message.chat.id, 'Выбери раздел:', reply_markup=keyboard)


@bot.message_handler(commands=['next'])
def next_message(next_m):
    global sections, sections_lst, sections_check
    sections[next_m.from_user.id] += 1
    if sections[next_m.from_user.id] == 1:
        if "Мемы" in sections_check[next_m.from_user.id]:
            keyboard_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_next_step.row("Организация учебного процесса")
            keyboard_next_step.row("Цитаты преподавателей")
            mesg = bot.send_message(next_m.chat.id, "Выбери следующий раздел:", reply_markup=keyboard_next_step)
            bot.register_next_step_handler(mesg, meme_next_step1)
        elif "Организация учебного процесса" in sections_check[next_m.from_user.id]:
            keyboard_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_next_step.row("Мемы")
            keyboard_next_step.row("Цитаты преподавателей")
            mesg = bot.send_message(next_m.chat.id, "Выбери следующий раздел:", reply_markup=keyboard_next_step)
            bot.register_next_step_handler(mesg, org_next_step1)
        elif "Цитаты преподавателей" in sections_check[next_m.from_user.id]:
            keyboard_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_next_step.row("Организация учебного процесса")
            keyboard_next_step.row("Мемы")
            mesg = bot.send_message(next_m.chat.id, "Выбери следующий раздел:", reply_markup=keyboard_next_step)
            bot.register_next_step_handler(mesg, quote_next_step1)
    elif sections[next_m.from_user.id] == 2:
        if "Цитаты преподавателей" not in sections_check[next_m.from_user.id]:
            keyboard_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_next_step.row("Цитаты преподавателей")
            mesg = bot.send_message(next_m.chat.id, "Выбери следующий раздел:",
                                    reply_markup=keyboard_next_step)
            bot.register_next_step_handler(mesg, org_next_step1)
        elif "Мемы" not in sections_check[next_m.from_user.id]:
            keyboard_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_next_step.row("Мемы")
            mesg = bot.send_message(next_m.chat.id, "Выбери следующий раздел:",
                                    reply_markup=keyboard_next_step)
            bot.register_next_step_handler(mesg, org_next_step1)
        elif "Организация учебного процесса" not in sections_check[next_m.from_user.id]:
            keyboard_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_next_step.row("Организация учебного процесса")
            mesg = bot.send_message(next_m.chat.id, "Выбери следующий раздел:",
                                    reply_markup=keyboard_next_step)
            bot.register_next_step_handler(mesg, quote_next_step1)
    else:
        bot.send_message(next_m.chat.id, "Вы все сделали!\nЗаканчиваем...", reply_markup=types.ReplyKeyboardRemove())
        end_message(next_m)


@bot.message_handler(commands=['end'])
def end_message(end_m):
    global sections, sections_lst, sections_check
    text_res = "Твои баллы: " + str(scores[end_m.from_user.id]) + " из 17" + "\n"
    bot.send_message(end_m.chat.id, text_res, reply_markup=types.ReplyKeyboardRemove())
    perc = scores[end_m.from_user.id] / 17 * 100
    if 0 <= perc <= 29:
        text_res = emoji.emojize('''Все мы, как редуцированные, падаем… Это нормально! Главное вовремя встать и поехать к первой паре на Басмач… Ты хорошо постарался! Желаем, чтобы ридинги Даниэля действительно были попроще и полегче, а лмс никогда не ложился… 
Неважно, сколько баллов ты набрал… Важно, что мы одна большая лингвистическая семья и все мы найдем работу (наверно)! :green_heart:\n
Мы рады, что ты прошёл/прошла этот тест! Желаем хорошего завершения года и успешной сдачи экзаменов :two_hearts:''', use_aliases=True)
        bot.send_message(end_m.chat.id, text_res)
    elif 29 < perc <= 54:
        text_res = emoji.emojize('''Ты молодец! Однако мир лингвистики еще полон тайн и загадок, которые тебе предстоит раскрыть… Не отчаивайся, когда что-то не получается. Если тебе грустно, в столовой всегда ждет комплексный обед за 135 рублей! И, конечно же, твои любимые однокурсники, которые всегда готовы прийти на помощь (и сделать лингвистические опросы в нашей беседе). :blue_heart:\n
Мы рады, что ты прошёл/прошла этот тест! Желаем хорошего завершения года и успешной сдачи экзаменов :two_hearts:''', use_aliases=True)
        bot.send_message(end_m.chat.id, text_res)
    elif 54 < perc <= 79:
        text_res = emoji.emojize('''Ты замечательно справился с тестом! Сразу видно, что ты выдержал все лаги руза, внезапные квизы и контрольные работы по фонетике и фонологии… Надеемся, что ты пересмотришь все лекции Инны Зибер и все серии “Щенячьего патруля”, прочитаешь все статьи по социолингвистике и загрузишь курсач в лмс до дедлайна! 
Мы уверены, что ты никогда не опаздываешь на лучшие в мире занятия Школы Лингвистики, потому что твои часы еще точнее, чем часы Даниэля! :purple_heart:\n
Мы рады, что ты прошёл/прошла этот тест! Желаем хорошего завершения года и успешной сдачи экзаменов :two_hearts:''', use_aliases=True)
        bot.send_message(end_m.chat.id, text_res)
    elif 79 < perc <= 100:
        text_res = emoji.emojize('''Отличный результат! Ты прошел все испытания первого курса фикла… Прочитал все ридинги Даниэля… Решил все задачи по проге… Наверно, ты даже умеешь произносить эйективные согласные и [ɬ]… Твой курсач, скорее всего, уже загружен в лмс… Команда нашего проекта гордится такими людьми, как ты! 
Мы уверены, что ты войдешь в те самые 10% потока с отличными оценками! Желаем тебе попить чай с Екатериной Владимировной Рахилиной на собрании потока (не в зуме!). Не сомневаемся, что ты станешь ведущим лингвистом России и будущие студенты НИУ ВШЭ будут учиться по твоим учебникам! :heart:\n
Мы рады, что ты прошёл/прошла этот тест! Желаем хорошего завершения года и успешной сдачи экзаменов :two_hearts:''', use_aliases=True)
        bot.send_message(end_m.chat.id, text_res)
    bot.send_photo(end_m.chat.id, get(
        'https://github.com/ioiimm/drafts/blob/main/bot/img/dog.jpg?raw=true').content)
    scores[end_m.from_user.id] = 0
    sections_lst[end_m.from_user.id].clear()
    sections_check[end_m.from_user.id].clear()
    sections[end_m.from_user.id] = 0


@bot.message_handler(content_types=['text', 'photo', 'audio', 'document'])
def send_text(message):
    bot.send_message(message.chat.id, 'Прости, я тебя не понимаю. Попробуй написать /start')


@bot.callback_query_handler(
    func=lambda call: call.data == 'memes' or call.data == 'quotes' or call.data == 'organisation')
def callback_worker(call):
    global sections_lst
    if call.data == 'memes':
        sections_lst[call.message.from_user.id].append('Мемы')
        bot.send_message(call.message.chat.id, '''В каждом задании этого раздела вам будет показан мем, 
связанный с нашим потоком. Вам нужно будет выбрать один вариант ответа или ввести слово.''', reply_markup=types.ReplyKeyboardRemove())
        bot.send_photo(call.message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/chicken.jpg?raw=true').content)
        mesg = bot.send_message(call.message.chat.id, 'Введите слово:')
        bot.register_next_step_handler(mesg, meme1)
    elif call.data == 'quotes':
        sections_lst[call.message.from_user.id].append('Цитаты преподавателей')
        bot.send_message(call.message.chat.id, '''В этом разделе тебе будут показаны цитаты преподавателей. 
Отгадай, кому они принадлежат.''', reply_markup=types.ReplyKeyboardRemove())
        mesg = bot.send_message(call.message.chat.id, '''Чья цитата? Введи сначала имя, потом фамилию преподавателя. '
\n"Видите ли вы эту красивую табличку с буквами? Она вам нравится или вызывает ужас? Вы пока подумайте, а я включу 
«Щенячий патруль»".''')
        bot.register_next_step_handler(mesg, quote1)
    elif call.data == 'organisation':
        sections_lst[call.message.from_user.id].append('Организация учебного процесса')
        bot.send_message(call.message.chat.id, '''В этом разделе будут вопросы, связанные с учебным процессом на фикле. 
Выберите верный вариант ответа или введите слово.''', reply_markup=types.ReplyKeyboardRemove())

        keyboard_org = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        key_var1 = types.KeyboardButton("фонетика")
        key_var2 = types.KeyboardButton("социолингвистика")
        key_var3 = types.KeyboardButton("академическое письмо")
        key_var4 = types.KeyboardButton("пары по языкам")
        keyboard_org.row(key_var1, key_var2)
        keyboard_org.row(key_var3, key_var4)
        r = bot.send_message(call.message.chat.id, "Какие семинары загадочно исчезают из РУЗа?",
                             reply_markup=keyboard_org)
        bot.register_next_step_handler(r, organisation1)


def organisation1(org1):
    global sections_check
    sections_check[org1.from_user.id].append('Организация учебного процесса')
    if org1.text == "/end":
        bot.send_message(org1.chat.id, "Заканчиваем...", reply_markup=types.ReplyKeyboardRemove())
        end_message(org1)
    elif org1.text == '/start':
        bot.send_message(org1.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif org1.text == '/next':
        bot.send_message(org1.chat.id, "Перехожу в следующий раздел...")
        next_message(org1)
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
        r = bot.send_message(org1.chat.id, 'Нет( \nправильный ответ: фонетика',
                             reply_markup=types.ReplyKeyboardRemove())
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
        bot.send_message(org2.chat.id, "Заканчиваем...", reply_markup=types.ReplyKeyboardRemove())
        end_message(org2)
    elif org2.text == '/start':
        bot.send_message(org2.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif org2.text == '/next':
        bot.send_message(org2.chat.id, "Перехожу в следующий раздел...")
        next_message(org2)
    elif org2.text == 'Юрий Александрович':
        scores[org2.from_user.id] += 1
        bot.send_message(org2.chat.id, 'Верно!', reply_markup=types.ReplyKeyboardRemove())
        r2 = bot.send_message(org2.chat.id, "На каком этаже находится учебный офис ФиКЛ? Введите число")
        bot.register_next_step_handler(r2, organisation3)
    elif org2.text == 'Михаил Александрович' or org2.text == 'Владимир Владимирович' or org2.text == 'Андриан Викторович':
        bot.send_message(org2.chat.id, 'Нет( \nправильный ответ: Юрий Александрович',
                         reply_markup=types.ReplyKeyboardRemove())
        r2 = bot.send_message(org2.chat.id, "На каком этаже находится учебный офис ФиКЛ? Введите число")
        bot.register_next_step_handler(r2, organisation3)


def organisation3(org3):
    if org3.text == "/end":
        bot.send_message(org3.chat.id, "Заканчиваем...", reply_markup=types.ReplyKeyboardRemove())
        end_message(org3)
    elif org3.text == '/start':
        bot.send_message(org3.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif org3.text == '/next':
        bot.send_message(org3.chat.id, "Перехожу в следующий раздел...")
        next_message(org3)
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
        bot.send_message(org4.chat.id, "Заканчиваем...", reply_markup=types.ReplyKeyboardRemove())
        end_message(org4)
    elif org4.text == '/start':
        bot.send_message(org4.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif org4.text == '/next':
        bot.send_message(org4.chat.id, "Перехожу в следующий раздел...")
        next_message(org4)
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
        r4 = bot.send_message(org4.chat.id, 'Нет( \nправильный ответ: лингвистические опросы',
                              reply_markup=types.ReplyKeyboardRemove())
        markup = types.ReplyKeyboardMarkup(selective=False)
        itembtna = types.KeyboardButton('лингвисты 2020')
        itembtnv = types.KeyboardButton('лесбисты(-ки)’20')
        itembtnc = types.KeyboardButton('лингвистки’20')
        itembtnd = types.KeyboardButton('лесбистки(-ы)’20')
        markup.row(itembtna, itembtnv)
        markup.row(itembtnc, itembtnd)
        bot.send_message(org4.chat.id, "Как называется беседа потока?", reply_markup=markup)
        bot.register_next_step_handler(r4, organisation5)


def organisation5(org5):
    global sections
    if org5.text == "/end":
        bot.send_message(org5.chat.id, "Заканчиваем...", reply_markup=types.ReplyKeyboardRemove())
        end_message(org5)
    elif org5.text == '/start':
        bot.send_message(org5.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif org5.text == '/next':
        bot.send_message(org5.chat.id, "Перехожу в следующий раздел...")
        next_message(org5)
    elif org5.text == "лесбистки(-ы)’20":
        scores[org5.from_user.id] += 1
        bot.send_message(org5.chat.id, "Да!", reply_markup=types.ReplyKeyboardRemove())
        sections[org5.from_user.id] += 1
        if sections[org5.from_user.id] != 3:
            keyboard_org_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_org_next_step.row("завершить тест")
            keyboard_org_next_step.row("выбрать следующий раздел")
            mesg = bot.send_message(org5.chat.id, "Завершить тест или продолжить дальше?",
                                    reply_markup=keyboard_org_next_step)
            bot.register_next_step_handler(mesg, org_next_step)
        else:
            bot.send_message(org5.chat.id, "Вы все сделали!\nЗаканчиваем...", reply_markup=types.ReplyKeyboardRemove())
            end_message(org5)
    else:
        bot.send_message(org5.chat.id, "Нет( \nправильный ответ: лесбистки(-ы)’20",
                         reply_markup=types.ReplyKeyboardRemove())
        sections[org5.from_user.id] += 1
        if sections[org5.from_user.id] != 3:
            keyboard_org_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_org_next_step.row("завершить тест")
            keyboard_org_next_step.row("выбрать следующий раздел")
            mesg = bot.send_message(org5.chat.id, "Завершить тест или продолжить дальше?",
                                    reply_markup=keyboard_org_next_step)
            bot.register_next_step_handler(mesg, org_next_step)
        else:
            bot.send_message(org5.chat.id, "Вы все сделали!\nЗаканчиваем...", reply_markup=types.ReplyKeyboardRemove())
            end_message(org5)


def org_next_step(message):
    global sections, sections_lst
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "завершить тест":
        bot.send_message(message.chat.id, "Заканчиваем...", reply_markup=types.ReplyKeyboardRemove())
        end_message(message)
    elif message.text == "выбрать следующий раздел":
        if sections[message.from_user.id] == 1:
            keyboard_org_next_step1 = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_org_next_step1.row("Мемы")
            keyboard_org_next_step1.row("Цитаты преподавателей")
            mesg = bot.send_message(message.chat.id, "Выбери следующий раздел:", reply_markup=keyboard_org_next_step1)
            bot.register_next_step_handler(mesg, org_next_step1)
        elif sections[message.from_user.id] == 2:
            if "Мемы" in sections_lst[message.from_user.id]:
                keyboard_org_next_step1 = telebot.types.ReplyKeyboardMarkup(False, True)
                keyboard_org_next_step1.row("Цитаты преподавателей")
                mesg = bot.send_message(message.chat.id, "Выбери следующий раздел:",
                                        reply_markup=keyboard_org_next_step1)
                bot.register_next_step_handler(mesg, org_next_step1)
            else:
                keyboard_org_next_step1 = telebot.types.ReplyKeyboardMarkup(False, True)
                keyboard_org_next_step1.row("Мемы")
                mesg = bot.send_message(message.chat.id, "Выбери следующий раздел:",
                                        reply_markup=keyboard_org_next_step1)
                bot.register_next_step_handler(mesg, org_next_step1)


def org_next_step1(message):
    global sections_lst
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "Цитаты преподавателей":
        sections_lst[message.from_user.id].append("Цитаты преподавателей")
        bot.send_message(message.chat.id,
                         '''В этом разделе тебе будут показаны цитаты преподавателей. Отгадай, кому они принадлежат.''')
        mesg = bot.send_message(message.chat.id, '''Чья цитата? Введи сначала имя, потом фамилию преподавателя. 
\n"Видите ли вы эту красивую табличку с буквами? Она вам нравится или вызывает ужас? Вы пока подумайте, а я включу 
«Щенячий патруль»".''')
        bot.register_next_step_handler(mesg, quote1)
    elif message.text == "Мемы":
        sections_lst[message.from_user.id].append("Мемы")
        bot.send_message(message.chat.id, '''В каждом задании этого раздела вам будет показан мем, 
связанный с нашим потоком. Вам нужно будет выбрать один вариант ответа или ввести слово.''')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/chicken.jpg?raw=true').content)
        mesg = bot.send_message(message.chat.id, 'Введите слово:')
        bot.register_next_step_handler(mesg, meme1)


@bot.message_handler(func=lambda message: True)
def meme1(message):
    global sections_check
    sections_check[message.from_user.id].append('Мемы')
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == '/next':
        bot.send_message(message.chat.id, "Перехожу в следующий раздел...")
        next_message(message)
    elif message.text.lower() == 'курица':
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/phonetics.jpg?raw=true').content)
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
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...", reply_markup=types.ReplyKeyboardRemove())
        end_message(message)
    elif message.text == '/next':
        bot.send_message(message.chat.id, "Перехожу в следующий раздел...")
        next_message(message)
    elif message.text == "тест по фонетике":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!', reply_markup=types.ReplyKeyboardRemove())
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/dobrushina.jpg?raw=true').content)
        keyboard_memes = telebot.types.ReplyKeyboardMarkup(False, True)
        keyboard_memes.row("Добрушина, эксперимент")
        keyboard_memes.row("Зибер, тест по артикуляции")
        keyboard_memes.row("Ландер, экспедицию в Индонезию")
        keyboard_memes.row("учебный офис, РУЗ")
        mesg = bot.send_message(message.chat.id, "Здравствуйте ... одобрите ... :", reply_markup=keyboard_memes)
        bot.register_next_step_handler(mesg, meme3)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: тест по фонетике',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/dobrushina.jpg?raw=true').content)
        keyboard_memes = telebot.types.ReplyKeyboardMarkup(False, True)
        keyboard_memes.row("Добрушина, эксперимент")
        keyboard_memes.row("Зибер, тест по артикуляции")
        keyboard_memes.row("Ландер, экспедицию в Индонезию")
        keyboard_memes.row("учебный офис, РУЗ")
        mesg = bot.send_message(message.chat.id, "Здравствуйте ... одобрите ... :", reply_markup=keyboard_memes)
        bot.register_next_step_handler(mesg, meme3)


def meme3(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...", reply_markup=types.ReplyKeyboardRemove())
        end_message(message)
    elif message.text == '/next':
        bot.send_message(message.chat.id, "Перехожу в следующий раздел...")
        next_message(message)
    elif message.text == "Добрушина, эксперимент":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!', reply_markup=types.ReplyKeyboardRemove())
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/daniel.jpg?raw=true').content)
        mesg = bot.send_message(message.chat.id, "Кто на картинке? Введите имя и фамилию.")
        bot.register_next_step_handler(mesg, meme4)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: Добрушина, эксперимент',
                         reply_markup=types.ReplyKeyboardRemove())
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/daniel.jpg?raw=true').content)
        mesg = bot.send_message(message.chat.id, "Кто на картинке? Введите имя и фамилию.")
        bot.register_next_step_handler(mesg, meme4)


def meme4(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == '/next':
        bot.send_message(message.chat.id, "Перехожу в следующий раздел...")
        next_message(message)
    elif message.text.lower() == "Михаил Даниэль".lower():
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
        bot.send_photo(message.chat.id,
                       get('https://github.com/ioiimm/drafts/blob/main/bot/img/lms.jpg?raw=true').content)
        mesg = bot.send_message(message.chat.id, "Кто / что на фото? Введите одно слово:")
        bot.register_next_step_handler(mesg, meme5)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: Михаил Даниэль')
        bot.send_photo(message.chat.id,
                       get('https://github.com/ioiimm/drafts/blob/main/bot/img/lms.jpg?raw=true').content)
        mesg = bot.send_message(message.chat.id, "Кто / что на фото? Введите одно слово:")
        bot.register_next_step_handler(mesg, meme5)


def meme5(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == '/next':
        bot.send_message(message.chat.id, "Перехожу в следующий раздел...")
        next_message(message)
    elif message.text.lower() == "лмс" or message.text.lower() == "lms":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/causativ.jpg?raw=true').content)
        mesg = bot.send_message(message.chat.id, "Введите слово:")
        bot.register_next_step_handler(mesg, meme6)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: lms или лмс')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/causativ.jpg?raw=true').content)
        mesg = bot.send_message(message.chat.id, "Введите слово:")
        bot.register_next_step_handler(mesg, meme6)


def meme6(message):
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == '/next':
        bot.send_message(message.chat.id, "Перехожу в следующий раздел...")
        next_message(message)
    elif message.text.lower() == "каузация" or message.text.lower() == "каузацию":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
        bot.send_photo(message.chat.id,
                       get('https://github.com/ioiimm/drafts/blob/main/bot/img/stenin.jpg?raw=true').content)
        mesg = bot.send_message(message.chat.id, "Кто на фото? Введите фамилию:")
        bot.register_next_step_handler(mesg, meme6_reply)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: каузация или каузацию')
        bot.send_photo(message.chat.id,
                       get('https://github.com/ioiimm/drafts/blob/main/bot/img/stenin.jpg?raw=true').content)
        mesg = bot.send_message(message.chat.id, "Кто на фото? Введите фамилию:")
        bot.register_next_step_handler(mesg, meme6_reply)


def meme6_reply(message):
    global sections
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text.lower() == "стенин":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id, 'Отлично, это правильный ответ!')
        sections[message.from_user.id] += 1
        if sections[message.from_user.id] != 3:
            keyboard_memes_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_memes_next_step.row("завершить тест")
            keyboard_memes_next_step.row("выбрать следующий раздел")
            mesg = bot.send_message(message.chat.id, "Завершить тест или продолжить дальше?",
                                    reply_markup=keyboard_memes_next_step)
            bot.register_next_step_handler(mesg, meme_next_step)
        else:
            bot.send_message(message.chat.id, "Вы все сделали!\nЗаканчиваем...",
                             reply_markup=types.ReplyKeyboardRemove())
            sections[message.from_user.id] = 0
            end_message(message)
    else:
        bot.send_message(message.chat.id, 'Это неверно, правильный ответ: Стенин')
        sections[message.from_user.id] += 1
        if sections[message.from_user.id] != 3:
            keyboard_memes_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_memes_next_step.row("завершить тест")
            keyboard_memes_next_step.row("выбрать следующий раздел")
            mesg = bot.send_message(message.chat.id, "Завершить тест или продолжить дальше?",
                                    reply_markup=keyboard_memes_next_step)
            bot.register_next_step_handler(mesg, meme_next_step)
        else:
            bot.send_message(message.chat.id, "Вы все сделали!\nЗаканчиваем...",
                             reply_markup=types.ReplyKeyboardRemove())
            sections[message.from_user.id] = 0
            end_message(message)


def meme_next_step(message):
    global sections, sections_lst
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "завершить тест":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == "выбрать следующий раздел":
        if sections[message.from_user.id] == 1:
            keyboard_memes_next_step1 = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_memes_next_step1.row("Цитаты преподавателей")
            keyboard_memes_next_step1.row("Организация учебного процесса")
            mesg = bot.send_message(message.chat.id, "Выбери следующий раздел:", reply_markup=keyboard_memes_next_step1)
            bot.register_next_step_handler(mesg, meme_next_step1)
        elif sections[message.from_user.id] == 2:
            if "Организация учебного процесса" in sections_lst[message.from_user.id]:
                keyboard_memes_next_step1 = telebot.types.ReplyKeyboardMarkup(False, True)
                keyboard_memes_next_step1.row("Цитаты преподавателей")
                mesg = bot.send_message(message.chat.id, "Выбери следующий раздел:",
                                        reply_markup=keyboard_memes_next_step1)
                bot.register_next_step_handler(mesg, meme_next_step1)
            else:
                keyboard_memes_next_step1 = telebot.types.ReplyKeyboardMarkup(False, True)
                keyboard_memes_next_step1.row("Организация учебного процесса")
                mesg = bot.send_message(message.chat.id, "Выбери следующий раздел:",
                                        reply_markup=keyboard_memes_next_step1)
                bot.register_next_step_handler(mesg, meme_next_step1)


def meme_next_step1(message):
    global sections_lst
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "Цитаты преподавателей":
        sections_lst[message.from_user.id].append("Цитаты преподавателей")
        bot.send_message(message.chat.id,
                         '''В этом разделе тебе будут показаны цитаты преподавателей. Отгадай, кому они принадлежат.''')
        mesg = bot.send_message(message.chat.id, '''Чья цитата? Введи сначала имя, потом фамилию преподавателя. 
\n"Видите ли вы эту красивую табличку с буквами? Она вам нравится или вызывает ужас? Вы пока подумайте, а я включу 
«Щенячий патруль»".''')
        bot.register_next_step_handler(mesg, quote1)
    elif message.text == "Организация учебного процесса":
        sections_lst[message.from_user.id].append("Организация учебного процесса")
        bot.send_message(message.chat.id, '''В этом разделе будут вопросы, связанные с учебным процессом на фикле. 
Выберите верный вариант ответа или введите слово.''')

        keyboard_org = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        key_var1 = types.KeyboardButton("фонетика")
        key_var2 = types.KeyboardButton("социолингвистика")
        key_var3 = types.KeyboardButton("академическое письмо")
        key_var4 = types.KeyboardButton("пары по языкам")
        keyboard_org.row(key_var1, key_var2)
        keyboard_org.row(key_var3, key_var4)
        r = bot.send_message(message.chat.id, "Какие семинары загадочно исчезают из РУЗа?",
                             reply_markup=keyboard_org)
        bot.register_next_step_handler(r, organisation1)


@bot.message_handler(func=lambda message: True)
def quote1(message):
    global sections_check
    sections_check[message.from_user.id].append('Цитаты преподавателей')
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == '/next':
        bot.send_message(message.chat.id, "Перехожу в следующий раздел...")
        next_message(message)
    elif message.text.lower() == 'инна зибер':
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id,
                         'Совершенно верно! Сразу видно, что смотришь все лекции и читаешь все письма :)')
        bot.send_photo(message.chat.id, get(
            'https://github.com/dianaaskarova/photos_project/blob/main/%D0%98%D0%BD%D0%BD%D0%B0%20%D0%B2%D0%B5%D1%81%D0%B5%D0%BB%D0%B0%D1%8F.jpg?raw=true').content)  # Инна веселая
        mesg = bot.send_message(message.chat.id, '''Чья цитата? Введи сначала имя, потом фамилию преподавателя. 
\n"Надеюсь, скоро станет попроще".''')
        bot.register_next_step_handler(mesg, quote2)
    else:
        bot.send_message(message.chat.id, 'Ошибочка! Правильный ответ: Инна Зибер.')
        bot.send_photo(message.chat.id, get(
            'https://github.com/dianaaskarova/photos_project/blob/main/%D0%98%D0%BD%D0%BD%D0%B0%20%D0%B3%D1%80%D1%83%D1%81%D1%82%D0%BD%D0%B0%D1%8F.jpg?raw=true').content)  # Инна грустная
        mesg = bot.send_message(message.chat.id, '''Чья цитата? Введи сначала имя, потом фамилию преподавателя. 
\n"Надеюсь, скоро станет попроще".''')
        bot.register_next_step_handler(mesg, quote2)


def quote2(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == '/next':
        bot.send_message(message.chat.id, "Перехожу в следующий раздел...")
        next_message(message)
    elif message.text.lower() == 'юрий ландер':
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id,
                         'Совершенно верно! Сразу видно, что смотришь все лекции и читаешь все письма :)')
        bot.send_photo(message.chat.id, get(
            'https://github.com/dianaaskarova/photos_project/blob/main/%D0%9B%D0%B0%D0%BD%D0%B4%D0%B5%D1%80%20%D0%B2%D0%B5%D1%81%D0%B5%D0%BB%D1%8B%D0%B9.jpg?raw=true').content)  # Ландер веселый
        mesg = bot.send_message(message.chat.id, '''Чья цитата? Введи сначала имя, потом фамилию преподавателя. 
\n"Так-так-так-так... Прум-пум-пум. Так. Пуф-пуф-пуф... Так-так-так-так. Щи-щи-щи-щу-щу... А-а-ай! Трррам-пам-пам".''')
        bot.register_next_step_handler(mesg, quote4)
    else:
        bot.send_message(message.chat.id, 'Ошибочка! Правильный ответ: Юрий Ландер.')
        bot.send_photo(message.chat.id, get(
            'https://github.com/dianaaskarova/photos_project/blob/main/%D0%9B%D0%B0%D0%BD%D0%B4%D0%B5%D1%80%20%D0%B3%D1%80%D1%83%D1%81%D1%82%D0%BD%D1%8B%D0%B9.jpg?raw=true').content)  # Ландер грустный
        mesg = bot.send_message(message.chat.id, '''Чья цитата? Введи сначала имя, потом фамилию преподавателя. 
\n"Так-так-так-так... Прум-пум-пум. Так. Пуф-пуф-пуф... Так-так-так-так. Щи-щи-щи-щу-щу... А-а-ай! Трррам-пам-пам".''')
        bot.register_next_step_handler(mesg, quote4)


def quote4(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == '/next':
        bot.send_message(message.chat.id, "Перехожу в следующий раздел...")
        next_message(message)
    elif message.text.lower() == 'александр подобряев':
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id,
                         'Совершенно верно! Сразу видно, что смотришь все лекции и читаешь все письма :)')
        bot.send_photo(message.chat.id, get(
            'https://github.com/dianaaskarova/photos_project/blob/main/%D0%9F%D0%BE%D0%B4%D0%BE%D0%B1%D1%80%D1%8F%D0%B5%D0%B2%20%D0%B2%D0%B5%D1%81%D0%B5%D0%BB%D1%8B%D0%B9.jpg?raw=true').content)  # Подобряев веселый
        mesg = bot.send_message(message.chat.id, '''Чья цитата? Введи сначала имя, потом фамилию преподавателя. 
\n"Мне нравится слово «актор», потому что я продался Западу".''')
        bot.register_next_step_handler(mesg, quote5)
    else:
        bot.send_message(message.chat.id, 'Ошибочка! Правильный ответ: Александр Подобряев.')
        bot.send_photo(message.chat.id, get(
            'https://github.com/dianaaskarova/photos_project/blob/main/%D0%9F%D0%BE%D0%B4%D0%BE%D0%B1%D1%80%D1%8F%D0%B5%D0%B2%20%D0%B3%D1%80%D1%83%D1%81%D1%82%D0%BD%D1%8B%D0%B9.jpg?raw=true').content)  # Подобряев грустный
        mesg = bot.send_message(message.chat.id, '''Чья цитата? Введи сначала имя, потом фамилию преподавателя. 
\n"Мне нравится слово «актор», потому что я продался Западу".''')
        bot.register_next_step_handler(mesg, quote5)


def quote5(message):
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == '/next':
        bot.send_message(message.chat.id, "Перехожу в следующий раздел...")
        next_message(message)
    elif message.text.lower() == 'андриан влахов':
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id,
                         'Совершенно верно! Сразу видно, что смотришь все лекции и читаешь все письма :)')
        bot.send_photo(message.chat.id, get(
            'https://github.com/dianaaskarova/photos_project/blob/main/%D0%92%D0%BB%D0%B0%D1%85%D0%BE%D0%B2%20%D0%B2%D0%B5%D1%81%D0%B5%D0%BB%D1%8B%D0%B9.jpg?raw=true').content)  # Влахов веселый
        mesg = bot.send_message(message.chat.id, '''Чья цитата? Введи сначала имя, потом фамилию преподавателя. 
\n"Будет чтение разных уровней сложности: иногда попроще, иногда полегче".''')
        bot.register_next_step_handler(mesg, quote3)
    else:
        bot.send_message(message.chat.id, 'Ошибочка! Правильный ответ: Андриан Влахов.')
        bot.send_photo(message.chat.id, get(
            'https://github.com/dianaaskarova/photos_project/blob/main/%D0%92%D0%BB%D0%B0%D1%85%D0%BE%D0%B2%20%D0%B3%D1%80%D1%83%D1%81%D1%82%D0%BD%D1%8B%D0%B9.jpg?raw=true').content)  # Влахов грустный
        mesg = bot.send_message(message.chat.id, '''Чья цитата? Введи сначала имя, потом фамилию преподавателя. 
\n"Будет чтение разных уровней сложности: иногда попроще, иногда полегче".''')
        bot.register_next_step_handler(mesg, quote3)


def quote3(message):
    global sections, sections_lst
    if message.text == "/end":
        bot.send_message(message.chat.id, "Заканчиваем...")
        end_message(message)
    elif message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == '/next':
        bot.send_message(message.chat.id, "Перехожу в следующий раздел...")
        next_message(message)
    elif message.text.lower() == "михаил даниэль":
        scores[message.from_user.id] += 1
        bot.send_message(message.chat.id,
                         'Совершенно верно! Сразу видно, что смотришь все лекции и читаешь все письма :)')
        bot.send_photo(message.chat.id, get(
            'https://github.com/dianaaskarova/photos_project/blob/main/%D0%94%D0%B0%D0%BD%D0%B8%D1%8D%D0%BB%D1%8C%20%D0%B2%D0%B5%D1%81%D0%B5%D0%BB%D1%8B%D0%B9.jpg?raw=true').content)  # Даниэль веселый
        sections[message.from_user.id] += 1
        if sections[message.from_user.id] != 3:
            keyboard_quotes_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_quotes_next_step.row("завершить тест")
            keyboard_quotes_next_step.row("выбрать следующий раздел")
            mesg = bot.send_message(message.chat.id, "Завершить тест или продолжить дальше?",
                                    reply_markup=keyboard_quotes_next_step)
            bot.register_next_step_handler(mesg, quote_next_step)
        else:
            bot.send_message(message.chat.id, "Вы все сделали!\nЗаканчиваем...",
                             reply_markup=types.ReplyKeyboardRemove())
            sections[message.from_user.id] = 0
            sections_lst[message.from_user.id].clear()
            end_message(message)
    else:
        bot.send_message(message.chat.id, 'Ошибочка! Правильный ответ: Михаил Даниэль.')
        bot.send_photo(message.chat.id, get(
            'https://github.com/dianaaskarova/photos_project/blob/main/%D0%94%D0%B0%D0%BD%D0%B8%D1%8D%D0%BB%D1%8C%20%D0%B3%D1%80%D1%83%D1%81%D1%82%D0%BD%D1%8B%D0%B9.jpg?raw=true').content)  # Даниэль грустный
        sections[message.from_user.id] += 1
        if sections[message.from_user.id] != 3:
            keyboard_quotes_next_step = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_quotes_next_step.row("завершить тест")
            keyboard_quotes_next_step.row("выбрать следующий раздел")
            mesg = bot.send_message(message.chat.id, "Завершить тест или продолжить дальше?",
                                    reply_markup=keyboard_quotes_next_step)
            bot.register_next_step_handler(mesg, quote_next_step)
        else:
            bot.send_message(message.chat.id, "Вы все сделали!\nЗаканчиваем...",
                             reply_markup=types.ReplyKeyboardRemove())
            sections[message.from_user.id] = 0
            sections_lst[message.from_user.id].clear()
            end_message(message)


def quote_next_step(message):
    global sections, sections_lst
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == "завершить тест":
        bot.send_message(message.chat.id, "Заканчиваем...", reply_markup=types.ReplyKeyboardRemove())
        sections_lst[message.from_user.id].clear()
        sections[message.from_user.id] = 0
        end_message(message)
    elif message.text == "выбрать следующий раздел":
        if sections[message.from_user.id] == 1:
            keyboard_quotes_next_step1 = telebot.types.ReplyKeyboardMarkup(False, True)
            keyboard_quotes_next_step1.row("Мемы")
            keyboard_quotes_next_step1.row("Организация учебного процесса")
            mesg = bot.send_message(message.chat.id, "Выбери следующий раздел:",
                                    reply_markup=keyboard_quotes_next_step1)
            bot.register_next_step_handler(mesg, quote_next_step1)
        elif sections[message.from_user.id] == 2:
            if "Организация учебного процесса" in sections_lst[message.from_user.id]:
                keyboard_quotes_next_step1 = telebot.types.ReplyKeyboardMarkup(False, True)
                keyboard_quotes_next_step1.row("Мемы")
                mesg = bot.send_message(message.chat.id, "Выбери следующий раздел:",
                                        reply_markup=keyboard_quotes_next_step1)
                bot.register_next_step_handler(mesg, quote_next_step1)
            else:
                keyboard_quotes_next_step1 = telebot.types.ReplyKeyboardMarkup(False, True)
                keyboard_quotes_next_step1.row("Организация учебного процесса")
                mesg = bot.send_message(message.chat.id, "Выбери следующий раздел:",
                                        reply_markup=keyboard_quotes_next_step1)
                bot.register_next_step_handler(mesg, quote_next_step1)


def quote_next_step1(message):
    global sections_lst
    if message.text == '/start':
        bot.send_message(message.chat.id, "Возвращаюсь в начало...", reply_markup=keyboard)
    elif message.text == '/end':
        bot.send_message(message.chat.id, "Заканчиваем...", reply_markup=types.ReplyKeyboardRemove())
        end_message(message)
    elif message.text == "Мемы":
        sections_lst[message.from_user.id].append("Мемы")
        bot.send_message(message.chat.id, '''В каждом задании этого раздела вам будет показан мем,
связанный с нашим потоком. Вам нужно будет выбрать один вариант ответа или ввести слово.''')
        bot.send_photo(message.chat.id, get(
            'https://github.com/ioiimm/drafts/blob/main/bot/img/chicken.jpg?raw=true').content)
        mesg = bot.send_message(message.chat.id, 'Введите слово:')
        bot.register_next_step_handler(mesg, meme1)
    elif message.text == "Организация учебного процесса":
        sections_lst[message.from_user.id].append("Организация учебного процесса")
        bot.send_message(message.chat.id, '''В этом разделе будут вопросы, связанные с учебным процессом на фикле.
Выберите верный вариант ответа или введите слово.''')

        keyboard_org = types.ReplyKeyboardMarkup(one_time_keyboard=True)
        key_var1 = types.KeyboardButton("фонетика")
        key_var2 = types.KeyboardButton("социолингвистика")
        key_var3 = types.KeyboardButton("академическое письмо")
        key_var4 = types.KeyboardButton("пары по языкам")
        keyboard_org.row(key_var1, key_var2)
        keyboard_org.row(key_var3, key_var4)
        r = bot.send_message(message.chat.id, "Какие семинары загадочно исчезают из РУЗа?",
                             reply_markup=keyboard_org)
        bot.register_next_step_handler(r, organisation1)


bot.polling()

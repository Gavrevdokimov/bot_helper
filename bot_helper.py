# -*- coding: utf8 -*-

import telebot
from telebot import types
import copy
import json


token = os.environ.get("BOT_TOKEN_2")
bot = telebot.TeleBot(token)

# открываем сохраненную игру
with open('save_askers.json') as f:
    try:
        askers = json.load(f)
        askers_2 = copy.deepcopy(askers)
        askers = {}
        for asker in askers_2:
            asker_2 = int(asker)
            askers[asker_2] = copy.deepcopy(askers_2[asker])
    except:
        askers = {}



sticker = 'CAACAgIAAxkBAAIPnV67u5l7uBx-N1IYtu70VgclQuO4AAIVAwACnNbnCgbnCWarj1O-GQQ'


#клава планируете праздник?
def keyboard_wanna_party():
    keyboard = types.InlineKeyboardMarkup()
    private = types.InlineKeyboardButton(text="Частный праздник", callback_data='private_party')
    corporate = types.InlineKeyboardButton(text="Корпоративное мероприятие", callback_data='corporate_party')
    tourist = types.InlineKeyboardButton(text="Я турист, погулять по городу", callback_data='tourist')
    just_play = types.InlineKeyboardButton(text="Просто поиграть в квест без повода", callback_data="just_play")
    just_call = types.InlineKeyboardButton(text="Заказать звонок", callback_data="just_call")
    keyboard.add(private)
    keyboard.add(corporate)
    keyboard.add(tourist)
    keyboard.add(just_play)
    keyboard.add(just_call)
    return keyboard


#клава какой частный праздник?
def keyboard_party():
    keyboard = types.InlineKeyboardMarkup()
    dr = types.InlineKeyboardButton(text="День рождения", callback_data='birthday')
    dp = types.InlineKeyboardButton(text="Детский праздник", callback_data="child")
    date = types.InlineKeyboardButton(text="Свидание", callback_data="date")
    wed = types.InlineKeyboardButton(text="Свадьба", callback_data="wed")
    boy = types.InlineKeyboardButton(text="Мальчишник", callback_data="boys")
    girl = types.InlineKeyboardButton(text="Девичник", callback_data="girls")
    other = types.InlineKeyboardButton(text="Другое", callback_data="other")
    back = types.InlineKeyboardButton(text="Начать подбор сначала", callback_data="back")
    keyboard.add(dr)
    keyboard.add(dp)
    keyboard.add(wed)
    keyboard.add(boy)
    keyboard.add(girl)
    keyboard.add(date)
    keyboard.add(other)
    keyboard.add(back)
    return keyboard


#клава какой корпорат?
def keyboard_corporate():
    keyboard = types.InlineKeyboardMarkup()
    hr = types.InlineKeyboardButton(text="Квест для сотрудников", callback_data='hr')
    promo = types.InlineKeyboardButton(text="Промо-квест", callback_data="promo")
    other = types.InlineKeyboardButton(text="Другое", callback_data="other")
    back = types.InlineKeyboardButton(text="Начать подбор сначала", callback_data="back")
    keyboard.add(hr)
    keyboard.add(promo)
    keyboard.add(other)
    keyboard.add(back)
    return keyboard


#клава возраст
def keyboard_age_birthday():
    keyboard = types.InlineKeyboardMarkup()
    q = types.InlineKeyboardButton(text="до 15 лет", callback_data='children_birthday')
    w = types.InlineKeyboardButton(text="15 - 20 лет", callback_data='young_birthday')
    e = types.InlineKeyboardButton(text="20 - 30 лет", callback_data='middle_birthday')
    r = types.InlineKeyboardButton(text="старше 30", callback_data='adult_birthday')
    t = types.InlineKeyboardButton(text="Начать подбор сначала", callback_data="back")
    keyboard.add(q)
    keyboard.add(w)
    keyboard.add(e)
    keyboard.add(r)
    keyboard.add(t)
    return keyboard


#клава просто назад
def keyboard_back():
    keyboard = types.InlineKeyboardMarkup()
    q = types.InlineKeyboardButton(text="Начать подбор сначала", callback_data="back")
    w = types.InlineKeyboardButton(text="Заказать звонок", callback_data="just_call")
    keyboard.add(q)
    keyboard.add(w)
    return keyboard


#клава онлайн или оффлайн
def keyboard_online():
    keyboard = types.InlineKeyboardMarkup()
    q = types.InlineKeyboardButton(text="Офлайн", callback_data="offline")
    w = types.InlineKeyboardButton(text="Онлайн", callback_data="online")
    keyboard.add(q)
    keyboard.add(w)
    return keyboard


#клава в помещении или снаружи
def keyboard_outside():
    keyboard = types.InlineKeyboardMarkup()
    q = types.InlineKeyboardButton(text="Уличный квест", callback_data="outside")
    w = types.InlineKeyboardButton(text="Под крышей", callback_data="inside")
    keyboard.add(q)
    keyboard.add(w)
    return keyboard


#сохраняем players в файл
def saving():
    with open("save_askers.json", "w") as write_file:
        json.dump(askers, write_file)
    return


@bot.message_handler(commands=["start", "call"])  # реакция на команду, которая вводится после /
def command_hadler(message):
    global askers
    if message.text == "/start":
        bot.send_message(message.from_user.id, f"Здравствуйте, я бот-помощник от PiterQuest. Я помогу вам подобрать подходящий квест. Я разбираюсь только в наших стандартных программах, если я не смогу вам помочь, обратитесь к менеджеру по телефону +7 911 1379398.\n\nДля начала выберите повод для квеста:", reply_markup = keyboard_wanna_party())
        askers[message.from_user.id] = {}
        askers[message.from_user.id]["name"] = message.from_user.first_name
        askers[message.from_user.id]["last_name"] = message.from_user.last_name
        bot.send_message(325051402, f"{askers[message.from_user.id]['name']} {askers[message.from_user.id]['last_name']} задает мне вопрос")
        saving()
    elif message.text == "/call":
        bot.send_message(message.from_user.id, "Напишите свой номер телефона, и мы позвоним в ближайшее время.")
        askers[message.from_user.id]["call"] = "yes"


@bot.callback_query_handler(func=lambda message: True)
def answer(message):
    global players
    if message.data == 'just_call':
        bot.send_message(message.from_user.id, "Напишите свой номер телефона, и мы позвоним в ближайшее время.", reply_markup=keyboard_back())
        askers[message.from_user.id]["call"] = "yes"
    elif message.data == 'tourist':
        bot.send_message(message.from_user.id, "Наши квесты для туристов:\n\n1. Интеллектуальный квест - для взрослых или всей семьи\npiterquests.ru/intellektualnijkvest"
                                                   "\n\n2. Квест в Русском музее - для взрослых или всей семьи\npiterquests.ru/kvestvmuzee"
                                                   "\n\n3. Фотоквест квест - для компаний молодых и автивных\npiterquests.ru/photokvest"
                                                   "\n\n4. Активный квест - для детей (классы, лагеря)\npiterquests.ru/ulichnijkvest"
                                                   "\n\n5. Барный квест - для взрослых мужских компаний (девушкам тоже можно присоединиться)\npiterquests.ru/alcoholkvest", reply_markup=keyboard_back())
    elif message.data == 'just_play':
        bot.send_message(message.from_user.id, "Наши квесты без повода:\n\n1. Интеллектуальный квест - для взрослых или всей семьи\npiterquests.ru/intellektualnijkvest"
                                                   "\n\n2. Квест в Русском музее - для взрослых или всей семьи\npiterquests.ru/kvestvmuzee"
                                                   "\n\n3. Фотоквест квест - для компаний молодых и автивных\npiterquests.ru/photokvest"
                                                   "\n\n4. Активный квест - для детей\npiterquests.ru/ulichnijkvest"
                                                   "\n\n5. Барный квест - для взрослых мужских компаний (девушкам тоже можно присоединиться)\npiterquests.ru/alcoholkvest", reply_markup=keyboard_back())
    elif message.data == 'back':
        bot.send_message(message.from_user.id, f"Выберите повод для квеста:", reply_markup=keyboard_wanna_party())
    elif message.data == 'private_party':
        bot.send_message(message.from_user.id, f"Какой праздник у вас намечается?", reply_markup=keyboard_party())
    elif message.data == 'corporate_party':
        bot.send_message(message.from_user.id, f"Какой вид мероприятия планируется?", reply_markup=keyboard_corporate())
    elif message.data == 'birthday':
        bot.send_message(message.from_user.id, f"Какой возраст участников?", reply_markup=keyboard_age_birthday())
    elif message.data == 'child':
        bot.send_message(message.from_user.id, 'Вам подойдет "Активный квест". По формату он похож на ФортБоярд. Мы подберем 6 локаций в одном районе города (обычно это Гостиный двор), все места зашифруем загадками. На каждом месте аниматоры дадут задание в игровой форме. Если участников много, можно поделить их на команды и устроить соревнование.\nПодробности о квесте - по ссылке piterquests.ru/ulichnijkvest', reply_markup=keyboard_back())
    elif message.data == 'date':
        bot.send_message(message.from_user.id, "Романтические квесты:\n\n1. Прогулка для двоих по местам, где принято загадывать желания. В загадки квеста мы вставим факты из вашей общей истории.\n4500 рублей\n\n"
                                               "2. Сюрприз для девушки. Квест может начаться в любой момент с письма от курьера или неожиданного звонка, а наши актеры и различные намеки помогут ей найти место свидания, где вы будете ее ждать.\nот 30 000 руб\n\nПодробности об обоих квестах - piterquests.ru/romanticheskijkvest")
    elif message.data == 'wed':
        bot.send_message(message.from_user.id, "Как квест может пригодиться на свадьбе:\n\n"
                                               "1. Развлечение для гостей, пока молодые заняты на фотосессии.\n\n"
                                               "2. Оригинальный способ доставить гостей от ЗАГСа до ресторана.\n\n"
                                               "3. Лучший вариант проведения второго дня свадьбы\n\n"
                                               "4. Современный формат выкупа невесты\n\nПодробности о сваденбых квестах по ссылке - piterquests.ru/svadbakvest#price", reply_markup=keyboard_back())
    elif message.data == 'boys':
        bot.send_message(message.from_user.id, "Квесты на мальчишник:\n\n1. Городской квест, в загадки которого вплетены факты из биографии жениха. В маршрут можно добавить 2 бара.\nот 4500 рублей\n\n"
                                               "2. Квест 'Джентльмен' - игра по 3 атмосферным барам позволит вам примерить на себя это почетное звание и узнать, как развлекались джентльмены в конце 19 века.\nот 26 500 руб\n\nПодробности об обоих квестах - piterquests.ru/kvestnamalchishnik", reply_markup=keyboard_back())
    elif message.data == 'girls':
        bot.send_message(message.from_user.id, 'Квесты на девичник:\n\n1. Пакет "Только квест"\nМы напишем квест, в задания которого добавим факты из истории невесты и жениха. А наш ведущий проведет для вас квест. 1000 рублей за участницу\n\n'
                                               '2. Пакет "Целый девичник"\nВесь пакет "Только квест", а еще фоограф на весь квест, браслетики с живыми цветами для каждой участницы, красивая церемония прощания с фамилией на крыше и загадки, оформленные индивидуально для вашей невесты. от 2200 рублей за участницу.'
                                               '\n\nПодробнее об обоих форматах - по ссылке piterquests.ru/kvestnadevichnik', reply_markup=keyboard_back())
    elif message.data == 'other':
        bot.send_message(message.from_user.id, "Пожалуйста, напишите свой номер телефона, мы позвоним в ближайшее время и расскажем, какой квест можем устроить на ваш праздник.")
        askers[message.from_user.id]["call"] = "yes"
    elif message.data == 'children_birthday':
        bot.send_message(message.from_user.id, 'Вам подойдет "Активный квест". По формату он похож на ФортБоярд. Мы подберем 6 локаций в одном районе города (обычно это Гостиный двор), все места зашифруем загадками. На каждом месте аниматоры дадут задание в игровой форме. В некоторые задания мы можем добавить факты об имениннике. Если участников много, можно поделить их на команды и устроить соревнование.\nПодробности о квесте - по ссылке piterquests.ru/ulichnijkvest', reply_markup=keyboard_back())
    elif message.data == 'young_birthday':
        bot.send_message(message.from_user.id, 'Вам подойдет "Развлекательный квест". Мы подберем 6 локаций в одном районе города (обычно это Гостиный двор), все места зашифруем загадками. На каждом месте ведущий даст участникам задание, связанное лично с именинником.\nПодробности о квесте - по ссылке piterquests.ru/kvestnadenrozhdenija', reply_markup=keyboard_back())
    elif message.data == 'adult_birthday':
        bot.send_message(message.from_user.id, 'Вам подойдет "Интеллектуальный квест". Мы подберем 15 локаций в одном районе города (обычно это Гостиный двор), все места зашифруем загадками. В загадки вставим факты из биографии именинника. А еще добавим приятный сюрприз для него в конце.\nПодробности о квесте - по ссылке piterquests.ru/kvestnadenrozhdenija', reply_markup=keyboard_back())
    elif message.data == 'middle_birthday':
        bot.send_message(message.from_user.id, 'У нас 2 подходящих квеста:\n1. Развлекательный квест\nМы подберем 6 локаций в одном районе города (обычно это Гостиный двор), все места зашифруем загадками. На каждом месте ведущий даст участникам развлекательное задание, связанное лично с именинником.\n\n'
                                               '2. Интеллектуальный квест\nМы подберем 15 локаций в одном районе города (обычно это Гостиный двор), все места зашифруем загадками. В загадки вставим факты из биографии именинника. А еще добавим приятный сюрприз для него в конце.\n\n'
                                               'Как выбрать. Если вы хотите развлечься и не напрягаться, тогда Развлекательный. Если любите поломать голову, тогда Интеллектуальный.\n\nПодробности об обоих квестах - по ссылке piterquests.ru/kvestnadenrozhdenija', reply_markup=keyboard_back())
    elif message.data == 'hr':
        bot.send_message(message.from_user.id, 'Нужна офлайн-игра или онлайн?', reply_markup=keyboard_online())
    elif message.data == 'promo':
        bot.send_message(message.from_user.id, 'В данном направлении не может быть готовых решений. По ссылке вы можете посмотреть основные форматы, которые мы готовы предложить, а также наши кейсы.\npiterquests.ru/promokvest', reply_markup=keyboard_back())
    elif message.data == 'online':
        bot.send_message(message.from_user.id, 'Онлайн-игра "Капиталист".\n7 раундов, в каждом мы предложим 5 компаний. Вы предполагаете, какие из них будут успешны, а какие прогорят, и инвестируете в выбранные, чтобы заработать больше остальных.\nПодробнее об игре - по ссылке piterquests.ru/online-kvest', reply_markup=keyboard_back())
    elif message.data == 'offline':
        bot.send_message(message.from_user.id, 'Городской квест или игра под крышей?', reply_markup=keyboard_outside())
    elif message.data == 'inside':
        bot.send_message(message.from_user.id, 'Игры в помещении:\n\n1. Игра "Капиталист"\n7 раундов, в каждом мы предложим 5 компаний. Вы предполагаете, какие из них будут успешны, а какие прогорят, и инвестируете в выбранные, чтобы заработать больше остальных. Играть можно в офисе, в ресторане, где угодно.\nПодробнее об игре - по ссылке piterquests.ru/online-kvest'
                                               '\n\n2. Квест в Русском музее "Ограбление"\n2 часа, 15 загадок и все самые известные экспонаты музея. Знания искусства не требуются. Требуются внимательность, логика и эрудиция.\nПодробнее - по ссылке piterquests.ru/kvestvmuzee'
                                               '\n\n3. Квест в офисе\nМы приедем к вам в офис и устроим игру прямо там, где вы каждый день работаете. Сценарий напишем индивидуально под вашу компанию.\nПодробности - по ссылке piterquests.ru/kvestvofise'
                                                '\n\n4. Барный квест - для взрослых мужских компаний (девушкам тоже можно присоединиться)\npiterquests.ru/alcoholkvest', reply_markup=keyboard_back())
    elif message.data == 'outside':
        bot.send_message(message.from_user.id, 'Городские квесты\nМы подберем около 15 локаций в одном районе города, все зашифруем загадками. Ваша задача - отгадать загадки, найти локации, ответить на наши вопросы о них и из ответов собрать ключевую фразу. Есть готовые маршруты, также вы можете задать место старта и финиша.\nПодробнее о формате - по ссылке piterquests.ru/intellektualnijkvest', reply_markup=keyboard_back())



@bot.message_handler(content_types=["text"])
def sticker_hadler(message):
    global players
    if message.text.isdigit() or "+7" in message.text:
        if askers[message.from_user.id]["call"] == "yes":
            askers[message.from_user.id]["tel"] = message.text
            bot.send_message(message.from_user.id, "Спасибо, наш менеджер скоро позвонит вам!")
            bot.send_message(325051402, f"Заказ звонка: {askers[message.from_user.id]['name']} {askers[message.from_user.id]['last_name']} {askers[message.from_user.id]['tel']}")
    else:
        bot.send_message(message.from_user.id, "Извините, я не умею отвечать на вопросы. Если вы напишите свой номер телефона, наш менеджер позвонит и ответит на все вопросы.")
        askers[message.from_user.id]["call"] = "yes"

                             
bot.polling(timeout=60)

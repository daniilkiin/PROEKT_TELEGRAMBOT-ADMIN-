import asyncio
import json
from telebot import types, TeleBot

token = '6324727670:AAGgUk1O13kbLa0wuMWSBeZw6Fy7uLVI45A'

bot = TeleBot(token)

active_question = None
active_otvet = None
active_themes = {}

def del_theme(message):
    global active_question, active_themes, active_otvet

    file = open('themes.json', 'r', encoding='utf-8')
    themes = json.load(file)
    file.close()
    del themes[active_themes[message.from_user.id]]
    file = open('themes.json', 'w', encoding='utf-8')
    json.dump(themes, file, ensure_ascii=False)
    file.close()
    bot.send_message(message.from_user.id, text='Вы успешно удалили тему')

def del_questions(message):
    global active_question, active_themes, active_otvet

    file = open('themes.json', 'r', encoding='utf-8')
    questions = json.load(file)
    file.close()

def del_otvets(message):
    global active_question, active_themes, active_otvet

    file = open('themes.json', 'r', encoding='utf-8')
    otvets = json.load(file)
    file.close()


def edit_otvets(message):
    global active_question, active_themes, active_otvet

    file = open('themes.json', 'r', encoding='utf-8')
    otvets = json.load(file)
    file.close()
    otvets[active_themes]["questions"]["otvets"][message.text] = otvets[active_themes]["questions"]["otvets"].pop(message.text)
    file = open('themes.json', 'w', encoding='utf-8')
    json.dump(questions, file, ensure_ascii=False)
    file.close()
    bot.send_message(message.from_user.id, text='Ответ успешно изменён')

def edit_questions(message):
    global active_question, active_themes, active_otvet

    file = open('themes.json', 'r', encoding='utf-8')
    questions = json.load(file)
    file.close()
    print(active_themes)
    questions[active_themes]["questions"][message.text] = questions[active_themes]["questions"].pop()
    print(questions)
    file = open('themes.json', 'w', encoding='utf-8')
    json.dump(questions, file, ensure_ascii=False)
    file.close()
    bot.send_message(message.from_user.id, text='Вопрос успешно изменён')

def edit_theme_name(message):
    file = open('themes.json', 'r', encoding='utf-8')
    themes = json.load(file)
    file.close()
    value = themes[active_themes[message.from_user.id]]
    themes[message.text] = value
    del themes[active_themes[message.from_user.id]]
    file = open('themes.json', 'w', encoding='utf-8')
    json.dump(themes, file, ensure_ascii=False)
    file.close()
    active_themes[message.from_user.id] = message.text
    bot.send_message(message.from_user.id, text='Название темы успешно изменено')


def get_editing(user_id):
    global active_otvet, active_themes, active_question

    file = open('themes.json', 'r', encoding='utf-8')
    themes = json.load(file)
    file.close()
    keyborddd = types.InlineKeyboardMarkup()
    buttonn1 = types.InlineKeyboardButton(text='1. Изменение темы', callback_data='1. Изменение темы')
    buttonn2 = types.InlineKeyboardButton(text='2. Изменение вопросов', callback_data='2. Изменение вопросов')
    buttonn3 = types.InlineKeyboardButton(text='3. Изменение ответов', callback_data='3. Изменение ответов')
    buttonn4 = types.InlineKeyboardButton(text='4. Удаление темы', callback_data='4. Удаление темы')
    buttonn5 = types.InlineKeyboardButton(text='5. Удаление вопросов', callback_data='5. Удаление вопросов')
    buttonn6 = types.InlineKeyboardButton(text='6. Удаление ответов', callback_data='6. Удаление ответов')
    keyborddd.add(buttonn1)
    keyborddd.add(buttonn2)
    keyborddd.add(buttonn3)
    keyborddd.add(buttonn4)
    keyborddd.add(buttonn5)
    keyborddd.add(buttonn6)
    bot.send_message(user_id, text='Выберите одну из кнопок', reply_markup=keyborddd)

def get_otvet(message):
    global active_otvet, active_themes

    file = open('themes.json', 'r', encoding='utf-8')
    otvets = json.load(file)
    file.close()
    file = open('themes.json', 'w', encoding='utf-8')
    otvets[active_themes[message.from_user.id]]["questions"][active_question]["otvets"][message.text] = {}
    json.dump(otvets, file, ensure_ascii=False)
    active_otvet = message.text
    file.close()
    bot.send_message(message.from_user.id, text='Напишите ответ')
    bot.send_message(message.from_user.id, text='Ответ успешно добавлен')
    bot.register_next_step_handler(message, get_otvet)

def get_question(message):
    global active_question, active_themes

    file = open('themes.json', 'r', encoding='utf-8')
    questions = json.load(file)
    file.close()
    file = open('themes.json', 'w', encoding='utf-8')
    questions[active_themes[message.from_user.id]]["questions"][message.text] = {
        "otvets": {}
    }
    json.dump(questions, file, ensure_ascii=False)
    active_question = message.text
    file.close()
    bot.send_message(message.from_user.id, text='Напишите вопрос')
    bot.send_message(message.from_user.id, text='Вопрос успешно добавлен')
    bot.register_next_step_handler(message, get_question)

def get_theme(message):
    global active_themes

    file = open('themes.json', 'r', encoding='utf-8')
    themes = json.load(file)
    file.close()
    file = open('themes.json', 'w', encoding='utf-8')
    themes[message.text] = {
        "questions": {}
    }
    json.dump(themes, file, ensure_ascii=False)
    active_themes[message.from_user.id] = message.text
    file.close()
    bot.send_message(message.from_user.id, text='Тема успешно добавлена')
    keyborddd = types.InlineKeyboardMarkup()
    buttonn1 = types.InlineKeyboardButton(text='Добавить вопрос к теме', callback_data='Добавить вопрос к теме')
    buttonn2 = types.InlineKeyboardButton(text='Добавить ещё одну тему', callback_data='Добавить ещё одну тему')
    keyborddd.add(buttonn1)
    keyborddd.add(buttonn2)
    bot.send_message(message.from_user.id, text='Выберите одну из кнопок', reply_markup=keyborddd)
    # bot.register_next_step_handler(message, get_theme)

@bot.message_handler(content_types=['text'])

def get_message(message):
    if message.text == '/start':
        bot.set_my_commands(
            commands=[
                types.BotCommand('/start', 'Запуск Бота')
            ],
            scope=types.BotCommandScopeChat(message.chat.id)
        )
        klava = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Список существующих тем', callback_data='Список существующих тем')
        button2 = types.InlineKeyboardButton(text='Добавление темы', callback_data='Добавление темы')
        klava.add(button1)
        klava.add(button2)
        bot.send_message(message.from_user.id, text='Добро пожаловать в телеграм бот (Администратор)')
        bot.send_message(message.from_user.id, text='Выберите одну из перечисленных кнопок', reply_markup=klava)

def get_exsisting(chat_id):
    file = open('themes.json', 'r', encoding='utf-8')
    themes = json.load(file)
    file.close()
    keyboard = types.InlineKeyboardMarkup()
    for theme in list(themes.keys()):
        button = types.InlineKeyboardButton(text=theme, callback_data=theme)
        keyboard.add(button)
    bot.send_message(chat_id, text='Выберите одну из существующих тем', reply_markup=keyboard)

# def now_theme(message):
#     file = open('themes.json', 'r', encoding='utf-8')
#     themes = json.load(file)
#     file.close()
#     keyboard = types.InlineKeyboardMarkup()
#     for theme in list(themes):
#         button = types.InlineKeyboardButton(text=theme, callback_data=theme)
#         keyboard.add(button)
#     keyboard2 = types.InlineKeyboardMarkup()
#     for question in list(themes):
#         button2 = types.InlineKeyboardButton(text=question, callback_data=question)
#         keyboard2.add(button2)
#     keyboard3 = types.InlineKeyboardMarkup()
#     for otvet in list(themes):
#         button3 = types.InlineKeyboardButton(text=otvet, callback_data=otvet)
#         keyboard3.add(button3)
#     bot.send_message(message.from_user.id, text='Выберите одну из перечисленных тем для редактирования', reply_markup=keyboard)
#     keybord = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton(text='Добавление новой темы', callback_data='Добавление новой темы')
#     button2 = types.InlineKeyboardButton(text='Добавление вопросов', callback_data='Добавление вопросов')
#     button3 = types.InlineKeyboardButton(text='Добавление ответов', callback_data='Добавление ответов')
#     keybord.add(button1)
#     keybord.add(button2)
#     keybord.add(button3)
#     bot.send_message(message.from_user.id, text='888888')
#     bot.send_message(message.from_user.id, text='lllllll', reply_markup=keybord)

# def get_addition(chat_id):
#     file = open('themes.json', 'r', encoding='utf-8')
#     themes = json.load(file)
#     file.close()
#     keybord = types.InlineKeyboardMarkup()
#     button1 = types.InlineKeyboardButton(text='Добавление новой темы', callback_data='Добавление новой темы')
#     button2 = types.InlineKeyboardButton(text='Добавление вопросов', callback_data='Добавление вопросов')
#     button3 = types.InlineKeyboardButton(text='Добавление ответов', callback_data='Добавление ответов')
#     keybord.add(button1)
#     keybord.add(button2)
#     keybord.add(button3)
#     bot.send_message(chat_id, text='Выбирайте кнопки по порядку', reply_markup=keybord)

@bot.callback_query_handler(func=lambda call:True)
def callback_worker(call):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    if call.data == 'Список существующих тем':
        get_exsisting(call.message.chat.id)
    elif call.data == 'Добавление темы':
        bot.send_message(call.from_user.id, text='Напишите название для новой темы')
        bot.register_next_step_handler(call.message, get_theme)
    elif call.data == 'Добавить вопрос к теме':
        get_question(call.message.chat.id)
    # elif call.data == 'Добавление новой темы':
    #     bot.send_message(call.from_user.id, text='Напишите название для новой темы')
    #     bot.register_next_step_handler(call.message, get_theme)
    # elif call.data == 'Добавление вопросов':
    #     bot.send_message(call.from_user.id, text='Напишите вопрос')
    #     bot.register_next_step_handler(call.message, get_question)
    elif call.data == 'Добавление ответов':
        bot.send_message(call.from_user.id, text='Напишите ответ')
        bot.register_next_step_handler(call.message, get_otvet)
    elif call.data == '1. Изменение темы':
        bot.send_message(call.from_user.id, text='Напишите новое название для темы')
        bot.register_next_step_handler(call.message, edit_theme_name)
    elif call.data == '2. Изменение вопросов':
        bot.send_message(call.from_user.id, text='Напишите новый вопрос для темы')
        bot.register_next_step_handler(call.message, edit_questions)
    elif call.data == '3. Изменение ответов':
        bot.send_message(call.from_user.id, text='Напишите новый ответ для темы')
        bot.register_next_step_handler(call.message, edit_otvets)
    elif call.data == '4. Удаление темы':
        bot.register_next_step_handler(call.message, del_theme)
    elif call.data == '5. Удаление вопросов':
        bot.register_next_step_handler(call.message, del_questions)
    elif call.data == '6. Удаление ответов':
        bot.register_next_step_handler(call.message, del_otvets)
    else:
        file = open('themes.json', 'r', encoding='utf-8')
        themes = json.load(file)
        file.close()
        for theme in list(themes):
            if call.data == theme:
                active_themes[call.from_user.id] = theme
                get_editing(call.from_user.id)
                break


bot.polling(none_stop=True, interval=0)

import asyncio
import json
from telebot import types, TeleBot

token = '6324727670:AAGgUk1O13kbLa0wuMWSBeZw6Fy7uLVI45A'

bot = TeleBot(token)

active_question = None
active_otvet = None
active_themes = {}

def edit_question(message):
    file = open('themes.json', 'r', encoding='utf-8')
    questions = json.load(file)
    file.close()
    keyboard123 = types.InlineKeyboardMarkup()
    for question in list(questions):
        print(question)
        button = types.InlineKeyboardButton(text=question, callback_data=question)
        keyboard123.add(button)

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
    # print(active_themes)

def get_editing(user_id):
    global active_otvet, active_themes, active_question

    file = open('themes.json', 'r', encoding='utf-8')
    themes = json.load(file)
    file.close()
    keyborddd = types.InlineKeyboardMarkup()
    buttonn1 = types.InlineKeyboardButton(text='Изменение темы', callback_data='Изменение темы')
    buttonn2 = types.InlineKeyboardButton(text='Изменение вопросов', callback_data='Изменение вопросов')
    buttonn3 = types.InlineKeyboardButton(text='Изменение ответов', callback_data='Изменение ответов')
    keyborddd.add(buttonn1, buttonn2, buttonn3)
    bot.send_message(user_id, text='Выберите одну из кнопок', reply_markup=keyborddd)

def get_otvet(message):
    global active_otvet, active_themes

    file = open('themes.json', 'r', encoding='utf-8')
    otvets = json.load(file)
    file.close()
    file = open('themes.json', 'w', encoding='utf-8')
    otvets[active_themes[message.from_user.id]]['otvets'].append(message.text)
    json.dump(otvets, file, ensure_ascii=False)
    active_otvet = message.text
    file.close()
    bot.send_message(message.from_user.id, text='Напишите ответы')
    bot.register_next_step_handler(message, get_question)

def get_question(message):
    global active_question, active_themes

    file = open('themes.json', 'r', encoding='utf-8')
    questions = json.load(file)
    file.close()
    file = open('themes.json', 'w', encoding='utf-8')
    questions[active_themes[message.from_user.id]]["questions"].append(message.text)
    json.dump(questions, file, ensure_ascii=False)
    active_question = message.text
    file.close()
    bot.send_message(message.from_user.id, text='Напишите вопросы')
    bot.register_next_step_handler(message, get_question)

def get_theme(message):
    global active_themes

    file = open('themes.json', 'r', encoding='utf-8')
    themes = json.load(file)
    file.close()
    file = open('themes.json', 'w', encoding='utf-8')
    themes[message.text] = {
        "questions": {
            "otvets": {

            }
        }
    }
    json.dump(themes, file, ensure_ascii=False)
    active_themes[message.from_user.id] = message.text
    file.close()
    bot.send_message(message.from_user.id, text='Напишите название для новой темы')
    bot.register_next_step_handler(message, get_theme)

@bot.message_handler(content_types=['text'])

def get_message(message):
    if message.text == '/start':
        bot.set_my_commands(
            commands=[
                types.BotCommand('/start', 'Запуск Бота')
            ],
            scope=types.BotCommandScopeChat(message.chat.id)
        )
        file = open('themes.json', 'r', encoding='utf-8')
        themes = json.load(file)
        file.close()
        keyboard = types.InlineKeyboardMarkup()
        for theme in list(themes):
            button = types.InlineKeyboardButton(text=theme, callback_data=theme)
            keyboard.add(button)
        keyboard2 = types.InlineKeyboardMarkup()
        for question in list(themes):
            button2 = types.InlineKeyboardButton(text=question, callback_data=question)
            keyboard2.add(button2)
        keyboard3 = types.InlineKeyboardMarkup()
        for otvet in list(themes):
            button3 = types.InlineKeyboardButton(text=otvet, callback_data=otvet)
            keyboard3.add(button3)
        bot.send_message(message.from_user.id, text='Выберите одну из перечисленных тем для редактирования', reply_markup=keyboard)
        keybord = types.InlineKeyboardMarkup()
        button1 = types.InlineKeyboardButton(text='Добавление новой темы', callback_data='Добавление новой темы')
        button2 = types.InlineKeyboardButton(text='Добавление вопросов', callback_data='Добавление вопросов')
        button3 = types.InlineKeyboardButton(text='Добавление ответов', callback_data='Добавление ответов')
        keybord.add(button1, button2, button3)
        bot.send_message(message.from_user.id, text='Добро пожаловать в телеграм бот (Администратор)')
        bot.send_message(message.from_user.id, text='Выберите одну из кнопок', reply_markup=keybord)

@bot.callback_query_handler(func=lambda call:True)
def callback_worker(call):
    bot.clear_step_handler_by_chat_id(chat_id=call.message.chat.id)
    if call.data == 'Добавление новой темы':
        bot.send_message(call.from_user.id, text='Напишите название для новой темы')
        bot.register_next_step_handler(call.message, get_theme)
    elif call.data == 'Добавление вопросов':
        bot.send_message(call.from_user.id, text='Напишите вопросы')
        bot.register_next_step_handler(call.message, get_question)
    elif call.data == 'Добавление ответов':
        bot.send_message(call.from_user.id, text='Напишите ответы')
        bot.register_next_step_handler(call.message, get_otvet)
    elif call.data == 'Изменение темы':
        bot.send_message(call.from_user.id, text='Напишите новое название для темы')
        bot.register_next_step_handler(call.message, edit_theme_name)
    elif call.data == 'Изменение вопросов':
        bot.send_message(call.from_user.id, text='Напишите новый вопрос для темы')
        bot.register_next_step_handler(call.message, edit_question)
    elif call.data == 'Изменение ответов':
        bot.send_message(call.from_user.id, text='Напишите новый ответ для темы')
        bot.register_next_step_handler(call.message, get_editing)
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

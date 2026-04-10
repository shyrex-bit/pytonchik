import os
import telebot
from telebot import types

TOKEN = "8613202718:AAEcntvqJh0dphNRscv1oZLZNGT_XT3N9qY"
bot = telebot.TeleBot(TOKEN)

records = {}    
sessions = {}   

def main_menu_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Записаться на занятие", callback_data="register"))
    kb.add(types.InlineKeyboardButton("Показать все записи", callback_data="show_all"))
    return kb

def direction_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Python", callback_data="dir:Python"))
    kb.add(types.InlineKeyboardButton("Web-разработка", callback_data="dir:Web"))
    kb.add(types.InlineKeyboardButton("Разработка игр", callback_data="dir:Games"))
    return kb

def confirm_kb():
    kb = types.InlineKeyboardMarkup()
    kb.add(types.InlineKeyboardButton("Да", callback_data="confirm:yes"))
    kb.add(types.InlineKeyboardButton("Нет", callback_data="confirm:no"))
    return kb

@bot.message_handler(commands=["start"])
def start_cmd(msg):
    sessions.pop(msg.from_user.id, None)
    bot.send_message(msg.chat.id, "Добро пожаловать в бот записи на пробное занятие! Выберите действие:", reply_markup=main_menu_kb())

@bot.callback_query_handler(func=lambda c: c.data == "register")
def cb_register(call):
    uid = call.from_user.id
    sessions[uid] = {'step': 'name', 'data': {}}
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, "Введите имя ученика (от 2 до 20 символов):")

@bot.callback_query_handler(func=lambda c: c.data == "show_all")
def cb_show_all(call):
    bot.answer_callback_query(call.id)
    if not records:
        bot.send_message(call.message.chat.id, "Записей пока нет.")
        return
    lines = []
    for uid, d in records.items():
        lines.append(f"{d['student_name']}, {d['student_age']} лет — {d['course_direction']} (user {uid})")
    bot.send_message(call.message.chat.id, "\n".join(lines))

@bot.message_handler(func=lambda m: sessions.get(m.from_user.id, {}).get('step') == 'name')
def handle_name(msg):
    uid = msg.from_user.id
    text = msg.text.strip()
    if len(text) < 2 or len(text) > 20:
        bot.send_message(msg.chat.id, "Ошибка: имя должно быть от 2 до 20 символов. Введите имя ещё раз:")
        return
    sessions[uid]['data']['student_name'] = text
    sessions[uid]['step'] = 'age'
    bot.send_message(msg.chat.id, "Введите возраст ученика (от 7 до 17 лет):")

@bot.message_handler(func=lambda m: sessions.get(m.from_user.id, {}).get('step') == 'age')
def handle_age(msg):
    uid = msg.from_user.id
    text = msg.text.strip()
    if not text.isdigit():
        bot.send_message(msg.chat.id, "Ошибка: введите число. Возраст (7-17):")
        return
    age = int(text)
    if age < 7 or age > 17:
        bot.send_message(msg.chat.id, "Ошибка: возраст должен быть от 7 до 17. Введите возраст заново:")
        return
    sessions[uid]['data']['student_age'] = age
    sessions[uid]['step'] = 'direction'
    bot.send_message(msg.chat.id, "Выберите направление обучения:", reply_markup=direction_kb())

@bot.callback_query_handler(func=lambda c: c.data.startswith("dir:"))
def cb_direction(call):
    uid = call.from_user.id
    if uid not in sessions or sessions[uid].get('step') != 'direction':
        bot.answer_callback_query(call.id, "Сессия не найдена. Начните заново /start")
        return
    code = call.data.split(":", 1)[1]
    mapping = {'Python': 'Python', 'Web': 'Web-разработка', 'Games': 'Разработка игр'}
    sessions[uid]['data']['course_direction'] = mapping.get(code, code)
    sessions[uid]['step'] = 'confirm'
    d = sessions[uid]['data']
    text = f"Проверка данных:\nИмя: {d['student_name']}\nВозраст: {d['student_age']}\nНаправление: {d['course_direction']}\n\nСохранить запись?"
    bot.answer_callback_query(call.id)
    bot.send_message(call.message.chat.id, text, reply_markup=confirm_kb())

@bot.callback_query_handler(func=lambda c: c.data.startswith("confirm:"))
def cb_confirm(call):
    uid = call.from_user.id
    bot.answer_callback_query(call.id)
    if uid not in sessions:
        bot.send_message(call.message.chat.id, "Сессия не найдена. Начните /start")
        return
    ans = call.data.split(":",1)[1]
    if ans == "yes":
        records[uid] = sessions[uid]['data']
        bot.send_message(call.message.chat.id, "Запись успешно сохранена. Для возврата в меню используйте /start")
    else:
        bot.send_message(call.message.chat.id, "Запись отменена. Для возврата в меню используйте /start")
    sessions.pop(uid, None)

@bot.message_handler(func=lambda m: True)
def fallback(msg):
    uid = msg.from_user.id
    if uid in sessions:
        step = sessions[uid].get('step')
        if step == 'name':
            handle_name(msg); return
        if step == 'age':
            handle_age(msg); return
    bot.send_message(msg.chat.id, "Не понимаю. Используйте /start для начала.")

bot.infinity_polling()
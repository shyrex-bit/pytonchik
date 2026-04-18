import telebot
from telebot import types
from telebot.handler_backends import State, StatesGroup
from telebot.storage import StateMemoryStorage

TOKEN = "8613202718:AAEcntvqJh0dphNRscv1oZLZNGT_XT3N9qY"
bot = telebot.TeleBot(TOKEN, state_storage=StateMemoryStorage())


class RegStates(StatesGroup):
    name = State()
    age = State()
    direction = State()
    confirm = State()

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


def _get_global_store():
    with bot.retrieve_data(0, 0) as g:
        if 'records' not in g:
            g['records'] = {}
        return g  
@bot.message_handler(commands=["start"])
def start_cmd(msg):
    bot.delete_state(msg.from_user.id, msg.chat.id)
    bot.send_message(msg.chat.id, "Добро пожаловать в бот записи на пробное занятие! Выберите действие:", reply_markup=main_menu_kb())

@bot.callback_query_handler(func=lambda c: c.data == "register")
def cb_register(call):
    uid, chat = call.from_user.id, call.message.chat.id
    bot.set_state(uid, RegStates.name, chat)
    # clear any previous data for this user
    with bot.retrieve_data(uid, chat) as data:
        data.clear()
    bot.answer_callback_query(call.id)
    bot.send_message(chat, "Введите имя ученика (от 2 до 20 символов):")

@bot.callback_query_handler(func=lambda c: c.data == "show_all")
def cb_show_all(call):
    bot.answer_callback_query(call.id)
    with bot.retrieve_data(0, 0) as g:
        recs = g.get('records', {})
    if not recs:
        bot.send_message(call.message.chat.id, "Записей пока нет.")
        return
    lines = []
    for uid_str, d in recs.items():
        # uid_str может быть строкой
        lines.append(f"{d.get('student_name')}, {d.get('student_age')} лет — {d.get('course_direction')} (user {uid_str})")
    bot.send_message(call.message.chat.id, "\n".join(lines))

@bot.message_handler(state=RegStates.name)
def handle_name(msg):
    uid, chat = msg.from_user.id, msg.chat.id
    text = (msg.text or "").strip()
    if len(text) < 2 or len(text) > 20:
        bot.send_message(chat, "Ошибка: имя должно быть от 2 до 20 символов. Введите имя ещё раз:")
        return
    with bot.retrieve_data(uid, chat) as data:
        data['student_name'] = text
    bot.set_state(uid, RegStates.age, chat)
    bot.send_message(chat, "Введите возраст ученика (от 7 до 17 лет):")

@bot.message_handler(state=RegStates.age)
def handle_age(msg):
    uid, chat = msg.from_user.id, msg.chat.id
    text = (msg.text or "").strip()
    if not text.isdigit():
        bot.send_message(chat, "Ошибка: введите число. Возраст (7-17):")
        return
    age = int(text)
    if age < 7 or age > 17:
        bot.send_message(chat, "Ошибка: возраст должен быть от 7 до 17. Введите возраст заново:")
        return
    with bot.retrieve_data(uid, chat) as data:
        data['student_age'] = age
    bot.set_state(uid, RegStates.direction, chat)
    bot.send_message(chat, "Выберите направление обучения:", reply_markup=direction_kb())

@bot.callback_query_handler(func=lambda c: c.data.startswith("dir:"), state=RegStates.direction)
def cb_direction(call):
    uid, chat = call.from_user.id, call.message.chat.id
    code = call.data.split(":", 1)[1]
    mapping = {'Python': 'Python', 'Web': 'Web-разработка', 'Games': 'Разработка игр'}
    with bot.retrieve_data(uid, chat) as data:
        data['course_direction'] = mapping.get(code, code)
    bot.set_state(uid, RegStates.confirm, chat)
    with bot.retrieve_data(uid, chat) as d:
        text = (f"Проверка данных:\nИмя: {d.get('student_name')}\n"
                f"Возраст: {d.get('student_age')}\nНаправление: {d.get('course_direction')}\n\nСохранить запись?")
    bot.answer_callback_query(call.id)
    bot.send_message(chat, text, reply_markup=confirm_kb())

@bot.callback_query_handler(func=lambda c: c.data.startswith("confirm:"), state=RegStates.confirm)
def cb_confirm(call):
    uid, chat = call.from_user.id, call.message.chat.id
    ans = call.data.split(":", 1)[1]
    bot.answer_callback_query(call.id)
    if ans == "yes":
        # берем данные пользователя и сохраняем в глобальное state-хранилище
        with bot.retrieve_data(uid, chat) as pdata:
            user_data = dict(pdata)  # копируем
        with bot.retrieve_data(0, 0) as g:
            recs = g.setdefault('records', {})
            recs[str(uid)] = user_data
        bot.send_message(chat, "Запись успешно сохранена. Для возврата в меню используйте /start")
    else:
        bot.send_message(chat, "Запись отменена. Для возврата в меню используйте /start")
    bot.delete_state(uid, chat)

@bot.message_handler(func=lambda m: True)
def fallback(msg):
    st = bot.get_state(msg.from_user.id, msg.chat.id)
    if st is None:
        bot.send_message(msg.chat.id, "Не понимаю. Используйте /start для начала.")
        return
    # give a helpful prompt depending on current state
    if st == RegStates.name:
        bot.send_message(msg.chat.id, "Введите имя ученика (от 2 до 20 символов):")
    elif st == RegStates.age:
        bot.send_message(msg.chat.id, "Введите возраст ученика (от 7 до 17 лет):")
    else:
        bot.send_message(msg.chat.id, "Используйте кнопки или /start для возврата в меню.")

if __name__ == "__main__":
    bot.infinity_polling()
# ...existing code...
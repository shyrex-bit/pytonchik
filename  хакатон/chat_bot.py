import sqlite3
import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.states.sync.middleware import StateMiddleware
from telebot.storage import StateMemoryStorage


BOT_TOKEN = "8713877873:AAGqd8kse3n25s1_D6oHa5b3VG1jMeKMj7o"

bot = telebot.TeleBot(
    BOT_TOKEN,
    state_storage=StateMemoryStorage(),
    use_class_middlewares=True,
)

DB_NAME = "home_tasks.db"


class HomeStates(StatesGroup):
    main_menu_buttons_press = State()
    choose_category = State()
    input_task_title = State()
    input_task_date = State()
    input_done_task_id = State()
    input_delete_task_id = State()


def init_db():
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute("""
        CREATE TABLE IF NOT EXISTS tasks (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER NOT NULL,
            category TEXT NOT NULL,
            title TEXT NOT NULL,
            date TEXT NOT NULL,
            is_done INTEGER DEFAULT 0
        )
    """)

    connection.commit()
    connection.close()


def add_task(user_id, category, title, date):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "INSERT INTO tasks (user_id, category, title, date) VALUES (?, ?, ?, ?)",
        (user_id, category, title, date)
    )

    connection.commit()
    connection.close()


def get_tasks(user_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, category, title, date, is_done FROM tasks WHERE user_id = ?",
        (user_id,)
    )

    tasks = cursor.fetchall()
    connection.close()
    return tasks


def get_active_tasks(user_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "SELECT id, category, title, date FROM tasks WHERE user_id = ? AND is_done = 0",
        (user_id,)
    )

    tasks = cursor.fetchall()
    connection.close()
    return tasks


def mark_task_done(user_id, task_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "UPDATE tasks SET is_done = 1 WHERE user_id = ? AND id = ?",
        (user_id, task_id)
    )

    connection.commit()
    changed_rows = cursor.rowcount
    connection.close()

    return changed_rows > 0


def delete_task(user_id, task_id):
    connection = sqlite3.connect(DB_NAME)
    cursor = connection.cursor()

    cursor.execute(
        "DELETE FROM tasks WHERE user_id = ? AND id = ?",
        (user_id, task_id)
    )

    connection.commit()
    changed_rows = cursor.rowcount
    connection.close()

    return changed_rows > 0


def build_main_menu_keyboard():
    inline_keyboard = telebot.types.InlineKeyboardMarkup()

    button_add = telebot.types.InlineKeyboardButton(
        "➕ Добавить задачу", callback_data="button_add_task"
    )
    button_tasks = telebot.types.InlineKeyboardButton(
        "📋 Мои задачи", callback_data="button_show_tasks"
    )
    button_done = telebot.types.InlineKeyboardButton(
        "✅ Отметить выполненной", callback_data="button_done_task"
    )
    button_delete = telebot.types.InlineKeyboardButton(
        "🗑 Удалить задачу", callback_data="button_delete_task"
    )
    button_help = telebot.types.InlineKeyboardButton(
        "ℹ️ Помощь", callback_data="button_help"
    )

    inline_keyboard.add(button_add)
    inline_keyboard.add(button_tasks)
    inline_keyboard.add(button_done)
    inline_keyboard.add(button_delete)
    inline_keyboard.add(button_help)

    return inline_keyboard


def build_categories_keyboard():
    inline_keyboard = telebot.types.InlineKeyboardMarkup()

    button_cleaning = telebot.types.InlineKeyboardButton(
        "🧹 Уборка", callback_data="🧹 Уборка"
    )
    button_shopping = telebot.types.InlineKeyboardButton(
        "🛒 Покупки", callback_data="🛒 Покупки"
    )
    button_plants = telebot.types.InlineKeyboardButton(
        "🌱 Растения", callback_data="🌱 Растения"
    )
    button_cooking = telebot.types.InlineKeyboardButton(
        "🍳 Готовка", callback_data="🍳 Готовка"
    )
    button_pets = telebot.types.InlineKeyboardButton(
        "🐾 Питомцы", callback_data="🐾 Питомцы"
    )
    button_other = telebot.types.InlineKeyboardButton(
        "📌 Другое", callback_data="📌 Другое"
    )

    inline_keyboard.add(button_cleaning)
    inline_keyboard.add(button_shopping)
    inline_keyboard.add(button_plants)
    inline_keyboard.add(button_cooking)
    inline_keyboard.add(button_pets)
    inline_keyboard.add(button_other)

    return inline_keyboard


def send_main_menu(chat_id):
    output_text = (
        "Привет! Я бот для домашней рутины 🏠\n"
        "Я помогу тебе не забывать про уборку, покупки, растения, готовку и питомцев.\n\n"
        "Выбери нужное действие:"
    )

    bot.send_message(chat_id, output_text, reply_markup=build_main_menu_keyboard())


def show_tasks(message):
    tasks = get_tasks(message.from_user.id)

    if len(tasks) == 0:
        bot.send_message(
            message.chat.id,
            "Пока задач нет. Добавь первую задачу 🏠",
            reply_markup=build_main_menu_keyboard()
        )
        return

    output_text = "Твои задачи:\n\n"

    for task in tasks:
        task_id, category, title, date, is_done = task
        status = "✅" if is_done == 1 else "❌"
        output_text += f"{task_id}. [{category}] {title} — {date} {status}\n"

    bot.send_message(
        message.chat.id,
        output_text,
        reply_markup=build_main_menu_keyboard()
    )


@bot.message_handler(commands=["start"])
def command_start_handler(message: types.Message, state: StateContext):
    state.delete()
    state.set(HomeStates.main_menu_buttons_press)
    send_main_menu(message.chat.id)


@bot.message_handler(commands=["help"])
def command_help_handler(message: types.Message, state: StateContext):
    output_text = (
        "Я умею:\n"
        "➕ добавлять домашние задачи\n"
        "📋 показывать список задач\n"
        "✅ отмечать задачи выполненными\n"
        "🗑 удалять задачи\n\n"
        "Команды:\n"
        "/start — главное меню\n"
        "/add — добавить задачу\n"
        "/tasks — показать задачи\n"
        "/done — отметить выполненной\n"
        "/delete — удалить задачу\n"
        "/cancel — отменить действие"
    )

    bot.send_message(message.chat.id, output_text, reply_markup=build_main_menu_keyboard())


@bot.message_handler(commands=["add"])
def command_add_handler(message: types.Message, state: StateContext):
    output_text = "Выбери категорию задачи:"

    state.set(HomeStates.choose_category)

    bot.send_message(
        message.chat.id,
        output_text,
        reply_markup=build_categories_keyboard()
    )


@bot.message_handler(commands=["tasks"])
def command_tasks_handler(message: types.Message):
    show_tasks(message)


@bot.message_handler(commands=["done"])
def command_done_handler(message: types.Message, state: StateContext):
    active_tasks = get_active_tasks(message.from_user.id)

    if len(active_tasks) == 0:
        bot.send_message(
            message.chat.id,
            "У тебя нет невыполненных задач ✅",
            reply_markup=build_main_menu_keyboard()
        )
        return

    output_text = "Невыполненные задачи:\n\n"

    for task in active_tasks:
        task_id, category, title, date = task
        output_text += f"{task_id}. [{category}] {title} — {date}\n"

    output_text += "\nВведи номер задачи, которую нужно отметить выполненной."

    state.set(HomeStates.input_done_task_id)

    bot.send_message(message.chat.id, output_text)


@bot.message_handler(commands=["delete"])
def command_delete_handler(message: types.Message, state: StateContext):
    tasks = get_tasks(message.from_user.id)

    if len(tasks) == 0:
        bot.send_message(
            message.chat.id,
            "У тебя пока нет задач для удаления.",
            reply_markup=build_main_menu_keyboard()
        )
        return

    output_text = "Твои задачи:\n\n"

    for task in tasks:
        task_id, category, title, date, is_done = task
        status = "✅" if is_done == 1 else "❌"
        output_text += f"{task_id}. [{category}] {title} — {date} {status}\n"

    output_text += "\nВведи номер задачи, которую нужно удалить."

    state.set(HomeStates.input_delete_task_id)

    bot.send_message(message.chat.id, output_text)


@bot.message_handler(commands=["cancel"])
def command_cancel_handler(message: types.Message, state: StateContext):
    state.delete()

    bot.send_message(
        message.chat.id,
        "Действие отменено.",
        reply_markup=build_main_menu_keyboard()
    )


@bot.callback_query_handler(state=HomeStates.main_menu_buttons_press)
def callback_main_menu_handler(call: types.CallbackQuery, state: StateContext):
    bot.answer_callback_query(call.id)

    if call.data == "button_add_task":
        output_text = "Выбери категорию задачи:"

        state.set(HomeStates.choose_category)

        bot.send_message(
            call.message.chat.id,
            output_text,
            reply_markup=build_categories_keyboard()
        )

    elif call.data == "button_show_tasks":
        fake_message = call.message
        fake_message.from_user = call.from_user
        show_tasks(fake_message)

    elif call.data == "button_done_task":
        active_tasks = get_active_tasks(call.from_user.id)

        if len(active_tasks) == 0:
            bot.send_message(
                call.message.chat.id,
                "У тебя нет невыполненных задач ✅",
                reply_markup=build_main_menu_keyboard()
            )
            return

        output_text = "Невыполненные задачи:\n\n"

        for task in active_tasks:
            task_id, category, title, date = task
            output_text += f"{task_id}. [{category}] {title} — {date}\n"

        output_text += "\nВведи номер задачи, которую нужно отметить выполненной."

        state.set(HomeStates.input_done_task_id)

        bot.send_message(call.message.chat.id, output_text)

    elif call.data == "button_delete_task":
        tasks = get_tasks(call.from_user.id)

        if len(tasks) == 0:
            bot.send_message(
                call.message.chat.id,
                "У тебя пока нет задач для удаления.",
                reply_markup=build_main_menu_keyboard()
            )
            return

        output_text = "Твои задачи:\n\n"

        for task in tasks:
            task_id, category, title, date, is_done = task
            status = "✅" if is_done == 1 else "❌"
            output_text += f"{task_id}. [{category}] {title} — {date} {status}\n"

        output_text += "\nВведи номер задачи, которую нужно удалить."

        state.set(HomeStates.input_delete_task_id)

        bot.send_message(call.message.chat.id, output_text)

    elif call.data == "button_help":
        output_text = (
            "Я умею:\n"
            "➕ добавлять домашние задачи\n"
            "📋 показывать список задач\n"
            "✅ отмечать задачи выполненными\n"
            "🗑 удалять задачи"
        )

        bot.send_message(call.message.chat.id, output_text)


@bot.callback_query_handler(state=HomeStates.choose_category)
def callback_choose_category_handler(call: types.CallbackQuery, state: StateContext):
    bot.answer_callback_query(call.id)

    state.add_data(category=call.data)

    output_text = "Напиши название задачи. Например: Полить фикус"

    state.set(HomeStates.input_task_title)

    bot.send_message(call.message.chat.id, output_text)


@bot.message_handler(state=HomeStates.input_task_title)
def message_input_task_title_handler(message: types.Message, state: StateContext):
    title = message.text.strip()

    if len(title) == 0:
        bot.send_message(message.chat.id, "Ошибка. Название задачи не может быть пустым.")
        return

    if len(title) > 100:
        bot.send_message(message.chat.id, "Ошибка. Название задачи слишком длинное.")
        return

    state.add_data(title=title)

    output_text = (
        "Когда нужно выполнить задачу?\n"
        "Например: сегодня, завтра, каждый понедельник, каждые 3 дня."
    )

    state.set(HomeStates.input_task_date)

    bot.send_message(message.chat.id, output_text)


@bot.message_handler(state=HomeStates.input_task_date)
def message_input_task_date_handler(message: types.Message, state: StateContext):
    date = message.text.strip()

    if len(date) == 0:
        bot.send_message(message.chat.id, "Ошибка. Дата не может быть пустой.")
        return

    state.add_data(date=date)

    with state.data() as data:
        category = data["category"]
        title = data["title"]
        task_date = data["date"]

    add_task(message.from_user.id, category, title, task_date)

    state.delete()
    state.set(HomeStates.main_menu_buttons_press)

    bot.send_message(
        message.chat.id,
        "Задача добавлена ✅",
        reply_markup=build_main_menu_keyboard()
    )


@bot.message_handler(state=HomeStates.input_done_task_id)
def message_input_done_task_id_handler(message: types.Message, state: StateContext):
    task_id_text = message.text.strip()

    if task_id_text.isdigit() == False:
        bot.send_message(
            message.chat.id,
            "Ошибка. Введи номер задачи цифрой или нажми /cancel."
        )
        return

    task_id = int(task_id_text)
    result = mark_task_done(message.from_user.id, task_id)

    if result == False:
        bot.send_message(
            message.chat.id,
            "Задача не найдена. Попробуй ещё раз или нажми /cancel."
        )
        return

    state.delete()
    state.set(HomeStates.main_menu_buttons_press)

    bot.send_message(
        message.chat.id,
        "Задача отмечена как выполненная ✅",
        reply_markup=build_main_menu_keyboard()
    )


@bot.message_handler(state=HomeStates.input_delete_task_id)
def message_input_delete_task_id_handler(message: types.Message, state: StateContext):
    task_id_text = message.text.strip()

    if task_id_text.isdigit() == False:
        bot.send_message(
            message.chat.id,
            "Ошибка. Введи номер задачи цифрой или нажми /cancel."
        )
        return

    task_id = int(task_id_text)
    result = delete_task(message.from_user.id, task_id)

    if result == False:
        bot.send_message(
            message.chat.id,
            "Задача не найдена. Попробуй ещё раз или нажми /cancel."
        )
        return

    state.delete()
    state.set(HomeStates.main_menu_buttons_press)

    bot.send_message(
        message.chat.id,
        "Задача удалена 🗑",
        reply_markup=build_main_menu_keyboard()
    )


@bot.message_handler()
def message_unknown_handler(message: types.Message):
    bot.send_message(
        message.chat.id,
        "Я не понял сообщение. Нажми /start, чтобы открыть главное меню."
    )


init_db()

bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.setup_middleware(StateMiddleware(bot))

bot.infinity_polling()
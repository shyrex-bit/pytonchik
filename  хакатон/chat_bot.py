# ...existing code... 

import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.states.sync.middleware import StateMiddleware
from telebot.storage import StateMemoryStorage

# Токен (в реальном проекте хранить в переменной окружения)
TOKEN = "8610851744:AAESwcQaW89k33kOMsiClZS6KJgKItSnP74"

bot = telebot.TeleBot(
    TOKEN,
    state_storage=StateMemoryStorage(),
    use_class_middlewares=True,
)

# --- Простое in-memory хранилище вместо sqlite ---
USERS = set()   # множество user_id
TASKS = []      # список записей: dict {user_id, task_name, task_time, task_type}

def add_user(user_id: int):
    USERS.add(user_id)

def create_task(user_id: int, task_title: str, task_time: str, task_category: str):
    TASKS.append({
        "user_id": user_id,
        "task_name": task_title,
        "task_time": task_time,
        "task_type": task_category,
    })

def get_user_tasks_list(user_id: int):
    return [(t["task_name"], t["task_time"]) for t in TASKS if t["user_id"] == user_id]

def get_all_users():
    # вернуть всех известных пользователей (из USERS)
    return list(USERS)

# --- Стейты ---
class AppStates(StatesGroup):
    main_menu = State()
    choose_time = State()
    admin_password = State()
    admin_pagination = State()

# --- Клавиатуры ---
def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.row("🌿 Растения", "🐾 Питомцы")
    kb.row("🧹 Уборка", "🛒 Покупки")
    kb.row("📊 Статистика", "📋 Мои задачи")
    return kb

def build_pagination_kb(prev_enabled: bool, next_enabled: bool):
    kb = types.InlineKeyboardMarkup()
    btns = []
    if prev_enabled:
        btns.append(types.InlineKeyboardButton("⬅️ Назад", callback_data="admin_prev"))
    if next_enabled:
        btns.append(types.InlineKeyboardButton("Вперёд ➡️", callback_data="admin_next"))
    if btns:
        kb.row(*btns)
    return kb

# --- Обработчики ---
@bot.message_handler(commands=["start"])
def cmd_start(message: types.Message, state: StateContext):
    add_user(message.from_user.id)
    # очистить state пользователя и установить main_menu
    state.delete()
    state.set(AppStates.main_menu)
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в Home Harmony! Выберите категорию:",
        reply_markup=main_keyboard(),
    )

@bot.message_handler(func=lambda m: isinstance(m.text, str) and m.text in ["🌿 Растения", "🐾 Питомцы", "🧹 Уборка", "🛒 Покупки"], state=AppStates.main_menu)
def category_chosen(message: types.Message, state: StateContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text
    if text == "🌿 Растения":
        task_title = "Полив растений"
    elif text == "🐾 Питомцы":
        task_title = "Кормление питомцев"
    elif text == "🧹 Уборка":
        task_title = "Уборка"
    else:
        task_title = "Список покупок"

    # сохраняем выбор в state и просим время
    state.add_data(task_title=task_title, task_category="общая")
    state.set(AppStates.choose_time)
    bot.send_message(chat_id, f"Вы выбрали задачу: {task_title}. Когда выполнить? (формат ЧЧ:ММ)")

@bot.message_handler(state=AppStates.choose_time)
def handle_time(message: types.Message, state: StateContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    task_time = (message.text or "").strip()
    if len(task_time) != 5 or task_time[2] != ":" or not task_time[:2].isdigit() or not task_time[3:].isdigit():
        bot.send_message(chat_id, "Неверный формат времени. Введите в формате ЧЧ:ММ, например 08:30.")
        return
    hh = int(task_time[:2])
    mm = int(task_time[3:])
    if not (0 <= hh <= 23 and 0 <= mm <= 59):
        bot.send_message(chat_id, "Неверное время. Введите корректное время ЧЧ:ММ.")
        return

    # получить временные данные и сохранить задачу
    with state.data() as data:
        task_title = data.get("task_title", "Задача")
        task_category = data.get("task_category", "общая")

    create_task(user_id, task_title, task_time, task_category)
    state.delete()
    bot.send_message(chat_id, f"Задача '{task_title}' добавлена на {task_time}.", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: isinstance(m.text, str) and m.text == "📋 Мои задачи", state=AppStates.main_menu)
def my_tasks(message: types.Message, state: StateContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    tasks = get_user_tasks_list(user_id)
    if not tasks:
        bot.send_message(chat_id, "У вас пока нет задач.")
        return
    lines = [f"- {t[0]} в {t[1]}" for t in tasks]
    bot.send_message(chat_id, "Ваши задачи:\n" + "\n".join(lines))

@bot.message_handler(func=lambda m: isinstance(m.text, str) and m.text == "📊 Статистика", state=AppStates.main_menu)
def stats_handler(message: types.Message, state: StateContext):
    # админская команда: запрашиваем пароль
    state.set(AppStates.admin_password)
    bot.send_message(message.chat.id, "Введите пароль администратора для просмотра статистики:")

@bot.message_handler(state=AppStates.admin_password)
def check_admin_password(message: types.Message, state: StateContext):
    pwd = (message.text or "").strip()
    if pwd != "12345":
        bot.send_message(message.chat.id, "Неверный пароль. Введите ещё раз или вернитесь в меню /start")
        return

    users = get_all_users()
    if not users:
        bot.send_message(message.chat.id, "Пользователей пока нет. Вернитесь в меню /start")
        state.delete()
        return

    # формируем страницы простым способом из TASKS
    lines = []
    rows = sorted(TASKS, key=lambda r: r["user_id"])
    for r in rows:
        lines.append(f"user {r['user_id']} — {r['task_name']} @ {r['task_time']}")

    # простая постраничка по 8 строк
    page_size = 8
    pages = [lines[i : i + page_size] for i in range(0, len(lines), page_size)]
    if not pages:
        bot.send_message(message.chat.id, "Записей нет.")
        state.delete()
        return

    state.add_data(admin_pages=pages, admin_page_index=0)
    state.set(AppStates.admin_pagination)

    page_text = "\n".join(pages[0]) + "\n\nВернитесь в меню: /start"
    kb = build_pagination_kb(prev_enabled=False, next_enabled=(len(pages) > 1))
    bot.send_message(message.chat.id, page_text, reply_markup=kb)

@bot.callback_query_handler(state=AppStates.admin_pagination)
def admin_pagination_cb(call: types.CallbackQuery, state: StateContext):
    if call.data not in ("admin_prev", "admin_next"):
        bot.answer_callback_query(call.id)
        return

    with state.data() as data:
        pages = data.get("admin_pages", [])
        idx = data.get("admin_page_index", 0)

    if not pages:
        bot.answer_callback_query(call.id, "Список не найден.")
        return

    if call.data == "admin_prev" and idx > 0:
        idx -= 1
    if call.data == "admin_next" and idx < len(pages) - 1:
        idx += 1

    state.add_data(admin_page_index=idx)
    page_text = "\n".join(pages[idx]) + "\n\nВернитесь в меню: /start"
    kb = build_pagination_kb(prev_enabled=(idx > 0), next_enabled=(idx < len(pages) - 1))

    bot.edit_message_text(page_text, call.message.chat.id, call.message.message_id, reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: True)
def fallback(message: types.Message):
    # если нет состояния — подсказка
    st = bot.get_state(message.from_user.id, message.chat.id)
    if st is None:
        bot.send_message(message.chat.id, "Не понял. Используйте /start для начала.", reply_markup=main_keyboard())
    else:
        bot.send_message(message.chat.id, "Следуйте подсказкам или введите /start для отмены.")

# middleware и фильтры как в sample1
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.setup_middleware(StateMiddleware(bot))

bot.infinity_polling()
# ...existing code...
```# filepath: /Users/ildar/Desktop/pytonchik/ хакатон/chat_bot.py
# ...existing code...
import warnings
from urllib3.exceptions import NotOpenSSLWarning
warnings.filterwarnings("ignore", category=NotOpenSSLWarning)

import telebot
from telebot import custom_filters, types
from telebot.states import State, StatesGroup
from telebot.states.sync.context import StateContext
from telebot.states.sync.middleware import StateMiddleware
from telebot.storage import StateMemoryStorage

# Токен (в реальном проекте хранить в переменной окружения)
TOKEN = "8610851744:AAESwcQaW89k33kOMsiClZS6KJgKItSnP74"

bot = telebot.TeleBot(
    TOKEN,
    state_storage=StateMemoryStorage(),
    use_class_middlewares=True,
)

# --- Простое in-memory хранилище вместо sqlite ---
USERS = set()   # множество user_id
TASKS = []      # список записей: dict {user_id, task_name, task_time, task_type}

def add_user(user_id: int):
    USERS.add(user_id)

def create_task(user_id: int, task_title: str, task_time: str, task_category: str):
    TASKS.append({
        "user_id": user_id,
        "task_name": task_title,
        "task_time": task_time,
        "task_type": task_category,
    })

def get_user_tasks_list(user_id: int):
    return [(t["task_name"], t["task_time"]) for t in TASKS if t["user_id"] == user_id]

def get_all_users():
    # вернуть всех известных пользователей (из USERS)
    return list(USERS)

# --- Стейты ---
class AppStates(StatesGroup):
    main_menu = State()
    choose_time = State()
    admin_password = State()
    admin_pagination = State()

# --- Клавиатуры ---
def main_keyboard():
    kb = types.ReplyKeyboardMarkup(resize_keyboard=True, one_time_keyboard=False)
    kb.row("🌿 Растения", "🐾 Питомцы")
    kb.row("🧹 Уборка", "🛒 Покупки")
    kb.row("📊 Статистика", "📋 Мои задачи")
    return kb

def build_pagination_kb(prev_enabled: bool, next_enabled: bool):
    kb = types.InlineKeyboardMarkup()
    btns = []
    if prev_enabled:
        btns.append(types.InlineKeyboardButton("⬅️ Назад", callback_data="admin_prev"))
    if next_enabled:
        btns.append(types.InlineKeyboardButton("Вперёд ➡️", callback_data="admin_next"))
    if btns:
        kb.row(*btns)
    return kb

# --- Обработчики ---
@bot.message_handler(commands=["start"])
def cmd_start(message: types.Message, state: StateContext):
    add_user(message.from_user.id)
    # очистить state пользователя и установить main_menu
    state.delete()
    state.set(AppStates.main_menu)
    bot.send_message(
        message.chat.id,
        "Добро пожаловать в Home Harmony! Выберите категорию:",
        reply_markup=main_keyboard(),
    )

@bot.message_handler(func=lambda m: isinstance(m.text, str) and m.text in ["🌿 Растения", "🐾 Питомцы", "🧹 Уборка", "🛒 Покупки"], state=AppStates.main_menu)
def category_chosen(message: types.Message, state: StateContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    text = message.text
    if text == "🌿 Растения":
        task_title = "Полив растений"
    elif text == "🐾 Питомцы":
        task_title = "Кормление питомцев"
    elif text == "🧹 Уборка":
        task_title = "Уборка"
    else:
        task_title = "Список покупок"

    # сохраняем выбор в state и просим время
    state.add_data(task_title=task_title, task_category="общая")
    state.set(AppStates.choose_time)
    bot.send_message(chat_id, f"Вы выбрали задачу: {task_title}. Когда выполнить? (формат ЧЧ:ММ)")

@bot.message_handler(state=AppStates.choose_time)
def handle_time(message: types.Message, state: StateContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    task_time = (message.text or "").strip()
    if len(task_time) != 5 or task_time[2] != ":" or not task_time[:2].isdigit() or not task_time[3:].isdigit():
        bot.send_message(chat_id, "Неверный формат времени. Введите в формате ЧЧ:ММ, например 08:30.")
        return
    hh = int(task_time[:2])
    mm = int(task_time[3:])
    if not (0 <= hh <= 23 and 0 <= mm <= 59):
        bot.send_message(chat_id, "Неверное время. Введите корректное время ЧЧ:ММ.")
        return

    # получить временные данные и сохранить задачу
    with state.data() as data:
        task_title = data.get("task_title", "Задача")
        task_category = data.get("task_category", "общая")

    create_task(user_id, task_title, task_time, task_category)
    state.delete()
    bot.send_message(chat_id, f"Задача '{task_title}' добавлена на {task_time}.", reply_markup=main_keyboard())

@bot.message_handler(func=lambda m: isinstance(m.text, str) and m.text == "📋 Мои задачи", state=AppStates.main_menu)
def my_tasks(message: types.Message, state: StateContext):
    user_id = message.from_user.id
    chat_id = message.chat.id
    tasks = get_user_tasks_list(user_id)
    if not tasks:
        bot.send_message(chat_id, "У вас пока нет задач.")
        return
    lines = [f"- {t[0]} в {t[1]}" for t in tasks]
    bot.send_message(chat_id, "Ваши задачи:\n" + "\n".join(lines))

@bot.message_handler(func=lambda m: isinstance(m.text, str) and m.text == "📊 Статистика", state=AppStates.main_menu)
def stats_handler(message: types.Message, state: StateContext):
    # админская команда: запрашиваем пароль
    state.set(AppStates.admin_password)
    bot.send_message(message.chat.id, "Введите пароль администратора для просмотра статистики:")

@bot.message_handler(state=AppStates.admin_password)
def check_admin_password(message: types.Message, state: StateContext):
    pwd = (message.text or "").strip()
    if pwd != "12345":
        bot.send_message(message.chat.id, "Неверный пароль. Введите ещё раз или вернитесь в меню /start")
        return

    users = get_all_users()
    if not users:
        bot.send_message(message.chat.id, "Пользователей пока нет. Вернитесь в меню /start")
        state.delete()
        return

    # формируем страницы простым способом из TASKS
    lines = []
    rows = sorted(TASKS, key=lambda r: r["user_id"])
    for r in rows:
        lines.append(f"user {r['user_id']} — {r['task_name']} @ {r['task_time']}")

    # простая постраничка по 8 строк
    page_size = 8
    pages = [lines[i : i + page_size] for i in range(0, len(lines), page_size)]
    if not pages:
        bot.send_message(message.chat.id, "Записей нет.")
        state.delete()
        return

    state.add_data(admin_pages=pages, admin_page_index=0)
    state.set(AppStates.admin_pagination)

    page_text = "\n".join(pages[0]) + "\n\nВернитесь в меню: /start"
    kb = build_pagination_kb(prev_enabled=False, next_enabled=(len(pages) > 1))
    bot.send_message(message.chat.id, page_text, reply_markup=kb)

@bot.callback_query_handler(state=AppStates.admin_pagination)
def admin_pagination_cb(call: types.CallbackQuery, state: StateContext):
    if call.data not in ("admin_prev", "admin_next"):
        bot.answer_callback_query(call.id)
        return

    with state.data() as data:
        pages = data.get("admin_pages", [])
        idx = data.get("admin_page_index", 0)

    if not pages:
        bot.answer_callback_query(call.id, "Список не найден.")
        return

    if call.data == "admin_prev" and idx > 0:
        idx -= 1
    if call.data == "admin_next" and idx < len(pages) - 1:
        idx += 1

    state.add_data(admin_page_index=idx)
    page_text = "\n".join(pages[idx]) + "\n\nВернитесь в меню: /start"
    kb = build_pagination_kb(prev_enabled=(idx > 0), next_enabled=(idx < len(pages) - 1))

    bot.edit_message_text(page_text, call.message.chat.id, call.message.message_id, reply_markup=kb)
    bot.answer_callback_query(call.id)

@bot.message_handler(func=lambda m: True)
def fallback(message: types.Message):
    # если нет состояния — подсказка
    st = bot.get_state(message.from_user.id, message.chat.id)
    if st is None:
        bot.send_message(message.chat.id, "Не понял. Используйте /start для начала.", reply_markup=main_keyboard())
    else:
        bot.send_message(message.chat.id, "Следуйте подсказкам или введите /start для отмены.")

# middleware и фильтры как в sample1
bot.add_custom_filter(custom_filters.StateFilter(bot))
bot.setup_middleware(StateMiddleware(bot))

bot.infinity_polling()
# ...existing code...
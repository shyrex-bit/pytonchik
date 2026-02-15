from dataclasses import dataclass

@dataclass
class GameComputer:
    id: int
    performance: int
    cpu: str
    video_card: str
    ssd: int
    ram: int
    weight: int
    price: int
    number_in_stock: int

def input_computer_data():
    performance = int(input("Производительность: "))
    cpu = input("Процессор: ")
    video_card = input("Видеокарта: ")
    ssd = int(input("Объем SSD (ГБ): "))
    ram = int(input("Объем RAM (ГБ): "))
    weight = int(input("Вес (кг): "))
    price = int(input("Цена: "))
    number_in_stock = int(input("Количество на складе: "))
    return GameComputer(0, performance, cpu, video_card, ssd, ram, weight, price, number_in_stock)

computers = []

def next_id():
    m = 0
    for c in computers:
        if c.id > m:
            m = c.id
    return m + 1

def print_computer(c: GameComputer):
    print(f"ID:{c.id} | perf:{c.performance} | CPU:{c.cpu} | GPU:{c.video_card} | SSD:{c.ssd}GB | RAM:{c.ram}GB | weight:{c.weight}kg | price:{c.price} | stock:{c.number_in_stock}")

def find_by_id(i):
    for c in computers:
        if c.id == i:
            return c
    return None

# 1. поиск по нескольким условиям одновременно
def search_multi():
    print("Оставьте пустым чтобы пропустить условие.")
    ram_min = input("Мин. RAM (ГБ): ").strip()
    price_max = input("Макс. цена: ").strip()
    cpu_sub = input("Часть названия CPU: ").strip().lower()
    gpu_sub = input("Часть названия GPU: ").strip().lower()

    res = []
    for c in computers:
        if ram_min and c.ram < int(ram_min): continue
        if price_max and c.price > int(price_max): continue
        if cpu_sub and cpu_sub not in c.cpu.lower(): continue
        if gpu_sub and gpu_sub not in c.video_card.lower(): continue
        res.append(c)
    if not res:
        print("Ничего не найдено.")
        return
    for r in res:
        print_computer(r)

# 2. сортировка
def sort_by_price(reverse=False):
    computers.sort(key=lambda c: c.price, reverse=reverse)
def sort_by_ram_plus_ssd(reverse=False):
    computers.sort(key=lambda c: (c.ram + c.ssd), reverse=reverse)

# 3. добавление с проверкой уникальности ИД
def add_computer():
    choose_id = input("Хотите задать ID вручную? (enter - нет / введите ID): ").strip()
    comp = input_computer_data()
    if choose_id:
        try:
            iid = int(choose_id)
        except:
            iid = None
    else:
        iid = None
    if iid is None or find_by_id(iid) is not None:
        comp.id = next_id()
        if iid is not None:
            print("ID занят — присвоен новый ID:", comp.id)
    else:
        comp.id = iid
    computers.append(comp)
    print("Добавлено:")
    print_computer(comp)

# 4. удаление: по ID или по номеру в списке
def delete_computer():
    mode = input("Удалить по (1) ID или (2) номеру в списке? (1/2): ").strip()
    if mode == "1":
        try:
            iid = int(input("ID: "))
        except:
            print("Неверный ID"); return
        c = find_by_id(iid)
        if c:
            computers.remove(c); print("Удалено")
        else:
            print("Не найдено")
    elif mode == "2":
        try:
            idx = int(input("Номер в списке (1..): ")) - 1
            comp = computers.pop(idx)
            print("Удалено:", comp.id)
        except:
            print("Неверный номер")
    else:
        print("Отмена")

# 5. увеличение объёма ОЗУ по ID
def increase_ram():
    try:
        iid = int(input("ID: "))
        add = int(input("Увеличить на (ГБ): "))
    except:
        print("Неверный ввод"); return
    c = find_by_id(iid)
    if c:
        c.ram += add
        print("Обновлено:", c.ram, "GB")
    else:
        print("Не найдено")

# 6. пометить как распродажа (уменьшить цену на 10%)
def mark_sale():
    try:
        iid = int(input("ID: "))
    except:
        print("Неверный ID"); return
    c = find_by_id(iid)
    if c:
        old = c.price
        c.price = int(c.price * 0.9)
        print(f"Цена {old} -> {c.price}")
    else:
        print("Не найдено")

# 7. самый дорогой и самый дешёвый
def show_min_max():
    if not computers:
        print("Список пуст"); return
    mx = max(computers, key=lambda c: c.price)
    mn = min(computers, key=lambda c: c.price)
    print("Самый дорогой:")
    print_computer(mx)
    print("Самый дешёвый:")
    print_computer(mn)

# 8. видеокарты не слабее заданной — простая проверка по подстроке
def show_gpu_not_weaker():
    key = input("Укажите часть имени видеокарты (например 'rtx', 'rx', 'gtx', '3060'): ").strip().lower()
    if not key:
        print("Отмена"); return
    res = [c for c in computers if key in c.video_card.lower()]
    if not res:
        print("Не найдено")
    else:
        for c in res:
            print_computer(c)

def main():
    # примеры
    if not computers:
        computers.append(GameComputer(next_id(), 9000, "Intel i7", "RTX 3060", 512, 16, 8, 150000, 3))
        computers.append(GameComputer(next_id(), 5000, "Intel i5", "GTX 1650", 256, 8, 6, 70000, 2))
    while True:
        print("\nМеню:")
        print("1 Добавить")
        print("2 Показать все")
        print("3 Поиск (несколько условий)")
        print("4 Сортировать по цене")
        print("5 Сортировать по RAM+SSD")
        print("6 Удалить (ID/номер)")
        print("7 Увеличить RAM по ID")
        print("8 Пометить как распродажа (ID)")
        print("9 Показать самый дорогой и самый дешёвый")
        print("10 Показать GPU не слабее указанной")
        print("0 Выход")
        cmd = input("Выбор: ").strip()
        if cmd == "0": break
        if cmd == "1": add_computer()
        elif cmd == "2":
            if not computers: print("Список пуст")
            for c in computers: print_computer(c)
        elif cmd == "3": search_multi()
        elif cmd == "4":
            sort_by_price()
            print("Отсортировано по цене (по возрастанию)")
        elif cmd == "5":
            sort_by_ram_plus_ssd(reverse=True)
            print("Отсортировано по сумме RAM+SSD (по убыванию)")
        elif cmd == "6": delete_computer()
        elif cmd == "7": increase_ram()
        elif cmd == "8": mark_sale()
        elif cmd == "9": show_min_max()
        elif cmd == "10": show_gpu_not_weaker()
        else:
            print("Неизвестная команда")


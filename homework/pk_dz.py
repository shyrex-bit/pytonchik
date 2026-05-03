from dataclasses import dataclass
from typing import List

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

class ComputerStore:
    def __init__(self):
        self.computers: List[GameComputer] = []

    def next_id(self):
        m = 0
        for c in self.computers:
            if c.id > m:
                m = c.id
        return m + 1

    def add_computer(self, comp: GameComputer, use_given_id=False):
        if not use_given_id or comp.id == 0 or any(c.id == comp.id for c in self.computers):
            comp.id = self.next_id()
        self.computers.append(comp)
        return comp

    def list_all(self):
        if not self.computers:
            print("Список пуст")
            return
        for c in self.computers:
            self.print_computer(c)

    def print_computer(self, c: GameComputer):
        print(f"ID:{c.id} | perf:{c.performance} | CPU:{c.cpu} | GPU:{c.video_card} | SSD:{c.ssd}GB | RAM:{c.ram}GB | weight:{c.weight}kg | price:{c.price} | stock:{c.number_in_stock}")

    def find_by_id(self, iid: int):
        for c in self.computers:
            if c.id == iid:
                return c
        return None

    def search_multi(self, ram_min="", price_max="", cpu_sub="", gpu_sub=""):
        res = []
        for c in self.computers:
            if ram_min and c.ram < int(ram_min): continue
            if price_max and c.price > int(price_max): continue
            if cpu_sub and cpu_sub.lower() not in c.cpu.lower(): continue
            if gpu_sub and gpu_sub.lower() not in c.video_card.lower(): continue
            res.append(c)
        return res

    def sort_by_price(self, reverse=False):
        self.computers.sort(key=lambda c: c.price, reverse=reverse)

    def sort_by_ram_plus_ssd(self, reverse=False):
        self.computers.sort(key=lambda c: c.ram + c.ssd, reverse=reverse)

    def delete_computer_by_id(self, iid: int):
        c = self.find_by_id(iid)
        if c:
            self.computers.remove(c)
            return True
        return False

    def delete_computer_by_index(self, idx: int):
        if 0 <= idx < len(self.computers):
            del self.computers[idx]
            return True
        return False

    def increase_ram(self, iid: int, add_gb: int):
        c = self.find_by_id(iid)
        if c:
            c.ram += add_gb
            return True
        return False

    def mark_sale(self, iid: int):
        c = self.find_by_id(iid)
        if c:
            c.price = int(c.price * 0.9)
            return True
        return False

    def show_min_max(self):
        if not self.computers:
            print("Список пуст"); return
        mx = max(self.computers, key=lambda c: c.price)
        mn = min(self.computers, key=lambda c: c.price)
        print("Самый дорогой:")
        self.print_computer(mx)
        print("Самый дешёвый:")
        self.print_computer(mn)

    def show_gpu_not_weaker(self, key: str):
        key = key.strip().lower()
        res = [c for c in self.computers if key in c.video_card.lower()]
        return res

    def save_machine(self, path: str):
        with open(path, "w", encoding="utf-8") as f:
            for c in self.computers:
                f.write(f"{c.id}\n{c.performance}\n{c.cpu}\n{c.video_card}\n{c.ssd}\n{c.ram}\n{c.weight}\n{c.price}\n{c.number_in_stock}\n")

    def load_machine(self, path: str):
        try:
            with open(path, "r", encoding="utf-8") as f:
                lines = [l.rstrip("\n") for l in f if l.rstrip("\n") != ""]
        except FileNotFoundError:
            print("Файл не найден")
            return
        i = 0
        while i + 8 < len(lines):
            try:
                iid = int(lines[i])
                perf = int(lines[i+1])
                cpu = lines[i+2]
                gpu = lines[i+3]
                ssd = int(lines[i+4])
                ram = int(lines[i+5])
                weight = int(lines[i+6])
                price = int(lines[i+7])
                stock = int(lines[i+8])
            except Exception:
                print("Ошибка формата в файле")
                return
            comp = GameComputer(iid, perf, cpu, gpu, ssd, ram, weight, price, stock)
            self.add_computer(comp, use_given_id=True)
            i += 9

def input_computer_data() -> GameComputer:
    try:
        performance = int(input("Производительность: "))
        cpu = input("Процессор: ")
        video_card = input("Видеокарта: ")
        ssd = int(input("Объем SSD (ГБ): "))
        ram = int(input("Объем RAM (ГБ): "))
        weight = int(input("Вес (кг): "))
        price = int(input("Цена: "))
        number_in_stock = int(input("Количество на складе: "))
    except Exception:
        print("Неверный ввод, попробуйте снова.")
        return GameComputer(0,0,"","",0,0,0,0,0)
    return GameComputer(0, performance, cpu, video_card, ssd, ram, weight, price, number_in_stock)

def main():
    store = ComputerStore()
    store.add_computer(GameComputer(0, 9000, "Intel i7", "RTX 3060", 512, 16, 8, 150000, 3))
    store.add_computer(GameComputer(0, 5000, "Intel i5", "GTX 1650", 256, 8, 6, 70000, 2))

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
        print("11 Сохранить в файл")
        print("12 Загрузить из файла")
        print("0 Выход")
        cmd = input("Выбор: ").strip()

        if cmd == "0":
            break
        elif cmd == "1":
            comp = input_computer_data()
            store.add_computer(comp)
            print("Добавлено:")
            store.print_computer(comp)
        elif cmd == "2":
            store.list_all()
        elif cmd == "3":
            print("Оставьте пустым чтобы пропустить условие.")
            ram_min = input("Мин. RAM (ГБ): ").strip()
            price_max = input("Макс. цена: ").strip()
            cpu_sub = input("Часть названия CPU: ").strip()
            gpu_sub = input("Часть названия GPU: ").strip()
            res = store.search_multi(ram_min, price_max, cpu_sub, gpu_sub)
            if not res:
                print("Ничего не найдено.")
            else:
                for r in res:
                    store.print_computer(r)
        elif cmd == "4":
            store.sort_by_price()
            print("Отсортировано по цене (по возрастанию)")
        elif cmd == "5":
            store.sort_by_ram_plus_ssd(reverse=True)
            print("Отсортировано по сумме RAM+SSD (по убыванию)")
        elif cmd == "6":
            mode = input("Удалить по (1) ID или (2) номеру в списке? (1/2): ").strip()
            if mode == "1":
                iid = int(input("ID: "))
                print("Удалено" if store.delete_computer_by_id(iid) else "Не найдено")
            else:
                idx = int(input("Номер в списке (1..): ")) - 1
                print("Удалено" if store.delete_computer_by_index(idx) else "Не найдено")
        elif cmd == "7":
            iid = int(input("ID: "))
            add = int(input("Увеличить на (ГБ): "))
            print("Обновлено" if store.increase_ram(iid, add) else "Не найдено")
        elif cmd == "8":
            iid = int(input("ID: "))
            print("Помечено" if store.mark_sale(iid) else "Не найдено")
        elif cmd == "9":
            store.show_min_max()
        elif cmd == "10":
            key = input("Часть имени GPU: ").strip()
            res = store.show_gpu_not_weaker(key)
            if not res:
                print("Не найдено")
            else:
                for r in res:
                    store.print_computer(r)
        elif cmd == "11":
            path = input("Путь для сохранения: ").strip()
            store.save_machine(path)
            print("Сохранено")
        elif cmd == "12":
            path = input("Путь для загрузки: ").strip()
            store.load_machine(path)
            print("Загружено")
        else:
            print("Неизвестная команда")

if __name__ == "__main__":
    main()
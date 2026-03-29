from pets import Dog, Cat, Parrot

def main():
    pets = [
        Dog("Бим", 12.0, 4, 60, 20, 3, "Лабрадор", True),
        Cat("Мурка", 4.5, 2, 50, 30, 2, True, "кровать"),
        Parrot("Кеша", 0.5, 1, 70, 10, 5, True, 25)
    ]

    print("Информация о питомцах (до кормления/игры):")
    for p in pets:
        p.print_info()
        print("----")

    print("\nКормим и играем с каждым питомцем...")
    for p in pets:
        try:
            p.feed()
        except TypeError:
            pass
        p.play()
        print("----")

    print("\nИнформация о питомцах (после):")
    for p in pets:
        p.print_info()
        print("----")

    total = sum(p.get_total_price() for p in pets)
    print(f"\nСуммарная стоимость проживания всех питомцев: {total} рублей")

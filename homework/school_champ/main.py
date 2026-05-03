from participant import Participant
from captain import Captain
from tournament import Tournament


def main():
    tournament = Tournament()

    while True:
        print("\n=== Школьный турнир знаний ===")
        print("1. Добавить обычного участника")
        print("2. Добавить капитана")
        print("3. Показать всех участников")
        print("4. Начислить баллы участнику")
        print("5. Снять баллы с участника")
        print("6. Показать рейтинг")
        print("7. Показать участников")
        print("8. Показать победителя")
        print("0. Выйти")

        choice = input("Выберите пункт: ")

        if choice == "1":
            name = input("Введите имя: ")
            school_class = input("Введите класс: ")
            tournament.add_participant(Participant(name, school_class))

        elif choice == "2":
            name = input("Введите имя: ")
            school_class = input("Введите класс: ")
            team_name = input("Введите название команды: ")
            tournament.add_participant(Captain(name, school_class, team_name))

        elif choice == "3":
            tournament.show_participants()

        elif choice == "4":
            name = input("Введите имя участника: ")
            points = int(input("Введите количество баллов: "))
            tournament.add_points_to_participant(name, points)

        elif choice == "5":
            name = input("Введите имя участника: ")
            points = int(input("Введите количество баллов: "))
            tournament.remove_points_from_participant(name, points)

        elif choice == "6":
            tournament.show_rating()

        elif choice == "7":
            tournament.show_debug_info()

        elif choice == "8":
            tournament.get_winner()

        elif choice == "0":
            print("Программа завершена.")
            break

        else:
            print("Нет такого пункта меню.")


main()
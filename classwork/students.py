
from dataclasses import dataclass

@dataclass
class Student:
    name: str
    age: int
    grade: int


def info(student: Student):
    print(f"{student.name}, {student.age} лет, {student.grade} класс")


student1 = Student("Иван", 14, 3)
student2 = Student("Мария", 13, 7)

info(student1)
info(student2)

try:
    who = int(input("чей класс повысить? (1 - Иван, 2 - Мария, 0 - оба) "))
    if who in (0, 1, 2):
        step = int(input("На сколько повысить класс? "))
        if who == 1:
            student1.grade += step
            print("После повышения:")
            info(student1)
        elif who == 2:
            student2.grade += step
            print("После повышения:")
            info(student2)
        else:  
            student1.grade += step
            student2.grade += step
            print("После повышения:")
            info(student1)
            info(student2)
    else:
        print("Неверный выбор")
except:
    print("Некорректный ввод")
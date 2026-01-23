file = open("hi.txt", 'r', encoding="utf-8")
first_line = file.readline()
file.close()
if len(first_line) >= 5:
    print(first_line[4])
else:
    print("Первая строка короче 5 символов")
#------------------------------------------
file = open("hi.txt", 'r', encoding="utf-8")
first_line = file.readline()
file.close()

kolvo = first_line[:10]
if kolvo:
    print(kolvo)
else:
    print("Файл пустой или первая строка отсутствует")
#------------------------------------------
file = open("hi.txt", 'r', encoding="utf-8")
file.readline()
second_line = file.readline()
file.close()

if second_line:
    print(second_line[0])
else:
    print("В файле меньше двух строк или вторая строка пуста")


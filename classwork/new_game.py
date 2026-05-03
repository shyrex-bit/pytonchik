count_students = int(input("введите кол-во студентов, которые пришли на пересдачу: "))

sum_marks=0
current_mark=0
avg_mark=0

for  _ in range(count_students):
    current_mark=int(input("введите оценку студентика"))
    sum_marks=sum_marks+current_mark

avg_mark=sum_marks/count_students

print(f"среняя оценка: {avg_mark:.2f}")

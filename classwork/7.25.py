
sum_chisel=0
current_chisel=0
avg_chisel=0

count_chisel=int(input("введите кол-во оценок "))


for _ in range(count_chisel):
    current_chisel=int(input("введите оценочку "))
    if current_chisel>5:
        print("не такой оценки,но я посчитаю")
    sum_chisel=sum_chisel+current_chisel
avg_chisel=sum_chisel/count_chisel

print(avg_chisel)

days=int(input("введите кол-во дней "))
count=0

for _ in range(days):
    temp=int(input("введите температуру "))
    if temp<=0:
        count=count+1
        
print(f"в месяце температура 0 или меньше была {count} раз")
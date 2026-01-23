import random

my_collection = []

count_elements = 10

for _ in range(count_elements):
    my_collection.append(random.randint(1, 100))

for i in range(count_elements):  
    print(f"{i}: {my_collection[i]}")

my_collection[0] = 999

print(my_collection)

print(my_collection[1])

my_collection.pop(1)

my_collection.insert(1,777)

print(my_collection)
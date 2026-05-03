import random

is_run = True

while is_run == True:
    print("hello")

    if random.randint(1, 1000 + 1) < 500:
        is_run = False

#отдельно стоп

import random

is_stop = False

while not is_stop:
    print("hello")

    if random.randint(1, 1000 + 1) < 500:
        is_stop = True
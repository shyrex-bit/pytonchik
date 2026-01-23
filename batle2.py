import random

ALIVE_SHIP = "K"
DEAD_SHIP = "X"
MISS_CELL = "O"
EMPTY_CELL = "."

COLS = 10
ROWS = 10

COUNT_SHIPS = 10

USER_STEP = "USER"
COMP_STEP = "COMP"

USER_WINNER = "USER"
COMP_WINNER = "COMP"


user_field = []
comp_field = []

def user_deck(user_field):
    for i in range(ROWS):
        user_field.append([])
        for j in range(COLS):
            user_field[i].append(EMPTY_CELL)
    
    return user_field

def comp_deck(comp_field):
    for i in range(ROWS):
        comp_field.append([])
        for j in range(COLS):
            comp_field[i].append(EMPTY_CELL)
    
    return comp_field

def random_user_field(user_field):
    for _ in range(COUNT_SHIPS):
        continue_random = True
        i_rand = 0
        j_rand = 0
        while continue_random == True:
            i_rand = random.randint(0, ROWS - 1)
            j_rand = random.randint(0, COLS - 1)
            
            if user_field[i_rand][j_rand] == EMPTY_CELL:
                continue_random = False

    user_field[i_rand][j_rand] = ALIVE_SHIP

    return user_field

def random_comp_field(comp_field):
    for _ in range(COUNT_SHIPS):
        continue_random = True
        i_rand = 0
        j_rand = 0
        while continue_random == True:
            i_rand = random.randint(0, ROWS - 1)
            j_rand = random.randint(0, COLS - 1)
            if comp_field[i_rand][j_rand] == EMPTY_CELL:
                continue_random = False

    comp_field[i_rand][j_rand] = ALIVE_SHIP

    return comp_field

current_step = ""
if random.randint(1, 1000) < 500:
    current_step = USER_STEP
else:
    current_step = COMP_STEP

game_is_running = True

user_alive_ships = COUNT_SHIPS
comp_alive_ships = COUNT_SHIPS

winner = ""

#------------------------------------------------------

while game_is_running == True:
    def fill_user(user_field):
        print("Поле человека: ")
        for i in range(ROWS):
            for j in range(COLS):
                print(user_field[i][j], end="")
        print()

       
    def fill_comp(comp_field):
        print("Поле компьютера: ")
        for i in range(ROWS):
            for j in range(COLS):
                if comp_field[i][j] == ALIVE_SHIP:
                    print(EMPTY_CELL, end="")
                else:
                    print(comp_field[i][j], end="")
        print()

    def usr_stp(current_step,USER_STEP,):

        if current_step == USER_STEP:
            print("Ход человека:")
            i_input = int(input("введите номер строки: ")) - 1
            j_input = int(input("введите номер столбца: ")) - 1
            
    def comp_aliv_ship(comp_field,comp_alive_ships):
            if comp_field[i_input][j_input] == ALIVE_SHIP:
                comp_field[i_input][j_input] = DEAD_SHIP
                comp_alive_ships -= 1
                
                if comp_alive_ships == 0:
                    game_is_running = False
                    winner = USER_WINNER

            elif comp_field[i_input][j_input] == EMPTY_CELL:
                comp_field[i_input][j_input] = MISS_CELL
                current_step = COMP_STEP
            
            elif current_step == COMP_STEP:
                print("Ход компьютера (нажмите Enter):")
                
            input()

            i_input = random.randint(0, ROWS - 1)
            j_input = random.randint(0, COLS - 1)
            
            if user_field[i_input][j_input] == ALIVE_SHIP:
                user_field[i_input][j_input] = DEAD_SHIP
                user_alive_ships -= 0
                
                if user_alive_ships == 0:
                    game_is_running = False
                    winner = COMP_WINNER
                
                elif user_field[i_input][j_input] == EMPTY_CELL:
                    user_field[i_input][j_input] = MISS_CELL
                    current_step = USER_STEP
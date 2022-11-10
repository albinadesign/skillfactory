# krestiki-noliki

# define the list of cells:
cells_list = list(range(1, 10))

# draw the board:
def draw_board():
    print("____________________")
    print("| ", cells_list[0], " | ", cells_list[1], " | ", cells_list[2], " |", "\n"
          "____________________", "\n"                                                                      
          "| ", cells_list[3], " | ", cells_list[4], " | ", cells_list[5], " |", "\n"
          "____________________", "\n"                                                                        
          "| ", cells_list[6], " | ", cells_list[7], " | ", cells_list[8], " |"
          )
    print("--------------------")

# function for input:
def function_for_input(x_or_o):
    # input number of the cell, pointing the due player in the request
    while True:
        players_choice = input('В какую клетку поставить ' + x_or_o +'? ')
        # check if input is a number
        if players_choice not in '123456789':
            print("Введите номер клетки в диапазоне от 1 до 9 ")
            continue
        # check if number is within 1-9
        if int(players_choice) < 1 or int(players_choice) > 9:
            print('Выберите номер клетки от 1 до 9')
            continue
        # check if the cell is not taken
        if cells_list[int(players_choice) - 1] == "Х" or cells_list[int(players_choice) - 1] == "О":
             print('Клетка уже занята. Выберите другую.')
             continue
        # if everything is ok redefine the cell as x or o
        cells_list[int(players_choice) - 1] = x_or_o
        break

# function for defining the winner:
def define_the_winner():
    # define winning combinations:
    winning_combinations = [(1, 2, 3), (4, 5, 6), (7, 8, 9), (1, 4, 7), (2, 5, 8), (3, 6, 9), (7, 5, 3), (1, 5, 9)]
     # check if combinations of the cells in cells_list are equal to the winning combinations
    for cells in winning_combinations:
        if (cells_list[cells[0]-1]) == (cells_list[cells[1]-1]) == (cells_list[cells[2]-1]):
            return cells_list[cells[0] - 1]
    else:
        return False

# the play
def the_play():
    # counter of moves
    counter = 0
    while True:
        draw_board()
        # define the player - x or y (even or odd number of move) and start function_for_input (x or y)
        if counter % 2 == 0:
            function_for_input("Х")
        else:
            function_for_input("О")
        counter += 1
        # start function for defining the winner, if this function is True print" x, or y, you are the winner" and break
        if counter > 4:
            winner = define_the_winner()
            if winner:
                draw_board()
                print('Выиграл', winner, ". Поздравляем!")
                break
        # define no more than 9 moves(or more properly 8), if all moves are made print there is no winner and break
        if counter == 8:
            draw_board()
            print("Ничья")
            break

the_play()


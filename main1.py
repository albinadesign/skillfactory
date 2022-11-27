import pygame as pg
import random
import copy

# set the colors for the project in pygame
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# set the main sizes so they can be changed easily
square_size = 30
left_border = 70
upper_border = 60
# calculate the size of the playing screen
size = (left_border + 30 * square_size, upper_border + 15 * square_size)
LETTERS = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J']
# switch on pygame
pg.init()
# set the size of the playing screen
screen = pg.display.set_mode(size)
pg.display.set_caption("Морской бой")
# calculating the font size in dependence to the size of squares
font_size = int(square_size / 1.5)
# set the font
font = pg.font.SysFont('areal', font_size)
# set other global sets and list to store the data of the game
computer_free_to_fire_coordinates = {(x, y) for x in range(16, 25) for y in range(1, 11)}
set_of_squares_around_last_hit = set()
hit_squares = set()
missed_dotted_squares = set()
squares_computer_cannot_shoot = set()
hit_by_computer_squares = set()
last_hits = []
list_of_destroyed_ships = []


class Field:
    """create players' board,
    add numbers and letters to define squares,
    puts names of players over the boards
    """
    def __init__(self, title, offset):
        self.title = title
        self.offset = offset
        self.draw_boards()
        self.add_numbers_and_letters_to_field()
        self.sign_field()

    def draw_boards(self):
        """Draws two grids for both players
        """
        for i in range(11):
            # Horizontal lines
            pg.draw.line(screen, BLACK, (left_border + self.offset * square_size, upper_border + i * square_size),
                             (left_border + (10 + self.offset) * square_size, upper_border + i * square_size), 1)
            # Vertical lines
            pg.draw.line(screen, BLACK, (left_border + (i + self.offset) * square_size, upper_border),
                             (left_border + (i + self.offset) * square_size, upper_border + 10 * square_size), 1)

    def add_numbers_and_letters_to_field(self):
         for i in range(10):
            numbers = font.render(str(i + 1), True, BLACK)
            letters = font.render(LETTERS[i], True, BLACK)
            numbers_width = numbers.get_width()
            numbers_height = numbers.get_height()
            letters_width = letters.get_width()

            # draw numbers vertically
            screen.blit(numbers, (left_border - (square_size // 2 + numbers_width // 2) + self.offset * square_size,
                                  upper_border + i * square_size + (square_size // 2 - numbers_height // 2)))
            # draw letters horizontally
            screen.blit(letters, (left_border + i * square_size + (square_size //
                                                                   2 - letters_width // 2) + self.offset * square_size,
                                  upper_border + 10 * square_size))

    def sign_field(self):
        # put the signs of the players to the screen. The names can be easily changed any moment
        player = font.render(self.title, True, BLACK)
        sign_width = player.get_width()
        screen.blit(player, (left_border + 5 * square_size - sign_width //
                             2 + self.offset * square_size, upper_border - square_size // 2 - font_size +20))


class Ships:
    """create the coordinates of all ships,
    first create start square of the ship,
    then choose the direction,
    check if the ship is constructed within boards,
    check if the ship is correct
    """
    def __init__(self, offset):
        self.offset = offset
        self.free_squares_to_draw_a_ship = {(x, y) for x in range(1 + self.offset, 11 + self.offset) for y in range(1, 11)}
        self.ships_set = set()
        self.ships = self.set_of_ships_on_board()

    def create_first_square(self, free_squares_to_draw_a_ship):
        # after randomly  choosing the first square to construct a ship,
        # choose the direction of ship construction - up or down, forward or reverse
        horiz_or_vert_ship = random.randint(0, 1)
        forw_or_backw_ship = random.choice((-1, 1))
        x, y = random.choice(tuple(free_squares_to_draw_a_ship))
        return x, y, horiz_or_vert_ship, forw_or_backw_ship

    def create_ship(self, number_of_squares, free_squares_to_draw_a_ship):
        # create list to store new ships' coordinates
        new_ship_coordinates = []
        # take the data from the previous function
        x, y, horiz_or_vert_ship, forw_or_backw_ship = self.create_first_square(free_squares_to_draw_a_ship)
        # construct the ship using the next function
        for _ in range(number_of_squares):
            new_ship_coordinates.append((x, y))
            if not horiz_or_vert_ship:
                forw_or_backw_ship, x = self.get_new_block_for_ship(
                    x, forw_or_backw_ship, horiz_or_vert_ship, new_ship_coordinates)
            else:
                forw_or_backw_ship, y = self.get_new_block_for_ship(
                    y, forw_or_backw_ship, horiz_or_vert_ship, new_ship_coordinates)
        # check the newly constructed ship using special function below
        if self.is_ship_valid(new_ship_coordinates):
            return new_ship_coordinates
        return self.create_ship(number_of_squares, free_squares_to_draw_a_ship)

    # the function that checks the ships to be constructed within playing boards
    def get_new_block_for_ship(self, coordinates, forw_or_backw_ship, horiz_or_vert_ship, new_ship_coordinates):
        if (coordinates <= 1 - self.offset * (horiz_or_vert_ship - 1) and forw_or_backw_ship == -1) or (
                coordinates >= 10 - self.offset * (horiz_or_vert_ship - 1) and forw_or_backw_ship == 1):
            forw_or_backw_ship *= -1
            return forw_or_backw_ship, new_ship_coordinates[0][horiz_or_vert_ship] + forw_or_backw_ship
        else:
            return forw_or_backw_ship, new_ship_coordinates[-1][horiz_or_vert_ship] + forw_or_backw_ship

    # the function that checks the ship is constructed properly
    def is_ship_valid(self, new_ship):
        ship = set(new_ship)
        # check the ship is constructed using free set of proper coordinates
        return ship.issubset(self.free_squares_to_draw_a_ship)

    # add the newly constructed ship to the set of ships
    def add_new_ship_to_set(self, new_ship):
        self.ships_set.update(new_ship)

    # update the set of free squares to subtract from them the newly constructed ship
    def free_squares_to_draw_a_ship_update(self, new_ship):
        for i in new_ship:
            for x in range(-1, 2):
                for y in range(-1, 2):
                    if 0 + self.offset < (i[0] + x) < 11 + self.offset and 0 < (i[1] + y) < 11:
                        self.free_squares_to_draw_a_ship.discard((i[0] + x, i[1] + y))

    # the quantity of the ship of the certain lenght deneds on their length:
    # 4-squared ship - 1, 3-squared ships - 2, etc
    # here we use this formula to construct the certain set of ships in needed quantities
    def set_of_ships_on_board(self):
        ships_coordinates_list = []
        for ship_length in range(4, 0, -1):
            for _ in range(5 - ship_length):
                new_ship = self.create_ship(
                    ship_length, self.free_squares_to_draw_a_ship)
                # update all the sets
                ships_coordinates_list.append(new_ship)
                self.add_new_ship_to_set(new_ship)
                self.free_squares_to_draw_a_ship_update(new_ship)
        return ships_coordinates_list


# logic of the game

def computer_shoots(set_to_shoot_from):
    # set some time between computer shoots, so we could see them
    pg.time.delay(800)
    # enable computer to choose the squares to shoot randomly from the set of available coordinates
    squares_shot_by_computer = random.choice(tuple(set_to_shoot_from))
    # subtract the shot squares from the set to make sure the computer doesn't shoot twice the same square
    computer_free_to_fire_coordinates.discard(squares_shot_by_computer)
    return squares_shot_by_computer


def check_successful_hit(fired_square, enemy_ships_list, computer_turn, enemy_ships_list_copy,
                         enemy_ships_set):
    ''' check if the shoot is successful,
    update all the necessary set (the dots around or by diagonal of the hit target
    '''
    for elem in enemy_ships_list:
        diagonal = True
        if fired_square in elem:
            ind = enemy_ships_list.index(elem)
            if len(elem) == 1:
                diagonal = False
            update_dotted_and_hit_sets(fired_square, computer_turn, diagonal)
            elem.remove(fired_square)
            enemy_ships_set.discard(fired_square)
            if computer_turn:
                last_hits.append(fired_square)
                update_around_last_computer_hit(fired_square)
            if not elem:
                update_destroyed_ships(ind, computer_turn, enemy_ships_list_copy)
                if computer_turn:
                    last_hits.clear()
                    set_of_squares_around_last_hit.clear()
                else:
                    list_of_destroyed_ships.append(computer.ships[ind])
            return True
    add_missed_block_to_dotted_set(fired_square)
    if computer_turn:
        # this set is for computer to shoot further to the once hit ship to sink it all
        update_around_last_computer_hit(fired_square, False)
    return False


def update_destroyed_ships(ind, computer_turn, enemy_ships_list_copy):
    ''' function to put dots if the ship is not shot and X if it is
    '''
    ship = sorted(enemy_ships_list_copy[ind])
    for i in range(-1, 1):
        update_dotted_and_hit_sets(ship[i], computer_turn, False)


def update_around_last_computer_hit(fired_squares, computer_hits=True):
    ''' the function for computer to sink quickly the shot ship,
    update the set of coordinates around the hit point for further use
    as the next targets'''
    global set_of_squares_around_last_hit, computer_free_to_fire_coordinates
    if computer_hits and fired_squares in set_of_squares_around_last_hit:
        set_of_squares_around_last_hit = computer_hits_twice()
    elif computer_hits and fired_squares not in set_of_squares_around_last_hit:
        computer_first_hit(fired_squares)
    elif not computer_hits:
        set_of_squares_around_last_hit.discard(fired_squares)

    # update the sets
    set_of_squares_around_last_hit -= squares_computer_cannot_shoot
    set_of_squares_around_last_hit -= hit_by_computer_squares
    computer_free_to_fire_coordinates -= set_of_squares_around_last_hit
    computer_free_to_fire_coordinates -= squares_computer_cannot_shoot


def computer_first_hit(fired_square):
    ''' the function to store the coordinates of the shot target to use
    them further to shoot around'''
    xhit, yhit = fired_square
    if xhit > 16:
        set_of_squares_around_last_hit.add((xhit - 1, yhit))
    if xhit < 25:
        set_of_squares_around_last_hit.add((xhit + 1, yhit))
    if yhit > 1:
        set_of_squares_around_last_hit.add((xhit, yhit - 1))
    if yhit < 10:
        set_of_squares_around_last_hit.add((xhit, yhit + 1))


def computer_hits_twice():
    ''' when there are more than one shot squares,
    the function adds the squares around those squares to the new set
    to shoot further in order to sink the ship faster'''
    last_hits.sort()
    new_around_last_hit_set = set()
    for i in range(len(last_hits) - 1):
        x1 = last_hits[i][0]
        x2 = last_hits[i + 1][0]
        y1 = last_hits[i][1]
        y2 = last_hits[i + 1][1]
        if x1 == x2:
            if y1 > 1:
                new_around_last_hit_set.add((x1, y1 - 1))
            if y2 < 10:
                new_around_last_hit_set.add((x1, y2 + 1))
        elif y1 == y2:
            if x1 > 16:
                new_around_last_hit_set.add((x1 - 1, y1))
            if x2 < 25:
                new_around_last_hit_set.add((x2 + 1, y1))
    return new_around_last_hit_set


def update_dotted_and_hit_sets(fired_square, computer_turn, diagonal=True):
    ''' the function to put dots to the missed squares and to the squares
    around and by diagonal to the hit targets'''
    global missed_dotted_squares
    x, y = fired_square
    a, b = 0, 11
    if computer_turn:
        # plus 15 to let computer operate on the human's board
        a += 15
        b += 15
        # add a square shot by computer to the set
        hit_by_computer_squares.add(fired_square)
    # add shot squares on playing boards
    hit_squares.add(fired_square)
    # add squares to the diagonal or around hit square to their own sets
    for i in range(-1, 2):
        for j in range(-1, 2):
            if diagonal:
                if i != 0 and j != 0 and a < x + i < b and 0 < y + j < 11:
                    missed_dotted_squares.add((x + i, y + j))
                    if computer_turn:
                        squares_computer_cannot_shoot.add((x + i, y + j))
            else:
                if a < x + i < b and 0 < y + j < 11:
                    missed_dotted_squares.add((x + i, y + j))
                    if computer_turn:
                        squares_computer_cannot_shoot.add((x + i, y + j))
    missed_dotted_squares -= hit_squares


def add_missed_block_to_dotted_set(fired_square):
    """ remove all missed shots and squares around the hit
    targets from the set of possible targets for the computer
    and add then to the set of missed or dotted squares
    """
    missed_dotted_squares.add(fired_square)
    squares_computer_cannot_shoot.add(fired_square)


# draw the game

def draw_ships(ships_coordinates_list):
    """ the function to draw the ships on the boards using
    the ship coordinates list made previously
    """
    for elem in ships_coordinates_list:
        ship = sorted(elem)
        x_start = ship[0][0]
        y_start = ship[0][1]
        # draw horizontal and 1-square ships
        ship_width = square_size * len(ship)
        ship_height = square_size
        # draw vertical ships. The size of the ships depends on the size
        # of the squares, so it can be easily changed any time
        if len(ship) > 1 and ship[0][0] == ship[1][0]:
            ship_width, ship_height = ship_height, ship_width
        x = square_size * (x_start - 1) + left_border
        y = square_size * (y_start - 1) + upper_border
        pg.draw.rect(
            screen, BLACK, ((x, y), (ship_width, ship_height)), width=square_size // 10)


def draw_from_dotted_set(dotted_set):
    """ the function to draw dots in the centers
    of the squares at pygame screen, the size of dots
    depends on the size of squares to change it quickly if needed
    """
    for elem in dotted_set:
        pg.draw.circle(screen, BLACK, (square_size * (
                elem[0] - 0.5) + left_border, square_size * (elem[1] - 0.5) + upper_border), square_size // 6)


def draw_hit_blocks(hit_blocks):
     ''' the function to draw X on playing boards at pygame screen
     '''
     for block in hit_blocks:
        x1 = square_size * (block[0] - 1) + left_border
        y1 = square_size * (block[1] - 1) + upper_border
        pg.draw.line(screen, BLACK, (x1, y1),
                         (x1 + square_size, y1 + square_size), square_size // 6)
        pg.draw.line(screen, BLACK, (x1, y1 + square_size),
                         (x1 + square_size, y1), square_size // 6)


computer = Ships(0)
human = Ships(15)
computer_ships_in_play = copy.deepcopy(computer.ships)
human_ships_in_play = copy.deepcopy(human.ships)


def main():
    game_over = False
    computer_turn = False

    screen.fill(WHITE)
    computer_grid = Field("Море компьютера", 0)
    human_grid = Field("Твое море", 15)

    draw_ships(human.ships)
    pg.display.update()

    while not game_over:
        for event in pg.event.get():
            if event.type == pg.QUIT:
                game_over = True
            elif not computer_turn and event.type == pg.MOUSEBUTTONDOWN:
                x, y = event.pos
                # There should be stict '<' and not <=! Oterwise we will shoot at grid's lines
                # and the dot will be put outside of the grid!
                if (left_border < x < left_border + 10 * square_size) and (
                        upper_border < y < upper_border + 10 * square_size):
                    fired_block = ((x - left_border) // square_size + 1,
                                   (y - upper_border) // square_size + 1)
                    computer_turn = not check_successful_hit(fired_block, computer_ships_in_play, False, computer.ships,
                                                             computer.ships_set)

        if computer_turn:
            set_to_shoot_from = computer_free_to_fire_coordinates
            if set_of_squares_around_last_hit:
                set_to_shoot_from = set_of_squares_around_last_hit
            fired_block = computer_shoots(set_to_shoot_from)
            computer_turn = check_successful_hit(fired_block, human_ships_in_play, True, human.ships, human.ships_set)

        draw_from_dotted_set(missed_dotted_squares)
        draw_hit_blocks(hit_squares)
        draw_ships(list_of_destroyed_ships)
        pg.display.update()


main()
pg.quit()


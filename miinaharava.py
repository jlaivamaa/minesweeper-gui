import random
import time
import haravasto

def make_grid(width, height):
    #Creates the minefield by taking the width and height coordinates
    field = []
    for row in range(width):
        field.append([])
        for column in range(height):
            field[-1].append(" ")
    return field


def plant_mines(mine_amount, grid):
    #Creates amount of mines designated by the player inside the minefield in random locations and saves them in a list of tuples
    list_of_mines = []
    unmined = []
    for x in range(len(grid)):
        for y in range(len(grid[0])):
            unmined.append((x, y))

    while mine_amount > 0:
        x = random.randrange(len(grid))
        y = random.randrange(len(grid[0]))
        mines = (x, y)
        if mines in unmined:
                unmined.remove(mines)
                list_of_mines.append(mines)
                mine_amount -= 1
    return list_of_mines


def draw_field():
    #Handler -function, which draws the 2d list minefield to the screen. Function is called every time the game asks to refresh the screen
    haravasto.tyhjaa_ikkuna()
    haravasto.piirra_tausta()
    haravasto.aloita_ruutujen_piirto()
    for row_index, row in enumerate(grid):
        for col_index, col in enumerate(row):
            haravasto.lisaa_piirrettava_ruutu(col, row_index * 40, col_index * 40)
    haravasto.piirra_ruudut()

def mouse_handler(x, y, nappi, muokkausnapit):
    #Mouse-handler, which takes the left mouse button input and calls functions that check whether the coordinates contain a mine
    win_flag = False
    lose_flag = False
    cx = x//40
    cy = y//40
    if nappi == 1:
        if (cx, cy) in mines:
            grid[cx][cy] = "x"
            lose_flag = True
            print("You lost")
        else:
            floodfill(grid, cx, cy, mines)
            draw_field()
            win_flag = winstate(grid, cx, cy, mines)
            if win_flag == True:
                print("You won")
    if win_flag or lose_flag is True:
        end_time = time.time() - start_time
        reveal_mines(grid, mines)
        draw_field()
        record_statistics(date, end_time, win_flag, mine_amount)

def record_statistics(date, end_time, win_flag, mine_amount):
    #Creates or adds the statistics of the completed game to a text file
    with open("statistics.txt", "a+") as f:
        f.write("DATE: " + date + "\n")
        f.write("ELAPSED TIME: {:.2f} seconds".format(end_time) + "\n")
        f.write("VICTORY: " + str(win_flag) + "\n")
        f.write("MINES: " + str(mine_amount) + "\n\n")
        f.close()


def show_statistics():
    #Opens the statistics and shows previous games results
    with open("statistics.txt", "r") as q:
        stats = q.read()
        print(stats)
        q.close()

def floodfill(grid, x, y, mines):
    #Floodfill -algorithm, which goes through the neighbors of the given coordinates, 
    #opens the empty neighbors and stops when it borders a mine
    if(x < 0 or y < 0 or x > len(grid) or y > len(grid[0])):
        return

    if (x, y) in mines:
        return

    if grid[x][y] == " ":
        count = get_neighbors(grid, x, y, mines)

        grid[x][y] = "{}".format(count)
        if count == 0:
            grid[x][y] = "0"
            if x > 0:
                floodfill(grid, x - 1, y, mines)
            if x < len(grid) - 1:
                floodfill(grid, x + 1, y, mines)
            if y > 0:
                floodfill(grid, x, y - 1, mines)
            if y < len(grid[0]) - 1:
                floodfill(grid, x, y + 1, mines)
            if x > 0 and y > 0:
                floodfill(grid, x - 1, y - 1, mines)
            if x < len(grid) - 1 and y < len(grid[0]) - 1:
                floodfill(grid, x + 1, y + 1, mines)
            if x < len(grid) - 1 and y > 0:
                floodfill(grid, x + 1, y - 1, mines)
            if x > 0 and y < len(grid[0]) - 1:
                floodfill(grid, x - 1, y + 1, mines)
    return grid

def get_neighbors(grid, x, y, mines):
    #Goes through given coordinates neighbors, checks whether they contain any mines and returns the amount of mines found
    neighbor_mine_count = 0
    for i in range(max(0, x - 1), min(len(grid), x + 2)):
        for j in range(max(0, y - 1), min(len(grid[0]), y + 2)):
            if(i != x or j != y):
                for mine in mines:
                    if mine == (i, j):
                        neighbor_mine_count += 1
    return neighbor_mine_count

def reveal_mines(grid, mines):
    #Reveals the leftover mines after the game has ended
    for mine in mines:
        x, y = mine
        grid[x][y] = "x"

def winstate(grid, x, y, mines):
    #Checks whether the player has won the game by comparing the unrevealed cells to the list of mines
    unrevealed = 0
    for row in grid:
        for tile in row:
            if tile == " ":
                unrevealed += 1
    if unrevealed == len(mines):
        return True
    return False

def main():
    """"""
    haravasto.lataa_kuvat("spritet")
    haravasto.luo_ikkuna(len(grid) * 40, len(grid[0]) * 40)
    haravasto.aseta_piirto_kasittelija(draw_field)
    haravasto.aseta_hiiri_kasittelija(mouse_handler)
    haravasto.aloita()

if __name__=="__main__":
    #Main -function, which acts as a menu where the player can check the 
    #statistics of previous games, start a new game or exit the program
    user_input = ""
    max_space = 0
    mine_amount = 0
    unmined_amount = 0
    while user_input != "n":
        user_input = input("y - Play minesweeper \nn - Quit \ns - Show statistics \n")
        if user_input == "y":
            try:
                user_input = input("\nInput the dimensions of the field in the format x,y: ")
                user_input = user_input.split(",")
                width, height = int(user_input[0]), int(user_input[1])
                if width <= 0 or height <= 0:
                    print("\nThe dimensions are too small\n")
                    continue
                max_space = width * height
            except ValueError:
                print("\nThe dimensions must be integers and seperated by a comma\n")
                continue
            except IndexError:
                print("\nThe dimensions must be integers and seperated by a comma\n")
                continue
            try:
                mine_amount = int(input("Input the amount of mines in the field (Available space: {}): ".format(max_space)))
                unmined_amount = max_space - mine_amount
                if mine_amount < 0:
                    print("\nInteger must be positive\n")
                    continue
                elif mine_amount > max_space:
                    print("\nToo many mines to fit the dimensions of the field\n")
                    continue
            except ValueError:
                print("\nAmount of mines must be an integer\n")
                continue

            grid = make_grid(width, height)
            mines = plant_mines(mine_amount, grid)
            date = time.strftime("%d/%m/%Y %H:%M:%S")
            start_time = time.time()
            main()

        elif user_input == "s":
            try:
                show_statistics()
            except FileNotFoundError:
                print("\nFile containing the statistics doesn't exist!\n")

        elif user_input != "n":
            print("\nIncorrect input!\n")

# SudokuSolver

import pygame

pygame.init()

# Setup
WIDTH = HEIGHT = 540
GRIDSIZE = int(WIDTH/9)  
screen = pygame.display.set_mode((WIDTH+300,HEIGHT))
picture = pygame.image.load('images/chalkboard.jpg')
background = pygame.transform.scale(picture, (WIDTH+300, HEIGHT))
font = pygame.font.Font('font/FreeSansBold.ttf', 60)
font2 = pygame.font.Font('font/FreeSansBold.ttf', 24)

pygame.display.set_caption('SudokuSolver')

# Variables
WHITE = (255,255,255)
GREEN = (51,102,0)
RED = (255,0,0)
LGREY = (150,150,150)
DGREY = (50,50,50)
x = y = 0
change_x = 0
change_y = 0
start_sudoku =[ [0,0,0,5,6,2,0,0,0],
                [0,0,0,0,0,0,7,3,0],
                [4,1,9,0,0,0,6,0,0],
                [9,0,0,0,0,0,8,4,5],
                [8,0,0,1,0,9,0,0,6],
                [2,6,4,0,0,0,0,0,7],
                [0,0,5,0,0,0,2,6,9],
                [0,4,8,0,0,0,0,0,0],
                [0,0,0,3,7,6,0,0,0]]
edit_sudoku = [ [0,0,0,5,6,2,0,0,0],
                [0,0,0,0,0,0,7,3,0],
                [4,1,9,0,0,0,6,0,0],
                [9,0,0,0,0,0,8,4,5],
                [8,0,0,1,0,9,0,0,6],
                [2,6,4,0,0,0,0,0,7],
                [0,0,5,0,0,0,2,6,9],
                [0,4,8,0,0,0,0,0,0],
                [0,0,0,3,7,6,0,0,0]]
solved_sudoku = [ [0,0,0,5,6,2,0,0,0],
                [0,0,0,0,0,0,7,3,0],
                [4,1,9,0,0,0,6,0,0],
                [9,0,0,0,0,0,8,4,5],
                [8,0,0,1,0,9,0,0,6],
                [2,6,4,0,0,0,0,0,7],
                [0,0,5,0,0,0,2,6,9],
                [0,4,8,0,0,0,0,0,0],
                [0,0,0,3,7,6,0,0,0]]

# Functions
def draw_grid():
    for i in range (1,9):
        pygame.draw.line(screen,DGREY,(i*GRIDSIZE,0),(i*GRIDSIZE,WIDTH),2)
        pygame.draw.line(screen,DGREY,(0,i*GRIDSIZE),(HEIGHT,i*GRIDSIZE),2)
    for i in range(3,9,3):
        pygame.draw.line(screen,LGREY,(i*GRIDSIZE,0),(i*GRIDSIZE,WIDTH),2)
        pygame.draw.line(screen,LGREY,(0,i*GRIDSIZE),(HEIGHT,i*GRIDSIZE),2)
    pygame.draw.rect(screen,LGREY,pygame.Rect(0,0,WIDTH,HEIGHT),2)

def draw_box():
    global x,y
    if x > 480:
        x = 0
    elif x <0:
        x = 480    
    if y > 480:
        y = 0
    elif y < 0:
        y = 480
    pygame.draw.rect(screen,WHITE,pygame.Rect(x+2,y+2,GRIDSIZE-2,GRIDSIZE-2),2)

def update_pos(x1,y1):
    global x,y
    x += x1
    y += y1

def update_sudoku(number):
    row = int(y/GRIDSIZE)
    col = int(x/GRIDSIZE)
    edit_sudoku[row][col] = number
    solved_sudoku[row][col] = number

def draw_sudoku(sudoku):
    for row in range(9):
        for col in range(9):
            x = int(col*GRIDSIZE)+12
            y = int(row*GRIDSIZE)-6
            if sudoku[row][col] == 0:
                nr = ""
            else:
                nr = str(sudoku[row][col])       
            screen.blit(font.render(nr, True, GREEN), (x,y))
            if edit_sudoku[row][col] != 0:
                screen.blit(font.render(str(edit_sudoku[row][col]), True, LGREY), (x,y))

def Reset(start_sudoku):
    for row in range(9):
        for col in range(9):
            edit_sudoku[row][col] = start_sudoku[row][col]
            solved_sudoku[row][col] = start_sudoku[row][col]
             

def Check(grid, row, col, num):
    for x in range(9):
        if grid[row][x] == num:
            return False
             
    for x in range(9):
        if grid[x][col] == num:
            return False
 
    startRow = row - row % 3
    startCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if grid[i + startRow][j + startCol] == num:
                return False
    return True
 
def Solve(grid, row, col):
 
    if (row == 8 and col == 9):
        return True
    if col == 9:
        row += 1
        col = 0
    if grid[row][col] > 0:
        return Solve(grid, row, col + 1)
    for num in range(1, 10, 1):    
        if Check(grid, row, col, num):
            grid[row][col] = num
            if Solve(grid, row, col + 1):
                return True
        grid[row][col] = 0
    return False

def Clear():
    for row in range(9):
        for col in range(9):
            edit_sudoku[row][col] = 0
            solved_sudoku[row][col] = 0 

def Write():
    for row in range(9):
        for col in range(9):
            start_sudoku[row][col] = edit_sudoku[row][col]
    
def Text():
    INTERLINIE = 30
    screen.blit(font2.render("Sudoku Solver 2022", True, WHITE), (550,25))
    screen.blit(font2.render("E = Edit", True, WHITE), (550,100))
    screen.blit(font2.render("S = Solve", True, WHITE), (550,100+INTERLINIE*1))
    screen.blit(font2.render("R = Reload from Memory", True, WHITE), (550,100+INTERLINIE*2))
    screen.blit(font2.render("W = Write to Memory ", True, WHITE), (550,100+INTERLINIE*3))
    screen.blit(font2.render("C = Clear Grid", True, WHITE), (550,100+INTERLINIE*4))

# ===============================================================================================
def main():
    # flags
    key_pressed = 0
    key_number = 10
    sudoku_edit = 0
    sudoku_solve = 0
    clear_sudoku = 0
    reload_sudoku = 0
    write_sudoku = 0

    # Run until quit
    running = True
    clock = pygame.time.Clock()

    while running:

        for event in pygame.event.get():

            if event.type == pygame.QUIT:
                running = False

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_DOWN:
                   change_y = GRIDSIZE
                   change_x = 0
                   key_pressed = 1
                elif event.key == pygame.K_UP:
                    change_y = -GRIDSIZE
                    change_x = 0
                    key_pressed = 1
                elif event.key == pygame.K_RIGHT:
                    change_x = GRIDSIZE
                    change_y=0
                    key_pressed = 1
                elif event.key == pygame.K_LEFT:  
                    change_x = -GRIDSIZE
                    change_y =0
                    key_pressed = 1
                elif event.key == pygame.K_e:
                    sudoku_edit = 1
                elif event.key == pygame.K_s:
                    sudoku_solve = 1
                    sudoku_edit = 0
                elif event.key == pygame.K_c:
                    clear_sudoku = 1
                    sudoku_edit = 1
                elif event.key == pygame.K_r:
                    reload_sudoku = 1
                    sudoku_edit = 1
                elif event.key == pygame.K_w:
                     write_sudoku = 1
                elif (event.key == pygame.K_DELETE) and sudoku_edit == 1:
                    key_number = 0
                elif (event.key == pygame.K_1 or event.key == pygame.K_KP1) and sudoku_edit == 1:
                    key_number = 1
                elif (event.key == pygame.K_2 or event.key == pygame.K_KP2) and sudoku_edit == 1:
                    key_number = 2
                elif (event.key == pygame.K_3 or event.key == pygame.K_KP3) and sudoku_edit == 1:
                    key_number = 3
                elif (event.key == pygame.K_4 or event.key == pygame.K_KP4) and sudoku_edit == 1:
                    key_number = 4
                elif (event.key == pygame.K_5 or event.key == pygame.K_KP5) and sudoku_edit == 1:
                    key_number = 5
                elif (event.key == pygame.K_6 or event.key == pygame.K_KP6) and sudoku_edit == 1:
                    key_number = 6
                elif (event.key == pygame.K_7 or event.key == pygame.K_KP7) and sudoku_edit == 1:
                    key_number = 7
                elif (event.key == pygame.K_8 or event.key == pygame.K_KP8) and sudoku_edit == 1:
                    key_number = 8
                elif (event.key == pygame.K_9 or event.key == pygame.K_KP9) and sudoku_edit == 1:
                    key_number = 9

            elif event.type == pygame.KEYUP:
                if event.key in (pygame.K_DOWN, pygame.K_UP):
                    change_y =  0
                elif event.key in (pygame.K_LEFT, pygame.K_RIGHT):
                    change_x =  0

        if key_pressed == 1:
            update_pos(change_x,change_y)
            key_pressed =0

        if key_number < 10:
            update_sudoku(key_number)
            key_number = 10
        
        if sudoku_solve == 1:
            Solve(solved_sudoku,0,0)
            sudoku_solve = 0

        if write_sudoku == 1:
            Write()
            write_sudoku = 0

        if clear_sudoku == 1:
            Clear()
            clear_sudoku = 0
        
        if reload_sudoku == 1:
            Clear()
            Reset(start_sudoku)
            reload_sudoku = 0

        screen.blit(background,(0,0))
        draw_grid()
        if sudoku_solve == 0:
            draw_box()
        draw_sudoku(solved_sudoku)               

        Text()

        # Update the display
        pygame.display.update()
        clock.tick(50)
    # Done! Time to quit.
    pygame.quit()

# If the name of the file == main -> run main()
if __name__ == '__main__':
    main()
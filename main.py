from operator import truediv
import os
import sys
import time
import keyboard
import random

FPS = 30
SCREEN_WIDTH = 19
SCREEN_HEIGHT = 19
MAX_FOOD = 10


class Snake():
    def __init__(self, x_coord=0, y_coord=0, length=1, points=0) -> None:
        self.x = x_coord
        self.y = y_coord
        self.points = points
        self.len = length

    def draw_on_board(self, Board):
        if 0 <= self.x <= Board.width and 0 <= self.y <= Board.height:
            Board.board[self.x][self.y] = '@ '

    def clear_current_position(self, Board):
        Board.board[self.x][self.y] = '. '

    def move(self, Board, direction):
        if direction == 'right' and self.y < Board.width:
            self.clear_current_position(Board)
            self.y += 1
            self.draw_on_board(Board)
        if direction == 'left' and 0 < self.y:
            self.clear_current_position(Board)
            self.y -= 1
            self.draw_on_board(Board)
        if direction == 'up' and 0 < self.x:
            self.clear_current_position(Board)
            self.x -= 1
            self.draw_on_board(Board)
        if direction == 'down' and self.x < Board.height:
            self.clear_current_position(Board)
            self.x += 1
            self.draw_on_board(Board)



class Board():
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT) -> None:
        self.width = width
        self.height = height
        self.max_food = 10
        self.food = []
        self.board = [['. ' for k in range(self.width + 1)] for m in range(self.height + 1)]
    
    def spawn_food(self, x=0, y=0):
        while len(self.food) < 10:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.food.append((x, y))
            self.board[x][y] = 'X '

    def draw(self):
        to_draw = ''
        print('--' * (self.width+1), end='')
        for row in self.board:
            to_draw = to_draw + '\n'
            for cell in row:
                to_draw = to_draw + cell
        print(to_draw, end='')
        print('\n', end='')
        print('--' * (self.width+1))


def update(snake, board):
    board.spawn_food()
    if keyboard.is_pressed('right'):
        snake.move(board, 'right')
    if keyboard.is_pressed('left'):
        snake.move(board, 'left')
    if keyboard.is_pressed('up'):
        snake.move(board, 'up')
    if keyboard.is_pressed('down'):
        snake.move(board, 'down')
    if keyboard.is_pressed('q'):
        os.system('cls')
        sys.exit()




def clear_screen():
    print('')
    print('\033[' + str(SCREEN_HEIGHT + 4) + 'A\033[2K', end='')

def main():
    os.system('cls')
    os.system('mode con: cols=80 lines=40')
    snake = Snake()
    board = Board()


    while True:
        clear_screen()
        update(snake, board)
        board.draw()
        time.sleep(0.05)
                        
if __name__ == "__main__":
    main()

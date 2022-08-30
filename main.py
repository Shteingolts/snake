import os
import sys
import time
import keyboard
import random

FPS = 30
SNAKE_SPEED = 400
SCREEN_WIDTH = 20
SCREEN_HEIGHT = 20
MAX_FOOD = 10


class Snake():
    def __init__(self, x_coord=10, y_coord=10, direction='right', speed=SNAKE_SPEED, points=0) -> None:
        self.x = x_coord
        self.y = y_coord
        self.direction = direction
        self.speed = speed
        self.points = points
        self.body = []

    def draw_on_board(self, Board):
        if 0 <= self.x <= Board.width*100 and 0 <= self.y <= Board.height*100:
            Board.board[round(self.x / 100)][round(self.y / 100)] = '@ '
        for snake_part in self.body:
            Board.board[round(snake_part[0] / 100)
                        ][round(snake_part[1] / 100)] = '@ '

    def clear_tail(self, Board):
        if len(self.body) == 0:
            Board.board[round(self.x / 100)][round(self.y / 100)] = '. '
        else:
            Board.board[self.body[-1][0]][self.body[-1][1]] = '. '

    def move(self, Board, dt):
        y_max = Board.width * 100
        x_max = Board.height * 100

        if self.direction == 'right' and self.y < y_max:
            self.y = self.y + self.speed * dt
        if self.direction == 'left' and 0 < self.y:
            self.y = self.y - self.speed * dt
        if self.direction == 'up' and 0 < self.x:
            self.x = self.x - self.speed * dt
        if self.direction == 'down' and self.x < x_max:
            self.x = self.x + self.speed * dt

        if self.y > y_max:
            self.y = y_max
        if self.y < 0:
            self.y = 0
        if self.x > x_max:
            self.x = x_max
        if self.x < 0:
            self.x = 0


class Board():
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT) -> None:
        self.width = width
        self.height = height
        self.max_food = 10
        self.food = []
        self.board = [['. ' for k in range(self.width + 1)]
                      for m in range(self.height + 1)]

    def spawn_food(self):
        while len(self.food) < 10:
            x = random.randint(0, self.width)
            y = random.randint(0, self.height)
            self.food.append((x, y))
            self.board[x][y] = 'X '

    def draw(self, snake, dt):
        to_draw = ''
        to_draw = to_draw + '--' * (self.width+1)

        for row in self.board:
            to_draw = to_draw + '\n'
            for cell in row:
                to_draw = to_draw + cell

        to_draw = to_draw + '\n' + ('--' * (self.width+1)) + '\n'
        to_draw = to_draw + (f'Points: {snake.points}')
        print(to_draw)


def update(snake, board, dt):

    board.spawn_food()

    if keyboard.is_pressed('right'):
        snake.direction = 'right'
    if keyboard.is_pressed('left'):
        snake.direction = 'left'
    if keyboard.is_pressed('up'):
        snake.direction = 'up'
    if keyboard.is_pressed('down'):
        snake.direction = 'down'

    if (round(snake.x / 100), round(snake.y / 100)) in board.food:
        snake.points += 1
        board.food.remove((round(snake.x / 100), round(snake.y / 100)))

    snake.clear_tail(board)
    snake.move(board, dt)
    snake.draw_on_board(board)

    if keyboard.is_pressed('q'):
        os.system('cls')
        sys.exit()


def clear_screen():
    print('')
    print('\033[' + str(SCREEN_HEIGHT + 7) + 'A\033[2K', end='')


def main():
    os.system('cls')
    os.system('mode con: cols=80 lines=40')
    snake = Snake()
    board = Board()
    start_time = time.time()

    while True:
        dt = (time.time() - start_time)
        start_time = time.time()
        clear_screen()
        update(snake, board, dt)
        board.draw(snake, dt)


if __name__ == "__main__":
    main()

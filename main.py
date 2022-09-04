import os
import sys
import time
import random
import keyboard
import copy

FPS = 30
SNAKE_SPEED = 3
SCREEN_WIDTH = 20
SCREEN_HEIGHT = 20
MAX_FOOD = 10

class Snake():
    def __init__(
                self,
                direction='right',
                speed=SNAKE_SPEED,
                points=0) -> None:
        self.direction = direction
        self.speed = speed
        self.points = points
        self.draw_state = [[10, 10], [10, 9], [10, 8], [10, 7], [10, 6]]
        self.body = [[10, 10], [10, 9], [10, 8], [10, 7], [10, 6]]

    def draw_on_board(self, board):
        self.clear_snake(board)
        for snake_part in self.draw_state:
            board.board[round(snake_part[0])
                        ][round(snake_part[1])] = '@ '

    def clear_snake(self, board):
        for snake_part in self.draw_state:
            board.board[round(snake_part[0])][round(snake_part[1])] = '. '

    def update_direction(self):
        if keyboard.is_pressed('right'):
            self.direction = 'right'
        if keyboard.is_pressed('left'):
            self.direction = 'left'
        if keyboard.is_pressed('up'):
            self.direction = 'up'
        if keyboard.is_pressed('down'):
            self.direction = 'down'

    def move(self, board, dt):
        y_max = board.width
        x_max = board.height

        body_copy = copy.deepcopy(self.draw_state)
        previous_position = (body_copy[0][0], body_copy[0][1])

        if self.direction == 'right' and self.body[0][1] < y_max:
            self.body[0][1] = self.body[0][1] + self.speed * dt # [10.01, 10.01]
        if self.direction == 'left' and 0 < self.body[0][1]:
            self.body[0][1] = self.body[0][1] - self.speed * dt
        if self.direction == 'up' and 0 < self.body[0][0]:
            self.body[0][0] = self.body[0][0] - self.speed * dt
        if self.direction == 'down' and self.body[0][0] < x_max:
            self.body[0][0] = self.body[0][0] + self.speed * dt

        if round(previous_position[0]) != round(self.body[0][0]) or round(previous_position[1]) != round(self.body[0][1]):
            new_head = (round(copy.copy(self.body[0][0])), round(copy.copy(self.body[0][1])))
            self.draw_state = body_copy[:-1]
            # self.draw_state.insert(0, self.body[0])
            self.draw_state.insert(0, new_head)

    def check_collision(self, board):
        if self.draw_state[0] in self.draw_state[1:]:
            return False
        if self.body[0][0] > board.height or self.body[0][1] > board.width:
            return False
        return True
    
    def update_on_food(self, board):
        if (round(self.body[0][0]), round(self.body[0][1])) in board.food:
            self.points += 1
            board.food.remove((round(self.body[0][0]), round(self.body[0][1])))

            tail_part = copy.deepcopy(self.draw_state[-1])
            tail_adjacent_cells = [
                (tail_part[0] + 1,tail_part[0]),
                (tail_part[0] - 1,tail_part[0]),
                (tail_part[0],tail_part[0] + 1),
                (tail_part[0],tail_part[0] - 1)]
            
            while True:
                random_grow = random.choice(tail_adjacent_cells)
                if random_grow not in self.draw_state:
                    break

            self.draw_state.append(random_grow)

class Board():
    def __init__(self, width=SCREEN_WIDTH, height=SCREEN_HEIGHT) -> None:
        self.width = width
        self.height = height
        self.max_food = 10
        self.food = []
        self.board = [['. ' for k in range(self.width + 1)]
                      for m in range(self.height + 1)]

    def spawn_food(self):
        if len(self.food) < 10:
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
        to_draw = to_draw + (f'Score: {snake.points}')
        print(to_draw)

def update(snake: Snake, board: Board, dt):
    board.spawn_food()
    snake.clear_snake(board)
    snake.update_direction()
    snake.update_on_food(board)
    snake.move(board, dt)
    snake.draw_on_board(board)

    if keyboard.is_pressed('q'):
        os.system('cls')
        sys.exit()

def clear_screen():
    print('')
    print('\033[' + str(SCREEN_HEIGHT + 7) + 'A\033[2K', end='')
    print('\033[?25l', end="")


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
        
        not_over = snake.check_collision(board)
        if not not_over:
            os.system('cls')
            print('\n' * (SCREEN_HEIGHT - 1))
            print('GAME OVER')
            print(f'Points: {snake.points}')
            break

        board.draw(snake, dt)

if __name__ == "__main__":
    main()

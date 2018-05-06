import copy
import tkinter
from typing import Tuple

from constants import *
from field.field import Field


class Score:
    def __init__(self):
        self.value = -100


class Move:
    def __init__(self):
        self.direction = -1
        self.num_of_steps = -1


class Board:
    def __init__(self, num_of_rows=7, num_of_cols=7):
        self.current_player = PLAYER
        self.num_of_rows = num_of_rows
        self.num_of_cols = num_of_cols
        self.board_fields = []
        self.player_positions = [-1, -1]
        self.best_direction_to_go = -1
        self.best_num_of_steps = -1

        ai_player_x = 0
        ai_player_y = self.num_of_cols//2

        player_x = self.num_of_rows-1
        player_y = self.num_of_cols//2

        print(ai_player_x, ai_player_y, player_x, player_y)
        for i in range(num_of_rows):

            for j in range(num_of_cols):

                if i == ai_player_x and j == ai_player_y:

                    self.player_positions[0] = len(self.board_fields)
                    self.board_fields.append(Field(ai_player_x, ai_player_y, AI_PLAYER, True))

                elif i == player_x and j == player_y:

                    self.player_positions[1] = len(self.board_fields)
                    self.board_fields.append(Field(player_x, player_y, PLAYER, True))

                else:

                    self.board_fields.append(Field(i, j))

    def draw(self):

        for i, field in enumerate(self.board_fields):

            if i % self.num_of_cols == 0:

                print('\n', end='')

            field.draw()
        print('\n')

    def calculate_next_field_position(self, direction: int):
        next_field_position = {
            '0': lambda prev_field_position, num_of_steps: prev_field_position + num_of_steps,
            '1': lambda prev_field_position, num_of_steps: prev_field_position - num_of_steps * (self.num_of_cols - 1),
            '2': lambda prev_field_position, num_of_steps: prev_field_position - num_of_steps * self.num_of_cols,
            '3': lambda prev_field_position, num_of_steps: prev_field_position - num_of_steps * (self.num_of_cols + 1),
            '4': lambda prev_field_position, num_of_steps: prev_field_position - num_of_steps,
            '5': lambda prev_field_position, num_of_steps: prev_field_position + num_of_steps * (self.num_of_cols - 1),
            '6': lambda prev_field_position, num_of_steps: prev_field_position + num_of_steps * self.num_of_cols,
            '7': lambda prev_field_position, num_of_steps: prev_field_position + num_of_steps * (self.num_of_cols + 1),
        }[str(direction)]

        return next_field_position

    def calculate_row_col(self, field_position):
        return field_position//self.num_of_rows, field_position % self.num_of_rows

    def is_move_allowed(self, field_position: int, direction: int) -> bool:

        if field_position == 0 and (direction == directions['UP'] or direction == directions['UP_LEFT']
                                    or direction == directions['LEFT'] or direction == directions['RIGHT_UP']
                                    or direction == directions['LEFT_DOWN']):
            return False

        if field_position == self.num_of_cols-1 and (direction == directions['UP']
                                                     or direction == directions['UP_LEFT']
                                                     or direction == directions['RIGHT']
                                                     or direction == directions['RIGHT_UP']
                                                     or direction == directions['DOWN_RIGHT']):
            return False

        if field_position == self.num_of_rows*self.num_of_cols-1 and (direction == directions['DOWN']
                                                                      or direction == directions['DOWN_RIGHT']
                                                                      or direction == directions['RIGHT']
                                                                      or direction == directions['RIGHT_UP']
                                                                      or direction == directions['LEFT_DOWN']):
            return False

        if field_position == self.num_of_rows*self.num_of_cols-self.num_of_cols \
                and (direction == directions['DOWN'] or direction == directions['DOWN_RIGHT']
                     or direction == directions['LEFT'] or direction == directions['UP_LEFT']
                     or direction == directions['LEFT_DOWN']):
            return False

        if 0 < field_position < self.num_of_cols-1 \
                and (direction == directions['UP'] or direction == directions['UP_LEFT']
                     or direction == directions['RIGHT_UP']):
            return False

        if self.num_of_rows*self.num_of_cols-self.num_of_cols < field_position < self.num_of_rows*self.num_of_cols-1 \
                and (direction == directions['DOWN'] or direction == directions['LEFT_DOWN']
                     or direction == directions['DOWN_RIGHT']):
            return False

        quotient = field_position/self.num_of_cols
        if 0 < quotient < self.num_of_rows:
            if field_position % self.num_of_cols == 0 \
                and (direction == directions['LEFT'] or direction == directions['UP_LEFT']
                     or direction == directions['LEFT_DOWN']):
                return False
            if field_position % self.num_of_cols == self.num_of_cols-1\
                and (direction == directions['RIGHT'] or direction == directions['RIGHT_UP']
                     or direction == directions['DOWN_RIGHT']):
                return False
        quotient = field_position / self.num_of_cols
        if 0 < quotient < self.num_of_rows:
            if field_position % self.num_of_cols == 0 \
                    and (direction == directions['LEFT'] or direction == directions['UP_LEFT']
                         or direction == directions['LEFT_DOWN']):
                return False
            if field_position % self.num_of_cols == self.num_of_cols - 1 \
                    and (direction == directions['RIGHT'] or direction == directions['RIGHT_UP']
                         or direction == directions['DOWN_RIGHT']):
                return False

        return True

    def is_move_possible(self, field_position: int, direction: int, num_of_steps: int) -> bool:
        if not self.is_move_allowed(field_position, direction):
            return False
        counter = 1
        while counter != num_of_steps:
            next_field_position = self.calculate_next_field_position(direction)(field_position, counter)
            counter += 1
            if 0 > next_field_position or next_field_position >= len(self.board_fields):
                return False
            if self.board_fields[next_field_position].visited:
                return False
            if not self.is_move_allowed(next_field_position, direction):
                return False

        next_field_position = self.calculate_next_field_position(direction)(field_position, num_of_steps)
        if 0 > next_field_position or next_field_position >= len(self.board_fields):
            return False
        if self.board_fields[next_field_position].visited:
            return False

        return True

    def move(self, direction: int, num_of_steps: int):

        prev_field_position = self.player_positions[self.current_player % 2]
        counter = 1
        moves = []
        next_field_position = 0
        while counter != num_of_steps + 1:
            next_field_position = self.calculate_next_field_position(direction)(prev_field_position, counter)
            moves.append(next_field_position)
            counter += 1
            self.board_fields[next_field_position].belongs_to = self.current_player
            self.board_fields[next_field_position].visited = True
        self.player_positions[self.current_player % 2] = next_field_position
        self.current_player = (self.current_player + 1) % 2
        return moves

    def move_to_field_position(self, field_position: int):
        self.board_fields[field_position].belongs_to = self.current_player
        self.board_fields[field_position].visited = True

        self.player_positions[self.current_player % 2] = field_position
        self.current_player = (self.current_player + 1) % 2

    def has_one_move_to_win(self, field_position: int) -> Tuple[bool, int, int]:

        for direction in directions:
            for num in range(1, max(self.num_of_rows, self.num_of_cols)):
                if self.is_move_possible(field_position, directions[direction], num):
                    pom_board = copy.deepcopy(self)
                    pom_board.move(directions[direction], num)
                    if is_end(pom_board):
                        return True, directions[direction], num

        return False, -1, -1


def enter_command() -> Tuple:
    command = input("What is your next move (DIRECTION NUMBER_OF_STEPS)?")
    commands = parse_command(command)
    return commands


def parse_command(command) -> Tuple:
    c1, c2 = command.split(" ")
    c1 = c1.upper()
    return directions[c1], int(c2)


def is_end(board: Board) -> bool:
    field_position = board.player_positions[board.current_player % 2]
    for direction in directions:
        next_move = board.calculate_next_field_position(directions[direction])(field_position, 1)
        if board.is_move_allowed(field_position, directions[direction]) and 0 <= next_move < len(board.board_fields) \
                and not board.board_fields[next_move].visited:

            return False

    return True


def calculate_best_move(board: Board, score: Score, move: Move) -> Tuple:

    field_position = board.player_positions[board.current_player % 2]
    has, direction, num_of_moves = board.has_one_move_to_win(field_position)
    if has:
        if board.current_player == AI_PLAYER:
            return direction, num_of_moves, 1
        else:
            return direction, num_of_moves, -1

    for direction in directions:
        for num in range(1, max(board.num_of_rows, board.num_of_cols)):
            if board.is_move_possible(field_position, directions[direction], num):
                prev_direction = directions[direction]
                prev_num = num
                pom_board = copy.deepcopy(board)
                pom_board.move(directions[direction], num)
                next_direction, next_num, next_score = calculate_best_move(pom_board, score, move)
            else:
                break

            if board.current_player == AI_PLAYER and (next_score > score.value):
                score.value = next_score
                move.direction = prev_direction
                move.num_of_steps = prev_num

            if board.current_player == PLAYER and (next_score < score.value):
                score.value = next_score
                move.direction = prev_direction
                move.num_of_steps = prev_num

    return move.direction, move.num_of_steps, score.value


def move_agent(board: Board):
    score = Score()
    move = Move()
    copy_of_board = copy.deepcopy(board)
    command = calculate_best_move(copy_of_board, score, move)
    # print('command', command)
    moves = board.move(command[0], command[1])
    return moves



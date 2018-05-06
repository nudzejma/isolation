from typing import Tuple

from board.board import Board, enter_command, is_end, move_agent, Score
from constants import *


def play() -> None:
    b = Board(3, 3)
    b.draw()
    player_string = ''

    while not is_end(b):
        if b.current_player == AI_PLAYER:
            player_string = 'AI player'
            print(player_string, ' on move.')
            move_agent(b)
            b.draw()
        else:
            player_string = 'Player'
            print(player_string, ' on move.')

            command = enter_command()
            while not b.is_move_possible(b.player_positions[1], command[0], command[1]):
                print("Command not allowed. Enter again.")
                command = enter_command()
            b.draw()

    print('Game is over.', player_string, 'has won.')


play()


import tkinter

from board.board import Board, is_end, move_agent
from constants import *


class Player:
    def __init__(self, name, color):
        self.name = name
        self.color = color


class GuiBoard:
    def __init__(self, board: Board, root=tkinter.Tk, sq_size=100):
        self.container = tkinter.Frame(root)
        self.container.pack()
        self.sq_size = sq_size
        self.canvas = tkinter.Canvas(self.container, width=self.sq_size * board.num_of_cols,
                                     height=self.sq_size * board.num_of_rows)
        self.canvas.grid()
        self.board = board

    def draw(self):
        for row in range(3):
            for column in range(3):
                self.canvas.create_rectangle(self.sq_size * column, self.sq_size * row, self.sq_size * (column + 1),
                                             self.sq_size * (row + 1), fill="#ECECEC")

    def get_row_col(self, evt):
        # get the row and col from event's x and y coords

        return evt.x, evt.y

    def floor_of_row_col(self, col, rw):
        """
        normalize col and row number for all board size by taking
        the floor of event's x and y coords as col and row, respectively
        """
        col_flr = col // self.sq_size
        rw_flr = rw // self.sq_size
        return col_flr, rw_flr

    def convert_to_key(self, col_floor, row_floor):
        # turn col and row's quotient into a string for the key
        return str(col_floor) + str(row_floor)

    def find_coords_of_selected_sq(self, evt):
        """
        finding coords in a 9-sq grid

        params: event triggered by user's click
        return: tuple of two values for second corner's col, row
        """
        # saves row and col tuple into two variables

        column, row = self.get_row_col(evt)
        # normalize for all square size by keeping the floor
        column_floor, row_floor = self.floor_of_row_col(column, row)

        # convert to key, use key to locate position in 3x3 grid
        rowcol_key_str = self.convert_to_key(column_floor, row_floor)

        corner_column = (column_floor * self.sq_size) + self.sq_size
        corner_row = (row_floor * self.sq_size) + self.sq_size

        return corner_column, corner_row

    def color_selected_sq(self, evt, second_corner_col,
                          second_corner_row, player_color):

        self.canvas.create_rectangle(
            (evt.x // self.sq_size) * self.sq_size,
            (evt.y // self.sq_size) * self.sq_size,
            second_corner_col,
            second_corner_row,
            fill=player_color)

    def color_selected_sq_using_xy(self, x, y, second_corner_col, second_corner_row, player_color):

        self.canvas.create_rectangle((x // self.sq_size) * self.sq_size,(y // self.sq_size) * self.sq_size,
                                     second_corner_col, second_corner_row, fill=player_color)


class Game:
    def __init__(self, parent):
        self.parent = parent  # parent is root
        global root
        self.gui_board = GuiBoard(Board(3, 3), root)
        self.gui_board.draw()
        self.initialize_buttons()

        self.player1 = Player("AI", "#446CB3")
        self.player2 = Player("PLAYER", "#F4D03F")

        self.two_players_button.grid()

    def initialize_buttons(self):
        self.reset_button = tkinter.Button(self.gui_board.container,
                                           text="RESET",
                                           width=25,
                                           command=self.restart)

        self.two_players_button = tkinter.Button(self.gui_board.container,
                                                 text="PLAY",
                                                 width=25,
                                                 command=self.init_two_players_game)

    def init_two_players_game(self):
        # reset board's unused squares
        # AI player
        # self.gui_board.board.draw()
        self.two_players_button.destroy()
        row, column = self.gui_board.board.calculate_row_col(self.gui_board.board.player_positions[0])
        row, column = row*100, column*100
        column_floor, row_floor = self.gui_board.floor_of_row_col(column, row)
        corner_column = (column_floor * self.gui_board.sq_size) + self.gui_board.sq_size
        corner_row = (row_floor * self.gui_board.sq_size) + self.gui_board.sq_size

        self.gui_board.color_selected_sq_using_xy(column, row, corner_column, corner_row, self.player1.color)

        # player
        row, column = self.gui_board.board.calculate_row_col(self.gui_board.board.player_positions[1])
        row, column = row * 100, column * 100
        column_floor, row_floor = self.gui_board.floor_of_row_col(column, row)
        corner_column = (column_floor * self.gui_board.sq_size) + self.gui_board.sq_size
        corner_row = (row_floor * self.gui_board.sq_size) + self.gui_board.sq_size

        self.gui_board.color_selected_sq_using_xy(column, row, corner_column, corner_row, self.player2.color)
        # reset players' squares to empty set

        # keep track of turns
        if self.gui_board.board.current_player == AI_PLAYER:
            self.player1_turn = True
            self.show_text("My turn.")
        else:
            self.player1_turn = False
            self.show_text("Your turn.")

        # show reset button
        self.reset_button.grid()
        # bind play() to the leftmost button click, for macs
        # windows or other pcs might be "<Button-2>"
        self.gui_board.canvas.bind("<Button-1>", self.play)

    def play_ai(self):
        moves = move_agent(self.gui_board.board)

        for move in moves:
            row, column = self.gui_board.board.calculate_row_col(move)

            row, column = row*100, column*100
            column_floor, row_floor = self.gui_board.floor_of_row_col(column, row)
            corner_column = (column_floor * self.gui_board.sq_size) + self.gui_board.sq_size
            corner_row = (row_floor * self.gui_board.sq_size) + self.gui_board.sq_size

            self.gui_board.color_selected_sq_using_xy(column, row, corner_column, corner_row, self.player1.color)

        if is_end(self.gui_board.board):
            self.show_game_result(self.player1.name + " WIN!")
            self.restart()

        # switch turn
        self.player1_turn = False

        # self.gui_board.board.draw()

    def play(self, event):
        """  method is invoked when the user clicks on a square
        handles click event on UI for player
        Params: event (as mouse click, with x/y coords)
        """
        self.show_text("Your turn")
        if self.player1_turn == True:

            column, row = move_agent(self.gui_board.board)
            column_floor, row_floor = self.gui_board.floor_of_row_col(column, row)

            corner_column = (column_floor * self.gui_board.sq_size) + self.gui_board.sq_size
            corner_row = (row_floor * self.gui_board.sq_size) + self.gui_board.sq_size

            self.gui_board.color_selected_sq(event, corner_column, corner_row, self.player1.color)

            if is_end(self.gui_board.board):
                self.show_game_result(self.player1.name + " WIN!")
                self.restart()
            # switch turn
            self.player1_turn = False

            # self.gui_board.board.draw()

        else:  # player2's turn

            field_position_y, field_position_x = self.gui_board.get_row_col(event)
            field_position_y, field_position_x = self.gui_board.floor_of_row_col(field_position_y, field_position_x)
            field_position = field_position_x*self.gui_board.board.num_of_cols + field_position_y
            self.gui_board.board.move_to_field_position(field_position)
            self.gui_board.board.draw()

            colrow_tuple = self.gui_board.find_coords_of_selected_sq(event)

            corner_two_col, corner_two_row = colrow_tuple[0], colrow_tuple[1]

            col_fl, row_fl = self.gui_board.floor_of_row_col(event.x, event.y)
            rowcol_key = self.gui_board.convert_to_key(col_fl, row_fl)
            self.gui_board.color_selected_sq(event, corner_two_col, corner_two_row, self.player2.color)

            if is_end(self.gui_board.board):
                self.show_game_result(self.player2.name + " WIN!")
                self.restart()

            self.player1_turn = True
            self.show_text("Played. Your turn again.")
            self.play_ai()

    def show_text(self, text):
        global T
        T.delete(1.0,tkinter.END)
        T.insert(tkinter.END, text)

    def show_game_result(self, txt):
        """
        make a label to display three possible winning conditions
        params: txt to display the winner
                player_color to display matching color as player's sq
        """
        result_label = tkinter.Label(self.gui_board.container,
                                     text=txt,
                                     width=32,
                                     height=10,
                                     foreground="red",
                                     background="gray",
                                     borderwidth=3)

        result_label.grid(row=0, column=0)
        # unbind button so player cannot click on square
        self.gui_board.canvas.unbind("<Button-1>", self.play)

    def restart(self):
        global root
        self.gui_board.container.destroy()
        self.gui_board = GuiBoard(Board(3, 3), root)
        self.gui_board.draw()
        self.initialize_buttons()
        # self.init_two_players_game()
        self.two_players_button.grid()
        self.init_two_players_game()


root = tkinter.Tk()
root.title("Isolation")
T = tkinter.Text(root, height=2, width=30)
T.pack()
T.insert(tkinter.END, "Click on play button\nto play\n")
game = Game(root)
root.mainloop()





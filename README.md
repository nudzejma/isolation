# Isolation

Isolation is a turn-based strategy board game where two players try to confine their opponent on a 7x7 checker-like board. Eventually, they can no longer make a move (thus isolating them).

Each player has one piece, which they can move around like a queen in chess — up-down, left-right, and diagonal. There are three conditions under which the pieces can be moved —

They cannot place their piece on an already visited square.
They cannot cross over already visited squares (squeezing through them diagonally is OK).
They cannot cross over each other’s piece.

This is the implementation of AI player using `minimax` algorithm.

To play the game start `gui.py` file.


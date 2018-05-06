from constants import NO_ONE, AI_PLAYER


class Field:
    def __init__(self, x: int, y: int, belongs_to=NO_ONE, visited=False) -> None:
        self.x = x
        self.y = y
        self.visited = visited
        self.belongs_to = belongs_to

    def draw(self):
        if self.belongs_to == NO_ONE:
            print(' NO ', end='')
        elif self.belongs_to == AI_PLAYER:
            print(' AI ', end='')
        else:
            print(' PL ', end='')
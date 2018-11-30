from enum import Enum

class Node:
    def __init__(self, x, y, parent, direction, move):
        """param: h manhattan distance from node to goal
           param: g actual steps to node from start"""
        self.parent: Node
        self.parent = parent
        self.x = x
        self.y = y
        self.g = None
        self.h = None
        self.f = None
        self.direction = direction
        self.move = move

    def pretty(self):
        return "{} {} {} {} {} {}".format(self.x, self.y, self.g, self.h, self.parent, self.direction)

    def set_f(self):
        self.f = self.g + self.h

    def __lt__(self, other):
        if self.x == other.y:
            return self.y < self.y
        return self.x < other.x

class Frontier(Enum):
    IS_LOWER = 0
    IS_EQUAL = 1
    IS_LARGER = 2
    NOT_IN = 3

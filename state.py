from enum import Enum
import gameobjects

class State:
    def __init__(self, x, y, food, direction, board, snake_head):
        """param: h manhattan distance from node to goal
           param: g actual steps to node from start"""
        self.parent: State
        self.food = food
        self.snake_head = snake_head
        self.board = board
        self.vertical_move = None
        self.horizontal_move = None
        self.get_food_dir()
        self.x = x
        self.y = y
        self.direction = direction

    def get_food_dir(self, food, snake_head):
        self.vertical_move = snake_head[0] - food[0]
        self.horizontal_move = snake_head[1] - food[1]
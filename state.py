import move


class State:
    def __init__(self, x, y, food, direction, board):
        """param: h manhattan distance from node to goal
           param: g actual steps to node from start"""
        self.parent: State
        self.food = food
        self.board = board
        self.vertical_move = None
        self.horizontal_move = None
        self.x = x
        self.y = y
        self.direction = direction
        self.food_dir = self.get_food_dir
        self.clear_left, self.clear_straight, self.clear_right = False, False, False

    def check_moves(self):
        straight = {
            self.direction == move.Direction.NORTH: self.board[self.x][self.y + 1] == 3,
            self.direction == move.Direction.EAST: self.board[self.x + 1][self.y] == 3,
            self.direction == move.Direction.SOUTH: self.board[self.x][self.y - 1] == 3,
            self.direction == move.Direction.WEST: self.board[self.x - 1][self.y] == 3,
        }

        left = {
            self.direction == move.Direction.NORTH: self.board[self.x - 1][self.y ] == 3,
            self.direction == move.Direction.EAST: self.board[self.x ][self.y + 1] == 3,
            self.direction == move.Direction.SOUTH: self.board[self.x + 1][self.y] == 3,
            self.direction == move.Direction.WEST: self.board[self.x][self.y - 1] == 3,
        }

        right = {
            self.direction == dir.NORTH: self.board[self.x + 1][self.y] == 3,
            self.direction == dir.EAST: self.board[self.x][self.y - 1] == 3,
            self.direction == dir.SOUTH: self.board[self.x - 1][self.y] == 3,
            self.direction == dir.WEST: self.board[self.x][self.y + 1] == 3,
        }

        return left, straight, right

    @property
    def get_food_dir(self):

        straight = {
            self.direction == move.Direction.NORTH: self.food[1] <= self.y,
            self.direction == move.Direction.EAST: self.x >= self.food[0],
            self.direction == move.Direction.SOUTH: self.y <= self.food[1],
            self.direction == move.Direction.WEST: self.x <= self.food[0]

        }
        if straight:
            return move.Move.STRAIGHT

        left = {
            self.direction == move.Direction.NORTH: self.x < self.food[0],
            self.direction == move.Direction.EAST: self.y >  self.food[1],
            self.direction == move.Direction.SOUTH: self.x > self.food[0],
            self.direction == move.Direction.WEST: self.y < self.food[1]
        }

        if left:
            return move.Move.LEFT
        return move.Move.RIGHT

    def get_dist(self):
        return abs(self.x - self.food[0]), abs(self.y - self.food[1])
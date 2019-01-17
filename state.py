import move


class State:
    def __init__(self, food_dist, direction):
        self.food_dist = food_dist
        self.direction = direction

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


class Q_entry:
    def __init__(self, state, action):
        self.state = state
        self.action = action
        self.reward = 0

    def set_reward(self, reward):
        self.reward = reward

    def __str__(self):
        return "FOODDIST" + self.state.food_dist + "Move: " + self.action + "R: " + self.reward
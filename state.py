import move


class State:
    def __init__(self, food_dist):
        self.food_dist = food_dist




class Q_entry:
    def __init__(self, state, action):
        self.state = state
        self.action = action
        self.reward = 0

    def __str__(self):
        return "FOODDIST" + self.state.food_dist + "Move: " + self.action + "R: " + self.reward
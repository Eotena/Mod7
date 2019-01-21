import random

import move as move

from move import Move
import move

from gameobjects import GameObject
from move import Move, Direction
from state import State, Q_entry
import queue

# used as upper bound for length manhattan distance if location is not empty
LIMIT = 1000


class Agent:

    def __init__(self):
        """" Constructor of the Agent, can be used to set up variables """
        self.died = False
        self.epsilon = None
        self.q_table = None
        self.alpha = 0.5
        self.gamma = 0.95
        self.last_state = None
        self.last_action = None
        self.state_size = 9
        self.last_score = 0
        self.q_table = [[[0 for x in range(0, 4)] for y in range(0, self.state_size)] for dir in range(0, self.state_size)]

    def get_move(self, board, score, turns_alive, turns_to_starve, direction, head_position, body_parts, fed):
        """This function behaves as the 'brain' of the snake. You only need to change the code in this function for
        the project. Every turn the agent needs to return a move. This move will be executed by the snake. If this
        functions fails to return a valid return (see return), the snake will die (as this confuses its tiny brain
        that much that it will explode). The starting direction of the snake will be North.

        :param board: A two dimensional array representing the current state of the board. The upper left most
        coordinate is equal to (0,0) and each coordinate (x,y) can be accessed by executing board[x][y]. At each
        coordinate a GameObject is present. This can be either GameObject.EMPTY (meaning there is nothing at the
        given coordinate), GameObject.FOOD (meaning there is food at the given coordinate), GameObject.WALL (meaning
        there is a wall at the given coordinate. TIP: do not run into them), GameObject.SNAKE_HEAD (meaning the head
        of the snake is located there) and GameObject.SNAKE_BODY (meaning there is a body part of the snake there.
        TIP: also, do not run into these). The snake will also die when it tries to escape the board (moving out of
        the boundaries of the array)

        :param score: The current score as an integer. Whenever the snake eats, the score will be increased by one.
        When the snake tragically dies (i.e. by running its head into a wall) the score will be reset. In ohter
        words, the score describes the score of the current (alive) worm.

        :param turns_alive: The number of turns (as integer) the current snake is alive.

        :param turns_to_starve: The number of turns left alive (as integer) if the snake does not eat. If this number
        reaches 1 and there is not eaten the next turn, the snake dies. If the value is equal to -1, then the option
        is not enabled and the snake can not starve.

        :param direction: The direction the snake is currently facing. This can be either Direction.NORTH,
        Direction.SOUTH, Direction.WEST, Direction.EAST. For instance, when the snake is facing east and a move
        straight is returned, the snake wil move one cell to the right.

        :param head_position: (x,y) of the head of the snake. The following should always hold: board[head_position[
        0]][head_position[1]] == GameObject.SNAKE_HEAD.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.

        :return: The move of the snake. This can be either Move.LEFT (meaning going left), Move.STRAIGHT (meaning
        going straight ahead) and Move.RIGHT (meaning going right). The moves are made from the viewpoint of the
        snake. This means the snake keeps track of the direction it is facing (North, South, West and East).
        Move.LEFT and Move.RIGHT changes the direction of the snake. In example, if the snake is facing north and the
        move left is made, the snake will go one block to the left and change its direction to west.
        """

        # search for food
        food = self.get_food_location(board)

        #        print(food)
        #        print(head_position)

        # get food distance and initialise the state
        food_dist = self.get_dist(food, head_position)
        food_dist = (food_dist[0] + 4, food_dist[1] + 4)

        print(self.last_state)
        print(self.last_action)
        # none if first move after init, since no action is taken and no update
        # updates reward values for last state action pair
        reward_value = 0
        if self.last_state is not None and self.last_action is not None and not self.died:
            if score > self.last_score:
                reward = 1
                reward_value = self.reward_value(reward, self.last_state, direction, food_dist)
                self.q_table[self.last_state[0]][self.last_state[1]][self.last_action.value] = reward_value
            else:
                reward = -0.04
                reward_value = self.reward_value(reward, self.last_state, direction, food_dist)
                self.q_table[self.last_state[0]][self.last_state[1]][self.last_action.value] = reward_value
        self.died = False
        future_action = self.choose_action(self.get_actions(direction), food_dist)
        future_move = Move(self.get_new_move(future_action, direction))
        self.last_action = direction.get_new_direction(future_move)
        self.last_state = food_dist
        print("------------------------------------------------------------------")
        self.last_score = score
        return future_move

    @staticmethod
    def get_new_move(future_move, direction):
        return (future_move.value - direction.value) % 2 - 1

    @staticmethod
    def get_food_location(board):
        # print(self.board)
        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] == GameObject.FOOD:
                    return x, y

    @staticmethod
    def get_actions(direction):
        """returns list of  directions when actions applied to given direction
        """
        actions = []
        for mov in Move:
            actions.append(direction.get_new_direction(mov))
        return actions

    @staticmethod
    def get_dist(food, head):
        return head[0] - food[0], head[1] - food[1]

    def choose_action(self, actions, state):
        """returns action with highest value in q_table
        :param state: the given state of which we want to return the highest

        :param actions: the possible actions we can make from the given state (Direction)

        :returns: achievable direction that gives the highest q_value
        """

        q_values = []

        for action in actions:
            q_values.append([(self.q_table[state[0]][state[1]][action.value]), action])
        print(q_values)
        print(q_values[0][0])
        print(q_values[1][0])
        print(q_values[2][0])
        if q_values[0][0] == q_values[1][0]:
            if q_values[0][0] == q_values[2][0]:
                index = random.randint(0, 2)
                return q_values[index][1]
            elif q_values[0][0] > q_values[2][0]:
                index = random.randint(0, 1)
                return q_values[index][1]
        elif q_values[1][0] == q_values[2][0] and q_values[1][0]:
            index = random.randint(0, 1)
            return q_values[index][1]
        elif q_values[0][0] == q_values[2][0]:
            q_values.remove(q_values[1])
            index = random.randint(0, 1)
            return q_values[index][1]
        elif q_values[0][0] > q_values[1][0]:
            if q_values[0][0] > q_values[2][0]:
                return q_values[0][1]
        elif q_values[1][0] > q_values[0][0]:
            if q_values[1][0] > q_values[2][0]:
                return q_values[1][1]
        else:

            return q_values[2][1]


        """"
        q_values = queue.PriorityQueue()
        for action in actions:
            q_values.put(-1 * self.q_table[state[0]][state[1]][action.value], action)
        if q_values.queue[0] == q_values.queue[1]:
            if q_values.queue[0] == q_values.queue[2]:
                index = random.randint(0, 2)
                while index != 0:
                    q_values.get()
                    index += -1
                return q_values.get()
            index = random.randint(0, 1)
            while index != 0:
                q_values.get()
                index += -1
            return q_values.get()
        else:
            return q_values.get()
        """

    def reward_value(self, reward, last_state, last_action, curr_state):
        print("I did not die")
        last_value = self.q_table[last_state[0]][last_state[1]][last_action.value]
        print(last_value)
        best_hypothetical_action = (self.choose_action(self.get_actions(last_action), curr_state))
        # add function to find the possible actions in this state
        print(best_hypothetical_action)

        max_next_reward = self.q_table[last_state[0]][last_state[1]][best_hypothetical_action.value]

        reward = last_value + self.alpha * (reward + self.gamma * max_next_reward - last_value)
        print(reward)
        return reward

    def reward_value_dead(self, last_state, last_action):
        print("Hey I died")
        last_value = self.q_table[last_state[0]][last_state[1]][last_action.value]
        reward = last_value + self.alpha * (-1 - last_value)
        print(reward)
        return reward

    @staticmethod
    def should_redraw_board():
        """
        This function indicates whether the board should be redrawn. Not drawing to the board increases the number of
        games that can be played in a given time. This is especially useful if you want to train you agent. The
        function is called before the get_move function.

        :return: True if the board should be redrawn, False if the board should not be redrawn.
        """
        return True

    @staticmethod
    def should_grow_on_food_collision():
        """
        This function indicates whether the snake should grow when colliding with a food object. This function is
        called whenever the snake collides with a food block.

        :return: True if the snake should grow, False if the snake should not grow
        """
        return False

    def on_die(self, head_position, board, score, body_parts):
        """This function will be called whenever the snake dies. After its dead the snake will be reincarnated into a
        new snake and its life will start over. This means that the next time the get_move function is called,
        it will be called for a fresh snake. Use this function to clean up variables specific to the life of a single
        snake or to host a funeral.

        :param head_position: (x, y) position of the head at the moment of dying.

        :param board: two dimensional array representing the board of the game at the moment of dying. The board
        given does not include information about the snake, only the food position(s) and wall(s) are listed.

        :param score: score at the moment of dying.

        :param body_parts: the array of the locations of the body parts of the snake. The last element of this array
        represents the tail and the first element represents the body part directly following the head of the snake.
        When the snake runs in its own body the following holds: head_position in body_parts.
        """

        reward_value = 0
        reward_value = (self.last_state, self.last_action)
        self.q_table[self.last_state[0]][self.last_state[1]][self.last_action.value] = reward_value
        self.died = True
        # self.last_state = None
        # self.last_action = None

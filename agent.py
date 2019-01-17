import random

import move as move

from move import Move
import move

from gameobjects import GameObject
from move import Move, Direction
from state import State, Q_entry
import heapq
import queue
import numpy as np
import gym

import move
# from keras.models import Sequential
# from keras.optimizers import Adam

# from rl.agents.dqn import DQNAgent
# from rl.policy import EpsGreedyQPolicy
# from rl.memory import SequentialMemory

# used as upper bound for length manhattan distance if location is not empty
LIMIT = 1000


class Agent:

    def __init__(self):
        """" Constructor of the Agent, can be used to set up variables """
        self.env = None
        self.epsilon = None
        self.q_table = []
        self.reward = 0
        self.board = None
        self.alpha = 0.5
        self.gamma = 0.95
        self.last_state = None
        self.last_action = None

        for x in range(5):
            for y in range(5):
                for a in range(5):
                    for b in range(5):
                        dist = self.get_dist([a, b], [x, y])
                        for direc in Direction:
                            state = State(dist, direc)

                            for mov in Move:
                                q_entry = Q_entry(state, mov)
                                self.q_table.append(q_entry)

        print(self.q_table.__str__())

    def get_move(self, board, score, turns_alive, turns_to_starve, direction, head_position, body_parts, died , fed):
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

        self.board = board
        food = []
        for x in range(len(board)):
            for y in range(len(board)):

                print(board[x][y])
                if board[x][y] == GameObject.FOOD:
                    food = [x, y]
                    break
        print(food)
        print(head_position)
        food_dist = self.get_dist(food, head_position)
        curr_state = State(food_dist, direction)

        if self.last_state is not None and self.last_action is not None:
            last_state_index = None
            for entry in self.q_table:
                index = self.q_table.index(entry)
                if entry == self.last_state and self.last_action == self.q_table[index]:
                    last_state_index = index

            if died:
                reward = -1
                self.reward_value(reward, last_state_index, self.last_state)
            elif fed:
                reward = 1
                self.reward_value(reward, last_state_index, self.last_state)

        q_indexes = []
        for entry in self.q_table:
            if curr_state.food_dist == entry.state.food_dist and curr_state.direction == entry.state.direction:
                print("hey, they are the same")
                q_indexes.append(self.q_table.index(entry))
                if q_indexes.__sizeof__() == 3:
                    break

        action = self.choose_action(q_indexes)

        self.last_action = action
        self.last_state = curr_state
        print("stuff is done")
        print(action)
#

        return action

    def get_food_location(self, board):
        # print(self.board)
        for x in range(len(board)):
            for y in range(len(board[x])):
                if board[x][y] == GameObject.FOOD:
                    return [x, y]

    @staticmethod
    def get_dist(food, head):
        return abs(head[0] - food[0]), abs(head[1] - food[1])

    @staticmethod
    def choose_action(q_indexes):
        print("some indexes")
        print(q_indexes)
        if q_indexes[0] == q_indexes[1] and q_indexes[0] == q_indexes[2]:
            return random.randint(0,2)

        max = -1
        maxes = []
        for index in q_indexes:
            if index >= max:
                max = index
                maxes.append(index)

        if maxes.__sizeof__() == 1:
            return maxes[0]
        else:
            return maxes[random.randint(0, len(maxes))]

    def reward_value(self, reward, q_index, curr_state):
        last_value = self.q_table[q_index].reward
        max_action = -1
        q_indexes = []
        for entry in self.q_table:
            if curr_state.food_dist == entry.state.food_dist and curr_state.direction == entry.state.direction:
                print("hey, they are the same")
                q_indexes.append(self.q_table.index(entry))
                if q_indexes.__sizeof__() == 3:
                    break
        if q_indexes[0] == q_indexes[1] and q_indexes[0] == q_indexes[2]:
            max_action =  random.randint(0,2)

        for index in q_indexes:
            if index >= max:
                max_action = index

        max_reward = self.q_table[q_indexes[index]]

        reward = reward + self.alpha * (reward + max_reward - reward)
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

from gameobjects import GameObject
from move import Move, Direction
import random

# used as upper bound for length manhattan distance if location is not empty
LIMIT = 1000


class Agent:

    def __init__(self):
        """" Constructor of the Agent, can be used to set up variables """
        self.locfood = None
        self.board = None
        self.distance = None
        self.head_pos = None
        self.manhattanmap = None
        self.lastdirection = None
        self.move_number = 0
        # print(len(Move))

    def get_move(self, board, score, turns_alive, turns_to_starve, direction, head_position, body_parts):
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
        self.lastdirection = direction
        self.board = board
        self.head_pos = head_position
        if self.locfood is None or self.board[self.locfood[0]][self.locfood[1]] != GameObject.FOOD:
            # print('locfood none or eaten')
            self.locfood = self.get_food_location()

        distances = None
        moves = None
        distance_shortest = LIMIT + 1
        move_shortest = Move.STRAIGHT
        multiple_shortest = False
        for mov in Move:
            x, y, hypothetical_direction = self.new_location(mov)
            if self.check_valid(hypothetical_direction):
                hypothetical_distance = self.manhattandistance(x, y)
                if hypothetical_distance == distance_shortest:
                    print('equally close manhattan distances')
                    if multiple_shortest: # add the current equal distance move
                        moves.append(mov)
                        distances.append(hypothetical_distance)
                    else: # reset lists and switch to true and add last one and current
                        multiple_shortest = True
                        distances = list()
                        moves = list()
                        moves.append(move_shortest)
                        moves.append(move_shortest)
                        distances.append(distance_shortest)
                        distances.append(hypothetical_distance)
                elif hypothetical_distance < distance_shortest: # switch to false and make move
                    multiple_shortest = False
                    move_shortest = mov
                    distance_shortest = hypothetical_distance

        if not multiple_shortest:
            nextmove = move_shortest
        else:
            nextmove = random.choice(moves)
        print('nextmove:', nextmove, 'len:', 'None' if moves is None else len(moves), self.move_number)
        self.move_number += 1
        return nextmove

    def check_valid(self, direction):
        """:param direction: gives a move, move.straight, move.left or move.left"""
        if self.head_pos[1] == 0 and direction == Direction.NORTH:
            return False
        elif self.head_pos[1] == 24 and direction == Direction.SOUTH:
            return False
        elif self.head_pos[0] == 0 and direction == Direction.WEST:
            return False
        elif self.head_pos[0] == 24 and direction == Direction.EAST:
            return False
        else:
            return True
            # moves.append(mov)
            # distances.append(self.manhattandistance(x, y))

    def new_location(self, direc):
        """:param direc indicates the hypothetical direction for the snake eg move.STRAIGHT"""
        new_direction = self.lastdirection.get_new_direction(direc)
        manip = new_direction.get_xy_manipulation()
        # print('old:', self.head_pos)
        x = self.head_pos[0] + manip[0]
        y = self.head_pos[1] + manip[1]
        # print('new pos:', (x, y))
        return x, y, new_direction

    def get_food_location(self):
        # print(self.board)
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                if self.board[x][y] == GameObject.FOOD:
                    return x, y

    def boarddistances(self):
        map = None
        for x in range(len(self.board)):
            for y in range(len(self.board[x])):
                map.append(self.manhattandistance(x, y))
                return map

    def manhattandistance(self, x, y):
        if (self.board[x][y] == GameObject.FOOD) or (self.board[x][y] == GameObject.EMPTY):
            return abs(x - self.locfood[0]) + abs(y - self.locfood[1])
        else:
            return LIMIT

    def should_redraw_board(self):
        """
        This function indicates whether the board should be redrawn. Not drawing to the board increases the number of
        games that can be played in a given time. This is especially useful if you want to train you agent. The
        function is called before the get_move function.

        :return: True if the board should be redrawn, False if the board should not be redrawn.
        """
        return True

    def should_grow_on_food_collision(self):
        """
        This function indicates whether the snake should grow when colliding with a food object. This function is
        called whenever the snake collides with a food block.

        :return: True if the snake should grow, False if the snake should not grow
        """
        return True

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

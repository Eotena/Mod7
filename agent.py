from gameobjects import GameObject
from move import Move, Direction
import random
from node import Node, Frontier
import heapq
import queue

# used as upper bound for length manhattan distance if location is not empty
LIMIT = 1000


class Agent:

    def __init__(self):
        """" Constructor of the Agent, can be used to set up variables """
        self.locfood = None
        self.board = None
        self.distance = None
        self.head_pos = None
        self.lastdirection = Direction.NORTH # should not matter since default is move.straight(north)
        self.move_number = 0
        self.frontier = queue.PriorityQueue()
        self.closed = list()
        self.remaining_moves = list()

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
        # find food location if necessary TODO: if multiple use shortest manhattan
        if self.locfood is None or self.board[self.locfood[0]][self.locfood[1]] != GameObject.FOOD:
            # print('locfood none or eaten')
            self.locfood = self.get_food_location()
        if len(self.remaining_moves) != 0:
            return self.remaining_moves.pop(0)
        # print('nextmove:', nextmove, 'len:', 'None' if moves is None else len(moves), self.move_number)
        if self.search_a_star(direction):
            return self.remaining_moves.pop(0)
        else:  # implement using most spaces and snake near edge
            pass
        # return Move.STRAIGHT

    def search_a_star(self, direction):
        # f(n) = g(n) + h(n)
        # weight = actual_steps_to_node_n(actual) + expected_steps_from_n_to_goal (manhattan)
        # add start node
        start_node = Node(self.head_pos[0], self.head_pos[1], None, direction, None) # didnt have to make a move to get there
        start_node.f = self.manhattandistance(start_node.x, start_node.y)
        start_node.g = 0
        # print(start_node.pretty())
        self.frontier.put((start_node.f, start_node))
        while len(self.frontier.queue) != 0:
            # remove node from frontier and add to closed -> will be expanded
            print("------------------------")
            f, expand_node = self.frontier.get()
            self.closed.append(expand_node)
            print("expand node: {}".format((expand_node.x, expand_node.y)))
            # check if goal
            if (expand_node.x == self.locfood[0]) and (expand_node.y == self.locfood[1]):
                # print('entered on food')
                self.backtrackpath(expand_node)  # TODO: implement backtrack function if at goal
                return True
            # print('after food match')
            for mov in Move:
                child_x, child_y, hypothetical_direction = self.hypothetical_new_location(expand_node.x, expand_node.y, expand_node.direction, mov)
                if self.valid_child(child_x, child_y):
                    child_node = Node(child_x, child_y, expand_node, hypothetical_direction, mov)
                    child_node.g = child_node.parent.g + 1
                    print("child: {}, {}".format(child_node.x, child_node.y))
                    a = []
                    for nod in self.frontier.queue:
                        a.append("{}, ({}, {});".format(nod[0], nod[1].x, nod[1].y))
                    print("frontier")
                    print("".join(a))
                    b = []
                    for nod in self.closed:
                        a.append("{}, ({}, {});".format(nod.f, nod.x, nod.y))
                    print("closed")
                    print("".join(b))
                    print("___________")
                    # child_node already in frontier list
                    in_frontier = False
                    for frontier in self.frontier.queue:
                        f, frontier_node = frontier
                        if frontier_node.x == child_node.x and frontier_node.y == child_node.y:
                            in_frontier = True
                            if frontier_node.g <= child_node.g:
                                break               # was continue
                            
                    if in_frontier:
                        continue
                    # child_node in the closed list and NOT in frontier list
                    in_closed = False
                    clos = ""
                    for closed_index in range(len(self.closed)):
                        closed_node = self.closed[closed_index]
                        if closed_node.x == child_node.x and closed_node.y == child_node.y:
                            in_closed = True
                            clos = clos + " in closed"
                            if closed_node.g <= child_node.g:
                                clos = clos + " and is better"
                                break               # was continue
                            else:  # can improve how quick to get to child_node
                                child_node.h = self.manhattandistance(child_node.x, child_node.y)
                                child_node.f = child_node.g + child_node.h
                                self.frontier.put((child_node.f, child_node))
                    if in_closed:
                        print(clos)
                        continue
                    # not in frontier or closed list
                    child_node.h = self.manhattandistance(child_x, child_y)
                    child_node.f = child_node.g + child_node.h
                    self.frontier.put((child_node.f, child_node))
        print("no path found")
        return False
                    
                    



                    # else:
                    #     closed_node_index = self.in_closed(child_node)
                    #     # in the closed list
                    #     if closed_node_index != False:
                    #         closed_node = self.closed[closed_node_index]
                    #         #present node in closed accessed quicker (g), so go to next
                    #         if closed_node.g <= child_node.g:
                    #             break            # was continue TODO most likely alter this
                    #         self.closed.pop(closed_node_index)
                    #         heapq.heappush(self.frontier, (closed_node.f, closed_node)
                    #     # NOT in closed list
                    #     else:
                    #         heapq.heappush(self.frontier, (child_node.f, child_node))
                    #         child_node.h = self.manhattandistance(child_x, child_y) # can be replaced to child_node.x and .y
                    #         child_node.set_f()
                    # # child_node NOT in frontier list yet
                    #     else:
                    #         heapq.heappush(self.frontier, (cchild_node) )

    def backtrackpath(self, last_node):
        print("at the final node!!")
        routelist = list()
        while last_node.parent is not None:
            routelist.append(last_node.move)
            last_node = last_node.parent
        routelist.reverse()
        self.remaining_moves = routelist
        self.frontier.
        print(*routelist)

    def in_frontier(self, node):
        for current_node in self.frontier:
            if current_node.x == node.x and current_node.y == node.y:
                if node < current_node:
                    return Frontier.IS_LOWER
                elif node > current_node:
                    return Frontier.IS_LARGER
                else:
                    return Frontier.IS_EQUAL
            else:
                return Frontier.NOT_IN

    def in_closed(self, node):
        for current_node in range(len(self.frontier)):
            if self.closed[current_node].x == node.x and self.closed[current_node].y == node.y:
                return current_node
        return False

    def search_closestmanhattan(self):
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
            return move_shortest
        else:
            return random.choice(moves)

    def valid_child(self, x, y):
        if x < 0 or x > 24 or y < 0 or y > 24 or self.board[x][y] == GameObject.WALL or self.board[x][y] == GameObject.SNAKE_BODY:
            return False
        else:
            return True

    def check_valid(self, x, y , direction):
        """ used by searchmanhattandistance
            :param direction: gives a move, move.straight, move.left or move.left"""
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

    def hypothetical_new_location(self, x, y, direc, mov):
        """:param direc indicates the hypothetical direction for the snake eg move.STRAIGHT"""
        new_direction = direc.get_new_direction(mov)
        manip = new_direction.get_xy_manipulation()
        x = x + manip[0]
        y = y + manip[1]
        return x, y, new_direction

    def new_location(self, direc):
        """:param direc indicates the hypothetical direction for the snake eg move.STRAIGHT"""
        new_direction = self.lastdirection.get_new_direction(direc)
        manip = new_direction.get_xy_manipulation()
        x = self.head_pos[0] + manip[0]
        y = self.head_pos[1] + manip[1]
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
        if (self.board[x][y] == GameObject.FOOD) or (self.board[x][y] == GameObject.EMPTY) or (self.board[x][y] == GameObject.SNAKE_HEAD):
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

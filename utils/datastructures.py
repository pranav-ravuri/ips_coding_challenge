from enum import IntEnum
from enum import auto
from utils import utils

class Directions(IntEnum):
    """
    Enum for storing Directions to make the code a little readable
    """
    UP = auto()
    DOWN = auto()
    LEFT = auto()
    RIGHT = auto()
    FORWARD = auto()
    BACKWARD = auto()

class Env():
    """
    A standard data structre to store the environment information
    Current this class does not store the path information, just the environment
    """
    def __init__(self, data, step_dist):
        self.description: str = str(data['description'])
        self.cube_width: float = float(data['cube_width'])
        self.step_dist: float = step_dist
        self.start_position: list = list(data['start_position'])
        self.goal_position: list = list(data['goal_position'])
        self.cube_positions: list = list(data['cube_positions'])
        self.domain_lower_corner: list = list(data['domain_lower_corner'])
        self.domain_upper_corner: list = list(data['domain_upper_corner'])



class Node(object):
    """
    A standard Class for storing node information, calculating cost etc
    """
    def __init__(self, env: Env, use_obs_cost, parent = None, cost_from_start: float = 0.0, approach_direction: Directions = 0, pos = 0):
        self.env = env
        self.parent = parent
        self.child = None
        self.is_dead_end = False
        if pos == 0:
            pos = env.start_position
        self.pos = pos
        self.cost_from_start = cost_from_start
        self.approach_direction = approach_direction
        self.resellection_cost = 0
        self.hash = hash((self.pos[0], self.pos[1], self.pos[2]))
        if use_obs_cost:
            self.compute_obstacle_cost()
        else:
            self.obs_cost = 0
        self.compute_cost(cost_from_start)

    def compute_cost(self, cost_from_start):
        self.cost = self.obs_cost + cost_from_start + utils.euic_distance(self.pos, self.env.goal_position) + self.env.step_dist + self.resellection_cost

    def set_resellection_cost(self, cost):
        """
        Cost if the same node is being visited again and again
        """

        self.resellection_cost = cost
        self.cost = self.obs_cost + self.cost_from_start + utils.euic_distance(self.pos, self.env.goal_position) + self.env.step_dist + self.resellection_cost

    def compute_obstacle_cost(self):
        """
        calculate sum of 1/distance from all the obstacle infront of the cube
        """
        self.obs_cost = 0
        for cube_pos in self.env.cube_positions:
            if (self.pos[0] < cube_pos[0]) and (self.pos[1] < cube_pos[1]) and (self.pos[2] < cube_pos[2]):
                self.obs_cost = self.obs_cost + 1/utils.euic_distance(self.pos, cube_pos)
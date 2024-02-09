import math

def euic_distance(p1: list, p2: list):
    """
    Compute Euclidian Distance between two 3D points
    
    Parameters:
    - p1: point 1 in (x, y, z) sequence
    - p2: point 2 in (x, y, z) sequence
    """
    return math.sqrt((p2[0] - p1[0])**2 + (p2[1] - p1[1])**2 + (p2[2] - p1[2])**2)

def check_collition(curr_pos: list, env):
        """
        returns True if there is collition, computed using sphere equation
        """
        for cube_center in env.cube_positions:
            if ((curr_pos[0] - cube_center[0])**2 + (curr_pos[1] - cube_center[1])**2 + (curr_pos[2] - cube_center[2])**2) - (env.cube_width ** 2) <= 0:
                return True
        return False
    
def boundary_check(curr_pos: list, env):
    ret = True
    if curr_pos[0] - env.cube_width/2 <= env.domain_lower_corner[0]:
        ret = False
    if curr_pos[1] - env.cube_width/2 <= env.domain_lower_corner[1]:
        ret = False
    if curr_pos[2] - env.cube_width/2 <= env.domain_lower_corner[2]:
        ret = False
    if curr_pos[0] + env.cube_width/2 >= env.domain_upper_corner[0]:
        ret = False
    if curr_pos[1] + env.cube_width/2 >= env.domain_upper_corner[1]:
        ret = False
    if curr_pos[2] + env.cube_width/2 >= env.domain_upper_corner[2]:
        ret = False
    return ret
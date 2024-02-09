from utils.datastructures import Env, Node, Directions
from utils.utils import euic_distance, check_collition, boundary_check

class Search():
    def __init__(self, env, fig, ax, live_update, use_obs_cost) -> None:
        """
        env: dict to represent the environment
        fig: matplotlib fig
        ax: subplot axes
        live_update: set True to draw the current path
        use_obs_cost: set True to include obstace cost
        """
        self.env: Env = env
        self.fig = fig
        self.ax = ax
        self.node_lookup = dict()
        self.use_obs_cost = use_obs_cost
        start_node = Node(env, self.use_obs_cost)
        self.live_update = live_update

        # initialise
        self.node_lookup[start_node.hash] = start_node
        self.path_reset()

        self.sc = ax.scatter(self.plot_xvals, self.plot_yvals, self.plot_zvals)

    def start(self):
        """
        starts searching
          1. Finds the node with the least cost
          2. Finds new nodes that are rechable from previous node
          3. 
        """
        max_tries = 100000
        path_found = False
        while(max_tries):
            print("Number of nodes discovered: ", len(self.node_lookup))
            max_tries = max_tries - 1
            node = self.find_best_node()
            print(node.hash, node.cost)
            new_node_list: list = self.find_next_nodes(node)

            # adding new nodes to the lookup table
            for node in new_node_list:
                if (node.hash in self.node_lookup) and (node.cost < self.node_lookup[node.hash].cost):
                    if self.node_lookup[node.hash].parent != node.parent:
                        self.node_lookup[node.hash] = node
                elif (node.hash not in self.node_lookup):
                    self.node_lookup[node.hash] = node
                else:
                    continue
                
                # check is we reached the goal
                if euic_distance(node.pos, self.env.goal_position) <= self.env.step_dist:
                    print("Path Found, in ", 10000000 - max_tries)
                    path_found = True
                    self.draw_path(node)
                    # to break the loop
                    max_tries = 0
                    break
        if not path_found:
            print("Path not found!!")
    
    def find_best_node(self):
        """
        Finds the node that has the least cost and the one that is not a dead end
        basically sort the node_lookup dict and pick the first node that is not a dead end
        """
        self.node_lookup = dict(sorted(self.node_lookup.items(), key=lambda item: item[1].cost))
        for i in range(10):
            hash, node = next(iter(self.node_lookup.items()))
            if not node.is_dead_end:
                node.set_resellection_cost(node.resellection_cost + 0.1)
                if self.live_update:
                    self.draw_path(node)
                return node
            print("Complete Dead End")

            
    def draw_path(self, node):
        # draw the path
        self.path_reset()
        while(1):
            if node == None:
                break
            self.plot_xvals.append(node.pos[0])
            self.plot_yvals.append(node.pos[1])
            self.plot_zvals.append(node.pos[2])
            node = node.parent
        self.sc._offsets3d = (self.plot_xvals, self.plot_yvals, self.plot_zvals)
        self.fig.canvas.draw()
        # to flush the GUI events
        self.fig.canvas.flush_events()

    def find_next_nodes(self, node: Node):
        """
        move in every possible direction and return the new node positions
        """
        available = list()
        # Check the 6 available diections but skip the direction that was used to reach the current node, 
        # as you will just get the parent
        for direction in Directions:
            if direction == Directions.UP and node.approach_direction != Directions.DOWN:
                new_pos = [node.pos[0], node.pos[1], node.pos[2] + node.env.step_dist]
            elif direction == Directions.DOWN and node.approach_direction != Directions.UP:
                new_pos = [node.pos[0], node.pos[1], node.pos[2] - node.env.step_dist]
            elif direction == Directions.LEFT and node.approach_direction != Directions.RIGHT:
                new_pos = [node.pos[0], node.pos[1] + node.env.step_dist, node.pos[2]]
            elif direction == Directions.RIGHT and node.approach_direction != Directions.LEFT:
                new_pos = [node.pos[0], node.pos[1] - node.env.step_dist, node.pos[2]]
            elif direction == Directions.FORWARD and node.approach_direction != Directions.BACKWARD:
                new_pos = [node.pos[0] + node.env.step_dist, node.pos[1], node.pos[2]]
            elif direction == Directions.BACKWARD and node.approach_direction != Directions.FORWARD:
                new_pos = [node.pos[0] - node.env.step_dist, node.pos[1], node.pos[2]]
            else:
                continue
            #check whether node is inside the frame
            # and it is not obstacle
            if (not boundary_check(new_pos, self.env)) or check_collition(new_pos, self.env):
                # print("OverStep or exist same loc")
                continue
            new_hash = hash((new_pos[0], new_pos[1], new_pos[2]))
            if new_hash not in self.node_lookup:
                n = Node(node.env, self.use_obs_cost, node, node.cost_from_start, direction, new_pos)
            else:
                n: Node = self.node_lookup[new_hash]
                n.compute_cost(node.cost_from_start)
            available.append(n)


        if len(available) == 0:
            self.is_dead_end = True
        return available
    
    def path_reset(self):
        self.plot_xvals = []
        self.plot_yvals = []
        self.plot_zvals = []

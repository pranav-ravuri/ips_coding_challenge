import json
from utils import visualize, datastructures
from grid_search import Search
import matplotlib.pyplot as plt

# Patameters to set
file_name = 'data/task.json'
use_obs_cost = True
live_update = True

# Read the JSON file
with open(file_name) as json_file:
    data = json.load(json_file)
    env = datastructures.Env(data, step_dist=0.1)

if live_update:
    plt.ion()
fig, ax = visualize.plot(env)
alg = Search(env, fig, ax, live_update=live_update, use_obs_cost = use_obs_cost)
alg.start()
plt.ioff()
plt.show()



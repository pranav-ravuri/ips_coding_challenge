import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
import json
from utils.datastructures import Env


def plot(env: Env):
    """
    Make the initial base plot of start cube and obstacles
    
    Parameters:
    - env: env configuration
    """
    
    # Print the accessed elements
    print("description:", env.description)

    fig, ax = plot_init(env.domain_lower_corner, env.domain_upper_corner)
    # Define the vertices of the cube
    draw_cubes(env.cube_positions, env.cube_width, env.start_position, ax)
    
    # Plot the point
    ax.scatter(env.start_position[0], env.start_position[1], env.start_position[2], color='g', marker='o')
    ax.scatter(env.goal_position[0], env.goal_position[1], env.goal_position[2], color='b', marker='x')
    return fig, ax


def plot_init(domain_lower_corner, domain_upper_corner):
    """
    Initialise and set plot limits
    """
    fig = plt.figure()
    ax = fig.add_subplot(111, projection='3d')
    ax.set_box_aspect([1,1,1])
    ax.set_xlabel('X')
    ax.set_ylabel('Y')
    ax.set_zlabel('Z')

    ax.set_xlim(domain_lower_corner[0], domain_upper_corner[0])
    ax.set_ylim(domain_lower_corner[1], domain_upper_corner[1])
    ax.set_zlim(domain_lower_corner[2], domain_upper_corner[2])
    return fig, ax

def draw_cubes(cube_positions, cube_width, start_position, ax):
    """
    Draws cubes in the 3D plot according to the given configuration
    
    Parameters:
    - cube_positions: List of Tuples (x, y, z) representing the center of the cube.
    - cube_width: Width of the cube.
    - start_position: Position of start cube
    - ax: Matplotlib axes
    """
    for i in range(len(cube_positions) + 1):
        if i == len(cube_positions):
            vertices = cube_vertices(start_position, cube_width)
            color = 'green'
        else:
            vertices = cube_vertices(cube_positions[i], cube_width)
            color = 'red'

        # Define the faces of the cube
        faces = [[vertices[0], vertices[1], vertices[2], vertices[3]],
                [vertices[1], vertices[5], vertices[6], vertices[2]],
                [vertices[5], vertices[4], vertices[7], vertices[6]],
                [vertices[4], vertices[0], vertices[3], vertices[7]],
                [vertices[0], vertices[4], vertices[5], vertices[1]],
                [vertices[3], vertices[2], vertices[6], vertices[7]]]

        cube = Poly3DCollection(faces, facecolors=color, edgecolors='k', alpha=0.5)
        ax.add_collection3d(cube)

    # draw the start cube as well
    start_position

def cube_vertices(center, width):
    """
    Generate the vertices of a cube given its center and width.
    
    Parameters:
    - center: Tuple (x, y, z) representing the center of the cube.
    - width: Width of the cube.
    
    Returns:
    A list of tuples representing the vertices of the cube.
    """
    x, y, z = center
    half_width = width / 2.0
    
    vertices = [
        [x - half_width, y - half_width, z - half_width],  # Vertex 0
        [x + half_width, y - half_width, z - half_width],  # Vertex 1
        [x + half_width, y + half_width, z - half_width],  # Vertex 2
        [x - half_width, y + half_width, z - half_width],  # Vertex 3
        [x - half_width, y - half_width, z + half_width],  # Vertex 4
        [x + half_width, y - half_width, z + half_width],  # Vertex 5
        [x + half_width, y + half_width, z + half_width],  # Vertex 6
        [x - half_width, y + half_width, z + half_width]   # Vertex 7
    ]
    
    return vertices

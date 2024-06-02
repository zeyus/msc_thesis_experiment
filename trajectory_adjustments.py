# -*- coding: utf-8 -*-
"""
Created on Thu Jan 11 13:53:48 2024

@author: kathr
"""
from human_mouse_trajectory import HumanizeMouseTrajectory
import random
import numpy as np
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

position_list = [(500, 400), (-500, 400)]
move = 70
possible_end_pos = [[-320, 210-move],[0,440-move],[320, 210-move],[200, -180-move],[-200, -180-move]]
trajectories = []

for i in range(10):
    end_index = random.randint(0,4)
    
    
    partner_pos = position_list[0]
    loner_pos = position_list[1]
    
    end_pos = possible_end_pos[end_index]
    
    if end_index > 2:
        start_pos = loner_pos[0], loner_pos[1]-50
    else:
        start_pos = partner_pos[0], partner_pos[1]-50
    
    distance = np.linalg.norm(np.array(start_pos)-np.array(end_pos))
    
    num_sec = distance/1000 + 0.2 + 0.8*np.random.rand()
    num_frames = round(61*num_sec)
    
    trajectory = HumanizeMouseTrajectory(start_pos,
                                         end_pos, 
                                         offset_boundary_x = 10,
                                         offset_boundary_y = 10,
                                         distortion_mean = 0.0, #1.2, 
                                         distortion_st_dev = 0.5, #1.2, 
                                         distortion_frequency = 1, 
                                         target_points = num_frames,
                                         knots_count = 1)
    
    trajectories.append(trajectory.points)

# Set up the plot
fig, ax = plt.subplots()

# Set the axis limits
min_x = min(min(x for x, y in traj) for traj in trajectories)
max_x = max(max(x for x, y in traj) for traj in trajectories)
min_y = min(min(y for x, y in traj) for traj in trajectories)
max_y = max(max(y for x, y in traj) for traj in trajectories)

ax.set_xlim(min_x, max_x)
ax.set_ylim(min_y, max_y)

# Define a list of colors for each trajectory
colors = ['b', 'g', 'r', 'c', 'm', 'y', 'k']

# Function to initialize the plot
def init():
    return []

# Function to update the position of the dot in each animation frame
def update(frame):
    ax.clear()  # Clear the previous plot
    for i in range(frame + 1):
        current_trajectory = trajectories[i]
        x_values, y_values = zip(*current_trajectory)
        ax.plot(x_values, y_values, marker='o', linestyle='-', color=colors[i % len(colors)])
    ax.set_title(f'Trajectories up to frame {frame + 1}')
    ax.set_xlabel('X-axis')
    ax.set_ylabel('Y-axis')
    ax.grid(True)
    return []

# Calculate the interval for 61 FPS
fps = 61
interval = 1000 / fps

# Calculate the total number of frames needed for all trajectories
total_frames = max(len(traj) for traj in trajectories)

# Create an animation
animation = FuncAnimation(fig, update, frames=total_frames, init_func=init, repeat=False, interval=interval)

# Show the animation
plt.show()
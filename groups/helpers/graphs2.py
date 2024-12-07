from vpython import *
from time import *


# Create a sphere representing a point
point = sphere(pos=vector(0, 0, 0), radius=0.1, color=color.red)

# Function to handle mouse drag
def move_point(evt):
    # evt.pos is the position of the mouse in 3D space when clicked
    point.pos = evt.pos

# Enable mouse drag events
scene.bind('mousemove', move_point)

# Keeps the scene running and responsive
while True:
    rate(160)



"""
pos = vp.vector(x,y,z)

box == length width height
cylinder with radius and length


curve is important: This can be used to create a list of lines connecting dots, 
Label to write the names of the elements
points could be better than spheres for network graphs

create an n-gon with compound types
color = vp.color.(whatever color)
"""
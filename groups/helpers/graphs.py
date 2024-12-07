from functools import cache
from math import pi, sin, cos, sqrt



@cache
def circle(numbers,
           radius=1):
    points = []
    r = sqrt(radius)
    for i in range(1,numbers+1):
        points.append([r*sin(2*i*pi/numbers), r*cos(2*i*pi/numbers),0])
    return points

def rotation_matrix_x(angle):
    return [[1, 0, 0], [0, cos(angle), -sin(angle)], [0, sin(angle), cos(angle)]]

def rotation_matrix_y(angle):
    return [[cos(angle), 0, sin(angle)], [0, 1, 0], [-sin(angle), 0, cos(angle)]]

def rotation_matrix_z(angle):
    return [[cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]]

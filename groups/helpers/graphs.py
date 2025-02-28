from functools import cache
from math import e, pi, sin, cos, sqrt
import numpy as np

@cache
def circle(numbers,
           radius=1):
    points = []
    r = sqrt(radius)
    for i in range(1,numbers+1):
        points.append([round(r*sin(2*i*pi/numbers),5),round(r*cos(2*i*pi/numbers),5),0])
    return points

x = lambda angle:  [[1, 0, 0], [0, cos(angle), -sin(angle)], [0, sin(angle), cos(angle)]]

y = lambda angle : [[cos(angle), 0, sin(angle)], [0, 1, 0], [-sin(angle), 0, cos(angle)]]

z = lambda angle: [[cos(angle), -sin(angle), 0], [sin(angle), cos(angle), 0], [0, 0, 1]]

def mult(a,b):
    return np.round((np.matrix(a)@np.matrix(b).T),5).tolist()

def sphere(Npoints:int,
           cosets:int):
    points = [i for i in circle(Npoints)]
    init = points.copy()
    for i in range(1,cosets):                   
        for j in mult(init,x(2*pi*i/cosets)):
            points.append(j)        
    return points

        
if __name__=='__main__':

    k = sphere(5,5)
    for i in k:
        for j in i:
            print(tuple(j),end=',')
        print()
from functools import cache
from math import pi, sin, cos, sqrt
from numpy import matrix, size, shape


def sub(x:list,
        y:list):
    return [[i-j for i,j in zip(a,b)] for a,b in zip(x,y)]

def add(x:list,
        y:list):
    return [[i+j for i,j in zip(a,b)] for a,b in zip(x,y)]

def optimal_matrix_mult(x:list,
                        y:list):
    """
    Computes matrix product by divide and conquer approach, recursively.
    Input: nxn matrices x and y
    Output: nxn matrix, product of x and y
    """
    # Base case when size of matrices is 1x1
    if len(x) == 1:
        # Handle both nested and non-nested lists
        x_val = x[0][0] if isinstance(x[0], list) else x[0]
        y_val = y[0][0] if isinstance(y[0], list) else y[0]
        return [[x_val * y_val]]
    
    # Splitting the matrices into quarters.
    n = len(x)
    mid = n // 2
    
    # Splitting the matrices into quarters.
    a, b, c, d = x[:mid][:mid], x[:mid][mid:], x[mid:][:mid], x[mid:][mid:]
    e, f, g, h = y[:mid][:mid], y[:mid][mid:], y[mid:][:mid], y[mid:][mid:]
    
    print(a,b,c,d)

    # Using the seven multiplications to compute the product value
    p1 = optimal_matrix_mult(a, sub(f,h))
    p2 = optimal_matrix_mult(add(a, b), h)
    p3 = optimal_matrix_mult(add(c ,d), e)
    p4 = optimal_matrix_mult(d, sub(g, e))
    p5 = optimal_matrix_mult(add(a, d), add(e, h))
    p6 = optimal_matrix_mult(sub(b, d), add(g, h))
    p7 = optimal_matrix_mult(sub(a, c), add(e ,f))
    
    # Calculating the values of the 4 quarters of the final matrix c
    c11 = p5 + p4 - p2 + p6
    c12 = p1 + p2
    c21 = p3 + p4
    c22 = p5 + p1 - p3 - p7
    
    # Combining the 4 quarters into a single matrix by using list comprehension
    c = [c11[i] + c12[i] for i in range(mid)] + [c21[i] + c22[i] for i in range(mid)]
    
    return c



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



def sphere(circle,
           cosets):
    points = []
    for i in cosets:
        ...


if __name__=='__main__':
    c = circle(5)
    print(optimal_matrix_mult(c,rotation_matrix_z(45)))
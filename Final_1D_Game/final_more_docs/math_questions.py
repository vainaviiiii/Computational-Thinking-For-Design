import math
import numpy as np
import matplotlib.pyplot as plt

# ===== Math helper functions: Basic modular functions ===== 

def permutation(n,r):
    if n < r:
        return 0
    p= math.factorial(n)/(math.factorial(n-r))
    return round(p)

def combination(n,r):
    if n < r:
        return 0
    c=math.factorial(n)/(math.factorial(r)*math.factorial(n-r))
    return round(c)

# ===== Derivative questions: Vitaly ===== 

def deriv_1(power):
    """ What is the derivative of x to power {}? """
    return f"{power}x^{round(power-1, 2)}"
            
def deriv_2(num):
    return "1/x"
    
def deriv_3(power_e):
    """ What is the derivative of e^({}x)? """
    return f"{power_e}e^({power_e}x)"
    
def deriv_4(integer1, integer2, power1):
    """ What is the derivative of ({}+{}x)^{}? """
    return f"{power1}*{integer2}*({integer1}+{integer2}x)^{power1 - 1}"
            
def deriv_5(integer1, power1):
    """ What is the derivative of sin({}x^{})? """
    return f"{power1}*{integer1}x^{power1 - 1}*cos({integer1}x^{power1})"

# ===== Geometry questions: Javier =====

def geom_1(length):
    """ What is the surface area of a cube of length {}?"""
    return round(length * 6, 2)

def geom_2(radius):
    """ What is the volume of half a sphere of radius {}?"""
    return round(2/3 * math.pi * radius ** 3, 2)

def geom_3(radius, height):
    """ What is the surface area of cylinder of radius {} and height {}?"""
    return round(2 * math.pi * height * radius + 2 * math.pi * radius ** 2, 2)

def geom_4(base_area, height):
    """ What is the volume of triangular prism of base area {}, and height of {}?"""
    return round(0.5 * base_area * height, 2)

def geom_5(height, first_side, second_side):
    """ What is the volume of trapezoid of sides {} and {} and height of {}?"""
    return round(0.5 * height * (first_side + second_side), 2)


# ===== Permutation and Combination questions: Nada =====

def pnc_1(previous):
    """ You are to pick a new 6-digit pin for your bank account and it can't be the same as your previous ones. You've had {} previous codes. How many different possible combinations are there? """
    answer = 10**6
    return answer-previous

def pnc_2(total, mingirls, boys, girls):
    """ A mixed team of total {} players containing a minimum of {} girls is to be chosen from a group of {} boys and {} girls. How many different teams can be picked? """
    minboys = total - mingirls
    return combination(boys, minboys) * combination(girls, mingirls)


def pnc_3(total, selected):
    """ If you have {total} books and want to arrange {selected} of them on a bookshelf, how many different ways can you do it? """
    return permutation(total,selected)

def pnc_4(oranges, apples, mangoes):
    """ There are {} oranges, {} apples and {} mangoes in a basket. In how many ways can a person select fruits among the fruits in the basket? """
    answer = 1
    for i in (oranges, apples, mangoes):
        answer *= i+1 
    return answer - 1

def pnc_5(number):
    """There are {number} students in a race. In how many different orders can they complete?"""
    return permutation(number,number)


# ===== Trigonometry questions: Reynard ===== 
# static questions are in json instead

def trigo_1(b, c, angle):
    """What is the length of side a of a triangle with other sides, b = {}, c = {}, and angle {}?"""
    return round(math.sqrt(b ** 2 + c ** 2 - 2 * b * c * math.cos(angle)), 2)

def trigo_2(b, B, A):
    "What is the length of side a of a triangle with side b = {}, with angles of A = {}, B = {}?"
    return round(b * (math.sin(A) / math.sin(B)), 2)

def trigo_3(a_b, A):
    "Find the area of an isoceles triangle ABC where a = b = {}, and angle A = {} rad. "
    return round(0.5 * a_b * a_b * math.sin(math.pi - (2 * A)), 2)

def trigo_4(a, b):
    "If sin(A) = a/b (a fraction), then what is the value of sin(90-A)?"
    return round(math.sqrt(b ** 2 - a ** 2) / b, 2)

def trigo_5(b, a):
    "Find the area of a triangle with one of the angles being cos(A) = b/a"
    return round(0.5 * b * (math.sqrt(a ** 2 - b ** 2)), 2)


# ===== Vector questions: Vainavi =====
# question 1i and 1ii is static
def vector_1(x_1, y_1, x_2, y_2):
    """Given OA = ({}, {}) and OB = ({}, {}). What is Vector BA?\nHint: Vector OA (RED), Vector OB (BLUE), Vector BA (BLACK)"""
    
    # Setup vectors in array and plot in quiver
    V = np.array([ [x_1,y_1], [x_2,y_2] ])
    origin = np.array([[0, 0],[0, 0]])
    plt.quiver(*origin, V[:,0], V[:,1], color=['r','b','g'], angles='xy', scale_units='xy', scale=1)

    # Setup resultant vector
    v12 = V[0] - V[1] # edit this to check resultant
    plt.quiver(*origin, v12[0], v12[1], angles='xy', scale_units='xy', scale=1)
    
    # Plot graph
    plt.xlim([-25,25])
    plt.ylim([-25,25])

    return str((x_1 - x_2, y_1 - y_2))


def vector_2(n_7, n_8, n_9, n_10):
    #Print the Question and ask for input
    """Given vector U = ({}, {}) and vector V = ({}, {}). What is U + V?"""
    return str((n_7 + n_9, n_8 + n_10))


def vector_3(n_11, n_12, n_13):
    """Given vector N is ({}, {}) and vector M is the scalar multiple of Vector N by {}. What is vector M? """ 
    return str((n_13 * n_11, n_13 * n_12))

def vector_4(n_14, n_15):
    """Given Vector P is ({}, {}). Find the modulus of Vector P. Round off your answer to 2 decimal places."""
    return round(math.sqrt(n_14 ** 2 + n_15 ** 2), 2)


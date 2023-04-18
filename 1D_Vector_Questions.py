#!/usr/bin/env python
# coding: utf-8

# In[ ]:


## Question 1 -> Normal vector question

def question_1():
    ans_1_i = input("Difference between Vector and Scalar: \n(i) Is distance a (a)Vector or (b)Scalar? Select a or b. ")
    ans_1_ii = input("Is displacement a (a)Vector or (b)Scalar? Select a or b. ")
    if((ans_1_i == ('b' or 'B')) and (ans_1_ii == ('a' or 'A'))):
        return True
    else:
        return False

## Question 2 -> Position vector

import numpy as np
import matplotlib.pyplot as plt

def question_2():
    n = random.randint(0,20)
    n_1 = random.randint(0,20)
    n_2 = random.randint(0,20)
    n_3 = random.randint(0,20)
    n_4 = random.randint(0,20)
    n_5 = random.randint(0,20)
    V = np.array([[n,n_1], [n_2,n_3], [n_4,n_5]])
    origin = np.array([[0, 0, 0],[0, 0, 0]])
    plt.quiver(*origin, V[:,0], V[:,1], color=['r','b','g'], scale=100)
    v12 = V[0] + V[1] # adding up the 1st (red) and 2nd (blue) vectors
    plt.quiver(*origin, v12[0], v12[1])
    plt.show()
    message_1 = print("OA = ({}, {}) and OB = ({}, {}). Vector AB = (_M_, _N_). ".format(n, n_1, n_2, n_3))
    ans_1_i = input("M = ")
    ans_1_ii = input("N = ")
    if ((ans_1_i == (-n+n_2)) and (ans_1_ii == (-n_1+n_3))):
        return True
    else:
        return False

## Question 3 -> Addition of Column Vectors

import random

def question_3():
    n_7 = random.randint(0,20)
    n_8 = random.randint(0,20)
    n_9 = random.randint(0,20)
    n_10 = random.randint(0,20)
    message_3 = "Vector U = ({}, {}) and Vector V = ({}, {}). U + V = (_A_, _B_).".format(n_7, n_8, n_9, n_10)
    qns_3 = print(message_3)
    ans_3_a = int(input("A = ")) 
    ans_3_b = int(input("B = "))
    if((ans_3_a == n_7 + n_9) and (ans_3_b == n_8 + n_10)):
        return True 
    else:
        return False
    
## Question 4 -> Scalar Multiplication of Column Vectors

def question_4():
    n_11 = random.randint(0,20)
    n_12 = random.randint(0,20)
    n_13 = random.randint(0,20)
    message_4 = "Vector N = ({}, {}). Vector M is the scalar nultiple of Vector N by {}? Vector M = (_A_, _B_).".format(n_11, n_12, n_13)
    qns_4 = print(message_4)
    ans_4_a = int(input("A = ")) 
    ans_4_b = int(input("B = "))
    if((ans_4_a == n_13*n_11) and (ans_4_b == n_13*n_12)):
        return True 
    else:
        return False
    
## Question 5 -> Modulus of Column Vectors

import random
from math import *

def question_5():
    n_14 = random.randint(0,20)
    n_15 = random.randint(0,20)
    qn_5 = print("Vector P = ({}, {}). Find the Modulus of Vector P. Round off your answer to 3 decimal places.".format (n_14, n_15))
    ans_5 = round((float(input("Your Answer: "))), 3)
    correct_ans = sqrt(n_14**2 + n_15**2)
    if(ans_5 == round(correct_ans,3)):
        return True 
    else:
        return False
    
print(question_1())
print(question_2())
print(question_3())
print(question_4())
print(question_5())


# In[ ]:





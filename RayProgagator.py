# -*- coding: utf-8 -*-
"""
Created on Fri Sep 24 08:57:28 2021

@author: ryan.robinson
"""

import numpy as np
import matplotlib.pyplot as plt
from sympy import symbols, Eq
import tkinter as tk

from sympy.solvers import solve
from sympy import tan
from sympy import Symbol

n_air = 1.0

def main():
    n_fsilica = 1.4658

    # Create ray object
    R1 = Ray(1,0)
    
    # Define lens properties
    radius = 77.172
    thickness = 12.5
    
    # Create lens object
    L1 = ThickLens(radius, np.inf, thickness)
    
    # Create symbol for focal length
    fl = Symbol('f1')
    
    # Create distance object with focal length parameter
    P1 = Prop(fl)
    
    # Multiply objects
    Total = P1*L1*R1
    
    # Get the expression for the ray height
    H = Total.getHeight()
    
    # Solve for ray height equal to zero, guess it's the first result
    sol = solve(H, fl)[0]
    
    # Print results
    print("Back focal length: {}".format(sol))
    print("Front focal length: {}".format(sol+thickness))

    return



        

class ABCD():
    def __init__(self,A):
        self.M = np.array(A)
        return
    
    def __mul__(self,other):
        return ABCD(np.matmul(self.M,other.M))        
        
    def __str__(self):
        return str(self.M)
    
    def getHeight(self):
        return self.M[0,0]

class Ray(ABCD):
    def __init__(self,x,theta):
        ABCD.__init__(self,[[x],[theta]])
        return
    
class ThinLens(ABCD):
    def __init__(self,f):
        A = 1.0
        B = 0.0
        C = -1/f
        D = 1.0
        ABCD.__init__(self,[[A,B],[C,D]]) 
        return
        
class Prop(ABCD):
    def __init__(self,d):
        A = 1.0
        B = d
        C = 0.0
        D = 1.0
        ABCD.__init__(self,[[A,B],[C,D]])
        return

class CurvedSurf(ABCD):
    def __init__(self,r,n1=1.0,n2=1.45):
        A = 1
        B = 0
        C = (n1 - n2) / (r * n2)
        D = n1/n2
        ABCD.__init__(self,[[A,B],[C,D]])
        return

class ThickLens(ABCD):
    def __init__(self,r1,r2,t,n1 = 1.0, n2 = 1.45):
        M1 = CurvedSurf(r1,n1,n2)
        M2 = Prop(t)
        M3 = CurvedSurf(r2,n2,n1)
        M = M3 * M2 * M1
        ABCD.__init__(self,M.M)

if __name__=="__main__":
    main()
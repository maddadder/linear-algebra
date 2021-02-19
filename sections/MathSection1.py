import sys
sys.path.append('..')
from MyTypes import MathSection
import numpy as np
from tkinter import * 
from PIL import Image, ImageTk
import numpy
import sympy as sp
from io import BytesIO

class MathSection1:
    def __init__(self, parent):
        self.parent = parent

    def getData(self):
        d: Dict[str, Point] = dict()
        d["i_origin"] = (1,0,0)
        d["j_origin"] = (0,1,0)
        d["k_origin"] = (0,0,1)
        d["i_vector"] = np.array((1, 1, 0))
        d["j_vector"] = np.array((0, 1, 1))
        d["k_vector"] = d["i_vector"] + d["j_vector"]
        d["i_plus_vector"] = np.array((0, 0, 0))
        d["j_plus_vector"] = np.array((0, 0, 0))
        d["k_plus_vector"] = np.array((0, 0, 0))
        return d

    def getMathSection(self):
        
        self.ui = MathSection(self.parent, self.getData())
        
        return self

    def getContent(self):
        self.text1 = 'Linear combination: cv + dw = c(1,1) + d(2,3) = (c + 2d, c + 3d) \n' \
            'Example: v + w = (1,1) + (2,3) = (3,4) is the combination with c = d = 1\n' \
            'The vectors cv line along a line. When w is not on that line, the combinations\n' \
            'cv + dw fill the whole two-dimensional plane.\n\n' \
            'Problem Set 1.1: A The linear combinations of v = (1,1,0) and w = (0,1,1) fill a plane in R^3.\n' \
            'Descibe that plane. Find a vector that is not a combination of v and w -- not on the plane\n\n' \
            'Solution: The plane of v and w contains all combinations cv + dw. The vectors in that \n' \
            'plane allow any c and d. The plane appears in Figure 1.3 when you slide the Transform \n' \
            'slider down. Use the Elevation and Angle sliders to get a better view.\n\n' \
            'Combinations cv + dw = c(1,1,0) + d(0,1,1) = (c, c + d, d) fill a plane.\n\n' \
            'Four vectors in that plane are (0,0,0) and (2,3,1) and (5,7,2) and (pi,2pi,pi).\n' \
            'The second component c + d is always the sum of the first and third components.\n' \
            'Like most vectors, (1,2,3) is NOT in the plane, because 2 != 1 + 3.\n' \
            'Another description of this plane through (0,0,0) is to know that n = (1,-1,1) is\n' \
            'perpendicular to the plane. We can confirm that 90 degree angle by testing dot products\n' \
            'v * n = 0 and w * n = 0.  Perpendicular vectors have zero dot products.\n' \
            '\nFigure 1.3'

        
        return self.text1
        
    
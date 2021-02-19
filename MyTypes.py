from typing import List
from tkinter import * 
import numpy as np
from matplotlib.backends.backend_tkagg import (FigureCanvasTkAgg,  NavigationToolbar2Tk) 
import sympy as sp
from io import BytesIO
from PIL import Image, ImageTk
from pylatex import Document, Section, Subsection, Math, Matrix, VectorName, Package
Vector = List[float]

class Point:
    def __init__(self, vector:Vector):
        self.vector = vector

class MathSection:
    def __init__(self, parent, d:dict):
        self.parent = parent
        self.d = d
        self.canvasFigure = None
    def on_latex(self):
        expr = "$\displaystyle " + 'test' + "$"

        #This creates a ByteIO stream and saves there the output of sympy.preview
        f = BytesIO()
        the_color = "{" + self.parent.window.cget('bg')[1:].upper()+"}"
        sp.preview(expr, euler = False, preamble = self.strvar.get(),
                   viewer = "BytesIO", output = "ps", outputbuffer=f)
        f.seek(0)
        #Open the image as if it were a file. This works only for .ps!
        img = Image.open(f)
        #See note at the bottom
        img.load(scale = 2)
        #img = img.resize((int(img.size[0]/2),int(img.size[1]/2)),Image.BILINEAR)
        photo = ImageTk.PhotoImage(img)
        self.label.config(image = photo)
        self.label.image = photo
        f.close()
    def addCanvas(self):
        #self.canvas = self.parent.window #remove this and fix
        self.frame1=Frame(self.parent.window,bg='#FFFFFF',width=200,height=200)
        self.frame1.pack(expand=True, fill=BOTH, pady=50, side=TOP )
        self.strvar = StringVar()
        self.label = Label(self.parent.window)
        self.label.pack(side=TOP)
        #self.entry = Entry(self.parent.window, textvariable = self.strvar, width=200)
        #self.entry.pack(side=TOP)
        #self.button = Button(self.parent.window, text = "LaTeX!", command = self.on_latex)
        #self.button.pack(side=TOP)
        self.frame2=Frame(self.parent.window,bg='#FFFFFF',width=200,height=200)
        self.frame2.pack(expand=True, fill=BOTH, side=TOP)

        

    def addUI(self):
        self.transformSliderLabel = Label(self.frame2,bg='#FFFFFF',text='Transform')
        self.transformSliderLabel.config(font=('Arial', 14))
        self.transformSliderLabel.grid( row=0,column=1 )

        self.transformSlider = Scale(self.frame2, from_=0, to=self.parent.frames,
                tickinterval=1,  command = self.update, bg='#FFFFFF')
        self.transformSlider.grid( row=1,column=1 )
        

        self.elevationSliderLabel = Label(self.frame2, bg='#FFFFFF',text='Elevation')
        self.elevationSliderLabel.config(font=('Arial', 14))
        self.elevationSliderLabel.grid( row=0,column=2 )

        self.elevationSlider = Scale(self.frame2, from_=-180, to=180,
                tickinterval=1,  command = self.updateElevation, bg='#FFFFFF')
        self.elevationSlider.grid( row=1,column=2 )
        self.elevationSlider.set(0)

        self.angleSliderLabel = Label(self.frame2, bg='#FFFFFF',text='Angle')
        self.angleSliderLabel.config(font=('Arial', 14))
        self.angleSliderLabel.grid( row=0,column=3 )
        
        self.angleSlider = Scale(self.frame2, from_=180, to=-180,
                tickinterval=1,  command = self.updateAngle, bg='#FFFFFF', orient=HORIZONTAL)
        self.angleSlider.grid( row=1,column=3 )
        self.angleSlider.set(0)

        

        self.distanceSliderLabel = Label(self.frame2, bg='#FFFFFF',text='Distance')
        self.distanceSliderLabel.config(font=('Arial', 14))
        self.distanceSliderLabel.grid( row=0,column=4 )

        self.distanceSlider = Scale(self.frame2, from_=1, to=20,
                tickinterval=1,  command = self.updateDistance, bg='#FFFFFF')
        self.distanceSlider.grid( row=1,column=4 )
        self.distanceSlider.set(5)

        
        self.canvasFigure = FigureCanvasTkAgg(self.parent.figure, 
                               master = self.frame2)   
        
        self.canvasFigure.get_tk_widget().grid( row=2,column=1,columnspan=3 )
        #self.toolbar = NavigationToolbar2Tk(self.parent.window, 
                                   #self.parent.window) 
        #self.toolbar.update() 
        
        # placing the toolbar on the Tkinter window 
        #self.parent.window.get_tk_widget().pack() 
        
        self.canvasFigure.draw()
        self.is_hidden = False
        self.update(0)

    def updateDistance(self, i):
        i = int(i)
        self.parent.dist = i
        self.parent.ax.dist = self.parent.dist
        self.canvasFigure.draw()

    def updateElevation(self, i):
        i = int(i)
        self.parent.elevation = i
        self.parent.ax.view_init(self.parent.elevation, self.parent.angle)
        self.canvasFigure.draw()
    
    def updateAngle(self, i):
        i = int(i)
        self.parent.angle = i
        self.parent.ax.view_init(self.parent.elevation, self.parent.angle)
        self.canvasFigure.draw()

    def update(self, i):
        i = int(i)
        self.parent.matrix = np.array((self.parent.i_vector, self.parent.j_vector, self.parent.k_vector)).T
        self.parent.plus_matrix = np.array((self.parent.i_plus_vector, self.parent.j_plus_vector, self.parent.k_plus_vector)).T

        if self.canvasFigure != None:
            try:
                self.parent.quiver.remove()
                self.parent.plus_quiver.remove()
            except:
                print("do nothing")
            self.parent.matrix = (1 - self.parent.sigmoid(i)) * np.array((self.parent.i_origin, self.parent.j_origin, self.parent.k_origin)) + self.parent.sigmoid(i) * self.parent.matrix
            self.parent.plus_matrix = (1 - self.parent.sigmoid(i)) * np.array((self.parent.i_origin, self.parent.j_origin, self.parent.k_origin)) + self.parent.sigmoid(i) * self.parent.plus_matrix
        else:
            self.parent.matrix = np.array((self.parent.i_origin, self.parent.j_origin, self.parent.k_origin)) + self.parent.matrix
            self.parent.plus_matrix = np.array((self.parent.i_origin, self.parent.j_origin, self.parent.k_origin)) + self.parent.plus_matrix
        # Compute a matrix that is in the middle between the full transformation matrix and the identity


        self.parent.vector_location = np.array((self.parent.matrix.dot(self.parent.i_origin), self.parent.matrix.dot(self.parent.j_origin), self.parent.matrix.dot(self.parent.k_origin))).T
        self.parent.quiver = self.parent.ax.quiver(0, 0, 0, self.parent.vector_location[0], self.parent.vector_location[1], self.parent.vector_location[2], length=1, color='r', arrow_length_ratio=0.1)
        self.parent.plus_vector_location = np.array((self.parent.plus_matrix.dot(self.parent.i_origin), self.parent.plus_matrix.dot(self.parent.j_origin), self.parent.plus_matrix.dot(self.parent.k_origin))).T
        self.parent.plus_quiver = self.parent.ax.quiver(0, 0, 0, self.parent.plus_vector_location[0], self.parent.plus_vector_location[1], self.parent.plus_vector_location[2], length=1, color='y', arrow_length_ratio=0.1)
        # Set vector location - must transpose since we need U and V representing x and y components
        # of each vector respectively (without transposing, e  ach column represents each unit vector)
        self.parent.transform = np.array([self.parent.matrix.dot(k) for k in self.parent.x])
        
        #ax.view_init((1 - self.parent.sigmoid(i)) * elevation, (1 - self.parent.sigmoid(i)) * angle)
        if self.canvasFigure != None:
            self.parent.scat._offsets3d = [self.parent.transform[:, 0], self.parent.transform[:, 1], self.parent.transform[:, 2]]
            self.canvasFigure.draw()
            a = self.parent.plus_vector_location
            #with pylatex.config.active.change(indent=False):
            doc = Document()
            doc.packages.append(Package('geometry', options = ['paperwidth=6in','paperheight=2.5in']))
            section = Section('Linear Combination')

            subsection = Subsection('Using the dot product')
            V1 = np.transpose(np.array([[1,1]]))
            M1 = np.array((self.parent.i_vector, self.parent.j_vector)).T
            math = Math(data=[Matrix(M1), 'dot', Matrix(V1),'=', Matrix(np.dot(M1, V1))])
            subsection.append(math)
            section.append(subsection)

            subsection = Subsection('Using vector addition')
            V1 = np.array([self.parent.i_vector])
            V2 = np.array([self.parent.j_vector])
            math = Math(data=[Matrix(V1), '+', Matrix(V2),'=', Matrix(V1 + V2)])
            subsection.append(math)
            section.append(subsection)
            #doc.append(section)
            '''
            subsection = Subsection('Product')

            math = Math(data=['M', vec_name, '=', Matrix(M * a)])
            subsection.append(math)

            section.append(subsection)
            doc.append(section)
            '''
            doc.append(section)
            latex = doc.dumps_as_content()
            print(latex)
            self.strvar.set(latex)
            #self.strvar.set("\prod_{p\,\mathrm{prime}}\\frac1{1-p^{-s}} = \sum_{n=1}^\infty \\frac1{n^s}")
            self.on_latex()

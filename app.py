import scatterplot
from tkinter import * 
class GUI:
    def __init__(self):
        print('GUI __init__')
        # the main Tkinter window 
        self.window = Tk() 
        # dimensions of the main window 
        self.window.geometry("800x600") 
        # setting the title  
        self.window.title('Plotting in Tkinter') 
        
        self.canvas=Canvas(self.window,bg='#FFFFFF',width=800,height=600,scrollregion=(0,0,800,1000))
        self.frame=Frame(self.canvas,bg='#FFFFFF',width=800,height=600)
        self.frame.pack(expand=True, fill=BOTH) #.grid(row=0,column=0)


        self.hbar=Scrollbar(self.window,orient=HORIZONTAL)
        self.hbar.pack(side=BOTTOM,fill=X)
        self.hbar.config(command=self.canvas.xview)
        self.vbar=Scrollbar(self.window,orient=VERTICAL)
        self.vbar.pack(side=RIGHT,fill=Y)
        self.vbar.config(command=self.canvas.yview)
        self.canvas.config(xscrollcommand=self.hbar.set, yscrollcommand=self.vbar.set)
        self.canvas.pack(side=LEFT,expand=True,fill=BOTH)
        self.canvas.create_window((4,4), window=self.frame, anchor="nw",
                                  tags="self.frame")
        self.frame.bind("<Configure>", self.onFrameConfigure)
        
        self.label1 = Label(self.canvas, bg='#FFFFFF', text='Introduction to Linear Algebra')
        self.label1.config(font=('Arial', 20))
        self.label1.pack()

        self.scatterplot = scatterplot.ScatterPlot(self.frame)

    def onFrameConfigure(self, event):
        '''Reset the scroll region to encompass the inner frame'''
        self.canvas.configure(scrollregion=self.canvas.bbox("all"))

    def graph(self):
        #print('graph')
        #self.scatterplot.set_title("Some Title")
        self.scatterplot.show()

gui = GUI()
gui.graph()

# run the gui 
gui.window.mainloop() 
import tkinter as tk
from tkinter import colorchooser
from tkinter import ttk

#Find a way to place the canvas in one column while buttons stay the same

class PaintApp:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("Python Paint")

        self.last_two_mouse_pos = []
        self.color = "black"
        self.eraserOn = False

        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.myCanvas = tk.Canvas(self.root, bg="white", width=400, height=400, cursor="@pencil.cur")
        self.myCanvas.grid(row=0, column=1, sticky="nswe")

        self.buttonFrame = tk.Frame(self.root)
        self.buttonFrame.grid(row=0, column=0)

        self.colorButton = tk.Button(self.buttonFrame, text="Color", command=self.chooseColor)
        self.colorButton.grid(row=0, column=0)

        self.clearButton = tk.Button(self.buttonFrame, text="Clear", command=self.clearBoard)
        self.clearButton.grid(row=1, column=0)

        self.eraserButton = tk.Button(self.buttonFrame, text="Eraser", command=self.activateEraser)
        self.eraserButton.grid(row=2, column=0)

        self.brushButton = tk.Button(self.buttonFrame, text="Brush", relief=tk.SUNKEN, command=self.activateBrush)
        self.brushButton.grid(row=3, column=0)

        self.values = [2,4,8,10,12,14,16]
        self.thickness = ttk.Combobox(self.buttonFrame, values=self.values)
        self.thickness.current(0)
        self.thickness.grid(row=4, column=0)

        self.bindEvents()
        self.root.mainloop()

    def resetList(self,event):
        #If mouse button released reset list
        del self.last_two_mouse_pos[:]

    def clearBoard(self):
        self.myCanvas.delete("all")

    def chooseColor(self):
        #Get the hexadecimal value of the chosen color
        self.color = colorchooser.askcolor()[1]

    def chooseThickness(self, event):
        print(self.thickness.get())

    def activateEraser(self):
        self.eraserOn = True

        self.eraserButton.config(relief=tk.SUNKEN)
        self.brushButton.config(relief=tk.RAISED)
        self.colorButton.config(relief=tk.RAISED)

        self.myCanvas.config(cursor="@eraser.cur")

    def activateBrush(self):
        self.eraserOn = False

        self.eraserButton.config(relief=tk.RAISED)
        self.brushButton.config(relief=tk.SUNKEN)
        self.colorButton.config(relief=tk.RAISED)

        self.myCanvas.config(cursor="@pencil.cur")

    def widgetUnderMouse(self):
        x, y = self.root.winfo_pointerxy()
        widget = self.root.winfo_containing(x, y)

        return widget

    def paint(self, event):
        #Set the color to white if the eraser is on
        color = "white" if self.eraserOn else self.color

        x, y = event.x, event.y

        self.last_two_mouse_pos.append((x, y))

        #Make sure there are only two elements in the list
        if len(self.last_two_mouse_pos) > 2:
            del self.last_two_mouse_pos[0]

        #?!?!?!??!!??!!?!?
        #If the list has only one element draw a 2 pixels long line
        if len(self.last_two_mouse_pos) == 1:
            x1, y1 = self.last_two_mouse_pos[0][0], self.last_two_mouse_pos[0][1]
            self.myCanvas.create_line(x1, y1, x1, y1 + 2, fill=color, capstyle=tk.ROUND, smooth=True,
                                      width=self.thickness.get(), splinesteps=48)

        #Else draw a line between the last mouse pos and current mouse pos
        else:
            x1, y1 = self.last_two_mouse_pos[0][0], self.last_two_mouse_pos[0][1]
            x2, y2 = self.last_two_mouse_pos[1][0], self.last_two_mouse_pos[1][1]
            self.myCanvas.create_line(x1, y1, x2, y2, fill=color, capstyle=tk.ROUND, smooth=True,
                                      width=self.thickness.get(), splinesteps=48)

        print(self.last_two_mouse_pos)

    def bindEvents(self):
        #Bind events to functions
        self.root.bind("<B1-Motion>", self.paint)
        self.root.bind("<Button-1>", self.paint)
        self.root.bind("<ButtonRelease-1>", self.resetList)

        self.thickness.bind("<<ComboboxSelected>>", lambda event: [self.chooseThickness(event), self.resetList(event)])




if __name__ == '__main__':
    app = PaintApp()
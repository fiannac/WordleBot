from tkinter import *

def counter():
    global label;
    label.config(text = "wewe");


#Create an instance of tkinter frame or window
win= Tk()
#Set the geometry of tkinter frame
win.geometry("750x250")
#Create a Label widget
label= Label(win, text="Open Source Learning is Awesome!", font= ('Courier 20 underline'))
label.grid(row = 0, column = 0)
my_button = Button(win, text = "Q",command = counter)
my_button.pack()
win.mainloop()
from Tkinter import *
import tkFileDialog
import time

n_buttons = 2
buttons = [0 for i in range(n_buttons)]
def foo():
    file_path = tkFileDialog.askopenfilename()
    print(file_path)
    buttons[1]["text"] = 'Clicked ' + str(time.time()) + ' times'

n = 0
def inc():
    global n
    n += 1
    print(n)
root = Tk()
can = Canvas(root, width=900, height=500)
img = PhotoImage(file='i.png')
buttons[0] = Button(root, command=lambda: foo(), text = 'Select file', bg='white',fg="black")
buttons[0].place(x=400, y=50, w=100, h=50)
buttons[1] = Button(root, command=lambda: inc(), text = 'abacaba')
buttons[1].place(x=50, y=120, w=800, h=300)

buttons[1]["text"] = 'Clicked ' + str(time.time()) + ' times'
buttons[1]["image"] = img
can.pack()
root.mainloop()

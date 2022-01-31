import tkinter as tk
from random import randint, uniform, random
import math

root = tk.Tk()
root.title("Tkinter Practice")
c = tk.Canvas(root, width=1000, height=800, bg='black')
c.grid()
c.configure(scrollregion=(-500, -400, 500, 400))

x=0
y=0

c.create_oval(x, y, x+25, y+50, fill='blue', outline='blue')
c.create_oval(x+50, y+75, x+100, y+125, fill='white', outline='blue')

root.mainloop()
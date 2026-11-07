import tkinter as tk

root = tk.Tk()
root.title('Hello Tkinter')
label = tk.Label(root, text='Hello, GUI!')
label.pack(pady=20)
tk.Button(root, text='Click Me', command=lambda: label.config(text='Clicked!')).pack(pady=10)
root.mainloop()

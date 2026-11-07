
import tkinter as tk

root = tk.Tk()
root.title("Tkinter Hello World")
root.geometry("300x200")

message = tk.Label(root, text="Hello, GUI!")
message.pack(pady=20)

button = tk.Button(
    root,
    text="Click Me",
    command=lambda: message.config(text="You clicked the button!")
)
button.pack()

root.mainloop()

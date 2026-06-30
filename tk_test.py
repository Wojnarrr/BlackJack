import sys
import tkinter as tk

print("Python executable:", sys.executable)
print("Python version:", sys.version)

root = tk.Tk()
print("Tk version:", root.tk.call("info", "patchlevel"))

root.title("Tk Test")
root.geometry("500x300")
root.configure(bg="green")

label = tk.Label(
    root,
    text="Tkinter is working",
    bg="green",
    fg="white",
    font=("Arial", 28)
)
label.pack(pady=80)

button = tk.Button(root, text="Test Button")
button.pack()

root.mainloop()
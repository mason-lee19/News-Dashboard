import tkinter as tk
from tkinter_gui import GUI

def main():

    root = tk.Tk()
    root.geometry("1200x800")
    app = GUI(root)
    root.mainloop()

if __name__ == "__main__":
    main()
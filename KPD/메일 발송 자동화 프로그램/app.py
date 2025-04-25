import tkinter as tk
from view import MainWindow

def main():
    root = tk.Tk()
    window = MainWindow(root)
    root.mainloop()

if __name__ == '__main__':
    main()
import tkinter as tk
from interface import Interface
from registro import RegistroHoras

if __name__ == "__main__":
    root = tk.Tk()
    registro_horas = RegistroHoras()
    interface = Interface(root, registro_horas)
    root.mainloop()
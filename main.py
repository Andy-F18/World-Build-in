import tkinter as tk
import os


class WolrdBuildIn:
    def __init__(self):
        # #################### BEGIN INIT VARS ####################
        self.size = {'h': 700, 'w': 1000}
        self.colors = {'bg_a': '#ccc', 'bg_na': '#', 'menu1': '#555555'}
        # #################### END INIT VARS ####################

        try:
            os.mkdir("Projects")
        except FileExistsError:
            pass

        # #################### BEGIN WINDOW ####################
        self.root = tk.Tk()
        self.root.title("World Build'in")

        self.root.configure(background=self.colors['bg_a'])
        p_r = int(self.root.winfo_screenwidth() / 2 - self.size['w'] / 2)
        p_d = int(self.root.winfo_screenheight() / 2 - self.size['h'] / 2-50)
        self.root.geometry("{}x{}+{}+{}".format(self.size['w'], self.size['h'], p_r, p_d))
        # #################### END WINDOW ####################

        self.__menu_p()
        self.__menu_h()

        self.root.mainloop()

    def __menu_p(self):
        menu = tk.Menu(self.root)

        fileMenu = tk.Menu(menu, tearoff=0, activebackground=self.colors['menu1'])
        fileMenu.add_command(label='New world')
        fileMenu.add_command(label='Open world')
        fileMenu.add_command(label='Save')
        fileMenu.add_command(label='Save as')
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=self.root.quit)
        menu.add_cascade(label='File', menu=fileMenu)

        menu.add_command(label='Add')

        self.root.config(menu=menu)

    def __menu_h(self):
        f_menue = tk.Frame(self.root, background=self.colors['menu1'])

        b_cara = tk.Button(f_menue, text="Personnage", relief='flat', width=25)
        b_obj = tk.Button(f_menue, text="Objets", relief='flat', width=25)
        b_place = tk.Button(f_menue, text="Lieux", relief='flat', width=25)

        self.__import_file = tk.StringVar()
        b_cara.grid(column=0, row=0)
        b_obj.grid(column=1, row=0)
        b_place.grid(column=2, row=0)

        f_menue.pack(anchor="w")


if __name__ == '__main__':
    WolrdBuildIn()
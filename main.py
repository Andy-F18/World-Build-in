import tkinter as tk
import os


class WolrdBuildIn:
    def __init__(self):
        # #################### BEGIN INIT VARS ####################
        self.size = {'h': 700, 'w': 1300}
        self.colors = {'bg1': '#ccc', 'menu1': '#555555', 'menu2': '#666666'}
        # #################### END INIT VARS ####################

        try:
            os.mkdir("Projects")
        except FileExistsError:
            pass

        # #################### BEGIN WINDOW ####################
        self.__root = tk.Tk()
        self.__root.title("World Build'in")

        self.__root.configure(background=self.colors['bg1'])
        p_r = int(self.__root.winfo_screenwidth() / 2 - self.size['w'] / 2)
        p_d = int(self.__root.winfo_screenheight() / 2 - self.size['h'] / 2 - 50)
        self.__root.geometry("{}x{}+{}+{}".format(self.size['w'], self.size['h'], p_r, p_d))
        # #################### END WINDOW ####################

        self.__menu_p()
        self.__menu_h()
        self.__currentFrame = tk.Frame(self.__root)
        self.__currentFrame.pack()

        self.__root.mainloop()

    def __menu_p(self):
        menu = tk.Menu(self.__root)

        fileMenu = tk.Menu(menu, tearoff=0, activebackground=self.colors['menu1'])
        fileMenu.add_command(label='New world')
        fileMenu.add_command(label='Open world')
        fileMenu.add_command(label='Save')
        fileMenu.add_command(label='Save as')
        fileMenu.add_separator()
        fileMenu.add_command(label='Exit', command=self.__root.quit)
        menu.add_cascade(label='File', menu=fileMenu)

        menu.add_command(label='Add')

        self.__root.config(menu=menu)

    def __menu_h(self):
        f_menu = tk.Frame(self.__root, background=self.colors['menu1'])
        w = int(self.size['w']/7.1)//4

        b_chara = tk.Button(f_menu, text="Character", relief='flat', width=w, command=self.__charPage,
                            background=self.colors['menu1'], activebackground=self.colors['menu2'])
        b_place = tk.Button(f_menu, text="Locations", relief='flat', width=w, command=self.__placePage,
                            background=self.colors['menu1'], activebackground=self.colors['menu2'])
        b_items = tk.Button(f_menu, text="Items", relief='flat', width=w, command=self.__itemPage,
                            background=self.colors['menu1'], activebackground=self.colors['menu2'])
        b_story = tk.Button(f_menu, text="Story", relief='flat', width=w, command=self.__storyPage,
                            background=self.colors['menu1'], activebackground=self.colors['menu2'])

        self.__import_file = tk.StringVar()
        b_chara.grid(column=0, row=0)
        b_place.grid(column=1, row=0)
        b_items.grid(column=2, row=0)
        b_story.grid(column=3, row=0)

        f_menu.pack(anchor="w")

    def __charPage(self):
        self.__currentFrame.destroy()
        charFrame = tk.Frame(self.__root, background=self.colors['bg1'])

        listFrame = tk.Frame(charFrame, background=self.colors['bg1'])
        tk.Label(listFrame, text='Characters', bg=self.colors['bg1']).pack()
        listFrame.pack(anchor=tk.NW)

        charFrame.pack()
        self.__currentFrame = charFrame

    def __placePage(self):
        self.__currentFrame.destroy()
        placeFrame = tk.Frame(self.__root, background=self.colors['bg1'])

        listFrame = tk.Frame(placeFrame, background=self.colors['bg1'])
        tk.Label(listFrame, text='Places', bg=self.colors['bg1']).pack()
        listFrame.pack(anchor=tk.NW)

        placeFrame.pack()
        self.__currentFrame = placeFrame

    def __itemPage(self):
        self.__currentFrame.destroy()
        itemFrame = tk.Frame(self.__root, background=self.colors['bg1'])

        listFrame = tk.Frame(itemFrame, background=self.colors['bg1'])
        tk.Label(listFrame, text='Item', bg=self.colors['bg1']).pack()
        listFrame.pack(anchor=tk.NW)

        itemFrame.pack()
        self.__currentFrame = itemFrame

    def __storyPage(self):
        self.__currentFrame.destroy()
        storyFrame = tk.Frame(self.__root, background=self.colors['bg1'])

        listFrame = tk.Frame(storyFrame, background=self.colors['bg1'])
        tk.Label(listFrame, text='Story', bg=self.colors['bg1']).pack()
        listFrame.pack(anchor=tk.NW)

        storyFrame.pack()
        self.__currentFrame = storyFrame


if __name__ == '__main__':
    WolrdBuildIn()
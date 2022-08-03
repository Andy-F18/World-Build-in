import tkinter as tk
import os
from tkinter import filedialog
from Frames import CharPage as Chp


class WorldBuildIn:
    def __init__(self):
        # #################### BEGIN INIT VARS ####################
        self.size = {'h': 700, 'w': 1300}
        self.colors = {'bg1': '#ccc', 'bg2': "#555", 'menu1': '#555555', 'menu2': '#666666'}
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

        self.worldName = tk.StringVar()
        self.workDir = tk.StringVar()
        self.workDir.set(os.path.abspath(".")+'\\Projects')

        self.__root.mainloop()

    def __menu_p(self):
        menu = tk.Menu(self.__root)

        fileMenu = tk.Menu(menu, tearoff=0, activebackground=self.colors['menu1'])
        fileMenu.add_command(label='New world', command=self.__new)
        fileMenu.add_command(label='Open world', command=self.__browseFiles)
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

    def __new(self):
        new = tk.Toplevel()
        new.title("New World")
        w = 500
        h = 150
        new.configure(background=self.colors["bg1"])
        pR = int(new.winfo_screenwidth() / 2 - w / 2)
        pD = int(new.winfo_screenheight() / 2 - h / 2 - 100)
        new.geometry("{}x{}+{}+{}".format(w, h, pR, pD))

        f_new = tk.Frame(new, background=self.colors['bg1'])
        # #################### BEGIN WORLD NAME FRAME ####################
        f_name = tk.Frame(f_new, background=self.colors['bg1'])
        tk.Label(f_name, text='Name :', background=self.colors['bg1']).grid(column=0, row=0)
        tk.Entry(f_name, textvariable=self.worldName, width=25).grid(column=1, row=0, padx=5)
        f_name.pack()
        # #################### END WORLD NAME FRAME ####################

        # #################### BEGIN WORk PATH FRAME ####################
        f_path = tk.Frame(f_new, background=self.colors['bg1'])
        tk.Label(f_path, text='Path :', background=self.colors['bg1']).grid(column=0, row=0)
        tk.Entry(f_path, textvariable=self.workDir, width=50).grid(column=1, row=0, padx=5)
        tk.Button(f_path, text='...', command=self.__browseFiles).grid(column=2, row=0)
        f_path.pack(pady=10)
        # #################### END WORK PATH FRAME ####################
        tk.Button(f_new, text='OK', command=new.destroy).pack()
        f_new.place(relx=0.5, rely=0.5, anchor=tk.CENTER)

        new.grab_set()
        self.__root.wait_window(new)
        os.mkdir(self.workDir.get()+"/"+self.worldName.get())
        os.mkdir(self.workDir.get()+"/"+self.worldName.get()+"/Characters")
        os.mkdir(self.workDir.get()+"/"+self.worldName.get()+"/Locations")
        os.mkdir(self.workDir.get()+"/"+self.worldName.get()+"/Items")
        os.mkdir(self.workDir.get()+"/"+self.worldName.get()+"/Story")

    def __charPage(self):
        self.__currentFrame.destroy()
        frame = tk.Frame(self.__root, background=self.colors['bg1'])
        frame.columnconfigure(0, weight=1)
        frame.columnconfigure(1, weight=2)

        listFrame = tk.Frame(frame, background=self.colors['bg1'])
        tk.Label(listFrame, text='Characters', bg=self.colors['bg1']).pack()
        listFrame.grid(column=0, row=0, sticky=tk.W)

        charFrame = tk.Frame(frame, background=self.colors['bg1'])
        Chp.CharPage(charFrame, self.colors, self.workDir)
        charFrame.grid(column=1, row=0, sticky=tk.W)

        frame.pack(fill=tk.X)
        self.__currentFrame = frame

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

    def __browseFiles(self):
        rep = os.path.abspath(os.getcwd())
        filename_s = tk.filedialog.askdirectory(initialdir=rep,
                                                title="Select a Rep")
        if filename_s != "":
            filename = filename_s
        else:
            filename = self.workDir.get()
        # Change label contents
        self.workDir.set(filename)


if __name__ == '__main__':
    WorldBuildIn()
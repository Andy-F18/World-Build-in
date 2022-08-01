import tkinter as tk


class Character:
    def __init__(self, master, colors):
        self.__master = tk.Frame(master)
        self.colors = colors

        # #################### BEGIN INIT VARS ####################
        self.name = tk.StringVar()
        self.photoFile = ""
        self.age = tk.IntVar()
        self.gender = tk.StringVar()
        self.placeOfBirth = tk.StringVar()
        self.about = tk.StringVar()
        # #################### END INIT VARS ####################
        self.createPage()
        self.__master.pack()

    def createPage(self):
        f_header = tk.Frame(self.__master, background=self.colors['bg1'])
        tk.Canvas(f_header, width=100, height=100).grid(column=0, row=0)
        tk.Label(f_header, text="Name:", background=self.colors['bg1']).grid(column=1, row=0, padx=5)
        tk.Entry(f_header, textvariable=self.name, width=25).grid(column=2, row=0)
        f_header.pack()

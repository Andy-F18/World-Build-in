import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import yaml


class CharPage:
    def __init__(self, master, colors, workdir):
        self.__master = tk.Frame(master)
        self.colors = colors
        self.workdir = workdir

        # #################### BEGIN INIT VARS ####################
        self.name = tk.StringVar()
        self.photoFile = tk.StringVar()
        self.age = tk.IntVar()
        self.gender = ttk.Combobox()
        self.placeOfBirth = tk.StringVar()
        self.about = tk.StringVar()
        # #################### END INIT VARS ####################
        self.createPage()
        self.__master.pack(pady=5)

    def createPage(self):
        # #################### BEGIN HEADER ####################
        f_header = tk.LabelFrame(self.__master, background=self.colors['bg1'])
        f_header2 = tk.LabelFrame(f_header, background=self.colors['bg1'])

        f_img = tk.LabelFrame(f_header, background=self.colors['bg1'])
        img = tk.Canvas(f_img, width=100, height=100)
        img.bind('<Button-1>', self.__openPicture)
        img.pack()
        f_img.grid(column=0, row=0, padx=5, pady=5)
        tk.Label(f_header2, text="Name:", background=self.colors['bg1']).grid(column=0, row=0, sticky=tk.W)
        tk.Entry(f_header2, textvariable=self.name, width=25).grid(column=1, row=0, sticky=tk.W, pady=5, padx=5)
        tk.Label(f_header2, text="Gender:", background=self.colors['bg1']).grid(column=0, row=1, sticky=tk.W)
        self.gender = ttk.Combobox(f_header2, values=['M', 'F', 'Non-binary', 'Inter', 'Trans-M', 'Trans-F'], width=22)
        self.gender.grid(column=1, row=1, sticky=tk.W, pady=5, padx=5)

        tk.Button(f_header, text='Save', command=self.save).grid(column=2, row=0)

        f_header2.grid(column=1, row=0)
        f_header.pack()
        # #################### END HEADER ####################

        # #################### BEGIN IMAGE AND NAME ####################
        # #################### END IMAGE AND NAME ####################

    def save(self):
        data = {
            'name': self.name.get(),
            'gender': self.gender.get(),
            'photoFile': self.photoFile.get()
        }

        print(os.listdir(self.workdir.get()+'/Characters/'))
        files = os.listdir()

        fileName = self.name.get().replace(' ', '_', 999) + '.yml'

        file = open(self.workdir.get()+'/Characters/'+str(fileName), 'w')
        file.write(yaml.dump(data, default_flow_style=False))
        file.close()

    def __openPicture(self, event):
        rep = os.path.abspath(os.getcwd())
        filename_s = filedialog.askopenfilename(initialdir=rep,
                                                title="Select a File",
                                                filetypes=(("PNG files", "*.png"),
                                                           ("all files", "*.*")))
        if filename_s != "":
            filename = filename_s
        else:
            filename = self.photoFile.get()
        # Change label contents
        self.photoFile.set(filename)
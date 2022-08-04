import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import yaml
from PIL import Image


class CharPage:
    def __init__(self, master, colors, workdir):
        self.__master = tk.Frame(master, background=colors['bg1'])
        self.colors = colors
        self.workdir = workdir
        self.can = tk.Canvas()

        # #################### BEGIN INIT VARS ####################
        self.name = tk.StringVar()
        self.photoFile = tk.StringVar()
        self.photo = Image.Image()
        self.age = tk.IntVar()
        self.gender = ttk.Combobox()
        self.placeOfBirth = tk.StringVar()
        self.about = tk.Text()
        # #################### END INIT VARS ####################
        self.createPage()
        self.__master.pack(pady=5)

    def createPage(self):
        # #################### BEGIN HEADER ####################
        f_header = tk.LabelFrame(self.__master, background=self.colors['bg1'])
        f_header2 = tk.LabelFrame(f_header, background=self.colors['bg1'])

        f_img = tk.LabelFrame(f_header, background=self.colors['bg1'])
        self.can = tk.Canvas(f_img, width=100, height=100)
        self.can.bind('<Button-1>', self.__openPicture)
        self.can.pack()
        f_img.grid(column=0, row=0, padx=5, pady=5)
        tk.Label(f_header2, text="Name:", background=self.colors['bg1']).grid(column=0, row=0, sticky=tk.W)
        tk.Entry(f_header2, textvariable=self.name, width=25).grid(column=1, row=0, sticky=tk.W, pady=5, padx=5)
        tk.Label(f_header2, text="Age:", background=self.colors['bg1']).grid(column=0, row=1, sticky=tk.W)
        tk.Entry(f_header2, textvariable=self.age, width=25).grid(column=1, row=1, sticky=tk.W, pady=5, padx=5)
        tk.Label(f_header2, text="Gender:", background=self.colors['bg1']).grid(column=0, row=2, sticky=tk.W)
        self.gender = ttk.Combobox(f_header2, values=['M', 'F', 'Non-binary', 'Inter', 'Trans-M', 'Trans-F'], width=22)
        self.gender.grid(column=1, row=2, sticky=tk.W, pady=5, padx=5)

        tk.Button(f_header, text='Save', command=self.save).grid(column=2, row=0, padx=5)

        f_header2.grid(column=1, row=0, padx=5)
        f_header.grid(column=0, row=0, sticky=tk.W)
        # #################### END HEADER ####################

        # #################### BEGIN IMAGE AND NAME ####################
        f_about = tk.LabelFrame(self.__master, text='About', background=self.colors['bg1'])

        self.about = tk.Text(f_about, width=50, height=20)
        self.about.pack(pady=5, padx=5)

        f_about.grid(column=0, row=1, pady=10, sticky=tk.W)
        # #################### END IMAGE AND NAME ####################

    def save(self):
        self.photoFile.set(self.workdir.get()+'/Images/'+self.name.get().replace(' ', '_', 999)+'.png')
        data = {
            'name': self.name.get(),
            'gender': self.gender.get(),
            'age': self.age.get(),
            'photoFile': self.photoFile.get(),
            'about': self.about.get(0.0, tk.END)
        }
        self.photo.save(self.photoFile.get())

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
            return
        # Change label contents
        self.photoFile.set(filename)

        img = Image.open(filename)
        size = (img.width, img.height)
        center = (size[0]//2, size[1]//2)
        if size[0] > size[1]:
            img = img.crop((center[0]-center[1], 0, center[0]+center[1], size[1]))

        if size[1] > size[0]:
            img = img.crop((0, center[1]-center[0], size[0], center[1]+center[0]))

        self.photo = img.resize((100, 100))
        self.photoFile.set(self.workdir.get()+'/Images/'+self.name.get().replace(' ', '_', 999)+'.png')
        self.photo.save(self.photoFile.get())
        imgCan = tk.PhotoImage(file=self.photoFile.get())
        self.can.create_image(0, 0, anchor=tk.NW, image=imgCan)
        self.can.update()

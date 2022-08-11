import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import yaml
from PIL import Image


class CharPage:
    def __init__(self, master, colors, workdir):
        self.master = master
        self.__root = tk.Frame(master, background=colors['bg1'])
        self.colors = colors
        self.workdir = workdir
        self.genders = ['M', 'F', 'Non-binary', 'Inter', 'Trans-M', 'Trans-F']
        self.can = tk.Canvas()

        # #################### BEGIN INIT VARS ####################
        self.name = tk.StringVar()
        self.photoFile = tk.BooleanVar()
        self.photoFile.set(False)
        self.photo = Image.Image()
        self.age = tk.IntVar()
        self.gender = ttk.Combobox(values=self.genders)
        self.placeOfBirth = tk.StringVar()
        self.about = tk.Text()
        self.aboutT = tk.StringVar()
        # #################### END INIT VARS ####################
        self.__root.pack(pady=5)

        # #################### BEGIN INIT VARS ####################

        # #################### BEGIN HEADER ####################
        f_header = tk.LabelFrame(self.__root, background=self.colors['bg1'])
        f_header2 = tk.LabelFrame(f_header, background=self.colors['bg1'])

        f_img = tk.LabelFrame(f_header, background=self.colors['bg1'])
        self.can = tk.Canvas(f_img, width=100, height=100)
        self.can.bind('<Button-1>', self.__openPicture)
        self.can.pack()
        f_img.grid(column=0, row=0, padx=5, pady=5)
        tk.Label(f_header2, text="Name:", background=self.colors['bg1']).grid(column=0, row=0, sticky=tk.W)
        self.eName = tk.Entry(f_header2, textvariable=self.name, width=25, disabledforeground='black')
        self.eName.grid(column=1, row=0, sticky=tk.W, pady=5, padx=5)

        tk.Label(f_header2, text="Age:", background=self.colors['bg1']).grid(column=0, row=1, sticky=tk.W)
        self.eAge = tk.Entry(f_header2, textvariable=self.age, width=25, disabledforeground='black')
        self.eAge.grid(column=1, row=1, sticky=tk.W, pady=5, padx=5)

        tk.Label(f_header2, text="Gender:", background=self.colors['bg1']).grid(column=0, row=2, sticky=tk.W)
        self.gender = ttk.Combobox(f_header2, values=self.genders, width=22)
        self.gender.config(state=tk.NORMAL)
        self.gender.grid(column=1, row=2, sticky=tk.W, pady=5, padx=5)

        self.bSaveEdit = tk.Button(f_header, text='Save', command=self.save, width=5)
        self.bSaveEdit.grid(column=2, row=0, padx=5)

        f_header2.grid(column=1, row=0, padx=5)
        f_header.grid(column=0, row=0, sticky=tk.W)
        # #################### END HEADER ####################

        # #################### BEGIN IMAGE AND NAME ####################
        f_about = tk.LabelFrame(self.__root, text='About', background=self.colors['bg1'])

        self.about = tk.Text(f_about, width=50, height=20)
        self.about.config(state=tk.NORMAL)
        self.about.pack(pady=5, padx=5)

        f_about.grid(column=0, row=1, pady=10, sticky=tk.W)

        self.createPage()
        # #################### END IMAGE AND NAME ####################

        # #################### END INIT VARS ####################

    def createPage(self):
        self.eName.config(state=tk.NORMAL)
        self.eAge.config(state=tk.NORMAL)
        self.gender.config(state=tk.NORMAL)
        self.about.config(state=tk.NORMAL)
        self.can.bind('<Button-1>', self.__openPicture)
        self.bSaveEdit.config(text='Save', command=self.save)

    def see(self, charFile):
        self.about.focus_get()
        self.createPage()
        self.can.delete('all')
        self.can.update()
        self.load(charFile)
        self.eName.config(state=tk.DISABLED)
        self.eAge.config(state=tk.DISABLED)
        self.gender.config(state=tk.DISABLED)
        self.can.unbind('<Button-1>')
        if self.photoFile.get():
            self.can.config(state=tk.NORMAL)
            img = tk.PhotoImage(file=charFile.replace('Characters', 'Images').replace('.yml', '.png'))
            self.can.create_image(0, 0, anchor=tk.NW, image=img)
            self.can.update()
        self.bSaveEdit.config(text='Edit', command=self.createPage)

    def load(self, charFile):
        file = open(charFile, mode='r')
        char = yaml.load(file, yaml.FullLoader)
        file.close()

        self.name.set(char['name'])
        self.age.set(char['age'])
        self.gender.current(self.genders.index(char['gender']))
        self.photoFile.set(char['photoFile'])
        self.about.replace(0.0, tk.END, char['about'])

    def save(self):
        data = {
            'name': self.name.get(),
            'gender': self.gender.get(),
            'age': self.age.get(),
            'photoFile': self.photoFile.get(),
            'about': self.about.get(0.0, tk.END).replace('\n\n', '')
        }
        fileName = self.name.get().replace(' ', '_', 99) + '.yml'

        file = open(self.workdir.get()+'/Characters/'+str(fileName), 'w')
        file.write(yaml.dump(data, default_flow_style=False))
        file.close()
        self.see(self.workdir.get()+'/Characters/'+self.name.get().replace(' ', '_', 99)+'.yml')

    def __openPicture(self, event):
        if self.name.get() == "":
            return
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

        img = Image.open(filename)
        size = (img.width, img.height)
        center = (size[0]//2, size[1]//2)
        if size[0] > size[1]:
            img = img.crop((center[0]-center[1], 0, center[0]+center[1], size[1]))

        if size[1] > size[0]:
            img = img.crop((0, center[1]-center[0], size[0], center[1]+center[0]))

        self.photo = img.resize((100, 100))
        self.photoFile.set(True)
        self.photo.save(self.workdir.get()+'/Images/'+self.name.get().replace(' ', '_', 99)+'.png')
        imgCan = tk.PhotoImage(file=self.workdir.get()+'/Images/'+self.name.get().replace(' ', '_', 99)+'.png')
        self.can.create_image(0, 0, anchor=tk.NW, image=imgCan)
        self.can.update()

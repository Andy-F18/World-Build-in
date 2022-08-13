import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import os
import yaml
from PIL import Image


class ItemPage:
    def __init__(self, master, colors, workdir):
        self.__root = master
        self.__root.columnconfigure(0, weight=1)
        self.__root.columnconfigure(1, weight=2)
        self.colors = colors
        self.workDir = workdir
        self.items = []
        for l in os.listdir(self.workDir.get() + '/Items'):
            self.items.append(l.replace('.yml', '').replace('_', ' ', 99))

        self.items.remove('Images')

        self.locations = []
        for l in os.listdir(self.workDir.get() + '/Locations'):
            self.locations.append(l.replace('.yml', '').replace('_', ' ', 99))

        self.locations.remove('Images')

        # #################### BEGIN INIT VARS ####################
        self.name = tk.StringVar()
        self.photoFile = tk.BooleanVar()
        self.photoFile.set(False)
        self.loc = ttk.Combobox(values=self.locations)
        self.about = tk.Text()
        self.photo = tk.PhotoImage
        # #################### END INIT VARS ####################
        self.__root.pack(fill=tk.X)

        # #################### BEGIN ITEMS LIST ####################
        listFrame = tk.LabelFrame(self.__root, text='Items', background=self.colors['bg1'])
        if len(self.items) == 0:
            tk.Label(listFrame, text="No Items founded", bg=self.colors['bg1']).pack()
        else:
            for item in self.items:
                l = tk.Label(listFrame, text=item)
                l.pack(pady=1, fill=tk.X, padx=5)
                l.bind('<Button-1>', lambda event, itemFile=item: self.redirect(itemFile.replace(' ', '_', 99)+'.yml'))

        listFrame.grid(column=0, row=0, sticky=tk.EW, padx=5)
        # #################### END ITEMS LIST ####################

        # #################### BEGIN ITEMS FORM ####################
        self.f_form = tk.Frame(self.__root, background=self.colors['bg1'])
        self.f_form.columnconfigure(0, weight=1)
        self.f_form.columnconfigure(1, weight=1)
        f_header = tk.LabelFrame(self.f_form, background=self.colors['bg1'])

        f_img = tk.LabelFrame(f_header, background=self.colors['bg1'])
        self.can = tk.Canvas(f_img, width=100, height=100)
        self.can.config(background=self.colors['bg1'], highlightbackground=self.colors['bg1'])
        self.can.bind('<Button-1>', self.__openPicture)
        self.can.pack()
        f_img.grid(column=0, row=0, pady=5, padx=5)

        f_headerBis = tk.LabelFrame(f_header, background=self.colors['bg1'])

        tk.Label(f_headerBis, text='Name:', background=self.colors['bg1']).grid(column=0, row=0, sticky=tk.W)
        self.eName = tk.Entry(f_headerBis, textvariable=self.name, width=25, disabledforeground='black')
        self.eName.grid(column=1, row=0, sticky=tk.W, pady=5, padx=5)

        tk.Label(f_headerBis, text='Location:', background=self.colors['bg1']).grid(column=0, row=1, sticky=tk.W)
        self.location = ttk.Combobox(f_headerBis, values=self.locations, width=22)
        self.location.grid(column=1, row=1, padx=5, pady=5, sticky=tk.W)
        f_headerBis.grid(column=1, row=0, sticky=tk.W, padx=5, pady=5)

        self.bSaveEdit = tk.Button(f_header, text='Save', width=5, command=lambda: self.see(self.save()))
        self.bSaveEdit.grid(column=2, row=0, padx=5)

        f_header.grid(column=0, row=0)

        f_about = tk.LabelFrame(self.f_form, text='About', background=self.colors['bg1'])
        self.about = tk.Text(f_about, width=50, height=20)
        self.about.pack(padx=5, pady=5)
        f_about.grid(column=0, row=1, pady=10)

        self.f_form.grid(column=1, row=0, sticky=tk.EW, pady=10)
        # #################### END ITEMS FORM ####################
        # self.createPage()

    def createPage(self):
        self.eName.config(state=tk.NORMAL)
        self.location.config(state=tk.NORMAL)
        self.location.unbind('<Button-1>')
        self.about.config(state=tk.NORMAL)
        self.can.bind('<Button-1>', self.__openPicture)
        self.bSaveEdit.config(text='Save', command=lambda: self.see(self.save()))

    def see(self, itemFile):
        self.createPage()
        self.load(itemFile)

        self.eName.config(state=tk.DISABLED)
        self.location.config(state=tk.DISABLED)
        # if self.location.get() != '':
        #     self.location.bind('<Button-1>',
        #                        lambda event, loc=self.location.get(): self.see(loc.replace(' ', '_', 99) + '.yml'))
        self.about.config(state=tk.DISABLED)
        self.can.unbind('<Button-1>')
        self.bSaveEdit.config(text='Edit', command=self.createPage)
        self.can.delete('all')
        if self.photoFile.get():
            self.can.bind('<Button-1>', lambda event: self.openFull())
            self.photo = tk.PhotoImage(file=self.workDir.get() + '/Items/Images/' + itemFile.replace('.yml', '.png'))
            self.can.create_image(0, 0, anchor=tk.NW, image=self.photo)

    def load(self, locFile):
        file = open(self.workDir.get() + '/Items/' + locFile, mode='r')
        item = yaml.load(file, yaml.FullLoader)
        file.close()

        self.name.set(item['name'])
        if item['location'] != '':
            self.location.current(self.locations.index(item['location']))
        else:
            self.location.set('')
        self.photoFile.set(item['photoFile'])
        self.about.replace(0.0, tk.END, item['about'])

    def save(self):
        if self.name.get() == '':
            return

        data = {
            'name': self.name.get(),
            'location': self.location.get(),
            'photoFile': self.photoFile.get(),
            'about': self.about.get(0.0, tk.END).rstrip(self.about.get(0.0, tk.END)[-1])
        }
        fileName = self.name.get().replace(' ', '_', 99) + '.yml'
        file = open(self.workDir.get() + '/Items/' + fileName, mode='w')
        file.write(yaml.dump(data, default_flow_style=False))
        file.close()
        return fileName

    def redirect(self, itemFile):
        self.save()
        self.see(itemFile)

    def openFull(self):
        img = Image.open(self.workDir.get() + '/Items/Images/' + self.name.get().replace(' ', '_', 99)+'_FULL.png')
        img.show()

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
        img.save(self.workDir.get() + '/Items/Images/' + self.name.get().replace(' ', '_', 99) + '_FULL.png')
        size = (img.width, img.height)
        center = (size[0] // 2, size[1] // 2)
        if size[0] > size[1]:
            img = img.crop((center[0] - center[1], 0, center[0] + center[1], size[1]))

        if size[1] > size[0]:
            img = img.crop((0, center[1] - center[0], size[0], center[1] + center[0]))

        self.photo = img.resize((100, 100))
        self.photoFile.set(True)
        self.photo.save(self.workDir.get() + '/Items/Images/' + self.name.get().replace(' ', '_', 99) + '.png')
        imgCan = tk.PhotoImage(file=self.workDir.get() + '/Items/Images/'
                                    + self.name.get().replace(' ', '_', 99) + '.png')
        self.can.create_image(0, 0, anchor=tk.NW, image=imgCan)
        self.can.update()

    def destroy(self):
        self.__root.destroy()
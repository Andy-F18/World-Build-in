import tkinter as tk
from tkinter import ttk
import os
import yaml


class StoryPage:
    def __init__(self, main, master, colors, workdir):
        self.main = main
        self.__root = master
        self.__root.columnconfigure(0, weight=1)
        self.__root.columnconfigure(1, weight=2)
        self.colors = colors
        self.workDir = workdir
        self.story = []
        for s in os.listdir(self.workDir.get()+'/Story'):
            self.story.append(s.replace('.yml', '').replace('_', ' ', 99))

        try:
            self.story.remove('Images')
        except ValueError:
            pass

        self.locations = []
        for l in os.listdir(self.workDir.get() + '/Locations'):
            self.locations.append(l.replace('.yml', '').replace('_', ' ', 99))

        self.locations.remove('Images')

        # #################### BEGIN INIT VARS ####################
        self.name = tk.StringVar()
        self.prevName = tk.StringVar()
        self.location = ttk.Combobox(values=self.locations)
        self.about = tk.Text()
        # #################### END INIT VARS ####################
        self.__root.grid(column=0, row=1, sticky=tk.NSEW)

        # #################### BEGIN STORY LIST ####################
        self.listFrame = tk.LabelFrame(self.__root, text='Chapters/Parts', background=self.colors['bg1'])
        self.listChaps()
        # #################### END STORY LIST ####################

        # #################### BEGIN STORY FORM ####################
        self.fForm = tk.Frame(self.__root, background=self.colors['bg1'])
        self.fForm.columnconfigure(0, weight=1)

        fHeader = tk.LabelFrame(self.fForm, background=self.colors['bg1'])
        fHeader.columnconfigure(0, weight=1)
        fHeader.columnconfigure(1, weight=1)
        fHeader.columnconfigure(2, weight=1)
        fHeader.columnconfigure(3, weight=1)
        fHeader.columnconfigure(4, weight=1)

        tk.Label(fHeader, text='Name:', background=self.colors['bg1']).grid(column=0, row=0, sticky=tk.W)
        self.eName = tk.Entry(fHeader, textvariable=self.name, width=25, disabledforeground='black')
        self.eName.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)

        tk.Label(fHeader, text='Location:', background=self.colors['bg1']).grid(column=2, row=0, sticky=tk.W)
        self.location = ttk.Combobox(fHeader, values=self.locations, width=22)
        self.location.grid(column=3, row=0, padx=5, pady=5, sticky=tk.W)

        self.bSaveEdit = tk.Button(fHeader, text='Save', width=5, command=lambda: self.see(self.save()))
        self.bSaveEdit.grid(column=4, row=0, padx=5, pady=5)

        fHeader.grid(column=0, row=0, padx=5, pady=10)

        fAbout = tk.LabelFrame(self.fForm, text='Content', background=self.colors['bg1'])
        fAbout.columnconfigure(0, weight=1)
        self.about = tk.Text(fAbout)
        scroll = tk.Scrollbar(fAbout)
        scroll.configure(command=self.about.yview)
        self.about.grid(column=0, row=0, sticky=tk.NSEW, pady=5, padx=5)
        scroll.grid(column=1, row=0, sticky=tk.NS, pady=5)
        self.about.configure(state=tk.DISABLED, yscrollcommand=scroll.set)
        fAbout.grid(column=0, row=1, pady=10, padx=10, sticky=tk.NSEW)

        fNext = tk.LabelFrame(self.fForm, background=self.colors['bg1'])
        tk.Label(fNext, text='Next:', background=self.colors['bg1']).grid(column=0, row=0, sticky=tk.W)
        self.next = ttk.Combobox(fNext, values=self.story, width=22)
        self.next.grid(column=1, row=0, padx=5, pady=5, sticky=tk.W)
        fNext.grid(column=0, row=2, pady=10)

        self.fForm.grid(column=1, row=0, pady=5, padx=5, sticky=tk.NSEW)
        # #################### END STORY FORM ####################
        self.createPage()

    def listChaps(self):
        self.listFrame.destroy()
        self.listFrame = tk.LabelFrame(self.__root, text='Chapters/Parts', background=self.colors['bg1'])
        if len(self.story) == 0:
            tk.Label(self.listFrame, text="No elements founded", bg=self.colors['bg1']).pack()
        else:
            for s in self.story:
                l = tk.Label(self.listFrame, text=s)
                l.pack(pady=1, fill=tk.X, padx=5)
                l.bind('<Button-1>', lambda event, storyFile=s: self.redirect(storyFile.replace(' ', '_', 99) + '.yml'))

        self.listFrame.grid(column=0, row=0, sticky=tk.EW, padx=5)

    def createPage(self):
        self.eName.config(state=tk.NORMAL)
        self.location.config(state=tk.NORMAL)
        self.location.unbind('<Button-1>')
        self.about.config(state=tk.NORMAL)
        self.next.config(values=self.story, state=tk.NORMAL)
        self.next.unbind('<Button-1>')
        self.bSaveEdit.config(text='Save', command=lambda: self.see(self.save()))

    def see(self, storyFile):
        self.createPage()
        self.load(storyFile)
        self.listChaps()

        self.eName.config(state=tk.DISABLED)
        self.location.config(state=tk.DISABLED)
        if self.location.get() != '':
            self.location.bind('<Button-1>',
                               lambda event, loc=self.location.get():
                               self.main.locPage(loc.replace(' ', '_', 99) + '.yml'))
        self.about.config(state=tk.DISABLED)
        self.next.config(state=tk.DISABLED)
        if self.next.get() != '':
            self.next.bind('<Button-1>', lambda event: self.redirect(self.next.get().replace(' ', '_', 99)+'.yml'))
        self.bSaveEdit.config(text='Edit', command=self.createPage)

    def load(self, storyFile):
        file = open(self.workDir.get() + '/Story/' + storyFile, mode='r')
        story = yaml.load(file, yaml.FullLoader)
        file.close()

        self.name.set(story['name'])
        self.prevName.set(self.name.get())
        if story['location'] != '':
            try:
                self.location.current(self.locations.index(story['location']))
            except ValueError:
                self.location.set('')
        else:
            self.location.set('')

        if story['next'] != '':
            self.next.current(self.story.index(story['next']))
        else:
            self.next.set('')

        self.about.replace(0.0, tk.END, story['about'])

        self.story = []
        for s in os.listdir(self.workDir.get()+'/Story'):
            self.story.append(s.replace('.yml', '').replace('_', ' ', 99))

    def save(self):
        if self.name.get() == '':
            return

        self.renameFile()
        data = {
            'name': self.name.get(),
            'location': self.location.get(),
            'about': self.about.get(0.0, tk.END).rstrip(self.about.get(0.0, tk.END)[-1]),
            'next': self.next.get()
        }
        fileName = self.name.get().replace(' ', '_', 99) + '.yml'
        file = open(self.workDir.get() + '/Story/' + fileName, mode='w')
        file.write(yaml.dump(data, default_flow_style=False))
        file.close()
        self.prevName.set(self.name.get())
        return fileName

    def renameFile(self):
        os.rename(self.workDir.get() + '/Story/' + self.prevName.get().replace(' ', '_', 99) + '.yml',
                  self.workDir.get() + '/Story/' + self.name.get().replace(' ', '_', 99) + '.yml')

    def redirect(self, storyFile):
        self.save()
        self.see(storyFile)

    def destroy(self):
        self.__root.destroy()
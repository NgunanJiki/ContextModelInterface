import os
import json
from pathlib import Path
from PyQt5.QtWidgets import QMainWindow, QAction, QFileDialog, QDesktopWidget, QSplitter, QListView, QVBoxLayout, QFrame, QLabel, QMessageBox, QWidget
from PyQt5.QtGui import QStandardItemModel, QStandardItem, QIcon
from PyQt5.QtCore import Qt, QModelIndex
from ConfirmExit import ConfirmExit

from context_view import ContextView
from model_view import ModelView
from utilities import Utilities

class View(QMainWindow):
    def __init__(self, app):
        super().__init__()
        self.utilities = Utilities(app)
        self.app = app
        self.initialize()

    def initialize(self):
        # load 
        self.settings, self.projects = self.loadSettings()
        self.setWindowTitle(self.settings["appName"])
        size = self.utilities.computeXY(800, 600)
        self.resize(size[0], size[1])
        self.splitter = QSplitter(Qt.Horizontal)
        self.listView = QListView()
        self.model = QStandardItemModel()
        self.currentIndex = 0 if self.projects.__len__() > 0 else None
        self.unsaved = {}

        ## save menu

        # new file menu
        newFile = QAction(QIcon('./assets/new-file.png'), '&New', self)
        newFile.setShortcut('Ctrl+N')
        newFile.setStatusTip('New')
        newFile.triggered.connect(self.createNew)
        # save menu
        save = QAction(QIcon('./assets/save.png'), '&Save', self)
        save.setShortcut('Ctrl+S')
        save.setStatusTip('Save')
        save.triggered.connect(self.save)
        # load menu
        load = QAction(QIcon('./assets/load.png'), '&Load', self)
        load.setShortcut('Ctrl+L')
        load.setStatusTip('Load')
        load.triggered.connect(self.load)
        # exit menu
        exit = QAction(QIcon('./assets/exit.png'), '&Exit', self)
        exit.setShortcut('Ctrl+Q')
        exit.setStatusTip('Close')
        exit.triggered.connect(self.quitApp)
        # generate menu
        generate = QAction(QIcon('./assets/generate.png'), '&Generate', self)
        generate.setShortcut('Ctrl+G')
        generate.setStatusTip('Generate')
        generate.triggered.connect(lambda: self.setProject(self.currentIndex, "g"))
        # models menu
        models = QAction(QIcon('./assets/model.png'), '&Models', self)
        models.setShortcut('Ctrl+M')
        models.setStatusTip('Models')
        models.triggered.connect(lambda: self.setProject(self.currentIndex, "m"))

        ## menu bar

        menubar = self.menuBar()
        # File
        fileMenu = menubar.addMenu('&File')
        fileMenu.addAction(newFile)
        fileMenu.addAction(save)
        fileMenu.addAction(load)
        fileMenu.addAction(exit)
        # Generate
        fileMenu = menubar.addMenu('&Generate')
        fileMenu.addAction(generate)
        # Models
        fileMenu = menubar.addMenu('&Models')
        fileMenu.addAction(models)

        ## tool bar

        toolbar = self.addToolBar('New')
        toolbar.addAction(newFile)
        toolbar = self.addToolBar('Save')
        toolbar.addAction(save)
        toolbar = self.addToolBar('Load')
        toolbar .addAction(load)
        toolbar = self.addToolBar('Generate')
        toolbar.addAction(generate)
        toolbar = self.addToolBar('Models')
        toolbar.addAction(models)
        toolbar = self.addToolBar('Exit')
        toolbar.addAction(exit)

        # define work area
        self.defineWorkArea()

        # set center
        self.center()

    # work area
    def defineWorkArea(self):
        for it in self.projects:
            self.model.appendRow(QStandardItem(it[0]))

        listFrame = QFrame()
        listFrame.setMinimumWidth(250)
        listFrame.setMaximumWidth(400)
        
        self.listView.setModel(self.model)
        self.listView.clicked[QModelIndex].connect(lambda i: self.setProject(i.row(), self.settings["tab"]))

        label = QLabel('PROJECTS')
        vLayout = QVBoxLayout()
        vLayout.addWidget(label)
        vLayout.addWidget(self.listView)
        listFrame.setLayout(vLayout)
        
        self.splitter.addWidget(listFrame)
        if (self.currentIndex != None):
            self.splitter.addWidget(ContextView(self, self.projects[self.currentIndex][1]))
        else:
            self.splitter.addWidget(QWidget())

        self.setCentralWidget(self.splitter)

    # load settings
    def loadSettings(self):
        # check if settings exists
        exists = os.path.exists('settings.json')
        if not exists:
            Path('settings.json').touch()
            with open('settings.json', 'w') as created:
                json.dump({"appName": "Context Modular", "state": 0, "tab": "g", "projects": []}, created)

        with open('settings.json') as settings:
            data = json.load(settings)
            projects = []
            for proj in data["projects"]:
                try:
                    with open(proj['file']) as file:
                        fileLoaded = json.load(file)
                        projects.append([proj["title"], fileLoaded['contexts'], proj["file"]])
                except:
                    pass
            
            return (data, projects)
    
    # set project
    def setProject(self, index, tab):
        if (index == None):
            return
        
        self.currentIndex = index
        self.settings["tab"] = tab
        if (tab == "g"):
            self.splitter.replaceWidget(1, ContextView(self, self.projects[index][1]))
        else:
            self.splitter.replaceWidget(1, ModelView(self, self.projects[index]))
        i = self.model.index(index, 0)
        self.listView.setCurrentIndex(i)

    # load contexts
    def load(self):
        folder = os.path.expanduser(f"~/Documents/CtxModular/")
        name = QFileDialog.getOpenFileName(self, 'Load Context', folder)
        with open(name[0]) as file:
            try:
                length = self.projects.__len__()
                data = json.load(file)
                title = os.path.basename(name[0]).replace('.ctx', '')

                exists = [obj for obj in self.settings["projects"] if obj["title"] == title]
                if (exists.__len__() == 0):
                    self.settings["projects"].append({ "title": title, "file": name[0] })
                    self.projects.append([title, data['contexts'], name[0]])

                    # add to menu
                    self.model.appendRow(QStandardItem(title))
                    self.setProject(length, "g")

                    # update settings
                    with open("settings.json", "w") as settings_file:
                        json.dump(self.settings, settings_file)
            except:
                msg = QMessageBox()
                msg.setIcon(QMessageBox.Information)
                msg.setText("Failed to load file")
                msg.exec_()

    # new project
    def createNew(self):
        length = self.projects.__len__()
        folder = os.path.expanduser(f"~/Documents/CtxModular/")
        if not os.path.exists(folder):
            os.makedirs(folder)
        
        # open file system
        filename = QFileDialog.getSaveFileName(self, 'Save file', folder, "Ctx files (*.ctx)")
        if filename[0] == '':
            return 0

        # create/store file data
        empty = [{"name": "", "attributes": [], "rules": [], "description": "" }]
        with open(f"{filename[0]}.ctx", "w") as file:
            json.dump({ "contexts": empty }, file)

        data = {}
        title = os.path.basename(filename[0])
        with open('settings.json') as settings:
            data = json.load(settings)
            data['projects'].append({ "title": title, "file": f"{filename[0]}.ctx" })

        # update setting
        with open("settings.json", "w") as settings_file:
            json.dump(data, settings_file)

        self.projects.append([title, empty, f"{filename[0]}.ctx"])
        self.model.appendRow(QStandardItem(title))
        self.setProject(length, "g")

    
    # update project
    def updateProject(self, listIndex, name, attributes, rules, description):
        self.projects[self.currentIndex][1][listIndex] = {"name": name, "attributes": attributes, "rules": rules, "description": description }
        # store unsaved
        self.unsaved[self.projects[self.currentIndex][0]] = self.projects[self.currentIndex]

    # save context 
    def save(self):
        for key in self.unsaved:
            proj = self.unsaved[key]
            with open(proj[2], 'w') as file:
                json.dump({ 'contexts': proj[1] }, file)
        # clear
        self.unsaved = {}

    # quit app
    def quitApp(self):
        if (self.unsaved != {}):
            dlg = ConfirmExit(self)
            if dlg.exec():
                self.app.quit()
        else:
            self.app.quit()

    # center window
    def center(self):
        fg = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        fg.moveCenter(cp)
        self.move(fg.topLeft())

            
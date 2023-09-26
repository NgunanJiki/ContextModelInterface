import os

import pandas as pd
from utilities import Utilities
from PyQt5.QtWidgets import QGroupBox, QFrame, QScrollArea, QVBoxLayout, QFileDialog, QMessageBox, QPushButton, QHBoxLayout, QPlainTextEdit
from PyQt5.QtCore import QSize

class TestsView(QGroupBox):
    def __init__(self, parentView, project):
        super().__init__()
        self.utilities = Utilities(parentView.app)
        self.Y50 = self.utilities.computeY(50)
        # self.X50 = self.utilities.computeX(50)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(self.utilities.computeY(20))

        self.npArray = None
        self.columns = {}
 
        self.setup()

        frame = QFrame()
        
        frame.setLayout(self.layout)
        scroll = QScrollArea()
        scroll.setWidget(frame)
        scroll.setWidgetResizable(True)
        vbox = QVBoxLayout()
        vbox.addWidget(scroll)
        self.setTitle(project[0])
        self.setLayout(vbox)


    def setup(self):
        hbox = QHBoxLayout()

        self.loadView = QPlainTextEdit()
        self.loadView.setFixedSize(QSize(self.utilities.computeX(800), self.utilities.computeY(350)))
        self.loadView.setReadOnly(True)

        loadDataBtn = QPushButton('Load Dataset', self)
        loadDataBtn.setFixedSize(QSize(self.utilities.computeX(200), self.Y50))
        loadDataBtn.clicked.connect(self.loadDataset)

        hbox.addWidget(loadDataBtn)
        hbox.addWidget(self.loadView)

        hbox1 = QHBoxLayout()

        self.testView = QPlainTextEdit()
        self.testView.setFixedSize(QSize(self.utilities.computeX(800), self.utilities.computeY(500)))
        self.testView.setReadOnly(True)

        testBtn = QPushButton('Test', self)
        testBtn.setFixedSize(QSize(self.utilities.computeX(200), self.Y50))
        testBtn.clicked.connect(lambda: self.process(self.npArray))

        hbox1.addWidget(testBtn)
        hbox1.addWidget(self.testView)

        self.layout.addItem(hbox)
        self.layout.addItem(hbox1)



    def loadDataset(self):
        folder = os.path.expanduser(f"~/Desktop/")
        name = QFileDialog.getOpenFileName(self, 'Load Dataset', folder)
        try:
            df = pd.read_excel(r''+name[0]+'')
            df.fillna(0.00)
            for i, col in enumerate(df.columns):
                self.columns[i] = col
            self.npArray = df.to_numpy()
            self.loadView.setPlainText(df.to_string())
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Failed to load data")
            msg.exec_()

    def process(self, arr):
        print(arr[0][0])
        # for i, item in enumerate(npArray):
        #     print(npArray.loc[i])
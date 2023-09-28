import os

import pandas as pd
from interpreter import PyInterpreter
from utilities import Utilities
from PyQt5.QtWidgets import QGroupBox, QFrame, QScrollArea, QVBoxLayout, QFileDialog, QMessageBox, QPushButton, QHBoxLayout, QPlainTextEdit, QComboBox
from PyQt5.QtCore import QSize

class TestsView(QGroupBox):
    def __init__(self, parentView, project):
        super().__init__()
        self.project = project
        self.utilities = Utilities(parentView.app)
        self.Y50 = self.utilities.computeY(50)
        # self.X50 = self.utilities.computeX(50)
        self.pyInterpreter = PyInterpreter()
        self.layout = QVBoxLayout()
        self.layout.setSpacing(self.utilities.computeY(20))

        self.npArray = None
        self.columns = {}
        self.currentModels = {}
        self.currentRuleNames = []
 
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
        # map models
        for i, data in enumerate(self.project[1]):
            self.currentModels[data["name"]] = i
        
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
        self.models = QComboBox()
        self.models.setFixedSize(QSize(self.utilities.computeX(200), self.Y50))
        self.models.addItems(self.currentModels.keys())
        self.models.currentTextChanged.connect(self.setCurrentRules)

        self.rules = QComboBox()
        self.rules.setFixedSize(QSize(self.utilities.computeX(200), self.Y50))
        self.setCurrentRules()

        hbox1.addWidget(self.models)
        hbox1.addWidget(self.rules)

        hbox2 = QHBoxLayout()
        self.testView = QPlainTextEdit()
        self.testView.setFixedSize(QSize(self.utilities.computeX(800), self.utilities.computeY(500)))
        self.testView.setReadOnly(True)

        testBtn = QPushButton('Test', self)
        testBtn.setFixedSize(QSize(self.utilities.computeX(200), self.Y50))
        testBtn.clicked.connect(lambda: self.process(self.npArray))

        hbox2.addWidget(testBtn)
        hbox2.addWidget(self.testView)

        self.layout.addItem(hbox)
        self.layout.addItem(hbox1)
        self.layout.addItem(hbox2)


    def loadDataset(self):
        folder = os.path.expanduser(f"~/Desktop/")
        name = QFileDialog.getOpenFileName(self, 'Load Dataset', folder)
        try:
            df = pd.read_excel(r''+name[0]+'')
            df.fillna(0.00)
            for i, col in enumerate(df.columns):
                self.columns[col] = i
            self.npArray = df.to_numpy()
            self.loadView.setPlainText(df.to_string())
        except:
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Information)
            msg.setText("Failed to load data")
            msg.exec_()

    def process(self, arr):
        selected = self.models.currentText()
        rule = self.rules.currentText()
        if not (selected == '' or rule == ''):
            data = self.project[1][self.currentModels[selected]]
            ruleData = data["rules"][self.rules.currentIndex()]
            interpreted = self.pyInterpreter.interprete(ruleData[2])
            
            headers = ruleData[1].split(',')

            args = []
            for item in arr:
                val = {}
                for x in headers:
                    val[x.strip()] = item[self.columns[x.strip()]]
                args.append(val)

            outputs = []

# create, compile and execute
            func = f"""
def {ruleData[0]}({ruleData[1]}):
    {interpreted}
for cont in {args}:
    outputs.append({ruleData[0]}(**cont))
"""
            exec(compile(func, '', 'exec'))
            result = ''
            for i, param in enumerate(args):
                result += f'{param} -> {outputs[i]}\n'
            
            self.testView.setPlainText(result)


    def setCurrentRules(self):
        self.rules.clear()
        data = self.project[1][self.currentModels[self.models.currentText()]]
        self.rules.addItems([rule[0] for rule in data["rules"]])
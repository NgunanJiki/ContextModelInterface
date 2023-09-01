import os
from PyQt5.QtWidgets import QGroupBox, QFrame, QPlainTextEdit, QVBoxLayout, QHBoxLayout, QScrollArea, QFileDialog, QPushButton
from PyQt5.QtCore import QSize

from model_data import ModelData
from utilities import Utilities

class ModelView(QGroupBox):
    def __init__(self, parentView, project):
        super().__init__()
        self.utilities = Utilities(parentView.app)
        layout = QVBoxLayout()
        layout.setSpacing(self.utilities.computeY(20))

        # add different classes
        for data in project[1]:
            model = ModelData(data["name"], data["description"], data["attributes"], data["rules"])
            model.createModel()

            plainClass = self.createClass(model.getModel())

            export = QPushButton('export', self)
            export.clicked.connect(lambda: self.export(model.getName(), model.getModel()))

            box = QHBoxLayout()
            box.addWidget(plainClass)
            box.addWidget(export)

            layout.addItem(box)

        frame = QFrame()
        # frame.setFrameShape(QFrame.StyledPanel)
        
        frame.setLayout(layout)
        scroll = QScrollArea()
        scroll.setWidget(frame)
        scroll.setWidgetResizable(True)
        vbox = QVBoxLayout()
        vbox.addWidget(scroll)
        self.setTitle(project[0])
        self.setLayout(vbox)

        
    def createClass(self, data):
        text = QPlainTextEdit()
        text.setReadOnly(True)
        text.setFixedSize(QSize(self.utilities.computeX(1000), self.utilities.computeY(1000)))
        text.setPlainText(data)
        return text
    
    def export(self, name, data):
        folder = os.path.expanduser(f"~/Documents/")
        if not os.path.exists(folder):
            os.makedirs(folder)  

        # open file system
        filename = QFileDialog.getSaveFileName(self, 'Export As', f"{folder}{name}", "Java files (*.java)")
        if filename[0] == '':
            return 0    

        # write file
        with open(f"{filename[0]}.java", "w") as file:
            file.write(data)
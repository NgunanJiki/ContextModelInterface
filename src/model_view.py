from PyQt5.QtWidgets import QGroupBox, QFrame, QPlainTextEdit, QVBoxLayout, QScrollArea
from PyQt5.QtCore import QSize

from model_data import ModelData

class ModelView(QGroupBox):
    def __init__(self, project):
        super().__init__()
        layout = QVBoxLayout()
        layout.setSpacing(20)

        # add different classes
        for data in project[1]:
            model = ModelData(data["name"], data["description"], data["attributes"], data["rules"])
            model.createModel()

            plainClass = self.createClass(model.getModel())
            layout.addWidget(plainClass)

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
        text.setFixedSize(QSize(1000, 1000))
        text.setPlainText(data)
        return text
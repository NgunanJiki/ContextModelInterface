from PyQt5.QtWidgets import QGroupBox, QFrame, QPlainTextEdit, QVBoxLayout, QScrollArea
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
        text.setFixedSize(QSize(self.utilities.computeX(1000), self.utilities.computeY(1000)))
        text.setPlainText(data)
        return text
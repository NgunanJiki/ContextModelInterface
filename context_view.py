from PyQt5.QtWidgets import QGridLayout, QPushButton, QFrame, QScrollArea, QVBoxLayout, QWidget
from PyQt5.QtCore import QSize

from context_data import ContextData

class ContextView(QWidget):
    def __init__(self, mainView, contexts):
        super().__init__()
        self.grid = QGridLayout()
        self.mainView = mainView
        self.contexts = contexts

        self.setup()

    def setup(self):
        # add contexts
        for i, data in enumerate(self.contexts):
            ctx = ContextData(self.mainView, i, data["name"], data["attributes"], data["rules"], data["description"])
            self.grid.addWidget(ctx, i-1 if (i>0 and i%2!=0) else i, i%2)

        # add context button
        addContext = QPushButton('Add New', self)
        addContext.setFixedSize(QSize(200, 50))
        addContext.setStyleSheet('border-radius: 50px; border: 2px solid gray')
        addContext.clicked.connect(self.addNew)
        self.grid.addWidget(addContext, self.grid.__len__()-1 if (self.grid.__len__()>0 and self.grid.__len__()%2!=0) else self.grid.__len__(), self.grid.__len__()%2)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setLayout(self.grid)
        frameScroll = QScrollArea()
        frameScroll.setWidget(frame)
        frameScroll.setWidgetResizable(True)
        layout = QVBoxLayout()
        layout.addWidget(frameScroll)
        self.setLayout(layout)

    # add empty context
    def addNew(self):
        self.mainView.projects[self.mainView.currentIndex][1].append({"name": "", "attributes": [], "rules": [], "description": "" })
        self.mainView.setProject(self.mainView.currentIndex, self.mainView.settings["tab"])

from PyQt5.QtWidgets import QPlainTextEdit, QPushButton, QFrame, QScrollArea, QVBoxLayout, QHBoxLayout, QGroupBox
from PyQt5.QtCore import QSize

from context_data import ContextData
from utilities import Utilities

class ContextView(QGroupBox):
    def __init__(self, mainView, contexts):
        super().__init__()
        self.utilities = Utilities(mainView.app)
        self.Y50 = self.utilities.computeY(50)
        self.X50 = self.utilities.computeX(50)
        # self.grid = QGridLayout()
        self.listBox = QVBoxLayout()
        self.listBox.setSpacing(self.Y50)
        self.mainView = mainView
        self.contexts = contexts

        self.setup()

    def setup(self):
        # add contexts
        for i, data in enumerate(self.contexts):
            ctx = ContextData(self.mainView, i, data["name"], data["attributes"], data["rules"], data["description"])
            # self.grid.addWidget(ctx, i-1 if (i>0 and i%2!=0) else i, i%2)
            self.listBox.addWidget(ctx)

        # add context button
        addContext = QPushButton('Add New', self)
        addContext.setFixedSize(QSize(self.utilities.computeX(200), self.Y50))
        addContext.clicked.connect(self.addNew)
        # self.grid.addWidget(addContext, self.grid.__len__()-1 if (self.grid.__len__()>0 and self.grid.__len__()%2!=0) else self.grid.__len__(), self.grid.__len__()%2)
        self.listBox.addWidget(addContext)

        instructions = QPlainTextEdit()
        instructions.setFixedWidth(self.utilities.computeX(500))
        # instructions.setFixedSize(QSize(self.utilities.computeX(600), self.utilities.computeY(1000)))
        instructions.setReadOnly(True)
        instructions.setPlainText(self.utilities.getManual())

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setLayout(self.listBox)
        frameScroll = QScrollArea()
        frameScroll.setWidget(frame)
        frameScroll.setWidgetResizable(True)
        layout = QHBoxLayout()
        layout.addWidget(frameScroll)
        layout.addWidget(instructions)

        self.setTitle(self.mainView.projects[self.mainView.currentIndex][0])
        self.setLayout(layout)

    # add empty context
    def addNew(self):
        self.mainView.projects[self.mainView.currentIndex][1].append({"name": "", "attributes": [], "rules": [], "description": "" })
        self.mainView.setProject(self.mainView.currentIndex, self.mainView.settings["tab"])

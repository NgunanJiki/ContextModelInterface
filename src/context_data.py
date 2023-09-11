from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QTextEdit, QPlainTextEdit, QComboBox, QPushButton, QHBoxLayout, QScrollArea, QFrame
from PyQt5.QtCore import QSize

from utilities import Utilities

class ContextData(QScrollArea):
    def __init__(self, parentView, listIndex, name, attributes, rules, description = ''):
        super().__init__()
        self.utilities = Utilities(parentView.app)
        self.Y50 = self.utilities.computeY(50)
        self.X50 = self.utilities.computeX(50)
        self.parentView = parentView
        self.listIndex = listIndex
        self.name = name
        self.attributes = attributes
        self.rules = rules
        self.description = description
        self.attrBox = QVBoxLayout()
        self.ruleBox = QVBoxLayout()

        self.textEdit = QTextEdit()
        self.desc = QTextEdit()

        self.attrs = []
        self.types = []

        self.ruleNames = []
        self.parameters = []
        self.modelLogic = []
        self.returnTypes = []
        
        self.setup()

    def setup(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Context'))
        
        self.textEdit.setText(self.name)
        self.textEdit.setFixedHeight(self.Y50)
        self.textEdit.textChanged.connect(self.makeUpdates)
        layout.addWidget(self.textEdit)

        layout.addWidget(QLabel('Description'))
        
        self.desc.setText(self.description)
        self.desc.setFixedHeight(self.utilities.computeY(100))
        self.desc.textChanged.connect(self.makeUpdates)
        layout.addWidget(self.desc)

        layout.addWidget(QLabel('Attributes'))
        add = QPushButton('+', self)
        add.setFixedSize(QSize(self.X50, self.Y50))
        add.clicked.connect(lambda: self.addAtribute('', ''))
        attrOutbox = QVBoxLayout()

        for it in self.attributes:
            self.addAtribute(it[0], it[1])
        
        attrOutbox.addLayout(self.attrBox)
        attrOutbox.addWidget(add)
        layout.addLayout(attrOutbox)

        layout.addWidget(QLabel('Rules'))
        makeRule = QPushButton('+', self)
        makeRule.setFixedSize(QSize(self.X50, self.Y50))
        makeRule.clicked.connect(lambda: self.addRule('', '', '', ''))
        ruleOutbox = QVBoxLayout()

        for rule in self.rules:
            self.addRule(rule[0], rule[1], rule[2], rule[3])

        ruleOutbox.addLayout(self.ruleBox)
        ruleOutbox.addWidget(makeRule)
        layout.addLayout(ruleOutbox)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setLayout(layout)

        self.setWidget(frame)
        self.setWidgetResizable(True)
        self.setFixedHeight(self.utilities.computeY(900))
        self.setFixedWidth(self.utilities.computeX(800))

    def addAtribute(self, attribute, typeValue):
        index = self.attrBox.__len__()
        attr = QTextEdit()
        self.attrs.append(attr)
        attr.setText(attribute)
        attr.setFixedHeight(self.Y50)
        attr.textChanged.connect(self.makeUpdates)
        attr.setPlaceholderText('attribute')
        

        type = QComboBox()
        self.types.append(type)
        type.addItems(['text', 'number'])
        type.setEditable(True)
        type.setEditText(typeValue)
        type.setFixedHeight(self.Y50)
        type.editTextChanged.connect(self.makeUpdates)
        type.setPlaceholderText('type')

        remove = QPushButton('x', self)
        remove.setFixedSize(QSize(self.X50, self.Y50))

        layoutbox = QHBoxLayout()
        layoutbox.addWidget(attr)
        layoutbox.addWidget(type)
        layoutbox.addWidget(remove)
        self.attrBox.addLayout(layoutbox)
        layoutbox.itemAt(0).widget()
        remove.clicked.connect(lambda: self.removeAttribute(layoutbox))
        

    def removeAttribute(self, layoutbox):
        self.attrs.remove(layoutbox.itemAt(0).widget())
        self.types.remove(layoutbox.itemAt(1).widget())
        self.deleteItemsOfLayout(layoutbox.layout())
        self.attrBox.removeItem(layoutbox.layout())
        self.makeUpdates()

    def addRule(self, ruleName, paramList, contextLogic, output):
        index = self.ruleBox.__len__()
        rule = QTextEdit()
        nameBox = QHBoxLayout()
        nameBox.addWidget(QLabel('name: '))
        nameBox.addWidget(rule)
        self.ruleNames.append(nameBox)
        rule.setText(ruleName)
        rule.setFixedHeight(self.Y50)
        rule.textChanged.connect(self.makeUpdates)
        rule.setPlaceholderText('name')

        params = QTextEdit()
        paramBox = QHBoxLayout()
        paramBox.addWidget(QLabel('params: '))
        paramBox.addWidget(params)
        self.parameters.append(paramBox)
        params.setText(paramList)
        params.setFixedHeight(self.Y50)
        params.textChanged.connect(self.makeUpdates)
        params.setPlaceholderText('input1, input2, ...')

        logic = QPlainTextEdit()
        logic.setFixedSize(QSize(self.utilities.computeX(500), self.utilities.computeY(400)))
        logicBox = QHBoxLayout()
        logicBox.addWidget(QLabel('logic: '))
        logicBox.addWidget(logic)
        self.modelLogic.append(logicBox)
        logic.setPlainText(contextLogic)
        logic.textChanged.connect(self.makeUpdates)
        logic.setPlaceholderText('model logic')

        returnType = QTextEdit()
        returnBox = QHBoxLayout()
        returnBox.addWidget(QLabel('output type: '))
        returnBox.addWidget(returnType)
        self.returnTypes.append(returnBox)
        returnType.setText(output)
        returnType.setFixedHeight(self.Y50)
        returnType.textChanged.connect(self.makeUpdates)
        returnType.setPlaceholderText('output type')

        remove = QPushButton('x', self)
        remove.setFixedSize(QSize(self.X50, self.Y50))

        layoutbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addItem(nameBox)
        hbox.addWidget(remove)
        layoutbox.addItem(hbox)
        layoutbox.addItem(paramBox)
        layoutbox.addItem(logicBox)
        layoutbox.addItem(returnBox)
        self.ruleBox.addLayout(layoutbox)

        remove.clicked.connect(lambda: self.removeRule(layoutbox.layout()))

    def removeRule(self, layoutbox):
        self.ruleNames.remove(layoutbox.itemAt(0).itemAt(0))
        self.parameters.remove(layoutbox.itemAt(1))
        self.modelLogic.remove(layoutbox.itemAt(2))
        self.returnTypes.remove(layoutbox.itemAt(3))
        self.deleteItemsOfLayout(layoutbox.layout())
        self.ruleBox.removeItem(layoutbox.layout())
        self.makeUpdates()

    # send updates to parent view
    def makeUpdates(self):
        attributes = []
        for i, att in enumerate(self.attrs):
            attributes.append([self.attrs[i].toPlainText(), self.types[i].currentText()])
        rules = []
        for i, rul in enumerate(self.ruleNames):
            rules.append([self.ruleNames[i].itemAt(1).widget().toPlainText(), self.parameters[i].itemAt(1).widget().toPlainText(), self.modelLogic[i].itemAt(1).widget().toPlainText(), self.returnTypes[i].itemAt(1).widget().toPlainText()])

        self.parentView.updateProject(
            self.listIndex,
            self.textEdit.toPlainText(), 
            attributes, 
            rules, 
            self.desc.toPlainText(),
        )

    # clear layout recursively
    def deleteItemsOfLayout(self, layout):
        if layout is not None:
            while layout.count():
                item = layout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.setParent(None)
                else:
                    self.deleteItemsOfLayout(item.layout())
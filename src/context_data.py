from PyQt5.QtWidgets import QGroupBox, QVBoxLayout, QLabel, QTextEdit, QComboBox, QPushButton, QHBoxLayout, QScrollArea, QFrame
from PyQt5.QtCore import QSize

from utilities import Utilities

class ContextData(QGroupBox):
    def __init__(self, parentView, listIndex, name, attributes, rules, description = ''):
        super().__init__()
        self.utilities = Utilities(parentView.app)
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
        self.returnTypes = []
        
        self.setup()

    def setup(self):
        layout = QVBoxLayout()
        layout.addWidget(QLabel('Context'))
        
        self.textEdit.setText(self.name)
        self.textEdit.setFixedHeight(self.utilities.computeY(50))
        self.textEdit.textChanged.connect(self.makeUpdates)
        layout.addWidget(self.textEdit)

        layout.addWidget(QLabel('Description'))
        
        self.desc.setText(self.description)
        self.desc.setFixedHeight(300)
        self.desc.textChanged.connect(self.makeUpdates)
        layout.addWidget(self.desc)

        layout.addWidget(QLabel('Attributes'))
        add = QPushButton('+', self)
        add.setFixedSize(QSize(self.utilities.computeX(50), self.utilities.computeY(50)))
        add.setStyleSheet('border-radius: 50px; border: 2px solid black')
        add.clicked.connect(lambda: self.addAtribute('', ''))
        attrOutbox = QVBoxLayout()

        for it in self.attributes:
            self.addAtribute(it[0], it[1])
        
        attrOutbox.addLayout(self.attrBox)
        attrOutbox.addWidget(add)
        layout.addLayout(attrOutbox)

        layout.addWidget(QLabel('Rules'))
        makeRule = QPushButton('+', self)
        makeRule.setFixedSize(QSize(self.utilities.computeX(50), self.utilities.computeY(50)))
        makeRule.setStyleSheet('border-radius: 50px; border: 2px solid black')
        makeRule.clicked.connect(lambda: self.addRule('', '', ''))
        ruleOutbox = QVBoxLayout()

        for rule in self.rules:
            self.addRule(rule[0], rule[1], rule[2])

        ruleOutbox.addLayout(self.ruleBox)
        ruleOutbox.addWidget(makeRule)
        layout.addLayout(ruleOutbox)

        frame = QFrame()
        frame.setFrameShape(QFrame.StyledPanel)
        frame.setLayout(layout)

        scroll = QScrollArea()
        scroll.setWidget(frame)
        scroll.setWidgetResizable(True)
        hbox = QVBoxLayout()
        hbox.addWidget(scroll)
        self.setLayout(hbox)
        self.setFixedHeight(self.utilities.computeY(800))
        self.setFixedWidth(self.utilities.computeX(1000))

    def addAtribute(self, attribute, typeValue):
        index = self.attrBox.__len__()
        attr = QTextEdit()
        self.attrs.append(attr)
        attr.setText(attribute)
        attr.setFixedHeight(self.utilities.computeY(50))
        attr.textChanged.connect(self.makeUpdates)
        attr.setPlaceholderText('attribute')
        

        type = QComboBox()
        self.types.append(type)
        type.addItems(['text', 'number'])
        type.setEditable(True)
        type.setEditText(typeValue)
        type.setFixedHeight(self.utilities.computeY(50))
        type.editTextChanged.connect(self.makeUpdates)
        type.setPlaceholderText('type')

        remove = QPushButton('x', self)
        remove.setFixedSize(QSize(self.utilities.computeX(50), self.utilities.computeY(50)))
        remove.setStyleSheet('border-radius: 50px; border: 2px solid gray')

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

    def addRule(self, ruleName, paramList, output):
        index = self.ruleBox.__len__()
        rule = QTextEdit()
        self.ruleNames.append(rule)
        rule.setText(ruleName)
        rule.setFixedHeight(self.utilities.computeY(50))
        rule.textChanged.connect(self.makeUpdates)
        rule.setPlaceholderText('name')

        params = QTextEdit()
        self.parameters.append(params)
        params.setText(paramList)
        params.setFixedHeight(self.utilities.computeY(50))
        params.textChanged.connect(self.makeUpdates)
        params.setPlaceholderText('input1, input2, ...')

        returnType = QTextEdit()
        self.returnTypes.append(returnType)
        returnType.setText(output)
        returnType.setFixedHeight(self.utilities.computeY(50))
        returnType.textChanged.connect(self.makeUpdates)
        returnType.setPlaceholderText('output type')

        remove = QPushButton('x', self)
        remove.setFixedSize(QSize(self.utilities.computeX(50), self.utilities.computeY(50)))
        remove.setStyleSheet('border-radius: 50px; border: 2px solid gray')

        layoutbox = QVBoxLayout()
        hbox = QHBoxLayout()
        hbox.addWidget(rule)
        hbox.addWidget(remove)
        layoutbox.addItem(hbox)
        layoutbox.addWidget(params)
        layoutbox.addWidget(returnType)
        self.ruleBox.addLayout(layoutbox)

        remove.clicked.connect(lambda: self.removeRule(layoutbox.layout()))

    def removeRule(self, layoutbox):
        self.ruleNames.remove(layoutbox.itemAt(0).itemAt(0).widget())
        self.parameters.remove(layoutbox.itemAt(1).widget())
        self.returnTypes.remove(layoutbox.itemAt(2).widget())
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
            rules.append([self.ruleNames[i].toPlainText(), self.parameters[i].toPlainText(), self.returnTypes[i].toPlainText()])

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
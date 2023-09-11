from PyQt5.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLabel

class ConfirmExit(QDialog):
    def __init__(self, mainParent):
        super().__init__()
        self.mainParent = mainParent
        self.setWindowTitle("Save Projects")

        btns = QDialogButtonBox.Discard | QDialogButtonBox.Cancel | QDialogButtonBox.SaveAll
        self.btnBox = QDialogButtonBox(btns)
        self.btnBox.clicked.connect(self.processAction)

        msg = QLabel("Usaved work!, Save?")

        layout = QVBoxLayout()
        layout.addWidget(msg)
        layout.addWidget(self.btnBox)

        self.setLayout(layout)

    def processAction(self, btn):
        if (btn == self.btnBox.button(QDialogButtonBox.SaveAll)):
            self.mainParent.save()
            self.accept()
        elif (btn == self.btnBox.button(QDialogButtonBox.Discard)):
            self.accept()
        else:
            self.reject()
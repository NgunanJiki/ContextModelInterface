import sys

from PyQt5.QtWidgets import QApplication
from view import View

if __name__ == "__main__":
    app = QApplication(sys.argv)

    # main view
    view = View(app)
    view.show()

    sys.exit(app.exec_())
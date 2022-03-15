import sys
from PySide2.QtWidgets import *
from test_window import TestWindow


if __name__ == '__main__':
    app = QApplication(sys.argv)
    wnd = TestWindow()
    wnd.show()

    sys.exit(app.exec_())
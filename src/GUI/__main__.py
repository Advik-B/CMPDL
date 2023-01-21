from PyQt6.QtWidgets import QApplication, QMainWindow

app = QApplication([])

window = QMainWindow()
window.resize(250, 150)
window.setWindowTitle("CMPDL")
window.show()

app.exec()

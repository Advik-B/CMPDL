from PyQt6.QtWidgets import QApplication, QWidget, QLabel
from qt_material import apply_stylesheet

app = QApplication([])
window = QWidget()
label = QLabel('Hello World', window)
label.move(50, 30)
apply_stylesheet(app, theme='dark_blue.xml')
window.show()
app.exec()
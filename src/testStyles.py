from PyQt6.QtWidgets import QApplication, QWidget, QFontComboBox
from qt_material import apply_stylesheet

app = QApplication([])
window = QWidget()
combo = QFontComboBox(window)
combo.move(50, 50)

apply_stylesheet(app, theme='dark_blue.xml')
window.show()
app.exec()

import os
from PySide2.QtGui import *
from PySide2.QtCore import *
from PySide2.QtWidgets import *
from main_window import MainWindow


class TestWindow(MainWindow):

    def initUI(self):

        self.initDocks()

        self.mdiArea = QMdiArea()
        self.mdiArea.setHorizontalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setVerticalScrollBarPolicy(Qt.ScrollBarAsNeeded)
        self.mdiArea.setViewMode(QMdiArea.TabbedView)
        self.mdiArea.setDocumentMode(True)
        self.mdiArea.setTabsClosable(True)
        self.mdiArea.setTabsMovable(True)
        self.setCentralWidget(self.mdiArea)

        child = MainContent(self)
        w1 = self.mdiArea.addSubWindow(QLabel())
        w1.setWindowTitle("QLabel")
        w1.setWindowIcon(QIcon("."))    # using non-existing icon disables the icon
        w2 = self.mdiArea.addSubWindow(QTextEdit())
        w2.setWindowTitle("QTextEdit")
        w2.setWindowIcon(QIcon("."))
        w3 = self.mdiArea.addSubWindow(QTextEdit())
        w3.setWindowTitle("QTextEdit")
        w3.setWindowIcon(QIcon("."))
        swnd = self.mdiArea.addSubWindow(child)
        swnd.setWindowIcon(QIcon("."))

        super().initUI()

        swnd.setWindowTitle("Demo Widgets")

    def initActions(self):
        super().initActions()
        self.actTile = QAction("&Tile", self, statusTip="Tile the windows", triggered=self.mdiArea.tileSubWindows)
        self.actCascade = QAction("&Cascade", self, statusTip="Cascade the windows", triggered=self.mdiArea.cascadeSubWindows)


    def initMenus(self):
        super().initMenus()
        self.windowMenu = self.menuBar().addMenu("&Window")
        self.windowMenu.addAction(self.actTile)
        self.windowMenu.addAction(self.actCascade)

    def initDocks(self):
        dock = QDockWidget("Files", self)
        dock.setWidget(self.createFilesDock())
        self.addDockWidget(Qt.LeftDockWidgetArea, dock)

        dock3 = QDockWidget("Foo", self)
        dock3.setWidget(QTextEdit())
        self.addDockWidget(Qt.LeftDockWidgetArea, dock3)

        dock2 = QDockWidget("Files2", self)
        dock2.setWidget(self.createFilesDock())
        self.addDockWidget(Qt.LeftDockWidgetArea, dock2)
        self.tabifyDockWidget(dock2, dock)

    def createFilesDock(self):
        wdg = QWidget()
        lay = QVBoxLayout(wdg)
        lay.setContentsMargins(QMargins(0, 0, 0, 0))

        lw = QListWidget()
        lw.setAlternatingRowColors(True)
        lay.addWidget(lw)
        for i in range(7): lw.addItem(QListWidgetItem("Item %d" % i))

        tw = QTreeWidget()
        tw.setHeaderItem(QTreeWidgetItem(["Name", "Options"]))
        lay.addWidget(tw)
        tw.setAlternatingRowColors(True)

        root = QTreeWidgetItem(tw, ["Tree Items", "our items"])
        root.setData(2, Qt.EditRole, 'Some hidden data here')
        for i in range(4):
            itm = QTreeWidgetItem(root, ["Item %d" % i, ""])
            itm.setData(2, Qt.EditRole, 'Some hidden data here')

        for i in range(3):
            dir = QTreeWidgetItem(tw, ["Dir%d" % i, ""])
            for j in range(2 - i):
                sd = QTreeWidgetItem(dir, ["SubDir%d" % j, ""])
                for k in range(3): QTreeWidgetItem(sd, ["SubItem %d" % (k + 1)])

        return wdg



class MainContent(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.initUI()

    def initUI(self):
        self.createBasicLayout()
        self.createBottomContent()
        self.createLeftContent()
        self.createRightContent()


    def createBottomContent(self):
        lay = QHBoxLayout(self.bottom)

        lay.addWidget(QLabel("Select active QSS Skin"))

        lay.addWidget(self.parent().createComboBoxWithQSSStyleSheets())

        lay.addWidget(QLabel(""))
        qpb = QPushButton("Reload QSS Skins List")
        qpb.clicked.connect(self.parent().refreshSkinCombo)
        lay.addWidget(qpb)

        lay.addStretch()

    def createLeftContent(self):
        main_layout = QHBoxLayout(self.topleft)

        # left part
        wdg_left = QWidget()
        lay = QVBoxLayout(wdg_left)
        main_layout.addWidget(wdg_left)

        ql = QLabel("Simple QLabel")
        ql.setObjectName("Example")
        lay.addWidget(ql)
        lay.addWidget(QLineEdit("Some text in QLineEdit..."))
        qle = QLineEdit("Another QLineEdit here...")
        # qle.setAttribute(Qt.WA_MacShowFocusRect, False)
        # qle.setFrame(False)
        lay.addWidget(qle)
        lay.addWidget(QSpinBox())
        lay.addWidget(QPushButton("QPushButton"))
        qpb = QPushButton("QPushButton#danger")
        qpb.setObjectName("danger")
        lay.addWidget(qpb)
        cb1 = QCheckBox("QCheckBox")
        cb1.setChecked(True)
        lay.addWidget(cb1)
        lay.addWidget(QCheckBox("QCheckBox2"))
        lay.addWidget(QCheckBox("QCheckBox3"))
        lay.addWidget(QRadioButton("QRadioButton1"))
        rb2 = QRadioButton("QRadioButton2")
        rb2.setChecked(True)
        lay.addWidget(rb2)
        lay.addWidget(QRadioButton("QRadioButton3"))

        combo_box = QComboBox()
        combo_box.addItems(["Option 1", "Option 2", "Option 3"])
        lay.addWidget(combo_box)
        qtex = QTextEdit("Some TextEdit text for editing...")
        qtex.setMaximumHeight(50)
        lay.addWidget(qtex)


        lay.addStretch()

        # right part
        wdg_right = QWidget()
        lay = QHBoxLayout(wdg_right)
        main_layout.addWidget(wdg_right)

        qs = QSlider(Qt.Vertical)
        qs.setValue(50)
        lay.addWidget(qs)
        qsc = QScrollBar(Qt.Vertical)
        qsc.setValue(50)
        lay.addWidget(qsc)



    def createRightContent(self):
        lay = QVBoxLayout(self.topright)

        qs = QSlider(Qt.Horizontal)
        qs.setValue(50)
        lay.addWidget(qs)
        qpb = QProgressBar()
        qpb.setValue(50)
        lay.addWidget(qpb)
        qsc = QScrollBar(Qt.Horizontal)
        qsc.setValue(50)
        lay.addWidget(qsc)

        lay.addSpacing(10)

        tw = QTabWidget()
        tw.addTab(QLabel(), "Tab1")
        tw.addTab(QLabel(), "Tab2 Super Name")
        tw.addTab(QLabel(), "Tab3")
        lay.addWidget(tw)

        lay.addWidget(QLabel("Another label"))

        lay.addStretch()


    def createBasicLayout(self):
        self.hbox = QHBoxLayout(self)
        self.hbox.setContentsMargins(QMargins(0, 0, 0, 0))

        self.topleft = QFrame(self)
        self.topleft.setFrameShape(QFrame.StyledPanel)
        self.topleft.setMinimumWidth(300)

        self.topright = QFrame(self)
        self.topright.setMinimumWidth(250)
        self.topright.setMaximumWidth(450)
        self.topright.setFrameShape(QFrame.StyledPanel)


        self.bottom = QFrame(self)
        self.bottom.setFrameShape(QFrame.StyledPanel)
        self.bottom.setMaximumHeight(100)

        self.splitter1 = QSplitter(Qt.Horizontal)
        self.splitter1.addWidget(self.topleft)
        self.splitter1.addWidget(self.topright)

        self.splitter2 = QSplitter(Qt.Vertical)
        self.splitter2.setContentsMargins(QMargins(0, 0, 0, 0))
        self.splitter2.addWidget(self.splitter1)
        self.splitter2.addWidget(self.bottom)

        self.hbox.addWidget(self.splitter2)
        self.setLayout(self.hbox)

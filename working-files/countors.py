"""
@file motion_detector_contours.py
@brief Script for setting ROI for Motion Detector by image.

@author Vitaly Streshchuk, Grovety Inc, agency@grovety.com
"""

import sys

from PyQt5 import QtCore, QtGui, QtWidgets
from PyQt5.QtCore import QCoreApplication, QMetaObject, QPoint, QSize, Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import *

cb = None


class UI(object):
    def setupUi(self, MainWindow):
        if MainWindow.objectName():
            MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 800)
        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.verticalLayout_2 = QVBoxLayout(self.centralwidget)
        self.verticalLayout_2.setObjectName("verticalLayout_2")
        self.verticalLayout = QVBoxLayout()
        self.verticalLayout.setSpacing(5)
        self.verticalLayout.setObjectName("verticalLayout")
        self.verticalLayout_3 = QVBoxLayout()
        self.verticalLayout_3.setObjectName("verticalLayout_3")
        self.lblImage = QLabel(self.centralwidget)
        self.lblImage.setObjectName("lblImage")
        self.lblImage.setMinimumSize(QSize(400, 600))
        self.lblImage.setAlignment(Qt.AlignTop | Qt.AlignHCenter)
        self.verticalLayout_3.addWidget(self.lblImage)
        self.groupBox = QGroupBox(self.centralwidget)
        self.groupBox.setObjectName("groupBox")
        self.verticalLayout_5 = QVBoxLayout(self.groupBox)
        self.verticalLayout_5.setObjectName("verticalLayout_5")
        self.verticalLayout_4 = QVBoxLayout()
        self.verticalLayout_4.setObjectName("verticalLayout_4")
        self.horizontalLayout = QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label_3 = QLabel(self.groupBox)
        self.label_3.setObjectName("label_3")
        self.horizontalLayout.addWidget(self.label_3)
        self.lineFile = QLineEdit(self.groupBox)
        self.lineFile.setObjectName("lineFile")
        self.lineFile.setEnabled(False)
        self.lineFile.setMinimumSize(QSize(0, 30))
        self.horizontalLayout.addWidget(self.lineFile)
        self.btnOpen = QPushButton(self.groupBox)
        self.btnOpen.setObjectName("btnOpen")
        self.btnOpen.setMinimumSize(QSize(60, 30))
        self.btnOpen.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout.addWidget(self.btnOpen)
        self.verticalLayout_4.addLayout(self.horizontalLayout)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName("verticalLayout_8")
        self.label_6 = QLabel(self.groupBox)
        self.label_6.setObjectName("label_6")
        self.verticalLayout_8.addWidget(self.label_6)
        self.btnDrawLine = QPushButton(self.groupBox)
        self.btnDrawLine.setObjectName("btnDrawLine")
        self.btnDrawLine.setMinimumSize(QSize(60, 30))
        self.btnDrawLine.setMaximumSize(QSize(16777215, 30))
        self.verticalLayout_8.addWidget(self.btnDrawLine)
        self.btnClear = QPushButton(self.groupBox)
        self.btnClear.setObjectName("btnClear")
        self.btnClear.setMinimumSize(QSize(60, 30))
        self.btnClear.setMaximumSize(QSize(16777215, 30))
        self.verticalLayout_8.addWidget(self.btnClear)
        self.btnDone = QPushButton(self.groupBox)
        self.btnDone.setObjectName("btnDone")
        self.btnDone.setMinimumSize(QSize(60, 30))
        self.btnDone.setMaximumSize(QSize(16777215, 30))
        self.verticalLayout_8.addWidget(self.btnDone)
        self.btnExit = QPushButton(self.groupBox)
        self.btnExit.setObjectName("btnExit")
        self.btnExit.setMinimumSize(QSize(60, 30))
        self.btnExit.setMaximumSize(QSize(16777215, 30))
        self.verticalLayout_8.addWidget(self.btnExit)
        self.horizontalLayout_2.addLayout(self.verticalLayout_8)
        self.verticalLayout_6 = QVBoxLayout()
        self.verticalLayout_6.setObjectName("verticalLayout_6")
        self.label_5 = QLabel(self.groupBox)
        self.label_5.setObjectName("label_5")
        self.verticalLayout_6.addWidget(self.label_5)
        self.textResults = QTextEdit(self.groupBox)
        self.textResults.setObjectName("textResults")
        self.textResults.setMaximumSize(QSize(16777215, 100))
        self.verticalLayout_6.addWidget(self.textResults)
        self.horizontalLayout_3 = QHBoxLayout()
        self.horizontalLayout_3.setObjectName("horizontalLayout_3")
        self.btnCopy = QPushButton(self.groupBox)
        self.btnCopy.setObjectName("btnCopy")
        self.btnCopy.setMinimumSize(QSize(60, 30))
        self.btnCopy.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_3.addWidget(self.btnCopy)
        self.btnClearResults = QPushButton(self.groupBox)
        self.btnClearResults.setObjectName("btnClearResults")
        self.btnClearResults.setMinimumSize(QSize(60, 30))
        self.btnClearResults.setMaximumSize(QSize(16777215, 30))
        self.horizontalLayout_3.addWidget(self.btnClearResults)
        self.verticalLayout_6.addLayout(self.horizontalLayout_3)
        self.horizontalLayout_2.addLayout(self.verticalLayout_6)
        self.verticalLayout_4.addLayout(self.horizontalLayout_2)
        self.verticalLayout_5.addLayout(self.verticalLayout_4)
        self.verticalLayout_3.addWidget(self.groupBox)
        self.verticalLayout.addLayout(self.verticalLayout_3)
        self.verticalLayout_2.addLayout(self.verticalLayout)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(QCoreApplication.translate("MainWindow", "CARTZY - Motion Detector", None))
        self.lblImage.setText(QCoreApplication.translate("MainWindow", "", None))
        self.groupBox.setTitle(QCoreApplication.translate("MainWindow", "Processing", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", "Image: ", None))
        self.btnOpen.setText(QCoreApplication.translate("MainWindow", "Open", None))
        self.label_6.setText(QCoreApplication.translate("MainWindow", "Control", None))
        self.btnDrawLine.setText(QCoreApplication.translate("MainWindow", "Draw Line", None))
        self.btnClear.setText(QCoreApplication.translate("MainWindow", "Clear", None))
        self.btnDone.setText(QCoreApplication.translate("MainWindow", "Done", None))
        self.btnExit.setText(QCoreApplication.translate("MainWindow", "Exit", None))
        self.label_5.setText(QCoreApplication.translate("MainWindow", "Results", None))
        self.btnCopy.setText(QCoreApplication.translate("MainWindow", "Copy", None))
        self.btnClearResults.setText(QCoreApplication.translate("MainWindow", "Clear", None))


class MainWindow(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        super(MainWindow, self).__init__(parent=parent)
        self.ui = UI()
        self.ui.setupUi(self)
        self.setFixedSize(800, 800)
        # Signals/Slots
        self.ui.btnOpen.clicked.connect(self.openFileClicked)
        self.ui.btnClear.clicked.connect(self.clearClicked)
        self.ui.btnDrawLine.clicked.connect(self.drawClicked)
        self.ui.btnDone.clicked.connect(self.doneClicked)
        self.ui.btnClearResults.clicked.connect(self.clearResultsClicked)
        self.ui.btnCopy.clicked.connect(self.copyClicked)
        self.ui.btnExit.clicked.connect(self.exitClicked)
        self.image = None
        self.drawing = False
        self.last_point = None
        self.currentPos = None
        self.mouse_click = False
        self.values = []

    def clearResultsClicked(self):
        self.ui.textResults.clear()

    def openFileClicked(self):
        fname, _ = QFileDialog.getOpenFileName(None, "Open File", "", "Image files (*.jpg *.gif *.png)")

        if fname == "":
            return

        self.image = QtGui.QPixmap(fname)
        self.scaled_image = self.image.scaled(self.ui.lblImage.size(), QtCore.Qt.KeepAspectRatio)
        self.ui.lblImage.setPixmap(self.scaled_image)
        self.ui.lineFile.setText(fname)

    def clearClicked(self):
        if self.scaled_image:
            self.ui.lblImage.setPixmap(self.scaled_image)
            self.last_point = None
            self.currentPos = None
            self.values.clear()

    def copyClicked(self):
        cb.setText(self.ui.textResults.toPlainText())

    def doneClicked(self):
        out = "["

        h_k = self.scaled_image.height() / self.image.height()
        h_w = self.scaled_image.width() / self.image.width()

        for i in range(len(self.values) - 1):
            out += f"[{int(self.values[i][0] / h_w)}, {int(self.values[i][1] / h_k)}], "

        out += f"[{int(self.values[-1][0] / h_w)}, {int(self.values[-1][1] / h_k)}]]"

        self.ui.textResults.setText(out)
        self.drawClicked()

    def drawClicked(self):
        if self.drawing:
            self.drawing = False
            self.ui.btnDrawLine.setText("Draw Line")
        else:
            self.drawing = True
            self.ui.btnDrawLine.setText("Stop")

    def exitClicked(self):
        QCoreApplication.quit()

    def paintEvent(self, event):
        if self.image and self.drawing and self.mouse_click:
            if self.currentPos:
                draw_pos_x = self.currentPos.x() - self.ui.lblImage.x()
                draw_pos_y = self.currentPos.y() - self.ui.lblImage.y()
                self.currentPos = QPoint(draw_pos_x, draw_pos_y)

                if (
                    draw_pos_x > self.scaled_image.width()
                    or draw_pos_x < 0
                    or draw_pos_y > self.scaled_image.height()
                    or draw_pos_y < 0
                ):
                    return

                if self.last_point:
                    q = QPainter(self.ui.lblImage.pixmap())
                    pen = QtGui.QPen()
                    pen.setWidth(3)
                    pen.setColor(QtGui.QColor("red"))
                    q.setPen(pen)
                    q.drawLine(self.last_point, self.currentPos)
                    self.last_point = self.currentPos
                    self.values.append([draw_pos_x, draw_pos_y])
                    self.mouse_click = False
                else:
                    self.last_point = self.currentPos

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton and self.drawing:
            self.currentPos = event.pos()
            self.update()
            self.mouse_click = True


if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    cb = QtWidgets.QApplication.clipboard()
    w = MainWindow()
    w.show()
    sys.exit(app.exec_())

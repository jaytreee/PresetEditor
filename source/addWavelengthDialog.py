# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addWavelengthDialog.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_AddWLDialog(object):
    def setupUi(self, AddWLDialog):
        AddWLDialog.setObjectName("AddWLDialog")
        AddWLDialog.resize(313, 152)
        AddWLDialog.setStyleSheet("QPlainTextEdit {\n"
"    font-family: \"Lucida Console\",\"Courier\";\n"
"    font-size: 9pt; \n"
"    background-color: #262626;\n"
"    selection-background-color: #2e5ea4;\n"
"/*    color: #dddddd;  */\n"
"}\n"
"QWidget:focus {\n"
"    border: 1px solid #2e5ea4;\n"
"}\n"
"\n"
"QTapWidget{\n"
"    border: 1px solid #2e5ea4;\n"
"}\n"
"QPushButton:pressed {\n"
"    background-color: #2e5ea4; \n"
"    border: 1px solid #2e5ea4;\n"
"    color: #ffffff;\n"
"}\n"
"/*QPushButton:flat {\n"
"    background-color: #666666;\n"
"    color: #ff0000;    \n"
"    border: 1px solid #cccccc;\n"
"}\n"
"QPushButton:default {\n"
"    background-color: #ff0000;\n"
"    color: #ff0000;    \n"
"    border: 1px solid #000000;\n"
"}*/\n"
"QPushButton {\n"
"    color: #cccccc;    \n"
"    border: 1px solid #888888;\n"
"    background: #ff0000;\n"
"    padding: 2px\n"
"} \n"
"QWidget {\n"
"    background: #222222;\n"
"    color: #cccccc;\n"
"}\n"
"\n"
"QTreeView::item:has-children {\n"
"    font-weight: bold;\n"
"}\n"
"QTreeView::item:selected {\n"
"     background-color: #2e5ea4;\n"
"     color: #cccccc;\n"
"     font-weight: bold;\n"
"}\n"
"\n"
"QTreeView::branch {\n"
"    background-color: #222222;\n"
"}\n"
"\n"
"QTabBar::tab {\n"
"    background: #222222;   \n"
"    border: 2px solid #cccccc;\n"
"    border-bottom-color: #cccccc; /* same as the pane color */\n"
"    border-top-left-radius: 4px;\n"
"    border-top-right-radius: 4px;\n"
"    min-width: 8ex;\n"
"    padding: 2px;\n"
"}\n"
"\n"
"QTabBar::tab:selected {\n"
"    background: #2e5ea4\n"
"    }\n"
"")
        self.buttonBox = QtWidgets.QDialogButtonBox(AddWLDialog)
        self.buttonBox.setGeometry(QtCore.QRect(180, 90, 91, 32))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.buttonBox.setFont(font)
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtWidgets.QDialogButtonBox.Cancel|QtWidgets.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName("buttonBox")
        self.spinBox = QtWidgets.QSpinBox(AddWLDialog)
        self.spinBox.setGeometry(QtCore.QRect(40, 90, 81, 22))
        self.spinBox.setMinimum(600)
        self.spinBox.setMaximum(1300)
        self.spinBox.setObjectName("spinBox")
        self.label = QtWidgets.QLabel(AddWLDialog)
        self.label.setGeometry(QtCore.QRect(100, 40, 141, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label.setFont(font)
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(AddWLDialog)
        self.label_2.setGeometry(QtCore.QRect(130, 100, 47, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.label_2.setFont(font)
        self.label_2.setObjectName("label_2")

        self.retranslateUi(AddWLDialog)
        self.buttonBox.accepted.connect(AddWLDialog.accept)
        self.buttonBox.rejected.connect(AddWLDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(AddWLDialog)

    def retranslateUi(self, AddWLDialog):
        _translate = QtCore.QCoreApplication.translate
        AddWLDialog.setWindowTitle(_translate("AddWLDialog", "Add Wavelength"))
        self.label.setText(_translate("AddWLDialog", "Valid values: 600-1300"))
        self.label_2.setText(_translate("AddWLDialog", "mm"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    AddWLDialog = QtWidgets.QDialog()
    ui = Ui_AddWLDialog()
    ui.setupUi(AddWLDialog)
    AddWLDialog.show()
    sys.exit(app.exec_())


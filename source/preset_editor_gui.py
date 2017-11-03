# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'preset_editor.ui'
#
# Created by: PyQt5 UI code generator 5.9
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets

class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(614, 653)
        font = QtGui.QFont()
        font.setBold(False)
        font.setWeight(50)
        MainWindow.setFont(font)
        MainWindow.setStyleSheet("QPlainTextEdit {\n"
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
        MainWindow.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        MainWindow.setAnimated(True)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.loadButton = QtWidgets.QPushButton(self.centralwidget)
        self.loadButton.setGeometry(QtCore.QRect(30, 20, 75, 23))
        self.loadButton.setObjectName("loadButton")
        self.saveAsButton = QtWidgets.QPushButton(self.centralwidget)
        self.saveAsButton.setGeometry(QtCore.QRect(140, 20, 75, 23))
        self.saveAsButton.setAutoDefault(False)
        self.saveAsButton.setDefault(False)
        self.saveAsButton.setFlat(False)
        self.saveAsButton.setObjectName("saveAsButton")
        self.nameLabel = QtWidgets.QLabel(self.centralwidget)
        self.nameLabel.setGeometry(QtCore.QRect(40, 80, 47, 13))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.nameLabel.setFont(font)
        self.nameLabel.setObjectName("nameLabel")
        self.detektorLabel = QtWidgets.QLabel(self.centralwidget)
        self.detektorLabel.setGeometry(QtCore.QRect(40, 180, 81, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.detektorLabel.setFont(font)
        self.detektorLabel.setObjectName("detektorLabel")
        self.nameBox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.nameBox.setGeometry(QtCore.QRect(140, 70, 161, 31))
        self.nameBox.setObjectName("nameBox")
        self.detectorBox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.detectorBox.setGeometry(QtCore.QRect(140, 170, 161, 31))
        self.detectorBox.setObjectName("detectorBox")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setGeometry(QtCore.QRect(40, 240, 511, 331))
        font = QtGui.QFont()
        font.setPointSize(9)
        font.setBold(True)
        font.setWeight(75)
        self.tabWidget.setFont(font)
        self.tabWidget.setToolTipDuration(-1)
        self.tabWidget.setStyleSheet("")
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.addButton = QtWidgets.QPushButton(self.tab)
        self.addButton.setGeometry(QtCore.QRect(200, 80, 51, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.addButton.setFont(font)
        self.addButton.setToolTipDuration(-1)
        self.addButton.setObjectName("addButton")
        self.deleteButton = QtWidgets.QPushButton(self.tab)
        self.deleteButton.setGeometry(QtCore.QRect(200, 120, 51, 23))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.deleteButton.setFont(font)
        self.deleteButton.setToolTipDuration(-1)
        self.deleteButton.setObjectName("deleteButton")
        self.unselectedList = QtWidgets.QListWidget(self.tab)
        self.unselectedList.setGeometry(QtCore.QRect(40, 50, 131, 221))
        self.unselectedList.setObjectName("unselectedList")
        self.selectedList = QtWidgets.QListWidget(self.tab)
        self.selectedList.setGeometry(QtCore.QRect(300, 50, 141, 221))
        self.selectedList.setObjectName("selectedList")
        self.selectedLabel = QtWidgets.QLabel(self.tab)
        self.selectedLabel.setGeometry(QtCore.QRect(350, 20, 51, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.selectedLabel.setFont(font)
        self.selectedLabel.setObjectName("selectedLabel")
        self.unselectedLabel = QtWidgets.QLabel(self.tab)
        self.unselectedLabel.setGeometry(QtCore.QRect(70, 20, 71, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.unselectedLabel.setFont(font)
        self.unselectedLabel.setObjectName("unselectedLabel")
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.groupBox_2 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_2.setGeometry(QtCore.QRect(290, 40, 191, 171))
        self.groupBox_2.setTitle("")
        self.groupBox_2.setObjectName("groupBox_2")
        self.visibleCheck = QtWidgets.QCheckBox(self.groupBox_2)
        self.visibleCheck.setGeometry(QtCore.QRect(30, 20, 70, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.visibleCheck.setFont(font)
        self.visibleCheck.setObjectName("visibleCheck")
        self.transparentCheck = QtWidgets.QCheckBox(self.groupBox_2)
        self.transparentCheck.setGeometry(QtCore.QRect(30, 50, 91, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.transparentCheck.setFont(font)
        self.transparentCheck.setObjectName("transparentCheck")
        self.tresholdLabel = QtWidgets.QLabel(self.groupBox_2)
        self.tresholdLabel.setGeometry(QtCore.QRect(50, 80, 81, 16))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.tresholdLabel.setFont(font)
        self.tresholdLabel.setObjectName("tresholdLabel")
        self.minBox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.minBox.setGeometry(QtCore.QRect(110, 110, 61, 22))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.minBox.setFont(font)
        self.minBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.minBox.setDecimals(3)
        self.minBox.setMinimum(-5000000.0)
        self.minBox.setMaximum(50000000.0)
        self.minBox.setObjectName("minBox")
        self.maxBox = QtWidgets.QDoubleSpinBox(self.groupBox_2)
        self.maxBox.setGeometry(QtCore.QRect(110, 140, 61, 22))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.maxBox.setFont(font)
        self.maxBox.setLocale(QtCore.QLocale(QtCore.QLocale.English, QtCore.QLocale.UnitedStates))
        self.maxBox.setPrefix("")
        self.maxBox.setDecimals(3)
        self.maxBox.setMinimum(-5000000.0)
        self.maxBox.setMaximum(500000.99)
        self.maxBox.setObjectName("maxBox")
        self.minLabel = QtWidgets.QLabel(self.groupBox_2)
        self.minLabel.setGeometry(QtCore.QRect(50, 110, 47, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.minLabel.setFont(font)
        self.minLabel.setObjectName("minLabel")
        self.maxLabel = QtWidgets.QLabel(self.groupBox_2)
        self.maxLabel.setGeometry(QtCore.QRect(50, 140, 47, 13))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.maxLabel.setFont(font)
        self.maxLabel.setObjectName("maxLabel")
        self.viewSpectraList = QtWidgets.QListWidget(self.tab_2)
        self.viewSpectraList.setGeometry(QtCore.QRect(140, 40, 131, 211))
        self.viewSpectraList.setObjectName("viewSpectraList")
        self.groupBox_3 = QtWidgets.QGroupBox(self.tab_2)
        self.groupBox_3.setGeometry(QtCore.QRect(20, 40, 101, 111))
        self.groupBox_3.setTitle("")
        self.groupBox_3.setObjectName("groupBox_3")
        self.view1Button = QtWidgets.QRadioButton(self.groupBox_3)
        self.view1Button.setGeometry(QtCore.QRect(20, 10, 61, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.view1Button.setFont(font)
        self.view1Button.setChecked(True)
        self.view1Button.setObjectName("view1Button")
        self.buttonGroup = QtWidgets.QButtonGroup(MainWindow)
        self.buttonGroup.setObjectName("buttonGroup")
        self.buttonGroup.addButton(self.view1Button)
        self.view2Button = QtWidgets.QRadioButton(self.groupBox_3)
        self.view2Button.setGeometry(QtCore.QRect(20, 30, 61, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.view2Button.setFont(font)
        self.view2Button.setObjectName("view2Button")
        self.buttonGroup.addButton(self.view2Button)
        self.view3Button = QtWidgets.QRadioButton(self.groupBox_3)
        self.view3Button.setGeometry(QtCore.QRect(20, 50, 61, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.view3Button.setFont(font)
        self.view3Button.setObjectName("view3Button")
        self.buttonGroup.addButton(self.view3Button)
        self.view4Button = QtWidgets.QRadioButton(self.groupBox_3)
        self.view4Button.setGeometry(QtCore.QRect(20, 70, 61, 17))
        font = QtGui.QFont()
        font.setBold(True)
        font.setWeight(75)
        self.view4Button.setFont(font)
        self.view4Button.setObjectName("view4Button")
        self.buttonGroup.addButton(self.view4Button)
        self.tabWidget.addTab(self.tab_2, "")
        self.browseFactorySpectra = QtWidgets.QPushButton(self.centralwidget)
        self.browseFactorySpectra.setGeometry(QtCore.QRect(250, 20, 91, 23))
        self.browseFactorySpectra.setAutoDefault(False)
        self.browseFactorySpectra.setDefault(False)
        self.browseFactorySpectra.setFlat(False)
        self.browseFactorySpectra.setObjectName("browseFactorySpectra")
        self.FactorySpectraTextBox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.FactorySpectraTextBox.setGeometry(QtCore.QRect(370, 10, 201, 41))
        self.FactorySpectraTextBox.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.FactorySpectraTextBox.setReadOnly(True)
        self.FactorySpectraTextBox.setObjectName("FactorySpectraTextBox")
        self.PresetIDLabel = QtWidgets.QLabel(self.centralwidget)
        self.PresetIDLabel.setGeometry(QtCore.QRect(350, 70, 71, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.PresetIDLabel.setFont(font)
        self.PresetIDLabel.setObjectName("PresetIDLabel")
        self.PresetIDTextBox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.PresetIDTextBox.setGeometry(QtCore.QRect(430, 60, 141, 41))
        self.PresetIDTextBox.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.PresetIDTextBox.setReadOnly(True)
        self.PresetIDTextBox.setObjectName("PresetIDTextBox")
        self.versionLabel = QtWidgets.QLabel(self.centralwidget)
        self.versionLabel.setGeometry(QtCore.QRect(40, 130, 61, 16))
        font = QtGui.QFont()
        font.setPointSize(10)
        font.setBold(True)
        font.setWeight(75)
        self.versionLabel.setFont(font)
        self.versionLabel.setObjectName("versionLabel")
        self.versionTextBox = QtWidgets.QPlainTextEdit(self.centralwidget)
        self.versionTextBox.setGeometry(QtCore.QRect(140, 120, 81, 31))
        self.versionTextBox.setLineWrapMode(QtWidgets.QPlainTextEdit.NoWrap)
        self.versionTextBox.setReadOnly(False)
        self.versionTextBox.setObjectName("versionTextBox")
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 614, 21))
        self.menubar.setObjectName("menubar")
        MainWindow.setMenuBar(self.menubar)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "Preset Editor"))
        self.loadButton.setText(_translate("MainWindow", "Load"))
        self.saveAsButton.setText(_translate("MainWindow", "Save As"))
        self.nameLabel.setText(_translate("MainWindow", "Name"))
        self.detektorLabel.setText(_translate("MainWindow", "Detector"))
        self.addButton.setToolTip(_translate("MainWindow", "Add Item"))
        self.addButton.setText(_translate("MainWindow", "--->"))
        self.deleteButton.setToolTip(_translate("MainWindow", "Remove Item"))
        self.deleteButton.setText(_translate("MainWindow", "<---"))
        self.unselectedList.setSortingEnabled(True)
        self.selectedList.setSortingEnabled(True)
        self.selectedLabel.setText(_translate("MainWindow", "Selected"))
        self.unselectedLabel.setText(_translate("MainWindow", "Unselected"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "Processing"))
        self.visibleCheck.setText(_translate("MainWindow", "Visible"))
        self.transparentCheck.setText(_translate("MainWindow", "Transparent"))
        self.tresholdLabel.setText(_translate("MainWindow", "Threshold"))
        self.minLabel.setText(_translate("MainWindow", "min : "))
        self.maxLabel.setText(_translate("MainWindow", "max"))
        self.viewSpectraList.setSortingEnabled(True)
        self.view1Button.setText(_translate("MainWindow", "View 1"))
        self.view2Button.setText(_translate("MainWindow", "View 2"))
        self.view3Button.setText(_translate("MainWindow", "View 3"))
        self.view4Button.setText(_translate("MainWindow", "View 4"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("MainWindow", "Visualization"))
        self.browseFactorySpectra.setToolTip(_translate("MainWindow", "<html><head/><body><p>Browse Factory Spectra</p></body></html>"))
        self.browseFactorySpectra.setText(_translate("MainWindow", "Factory Spectra"))
        self.PresetIDLabel.setToolTip(_translate("MainWindow", "<html><head/><body><p>Preset Identifier</p></body></html>"))
        self.PresetIDLabel.setText(_translate("MainWindow", "Preset ID"))
        self.versionLabel.setText(_translate("MainWindow", "Version"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())


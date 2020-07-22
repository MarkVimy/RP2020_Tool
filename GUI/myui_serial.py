# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'myui_serial.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(750, 694)
        MainWindow.setToolTip("")
        MainWindow.setStatusTip("")
        MainWindow.setWhatsThis("")
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(self.centralwidget)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.textBrowser = QtWidgets.QTextBrowser(self.tab)
        self.textBrowser.setObjectName("textBrowser")
        self.gridLayout_2.addWidget(self.textBrowser, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.gridLayout.addWidget(self.tabWidget, 0, 0, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.menubar = QtWidgets.QMenuBar(MainWindow)
        self.menubar.setGeometry(QtCore.QRect(0, 0, 750, 26))
        self.menubar.setObjectName("menubar")
        self.menu = QtWidgets.QMenu(self.menubar)
        self.menu.setObjectName("menu")
        MainWindow.setMenuBar(self.menubar)
        self.statusBar = QtWidgets.QStatusBar(MainWindow)
        self.statusBar.setObjectName("statusBar")
        MainWindow.setStatusBar(self.statusBar)
        self.toolBar = QtWidgets.QToolBar(MainWindow)
        self.toolBar.setObjectName("toolBar")
        MainWindow.addToolBar(QtCore.Qt.LeftToolBarArea, self.toolBar)
        self.actionSerialDebugger = QtWidgets.QAction(MainWindow)
        self.actionSerialDebugger.setObjectName("actionSerialDebugger")
        self.actionWaveformViewer = QtWidgets.QAction(MainWindow)
        self.actionWaveformViewer.setObjectName("actionWaveformViewer")
        self.actionSerialDebugger_2 = QtWidgets.QAction(MainWindow)
        self.actionSerialDebugger_2.setObjectName("actionSerialDebugger_2")
        self.actionWaveformViewer_2 = QtWidgets.QAction(MainWindow)
        self.actionWaveformViewer_2.setObjectName("actionWaveformViewer_2")
        self.actionUserManual = QtWidgets.QAction(MainWindow)
        self.actionUserManual.setObjectName("actionUserManual")
        self.menu.addAction(self.actionSerialDebugger_2)
        self.menu.addAction(self.actionWaveformViewer_2)
        self.menubar.addAction(self.menu.menuAction())
        self.toolBar.addAction(self.actionSerialDebugger)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionWaveformViewer)
        self.toolBar.addSeparator()
        self.toolBar.addAction(self.actionUserManual)

        self.retranslateUi(MainWindow)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "MainWindow"))
        self.textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-weight:600;\">RP2020上位机</span></p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><span style=\" font-style:italic;\">-* V1.0 *-</span></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">使用说明：</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- 主界面：</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1.左侧为工具栏。单击可跳转至对应工具所在的页，双击可以弹出独立窗口（也可以在菜单栏中选择弹出某一工具的独立窗口）</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">- 示波器：</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">1.根据数据帧显示数值部分</p>\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">关于我们：</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">深圳大学RobotPiolts战队</p></body></html>"))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("MainWindow", "使用说明"))
        self.menu.setTitle(_translate("MainWindow", "独立窗口(&F)"))
        self.toolBar.setWindowTitle(_translate("MainWindow", "toolBar"))
        self.actionSerialDebugger.setText(_translate("MainWindow", "串口调试助手"))
        self.actionSerialDebugger.setToolTip(_translate("MainWindow", "单击切换页\n"
"双击弹出独立窗口"))
        self.actionWaveformViewer.setText(_translate("MainWindow", "示波器"))
        self.actionWaveformViewer.setToolTip(_translate("MainWindow", "单击切换页\n"
"双击弹出独立窗口"))
        self.actionSerialDebugger_2.setText(_translate("MainWindow", "串口调试助手(&S)"))
        self.actionSerialDebugger_2.setToolTip(_translate("MainWindow", "打开串口调试助手独立窗口"))
        self.actionWaveformViewer_2.setText(_translate("MainWindow", "示波器(&W)"))
        self.actionWaveformViewer_2.setToolTip(_translate("MainWindow", "打开示波器独立窗口"))
        self.actionUserManual.setText(_translate("MainWindow", "使用说明"))
        self.actionUserManual.setToolTip(_translate("MainWindow", "关于上位机的使用说明"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    MainWindow = QtWidgets.QMainWindow()
    ui = Ui_MainWindow()
    ui.setupUi(MainWindow)
    MainWindow.show()
    sys.exit(app.exec_())

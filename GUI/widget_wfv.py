# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'widget_wfv.ui'
#
# Created by: PyQt5 UI code generator 5.13.2
#
# WARNING! All changes made in this file will be lost!


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_WaveformViewer(object):
    def setupUi(self, WaveformViewer):
        WaveformViewer.setObjectName("WaveformViewer")
        WaveformViewer.resize(865, 584)
        self.gridLayout = QtWidgets.QGridLayout(WaveformViewer)
        self.gridLayout.setObjectName("gridLayout")
        self.tabWidget = QtWidgets.QTabWidget(WaveformViewer)
        self.tabWidget.setObjectName("tabWidget")
        self.tab = QtWidgets.QWidget()
        self.tab.setObjectName("tab")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.tab)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.tableWidget = QtWidgets.QTableWidget(self.tab)
        self.tableWidget.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget.setStyleSheet("QHeaderView::section:vertical{width:30px}")
        self.tableWidget.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget.setObjectName("tableWidget")
        self.tableWidget.setColumnCount(8)
        self.tableWidget.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget.setItem(0, 0, item)
        self.tableWidget.horizontalHeader().setVisible(False)
        self.tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_2.addWidget(self.tableWidget, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab, "")
        self.tab_2 = QtWidgets.QWidget()
        self.tab_2.setObjectName("tab_2")
        self.gridLayout_3 = QtWidgets.QGridLayout(self.tab_2)
        self.gridLayout_3.setObjectName("gridLayout_3")
        self.tableWidget_2 = QtWidgets.QTableWidget(self.tab_2)
        self.tableWidget_2.setLayoutDirection(QtCore.Qt.LeftToRight)
        self.tableWidget_2.setStyleSheet("QHeaderView::section:vertical{width:30px}")
        self.tableWidget_2.setGridStyle(QtCore.Qt.SolidLine)
        self.tableWidget_2.setObjectName("tableWidget_2")
        self.tableWidget_2.setColumnCount(8)
        self.tableWidget_2.setRowCount(6)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_2.setVerticalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_2.setVerticalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_2.setVerticalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_2.setVerticalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_2.setVerticalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        item.setTextAlignment(QtCore.Qt.AlignCenter)
        self.tableWidget_2.setVerticalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(0, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(1, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(2, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(3, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(4, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(5, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(6, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setHorizontalHeaderItem(7, item)
        item = QtWidgets.QTableWidgetItem()
        self.tableWidget_2.setItem(0, 0, item)
        self.tableWidget_2.horizontalHeader().setVisible(False)
        self.tableWidget_2.horizontalHeader().setCascadingSectionResizes(False)
        self.tableWidget_2.horizontalHeader().setSortIndicatorShown(False)
        self.tableWidget_2.horizontalHeader().setStretchLastSection(True)
        self.gridLayout_3.addWidget(self.tableWidget_2, 0, 0, 1, 1)
        self.tabWidget.addTab(self.tab_2, "")
        self.gridLayout.addWidget(self.tabWidget, 2, 0, 1, 1)
        self.graphicsView = QtWidgets.QGraphicsView(WaveformViewer)
        self.graphicsView.setObjectName("graphicsView")
        self.gridLayout.addWidget(self.graphicsView, 0, 0, 1, 1)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.pushButton_resume = QtWidgets.QPushButton(WaveformViewer)
        self.pushButton_resume.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_resume.setObjectName("pushButton_resume")
        self.horizontalLayout.addWidget(self.pushButton_resume)
        self.pushButton_restart = QtWidgets.QPushButton(WaveformViewer)
        self.pushButton_restart.setIconSize(QtCore.QSize(24, 24))
        self.pushButton_restart.setObjectName("pushButton_restart")
        self.horizontalLayout.addWidget(self.pushButton_restart)
        self.checkBox_legend = QtWidgets.QCheckBox(WaveformViewer)
        self.checkBox_legend.setChecked(True)
        self.checkBox_legend.setObjectName("checkBox_legend")
        self.horizontalLayout.addWidget(self.checkBox_legend)
        self.checkBox_viewall = QtWidgets.QCheckBox(WaveformViewer)
        self.checkBox_viewall.setObjectName("checkBox_viewall")
        self.horizontalLayout.addWidget(self.checkBox_viewall)
        self.label_xscale = QtWidgets.QLabel(WaveformViewer)
        self.label_xscale.setObjectName("label_xscale")
        self.horizontalLayout.addWidget(self.label_xscale)
        self.spinBox_xscale = QtWidgets.QSpinBox(WaveformViewer)
        self.spinBox_xscale.setMinimum(1)
        self.spinBox_xscale.setMaximum(100)
        self.spinBox_xscale.setProperty("value", 100)
        self.spinBox_xscale.setObjectName("spinBox_xscale")
        self.horizontalLayout.addWidget(self.spinBox_xscale)
        self.pushButton_export = QtWidgets.QPushButton(WaveformViewer)
        self.pushButton_export.setObjectName("pushButton_export")
        self.horizontalLayout.addWidget(self.pushButton_export)
        self.gridLayout.addLayout(self.horizontalLayout, 1, 0, 1, 1)
        self.gridLayout.setRowStretch(0, 4)

        self.retranslateUi(WaveformViewer)
        self.tabWidget.setCurrentIndex(1)
        QtCore.QMetaObject.connectSlotsByName(WaveformViewer)

    def retranslateUi(self, WaveformViewer):
        _translate = QtCore.QCoreApplication.translate
        WaveformViewer.setWindowTitle(_translate("WaveformViewer", "Form"))
        self.tableWidget.setSortingEnabled(False)
        item = self.tableWidget.verticalHeaderItem(0)
        item.setText(_translate("WaveformViewer", "1"))
        item = self.tableWidget.verticalHeaderItem(1)
        item.setText(_translate("WaveformViewer", "2"))
        item = self.tableWidget.verticalHeaderItem(2)
        item.setText(_translate("WaveformViewer", "3"))
        item = self.tableWidget.verticalHeaderItem(3)
        item.setText(_translate("WaveformViewer", "4"))
        item = self.tableWidget.verticalHeaderItem(4)
        item.setText(_translate("WaveformViewer", "5"))
        item = self.tableWidget.verticalHeaderItem(5)
        item.setText(_translate("WaveformViewer", "6"))
        item = self.tableWidget.horizontalHeaderItem(0)
        item.setText(_translate("WaveformViewer", "名称"))
        item = self.tableWidget.horizontalHeaderItem(1)
        item.setText(_translate("WaveformViewer", "颜色"))
        item = self.tableWidget.horizontalHeaderItem(2)
        item.setText(_translate("WaveformViewer", "当前数值"))
        item = self.tableWidget.horizontalHeaderItem(3)
        item.setText(_translate("WaveformViewer", "最小值"))
        item = self.tableWidget.horizontalHeaderItem(4)
        item.setText(_translate("WaveformViewer", "最大值"))
        item = self.tableWidget.horizontalHeaderItem(5)
        item.setText(_translate("WaveformViewer", "滑动平均值"))
        item = self.tableWidget.horizontalHeaderItem(6)
        item.setText(_translate("WaveformViewer", "y轴偏移"))
        item = self.tableWidget.horizontalHeaderItem(7)
        item.setText(_translate("WaveformViewer", "y轴缩放"))
        __sortingEnabled = self.tableWidget.isSortingEnabled()
        self.tableWidget.setSortingEnabled(False)
        self.tableWidget.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab), _translate("WaveformViewer", "Frame 1"))
        self.tableWidget_2.setSortingEnabled(False)
        item = self.tableWidget_2.verticalHeaderItem(0)
        item.setText(_translate("WaveformViewer", "1"))
        item = self.tableWidget_2.verticalHeaderItem(1)
        item.setText(_translate("WaveformViewer", "2"))
        item = self.tableWidget_2.verticalHeaderItem(2)
        item.setText(_translate("WaveformViewer", "3"))
        item = self.tableWidget_2.verticalHeaderItem(3)
        item.setText(_translate("WaveformViewer", "4"))
        item = self.tableWidget_2.verticalHeaderItem(4)
        item.setText(_translate("WaveformViewer", "5"))
        item = self.tableWidget_2.verticalHeaderItem(5)
        item.setText(_translate("WaveformViewer", "6"))
        item = self.tableWidget_2.horizontalHeaderItem(0)
        item.setText(_translate("WaveformViewer", "名称"))
        item = self.tableWidget_2.horizontalHeaderItem(1)
        item.setText(_translate("WaveformViewer", "颜色"))
        item = self.tableWidget_2.horizontalHeaderItem(2)
        item.setText(_translate("WaveformViewer", "当前数值"))
        item = self.tableWidget_2.horizontalHeaderItem(3)
        item.setText(_translate("WaveformViewer", "最小值"))
        item = self.tableWidget_2.horizontalHeaderItem(4)
        item.setText(_translate("WaveformViewer", "最大值"))
        item = self.tableWidget_2.horizontalHeaderItem(5)
        item.setText(_translate("WaveformViewer", "滑动平均值"))
        item = self.tableWidget_2.horizontalHeaderItem(6)
        item.setText(_translate("WaveformViewer", "y轴偏移"))
        item = self.tableWidget_2.horizontalHeaderItem(7)
        item.setText(_translate("WaveformViewer", "y轴缩放"))
        __sortingEnabled = self.tableWidget_2.isSortingEnabled()
        self.tableWidget_2.setSortingEnabled(False)
        self.tableWidget_2.setSortingEnabled(__sortingEnabled)
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_2), _translate("WaveformViewer", "Frame 2"))
        self.pushButton_resume.setText(_translate("WaveformViewer", "暂停"))
        self.pushButton_restart.setText(_translate("WaveformViewer", "启动"))
        self.checkBox_legend.setText(_translate("WaveformViewer", "显示图例"))
        self.checkBox_viewall.setText(_translate("WaveformViewer", "全局显示"))
        self.label_xscale.setText(_translate("WaveformViewer", "x轴缩放(％)"))
        self.pushButton_export.setText(_translate("WaveformViewer", "导出.."))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    WaveformViewer = QtWidgets.QWidget()
    ui = Ui_WaveformViewer()
    ui.setupUi(WaveformViewer)
    WaveformViewer.show()
    sys.exit(app.exec_())

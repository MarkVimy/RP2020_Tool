import sys
import time
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow,\
                            QLabel
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import pyqtSignal
from APP.myserial import SerialDebugger
from APP.mywfv import WaveformViewer
from APP.myexlist import ExList
from GUI.myui_serial import Ui_MainWindow


class MyConsole(QMainWindow, Ui_MainWindow):
    frame_signal = pyqtSignal(tuple)
    freeze_sd_signal = pyqtSignal(bool)
    export_signal = pyqtSignal()

    def __init__(self):
        super(MyConsole, self).__init__()
        self.ser_ui = QWidget()
        self.ser = SerialDebugger(self.ser_ui)
        self.wfv_ui = QWidget()
        self.wfv = WaveformViewer(self.wfv_ui)  # WaveformViewer
        self.exlist = ExList(*self.wfv.get_frames(), *self.wfv.get_timers())
        self.serbtn_last_clicked = 0
        self.wfvbtn_last_clicked = 0
        self.init_ui()
        self.init_serial_debugger()
        self.init_waveform_viewer()
        self.init_action()
        self.init_signal()

    def init_ui(self):
        """
        主窗口界面初始化
        :return:
        """
        self.setupUi(self)
        self.setWindowTitle('RP2020 上位机')
        self.setWindowIcon(QIcon('../GUI/RpLogo.jpg'))
        self.labelRp = QLabel('@Robopilots2020')
        self.labelTxCnt = QLabel('发送：0')
        self.labelRxCnt = QLabel('接收：0')
        self.labelRxRate = QLabel('速率：0')
        self.statusBar.addPermanentWidget(self.labelRp, stretch=3)
        self.statusBar.addPermanentWidget(self.labelTxCnt, stretch=1)
        self.statusBar.addPermanentWidget(self.labelRxCnt, stretch=1)
        self.statusBar.addPermanentWidget(self.labelRxRate, stretch=1)

    def init_serial_debugger(self):
        # 添加串口调试助手
        self.tabWidget.insertTab(0, self.ser_ui, '串口调试助手')
        self.tabWidget.setCurrentIndex(0)
        # 重定义关闭事件
        self.ser_ui.closeEvent = self.ser_closeEvent
        # 重定义信号发射函数
        self.ser.port_frame_emit = self.frame_emit
        self.ser.port_show_rx_rate = self.set_statusbar_rx_rate
        # 添加窗口通信
        self.ser.timer_rx.timeout.connect(self.set_statusbar_rx)
        self.ser.timer_tx.timeout.connect(self.set_statusbar_tx)
        self.ser.pushButton_send.clicked.connect(self.set_statusbar_tx)

    def init_waveform_viewer(self):
        # 添加示波器
        self.tabWidget.insertTab(1, self.wfv_ui, '示波器')
        # 重定义关闭事件
        self.wfv_ui.closeEvent = self.wfv_closeEvent
        # 重定义信号发射函数
        self.wfv.freeze_sd_emit = self.freeze_sd_emit
        self.wfv.export_emit = self.export_emit

    def init_action(self):
        # 串口调试助手
        self.actionSerialDebugger_2.triggered.connect(self.ser_ui_show)
        self.actionSerialDebugger.triggered.connect(self.ser_ui_show)
        # 示波器
        self.actionWaveformViewer_2.triggered.connect(self.wfv_ui_show)
        self.actionWaveformViewer.triggered.connect(self.wfv_ui_show)

    def init_signal(self):
        self.frame_signal.connect(self.wfv.add_frame)
        self.freeze_sd_signal.connect(self.ser.freeze)
        self.export_signal.connect(self.exlist.show)

    def frame_emit(self, frame):
        self.frame_signal.emit(frame)

    def freeze_sd_emit(self, cmd):
        # print(cmd)
        self.freeze_sd_signal.emit(cmd)

    def export_emit(self):
        self.export_signal.emit()

    def set_statusbar_rx(self):
        self.labelRxCnt.setText('接收：{}'.format(self.ser.rx_cnt))

    def set_statusbar_tx(self):
        self.labelTxCnt.setText('发送：{}'.format(self.ser.tx_cnt))

    def set_statusbar_rx_rate(self):
        self.labelRxRate.setText('速率：{:.3f} K/s'.format(self.ser.rx_rate))

    def ser_pop_win(self):
        # 将控件提升为顶层窗口
        self.ser_ui.setParent(None)
        self.ser_ui.setWindowTitle('RP2020 串口调试助手')
        self.ser_ui.setWindowIcon(QIcon('../GUI/RpLogo.jpg'))
        self.ser_ui.show()

    def ser_ui_show(self):
        if self.sender() == self.actionSerialDebugger_2:
            self.ser_pop_win()
        elif self.sender() == self.actionSerialDebugger:
            # TabWidget切换页
            self.tabWidget.setCurrentIndex(0)
            # 双击Toolbar按钮则弹窗
            now_clicked = time.time()
            if now_clicked - self.serbtn_last_clicked <= 0.5:
                self.ser_pop_win()
            else:
                self.serbtn_last_clicked = now_clicked

    def wfv_pop_win(self):
        # 将控件提升为顶层窗口
        self.wfv_ui.setParent(None)
        self.wfv_ui.setWindowTitle('RP2020 示波器')
        self.wfv_ui.setWindowIcon(QIcon('../GUI/RpLogo.jpg'))
        self.wfv_ui.show()

    def wfv_ui_show(self):
        if self.sender() == self.actionWaveformViewer_2:
            self.wfv_pop_win()
        elif self.sender() == self.actionWaveformViewer:
            # TabWidget切换页
            self.tabWidget.setCurrentIndex(1)
            # 双击Toolbar按钮则弹窗
            now_clicked = time.time()
            if now_clicked - self.wfvbtn_last_clicked <= 0.5:
                self.wfv_pop_win()
            else:
                self.wfvbtn_last_clicked = now_clicked

    def ser_closeEvent(self, event):
        """ 重定义串口调试助手独立窗口的退出事件(退出之前先关闭串口)
        """
        # 阻止调用close()方法；否则窗体内容将丢失，无法恢复
        event.ignore()
        # 将窗体内容转移至TabWidget中
        self.tabWidget.insertTab(0, self.ser_ui, '串口调试助手')
        self.tabWidget.setCurrentIndex(0)

    def wfv_closeEvent(self, event):
        """ 重定义示波器独立窗口的退出事件(退出之前先关闭串口)
        """
        # 阻止调用close()方法；否则窗体内容将丢失，无法恢复
        event.ignore()
        # 将窗体内容转移至TabWidget中
        self.tabWidget.insertTab(1, self.wfv_ui, '示波器')
        self.tabWidget.setCurrentIndex(1)

    def closeEvent(self, event):
        """ 主窗口关闭后会关闭所有独立弹窗，以便退出程序
        """
        self.ser_ui.close()
        self.wfv_ui.close()


if __name__ == '__main__':
    app = QApplication([])
    console = MyConsole()
    console.show()
    sys.exit(app.exec_())
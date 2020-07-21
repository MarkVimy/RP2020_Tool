# https://blog.csdn.net/u011625775/article/details/99681560

import serial
import serial.tools.list_ports
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow,\
                            QMessageBox, QComboBox, QLabel,\
                            QGridLayout
from PyQt5.QtCore import QTimer
from PyQt5.QtGui import QIcon
from GUI.widget_serial import Ui_SerialDebugger
import struct
from time import time


F1_BYTE = 0x01
F2_BYTE = 0x02
Fn_BYTES = (F1_BYTE, F2_BYTE)


class SerialDebugger(QWidget, Ui_SerialDebugger):
    def __init__(self, widget):
        super(SerialDebugger, self).__init__()
        self.frame_cnt = 0
        self.tx_cnt = 0
        self.rx_cnt = 0
        self.last_rx_cnt = 0
        self.rx_rate = 0
        self.port_index = -1    # port_list->None(一开始是-1)
        self.port_cnt = 0
        self.port_frame_surplus = None
        self.isFrozen = False
        self.ser = serial.Serial(baudrate=115200, timeout=0)
        self.init_ui(widget)
        self.init_action()
        self.init_port()

    def init_ui(self, widget):
        self.setupUi(widget)

    def init_port(self):
        self.port_check()
        # 定时接收(1ms)
        self.timer_rx = QTimer()
        self.timer_rx.timeout.connect(self.port_receive)
        self.timer_rx.start(1)
        self.timer_rx_tick = 0
        # 创建定时发送器
        self.timer_tx = QTimer()
        self.timer_tx.timeout.connect(self.port_send)
        self.timer_tx.stop()

    def init_action(self):
        # 下拉框动作
        self.comboBox_port.showPopup = self.port_showPopup
        self.comboBox_port.currentIndexChanged.connect(self.port_change)
        self.comboBox_baudrate.currentTextChanged.connect(self.port_set_baudrate)
        self.comboBox_bytesize.currentTextChanged.connect(self.port_set_bytesize)
        self.comboBox_stopbits.currentTextChanged.connect(self.port_set_stopbits)
        self.comboBox_parity.currentTextChanged.connect(self.port_set_parity)
        # 复选框动作
        self.checkBox_timer_en.toggled.connect(self.port_set_timer)
        self.checkBox_hex_send.toggled.connect(self.port_hex_send)
        self.checkBox_hex_show.toggled.connect(self.port_hex_show)
        # 文本输入框
        self.lineEdit_timer.textEdited.connect(self.port_edit_timer_hz)
        # 按钮动作
        self.pushButton_port_onoff.clicked.connect(self.port_onoff)
        self.pushButton_tx_clear.clicked.connect(self.port_tx_clear)
        self.pushButton_rx_clear.clicked.connect(self.port_rx_clear)
        self.pushButton_send.clicked.connect(self.port_send)

    def port_open_hint(self):
        self.label_port_state.setText("'{}' 已打开".format(self.ser.port))
        self.label_port_state.setStyleSheet("color:rgb(146,218,37)")
        self.pushButton_port_onoff.setText("关闭串口")

    def port_close_hint(self):
        self.label_port_state.setText("'{}' 已关闭".format(self.ser.port))
        self.label_port_state.setStyleSheet("color:rgb(255,128,64)")
        self.pushButton_port_onoff.setText("打开串口")

    def port_error_hint(self):
        self.label_port_state.setText("'{}' 异常".format(self.ser.port))
        self.label_port_state.setStyleSheet("color:rgb(128,0,128)")
        self.pushButton_port_onoff.setText("打开串口")

    def port_refresh(self):
        """
        重定义ComboBox实例的showPopup方法，刷新串口列表
        :return:None
        """
        # 先取消信号与槽的连接，防止removeItem的时候触发函数
        self.comboBox_port.currentIndexChanged.disconnect()
        # 清除选项
        for i in range(self.port_cnt):
            # print('-', self.comboBox_port.itemText(0))
            self.comboBox_port.removeItem(0)
        # 重构字典
        self.port_dict = {}
        port_list = list(serial.tools.list_ports.comports())
        self.port_cnt = len(port_list)
        for i, port in enumerate(port_list):
            # print(i, port, self.ser.name)
            # name: device
            self.port_dict[port[0]] = port[1]
            self.comboBox_port.addItem(port[0])
            if self.ser.name == port[0]:
                self.port_index = i
        self.comboBox_port.setCurrentIndex(self.port_index)
        # 恢复信号与槽的连接
        self.comboBox_port.currentIndexChanged.connect(self.port_change)

    def port_showPopup(self):
        """
        重定义串口下拉框弹出函数(加入刷新可用串口列表的操作)
        :note: 点击下拉框之后，会以下一个选项索引开始轮询一遍，存在''索引为-1
        :return: None
        """
        self.port_refresh()
        QComboBox.showPopup(self.comboBox_port)

    def port_check(self):
        """检测串口并将信息存储在字典中
        """
        self.port_refresh()
        if self.port_cnt == 0:
            self.label_port_state.setText("无串口")
            return

        self.port_set()
        for i in range(self.port_cnt):
            self.comboBox_port.setCurrentIndex(i)
            self.port_change(i, hint=False)
            # 如果打开成功则不再轮询
            if self.ser.isOpen():
                break
        else:
            self.port_error_hint()
            QMessageBox.critical(self, "串口错误", "{}无法打开！".format(self.comboBox_port.currentText()))

    def port_set(self):
        """根据下拉框配置串口属性
        """
        self.port_set_baudrate(self.comboBox_baudrate.currentText())
        self.port_set_bytesize(self.comboBox_bytesize.currentText())
        self.port_set_stopbits(self.comboBox_stopbits.currentText())
        self.port_set_parity(self.comboBox_parity.currentText())

    def port_open(self, new_port=None, hint=True):
        """打开串口
        """
        try:
            if new_port:
                self.ser.setPort(new_port)
            if not self.ser.isOpen():
                # 防止重复打开引起异常
                self.ser.open()
            self.port_open_hint()
        except serial.SerialException:
            self.port_error_hint()
            if hint:
                QMessageBox.critical(self, "串口错误", "{}无法打开！".format(self.comboBox_port.currentText()))

    def port_close(self):
        """关闭串口
        """
        try:
            self.ser.close()
            self.port_close_hint()
        except serial.SerialException:
            self.port_error_hint()
            QMessageBox.critical(self, "串口错误", "{}无法关闭！".format(self.comboBox_port.currentText()))

    def port_onoff(self):
        """串口开关状态切换
        """
        if self.ser.is_open:
            self.port_close()
        else:
            self.port_open()

    def port_change(self, p_int, hint=True):
        """
        切换串口
        :param p_int:
        :param hint:
        :return: None
        """
        new_port = self.comboBox_port.itemText(p_int)
        if new_port == '' or new_port == self.ser.port:
            return None
        # print('*', new_port)

        self.port_open(new_port, hint)

    def port_set_baudrate(self, p_str):
        """
        设置串口波特率
        :param p_str:
        :return: None
        """
        baudrate = int(p_str)
        # serial.Serial.BAUDRATES 最多支持到115200，这里选择直接赋值
        # if baudrate in serial.Serial.BAUDRATES:
        self.ser.baudrate = baudrate

    def port_set_bytesize(self, p_str):
        """
        设置串口数据位数
        :param p_str: 
        :return:None 
        """
        bytesize = int(p_str)
        if bytesize in serial.Serial.BYTESIZES:
            self.ser.bytesize = bytesize

    def port_set_parity(self, p_str):
        """
        设置串口奇偶校验
        :param p_str:
        :return:None
        """
        if p_str == '无':
            parity = serial.PARITY_NONE
        elif p_str == '奇校验':
            parity = serial.PARITY_ODD
        elif p_str == '偶校验':
            parity = serial.PARITY_EVEN
        if parity in serial.Serial.PARITIES:
            self.ser.parity = parity

    def port_set_stopbits(self, p_str):
        """
        设置串口停止位数
        :param p_str:
        :return:None
        """
        stopbits = float(p_str)
        if stopbits in serial.Serial.STOPBITS:
            self.ser.stopbits = stopbits

    def port_tx_clear(self):
        self.plainTextEdit_tx.clear()

    def port_rx_clear(self):
        self.plainTextEdit_rx.clear()
        self.tx_cnt = 0
        self.rx_cnt = 0

    def port_check_timer_hz(self):
        time_ms = self.lineEdit_timer.text()
        # print(time_ms)
        try:
            time_ms = int(time_ms)
            self.timer_tx.start(time_ms)
        except ValueError:
            self.timer_tx.stop()
            QMessageBox.critical(self, '格式错误', '请输入整数!')
            self.checkBox_timer_en.setChecked(False)

    def port_edit_timer_hz(self):
        if self.timer_tx.isActive():
            self.port_check_timer_hz()

    def port_set_timer(self):
        if self.checkBox_timer_en.isChecked():
            self.port_check_timer_hz()
        else:
            self.timer_tx.stop()

    def port_hex_send(self):
        pass
        # if self.checkBox_hex_send.isChecked():
        #     try:
        #         self.plainTextEdit_tx.setPlainText(self.plainTextEdit_tx.toPlainText().encode())
        #     except:
        #
        # else:

    def port_hex_show(self):
        pass

    def port_send(self):
        if not self.ser.is_open:
            return None

        tx_fifo = self.plainTextEdit_tx.toPlainText()
        # print(tx_fifo)
        if tx_fifo == '':
            return None
        else:
            # 非空字符串
            if not self.checkBox_hex_send.isChecked():
                # 非16进制发送
                tx_fifo = tx_fifo.encode('gb2312')  # utf-8
                if self.checkBox_newline.isChecked():
                    # 发送新行
                    tx_fifo += '\r\n'.encode('gb2312')  # utf-8
            else:
                # 16进制发送
                tx_fifo = tx_fifo.strip()
                tx_list = []
                while tx_fifo != "":
                    try:
                        # 16进制
                        num = int(tx_fifo[:2], 16)
                    except ValueError:
                        QMessageBox.critical(self, '格式错误', '请输入16进制, 以空格分开!')
                        self.checkBox_timer_en.setChecked(False)
                        return None
                    tx_fifo = tx_fifo[2:].strip()
                    tx_list.append(num)
                tx_fifo = bytes(tx_list)
                if self.checkBox_newline.isChecked():
                    # 发送新行
                    tx_fifo += bytes[ord('\r'), ord('\n')]

        tx_num = self.ser.write(tx_fifo)
        self.tx_cnt += tx_num
        # self.labelTxcnt.setText('发送：{}'.format(self.tx_cnt))

    def port_receive(self):
        now_time = time()
        if now_time - self.timer_rx_tick >= 1:
            self.rx_rate = (self.rx_cnt - self.last_rx_cnt)/1024
            self.timer_rx_tick = now_time
            self.last_rx_cnt = self.rx_cnt
            self.port_show_rx_rate()

        if not self.ser.is_open:
            return None

        try:
            rx_num = self.ser.inWaiting()
        except:
            # 拔掉串口或其它异常则自动关闭
            self.port_close()
            return None

        if rx_num > 0:
            rx_fifo = self.ser.read(rx_num)
            # print('rx: ', rx_fifo)
            self.port_frame_check(rx_fifo)
            rx_num = len(rx_fifo)
            if not self.isFrozen:
                if not self.checkBox_hex_show.isChecked():
                    # 非16进制显示
                    try:
                        # 获取text光标
                        text_cursor = self.plainTextEdit_rx.textCursor()
                        # 光标移动到底部
                        text_cursor.movePosition(text_cursor.End)
                        # 设置光标到text中去
                        self.plainTextEdit_rx.setTextCursor(text_cursor)
                        self.plainTextEdit_rx.insertPlainText(rx_fifo.decode('gb2312'))    # utf-8
                    except:
                        pass  # 可能是波特率不匹配导致的
                        # print("Error")
                else:
                    # 16进制显示
                    rx_str = ''
                    for i in range(0, rx_num):
                        rx_str += "{:02x} ".format(rx_fifo[i])
                    # 获取text光标
                    text_cursor = self.plainTextEdit_rx.textCursor()
                    # 光标移动到底部
                    text_cursor.movePosition(text_cursor.End)
                    # 设置光标到text中去
                    self.plainTextEdit_rx.setTextCursor(text_cursor)
                    self.plainTextEdit_rx.insertPlainText(rx_str)

            self.rx_cnt += rx_num
            # self.labelRxcnt.setText('接收：{}'.format(self.rx_cnt))

    def get_check_sum(self, data, frame_len):
        data = data[:frame_len]
        if not isinstance(data, bytes):
            try:
                # TODO:
                data = data.encode('utf-8')
            except:
                # TODO:
                print('No Bytes')
                return
        byte_list = [c for c in data]
        check_sum = hex(sum(byte_list))[-2:]
        return int(check_sum, 16)

    def check_sum(self, data, data_len):
        try:
            # data_len+4 = frame_len
            # print(data[data_len + 4]) -- check_sum_byte
            if data[data_len + 4] == self.get_check_sum(data, data_len + 4):
                return True
            else:
                return False
        except:
            return False

    def port_frame_check(self, rx_fifo: bytes):
        """
        检查收到的字节是否满足数据帧的格式
        :param rx_fifo: bytes
        :return: None
        """
        try:
            # print('rx_fifo = ', rx_fifo)
            if self.port_frame_surplus is not None:
                rx_fifo = self.port_frame_surplus + rx_fifo
                # print('surplus + rx_fifo = {}'.format(rx_fifo))
                self.port_frame_surplus = None
            i = rx_fifo.index(b'\xaa\xaa')
            # 这里的end_index是下一帧的头字节下标
            end_index = i + 5 + rx_fifo[i+3]  # 5 = 4(帧头) + 1(帧尾累加和校验)
            if self.check_sum(rx_fifo[i:end_index], rx_fifo[i+3]):
                # print('check ok')
                # print(rx_fifo[2:3] + rx_fifo[4:-1])
                # 发送tuple(Fx_Byte, [byte1, [...,]])
                if rx_fifo[i+2] == F1_BYTE:
                    dat = struct.unpack('fffhhh', rx_fifo[i+4:i+22])
                    frame = (F1_BYTE, *dat)
                    self.port_frame_emit(frame)
                    # self.frame_cnt += 1
                    # print(self.frame_cnt)
                elif rx_fifo[i+2] == F2_BYTE:
                    dat = struct.unpack('H', rx_fifo[i+4:i+6]) + struct.unpack('f', rx_fifo[i+6:i+10]) + struct.unpack('H', rx_fifo[i+10:i+12]) + struct.unpack('f', rx_fifo[i+12:i+16])
                    frame = (F2_BYTE, *dat)
                    self.port_frame_emit(frame)
            elif len(rx_fifo[i:end_index]) < 5 + rx_fifo[i+3]:
                # print('surplus', rx_fifo[i:end_index])
                raise IndexError
            # print('end_index: {}\ncheck[end_index:]: {}'.format(end_index, rx_fifo[end_index:]))
            rx_fifo = rx_fifo[end_index:]
            self.port_frame_check(rx_fifo)
        except ValueError:
            """
            不存在 b'\xaa\xaa'会引发该错误
            print(type(rx_fifo[-1])) -- <class 'int'>
            print(type(rx_fifo[-1:])) -- <class 'bytes'>
            170 != b'\xaa'
            170 = 0xaa
            """
            if rx_fifo[-1:] == b'\xaa':
                self.port_frame_surplus = b'\xaa'
                # print('surplus = ', self.port_frame_surplus)
            # print('ValueError')
        except IndexError:
            self.port_frame_surplus = rx_fifo[i:]
            # print('surplus =', self.port_frame_surplus)
            # print('IndexError')
        except TypeError:
            # e.g. TypeError / 数据帧格式出错
            print('**Type Error**')
        # except struct.error:
        #     print('***struct.error!***')

    def port_frame_emit(self, frame):
        # pass
        self.frame_cnt += 1
        print(self.frame_cnt)
        # print('Serial Debugger:', frame)
        # print(self.frame_cnt)

    def port_show_rx_rate(self):
        print(self.rx_rate)

    def freeze(self, cmd):
        if cmd:
            self.plainTextEdit_rx.setEnabled(False)
            self.plainTextEdit_tx.setEnabled(False)
            self.isFrozen = True
        else:
            self.plainTextEdit_rx.setEnabled(True)
            self.plainTextEdit_tx.setEnabled(True)
            self.isFrozen = False


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    widget = QWidget()
    ser = SerialDebugger(widget)
    MainWindow.setCentralWidget(widget)
    MainWindow.show()

    # widget = QWidget()
    # ser = MySerialPort(widget)
    # widget.show()

    sys.exit(app.exec_())


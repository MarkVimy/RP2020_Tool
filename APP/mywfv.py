from GUI.widget_wfv import Ui_WaveformViewer
from PyQt5.QtWidgets import QWidget, QApplication, QMainWindow,\
                            QGraphicsView, QMessageBox, QGridLayout,\
                            QPushButton, QTableWidgetItem, QCheckBox,\
                            QFrame, QColorDialog
from PyQt5.QtGui import QPen, QColor
from PyQt5.QtCore import QTimer, Qt, QPointF
import pyqtgraph as pg
import numpy as np
import math
import time
from APP.myserial import Fn_BYTES
# from APP.myexlist import ExList


class Curve(object):
    def __init__(self, plot_widget, color='r', name='curve'):
        self.name = name
        self.dat = [0]
        self.dat_min = None
        self.dat_max = None
        self.dat_sum = 0
        self.dat_cnt = 1
        self.curve = plot_widget.plot(pen=pg.mkPen(color=color, width=2), name=name)
        self.y_offset = 0
        self.y_scale = 1
        """
        以下参数与QTableWidget有关
        """
        # 可以打印成 #rrggbb 的格式
        self.pen_color = self.curve.opts['pen'].color().name()
        self.color_block = QFrame()
        self.color_block.setStyleSheet('margin: 6px; background-color: {}'.format(self.pen_color))
        # checkBox
        self.name_box = QCheckBox()
        self.name_box.setText(name)
        self.name_box.setChecked(True)

    def get_avr(self):
        return self.dat_sum/self.dat_cnt

    def get_colorBlock(self):
        return self.color_block

    def get_checkBox(self):
        return self.name_box

    def set_color(self, color):
        self.pen_color = color
        self.color_block.setStyleSheet('margin: 6px; background-color: {}'.format(color))
        self.curve.setPen(pg.mkPen(color=color))

    def update(self, new_dat):
        if self.dat_min is None:
            self.dat_min = new_dat
        elif new_dat < self.dat_min:
            self.dat_min = new_dat

        if self.dat_max is None:
            self.dat_max = new_dat
        elif new_dat > self.dat_max:
            self.dat_max = new_dat

        self.dat_sum += new_dat
        self.dat_cnt += 1
        self.dat.append(new_dat)

    def clear(self):
        self.dat_min = None
        self.dat_max = None
        self.dat_sum = 0
        self.dat_cnt = 1
        self.dat.clear()
        self.dat.append(0)

    def plot(self, t, num):
        if self.name_box.isChecked():
            # if not self.y_offset:
            #     self.curve.setData(time, self.dat)
            # else:
            #     # self.curve.setData(time, [dat+self.y_offset for dat in self.dat])
            #     self.curve.setData(time, [dat/self.y_scale+self.y_offset for dat in self.dat])
            # 增加这项功能会使得界面比较卡3/
            # now_time = time.time()
            if self.y_scale:
                self.curve.setData(t, [dat*self.y_scale+self.y_offset for dat in self.dat[-num:]])
            else:
                self.curve.setData(t, [dat+self.y_offset for dat in self.dat[-num:]])
            # print(time.time() - now_time)
            # 最原始的添加数据功能
            # now_time = time.time()
            # self.curve.setData(t, self.dat)
            # print(time.time() - now_time)
        else:
            self.curve.setData([], [])

    def unplot(self):
        self.curve.setData([], [])


class Frame(object):
    def __init__(self, func_byte=Fn_BYTES[0]):
        self.func_byte = func_byte
        self.rx_flag = 0
        self.cnt = 1

    def get_curves(self):
        return []

    def get_color_blocks(self):
        color_blocks = []
        for curve in self.get_curves():
            color_blocks.append(curve.color_block)
        return color_blocks

    def update(self, frame: tuple):
        if frame is None:
            # 新增数据 - 0
            for curve in self.get_curves():
                curve.update(0)
            self.cnt += 1
        elif isinstance(frame, tuple):
            try:
                for i, curve in enumerate(self.get_curves()):
                    curve.update(frame[i])
                self.rx_flag += 1
                self.cnt += 1
            except:
                print('The amount of args received in #Frame is wrong')

    def clear(self):
        for curve in self.get_curves():
            curve.clear()
        self.rx_flag = 0
        self.cnt = 1

    def plot(self, time, num):
        for curve in self.get_curves():
            curve.plot(time, num)

    def unplot(self):
        for curve in self.get_curves():
            curve.unplot()


class Frame1(Frame):
    def __init__(self, plot_widget):
        super(Frame1, self).__init__()
        self.func_byte = Fn_BYTES[0]

        self.yaw = Curve(plot_widget, color='r', name='yaw')
        self.pitch = Curve(plot_widget, color='g', name='pitch')
        self.roll = Curve(plot_widget, color='b', name='roll')
        self.yaw_rate = Curve(plot_widget, color='#ffff00', name='yaw_rate')
        self.pitch_rate = Curve(plot_widget, color='#ff00ff', name='pitch_rate')
        self.roll_rate = Curve(plot_widget, color='#00ffff', name='roll_rate')

        self.yaw.name_box.setChecked(False)
        self.pitch.name_box.setChecked(False)
        self.roll.name_box.setChecked(False)
        self.yaw_rate.name_box.setChecked(False)
        self.pitch_rate.name_box.setChecked(False)
        self.roll_rate.name_box.setChecked(False)

        self.param_cnt = 6
        # self.param_cnt = 3

    def get_curves(self):
        return [self.yaw, self.pitch, self.roll, self.yaw_rate, self.pitch_rate, self.roll_rate]
        # return [self.yaw, self.pitch, self.roll]


class Frame2(Frame):
    def __init__(self, plot_widget):
        super(Frame2, self).__init__()
        self.func_byte = Fn_BYTES[1]
        self.shoot_pwm = Curve(plot_widget, color='ff8040', name='shoot_pwm')
        # self.shoot_pwm.name_box.setChecked(False)
        self.shoot_speed = Curve(plot_widget, color='#8080ff', name='shoot_speed')
        # self.shoot_speed.name_box.setChecked(False)
        self.shoot_heat = Curve(plot_widget, color='ff8080', name='shoot_heat')
        self.shoot_heat.name_box.setChecked(False)
        self.power = Curve(plot_widget, color='80ff80', name='power')
        self.power.name_box.setChecked(False)
        self.param_cnt = 4

    def get_curves(self):
        return [self.shoot_pwm, self.shoot_speed, self.shoot_heat, self.power]


class WaveformTimer(QTimer):
    # 示波器显示间隔
    UPDATE_PERIOD = 100  # 20~30ms较为合适

    def __init__(self, ot_evt):
        super(WaveformTimer, self).__init__()
        self.time = [0]
        self.now_time = 0
        self.last_time = 0
        self.delta_time = 0
        self.point_num = 1
        self.min_time = 0
        self.max_time = 0.001
        self.init_timer(ot_evt)

    def init_timer(self, ot_evt):
        self.timeout.connect(ot_evt)
        self.stop()

    def restart(self):
        self.now_time = time.time()
        self.last_time = self.now_time
        self.delta_time = 0
        self.time.clear()
        self.time.append(0)
        self.point_num = 1
        self.min_time = 0
        self.max_time = 0.001
        self.start(self.UPDATE_PERIOD)

    def init_time(self):
        self.now_time = time.time()
        self.last_time = self.now_time
        self.delta_time = 0
        self.start(self.UPDATE_PERIOD)

    def iter_time(self):
        self.now_time = time.time()
        self.delta_time = self.now_time - self.last_time
        self.last_time = self.now_time
        self.time.append(self.time[-1] + self.delta_time)
        self.max_time = self.time[-1]


class WaveformViewer(QGraphicsView, Ui_WaveformViewer):
    # 示波器状态
    WFV_DISPLAY_START = 0
    WFV_DISPLAY_PAUSE = 1
    WFV_DISPLAY_RESUME = 2
    # 示波器x轴缩放系数
    XSCALE_COEF = 8

    def __init__(self, widget):
        super(WaveformViewer, self).__init__()
        # self.timer = WaveformTimer(self.update_plot)
        self.init_ui(widget)
        self.init_params()
        self.init_tableWidget()
        self.init_legend()
        self.init_action()

    def init_params(self):
        # timer下标索引
        self.cur_index = 0
        # tab选项索引
        self.cur_tab = 0
        # x轴缩放(=图像所显示的点数)
        self.xscale = self.XSCALE_COEF * 100
        # 示波器状态
        self.display_state = self.WFV_DISPLAY_START
        # 数据帧与时钟
        self.frame1 = Frame1(self.plt)
        self.frame2 = Frame2(self.plt)
        self.timer1 = WaveformTimer(self.update_plot)
        self.timer2 = WaveformTimer(self.update_plot)
        self.cur_frame = self.frame1
        self.cur_timer = self.timer1
        self.cur_table_widget = self.tableWidget
        self.frame_cnt = 1
        # # 导出窗口
        # self.exlist = ExList(*self.get_frames())

    def init_ui(self, widget):
        self.setupUi(widget)
        # 不添加下面这条语句反而可以提高显示速度和波形显示的质量
        # pg.setConfigOptions(antialias=True)
        # 将PlotWidget控件添加到布局中
        self.plt = pg.PlotWidget()
        self.plt_vb = self.plt.getViewBox()
        self.plt_layout = QGridLayout()
        self.plt_layout.addWidget(self.plt)
        self.graphicsView.setLayout(self.plt_layout)
        # 设置PlotWidget的显示格式
        self.plt_legend = self.plt.addLegend()
        self.plt.setLabel(axis='left', text='Value')
        self.plt.setLabel(axis='bottom', text='t (s)')
        self.plt.showGrid(x=True, y=True, alpha=0.5)
        # 添加竖线光标
        self.vline = pg.InfiniteLine(angle=90, movable=False)
        self.vline.setPos(0.001)
        self.plt.addItem(self.vline, ignoreBounds=True)

    def init_tableWidget(self):
        for i, frame in enumerate(self.get_frames()):
            table_widget = self.get_tableWidgets()[i]
            table_widget.setColumnWidth(1, 40)
            # 不添加下面的语句会出现表头隐藏的情况(可能是qtdesigner的bug?)
            table_widget.horizontalHeader().setVisible(True)
            table_widget.verticalHeader().setVisible(True)
            for row, curve in enumerate(frame.get_curves()):
                table_widget.setCellWidget(row, 0, curve.name_box)
                table_widget.setCellWidget(row, 1, curve.color_block)
                # # 当前时间
                # table_widget.setItem(row, 2, QTableWidgetItem('0.001'))
                # table_widget.item(row, 2).setTextAlignment(int(Qt.AlignHCenter | Qt.AlignVCenter))
                # table_widget.item(row, 2).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # 当前数值
                table_widget.setItem(row, 2, QTableWidgetItem('0.000'))
                table_widget.item(row, 2).setTextAlignment(int(Qt.AlignHCenter | Qt.AlignVCenter))
                table_widget.item(row, 2).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # 最小值
                table_widget.setItem(row, 3, QTableWidgetItem(str(curve.dat_min)))
                table_widget.item(row, 3).setTextAlignment(int(Qt.AlignHCenter | Qt.AlignVCenter))
                table_widget.item(row, 3).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # 最大值
                table_widget.setItem(row, 4, QTableWidgetItem(str(curve.dat_max)))
                table_widget.item(row, 4).setTextAlignment(int(Qt.AlignHCenter | Qt.AlignVCenter))
                table_widget.item(row, 4).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # 平均值
                table_widget.setItem(row, 5, QTableWidgetItem(str(curve.get_avr())))
                table_widget.item(row, 5).setTextAlignment(int(Qt.AlignHCenter | Qt.AlignVCenter))
                table_widget.item(row, 5).setFlags(Qt.ItemIsSelectable | Qt.ItemIsEnabled)
                # y轴偏移值(允许编辑)
                table_widget.setItem(row, 6, QTableWidgetItem(str(curve.y_offset)))
                table_widget.item(row, 6).setTextAlignment(int(Qt.AlignHCenter | Qt.AlignVCenter))
                # y轴缩放值(允许编辑)
                table_widget.setItem(row, 7, QTableWidgetItem(str(curve.y_scale)))
                table_widget.item(row, 7).setTextAlignment(int(Qt.AlignHCenter | Qt.AlignVCenter))

    def init_legend(self):
        for frame in self.get_frames()[1:]:
            for curve in frame.get_curves():
                self.plt_legend.removeItem(curve.name)

    def init_action(self):
        self.checkBox_freeze_serialdebugger.toggled.connect(self.checkBox_freeze_slot)
        self.checkBox_legend.toggled.connect(self.update_legend_view)
        self.checkBox_viewall.toggled.connect(self.view_all)
        self.pushButton_resume.clicked.connect(self.resume_display)
        self.pushButton_restart.clicked.connect(self.restart_display)
        self.pushButton_export.clicked.connect(self.export_data)
        self.spinBox_xscale.valueChanged.connect(self.update_xscale_value)
        self.tableWidget.doubleClicked.connect(self.get_color)
        self.tableWidget.cellChanged.connect(self.tableWidget_cellChanged)
        self.tableWidget_2.doubleClicked.connect(self.get_color)
        self.tableWidget_2.cellChanged.connect(self.tableWidget_cellChanged)
        self.tabWidget.currentChanged.connect(self.update_tab)
        self.plt.mouseMoveEvent = self.update_cursor

    def tableWidget_cellChanged(self, row, col):
        if col == 6:
            try:
                frame = self.get_frames()[self.cur_tab]
                table_widget = self.get_tableWidgets()[self.cur_tab]
                frame.get_curves()[row].y_offset = float(table_widget.item(row, col).text())
            except ValueError:
                pass
        elif col == 7:
            try:
                frame = self.get_frames()[self.cur_tab]
                table_widget = self.get_tableWidgets()[self.cur_tab]
                frame.get_curves()[row].y_scale = float(table_widget.item(row, col).text())
            except ValueError:
                pass

    def get_frames(self):
        return [self.frame1, self.frame2]

    def get_timers(self):
        return [self.timer1, self.timer2]

    def get_tableWidgets(self):
        return [self.tableWidget, self.tableWidget_2]

    def checkBox_freeze_slot(self, cmd):
        self.freeze_sd_emit(cmd)

    def freeze_sd_emit(self, cmd):
        if cmd:
            print('冻结调试助手界面')
        else:
            print('解锁调试助手界面')

    def update_tab(self, p_int):
        self.update_legend(self.cur_frame, self.get_frames()[p_int])
        self.cur_tab = p_int
        self.cur_timer = self.get_timers()[self.cur_tab]
        self.cur_frame = self.get_frames()[self.cur_tab]
        self.cur_table_widget = self.get_tableWidgets()[self.cur_tab]
        # print("tab: %s %s %s" % (self.cur_tab, self.cur_timer, self.cur_frame))

    def update_legend(self, last_frame, now_frame):
        # print('legend')
        if self.checkBox_legend.isChecked():
            for curve in last_frame.get_curves():
                self.plt_legend.removeItem(curve.name)
            for curve in now_frame.get_curves():
                self.plt_legend.addItem(curve.curve, curve.name)

    def update_legend_view(self):
        if self.checkBox_legend.isChecked():
            for curve in self.cur_frame.get_curves():
                self.plt_legend.addItem(curve.curve, curve.name)
        else:
            for curve in self.cur_frame.get_curves():
                self.plt_legend.removeItem(curve.name)

    def update_ui_info(self):
        self.plt.setLabel(axis='bottom', text='t (s) 当前时间：{:.3f}'.format(self.cur_timer.time[self.cur_index]))
        self.vline.setPos(self.cur_timer.time[self.cur_index])
        # frame = self.get_frames()[self.cur_tab]
        # table_widget = self.get_tableWidgets()[self.cur_tab]
        for row, curve in enumerate(self.cur_frame.get_curves()):
            # # 当前时间
            # self.cur_table_widget.item(row, 2).setText(str('%.3f' % self.cur_timer.time[self.cur_index]))
            # 当前数值
            self.cur_table_widget.item(row, 2).setText(str('%.3f' % curve.dat[self.cur_index]))
            # 最小值
            if curve.dat_min is not None:
                self.cur_table_widget.item(row, 3).setText(str('%.3f' % curve.dat_min))
            else:
                self.cur_table_widget.item(row, 3).setText(str(curve.dat_min))
            # 最大值
            if curve.dat_max is not None:
                self.cur_table_widget.item(row, 4).setText(str('%.3f' % curve.dat_max))
            else:
                self.cur_table_widget.item(row, 4).setText(str(curve.dat_max))
            # 平均值
            self.cur_table_widget.item(row, 5).setText(str('%.3f' % curve.get_avr()))

    def update_cursor(self, evt):
        pos = self.plt.mapToScene(evt.pos())
        if self.plt.sceneBoundingRect().contains(pos):
            # print(pos)
            mousePoint = self.plt_vb.mapSceneToView(pos)
            # print(mousePoint)
            if(mousePoint.x() > 0):
                coef = (self.cur_timer.max_time - mousePoint.x()) / (self.cur_timer.max_time - self.cur_timer.min_time)
                if self.display_state == self.WFV_DISPLAY_RESUME:
                    if coef <= 0:
                        index = -1
                    elif coef > 1:
                        index = -self.cur_timer.point_num
                    else:
                        index = -int(coef * self.cur_timer.point_num)
                    self.cur_index = index
                elif self.display_state == self.WFV_DISPLAY_PAUSE:
                    if coef < 0:
                        index = -1
                    else:
                        index = -int(coef * self.cur_timer.point_num)

                    if abs(index) > self.frame1.cnt:
                        index = -self.frame1.cnt

                    self.cur_index = index
                    if abs(index) > self.cur_timer.point_num:
                        self.cur_timer.point_num = -index
                        self.cur_timer.min_time = self.cur_timer.time[index]
                        self.frame_plot()
                self.update_ui_info()
        pg.GraphicsView.mouseMoveEvent(self.plt, evt)

    def export_emit(self):
        print('open exlist window')

    def export_data(self):
        self.export_emit()

    def get_color(self, index):
        # https://blog.csdn.net/weixin_43717845/article/details/104246426
        if index.column() == 1:
            qColor = QColorDialog.getColor()
            if qColor.isValid():
                color = qColor.name()
                frame = self.get_frames()[self.cur_tab]
                if index.row() < frame.param_cnt:
                    frame.get_curves()[index.row()].set_color(color)

    def view_all(self):
        if self.checkBox_viewall.isChecked():
            self.plt.enableAutoRange('xy', True)
            self.spinBox_xscale.setEnabled(False)
        else:
            self.spinBox_xscale.setEnabled(True)
            self.plt.enableAutoRange('x', False)

    def resume_display(self):
        if self.display_state == self.WFV_DISPLAY_PAUSE:
            self.display_state = self.WFV_DISPLAY_RESUME
            self.pushButton_resume.setText('暂停')
            self.cur_timer.start(self.cur_timer.UPDATE_PERIOD)
        elif self.display_state == self.WFV_DISPLAY_RESUME:
            self.display_state = self.WFV_DISPLAY_PAUSE
            self.pushButton_resume.setText('继续')
            for tmr in self.get_timers():
                tmr.stop()
            self.frame_plot()   # 更新剩余的点
        elif self.display_state == self.WFV_DISPLAY_START:
            pass

    def restart_display(self):
        if self.display_state == self.WFV_DISPLAY_START:
            self.checkBox_freeze_serialdebugger.setChecked(True)
            self.pushButton_restart.setText('重启')
            self.display_state = self.WFV_DISPLAY_RESUME
            for tmr in self.get_timers():
                tmr.init_time()
                if tmr != self.cur_timer:
                    tmr.stop()
        else:
            status = QMessageBox.question(self, "确定重启？", "注意：重启会清除已接收到的数据", QMessageBox.Yes | QMessageBox.No)
            if status == QMessageBox.Yes:
                self.display_state = self.WFV_DISPLAY_RESUME
                # 时钟暂停
                for tmr in self.get_timers():
                    tmr.stop()
                # 帧清零
                for frame in self.get_frames():
                    frame.clear()
                for tmr in self.get_timers():
                    tmr.restart()
                    if tmr != self.cur_timer:
                        tmr.stop()
                self.cur_index = 0
                self.pushButton_resume.setText('暂停')

    def frame_plot(self):
        # now_time = time.perf_counter()
        for i, frame in enumerate(self.get_frames()):
            timer = self.get_timers()[i]
            frame.plot(timer.time[-timer.point_num:], timer.point_num)
        # print(now_time-time.perf_counter())

        # for frame in self.get_frames():
        #     if frame == self.cur_frame:
        #         frame.plot(self.cur_timer.time[-self.cur_timer.point_num:], self.cur_timer.point_num)
        #     else:
        #         print(frame)
        #         frame.unplot()

    def update_xscale_value(self):
        try:
            self.xscale = self.XSCALE_COEF * int(self.spinBox_xscale.text())
        except ValueError:
            # 当文本编辑框为''时会触发错误，因此采用上次的数值
            pass
        self.update_xscale_view()

    def update_xscale_view(self):
        for i, frame in enumerate(self.get_frames()):
            timer = self.get_timers()[i]
            if not self.checkBox_viewall.isChecked():
                if frame.cnt > self.xscale:
                    # 数据点足够多，可以显示局部数据
                    self.plt.setXRange(timer.time[-self.xscale], timer.max_time)
                    timer.point_num = self.xscale
                    timer.min_time = timer.time[-self.xscale]
                else:
                    # 数据点不够多，显示全部数据
                    self.plt.setXRange(timer.time[0], timer.max_time)
                    timer.point_num = frame.cnt
                    timer.min_time = timer.time[0]
            else:
                self.plt.enableAutoRange('xy', True)
                timer.point_num = frame.cnt
                timer.min_time = timer.time[0]

    def add_frame(self, frame):
        if self.display_state == self.WFV_DISPLAY_RESUME:
            # TODO:加入对数据段的分类处理
            # F1 数据帧
            if frame[0] == self.frame1.func_byte:
                self.timer1.iter_time()
                self.frame1.update(frame[1:])
            # F2 数据帧
            if frame[0] == self.frame2.func_byte:
                self.timer2.iter_time()
                self.frame2.update(frame[1:])

    def update_plot(self):
        # TODO 数据过多的时候可以选择pop掉最早期的数据
        if self.frame1.rx_flag:
            """
            这里选择直接清零，否则每次-1会带来极大的延迟(setData()函数耗时比较多)
            说明：setData()一次就已经接收到较多数据，此时如果每次-1来消除的话
            ，则停止发送帧的时候需要极多的时间浪费在显示相同的数据。setData()会将
            目前为止接收到的数据全部显示出来，因此setData()的调用次数与rx_cnt-=1
            的次数不相同(后者远远大于前者)。等这段时间结束之后才会开始填充0。故这
            里选择直接清零
            """
            self.frame1.rx_flag = 0
        # else:
        #     self.timer1.iter_time()
        #     # 没接收到数据填0
        #     self.frame1.update(None)

        if self.frame2.rx_flag:
            self.frame2.rx_flag = 0
        # else:
        #     self.timer2.iter_time()
        #     self.frame2.update(None)

        # print(self.curve1_show_cnt)
        self.frame_plot()
        self.update_xscale_view()
        self.update_ui_info()

    def test_plot(self):
        # 5ms更新一次
        self.timer1.iter_time()
        dat2 = math.cos(self.timer1.time[-1] * math.pi / 64) + float(np.random.normal(size=1))
        if self.timer1.time[-1] <= 30:
            dat1 = math.sin(self.timer1.time[-1] * math.pi / 16)
        else:
            dat1 = math.sin(self.timer1.time[-1] * math.pi / 32)
        self.frame1.update((dat1, dat2, 0, 0, 0, 0))
        self.timer2.iter_time()
        self.frame2.update((1, 2, 3, 4))
        self.frame_plot()
        self.update_xscale_view()
        self.update_ui_info()


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)

    MainWindow = QMainWindow()
    widget = QWidget()
    wfv = WaveformViewer(widget)
    MainWindow.setCentralWidget(widget)
    MainWindow.resize(1000, 600)
    MainWindow.show()

    # widget = QWidget()
    # ser = WaveformViewer(widget)
    # widget.show()

    sys.exit(app.exec_())
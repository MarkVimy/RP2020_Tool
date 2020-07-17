import pyqtgraph as pg
from pyqtgraph import GraphicsWindow
from pyqtgraph import QtGui, QtCore
import numpy as np


class MyWaveformViewer(object):
    def __init__(self):
        super(MyWaveformViewer, self).__init__()
        self.win = GraphicsWindow()
        self.p1 = self.win.addPlot()
        self.ptr = 0
        self.init_ui()
        self.init_timer()

    def init_ui(self):
        self.win.setWindowTitle('Plot Demo')
        self.win.resize(600, 400)
        self.win.setBackground(background='k')
        self.p1.setLabel(axis='left', text='Y')
        self.p1.setLabel(axis='bottom', text='X')
        self.p1.addLegend()
        self.curve1 = self.p1.plot(pen='y', name='yaw')
        self.curve2 = self.p1.plot(pen='g', name='pitch')

    def init_timer(self):
        self.timer = pg.QtCore.QTimer()
        self.timer.timeout.connect(self.plot_data)
        self.timer.start(100)

    def plot_data(self):
        self.curve1.setData(list(range(11)), [x*x for x in range(11)])
        if self.ptr == 0:
            # self.p1.disableAutoRange('xy')
            self.p1.enableAutoRange(axis='xy', enable=False, x=1, y=0.5)
            self.p1.disableAutoRange('xy')
        self.ptr += 1


if __name__ == '__main__':
    import sys
    app = pg.mkQApp()
    wfv = MyWaveformViewer()
    sys.exit(app.exec_())


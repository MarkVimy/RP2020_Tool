from GUI.widget_exlist import Ui_ExList
from PyQt5.QtGui import QIcon
from PyQt5.QtCore import QStringListModel
from PyQt5.QtWidgets import QWidget, QApplication, QAbstractItemView, QMessageBox
from APP.myxlsx import MyWorkBook
from APP.mywfv import Frame, WaveformTimer


class ExList(QWidget, Ui_ExList):
    def __init__(self, *args):
        super(ExList, self).__init__()
        self.frames, self.timers = [], []
        self.init_ui()
        self.init_params(*args)
        self.init_action()

    def init_params(self, *args):
        for item in args:
            if isinstance(item, Frame):
                self.frames.append(item)
            elif isinstance(item, WaveformTimer):
                self.timers.append(item)

        # TODO:将来这里的2替换成传进来的frame的个数
        for i in range(len(self.frames)):
            listview_left, listview_right = self.get_listviews()[2*i:2*(i+1)]
            # 新建左列并设置数据
            listview_model = QStringListModel(self)
            listview_model.setStringList([curve.name for curve in self.frames[i].get_curves()])
            listview_left.setModel(listview_model)
            listview_left.setEditTriggers(QAbstractItemView.NoEditTriggers)
            # 新建右列
            listview_right.setModel(QStringListModel(self))
            listview_right.setEditTriggers(QAbstractItemView.NoEditTriggers)

    def init_ui(self):
        self.setupUi(self)
        self.setWindowTitle('导出工具')
        self.setWindowIcon(QIcon('../GUI/RpLogo.jpg'))

    def init_action(self):
        self.listView_left_1.doubleClicked.connect(lambda: self.transfer(self.listView_left_1))
        self.listView_right_1.doubleClicked.connect(lambda: self.transfer(self.listView_right_1))
        self.listView_left_2.doubleClicked.connect(lambda: self.transfer(self.listView_left_2))
        self.listView_right_2.doubleClicked.connect(lambda: self.transfer(self.listView_right_2))
        self.pushButton_all2right.clicked.connect(self.all2right)
        self.pushButton_all2left.clicked.connect(self.all2left)
        self.pushButton_confirm.clicked.connect(self.export)

    def get_listviews(self):
        return [self.listView_left_1, self.listView_right_1, self.listView_left_2, self.listView_right_2]

    def get_reverse_listview(self, listview):
        for i, view in enumerate(self.get_listviews()):
            if view == listview:
                i = i - 1 if i % 2 else i + 1
                return self.get_listviews()[i]

    def all2right(self):
        # 同步左右tab的index
        tab_left_index = self.tabWidget_left.currentIndex()
        # 在偶数下标(左列)中找到对应的listview
        listview = self.get_listviews()[::2][tab_left_index]
        listview_model = listview.model()
        # 左 -> 右
        for i in range(listview_model.rowCount()):
            listview.setCurrentIndex(listview_model.index(i))
            self.transfer(listview)

    def all2left(self):
        # 同步左右tab的index
        tab_right_index = self.tabWidget_right.currentIndex()
        # 在奇数下标(右列)中找到对应的listview
        listview = self.get_listviews()[1::2][tab_right_index]
        listview_model = listview.model()
        # 删除右列所有项
        listview_model.removeRows(0, listview_model.rowCount())

    def export(self, *args):
        # 有效帧数
        frame_num = 0
        # 获取右边的全部listview
        right_listviews = self.get_listviews()[1::2]
        # xlsx工作簿
        wb = MyWorkBook()

        # 工作簿初始化
        wb.export_start()
        # 导出所有选中的数据
        for i, listview in enumerate(right_listviews):
            listview_model = listview.model()
            # 每次重新清空(防止第2次进入的时候仍保留上一帧数据)
            curves = []
            # 如果右列表非空
            if listview_model.rowCount():
                frame_num += 1
                # 完成一帧的遍历
                for j in range(listview_model.rowCount()):
                    # 从0开始遍历
                    listview.setCurrentIndex(listview_model.index(j))
                    # 找到帧[i]中对应的curve_name的位置
                    k = [curve.name for curve in self.frames[i].get_curves()].index(listview.currentIndex().data())
                    curve = self.frames[i].get_curves()[k]
                    curves.append(curve)
                # 创建一页Sheet并将数据填入其中
                wb.export_add_sheet(self.timers[i].time[1:], *[curve.dat[1:] for curve in curves], headings=['时间'] + [curve.name for curve in curves], sheet_name='Frame %d' % (i+1))
        # 保存wb并给出提示信息
        wb.export_end()
        QMessageBox.information(self, '导出数据', '导出成功! 共 %d 帧'%frame_num, QMessageBox.Yes)

    def traversal(self, listview, data):
        listmodel = listview.model()
        # 遍历该数据是否已存在
        for r in range(listmodel.rowCount()):
            if data == listmodel.index(r).data():
                # 该数据已存在
                return True
        # 该数据不存在
        return False

    def transfer(self, listview):
        # 偶数为左边的list
        if not self.get_listviews().index(listview) % 2:
            # 同步左右tab的index
            tab_left_index = self.tabWidget_left.currentIndex()
            self.tabWidget_right.setCurrentIndex(tab_left_index)
            # 左 -> 右
            r_listview = self.get_reverse_listview(listview)
            if self.traversal(r_listview, listview.currentIndex().data()):
                # 转移失败
                return False
            r_listview_model = r_listview.model()
            r_listview_model.insertRow(r_listview_model.rowCount())
            data = listview.currentIndex().data()
            index = r_listview_model.index(r_listview_model.rowCount() - 1)
            r_listview_model.setData(index, data)
        # 奇数为右边的list
        else:
            # 同步左右tab的index
            tab_right_index = self.tabWidget_right.currentIndex()
            self.tabWidget_left.setCurrentIndex(tab_right_index)
            # 右 -> 左
            listview.model().removeRow(listview.currentIndex().row())
        # 转移成功
        return True


if __name__ == '__main__':
    import sys
    app = QApplication(sys.argv)
    exlist = ExList([1,2], [3,4])
    sys.exit(app.exec_())

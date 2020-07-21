import time
import xlsxwriter as xlwt


class MyWorkBook(xlwt.Workbook):
    def __init__(self):
        super().__init__()
        self.workbook = None

    def export(self, *args, headings=['时间', '数值']):
        col_num = len(headings)
        # 用时间戳来命名文件
        t = '-'.join(map(str, time.localtime()[:6]))
        filename = t + '.xlsx'
        # 新建excel表
        wb = xlwt.Workbook(filename)
        # 新建sheet(sheet的名称为"bullet_spd")
        ws = wb.add_worksheet('新建列')
        # 写入表头
        ws.write_row(0, 0, headings)
        # 写入数据
        for col in range(col_num):
            ws.write_column(1, col, args[col])
        # 保存excel文件
        wb.close()

    def export_start(self, fp):
        # 用时间戳来命名文件
        t = '-'.join(map(str, time.localtime()[:6]))
        filename = t + '.xlsx'
        # 新建excel表
        self.workbook = xlwt.Workbook(fp + filename)

    def export_add_sheet(self, *args, headings=['时间', '数值'], sheet_name=None):
        if len(args) != len(headings):
            # print('Wrong!len(args) mismatch len(headings).Please check')
            return
        ws = self.workbook.add_worksheet(sheet_name)
        col_num = len(headings)
        ws.set_column(0, col_num, 15)
        cell_format = self.workbook.add_format({'bold': True})
        ws.set_row(0, 15, cell_format)
        # 写入表头
        ws.write_row(0, 0, headings)
        # 写入数据
        for col in range(col_num):
            ws.write_column(1, col, args[col])

    def export_end(self):
        # 保存excel文件
        self.workbook.close()


if __name__ == '__main__':
    ex = MyWorkBook()
    dat1 = [1, 2, 3, 4, 5]
    dat2 = [123, 234, 345, 456, 567]
    # ex.export(dat1, dat2, headings=['PWM', '射速'])
    # ex.export_add_sheet(dat1, dat2, headings=['1', '2', '3'])

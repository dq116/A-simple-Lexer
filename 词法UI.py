import sys
from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5 import QtGui
from lexer_utils import *
import lexer
import win32ui
import os
import time
import number_bar
class mybutton(QPushButton):
    def __init__(self,name,wi):
        super().__init__(wi)
        self.setText(name)
        self.setFont(QFont("Miscrosoft YaHei",10))

    def focusInEvent(self, a0: QtGui.QFocusEvent) -> None:#设置阴影特效
        shadow = QGraphicsDropShadowEffect()
        shadow.setBlurRadius(26)
        shadow.setOffset(0,0)
        pal = self.palette()
        color = pal.color(QPalette.Background)
        rgba =color.getRgb()
        brigt_num = 0
        r = rgba[0]+brigt_num
        g = rgba[1] + brigt_num
        b = rgba[2] + brigt_num
        shadow.setColor(QColor(r,g,b,255))
        self.setGraphicsEffect(shadow)
    def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:#失去焦点移除特效
        self.setGraphicsEffect(None)

class myform(QWidget):
    lab2,line= None,None

    def __init__(self):
        super().__init__()
        self.initUI()
        self.back_up=None


    def initUI(self):
        self.setGeometry(100,100,1250,600)
        self.setWindowTitle(' ')
        self.setWindowIcon(QIcon('C:/Users/11610/data_for_python/pka1'))

        btn1=mybutton(n_open,self)
        btn1.setStyleSheet('QPushButton{background-color:rgba(134,227,208,255);border-radius:25px;}'
                           'QPushButton:hover{background-color:rgba(134,227,208,100)}'
                           'QPushButton:pressed{background-color:grey}'
                           'QPushButton:focus{outline:None}'
                   )
        btn2 = mybutton(n_file, self)
        btn2.setStyleSheet('QPushButton{background-color:rgba(208,255,165,255);border-radius:25px;}'
                           'QPushButton:hover{background-color:rgba(208, 255, 165,100)}'
                           'QPushButton:pressed{background-color:grey}'
                           'QPushButton:focus{outline:None}'
                           )
        btn3 = mybutton(n_save, self)
        btn3.setStyleSheet('QPushButton{background-color:rgba(255,221,148,255);border-radius:25px;}'
                           'QPushButton:hover{background-color:rgba(255,221,148,100)}'
                           'QPushButton:pressed{background-color:grey}'
                           'QPushButton:focus{outline:None}'
                           )
        btn4 = mybutton(n_compile, self)
        btn4.setStyleSheet("QPushButton{background-color:rgba(250,137,123,255);border-radius:25px;}"
                           'QPushButton:hover{background-color:rgba(250,137,123,100)}'
                           'QPushButton:pressed{background-color:grey}'
                           'QPushButton:focus{outline:None}'
                           )
        btn1.setFixedSize(50, 50)
        btn2.setFixedSize(50, 50)
        btn3.setFixedSize(50, 50)
        btn4.setFixedSize(50, 50)
        btn1.clicked.connect(self.buttonClicked)
        btn2.clicked.connect(self.buttonClicked)
        btn3.clicked.connect(self.buttonClicked)
        btn4.clicked.connect(self.buttonClicked)
        self.txt=number_bar.QCodeEditor(self)
        self.txt.setFont(QFont("Roman times",12))
        self.txt.setWordWrapMode(QTextOption.NoWrap)

        self.table=QTableWidget(20,5)
        self.table.setHorizontalHeaderLabels(['行号','符号','描述','类型码','内容'])
        self.table.verticalHeader().setVisible(False)
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.prompt=QLabel(prompt_init)
        self.prompt.setMinimumHeight(150)
        self.prompt.setStyleSheet("font-family:Roman times;font-weight:bold;font-size:16px;color:rgba(20,20,20,200);background-color:rgba(255,255,255,255)")
        self.path_lab = QLabel('path:')
        self.path_lab.setFont(QFont("Roman times",10,QFont.Bold))
        self.path_line = QLineEdit()
        self.path_line.setFont(QFont("Miscrosoft YaHei", 10))
        self.path_line.setMinimumHeight(50)

        layout_upper_right = QHBoxLayout()
        layout_upper_right.addWidget(self.path_lab)
        layout_upper_right.addWidget(self.path_line)
        layout_upper_right.addWidget(btn1)
        layout_upper_right.addWidget(btn2)
        layout_upper_right.addWidget(btn3)
        layout_upper_right.addWidget(btn4)
        layout_right=QVBoxLayout()
        layout_right.addLayout(layout_upper_right)
        layout_right.addWidget(self.txt)
        layout_right.addWidget(self.prompt)

        layout_whole = QHBoxLayout()
        layout_whole.addWidget(self.table)
        layout_whole.addLayout(layout_right)
        self.setLayout(layout_whole)
        self.show()


    def buttonClicked(self):

        sender = self.sender()
        name=sender.text()
        if name==n_open:
            if not self.path_line.text():
                self.prompt.setText('please input the source code path')
            else:
                path=self.path_line.text()
                self.set_path(path)

        elif name == n_file:
            dlg = win32ui.CreateFileDialog(1)  # 1表示打开文件对话框
            # dlg.SetOFNInitialDir(os.path.join(os.path.expanduser("~"), 'Desktop'))   # 设置初始显示目录为桌面
            dlg.SetOFNInitialDir(os.getcwd()) #初始显示目录为当前工作目录
            dlg.DoModal()
            path = dlg.GetPathName()
            if path:
                self.set_path(path)

        elif name == n_compile:

            if not self.txt.toPlainText():
                self.prompt.setText(error_txt)
            else:

                is_right,r=lexer.analyze(self.txt.toPlainText())
                if is_right:
                    self.table.setRowCount(len(r))
                    row=0
                    for i in r:
                        column=0
                        for j in i:
                            item=QTableWidgetItem(str(j))
                            self.table.setItem(row,column,item)
                            column+=1
                        row+=1
                    self.prompt.setText('0 error\n')
                    ##自动保存
                    # if self.path_line.text():
                    #     is_right, message = self.save(self.txt.toPlainText())
                    #     if is_right:
                    #         self.prompt.setText(self.prompt.text()+'\nsave sucessfully\n'+time.asctime(time.localtime(time.time())))
                    #     else:
                    #         self.prompt.setText(self.prompt.text()+message)
                else:
                    self.prompt.setText(r)
        elif name==n_save:
            is_right,message=self.save(self.txt.toPlainText())
            if is_right:
                self.prompt.setText('save sucessfully\n'+time.asctime(time.localtime(time.time())))
            else:
                self.prompt.setText(message)
    def set_path(self, path):

        is_right,content=lexer.read_file(path)
        if is_right:
            self.path_line.setText(path)
            self.txt.setPlainText(content)
            self.back_up = content
        else:
            self.prompt.setText(content)


    def save(self,s):
        path = self.path_line.text()
        if path:
            try:
                if s == self.back_up:
                    return False, no_change
                with open(path, "w",encoding="UTF-8") as f:
                    f.write(s)
                    return True,''
            except IOError as err:
                return  False,str(err)  # str()将异常转换为字符串
        else:
            return False,(error_save)


if __name__ == '__main__':
    app =  QApplication(sys.argv)
    w = myform()
    sys.exit(app.exec_())

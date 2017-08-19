#!/usr/bin/python
#-*- coding: utf-8 -*-

from PyQt4.QtGui import *
from PyQt4.QtCore import QModelIndex
import sys
import mypydicUI
import numpy as np
from xlrd import open_workbook

book = open_workbook("dic.xlsx")
sheet = book.sheet_by_index(0) #If your data is on sheet 1

column1 = sheet.col_values(0) # keyword
column2 = sheet.col_values(1) # title
column3 = sheet.col_values(2) # code
column4 = sheet.col_values(3) # explain code

class XDialog(QDialog, mypydicUI.Ui_Dialog):

    def __init__(self):
        QDialog.__init__(self)
        # setupUi() 메서드는 화면에 다이얼로그 보여줌
        self.setupUi(self)
        
        # 버튼 이벤트 핸들러
        self.btnFind.clicked.connect(self.findData)
        self.btnSelect.clicked.connect(self.selectData)

     # 저장 버튼 클릭시 listOFtitle
    def findData(self):
        key = self.keyWord.toPlainText()
        indexArr=[]
        index=0
        for s in column1 :
            if key in s:
                indexArr.append(index)
            index +=1
        #self.listOFtitle.clear()
        model = QStandardItemModel()
        for index in indexArr:
            #self.listOFtitle.append(column2[index])
            model.appendRow(QStandardItem(str(index)+" : "+column2[index]))
        self.listOFtitle.setModel(model)

    def selectData(self):
        currentITEM=self.listOFtitle.selectedIndexes()[0]
        index = int(currentITEM.data().toString().split(':')[0])
        self.code.setText(column3[index])
        self.codeExp.setText(column4[index])

app = QApplication(sys.argv)
dlg = XDialog()
dlg.show()
app.exec_()
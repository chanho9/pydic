#!/usr/bin/python
#-*- coding: utf-8 -*-

from PyQt5.QtGui import QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow
from PyQt5.uic import loadUi
from PyQt5.QtCore import QObject, QEvent
import sys
import webbrowser
import pandas as pd
import pickle

import qdarktheme


class Filter(QObject):
    def __init__(self, _Button):
        super().__init__()
        self.targetButton = _Button

    def eventFilter(self, widget, event):
        # FocusOut event
        if event.type() == QEvent.FocusOut:
            self.targetButton.setEnabled(True)
            return False
        elif event.type() == QEvent.FocusIn:
            self.targetButton.setDisabled(True)
            return False
        else:
            return False


class MyApp(QMainWindow):

    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.dlg = loadUi('pydic.ui')
        # db 불러오기
        self.selectedDataSet = None
        self.selectedCategory = None
        self.iNeedFocus = False
        self.getDBdata()

        self.dlg.keyWord.returnPressed.connect(self.findData)

        # 에디트로 복귀하는 키를 비활성화
        self._filter = Filter(self.dlg.EditButton)
        self.dlg.keyWord.installEventFilter(self._filter)
        self.dlg.EditButton.clicked.connect(self.returnEdit)
        self.dlg.EditButton.setShortcut("Return")

        self.dlg.title.itemClicked.connect(self.selectData)
        self.dlg.title.currentItemChanged.connect(self.selectData)
        self.dlg.title.itemDoubleClicked.connect(self.FindOnWeb)

        self.dlg.columnComboBox.currentIndexChanged.connect(self.viewerUpdate)
        self.dlg.categoryComboBox.currentIndexChanged.connect(self.categoryUpdate)
        self.dlg.updateButton.clicked.connect(self.dictionaryUpdate)
        self.dlg.categoryCheckBox.stateChanged.connect(self.wholeCategoryUpdate)

        # 복사설정
        self.clipboard = QApplication.clipboard()
        self.dlg.label_1.clicked.connect(self.copyTitle)
        self.dlg.label_2.clicked.connect(lambda: self.copyText(self.dlg.browser_1))
        self.dlg.label_3.clicked.connect(lambda: self.copyText(self.dlg.browser_2))
        self.dlg.label_4.clicked.connect(lambda: self.copyText(self.dlg.browser_3))

        # clickable(self.dlg.label_2).connect(lambda: self.copyText(self.dlg.browser_1))
        # clickable(self.dlg.label_3).connect(lambda: self.copyText(self.dlg.browser_2))
        # clickable(self.dlg.label_4).connect(lambda: self.copyText(self.dlg.browser_3))


        # 초기 세팅
        self.dlg.label_1.setText( str(self.header[1]) ) # title
        self.dlg.label_1.setShortcut("Alt+F1")
        self.dlg.label_2.setText( str(self.header[2]) ) # browser1
        self.dlg.label_2.setShortcut("Alt+F2")
        self.dlg.label_3.setText( str(self.header[3]) ) # browser2
        self.dlg.label_3.setShortcut("Alt+F3")
        self.dlg.label_4.setText( str(self.header[4]) ) # browser3
        self.dlg.label_4.setShortcut("Alt+F4")

        # 사용가능 박스 생성
        self.dlg.columnComboBox.addItem("활성화 선택")
        for i, title in enumerate(self.dataList):
            if self.selectedViewer[i]:
                self.dlg.columnComboBox.addItem("✓ "+str(title))
            else:
                self.dlg.columnComboBox.addItem(str(title))

        # 사용가능 카테고리 생성
        self.dlg.categoryComboBox.addItem("카테고리 활성화 선택")
        for i, title in enumerate(self.categoryList):
            if self.selectedCategory[i]:
                self.dlg.categoryComboBox.addItem("✓ "+str(title))
            else:
                self.dlg.categoryComboBox.addItem(str(title))


        self.dlg.show()


    def returnEdit(self):
        self.dlg.terminal.setText("입력 대기중...")
        self.dlg.keyWord.clear()
        self.dlg.keyWord.setFocus()


    def viewerUpdate(self):
        index = self.dlg.columnComboBox.currentIndex()

        if index != 0:
            index -= 1
            self.selectedViewer[index] = not self.selectedViewer[index]
            title = self.dataList[index]
            if self.selectedViewer[index]:
                self.dlg.columnComboBox.setItemText(index+1, "✓ "+str(title))

                if index == 0:
                    self.dlg.browser_1.setMaximumSize(16777215, 16777215)
                    self.dlg.label_2.setMaximumSize(16777215, 16777215)
                elif index == 1:
                    self.dlg.browser_2.setMaximumSize(16777215, 16777215)
                    self.dlg.label_3.setMaximumSize(16777215, 16777215)
                elif index == 2:
                    self.dlg.browser_3.setMaximumSize(16777215, 16777215)
                    self.dlg.label_4.setMaximumSize(16777215, 16777215)

            else:
                self.dlg.columnComboBox.setItemText(index+1, str(title))
                if index == 0:
                    self.dlg.browser_1.setMaximumSize(16777215, 0)
                    self.dlg.label_2.setMaximumSize(16777215, 0)
                elif index == 1:
                    self.dlg.browser_2.setMaximumSize(16777215, 0)
                    self.dlg.label_4.setMaximumSize(16777215, 0)
                elif index == 2:
                    self.dlg.browser_3.setMaximumSize(16777215, 0)
                    self.dlg.label_4.setMaximumSize(16777215, 0)

        self.dlg.columnComboBox.setCurrentIndex(0)


    def wholeCategoryUpdate(self):
        if self.dlg.categoryCheckBox.isChecked():
            for index in range(len(self.selectedCategory)):
                self.selectedCategory[index] = True
                title = self.categoryList[index]
                self.dlg.categoryComboBox.setItemText(index+1, "✓ "+ str(title))
        else:
            for index in range(len(self.selectedCategory)):
                self.selectedCategory[index] = False
                title = self.categoryList[index]
                self.dlg.categoryComboBox.setItemText(index+1, str(title))



    def categoryUpdate(self):
        index = self.dlg.categoryComboBox.currentIndex()

        if index != 0:
            index -= 1
            self.selectedCategory[index] = not self.selectedCategory[index]
            title = self.categoryList[index]
            if self.selectedCategory[index]:
                self.dlg.categoryComboBox.setItemText(index+1, "✓ "+ str(title))
            else:
                self.dlg.categoryComboBox.setItemText(index+1, str(title))

        self.dlg.categoryComboBox.setCurrentIndex(0)


    def getDBdata(self):
        try:
            with open('db.pickle','rb') as f:
                (self.df, self.header, self.dataList, self.categoryList, self.selectedCategory, self.selectedViewer) = pickle.load(f)
            self.dlg.terminal.setText("사전이 확인되었습니다.")
        except Exception as e:
            self.dlg.terminal.setText("사전을 업데이트 합니다.")
            self.dictionaryUpdate()


    def dictionaryUpdate(self):

        self.df = pd.read_excel("dic.xlsx")

        self.header = self.df.columns.to_list()
        self.dataList = self.header[2:5]

        self.categoryList = self.df['category'].drop_duplicates().to_list()

        if (self.selectedCategory == None) or (len(self.categoryList) != len(self.selectedCategory)):
            self.selectedCategory = [True] * len(self.categoryList)
            self.selectedViewer = [True, True, True]

        with open('db.pickle','wb') as f:
            pickle.dump((self.df, self.header, self.dataList, self.categoryList, self.selectedCategory, self.selectedViewer)
                    , f)


    def findData(self):

        self.dlg.title.clear()
        self.dlg.browser_1.clear()
        self.dlg.browser_2.clear()
        self.dlg.browser_3.clear()

        keyword = self.dlg.keyWord.text()
        keys = keyword.split(" ")

        for i, key in enumerate(keys):
            if i == 0:
                ans = self.df['keyword'].str.contains(key)
            else:
                ans = ans & self.df['keyword'].str.contains(key)

        # 카테고리 검색
        isCategory = False
        for i, category in enumerate(self.selectedCategory):
            if category:
                if not isCategory:
                    isCategory = True
                    categoryAns = self.df['category']==self.categoryList[i]
                else:
                    categoryAns = categoryAns | (self.df['category']==self.categoryList[i])

        _ = self.df[ans & categoryAns]

        if not isCategory:
            _ = self.df[ans]
        else:
            _ = self.df[ans & categoryAns]

        _index = _.index

        for index, title, in enumerate(_['title']):
            self.dlg.title.insertItem(index, str(_index[index])+" : "+title)

        # default 선택값
        _item = self.dlg.title.item(0)
        self.dlg.title.setCurrentItem(_item)
        self.dlg.title.setFocus()

        self.selectData()


    def copyText(self, browser):
        self.clipboard.setText(browser.toPlainText())

    def copyTitle(self):
        self.clipboard.setText(self.title)

    def selectData(self):

        countNum = self.dlg.title.count()

        if countNum > 0:
            try:
                currentITEM=self.dlg.title.selectedIndexes()[0]
                index = currentITEM.data().split(':')[0]
                self.title = currentITEM.data().split(' : ')[1]
            except:
                currentITEM = self.dlg.title.item(0)
                index = currentITEM.text().split(':')[0]
                self.title = currentITEM.text().split(' : ')[1]

            selectedData = self.df.iloc[int(index)]

            data1 = str(selectedData[2])
            data2 = str(selectedData[3])
            data3 = str(selectedData[4])
            image = str(selectedData[5])

            self.dlg.browser_1.setText(data1)
            self.dlg.browser_2.setText(data2)
            self.dlg.browser_3.setText(data3)

            if image != None:
                pixmap = QPixmap("image/"+image)
                self.dlg.ImageViewer.setPixmap(pixmap)
            else:
                pixmap = QPixmap("image/0.png")
                self.dlg.ImageViewer.setPixmap(pixmap)

        self.iNeedFocus = True


    def FindOnWeb(self):
        self.selectData()
        webbrowser.open("https://ja.dict.naver.com/#/search?query="+self.title)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    qdarktheme.setup_theme()
    ex = MyApp()
    sys.exit(app.exec_())

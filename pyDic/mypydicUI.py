# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'pydic.ui'
#
# Created by: PyQt4 UI code generator 4.11.4
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Dialog(object):
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(402, 646)
        self.keyWord = QtGui.QTextEdit(Dialog)
        self.keyWord.setGeometry(QtCore.QRect(10, 10, 371, 31))
        self.keyWord.setObjectName(_fromUtf8("keyWord"))
        self.btnFind = QtGui.QPushButton(Dialog)
        self.btnFind.setGeometry(QtCore.QRect(10, 50, 181, 31))
        self.btnFind.setObjectName(_fromUtf8("btnFind"))
        self.code = QtGui.QTextEdit(Dialog)
        self.code.setGeometry(QtCore.QRect(10, 410, 371, 221))
        self.code.setObjectName(_fromUtf8("code"))
        self.listOFtitle = QtGui.QListView(Dialog)
        self.listOFtitle.setGeometry(QtCore.QRect(10, 90, 371, 141))
        self.listOFtitle.setObjectName(_fromUtf8("listOFtitle"))
        self.btnSelect = QtGui.QPushButton(Dialog)
        self.btnSelect.setGeometry(QtCore.QRect(200, 50, 181, 31))
        self.btnSelect.setObjectName(_fromUtf8("btnSelect"))
        self.codeExp = QtGui.QTextEdit(Dialog)
        self.codeExp.setGeometry(QtCore.QRect(10, 240, 371, 161))
        self.codeExp.setObjectName(_fromUtf8("codeExp"))

        self.retranslateUi(Dialog)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Dialog", None))
        self.btnFind.setText(_translate("Dialog", "FIND", None))
        self.btnSelect.setText(_translate("Dialog", "SELECT", None))


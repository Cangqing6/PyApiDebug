from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, Qt)
from PySide6.QtWidgets import (QCheckBox, QGroupBox,
                               QHBoxLayout, QLabel, QLineEdit, QPushButton,
                               QVBoxLayout, QWidget)


class Ui_Dialog(object):
    def setupUi(self, Dialog):
        if not Dialog.objectName():
            Dialog.setObjectName(u"SearchDialog")
        Dialog.setFixedSize(390, 190)
        self.verticalLayoutWidget_2 = QWidget(Dialog)
        self.verticalLayoutWidget_2.setObjectName(u"verticalLayoutWidget_2")
        self.verticalLayoutWidget_2.setGeometry(QRect(10, 20, 371, 61))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget_2)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.verticalLayoutWidget_2)
        self.label.setObjectName(u"label")

        self.horizontalLayout_2.addWidget(self.label, 0, Qt.AlignmentFlag.AlignLeft)

        self.lineEdit_FindTarget = QLineEdit(self.verticalLayoutWidget_2)
        self.lineEdit_FindTarget.setObjectName(u"lineEdit_FindTarget")

        self.horizontalLayout_2.addWidget(self.lineEdit_FindTarget)

        self.Button_next = QPushButton(self.verticalLayoutWidget_2)
        self.Button_next.setObjectName(u"Button_next")

        self.horizontalLayout_2.addWidget(self.Button_next)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        self.Button_count = QPushButton(self.verticalLayoutWidget_2)
        self.Button_count.setObjectName(u"Button_count")

        self.verticalLayout.addWidget(self.Button_count, 0, Qt.AlignmentFlag.AlignRight)

        self.groupBox = QGroupBox(Dialog)
        self.groupBox.setObjectName(u"groupBox")
        self.groupBox.setGeometry(QRect(10, 80, 361, 81))
        self.verticalLayoutWidget_3 = QWidget(self.groupBox)
        self.verticalLayoutWidget_3.setObjectName(u"verticalLayoutWidget_3")
        self.verticalLayoutWidget_3.setGeometry(QRect(10, 20, 341, 51))
        self.verticalLayout_2 = QVBoxLayout(self.verticalLayoutWidget_3)
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.verticalLayout_2.setContentsMargins(0, 0, 0, 0)
        self.checkBox_ReverseSeek = QCheckBox(self.verticalLayoutWidget_3)
        self.checkBox_ReverseSeek.setObjectName(u"checkBox_ReverseSeek")

        self.verticalLayout_2.addWidget(self.checkBox_ReverseSeek)

        self.checkBox_Case = QCheckBox(self.verticalLayoutWidget_3)
        self.checkBox_Case.setObjectName(u"checkBox_Case")

        self.verticalLayout_2.addWidget(self.checkBox_Case)

        self.retranslateUi(Dialog)

        QMetaObject.connectSlotsByName(Dialog)

    # setupUi

    def retranslateUi(self, Dialog):
        self.Button_next.setMinimumWidth(90)
        self.Button_next.setMinimumHeight(24)
        self.Button_count.setMinimumWidth(90)
        self.Button_count.setMinimumHeight(24)
        Dialog.setWindowTitle(QCoreApplication.translate("Dialog", u"搜索", None))
        self.label.setText(QCoreApplication.translate("Dialog", u"\u67e5\u627e\u76ee\u6807(F):", None))
        self.Button_next.setText(QCoreApplication.translate("Dialog", u"\u67e5\u627e\u4e0b\u4e00\u4e2a", None))
        self.Button_count.setText(QCoreApplication.translate("Dialog", u"\u8ba1\u6570", None))
        self.groupBox.setTitle(QCoreApplication.translate("Dialog", u"\u67e5\u8be2\u6a21\u5f0f", None))
        self.checkBox_ReverseSeek.setText(QCoreApplication.translate("Dialog", u"\u53cd\u5411\u67e5\u627e", None))
        self.checkBox_Case.setText(QCoreApplication.translate("Dialog", u"\u5339\u914d\u5927\u5c0f\u5199", None))
    # retranslateUi

# -*- coding: utf-8 -*-

################################################################################
## Form generated from reading UI file 'designerWEsSZx.ui'
##
## Created by: Qt User Interface Compiler version 6.9.0
##
## WARNING! All changes made in this file will be lost when recompiling UI file!
################################################################################

from PySide6.QtCore import (QCoreApplication, QMetaObject, QRect, QSize, QByteArray, Qt)
from PySide6.QtGui import QPixmap, QPainter, QFont, QColor
from PySide6.QtSvg import QSvgRenderer

from PySide6.QtWidgets import (QCheckBox, QComboBox, QHBoxLayout, QLabel, QLineEdit, QMainWindow, QPlainTextEdit,
                               QPushButton, QSizePolicy, QTabWidget, QVBoxLayout, QWidget, QStyleOptionComboBox, QStyle,
                               QStyledItemDelegate)


#  下拉框下拉显示的数据
class ComboDelegate(QStyledItemDelegate):
    def paint(self, painter, option, index):
        text = index.data(Qt.DisplayRole)
        painter.save()

        # 使用 QStyle.StateFlag 判断状态
        if option.state & QStyle.State_Selected:
            painter.fillRect(option.rect, QColor("#4a90e2"))  # 选中背景
            painter.setPen(Qt.white)
        elif option.state & QStyle.State_MouseOver:
            painter.fillRect(option.rect, QColor("#b3cde6"))  # 悬停背景
            painter.setPen(Qt.black)
        else:
            painter.fillRect(option.rect, QColor("#ffffff"))  # 普通背景
            painter.setPen(Qt.black)

        # 自定义字体
        font = QFont("Microsoft YaHei", 10)
        painter.setFont(font)

        # 绘制文字
        painter.drawText(option.rect.adjusted(4, 0, 0, 0), Qt.AlignVCenter | Qt.AlignLeft, text)
        painter.restore()

    def sizeHint(self, option, index):
        # 固定每一行高度 30px
        base_size = super().sizeHint(option, index)
        return base_size.expandedTo(QSize(base_size.width(), 16))


#  自定义下拉框
class Custom_Arrow_ComboBox(QComboBox):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setItemDelegate(ComboDelegate())  # 设置自定义委托
        # 你的自定义 SVG
        self.svg_data = b'''
<svg width="100" height="100" viewBox="0 0 100 100" xmlns="http://www.w3.org/2000/svg">
  <polygon points="30,40 70,40 50,70" fill="#4a90e2"/>
</svg>'''
        # 渲染 SVG 到 QPixmap
        size = 22  # 改成你想要的尺寸
        renderer = QSvgRenderer(QByteArray(self.svg_data))
        self.arrow_pix = QPixmap(size, size)
        self.arrow_pix.fill(Qt.transparent)
        painter = QPainter(self.arrow_pix)
        painter.setRenderHint(QPainter.Antialiasing)

        renderer.render(painter)
        painter.end()

    def paintEvent(self, event):
        # 先调用默认绘制
        super().paintEvent(event)

        # 绘制自定义箭头
        opt = QStyleOptionComboBox()
        self.initStyleOption(opt)
        painter = QPainter(self)
        arrow_rect = self.style().subControlRect(QStyle.CC_ComboBox, opt, QStyle.SC_ComboBoxArrow, self)

        # 居中绘制箭头
        painter.drawPixmap(
            arrow_rect.x() + (arrow_rect.width() - self.arrow_pix.width()) // 2,
            arrow_rect.y() + (arrow_rect.height() - self.arrow_pix.height()) // 2,
            self.arrow_pix
        )
        painter.end()

    def showPopup(self):
        # 调用原始 showPopup 展开下拉列表
        super().showPopup()
        # 强制下拉列表出现在控件下方
        popup = self.view().window()  # 获取弹出窗口
        if popup:
            pos = self.mapToGlobal(self.rect().bottomLeft())
            popup.move(pos)


class Ui_MainWindow(QMainWindow):
    def __init__(self, version):
        super().__init__()
        self.tab_2 = None
        self.tab_3 = None
        self.label = None
        self.label_2 = None
        self.label_3 = None
        self.label_4 = None
        self.label_5 = None
        self.label_9 = None
        self.label_10 = None
        self.label_11 = None
        self.plainTextEdit_response_cookie = None
        self.plainTextEdit_response_header = None
        self.plainTextEdit_response = None
        self.tabWidget_response = None
        self.plainTextEdit_Request_Head = None
        self.verticalLayout = None
        self.verticalLayout_2 = None
        self.horizontal_Layout_4 = None
        self.horizontalLayout_5 = None

        self.verticalLayout_7 = None
        self.verticalLayout_8 = None
        self.verticalLayout_9 = None
        self.plainTextEdit_Request_Cookie = None

        self.plainTextEdit_Request_Data = None
        self.plainTextEdit_Request_URL = None
        self.pushButton_Send_request = None

        self.lineEdit_agent_IP = None

        self.comboBox_browser = None
        self.comboBox_request_library = None
        self.comboBox_request_type = None
        self.comboBox_submit_type = None

        self.pushButton_clear = None
        self.pushButton_generate_code = None
        self.checkBox_decode = None
        self.checkBox_Static_redirection = None
        self.checkBox_record = None
        self.horizontalLayout_1 = None
        self.horizontalLayout_2 = None

        self.verticalLayoutWidget = None
        self.centralwidget = None
        self.pushButton_paste_wrap = None
        self.tab = None

        self.version = version

    def construct_URL_zone(self):
        self.verticalLayout_2 = QVBoxLayout()
        self.verticalLayout_2.setObjectName(u"verticalLayout_2")
        self.label_4 = QLabel(self.verticalLayoutWidget)
        self.label_4.setObjectName(u"label_4")
        self.verticalLayout_2.addWidget(self.label_4)
        self.plainTextEdit_Request_URL = QPlainTextEdit(self.verticalLayoutWidget)
        self.plainTextEdit_Request_URL.setObjectName(u"plainTextEdit_Request_URL")
        self.plainTextEdit_Request_URL.setFixedHeight(60)
        self.verticalLayout_2.addWidget(self.plainTextEdit_Request_URL)
        self.verticalLayout.addLayout(self.verticalLayout_2)

    def construct_Data_zone(self):
        self.verticalLayout_7 = QVBoxLayout()
        self.horizontal_Layout_4 = QHBoxLayout()
        self.horizontal_Layout_4.setObjectName(u"horizontal_Layout_4")
        self.label_9 = QLabel(self.verticalLayoutWidget)
        self.label_9.setObjectName(u"label_9")
        self.horizontal_Layout_4.addWidget(self.label_9)

        self.comboBox_submit_type = Custom_Arrow_ComboBox(self.verticalLayoutWidget)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHeightForWidth(self.comboBox_submit_type.sizePolicy().hasHeightForWidth())
        self.comboBox_submit_type.setSizePolicy(sizePolicy2)
        self.comboBox_submit_type.setFixedHeight(24)
        self.comboBox_submit_type.setMaxVisibleItems(5)
        self.comboBox_submit_type.setObjectName(u"comboBox_submit_type")

        self.horizontal_Layout_4.addWidget(self.comboBox_submit_type)

        self.comboBox_respond_type = Custom_Arrow_ComboBox(self.verticalLayoutWidget)
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHeightForWidth(self.comboBox_respond_type.sizePolicy().hasHeightForWidth())
        self.comboBox_respond_type.setSizePolicy(sizePolicy2)
        self.comboBox_respond_type.setFixedHeight(24)
        self.comboBox_respond_type.setMaxVisibleItems(5)
        self.comboBox_respond_type.setObjectName(u"comboBox_respond_type")

        self.horizontal_Layout_4.addWidget(self.comboBox_respond_type)

        self.verticalLayout_7.setObjectName(u"verticalLayout_7")

        self.verticalLayout_7.addLayout(self.horizontal_Layout_4)

        self.plainTextEdit_Request_Data = QPlainTextEdit(self.verticalLayoutWidget)
        self.plainTextEdit_Request_Data.setObjectName(u"plainTextEdit_Request_Data")
        self.plainTextEdit_Request_Data.setFixedHeight(120)
        self.verticalLayout_7.addWidget(self.plainTextEdit_Request_Data)
        self.verticalLayout.addLayout(self.verticalLayout_7)

    def setupUi(self, MainWindow):
        if not MainWindow.objectName():
            MainWindow.setObjectName(u"MainWindow")
        MainWindow.setFixedSize(810, 750)
        # 全局样式（美化）
        MainWindow.setStyleSheet("""
/* 全局字体 + 背景 */
QWidget {
    font-family: "Microsoft YaHei";
    font-size: 12px;
    color: palette(windowText);
    background: palette(window);
}

/* 输入框 */
QPlainTextEdit, QLineEdit {
    border: 1px solid #bfc9d4;
    border-radius: 6px;
    padding: 4px;
    background: palette(base);
    color: palette(text);
}
QPlainTextEdit:focus, QLineEdit:focus {
    border: 1px solid #4a90e2;
    background: palette(base);
}

/* 标签 */
QLabel {
    font-weight: bold;
    color: palette(windowText);
    background: palette(window);
}

/* 复选框 */
QCheckBox {
    spacing: 6px;
    font-weight: 500;
    background: palette(window);
    color: palette(windowText);
}

/* 标签页 */
QTabWidget::pane {
    border: 1px solid #c0c0c0;
    border-radius: 6px;
    background: palette(window);
}
QTabBar::tab {
    background: #e0e6ed;
    color: #333333;
    padding: 6px 14px;
    border-top-left-radius: 6px;
    border-top-right-radius: 6px;
    margin-right: 2px;
}
QTabBar::tab:selected {
    background: #4a90e2;
    color: white;
    font-weight: bold;
}
QTabBar::tab:hover {
    background: #b3cde6;
}

/* 按钮 */
QPushButton {
    background-color: #4a90e2;
    color: white;
    border: none;
    padding: 6px 14px;
    border-radius: 6px;
}
QPushButton:hover {
    background-color: #357ABD;
}
QPushButton:pressed {
    background-color: #2d5f91;
}

/* 下拉框 */
QComboBox {
    border: 1px solid #bfc9d4;
    padding: 4px 24px 4px 6px;
    background: palette(base);
    color: palette(text);
}
QComboBox:focus {
    border: 1px solid #4a90e2;
    background: palette(base);
}
QComboBox::drop-down {
    subcontrol-origin: padding;
    subcontrol-position: top right;
    width: 28px;
    border-left: 1px solid #bfc9d4;
    background: palette(base);
}
QComboBox::down-arrow {
}

QComboBox:disabled {
    background: #f0f0f0;
    color: #a0a0a0;
    border: 1px solid #d0d0d0;
}
QComboBox:disabled::drop-down {
    border-left: 1px solid #d0d0d0;
}
""")

        self.centralwidget = QWidget(MainWindow)
        self.centralwidget.setObjectName(u"centralwidget")
        self.verticalLayoutWidget = QWidget(self.centralwidget)
        self.verticalLayoutWidget.setObjectName(u"verticalLayoutWidget")
        self.verticalLayoutWidget.setGeometry(QRect(10, 10, 790, 470))
        self.verticalLayout = QVBoxLayout(self.verticalLayoutWidget)
        self.verticalLayout.setObjectName(u"verticalLayout")
        self.verticalLayout.setContentsMargins(0, 0, 0, 0)

        # 第一行（复选框 + 按钮）
        self.horizontalLayout_1 = QHBoxLayout()
        self.horizontalLayout_1.setObjectName(u"horizontalLayout")
        self.checkBox_record = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_record.setObjectName(u"checkBox_record")
        sizePolicy = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Minimum)
        sizePolicy.setHeightForWidth(self.checkBox_record.sizePolicy().hasHeightForWidth())
        self.checkBox_record.setSizePolicy(sizePolicy)
        self.horizontalLayout_1.addWidget(self.checkBox_record)

        self.checkBox_Static_redirection = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_Static_redirection.setObjectName(u"checkBox_Static_redirection")
        sizePolicy.setHeightForWidth(self.checkBox_Static_redirection.sizePolicy().hasHeightForWidth())
        self.checkBox_Static_redirection.setSizePolicy(sizePolicy)
        self.horizontalLayout_1.addWidget(self.checkBox_Static_redirection)

        self.checkBox_decode = QCheckBox(self.verticalLayoutWidget)
        self.checkBox_decode.setObjectName(u"checkBox_decode")
        sizePolicy.setHeightForWidth(self.checkBox_decode.sizePolicy().hasHeightForWidth())
        self.checkBox_decode.setSizePolicy(sizePolicy)
        self.horizontalLayout_1.addWidget(self.checkBox_decode)

        self.pushButton_generate_code = QPushButton(self.verticalLayoutWidget)
        self.pushButton_generate_code.setObjectName(u"pushButton_generate_code")
        sizePolicy1 = QSizePolicy(QSizePolicy.Policy.Minimum, QSizePolicy.Policy.Fixed)
        sizePolicy1.setHeightForWidth(self.pushButton_generate_code.sizePolicy().hasHeightForWidth())
        self.pushButton_generate_code.setSizePolicy(sizePolicy1)
        self.pushButton_generate_code.setMinimumSize(QSize(0, 30))
        self.horizontalLayout_1.addWidget(self.pushButton_generate_code)

        self.pushButton_paste_wrap = QPushButton(self.verticalLayoutWidget)
        self.pushButton_paste_wrap.setObjectName(u"pushButton_paste_wrap")
        sizePolicy1.setHeightForWidth(self.pushButton_paste_wrap.sizePolicy().hasHeightForWidth())
        self.pushButton_paste_wrap.setSizePolicy(sizePolicy1)
        self.pushButton_paste_wrap.setMinimumSize(QSize(0, 31))
        self.horizontalLayout_1.addWidget(self.pushButton_paste_wrap)

        self.pushButton_clear = QPushButton(self.verticalLayoutWidget)
        self.pushButton_clear.setObjectName(u"pushButton_clear")
        sizePolicy1.setHeightForWidth(self.pushButton_clear.sizePolicy().hasHeightForWidth())
        self.pushButton_clear.setSizePolicy(sizePolicy1)
        self.pushButton_clear.setMinimumSize(QSize(0, 31))
        self.horizontalLayout_1.addWidget(self.pushButton_clear)

        self.verticalLayout.addLayout(self.horizontalLayout_1)

        # 第二行（请求类型、库、代理等）
        self.horizontalLayout_2 = QHBoxLayout()
        self.horizontalLayout_2.setObjectName(u"horizontalLayout_2")
        self.label = QLabel(self.verticalLayoutWidget)
        self.label.setObjectName(u"label")
        sizePolicy.setHeightForWidth(self.label.sizePolicy().hasHeightForWidth())
        self.label.setSizePolicy(sizePolicy)
        self.label.setFixedHeight(24)
        self.horizontalLayout_2.addWidget(self.label)

        self.comboBox_request_type = Custom_Arrow_ComboBox(self.verticalLayoutWidget)

        self.comboBox_request_type.setObjectName(u"comboBox_request_type")
        sizePolicy2 = QSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
        sizePolicy2.setHeightForWidth(self.comboBox_request_type.sizePolicy().hasHeightForWidth())
        self.comboBox_request_type.setSizePolicy(sizePolicy2)
        self.comboBox_request_type.setFixedHeight(24)
        self.comboBox_request_type.setMaxVisibleItems(5)  # 最多显示 5 条，下方出现滚动条

        self.horizontalLayout_2.addWidget(self.comboBox_request_type)

        self.label_2 = QLabel(self.verticalLayoutWidget)
        self.label_2.setObjectName(u"label_2")
        sizePolicy.setHeightForWidth(self.label_2.sizePolicy().hasHeightForWidth())
        self.label_2.setSizePolicy(sizePolicy)
        self.label_2.setFixedHeight(24)
        self.horizontalLayout_2.addWidget(self.label_2)

        self.comboBox_request_library = Custom_Arrow_ComboBox(self.verticalLayoutWidget)

        self.comboBox_request_library.setObjectName(u"comboBox_request_library")
        sizePolicy2.setHeightForWidth(self.comboBox_request_library.sizePolicy().hasHeightForWidth())
        self.comboBox_request_library.setSizePolicy(sizePolicy2)
        self.comboBox_request_library.setFixedHeight(24)
        self.comboBox_request_library.setMaxVisibleItems(5)  # 最多显示 5 条，下方出现滚动条

        self.horizontalLayout_2.addWidget(self.comboBox_request_library)

        self.label_5 = QLabel(self.verticalLayoutWidget)
        self.label_5.setObjectName(u"label_5")
        sizePolicy.setHeightForWidth(self.label_5.sizePolicy().hasHeightForWidth())
        self.label_5.setSizePolicy(sizePolicy)
        self.label_5.setFixedHeight(24)
        self.horizontalLayout_2.addWidget(self.label_5)

        self.comboBox_browser = Custom_Arrow_ComboBox(self.verticalLayoutWidget)
        self.comboBox_browser.setObjectName(u"comboBox_browser")
        sizePolicy2.setHeightForWidth(self.comboBox_browser.sizePolicy().hasHeightForWidth())
        self.comboBox_browser.setSizePolicy(sizePolicy2)
        self.comboBox_browser.setFixedHeight(24)
        self.comboBox_browser.setMaxVisibleItems(5)  # 最多显示 5 条，下方出现滚动条

        self.horizontalLayout_2.addWidget(self.comboBox_browser)

        self.label_3 = QLabel(self.verticalLayoutWidget)
        self.label_3.setObjectName(u"label_3")
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setFixedHeight(24)
        self.horizontalLayout_2.addWidget(self.label_3)

        self.lineEdit_agent_IP = QLineEdit(self.verticalLayoutWidget)
        self.lineEdit_agent_IP.setObjectName(u"lineEdit_agent_IP")
        sizePolicy1.setHeightForWidth(self.lineEdit_agent_IP.sizePolicy().hasHeightForWidth())
        self.lineEdit_agent_IP.setSizePolicy(sizePolicy1)
        self.lineEdit_agent_IP.setMinimumSize(QSize(0, 24))
        self.horizontalLayout_2.addWidget(self.lineEdit_agent_IP)

        self.pushButton_Send_request = QPushButton(self.verticalLayoutWidget)
        self.pushButton_Send_request.setObjectName(u"pushButton_Send_request")
        sizePolicy2.setHeightForWidth(self.pushButton_Send_request.sizePolicy().hasHeightForWidth())
        self.pushButton_Send_request.setSizePolicy(sizePolicy2)
        self.pushButton_Send_request.setMinimumSize(QSize(0, 31))
        self.horizontalLayout_2.addWidget(self.pushButton_Send_request)

        self.verticalLayout.addLayout(self.horizontalLayout_2)

        # URL 区域
        self.construct_URL_zone()

        # Data 区域
        self.construct_Data_zone()

        # Cookie / Head 区域
        self.horizontalLayout_5 = QHBoxLayout()
        self.horizontalLayout_5.setObjectName(u"horizontalLayout_5")
        self.verticalLayout_8 = QVBoxLayout()
        self.verticalLayout_8.setObjectName(u"verticalLayout_8")
        self.label_10 = QLabel(self.verticalLayoutWidget)
        self.label_10.setObjectName(u"label_10")
        self.verticalLayout_8.addWidget(self.label_10)
        self.plainTextEdit_Request_Cookie = QPlainTextEdit(self.verticalLayoutWidget)
        self.plainTextEdit_Request_Cookie.setObjectName(u"plainTextEdit_Request_Cookie")
        self.verticalLayout_8.addWidget(self.plainTextEdit_Request_Cookie)
        self.horizontalLayout_5.addLayout(self.verticalLayout_8)

        self.verticalLayout_9 = QVBoxLayout()
        self.verticalLayout_9.setObjectName(u"verticalLayout_9")
        self.label_11 = QLabel(self.verticalLayoutWidget)
        self.label_11.setObjectName(u"label_11")
        self.verticalLayout_9.addWidget(self.label_11)
        self.plainTextEdit_Request_Head = QPlainTextEdit(self.verticalLayoutWidget)
        self.plainTextEdit_Request_Head.setObjectName(u"plainTextEdit_Request_Head")
        self.verticalLayout_9.addWidget(self.plainTextEdit_Request_Head)
        self.horizontalLayout_5.addLayout(self.verticalLayout_9)
        self.verticalLayout.addLayout(self.horizontalLayout_5)

        # 响应 Tab
        self.tabWidget_response = QTabWidget(self.centralwidget)
        self.tabWidget_response.setObjectName(u"tabWidget_response")
        self.tabWidget_response.setGeometry(QRect(10, 490, 792, 230))

        # 响应正文
        self.tab = QWidget()
        self.tab.setObjectName(u"tab")


        self.plainTextEdit_response = QPlainTextEdit(self.tab)
        self.plainTextEdit_response.setObjectName(u"plainTextEdit_response")
        self.plainTextEdit_response.setGeometry(QRect(6, 5, 777, 192))

        self.tabWidget_response.addTab(self.tab, "")

        # 协议头
        self.tab_2 = QWidget()
        self.tab_2.setObjectName(u"tab_2")
        self.plainTextEdit_response_header = QPlainTextEdit(self.tab_2)
        self.plainTextEdit_response_header.setObjectName(u"plainTextEdit_response_header")
        self.plainTextEdit_response_header.setGeometry(QRect(6, 5, 777, 192))
        self.tabWidget_response.addTab(self.tab_2, "")

        # cookie
        self.tab_3 = QWidget()
        self.tab_3.setObjectName(u"tab_3")
        self.plainTextEdit_response_cookie = QPlainTextEdit(self.tab_3)
        self.plainTextEdit_response_cookie.setObjectName(u"plainTextEdit_response_cookie")
        self.plainTextEdit_response_cookie.setGeometry(QRect(6, 5, 777, 192))
        self.tabWidget_response.addTab(self.tab_3, "")

        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        self.tabWidget_response.setCurrentIndex(0)
        QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        MainWindow.setWindowTitle(
            QCoreApplication.translate("MainWindow", f"API调试工具 - 作者: 苍 | 版本:{self.version}", None))
        self.checkBox_record.setText(QCoreApplication.translate("MainWindow", u"\u8bb0\u5f55\u65e5\u5fd7", None))
        self.checkBox_Static_redirection.setText(
            QCoreApplication.translate("MainWindow", u"\u7981\u6b62\u91cd\u5b9a\u5411", None))
        self.checkBox_decode.setText(QCoreApplication.translate("MainWindow", u"\u81ea\u52a8\u89e3\u7801", None))
        self.pushButton_generate_code.setText(
            QCoreApplication.translate("MainWindow", u"\u751f\u6210py\u4ee3\u7801", None))
        self.pushButton_paste_wrap.setText(
            QCoreApplication.translate("MainWindow", u"\u7c98\u8d34\u534f\u8bae\u5305", None))
        self.pushButton_clear.setText(QCoreApplication.translate("MainWindow", u"\u6e05\u7a7a", None))
        self.label.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u6c42\u7c7b\u578b", None))

        self.comboBox_request_type.addItem(QCoreApplication.translate("MainWindow", u"GET", None))
        self.comboBox_request_type.addItem(QCoreApplication.translate("MainWindow", u"POST", None))
        self.comboBox_request_type.addItem(QCoreApplication.translate("MainWindow", u"PUT", None))
        self.comboBox_request_type.addItem(QCoreApplication.translate("MainWindow", u"DELETE", None))

        self.comboBox_submit_type.addItem(QCoreApplication.translate("MainWindow", u"String提交", None))
        self.comboBox_submit_type.addItem(QCoreApplication.translate("MainWindow", u"Bytes提交(Hex or Base64)", None))
        self.comboBox_respond_type.addItem(QCoreApplication.translate("MainWindow", u"String返回", None))
        self.comboBox_respond_type.addItem(QCoreApplication.translate("MainWindow", u"Base64返回", None))
        self.comboBox_respond_type.addItem(QCoreApplication.translate("MainWindow", u"Bytes返回", None))

        self.label_2.setText(QCoreApplication.translate("MainWindow", u"\u8bbf\u95ee\u5e93", None))

        self.comboBox_request_library.addItem(QCoreApplication.translate("MainWindow", u"requests", None))
        self.comboBox_request_library.addItem(QCoreApplication.translate("MainWindow", u"curl_cffi", None))
        #  self.comboBox_request_library.setItemText(2, QCoreApplication.translate("MainWindow", u"urllib3", None))
        #  self.comboBox_request_library.setItemText(3, QCoreApplication.translate("MainWindow", u"httpx", None))
        #  self.comboBox_request_library.setItemText(4, QCoreApplication.translate("MainWindow", u"aiohttp", None))

        self.label_5.setText(QCoreApplication.translate("MainWindow", u"\u6307\u7eb9", None))
        self.label_3.setText(QCoreApplication.translate("MainWindow", u"\u4ee3\u7406IP", None))
        self.pushButton_Send_request.setText(QCoreApplication.translate("MainWindow", u"\u53d1\u9001\u8bf7\u6c42", None))
        self.label_4.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u6c42URL", None))
        self.plainTextEdit_Request_URL.setPlainText("")
        self.label_9.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u6c42Data", None))
        self.plainTextEdit_Request_Data.setPlainText("")
        self.label_10.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u6c42Cookie", None))
        self.plainTextEdit_Request_Cookie.setPlainText("")
        self.label_11.setText(QCoreApplication.translate("MainWindow", u"\u8bf7\u6c42Head", None))
        self.plainTextEdit_Request_Head.setPlainText("")
        self.plainTextEdit_response.setPlainText("")
        self.tabWidget_response.setTabText(self.tabWidget_response.indexOf(self.tab), QCoreApplication.translate("MainWindow", u"响应正文", None))
        self.plainTextEdit_response_header.setPlainText("")
        self.tabWidget_response.setTabText(self.tabWidget_response.indexOf(self.tab_2), QCoreApplication.translate("MainWindow", u"协议头", None))
        self.plainTextEdit_response_cookie.setPlainText("")
        self.tabWidget_response.setTabText(self.tabWidget_response.indexOf(self.tab_3), QCoreApplication.translate("MainWindow", u"cookie", None))

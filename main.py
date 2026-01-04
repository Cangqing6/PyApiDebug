import os
import sys
import pyperclip

from PySide6 import QtCore
from PySide6.QtCore import QTime, QTimer, QThread, QSettings
from PySide6.QtGui import QIcon, QAction, QPalette, QColor, QShortcut, QTextCursor, QKeySequence, QTextDocument
from PySide6.QtWidgets import (QApplication, QMainWindow, QStatusBar, QLabel, QMessageBox, QSystemTrayIcon, QMenu)
from SendSelector import Send_QtWorker
from win_ui import Ui_MainWindow
from HttpAnalyzer import parse_http_request, get_head, get_cookie, decodeDataStr, get_head_x, get_cookie_x
from Toast_ import Toast
from NetworkRequestExample import get_Example_curl_cffi, get_Example_requests
from SearchDialog import Ui_Dialog


class SearchDialog(QMainWindow):
    def __init__(self, parent=None, text_edit=None):
        super().__init__(parent)
        self.text_edit = text_edit
        self.Dialog = Ui_Dialog()
        self.Dialog.setupUi(self)
        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)
        self.Dialog.Button_next.clicked.connect(lambda: self.search(forward=self.Dialog.checkBox_ReverseSeek.isChecked()))
        self.Dialog.Button_count.clicked.connect(lambda: self.count_matches(self.Dialog.checkBox_Case.isChecked()))
        self.Dialog.lineEdit_FindTarget.returnPressed.connect(lambda: self.search(forward=True))

    def search(self, forward=True):
        self.status_bar.showMessage(f'')
        query = self.Dialog.lineEdit_FindTarget.text()
        if (not self.text_edit) or (not query):
            return

        flags = QTextDocument.FindFlags()
        if forward:
            flags |= QTextDocument.FindBackward
        if self.Dialog.checkBox_Case.isChecked():
            flags |= QTextDocument.FindCaseSensitively
        found = self.text_edit.find(query, flags)
        if not found:
            # 循环搜索
            cursor = self.text_edit.textCursor()
            if not forward:
                cursor.movePosition(QTextCursor.Start)
            else:
                cursor.movePosition(QTextCursor.End)
            self.text_edit.setTextCursor(cursor)
            # 第二次查找
            found = self.text_edit.find(query, flags)
            if not found:
                # 彻底找不到 → 只有这里才提示
                self.status_bar.showMessage(f'查找: 无法找到文本 "{query}"')

    def count_matches(self, case_sensitive=False):
        self.status_bar.showMessage(f'')
        query = self.Dialog.lineEdit_FindTarget.text()
        if not query:
            return 0
        doc = self.text_edit.document()
        flags = QTextDocument.FindFlags()
        if case_sensitive:
            flags |= QTextDocument.FindCaseSensitively
        count = 0
        cursor = QTextCursor(doc)
        cursor.movePosition(QTextCursor.Start)
        # 循环查找
        while True:
            cursor = doc.find(query, cursor, flags)
            if cursor.isNull():
                break
            count += 1
        self.status_bar.showMessage(f"计数: {count}次匹配")
        return count


class MainWindow(QMainWindow):
    def __init__(self, version):
        super().__init__()
        self.tray = None
        self.request_finger = None
        self.request_library = None
        self.request_type = None
        self.agent_IP = None
        self.IP_ = None
        self.proxies = None
        self.Data = None
        self.Cookie = None
        self.Head = None
        self.URL = None
        self.Send_Worker = None
        self.Send_thread = None

        # 初始化系统托盘
        self.init_tray()

        self.settings = QSettings(resource_path("assets/config.ini"), QSettings.IniFormat)
        self.ui = Ui_MainWindow(version)
        self.ui.setupUi(self)

        self.ui.comboBox_browser.setEnabled(False)

        redirection = self.settings.value("select/redirection", False, bool)
        record = self.settings.value("select/record", False, bool)
        decode = self.settings.value("select/decode", False, bool)

        agent_IP = self.settings.value("request/agent_IP", "", str)
        URL = self.settings.value("request/url", "", str)
        Data = self.settings.value("request/Data", "", str)
        Cookie = self.settings.value("request/Cookie", "", str)
        Head = self.settings.value("request/Head", "", str)

        browser = self.settings.value("select/browser", 0, int)
        library = self.settings.value("select/library", 0, int)
        submit = self.settings.value("select/submit", 0, int)
        Type = self.settings.value("select/type", 0, int)
        respond_type = self.settings.value("select/reqtype", 0, int)

        if library == 1:
            self.ui.comboBox_browser.setEnabled(True)
        else:
            self.ui.comboBox_browser.setEnabled(False)

        self.ui.comboBox_browser.setCurrentIndex(browser)
        self.ui.comboBox_request_library.setCurrentIndex(library)
        self.ui.comboBox_submit_type.setCurrentIndex(submit)
        self.ui.comboBox_request_type.setCurrentIndex(Type)
        self.ui.comboBox_respond_type.setCurrentIndex(respond_type)

        self.ui.checkBox_Static_redirection.setChecked(redirection)
        self.ui.checkBox_record.setChecked(record)
        self.ui.checkBox_decode.setChecked(decode)
        self.ui.lineEdit_agent_IP.setText(agent_IP)
        self.ui.plainTextEdit_Request_URL.setPlainText(URL)
        self.ui.plainTextEdit_Request_Data.setPlainText(Data)
        self.ui.plainTextEdit_Request_Cookie.setPlainText(Cookie)
        self.ui.plainTextEdit_Request_Head.setPlainText(Head)

        # 逐个添加
        for fingerprint in fingerprint_array:
            self.ui.comboBox_browser.addItem(fingerprint)

        # 显式指定允许的按钮
        self.setWindowFlags(QtCore.Qt.Window | QtCore.Qt.WindowMinimizeButtonHint | QtCore.Qt.WindowCloseButtonHint)

        # 连接按钮信号与槽
        self.ui.pushButton_clear.clicked.connect(self.on_clear)
        self.ui.pushButton_paste_wrap.clicked.connect(self.on_paste_wrap)
        self.ui.pushButton_Send_request.clicked.connect(self.on_Send_request)
        self.ui.pushButton_generate_code.clicked.connect(self.on_generate_code)

        # 连接组合框信号与槽
        self.ui.comboBox_request_type.currentTextChanged.connect(self.on_text_changed)
        self.ui.comboBox_request_library.currentTextChanged.connect(self.on_use_import)
        self.ui.comboBox_submit_type.currentTextChanged.connect(self.on_submit_type)
        self.ui.comboBox_respond_type.currentTextChanged.connect(self.on_respond_type)

        # 创建状态栏
        self.status_bar = QStatusBar()
        self.setStatusBar(self.status_bar)

        # 最左边的永久部件
        app_name_label = QLabel("API调试工具 ")
        app_name_label.setStyleSheet("font-weight: bold; color: #2c3e50;")
        self.status_bar.insertPermanentWidget(0, app_name_label)

        # 右侧的永久部件（标准方式）
        self.time_label = QLabel()
        self.status_bar.addPermanentWidget(self.time_label)

        # 更新时间
        self.update_time()
        timer = QTimer(self)
        timer.timeout.connect(self.update_time)
        timer.start(1000)
        self.tray.showMessage("提示", "部分功能尚未完善,请等待作者更新", QSystemTrayIcon.Information, 3000)

        # 搜索弹窗
        self.search_dialog = SearchDialog(self, self.ui.plainTextEdit_response)
        # 快捷键 Ctrl+F 弹出搜索框
        self.shortcut = QShortcut(QKeySequence("Ctrl+F"), self.ui.plainTextEdit_response)
        self.shortcut.activated.connect(self.show_search_dialog)

    def show_search_dialog(self):
        self.search_dialog.show()
        self.search_dialog.raise_()  # 提到最前面
        self.search_dialog.Dialog.lineEdit_FindTarget.setFocus()

    # 弹窗
    def show_toast(self, message, toast_type="info"):
        """显示Toast通知
        参数:
            message: 要显示的消息
            toast_type: 通知类型 (success, warning, error, info)
        """
        toast = Toast(message, self)

        # 根据类型设置不同样式
        if toast_type == "success":
            toast.setStyleSheet("""
                QWidget {
                    background-color: #28a745;
                    color: white;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-family: 'Microsoft YaHei';
                    font-size: 14px;
                }
            """)
        elif toast_type == "warning":
            toast.setStyleSheet(
                """ QWidget { background-color: #ffc107; color: black; border-radius: 8px; padding: 12px 24px; font-family: 'Microsoft YaHei'; font-size: 14px; } """)
        elif toast_type == "error":
            toast.setStyleSheet("""
                QWidget {
                    background-color: #dc3545;
                    color: white;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-family: 'Microsoft YaHei';
                    font-size: 14px;
                }
            """)
        else:  # info
            toast.setStyleSheet("""
                QWidget {
                    background-color: #17a2b8;
                    color: white;
                    border-radius: 8px;
                    padding: 12px 24px;
                    font-family: 'Microsoft YaHei';
                    font-size: 14px;
                }
            """)

        toast.adjustSize()
        toast.show_toast()

    #  创建系统托盘图标
    def init_tray(self):
        self.tray = QSystemTrayIcon(self)
        
        # 设置图标（注意：图标文件需要存在）
        try:
            self.tray.setIcon(QIcon(resource_path("assets/icon.ico")))
        except:
            # 如果图标文件不存在，使用默认图标
            self.tray.setIcon(QIcon(QSystemTrayIcon.Information))

        # 显示托盘图标
        self.tray.show()

        # 创建右键菜单
        self.create_tray_menu()

        # 连接点击事件
        self.tray.activated.connect(self.on_tray_activated)

    #  创建菜单
    def create_tray_menu(self):
        menu = QMenu()

        # 添加菜单项
        show_action = QAction("显示主窗口", self)
        show_action.triggered.connect(self.show)
        menu.addAction(show_action)

        # 添加分隔线
        menu.addSeparator()

        # 添加退出项
        exit_action = QAction("退出程序", self)
        exit_action.triggered.connect(self.close_app)
        menu.addAction(exit_action)

        # 将菜单设置给托盘图标
        self.tray.setContextMenu(menu)

    def on_tray_activated(self, reason):
        # 处理托盘图标被点击的事件
        if reason == QSystemTrayIcon.DoubleClick:
            self.showNormal()

    # 菜单-退出程序
    def close_app(self):
        msg = QMessageBox()
        msg.setWindowTitle("提示")
        msg.setText("确定要退出程序吗?")
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.No)

        # 设置固定大小
        msg.setFixedSize(400, 200)  # 宽 400，高 200

        # 确认退出对话框
        if msg.exec() == QMessageBox.Yes:
            self.tray.hide()  # 隐藏托盘图标
            QApplication.quit()  # 退出应用

    def update_time(self):
        current_time = QTime.currentTime().toString("hh:mm:ss")
        self.time_label.setText(f"时间: {current_time}")

    def closeEvent(self, event):
        """重写关闭事件"""
        self.settings.setValue("request/agent_IP", self.ui.lineEdit_agent_IP.text())
        self.settings.setValue("request/url", self.ui.plainTextEdit_Request_URL.toPlainText())
        self.settings.setValue("request/Data", self.ui.plainTextEdit_Request_Data.toPlainText())
        self.settings.setValue("request/Cookie", self.ui.plainTextEdit_Request_Cookie.toPlainText())
        self.settings.setValue("request/Head", self.ui.plainTextEdit_Request_Head.toPlainText())
        self.settings.setValue("select/redirection", self.ui.checkBox_Static_redirection.isChecked())
        self.settings.setValue("select/record", self.ui.checkBox_record.isChecked())
        self.settings.setValue("select/decode", self.ui.checkBox_decode.isChecked())

        self.settings.setValue("select/browser", self.ui.comboBox_browser.currentIndex())
        self.settings.setValue("select/library", self.ui.comboBox_request_library.currentIndex())
        self.settings.setValue("select/submit", self.ui.comboBox_submit_type.currentIndex())
        self.settings.setValue("select/type", self.ui.comboBox_request_type.currentIndex())
        self.settings.setValue("select/reqtype", self.ui.comboBox_respond_type.currentIndex())
        print("窗口正在关闭...")
        event.accept()  # 接受关闭事件

    #  清空所有
    def on_clear(self):
        """清空所有 事件"""
        self.ui.plainTextEdit_Request_URL.setPlainText("")
        self.ui.plainTextEdit_Request_Data.setPlainText("")
        self.ui.plainTextEdit_Request_Cookie.setPlainText("")
        self.ui.plainTextEdit_Request_Head.setPlainText("")
        self.ui.plainTextEdit_response.setPlainText("")
        print("清空所有")
        self.status_bar.showMessage("清空所有")

    #  粘贴协议包
    def on_paste_wrap(self):
        """粘贴协议包 事件"""
        # 获取剪贴板内容
        clipboard_content = pyperclip.paste()
        # print("剪贴板内容:")
        # print(clipboard_content)
        self.parsed = parse_http_request(clipboard_content)

        if self.parsed["method"]:
            self.ui.plainTextEdit_Request_URL.setPlainText(self.parsed['url'])
            if self.parsed['method'].upper() == 'GET':
                Type = 0
            if self.parsed['method'].upper() == 'POST':
                Type = 1

            self.ui.comboBox_request_type.setCurrentIndex(Type) # 通过文本设置
            self.ui.plainTextEdit_Request_Head.setPlainText(self.parsed['headers'])
            self.ui.plainTextEdit_Request_Cookie.setPlainText(self.parsed['cookies'])
            self.ui.plainTextEdit_Request_Data.setPlainText(self.parsed['data'])
            self.show_toast(f"解析请求包成功, 可以发送请求了!", "success")
            self.status_bar.showMessage(f"提示:       解析请求包成功, 可以发送请求了!")
        else:
            self.show_toast(f"解析请求包失败, 要不你手动粘贴一下...", "warning")
            self.status_bar.showMessage(f"提示:       解析请求包失败, 要不你手动粘贴一下")

    def on_use_import(self, text):
        if self.ui.comboBox_request_library.currentIndex() == 1:
            self.ui.comboBox_browser.setEnabled(True)
        else:
            self.ui.comboBox_browser.setEnabled(False)

    def on_text_changed(self, text):
        print(f"选中了文本: {text}")

    def on_submit_type(self, text):
        print(f"选中了文本: {text}")
    def on_respond_type(self, text):
        print(f"选中了文本: {text}")
    #  进行发包请求
    def on_Send_request(self):
        self.URL = self.ui.plainTextEdit_Request_URL.toPlainText()
        self.Head = get_head(self.ui.plainTextEdit_Request_Head.toPlainText())
        self.Cookie = get_cookie(self.ui.plainTextEdit_Request_Cookie.toPlainText())
        self.Data = self.ui.plainTextEdit_Request_Data.toPlainText()

        self.request_type = self.ui.comboBox_request_type.currentText()  # 请求的模型
        self.request_library = self.ui.comboBox_request_library.currentText()  # 请求的库
        self.submit_type = self.ui.comboBox_submit_type.currentIndex()  # 请求的数据类型
        self.respond_type = self.ui.comboBox_respond_type.currentIndex()  # 返回的数据类型
        self.request_finger = self.ui.comboBox_browser.currentText()  # 请求的指纹
        self.allow_redirects = self.ui.checkBox_Static_redirection.isChecked()  # 是否重定向
        if self.submit_type == 1:
            self.Data = decodeDataStr(self.Data)

        if not self.URL:
            # 显示临时消息
            self.status_bar.showMessage(f"提示:       请输入URL")
            self.show_toast(f"请输入URL!", "warning")
            return
        # 获取全部文本内容（返回字符串）
        self.agent_IP = self.ui.lineEdit_agent_IP.text()
        if self.agent_IP:
            self.IP_ = f"http://{self.agent_IP}"
            self.proxies = {"http": self.IP_, "https": self.IP_}
        else:
            self.proxies = {}
        try:
            if self.Send_thread and self.Send_thread.isRunning():
                self.show_toast(f"请等待上一个请求完成后再试!", "warning")
                print("请等待当前线程完成")
                return
            self.Send_Worker = Send_QtWorker(self.request_library, self.request_type, self.respond_type, self.URL, self.Data, self.Head, self.Cookie, self.proxies, self.request_finger, not self.allow_redirects)
            # 为每个信号连接到对应的文本编辑器
            self.Send_Worker.plainTextEdit_response.connect(self.ui.plainTextEdit_response.setPlainText)
            self.Send_Worker.plainTextEdit_response_header.connect(self.ui.plainTextEdit_response_header.setPlainText)
            self.Send_Worker.plainTextEdit_response_cookie.connect(self.ui.plainTextEdit_response_cookie.setPlainText)
            self.Send_Worker.status_bar.connect(self.status_bar.showMessage)
            self.Send_Worker.show_toast.connect(self.show_toast)
            # 连接worker的finished信号到清理函数
            self.Send_Worker.finished.connect(self.cleanup_send_thread)
            # 创建QThread线程对象
            self.Send_thread = QThread()
            self.Send_Worker.moveToThread(self.Send_thread)
            self.Send_thread.started.connect(self.Send_Worker.run)
            # 启动线程
            self.Send_thread.start()
        except Exception as e:
            self.ui.plainTextEdit_response.setPlainText(f"请求异常:{type(e).__name__}")

    # 清理槽函数
    def cleanup_send_thread(self):
        """清理工作线程和QThread对象"""
        if self.Send_thread.isRunning():
            self.Send_thread.quit()  # 温和地请求线程退出:cite[1]:cite[6]:cite[10]
            self.Send_thread.wait()  # 等待线程真正结束，可设置超时如wait(1000)表示等待1秒:cite[1]:cite[8]

        # 安全地销毁对象:cite[1]:cite[4]:cite[10]
        self.Send_Worker.deleteLater()
        self.Send_thread.deleteLater()

        # 可选：将引用设为None，避免重复使用
        self.Send_Worker = None
        self.Send_thread = None

        print("线程清理完毕。")

    #  生成代码
    def on_generate_code(self):
        URL = self.ui.plainTextEdit_Request_URL.toPlainText()
        Head = get_head(self.ui.plainTextEdit_Request_Head.toPlainText())
        Cookie = get_cookie(self.ui.plainTextEdit_Request_Cookie.toPlainText())

        submit_type = self.ui.comboBox_submit_type.currentIndex()
        Data = self.ui.plainTextEdit_Request_Data.toPlainText()  # 请求的数据
        if submit_type == 1:
            Data = decodeDataStr(Data)
        request_type = self.ui.comboBox_request_type.currentText()  # 当前选中项的文本
        request_library = self.ui.comboBox_request_library.currentText()  # 当前选中项的文本
        allow_redirects = self.ui.checkBox_Static_redirection.isChecked()  # 是否重定向

        agent_IP = self.ui.lineEdit_agent_IP.text()
        if not URL:
            # 显示临时消息
            self.status_bar.showMessage(f"提示:       请输入URL")
            self.show_toast(f"请输入URL!", "warning")
            return

        if agent_IP:
            IP_ = f"http://{agent_IP}"
            proxies = {"http": IP_, "https": IP_}
        else:
            proxies = {}
        if request_library == 'curl_cffi':
            code_ = get_Example_curl_cffi(URL, request_type, Data, Head, Cookie, proxies, not allow_redirects)
        elif request_library == 'requests':
            code_ = get_Example_requests(URL, request_type, Data, Head, Cookie, proxies, not allow_redirects)
        else:
            code_ = ""
            self.show_toast(f"暂时无法使用 {request_library} 库", "warning")

        pyperclip.copy(code_)  # 写入内容到剪切板
        self.show_toast(f"已复制代码,快去粘贴使用吧!", "success")
        self.status_bar.showMessage(f"提示:       已复制代码,快去粘贴使用吧!")


def resource_path(relative_path):
    """ 获取打包后资源的正确路径 """
    if hasattr(sys, '_MEIPASS'):
        return os.path.join(sys._MEIPASS, relative_path)
    return os.path.join(os.path.abspath("."), relative_path)


if __name__ == "__main__":
    fingerprint_array = ["chrome99", "chrome100", "chrome101", "chrome104", "chrome107", "chrome110", "chrome116",
                         "chrome119", "chrome120", "edge99", "edge101"]  # 模拟指纹
    version_app = "1.3.0"
    app = QApplication(sys.argv)
    # 使用 Fusion 风格，便于自定义 palette
    app.setStyle("Fusion")
    # 创建浅色 palette
    light_palette = QPalette()
    light_palette.setColor(QPalette.Window, QColor("#ffffff"))  # 窗口背景
    light_palette.setColor(QPalette.WindowText, QColor("#333333"))  # 窗口文字
    light_palette.setColor(QPalette.Base, QColor("#ffffff"))  # 输入框背景
    light_palette.setColor(QPalette.AlternateBase, QColor("#f0f0f0"))  # 备用背景
    light_palette.setColor(QPalette.Text, QColor("#333333"))  # 输入文字
    light_palette.setColor(QPalette.Button, QColor("#4a90e2"))  # 按钮背景
    light_palette.setColor(QPalette.ButtonText, QColor("#ffffff"))  # 按钮文字
    light_palette.setColor(QPalette.Highlight, QColor("#4a90e2"))  # 选中高亮
    light_palette.setColor(QPalette.HighlightedText, QColor("#ffffff"))  # 高亮文字

    app.setPalette(light_palette)
    app.setQuitOnLastWindowClosed(True)  # 默认就是True，显式设置更明确
    app.setWindowIcon(QIcon(resource_path("assets/icon.ico")))  # 设置应用程序图标
    app.setApplicationName("QQ 2424226501")
    app.setApplicationDisplayName("QQ 2424226501")
    app.setOrganizationName("QQ 2424226501")
    if sys.platform == 'win32':
        try:
            from ctypes import windll
            windll.shell32.SetCurrentProcessExplicitAppUserModelID(f'API调试工具 - 作者: 苍 版本 {version_app}')
        except ImportError:
            pass

    window = MainWindow(version_app)
    window.show()
    sys.exit(app.exec())





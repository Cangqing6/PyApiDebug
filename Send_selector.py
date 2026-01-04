import base64
from PySide6.QtCore import QObject, Signal
from datetime import datetime

from curl_cffi_library import cffi_send
from curl_requests_library import requests_send
from Analyzing_HTTP import get_head_x, get_cookie_x


class Send_QtWorker(QObject):
    # 为每个文本编辑器定义独立的信号
    plainTextEdit_response = Signal(str)  # 第一个文本编辑器
    plainTextEdit_response_header = Signal(str)  # 第二个文本编辑器
    plainTextEdit_response_cookie = Signal(str)  # 第三个文本编辑器
    status_bar = Signal(str)
    show_toast = Signal(str, str)  # (message, toast_type)
    finished = Signal()  # 完成信号

    def __init__(self, library, model, respond_type, url, data, header, cookie, proxies, element, allow_redirects):
        super().__init__()
        self.response = None

        self.Times = None
        self.TimingEnds = None
        self.TimingBegins = None
        self.local_time = None
        self.formatted_time = None

        self.library = library
        self.model = model
        self.respond_type = respond_type
        self.url = url
        self.data = data
        self.header = header
        self.cookie = cookie
        self.proxies = proxies
        self.element = element
        self.allow_redirects = allow_redirects

    def run(self):
        self.TimingBegins = int(datetime.now().timestamp() * 1000)
        try:
            self.status_bar.emit(f"提示:       发送中, 请稍后...")
            self.response = select_send(self.library, self.model, self.url, self.data, self.header, self.cookie, self.proxies, self.element, self.allow_redirects)
            if self.response is not None:
                if self.respond_type == 0:
                    self.plainTextEdit_response.emit(self.response.text)
                if self.respond_type == 1:
                    self.plainTextEdit_response.emit(base64.b64encode(self.response.content).decode('utf-8'))
                if self.respond_type == 2:
                    self.plainTextEdit_response.emit(repr(self.response.content))

                self.plainTextEdit_response_header.emit(get_head_x(self.response.headers))
                self.plainTextEdit_response_cookie.emit(get_cookie_x(self.response.cookies))
            else:
                self.show_toast.emit(f"暂时无法使用 {self.library} 或 {self.model} 请求, 耐心等待作者更新", "warning")
        except Exception as e:
            self.plainTextEdit_response.emit(f"请求异常:{str(e)}")
            self.show_toast.emit(f"请求异常:{type(e).__name__}", "error")
        self.TimingEnds = int(datetime.now().timestamp() * 1000)
        self.Times = self.TimingEnds - self.TimingBegins
        self.local_time = datetime.fromtimestamp(self.TimingBegins / 1000)
        self.formatted_time = self.local_time.strftime("%Y-%m-%d %H:%M:%S")
        # 显示临时消息
        self.status_bar.emit(f"提示:       请求用时{str(self.Times)}ms      请求时间 => {self.formatted_time}")
        self.finished.emit()  # 清理当前线程


def select_send(library, model, url, data, header, cookie, proxies, element, allow_redirects):
    if library == "curl_cffi":
        response = cffi_send(url, model, data, header, cookie, proxies, element, allow_redirects)
    elif library == "requests":
        response = requests_send(url, model, data, header, cookie, proxies, element, allow_redirects)
    else:
        response = None
    return response


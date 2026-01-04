# PyApiDebug
Python request tool

## 核心功能

### 一. HTTP 请求解析与发送
  #### 1.粘贴请求包
  支持从剪贴板直接粘贴原始 HTTP 请求包。
  自动解析出请求 URL、请求方法、Headers、Cookies 和 Body 数据。
  成功解析时会提示“解析请求包成功”，失败则提示手动输入。

  #### 2.请求发送
  支持选择请求类型（GET/POST 等）和请求库（requests、curl_cffi）。
  支持设置浏览器指纹模拟请求。
  支持设置代理（Agent IP）。
  可选择是否允许重定向。
  返回结果分别显示在响应内容、响应头和响应 Cookie 编辑框中。

### 二. 代码生成
根据用户配置的请求信息，生成可直接使用的 Python 请求代码。

#### 支持两种库：
curl_cffi, requests
生成的代码会自动复制到剪贴板，并弹出提示通知。

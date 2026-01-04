import base64
import re
import json

def parse_fetch_block(js: str):
    # 抽取 fetch("url", {...})
    m = re.search(r'fetch\(\s*"(.*?)"\s*,\s*(\{.*\})\s*\)', js, re.S)
    if not m:
        return parse_http_block(js)
    result = {'method': '', 'url': m.group(1), 'headers': '', 'header': {}, 'cookies': '', 'cookie': {}, 'data': ''}
    obj_text = m.group(2)
    cleaned = obj_text
    cleaned = cleaned.replace("\n", "")  # 保留 null
    cleaned = cleaned.replace("\r", "")  # 保留 null
    cleaned = re.sub(r",\s*}", "}", cleaned)   # 去除尾部逗号
    cleaned = re.sub(r",\s*]", "]", cleaned)
    data = json.loads(cleaned)
    result['method'] = data.get("method", "GET")
    result['data'] = data.get("body")
    headers_raw = data.get("headers", {})
    # header key 小写化
    headers = {k.lower(): v for k, v in headers_raw.items()}

    for (key, value) in headers.items():
        result['header'][key] = value
        result['headers'] += f'{key}:{value}\n'

    # cookie 解析
    if "cookie" in headers:
        for kv in headers["cookie"].split(";"):
            kv = kv.strip()
            if "=" in kv:
                k, v = kv.split("=", 1)
                result['cookie'][k] = v
                result['cookies'] += f'{k}={v};'
    if not ("://" in result['url']):
        result['url'] = "http://" + result['header']['host'] + result['url']
    return result
def parse_http_block(block: str):
    block = block.strip()
    if not block:
        return None
    result = {
        'method': '',
        'url': '',
        'headers': '',
        'header': {},
        'cookies': '',
        'cookie': {},
        'data': ''
    }
    lines = block.splitlines()

    # 请求行
    req = lines[0].strip().split()
    if len(req) < 2:
        return None

    result['method'] = req[0]
    result['url'] = req[1]
    result['http_version'] = req[2] if len(req) > 2 else None

    headers = {}
    body = None
    parsing_body = False

    for line in lines[1:]:
        line = line.rstrip("\r\n")

        if line == "":
            parsing_body = True
            continue

        if not parsing_body:
            if ":" in line:
                k, v = line.split(":", 1)
                # Header-Key 大小写归一化为小写
                result['header'][k.strip().lower()] = v.strip()
                result['headers'] += f'{k.strip().lower()}:{v.strip()}\n'
        else:
            body = (body or "") + line + "\n"

    result["data"] = body.strip() if body else None

    # 归一化 cookie
    ck = headers.get("cookie")
    if ck:
        for kv in ck.split(";"):
            kv = kv.strip()
            if "=" in kv:
                k, v = kv.split("=", 1)
                result['cookie'][k] = v
                result['cookies'] += f'{k}={v};'
    if not ("://" in result['url']):
        result['url'] = "http://" + result['header']['host'] + result['url']
    return result
def remove_lines_by_keyword(text, keyword):
    lines = text.splitlines()
    new_lines = [line for line in lines if keyword not in line]
    return "\n".join(new_lines)

def parse_http_request(request_text):
    """
    解析单个HTTP请求，返回包含URL、方法、头、cookie和数据的字典
    """
    requestsText = remove_lines_by_keyword(request_text, "sec-ch-ua")
    return parse_fetch_block(requestsText)


def get_head(text):
    headers = {}
    lines = text.replace(' ', '').splitlines()  # 先按行分割
    for line in lines:
        if ':' in line:
            header_name, header_value = line.split(':', 1)  # 默认按空格/制表符分割
            headers[header_name] = header_value
    return headers


def get_cookie(text):
    cookie = {}
    lines = text.replace(' ', '').split(';')
    for line in lines:
        if '=' in line:
            key, value = line.split('=', 1)
            cookie[key.strip()] = value.strip()
    return cookie


def get_head_x(headers):
    header = ''
    for key, value in headers.items():
        header += f'{key}:{value}\n'
    return header


def get_cookie_x(cookies):
    cookie = ''
    for key, value in cookies.items():
        cookie += f'{key}={value};'
    return cookie


def decodeDataStr(string):
    try:
        return base64.b64decode(string)
    except:
        try:
            return bytes.fromhex(string)
        except:
            return -1


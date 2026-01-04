def get_Example_curl_cffi(url, model, data, header, cookie, proxies, allow_redirects):
    if isinstance(data, bytes):
        # 是bytes类型
        Data = data
    else:
        Data = f"""'{data}'"""
    code_ = f'''import random
from curl_cffi import requests

def cffi_{model.lower()}():
    url = '{url}'
    data = {Data}
    header = {header}
    cookie = {cookie}
    proxies = {proxies}
    my_array = ["chrome99", "chrome100", "chrome101", "chrome104", "chrome107", "chrome110", "chrome116", "chrome119", "chrome120", "edge99", "edge101"]
    random_element = random.choice(my_array)
    response = requests.{model.lower()}(url, headers=header, data=data, cookies=cookie, proxies=proxies, impersonate=random_element, allow_redirects={allow_redirects}, verify=False, timeout=30)
    response.encoding = 'utf-8'
    return response'''
    return code_


def get_Example_requests(url, model, data, header, cookie, proxies, allow_redirects):
    if isinstance(data, bytes):
        # 是bytes类型
        Data = data
    else:
        Data = f"""'{data}'"""
    code_ = f'''import random
import requests

def requests_{model.lower()}():
    url = '{url}'
    data = {Data}
    header = {header}
    cookie = {cookie}
    proxies = {proxies}
    response = requests.{model.lower()}(url, headers=header, data=data, cookies=cookie, proxies=proxies, allow_redirects={allow_redirects}, verify=False, timeout=30)
    response.encoding = 'utf-8'
    return response'''
    return code_

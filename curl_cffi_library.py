from curl_cffi import requests

# 创建一个方法名到函数对象的映射字典
method_map = {
    "GET": requests.get,
    "POST": requests.post,
    "PUT": requests.put,
    "DELETE": requests.delete,
}
def cffi_send(url, model, data, header, cookie, proxies, random_element, allow_redirects):
    response = method_map[model](url, headers=header, data=data, cookies=cookie, proxies=proxies, impersonate=random_element, allow_redirects=allow_redirects, verify=False, timeout=30)  # , timeout=10
    response.encoding = 'utf-8'  # 或其他已知编码
    return response


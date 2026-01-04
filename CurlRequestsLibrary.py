import requests

method_map = {
    "GET": requests.get,
    "POST": requests.post,
    "PUT": requests.put,
    "DELETE": requests.delete,
}

def requests_send(url, model, data, header, cookie, proxies, random_element, allow_redirects):
    response = method_map[model](url, headers=header, data=data, cookies=cookie, proxies=proxies, allow_redirects=allow_redirects, verify=False, timeout=30)  # , timeout=10
    response.encoding = 'utf-8'  # 或其他已知编码
    return response


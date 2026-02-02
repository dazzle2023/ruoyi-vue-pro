# OneNET 城市物联网平台 V3.0 公开接口文档

> 本文档由 DOCX 自动转换生成

---


# 公开API


## 使用说明


### 公共请求说明

API接口请求参数包括公共参数和自定义业务参数两部分。公共请求参数是调用每个API时都需要携带的请求参数, 包括服务命名空间、接口名称、版本信息。自定义业务参数由各接口定义，根据调用方法不同，需要将参数携带至请求路径或者请求体中。API接口公共参数调用如下所示：
https(http)://xxxx.com/{namespace}?action=xxxx&version=1
参数说明:


| 序号 | 参数 | 类型 | 是否必选 | 描述 |
| --- | --- | --- | --- | --- |
| 1 | namespace | string | 是 | API接口类别, 目前支持common 设备管理类 |
| 2 | action | string | 是 | API接口名称 |
| 3 | version | string | 是 | API版本号, 目前所有API接口版本均为1 |



### 公共响应说明

成功响应：
```
{
```
"requestId": "8906582E6722409AA6C40E7863B733A5",
"success": true,
"data": {
status: 1
}
}
失败响应：
```
{
```
"requestId": "8906582E6722409AA6C40E7863B733A5",
"code":  "iot.application.deviceNotFound",
"msg": "device does not exist",
"success": false
}
参数说明:


| 序号 | 参数 | 类型 | 描述 |
| --- | --- | --- | --- |
| 1 | requestId | string | 请求ID，调用API时由平台生成唯一请求标识 |
| 2 | code | string | 调用失败时，返回的错误码 |
| 3 | msg | string | 调用失败时，返回的错误信息 |
| 4 | success | boolean | 接口是否调用成功 |
| 5 | data | object | 调用成功时，返回的业务数据（接口无业务数据返回，值为null） |



## 安全鉴权

平台需要对API调用方进行资源权限校验，使用API时，需要在请求Header中携带统一的安全鉴权信息。
(1)安全鉴权机制
安全鉴权authorization由多个参数构成，每个参数均采用key = value的形式表示，并用&作为分隔符：
authorization: version=2020-05-29&res=userid%2F38055&et=1623982416&method=sha1&sign=S04GcvafYIjtAMHJthkGPevbNwE%3D
参数说明：


| 序 号 | 参数 | 类型 | 说明 | 示例 |
| --- | --- | --- | --- | --- |
| 1 | version | string | 签名算法版本 | 目前仅支持 2020-05-29 |
| 2 | res | string | 访问资源信息 | 支持主用户访问方式： 1）主用户访问res为：userid/{userid}, userid为平台用户id，参数在个人「账号信息」中查看 |
| 3 | et | string | 访问过期时间 | 10位时间戳，1537255523 表示：北京时间 2018-09-18 15:25:23 |
| 4 | method | string | 签名方法 | 目前支持md5、sha1、sha256 |
| 5 | sign | string | 签名结果字符串 | version、res、et、method参数计算生成 |


其中sign的生成算法为：
sign = base64(hmac_<method>(base64decode(accessKey), utf-8(StringForSignature)))
laccessKey为平台分配的访问密钥（用户访问权限页面查看），如果访问资源以主用户形式访问, 使用主用户的accessKey，如果访问资源以项目群组方式访问，使用群组的accessKey，且只能对群组内设备进行操作。
laccessKey参与计算前应先进行base64decode操作
l用于计算签名的字符串 StringForSignature按照et、method、resource、version的顺序，以"\n"作为分隔符进行排列，如下所示：
StringForSignature = et + "\n" + method + "\n" + res + "\n" + version
(2)参数编码
authorization中key=value的形式的value部分需要经过URL编码，需要进行编码的特殊符号如下：


| 序号 | 符号 | 编码 |
| --- | --- | --- |
| 1 | + | %2B |
| 2 | 空格 | %20 |
| 3 | / | %2F |
| 4 | ? | %3F |
| 5 | % | %25 |
| 6 | # | %23 |
| 7 | & | %26 |
| 8 | = | %3D |


(3)authorization生成示例
Ønodejs代码示例
'use strict';
const crypto = require('crypto');
/**
* authorization生成函数
*
* @param {String} method        - hash method
* @param {String} res           - resource
* @param {String} accessKey     - access key
* @param {Number} et            - effective time
* @return {String} - authorization
*/
```
function generateAuthorization(method, res, accessKey, et) {
```
const version = '2020-05-29';
const et = Math.ceil((Date.now() + et) / 1000); // token有效时间
const base64Key = Buffer.from(accessKey, 'base64'); // accessKey base64编码
const StringForSignature = et + '\n' + method + '\n' + res + '\n' + version;
const sign = encodeURIComponent(crypto.createHmac(method, base64Key).update(StringForSignature).digest('base64'));
const encodeRes = encodeURIComponent(res);
return `version=${version}&res=${encodeRes}&et=${et}&method=${method}&sign=${sign}`;
}
const method = 'sha1';
const accessKey = 'mjgvkTCYTBF6DguxMmm+aV9EkDp2CYfL5jzRTph5Th6KhU8gqZz/cBivPTA7tfY5';
const res = 'userid/130037';
const et = 365 * 24 * 3600 * 1000; // 有效时间 - 365天
const authorization = generateAuthorization(method, res, accessKey, et);
Øpython代码示例
import base64
import hmac
import time
from urllib.parse import quote
def token(user_id,access_key):
version = '2020-05-29'
res = 'userid/%s' % user_id
# 用户自定义token过期时间
et = str(int(time.time()) + 3600)
# 签名方法，支持md5、sha1、sha256
method = 'sha1'
# 对access_key进行decode
key = base64.b64decode(access_key)
# 计算sign
org = et + '\n' + method + '\n' + res + '\n' + version
sign_b = hmac.new(key=key, msg=org.encode(), digestmod=method)
sign = base64.b64encode(sign_b.digest()).decode()
# value 部分进行url编码，method/res/version值较为简单无需编码
sign = quote(sign, safe='')
res = quote(res, safe='')
# token参数拼接
token = 'version=%s&res=%s&et=%s&method=%s&sign=%s' % (version, res, et, method, sign)
return token
if __name__ == '__main__':
user_id = '37715'
access_key = 'mjgvkTCYTBF6DguxMmm+aV9EkDp2CYfL5jzRTph5Th6KhU8gqZz/cBivPTA7tfY5'
print(token(user_id,access_key))
ØJava代码示例
import javax.crypto.Mac;
import javax.crypto.spec.SecretKeySpec;
import java.io.UnsupportedEncodingException;
import java.net.URLEncoder;
import java.security.InvalidKeyException;
import java.security.NoSuchAlgorithmException;
import java.util.Base64;
public class Token {
public static String assembleToken(String version, String resourceName, String expirationTime, String signatureMethod, String accessKey)
throws UnsupportedEncodingException, NoSuchAlgorithmException, InvalidKeyException {
StringBuilder sb = new StringBuilder();
String res = URLEncoder.encode(resourceName, "UTF-8");
String sig = URLEncoder.encode(generatorSignature(version, resourceName, expirationTime, accessKey, signatureMethod), "UTF-8");
sb.append("version=")
.append(version)
.append("&res=")
.append(res)
.append("&et=")
.append(expirationTime)
.append("&method=")
.append(signatureMethod)
.append("&sign=")
.append(sig);
return sb.toString();
}
public static String generatorSignature(String version, String resourceName, String expirationTime, String accessKey, String signatureMethod)
throws NoSuchAlgorithmException, InvalidKeyException {
String encryptText = expirationTime + "\n" + signatureMethod + "\n" + resourceName + "\n" + version;
String signature;
byte[] bytes = HmacEncrypt(encryptText, accessKey, signatureMethod);
signature = Base64.getEncoder().encodeToString(bytes);
return signature;
}
public static byte[] HmacEncrypt(String data, String key, String signatureMethod)
throws NoSuchAlgorithmException, InvalidKeyException {
//根据给定的字节数组构造一个密钥,第二参数指定一个密钥算法的名称
SecretKeySpec signinKey = null;
signinKey = new SecretKeySpec(Base64.getDecoder().decode(key),
"Hmac" + signatureMethod.toUpperCase());
//生成一个指定 Mac 算法 的 Mac 对象
Mac mac = null;
mac = Mac.getInstance("Hmac" + signatureMethod.toUpperCase());
//用给定密钥初始化 Mac 对象
mac.init(signinKey);
//完成 Mac 操作
return mac.doFinal(data.getBytes());
}
public enum SignatureMethod {
SHA1, MD5, SHA256;
}
public static void main(String[] args) throws UnsupportedEncodingException, NoSuchAlgorithmException, InvalidKeyException {
String version = "2020-05-29";
String resourceName = "userid/12321";
String expirationTime = System.currentTimeMillis() / 1000 + 100 * 24 * 60 * 60 + "";
String signatureMethod = SignatureMethod.SHA1.name().toLowerCase();
String accessKey = "KuF3NT/jUBJ62LNBB/A8XZA9CqS3Cu79B/ABmfA1UCw=";
String token = assembleToken(version, resourceName, expirationTime, signatureMethod, accessKey);
System.out.println("Authorization:" + token);
}
}
Øgo代码示例
func  (s *SignService) GenerateSign(params_map map[string]string, access_key string) (string, error){
signature_str := params_map["et"] + "\n" + params_map["method"] + "\n" + params_map["res"] + "\n" + params_map["version"]
hmac_str := ""
switch strings.ToLower(params_map["method"]) {
case "sha1":
hmac_str = tools.HmacSha1(signature_str, tools.Base64Decode(access_key))
case "sha256":
hmac_str = tools.HmacSha256(signature_str, tools.Base64Decode(access_key))
case "md5":
hmac_str = tools.HmacMd5(signature_str, tools.Base64Decode(access_key))
default:
return "",errors.New("签名参数错误！")
}
sign :=tools.Base64Encode(hmac_str)
return sign,nil
}
func Base64Encode(message string) string {
return base64.StdEncoding.EncodeToString([]byte(message))
}
func Base64Decode(message string) string {
decode_str, err := base64.StdEncoding.DecodeString(message)
if err != nil {
return ""
}
return string(decode_str)
}
func HmacSha256(data string, secret string) string {
h := hmac.New(sha256.New, []byte(secret))
h.Write([]byte(data))
return string(h.Sum(nil))
//return hex.EncodeToString(h.Sum(nil))
}
func HmacMd5(data string, secret string) string {
h := hmac.New(md5.New, []byte(secret))
h.Write([]byte(data))
return string(h.Sum(nil))
//return hex.EncodeToString(h.Sum(nil))
}
func HmacSha1(data string, secret string) string {
h := hmac.New(sha1.New, []byte(secret))
h.Write([]byte(data))
return string(h.Sum(nil))
//return hex.EncodeToString(h.Sum(nil)) //不需以十六进制字符串输出
}
Øphp代码示例
class SafetyAuth
```
{
```
private  $_version = '2020-05-29';//版本
private  $_method = 'sha1';//加密方法，还可以用md5、sha256
private  $_access_key;//访问密钥
private  $_res ;//资源参数
private  $_et;//到期时间戳
private  $_expiration;//有效期，有效时间
```
public function __construct($access_key, $expiration,$res){
```
$this->_expiration = $expiration;
$this->_access_key = $access_key;
$this->_res = $res;
}
//生成sign
```
private function _makeSign() {
```
date_default_timezone_set('PRC');
$this->_et =time() + $this->_expiration;
$string_for_signature = $this->_et . "\n" . $this->_method . "\n" . $this->_res  . "\n" . $this->_version;
$b64_decode_acckey = base64_decode($this->_access_key);
$hmac_key = hash_hmac($this->_method, $this->_strToUtf8($string_for_signature), $b64_decode_acckey, true);
$sign = base64_encode($hmac_key);
return $sign;
}
```
private  function _strToUtf8($str){
```
$encode = mb_detect_encoding($str, array("ASCII",'UTF-8',"GB2312","GBK",'BIG5'));
if($encode == 'UTF-8'){
return $str;
}else{
return mb_convert_encoding($str, 'UTF-8', $encode);
}
}
//生成token
```
public  function makeToken() {
```
$sign = $this->_makeSign();
$token = sprintf("version=2020-05-29&res=%s&et=%s&method=sha1&sign=%s", urlencode($this->_res), $this->_et, urlencode($sign));
return $token;
}
}

## 错误码

本文档列举API调用失败时，返回的错误码。出现缺少请求参数、不合法的请求参数等错误时，请参见具体API描述进行修改。
资源权限相关错误码：


| 错误码 | 描述 |
| --- | --- |
| authPermissionDeny | 鉴权失败 |
| resourePermissionDeny | 无资源访问权限 |
| parameterRequired | 缺少请求参数 |
| parameterMissing | 缺少请求参数 |
| invalidParameter | 不合法的请求参数 |


产品相关错误码：


| 错误码 | 描述 |
| --- | --- |
| productNotFound | 产品不存在 |
| productHasNoDevice | 产品未创建设备 |


设备相关错误码：


| 错误码 | 描述 |
| --- | --- |
| deviceNotFound | 设备不存在 |
| setPropertyFailed | 设备属性设置失败 |
| setDesiredPeropertyFailed | 设备属性期望设置失败 |
| queryDesiredProperyFailed | 设备属性期望查询失败 |
| getTmProperties | 设备属性获取失败 |
| callTmService | 设备服务调用失败 |
| deleteDesiredPeropertyFailed | 设备属性期望删除失败 |
| queryCurrentData | 设备最新数据查询失败 |
| queryPropertyHistoryData | 设备属性历史数据查询失败 |
| queryEventHistoryData | 设备事件历史数据查询失败 |
| queryOperationLog | 设备操作记录查询失败 |



## API列表


### 产品管理


#### 产品详情



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=ProductDetail&version=1&product_id=10132 | /common?action=ProductDetail&version=1&product_id=10132 | /common?action=ProductDetail&version=1&product_id=10132 | /common?action=ProductDetail&version=1&product_id=10132 |
| 请求头 |  |  |  |  |
| URL参数 | product_id | string | 必填 | 产品id |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.device_number | number | number | 设备数量 |
| 响应参数 | data.product_id | string | string | 产品ID |
| 响应参数 | data.name | string | string | 产品名称 |
| 响应参数 | data.desc | string | string | 产品描述 |
| 响应参数 | data.network | string | string | 联网方式 |
| 响应参数 | data.category | string | string | 产品所属分类ID |
| 响应参数 | data.category_name | string | string | 产品所属分类名称 |
| 响应参数 | data.protocol | number | number | 协议类型 1-泛协议 2-MQTT 3-CoAP |
| 响应参数 | data.create_time | string | string | 创建时间 |
| 响应参数 | data.ind_title | string | string | 产品行业名称 |
| 响应参数 | data.prod_ind | string | string | 产品行业编码 |
| 响应参数 | data.prod_chain | array | array | 产品行业编码层级关系 |
| 响应参数 | data.uid | string | string | 产品用户ID |
| 响应参数 | data.sec_key | string | string | 产品权限key |
| 响应参数 | data.template_id | string | string | 模板id |
| 响应参数 | data.template_info | array | array | 模板信息 |
| 请求示例 | GET /common?action=ProductDetail&version=1&product_id=10132 | GET /common?action=ProductDetail&version=1&product_id=10132 | GET /common?action=ProductDetail&version=1&product_id=10132 | GET /common?action=ProductDetail&version=1&product_id=10132 |
| 响应示例 | {     "data": {         "device_number":0,         "protocol":2,         "created_time":"2021-12-06T08:28:56.762Z",         "product_id":"wjrJjSRtsG",         "network":"1",         "category":"138",         "ind_title":"智慧城市",         "prod_ind":"1",         "uid":37782,         "sec_key":"vC3eX2gr8mapsNZ1zYVmtsFRMYaX953GbJiKlcAQTp4=",         "desc":"",         "name":"物模型", "template_id": "6406f2ee9641f20035c53b12", "template_info": []     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "device_number":0,         "protocol":2,         "created_time":"2021-12-06T08:28:56.762Z",         "product_id":"wjrJjSRtsG",         "network":"1",         "category":"138",         "ind_title":"智慧城市",         "prod_ind":"1",         "uid":37782,         "sec_key":"vC3eX2gr8mapsNZ1zYVmtsFRMYaX953GbJiKlcAQTp4=",         "desc":"",         "name":"物模型", "template_id": "6406f2ee9641f20035c53b12", "template_info": []     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "device_number":0,         "protocol":2,         "created_time":"2021-12-06T08:28:56.762Z",         "product_id":"wjrJjSRtsG",         "network":"1",         "category":"138",         "ind_title":"智慧城市",         "prod_ind":"1",         "uid":37782,         "sec_key":"vC3eX2gr8mapsNZ1zYVmtsFRMYaX953GbJiKlcAQTp4=",         "desc":"",         "name":"物模型", "template_id": "6406f2ee9641f20035c53b12", "template_info": []     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "device_number":0,         "protocol":2,         "created_time":"2021-12-06T08:28:56.762Z",         "product_id":"wjrJjSRtsG",         "network":"1",         "category":"138",         "ind_title":"智慧城市",         "prod_ind":"1",         "uid":37782,         "sec_key":"vC3eX2gr8mapsNZ1zYVmtsFRMYaX953GbJiKlcAQTp4=",         "desc":"",         "name":"物模型", "template_id": "6406f2ee9641f20035c53b12", "template_info": []     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 产品列表



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=ProductList&version=1 | /common?action=ProductList&version=1 | /common?action=ProductList&version=1 | /common?action=ProductList&version=1 |
| 请求头 |  |  |  |  |
| URL参数 | name | string | 可选 | 产品名称 |
| URL参数 | manufacturer | string | 可选 | 厂商名称 |
| URL参数 | protocol | string | 可选 | 接入协议，可选['1', '2', '3', '4', '5', '6', '7', '8', '9', '0'] |
| URL参数 | industry | string | 可选 | 行业类型编码 |
| URL参数 | offset | string | 可选 | 请求起始位置，默认0 |
| URL参数 | limit | string | 可选 | 每次请求记录数，默认10 |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时, 返回业务数据 |
| 响应参数 | data.list | array | array | 产品信息集合，如下的l表示 list 数组的单个对象标识 |
| 响应参数 | l. total | number | number | 设备数量 |
| 响应参数 | l. desc | string | string | 描述 |
| 响应参数 | l. protocol | number | number | 协议 1-泛协议 2-MQTT 3-CoAP |
| 响应参数 | l. created_time | string | string | 创建时间 |
| 响应参数 | l. product_id | string | string | 产品ID |
| 响应参数 | l. network | string | string | 联网模式 1-其他 2-蜂窝 3-wifi 4-以太网 |
| 响应参数 | l. ind_title | string | string | 产品行业名称 |
| 响应参数 | l. prod_ind | string | string | 产品行业编码 |
| 响应参数 | l. uid | string | string | 产品用户ID |
| 响应参数 | l. sec_key | string | string | 产品权限KEY |
| 响应参数 | l. name | string | string | 产品名称 |
| 响应参数 | l. manufacturer | string | string | 厂商名称 |
| 响应参数 | l.template_id | string | string | 模板id |
| 响应参数 | l.prod_chain | array | array | 产品行业编码层级关系 |
| 响应参数 | l. category | array | array | 分类ID |
| 响应参数 | l.category_name | string | string | 分类名称 |
| 响应参数 | data.meta | object | object | 分页信息 |
| 响应参数 | data.meta.limit | number | number | 每次请求记录数 |
| 响应参数 | data.meta.offset | number | number | 请求记录起始位置 |
| 响应参数 | data.meta.total | number | number | 条数 |
| 请求示例 | GET /common?action=ProductList&version=1&product_id=wA10WBynvt | GET /common?action=ProductList&version=1&product_id=wA10WBynvt | GET /common?action=ProductList&version=1&product_id=wA10WBynvt | GET /common?action=ProductList&version=1&product_id=wA10WBynvt |
| 响应示例 | {     "data": {          "list":[            "total":2,                 "protocol":4,                 "created_time":"2021-08-31T08:00:12.846Z",                 "product_id":"wA10WBynvt",                 "network":"3",                 "category":["66006c672de43d02590b098b"],                 "ind_title":"智慧城市",                 "prod_ind":"1", 				"prod_chain":["3","9"],                 "uid":5,                  "template_id":"6687c206537561748c69f470",        "sec_key":"RJKrcCGT22DYGSQ4KVXslu/Jnh3bezHzvhqCTFMk05Q=",                 "desc":"",                 "name":"qwe123",                 "manufacturer":"S1234567890", 				"category_name":"智能后视镜"         ],         "meta":{             "total":1,             "limit":10,             "offset":0         }      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "list":[            "total":2,                 "protocol":4,                 "created_time":"2021-08-31T08:00:12.846Z",                 "product_id":"wA10WBynvt",                 "network":"3",                 "category":["66006c672de43d02590b098b"],                 "ind_title":"智慧城市",                 "prod_ind":"1", 				"prod_chain":["3","9"],                 "uid":5,                  "template_id":"6687c206537561748c69f470",        "sec_key":"RJKrcCGT22DYGSQ4KVXslu/Jnh3bezHzvhqCTFMk05Q=",                 "desc":"",                 "name":"qwe123",                 "manufacturer":"S1234567890", 				"category_name":"智能后视镜"         ],         "meta":{             "total":1,             "limit":10,             "offset":0         }      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "list":[            "total":2,                 "protocol":4,                 "created_time":"2021-08-31T08:00:12.846Z",                 "product_id":"wA10WBynvt",                 "network":"3",                 "category":["66006c672de43d02590b098b"],                 "ind_title":"智慧城市",                 "prod_ind":"1", 				"prod_chain":["3","9"],                 "uid":5,                  "template_id":"6687c206537561748c69f470",        "sec_key":"RJKrcCGT22DYGSQ4KVXslu/Jnh3bezHzvhqCTFMk05Q=",                 "desc":"",                 "name":"qwe123",                 "manufacturer":"S1234567890", 				"category_name":"智能后视镜"         ],         "meta":{             "total":1,             "limit":10,             "offset":0         }      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "list":[            "total":2,                 "protocol":4,                 "created_time":"2021-08-31T08:00:12.846Z",                 "product_id":"wA10WBynvt",                 "network":"3",                 "category":["66006c672de43d02590b098b"],                 "ind_title":"智慧城市",                 "prod_ind":"1", 				"prod_chain":["3","9"],                 "uid":5,                  "template_id":"6687c206537561748c69f470",        "sec_key":"RJKrcCGT22DYGSQ4KVXslu/Jnh3bezHzvhqCTFMk05Q=",                 "desc":"",                 "name":"qwe123",                 "manufacturer":"S1234567890", 				"category_name":"智能后视镜"         ],         "meta":{             "total":1,             "limit":10,             "offset":0         }      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |
|  |  |  |  |  |



#### 产品设备列表



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DeviceList&version=1 | /common?action=DeviceList&version=1 | /common?action=DeviceList&version=1 | /common?action=DeviceList&version=1 |
| 请求头 |  |  |  |  |
| URL参数 | name | string | 可选 | 设备名称 |
| URL参数 | product_id | string | 可选 | 产品ID |
| URL参数 | status | string | 可选 | 设备状态，可选['1'未激活, '2'在线, '3'离线] |
| URL参数 | offset | string | 可选 | 请求起始位置，默认0 |
| URL参数 | limit | string | 可选 | 每次请求记录数，默认10 |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时, 返回业务数据 |
| 响应参数 | data.list | array | array | 产品信息集合，如下的l表示 list 数组的单个对象标识 |
| 响应参数 | l. product_id | string | string | 产品ID |
| 响应参数 | l. name | string | string | 设备名称 |
| 响应参数 | l. node_type | number | number | 节点类型1：直连设备，2：网关设备，3：网关子设备 |
| 响应参数 | l. status | number | number | 设备状态1：未激活，2：在线，3：离线 【默认为未激活】 |
| 响应参数 | l. last_time | string | string | 设备最后一次在线时间 |
| 响应参数 | l. created_time | string | string | 创建时间 |
| 响应参数 | l. from | string | string | 设备来源(1:自主创建，2:他人转移) |
| 响应参数 | l. lon | string | string | 经度 |
| 响应参数 | l. lat | string | string | 纬度 |
| 响应参数 | l. idid | string | string | 设备ID |
| 响应参数 | l. product_name | string | string | 产品名称 |
| 响应参数 | l.scene | array | array | 场景id |
| 响应参数 | data.meta | object | object | 分页信息 |
| 响应参数 | data.meta.limit | number | number | 每次请求记录数 |
| 响应参数 | data.meta.offset | number | number | 请求记录起始位置 |
| 响应参数 | data.meta.total | number | number | 条数 |
| 请求示例 | GET /common?action=DeviceList&version=1 | GET /common?action=DeviceList&version=1 | GET /common?action=DeviceList&version=1 | GET /common?action=DeviceList&version=1 |
| 响应示例 | {     "data": {           "list":[             {                 "pid":"7ubgKi1vhm",                 "name":"400A002090011001",                 "ct":"2021-11-30T08:22:53.519Z",                 "node_type":1,                 "status":3,                 "last_time":"2021-12-10T10:19:33.327Z",                 "from":1,                 "lon":"",                 "lat":"",                 "idid":"10015446",                 "product_id":"7ubgKi1vhm",                 "created_time":"2021-11-30T08:22:53.519Z",                 "id":10015446,                 "product_name":"水电费",                 "scene":["a25087f46df040ef0acfd115"]             }         ],         "meta":{             "total":1,             "limit":10,             "offset":0         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {           "list":[             {                 "pid":"7ubgKi1vhm",                 "name":"400A002090011001",                 "ct":"2021-11-30T08:22:53.519Z",                 "node_type":1,                 "status":3,                 "last_time":"2021-12-10T10:19:33.327Z",                 "from":1,                 "lon":"",                 "lat":"",                 "idid":"10015446",                 "product_id":"7ubgKi1vhm",                 "created_time":"2021-11-30T08:22:53.519Z",                 "id":10015446,                 "product_name":"水电费",                 "scene":["a25087f46df040ef0acfd115"]             }         ],         "meta":{             "total":1,             "limit":10,             "offset":0         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {           "list":[             {                 "pid":"7ubgKi1vhm",                 "name":"400A002090011001",                 "ct":"2021-11-30T08:22:53.519Z",                 "node_type":1,                 "status":3,                 "last_time":"2021-12-10T10:19:33.327Z",                 "from":1,                 "lon":"",                 "lat":"",                 "idid":"10015446",                 "product_id":"7ubgKi1vhm",                 "created_time":"2021-11-30T08:22:53.519Z",                 "id":10015446,                 "product_name":"水电费",                 "scene":["a25087f46df040ef0acfd115"]             }         ],         "meta":{             "total":1,             "limit":10,             "offset":0         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {           "list":[             {                 "pid":"7ubgKi1vhm",                 "name":"400A002090011001",                 "ct":"2021-11-30T08:22:53.519Z",                 "node_type":1,                 "status":3,                 "last_time":"2021-12-10T10:19:33.327Z",                 "from":1,                 "lon":"",                 "lat":"",                 "idid":"10015446",                 "product_id":"7ubgKi1vhm",                 "created_time":"2021-11-30T08:22:53.519Z",                 "id":10015446,                 "product_name":"水电费",                 "scene":["a25087f46df040ef0acfd115"]             }         ],         "meta":{             "total":1,             "limit":10,             "offset":0         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 产品设备数量统计



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=ProductDeviceStatistics&version=1 | /common?action=ProductDeviceStatistics&version=1 | /common?action=ProductDeviceStatistics&version=1 | /common?action=ProductDeviceStatistics&version=1 |
| 请求头 |  |  |  |  |
| URL参数 | product_id | string | 必填 | 产品id |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | 调用失败时，返回的错误码 | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | 调用失败时，返回的错误信息 | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | 调用API时生成的请求标识 | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | 接口是否调用成功 | 接口是否调用成功 |
| 响应参数 | data | － | 调用成功时，返回的业务数据 | 调用成功时，返回的业务数据 |
| 响应参数 | data.unactive | number | 未激活设备数 | 未激活设备数 |
| 响应参数 | data.online | number | 在线设备数 | 在线设备数 |
| 响应参数 | data.offline | number | 离线设备数 | 离线设备数 |
| 响应参数 | data.total | number | 总的设备数 | 总的设备数 |
| 请求示例 | GET /common?action=ProductDeviceStatistics&version=1&product_id=7ubgKi1vhm | GET /common?action=ProductDeviceStatistics&version=1&product_id=7ubgKi1vhm | GET /common?action=ProductDeviceStatistics&version=1&product_id=7ubgKi1vhm | GET /common?action=ProductDeviceStatistics&version=1&product_id=7ubgKi1vhm |
| 响应示例 | {     "data": {           "unactive":6, // 未激活数         "online":0, // 在线数         "offline":8, // 离线数         "total":14 // 总数 }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {           "unactive":6, // 未激活数         "online":0, // 在线数         "offline":8, // 离线数         "total":14 // 总数 }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {           "unactive":6, // 未激活数         "online":0, // 在线数         "offline":8, // 离线数         "total":14 // 总数 }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {           "unactive":6, // 未激活数         "online":0, // 在线数         "offline":8, // 离线数         "total":14 // 总数 }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



### 设备管理


#### 设备创建



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=CreateDevice&version=1 | /common?action=CreateDevice&version=1 | /common?action=CreateDevice&version=1 | /common?action=CreateDevice&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体参数 | device_name | string | 必填 | 设备名称 |
| 请求体参数 | product_id | string | 必填 | 产品ID |
| 请求体参数 | imei | string | 可选(LwM2M协议时必填) | NB设备imei，15个数字组成的电子串号，设备所属产品为LwM2M时，为必填 |
| 请求体参数 | imsi | string | 可选 | NB设备imsi，不超过15个的数字，设备所属产品为LwM2M时，为必填 |
| 请求体参数 | psk | string | 可选 | NB设备所需属性，若创建未填则平台随机生成，8-16位数字字母组合 |
| 请求体参数 | template_field | object | 可选 | 如产品有选择设备档案模版，根据所选模版构造的json对象 |
| 请求体参数 | auth_code | string | 可选 | NB设备鉴权码，1-16位数字字母组合 |
| 请求体参数 | desc | string | 可选 | 设备描述 |
| 请求体参数 | tag | object | 可选 | 设备标签 |
| 请求体参数 | scene | string | 必填 | 场景_id |
| 请求体参数 | supplier | number | 必填 | 供应商id |
| 请求体参数 | template_field | object | 可选 | 设备档案数据 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | ―― | ―― | 调用成功返回业务数据 |
| 响应参数 | data.name | string | string | 设备名称 |
| 响应参数 | data.node_type | string | string | 节点类型 1-直连设备 |
| 响应参数 | data.desc | string | string | 设备描述 |
| 响应参数 | data.sec_key | string | string | 设备密钥 |
| 响应参数 | data.protocol | int | int | 协议 1-泛协议 2-MQTT 3-CoAP |
| 响应参数 | data.created_time | string | string | 创建时间 |
| 响应参数 | data.imei | string | string | NB设备imei，15个数字组成的电子串号 |
| 响应参数 | data.imsi | string | string | NB设备imsi，不超过15个的数字 |
| 响应参数 | data.auth_code | string | string | NB设备鉴权码 |
| 响应参数 | data.psk | string | string | NB设备所需属性 |
| 响应参数 | data.tag | object | object | 设备标签 |
| 响应参数 | data.template_field | object | object | 设备档案数据 |
| 响应参数 | data.template_id | string | string | 模板ID |
| 请求示例 | {     "product_id":  "9MaNe52pNO",     "device_name": "no003",     "imei": "366322456556584",     "imsi": "366322456556584",     "auth_code": "authcode",        "psk": "authcode",    "desc": "iot application",     "tag": {"tagkey":"tagvalue"}, "template_field": {"key":"value"} } | {     "product_id":  "9MaNe52pNO",     "device_name": "no003",     "imei": "366322456556584",     "imsi": "366322456556584",     "auth_code": "authcode",        "psk": "authcode",    "desc": "iot application",     "tag": {"tagkey":"tagvalue"}, "template_field": {"key":"value"} } | {     "product_id":  "9MaNe52pNO",     "device_name": "no003",     "imei": "366322456556584",     "imsi": "366322456556584",     "auth_code": "authcode",        "psk": "authcode",    "desc": "iot application",     "tag": {"tagkey":"tagvalue"}, "template_field": {"key":"value"} } | {     "product_id":  "9MaNe52pNO",     "device_name": "no003",     "imei": "366322456556584",     "imsi": "366322456556584",     "auth_code": "authcode",        "psk": "authcode",    "desc": "iot application",     "tag": {"tagkey":"tagvalue"}, "template_field": {"key":"value"} } |
| 响应示例 | {     "data": {         "name": "no003",         "node_type": 1,          "desc": "iot application",          "sec_key": "imQE5CGsIiT9ZMBMD/bSbqMnPIBwXXsYynQQsi/fimk=",         "created_time": "2020-06-08T10:33:30.442Z",          "protocol": 1,         "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"}，     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "name": "no003",         "node_type": 1,          "desc": "iot application",          "sec_key": "imQE5CGsIiT9ZMBMD/bSbqMnPIBwXXsYynQQsi/fimk=",         "created_time": "2020-06-08T10:33:30.442Z",          "protocol": 1,         "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"}，     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "name": "no003",         "node_type": 1,          "desc": "iot application",          "sec_key": "imQE5CGsIiT9ZMBMD/bSbqMnPIBwXXsYynQQsi/fimk=",         "created_time": "2020-06-08T10:33:30.442Z",          "protocol": 1,         "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"}，     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "name": "no003",         "node_type": 1,          "desc": "iot application",          "sec_key": "imQE5CGsIiT9ZMBMD/bSbqMnPIBwXXsYynQQsi/fimk=",         "created_time": "2020-06-08T10:33:30.442Z",          "protocol": 1,         "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"}，     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 批量创建设备



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=BatchCreateDevices&version=1 | /common?action=BatchCreateDevices&version=1 | /common?action=BatchCreateDevices&version=1 | /common?action=BatchCreateDevices&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL 参数 | 无 | 无 | 无 | 无 |
| 请求体参数 | product_id | string | 必填 | 产品ID |
| 请求体参数 | devices | array | 必填 | 批量创建的设备信息集合, 一次最多创建500个设备。每个集合元素为json对象，包括name、desc、scene、supplier和档案数据属性值,例如[{ "name": "no001" , "scene": "660a1a925599c5007e1991cd" ，"supplier": 5，"desc": "iot application" ,"template_field": {"key":"value"}}], 设备为LwM2M协议时，增加imei、imsi、auth_code、psk属性，如产品有选择设备档案模版增加template_field属性，校验规则请参考设备创建接口 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | ―― | ―― | 调用成功返回业务数据 |
| 响应参数 | data.list | array | array | 创建成功设备信息集合，如下的l表示 list 数组的单个对象标识 |
| 响应参数 | l.name | string | string | 设备名称 |
| 响应参数 | l.node_type | Int | Int | 设备类型  1-直连设备 |
| 响应参数 | l.desc | string | string | 设备描述 |
| 响应参数 | l.sec_key | string | string | 设备密钥 |
| 响应参数 | l.protocol | int | int | 协议类型  1-泛协议  2-MQTT  3-CoAP |
| 响应参数 | l.imei | string | string | imei |
| 响应参数 | l.imsi | string | string | imsi |
| 响应参数 | l.auth_code | string | string | auth_code |
| 响应参数 | l.psk | string | string | psk |
| 响应参数 | l.created_time | string | string | 创建时间 |
| 响应参数 | l.template_field | object | object | 设备档案数据 |
| 响应参数 | l.template_id | string | string | 模板ID |
| 请求示例 | {       "product_id": "9MaNe52pNO",     "devices": [         {             "name": "no001",              "desc": "iot application",             "scene": "660a1a925599c5007e1991cd"，             "supplier": 5， "template_field": {"key":"value"}                   }     ] } | {       "product_id": "9MaNe52pNO",     "devices": [         {             "name": "no001",              "desc": "iot application",             "scene": "660a1a925599c5007e1991cd"，             "supplier": 5， "template_field": {"key":"value"}                   }     ] } | {       "product_id": "9MaNe52pNO",     "devices": [         {             "name": "no001",              "desc": "iot application",             "scene": "660a1a925599c5007e1991cd"，             "supplier": 5， "template_field": {"key":"value"}                   }     ] } | {       "product_id": "9MaNe52pNO",     "devices": [         {             "name": "no001",              "desc": "iot application",             "scene": "660a1a925599c5007e1991cd"，             "supplier": 5， "template_field": {"key":"value"}                   }     ] } |
| 响应示例 | {     "data": {         list: [{             "name": "no001",             "node_type": 1,               "desc": "iot application",             "sec_key": "imQE5CGsIiT9ZMBMD/bSbqMnPIBwXXsYynQQsi/fimk=",              "created_time": "2020-06-08T10:33:30.442Z",              "protocol": 1, "template_id": "6406f2ee9641f20035c53b12", "template_field": {"key":"value"}           }]      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         list: [{             "name": "no001",             "node_type": 1,               "desc": "iot application",             "sec_key": "imQE5CGsIiT9ZMBMD/bSbqMnPIBwXXsYynQQsi/fimk=",              "created_time": "2020-06-08T10:33:30.442Z",              "protocol": 1, "template_id": "6406f2ee9641f20035c53b12", "template_field": {"key":"value"}           }]      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         list: [{             "name": "no001",             "node_type": 1,               "desc": "iot application",             "sec_key": "imQE5CGsIiT9ZMBMD/bSbqMnPIBwXXsYynQQsi/fimk=",              "created_time": "2020-06-08T10:33:30.442Z",              "protocol": 1, "template_id": "6406f2ee9641f20035c53b12", "template_field": {"key":"value"}           }]      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         list: [{             "name": "no001",             "node_type": 1,               "desc": "iot application",             "sec_key": "imQE5CGsIiT9ZMBMD/bSbqMnPIBwXXsYynQQsi/fimk=",              "created_time": "2020-06-08T10:33:30.442Z",              "protocol": 1, "template_id": "6406f2ee9641f20035c53b12", "template_field": {"key":"value"}           }]      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备编辑



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=UpdateDevice&version=1 | /common?action=UpdateDevice&version=1 | /common?action=UpdateDevice&version=1 | /common?action=UpdateDevice&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体参数 | device_name | string | 必填 | 设备名称 |
| 请求体参数 | product_id | string | 必填 | 产品ID |
| 请求体参数 | imsi | string | 可选 | NB设备imsi，不超过15个的数字，设备所属产品为LwM2M时，为必填 |
| 请求体参数 | psk | string | 可选 | NB设备所需属性，若创建未填则平台随机生成，8-16位数字字母组合 |
| 请求体参数 | auth_code | string | 可选 | NB设备鉴权码，1-16位数字字母组合 |
| 请求体参数 | desc | string | 可选 | 设备描述 |
| 请求体参数 | tag | object | 可选 | 设备标签 |
| 请求体参数 | template_field | object | 可选 | 设备档案数据 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | ―― | ―― | 调用成功返回业务数据 |
| 响应参数 | data.device_name | string | string | 设备名称 |
| 响应参数 | data.desc | string | string | 设备描述 |
| 响应参数 | data.tag | object | object | 设备标签 |
| 响应参数 | data.template_field | object | object | 设备档案数据 |
| 请求示例 | {     "product_id":  "9MaNe52pNO", "device_name": "no003", "desc": "iot application", "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"} } | {     "product_id":  "9MaNe52pNO", "device_name": "no003", "desc": "iot application", "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"} } | {     "product_id":  "9MaNe52pNO", "device_name": "no003", "desc": "iot application", "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"} } | {     "product_id":  "9MaNe52pNO", "device_name": "no003", "desc": "iot application", "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"} } |
| 响应示例 | {     "data": {         "device_name": "no003",         "desc": "iot application", "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"}     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "device_name": "no003",         "desc": "iot application", "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"}     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "device_name": "no003",         "desc": "iot application", "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"}     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "device_name": "no003",         "desc": "iot application", "tag": {"tagkey":"tagvalue"},    "template_field": {"key":"value"}     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备删除



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DeleteDevice&version=1 | /common?action=DeleteDevice&version=1 | /common?action=DeleteDevice&version=1 | /common?action=DeleteDevice&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体参数 | device_name | string | 必填 | 设备名称 |
| 请求体参数 | product_id | string | 必填 | 产品ID |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 请求示例 | {     "product_id":  "9MaNe52pNO",     "device_name": "no003" } | {     "product_id":  "9MaNe52pNO",     "device_name": "no003" } | {     "product_id":  "9MaNe52pNO",     "device_name": "no003" } | {     "product_id":  "9MaNe52pNO",     "device_name": "no003" } |
| 响应示例 | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备详情



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=QueryDeviceDetail&version=1&product_id=lsibd9 &device_name=no001 | /common?action=QueryDeviceDetail&version=1&product_id=lsibd9 &device_name=no001 | /common?action=QueryDeviceDetail&version=1&product_id=lsibd9 &device_name=no001 | /common?action=QueryDeviceDetail&version=1&product_id=lsibd9 &device_name=no001 |
| 请求头 |  |  |  |  |
| URL参数 | product_id | string | 必填 | 产品id |
| URL参数 | device_name | string | 必填 | 设备名称 |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.device_name | string | string | 设备名称 |
| 响应参数 | data.product_id | string | string | 产品ID |
| 响应参数 | data.product_name | string | string | 产品名称 |
| 响应参数 | data.desc | string | string | 设备描述 |
| 响应参数 | data.status | int | int | 设备状态 1-未激活 2-在线 3-离线 |
| 响应参数 | data.node_type | int | int | 节点类型 1-直连设备 |
| 响应参数 | data.protocol | int | int | 协议类型 1-泛协议 2-MQTT 3-CoAP |
| 响应参数 | data.ip | string | string | 设备连接ip |
| 响应参数 | data.create_time | string | string | 创建时间 |
| 响应参数 | data.last_time | string | string | 最后一次在线时间 |
| 响应参数 | data.active_time | string | string | 激活时间 |
| 响应参数 | data.sec_key | string | string | 设备密钥 |
| 响应参数 | data.template_id | string | string | 所用的模板id |
| 响应参数 | data.template_field | object | object | 模板中添加的数据 |
| 请求示例 | GET /common?action=QueryDeviceDetail&version=1&product_id=lsibd9 &device_name=no001 | GET /common?action=QueryDeviceDetail&version=1&product_id=lsibd9 &device_name=no001 | GET /common?action=QueryDeviceDetail&version=1&product_id=lsibd9 &device_name=no001 | GET /common?action=QueryDeviceDetail&version=1&product_id=lsibd9 &device_name=no001 |
| 响应示例 | {     "data": {         "device_name": "no001",         "product_id": "9MaNe52pNO",         "product_name": "空气净化器",         "active_time": "2020-06-19T08:11:27.801Z",         "created_time": "2020-06-19T06:09:22.550Z",         "desc": "设备1",             "ip": "192.168.200.139",         "last_time": "2020-06-19T09:48:15.027Z",         "node_type": 1,             "protocol": 2,         "sec_key": "UQd3K9lXR/EbLXeJc50lJfvvkTVdu5uFgbfz48/fI5k=",         "status": 3,         "template_id": "6406f2ee9641f20035c53b12", "template_field": {}, "scene":["a25087f46df040ef0acfd115"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "device_name": "no001",         "product_id": "9MaNe52pNO",         "product_name": "空气净化器",         "active_time": "2020-06-19T08:11:27.801Z",         "created_time": "2020-06-19T06:09:22.550Z",         "desc": "设备1",             "ip": "192.168.200.139",         "last_time": "2020-06-19T09:48:15.027Z",         "node_type": 1,             "protocol": 2,         "sec_key": "UQd3K9lXR/EbLXeJc50lJfvvkTVdu5uFgbfz48/fI5k=",         "status": 3,         "template_id": "6406f2ee9641f20035c53b12", "template_field": {}, "scene":["a25087f46df040ef0acfd115"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "device_name": "no001",         "product_id": "9MaNe52pNO",         "product_name": "空气净化器",         "active_time": "2020-06-19T08:11:27.801Z",         "created_time": "2020-06-19T06:09:22.550Z",         "desc": "设备1",             "ip": "192.168.200.139",         "last_time": "2020-06-19T09:48:15.027Z",         "node_type": 1,             "protocol": 2,         "sec_key": "UQd3K9lXR/EbLXeJc50lJfvvkTVdu5uFgbfz48/fI5k=",         "status": 3,         "template_id": "6406f2ee9641f20035c53b12", "template_field": {}, "scene":["a25087f46df040ef0acfd115"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "device_name": "no001",         "product_id": "9MaNe52pNO",         "product_name": "空气净化器",         "active_time": "2020-06-19T08:11:27.801Z",         "created_time": "2020-06-19T06:09:22.550Z",         "desc": "设备1",             "ip": "192.168.200.139",         "last_time": "2020-06-19T09:48:15.027Z",         "node_type": 1,             "protocol": 2,         "sec_key": "UQd3K9lXR/EbLXeJc50lJfvvkTVdu5uFgbfz48/fI5k=",         "status": 3,         "template_id": "6406f2ee9641f20035c53b12", "template_field": {}, "scene":["a25087f46df040ef0acfd115"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备状态查询



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DeviceStatus&version=1 | /common?action=DeviceStatus&version=1 | /common?action=DeviceStatus&version=1 | /common?action=DeviceStatus&version=1 |
| 请求头 |  |  |  |  |
| URL参数 | product_id | string | 必填 | 产品ID |
| URL参数 | device_name | string | 必填 | 设备名称 |
| 请求体 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时, 返回业务数据 |
| 响应参数 | data.status | int | int | 设备状态 1-未激活 2-在线 3-离线 |
| 请求示例 | GET  /common?action=DeviceStatus&version=1&product_id=9MaNe52pNO&device_name=no001 | GET  /common?action=DeviceStatus&version=1&product_id=9MaNe52pNO&device_name=no001 | GET  /common?action=DeviceStatus&version=1&product_id=9MaNe52pNO&device_name=no001 | GET  /common?action=DeviceStatus&version=1&product_id=9MaNe52pNO&device_name=no001 |
| 响应示例 | {     "data": {         status: 1     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         status: 1     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         status: 1     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         status: 1     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备状态记录查询



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DeviceStatusHistory&version=1 | /common?action=DeviceStatusHistory&version=1 | /common?action=DeviceStatusHistory&version=1 | /common?action=DeviceStatusHistory&version=1 |
| 请求头 |  |  |  |  |
| URL参数 | product_id | string | 必填 | 产品ID |
| URL参数 | device_name | string | 必填 | 设备名称 |
| URL参数 | start_time | string | 必填 | 查询起始时间，毫秒时间戳 |
| URL参数 | end_time | string | 必填 | 查询结束时间，毫秒时间戳 |
| URL参数 | offset | string | 可选 | 请求起始位置，默认0 |
| URL参数 | limit | string | 可选 | 每次请求记录数，默认10, 范围[1, 100] |
| 请求体 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时, 返回业务数据 |
| 响应参数 | data.list | array | array | 设备状态历史数据集合，如下的l表示 list 数组的单个对象标识 |
| 响应参数 | l.status | int | int | 设备状态 0-离线 1-在线 |
| 响应参数 | l.time | date | date | 时间戳 |
| 响应参数 | data.meta | object | object | 分页信息 |
| 响应参数 | data.meta.limit | int | int | 每次请求记录数 |
| 响应参数 | data.meta.offset | int | int | 请求记录起始位置 |
| 请求示例 | GET url/common?action=QueryDeviceStatusHistory&version=1&product_id=9MaNe52pNO&device_name=no001&start_time=1592795951065&end_time=1592795971065 | GET url/common?action=QueryDeviceStatusHistory&version=1&product_id=9MaNe52pNO&device_name=no001&start_time=1592795951065&end_time=1592795971065 | GET url/common?action=QueryDeviceStatusHistory&version=1&product_id=9MaNe52pNO&device_name=no001&start_time=1592795951065&end_time=1592795971065 | GET url/common?action=QueryDeviceStatusHistory&version=1&product_id=9MaNe52pNO&device_name=no001&start_time=1592795951065&end_time=1592795971065 |
| 响应示例 | {     "data": {         "list": [{             "status": 0,             "time": 1592398421297,         }],         "meta": {             "limit": 10,             "offset": 0         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "list": [{             "status": 0,             "time": 1592398421297,         }],         "meta": {             "limit": 10,             "offset": 0         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "list": [{             "status": 0,             "time": 1592398421297,         }],         "meta": {             "limit": 10,             "offset": 0         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "list": [{             "status": 0,             "time": 1592398421297,         }],         "meta": {             "limit": 10,             "offset": 0         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备属性设置



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=SetDeviceProperty&version=1 | /common?action=SetDeviceProperty&version=1 | /common?action=SetDeviceProperty&version=1 | /common?action=SetDeviceProperty&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | device_name | string | 必填 | 设备名称 |
| 请求体 参数 | product_id | string | 必填 | 产品ID |
| 请求体 参数 | params | object | 必填 | 设置的属性值, 数据格式为json对象, 形式为key:value, key为属性功能点标识, value为属性值, 取值符合物模型定义的数据类型和取值范围, 例如 { "switch": true } |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | -- | -- | 调用成功时，返回的业务数据 |
| 响应参数 | data.id | string | string | 设备端回复消息id |
| 响应参数 | data.code | int | int | 设备端回复响应码 |
| 响应参数 | data.msg | string | string | 设备端回复响应消息 |
| 请求示例 | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": {         "switch": true,           // bool         "text": "hello",          // string         "humidity": 12 ,          // int32         "number": 1564448722123,        // int64         "temperature": 30.2             // float         "lng": 3.1234567890123456789,   // double         "type": 1,                      // enum         "error": 256,                   // bitmap         "event":  {                     // struct             "a": 1,             "b": true          }     } } | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": {         "switch": true,           // bool         "text": "hello",          // string         "humidity": 12 ,          // int32         "number": 1564448722123,        // int64         "temperature": 30.2             // float         "lng": 3.1234567890123456789,   // double         "type": 1,                      // enum         "error": 256,                   // bitmap         "event":  {                     // struct             "a": 1,             "b": true          }     } } | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": {         "switch": true,           // bool         "text": "hello",          // string         "humidity": 12 ,          // int32         "number": 1564448722123,        // int64         "temperature": 30.2             // float         "lng": 3.1234567890123456789,   // double         "type": 1,                      // enum         "error": 256,                   // bitmap         "event":  {                     // struct             "a": 1,             "b": true          }     } } | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": {         "switch": true,           // bool         "text": "hello",          // string         "humidity": 12 ,          // int32         "number": 1564448722123,        // int64         "temperature": 30.2             // float         "lng": 3.1234567890123456789,   // double         "type": 1,                      // enum         "error": 256,                   // bitmap         "event":  {                     // struct             "a": 1,             "b": true          }     } } |
| 响应示例 | {     "data": {         "id": "155",          "code":  200,                "msg": "success"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "id": "155",          "code":  200,                "msg": "success"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "id": "155",          "code":  200,                "msg": "success"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "id": "155",          "code":  200,                "msg": "success"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备属性获取



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=QueryDevicePropertyDetail&version=1 | /common?action=QueryDevicePropertyDetail&version=1 | /common?action=QueryDevicePropertyDetail&version=1 | /common?action=QueryDevicePropertyDetail&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | device_name | string | 必填 | 设备唯一标识 |
| 请求体 参数 | product_id | string | 必填 | 产品ID |
| 请求体 参数 | params | array | 必填 | 功能点标识数组，expample: ["light","model"] |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | -- | -- | 调用成功时，返回的业务数据 |
| 请求示例 | {   "product_id":"B7EEW578EbRg5Y4K",   "device_name":"device3",   "params":["light","model"] } | {   "product_id":"B7EEW578EbRg5Y4K",   "device_name":"device3",   "params":["light","model"] } | {   "product_id":"B7EEW578EbRg5Y4K",   "device_name":"device3",   "params":["light","model"] } | {   "product_id":"B7EEW578EbRg5Y4K",   "device_name":"device3",   "params":["light","model"] } |
| 响应示例 | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{         "light":1,         "model":1     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{         "light":1,         "model":1     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{         "light":1,         "model":1     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{         "light":1,         "model":1     } } |



#### 设备属性期望值设置



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=SetDeviceDesiredProperty&version=1 | /common?action=SetDeviceDesiredProperty&version=1 | /common?action=SetDeviceDesiredProperty&version=1 | /common?action=SetDeviceDesiredProperty&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | device_name | string | 必填 | 设备名称 |
| 请求体 参数 | product_id | string | 必填 | 产品ID |
| 请求体 参数 | params | object | 必填 | 设置的属性期望值, 数据格式为json对象, 形式为key:value, key为属性功能点标识, value为属性值, 取值符合物模型定义的数据类型和取值范围, 例如{ "switch": true } |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 请求示例 | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": {         "switch": true,             // bool         "text": "hello",            // string         "humidity": 12 ,            // int32         "number": 1564448722123,      // int64         "temperature": 30.2             // float         "lng": 3.1234567890123456789,   // double         "type": 1,                      // enum         "error": 256,                   // bitmap         "event":  {                    // struct             "a": 1,             "b": true          }     } } | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": {         "switch": true,             // bool         "text": "hello",            // string         "humidity": 12 ,            // int32         "number": 1564448722123,      // int64         "temperature": 30.2             // float         "lng": 3.1234567890123456789,   // double         "type": 1,                      // enum         "error": 256,                   // bitmap         "event":  {                    // struct             "a": 1,             "b": true          }     } } | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": {         "switch": true,             // bool         "text": "hello",            // string         "humidity": 12 ,            // int32         "number": 1564448722123,      // int64         "temperature": 30.2             // float         "lng": 3.1234567890123456789,   // double         "type": 1,                      // enum         "error": 256,                   // bitmap         "event":  {                    // struct             "a": 1,             "b": true          }     } } | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": {         "switch": true,             // bool         "text": "hello",            // string         "humidity": 12 ,            // int32         "number": 1564448722123,      // int64         "temperature": 30.2             // float         "lng": 3.1234567890123456789,   // double         "type": 1,                      // enum         "error": 256,                   // bitmap         "event":  {                    // struct             "a": 1,             "b": true          }     } } |
| 响应示例 | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备属性期望值查询



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=QueryDeviceDesiredProperty&version=1 | /common?action=QueryDeviceDesiredProperty&version=1 | /common?action=QueryDeviceDesiredProperty&version=1 | /common?action=QueryDeviceDesiredProperty&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | device_name | string | 必填 | 设备名称 |
| 请求体 参数 | product_id | string | 必填 | 产品ID |
| 请求体 参数 | params | array | 必填 | 查询期望值的功能点标识集合，参数不传默认查询所有属性期望，例如["switch", "temperature"] |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | ―― | ―― | 调用成功返回业务数据 |
| 响应参数 | data.params | object | object | 属性功能点期望值 |
| 响应参数 | data.params. identify | object | object | 功能点标识为对象key |
| 响应参数 | data.params. identify.value | string | string | 期望值值 |
| 请求示例 | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": [         "switch",         "temperature",     ] } | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": [         "switch",         "temperature",     ] } | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": [         "switch",         "temperature",     ] } | {     "product_id": "9MaNe52pNO",     "device_name": "no001",     "params": [         "switch",         "temperature",     ] } |
| 响应示例 | {     "data": {        "params": {              "switch": {                 "value": "on"             },             "temperature": {                 "value": 23             }         }      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {        "params": {              "switch": {                 "value": "on"             },             "temperature": {                 "value": 23             }         }      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {        "params": {              "switch": {                 "value": "on"             },             "temperature": {                 "value": 23             }         }      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {        "params": {              "switch": {                 "value": "on"             },             "temperature": {                 "value": 23             }         }      },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备属性期望删除



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DeleteDeviceDesiredProperty&version=1 | /common?action=DeleteDeviceDesiredProperty&version=1 | /common?action=DeleteDeviceDesiredProperty&version=1 | /common?action=DeleteDeviceDesiredProperty&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | device_name | string | 必填 | 设备名称 |
| 请求体 参数 | product_id | string | 必填 | 产品ID |
| 请求体 参数 | params | object | 必填 | 删除的属性期望, 数据格式为json对象, 形式为key:value, key为属性功能点标识, value为空对象{} |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 请求示例 | {     "product_id": "12909",     "device_name": "no001",     "params": {         "temperature": {},  // 删除期望值     } } | {     "product_id": "12909",     "device_name": "no001",     "params": {         "temperature": {},  // 删除期望值     } } | {     "product_id": "12909",     "device_name": "no001",     "params": {         "temperature": {},  // 删除期望值     } } | {     "product_id": "12909",     "device_name": "no001",     "params": {         "temperature": {},  // 删除期望值     } } |
| 响应示例 | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备属性最新数据查询



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DevicePropertyData&version=1 | /common?action=DevicePropertyData&version=1 | /common?action=DevicePropertyData&version=1 | /common?action=DevicePropertyData&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | product_id | string | 必填 | 产品id |
| URL参数 | device_name | string | 必填 | 设备名称 |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 错误码，code为“0”代表请求成功 |
| 响应参数 | msg | string | string | 错误消息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.list | array | array | 设备最新数据集合，如下的l表示 list 数组的单个对象标识 |
| 响应参数 | l.identifier | string | string | 功能点标识 |
| 响应参数 | l.time | string | string | 上报时间，毫秒时间戳 |
| 响应参数 | l.value | string | string | 功能点上报值，json字符串 |
| 响应参数 | l.data_type | string | string | 数据类型 int32、int64、float、double、enum、bool、string、struct、bitMap |
| 响应参数 | l.access_mode | string | string | 读写类型 |
| 响应参数 | l.expect_value | string | string | 期望值, json字符串，属性功能点具有该字段 |
| 响应参数 | l.name | string | string | 功能点名称 |
| 响应参数 | l.description | string | string | 功能描述 |
| 请求示例 | GET /common?action=DevicePropertyData&version=1&product_id=9MaNe52pNO&device_name=no001 | GET /common?action=DevicePropertyData&version=1&product_id=9MaNe52pNO&device_name=no001 | GET /common?action=DevicePropertyData&version=1&product_id=9MaNe52pNO&device_name=no001 | GET /common?action=DevicePropertyData&version=1&product_id=9MaNe52pNO&device_name=no001 |
| 响应示例 | {     "data": {         "list": [{            {                 "access_mode": "读写",                 "data_type": "int32",                 "description": "二氧化碳",                 "expect_value": "800",                 "identifier": "CO2",                 "name": "二氧化碳",                 "time": "1592797444539",                 "value": "600"             },             {                 "access_mode": "读写",                 "data_type": "bool",                 "description": "关",                 "expect_value": "true",                 "identifier": "fan",                 "name": "风扇",                 "time": "1592797444539",                 "value": "false"             }         }]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "list": [{            {                 "access_mode": "读写",                 "data_type": "int32",                 "description": "二氧化碳",                 "expect_value": "800",                 "identifier": "CO2",                 "name": "二氧化碳",                 "time": "1592797444539",                 "value": "600"             },             {                 "access_mode": "读写",                 "data_type": "bool",                 "description": "关",                 "expect_value": "true",                 "identifier": "fan",                 "name": "风扇",                 "time": "1592797444539",                 "value": "false"             }         }]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "list": [{            {                 "access_mode": "读写",                 "data_type": "int32",                 "description": "二氧化碳",                 "expect_value": "800",                 "identifier": "CO2",                 "name": "二氧化碳",                 "time": "1592797444539",                 "value": "600"             },             {                 "access_mode": "读写",                 "data_type": "bool",                 "description": "关",                 "expect_value": "true",                 "identifier": "fan",                 "name": "风扇",                 "time": "1592797444539",                 "value": "false"             }         }]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "list": [{            {                 "access_mode": "读写",                 "data_type": "int32",                 "description": "二氧化碳",                 "expect_value": "800",                 "identifier": "CO2",                 "name": "二氧化碳",                 "time": "1592797444539",                 "value": "600"             },             {                 "access_mode": "读写",                 "data_type": "bool",                 "description": "关",                 "expect_value": "true",                 "identifier": "fan",                 "name": "风扇",                 "time": "1592797444539",                 "value": "false"             }         }]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备属性功能点历史数据查询



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DevicePropertyHistory&version=1 | /common?action=DevicePropertyHistory&version=1 | /common?action=DevicePropertyHistory&version=1 | /common?action=DevicePropertyHistory&version=1 |
| 请求头 |  |  |  |  |
| URL参数 | product_id | string | 必填 | 产品id |
| URL参数 | device_name | string | 必填 | 设备名称 |
| URL参数 | identifier | string | 必填 | 属性功能点标识 |
| URL参数 | start_time | string | 必填 | 查询起始时间，毫秒时间戳 |
| URL参数 | end_time | string | 必填 | 查询结束时间，毫秒时间戳 |
| URL参数 | offset | string | 可选 | 请求起始位置，默认0 |
| URL参数 | limit | string | 可选 | 每次请求记录数，默认10, 范围[1, 100] |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 错误码，code为“0”代表请求成功 |
| 响应参数 | msg | string | string | 错误消息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.list | array | array | 设备属性记录集合，如下的l表示 list 数组的单个对象标识 |
| 响应参数 | l.value | string | string | 属性功能点上报值 |
| 响应参数 | l.time | string | string | 属性功能点上报时间 |
| 响应参数 | data.meta | object | object | 分页信息 |
| 响应参数 | data.meta.limit | int | int | 每次请求记录数 |
| 响应参数 | data.meta.offset | int | int | 请求记录起始位置 |
| 请求示例 | GET /common?action=DevicePropertyHistory&version=1&product_id=9MaNe52pNO&device_name=no001&identifier=fan&start_time=1615342778414&end_time=1615342898096 | GET /common?action=DevicePropertyHistory&version=1&product_id=9MaNe52pNO&device_name=no001&identifier=fan&start_time=1615342778414&end_time=1615342898096 | GET /common?action=DevicePropertyHistory&version=1&product_id=9MaNe52pNO&device_name=no001&identifier=fan&start_time=1615342778414&end_time=1615342898096 | GET /common?action=DevicePropertyHistory&version=1&product_id=9MaNe52pNO&device_name=no001&identifier=fan&start_time=1615342778414&end_time=1615342898096 |
| 响应示例 | {     "data": {         "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "time":"1639380798206",                 "value":"qweasd"             },             {                 "time":"1639380795091",                 "value":"qweasd"             }         ]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "time":"1639380798206",                 "value":"qweasd"             },             {                 "time":"1639380795091",                 "value":"qweasd"             }         ]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "time":"1639380798206",                 "value":"qweasd"             },             {                 "time":"1639380795091",                 "value":"qweasd"             }         ]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "time":"1639380798206",                 "value":"qweasd"             },             {                 "time":"1639380795091",                 "value":"qweasd"             }         ]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备事件功能点（单个）历史数据



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?version=1&action=DeviceEventHistory | /common?version=1&action=DeviceEventHistory | /common?version=1&action=DeviceEventHistory | /common?version=1&action=DeviceEventHistory |
| 请求头 |  |  |  |  |
| URL参数 | product_id | string | 必填 | 产品id |
| URL参数 | device_name | string | 必填 | 设备名称 |
| URL参数 | identifier | string | 可选 | 事件功能点标识 |
| URL参数 | start_time | string | 必填 | 查询起始时间，毫秒时间戳 |
| URL参数 | end_time | string | 必填 | 查询结束时间，毫秒时间戳 |
| URL参数 | offset | string | 可选 | 请求起始位置，默认0 |
| URL参数 | limit | string | 可选 | 每次请求记录数，默认10, 范围[1, 100] |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.list | array | array | 设备事件记录历史数据集合，如下的l表示 list 数组的单个对象标识 |
| 响应参数 | l.event_type | int | int | 事件类型 1-信息 2-告警 3-故障 |
| 响应参数 | l.identifier | string | string | 事件功能点标识 |
| 响应参数 | l.name | string | string | 事件功能点名称 |
| 响应参数 | l.time | string | string | 事件功能点上报时间 |
| 响应参数 | l.value | string | string | 事件功能点上报值，json字符串 |
| 响应参数 | data.meta | object | object | 分页信息 |
| 响应参数 | data.meta.limit | int | int | 每次请求记录数 |
| 响应参数 | data.meta.offset | int | int | 请求记录起始位置 |
| 请求示例 | GET /common?version=1&action=DeviceEventHistory&product_id=9MaNe52pNO&device_name=no001&start_time=1592811019119&end_time=1592811198213 | GET /common?version=1&action=DeviceEventHistory&product_id=9MaNe52pNO&device_name=no001&start_time=1592811019119&end_time=1592811198213 | GET /common?version=1&action=DeviceEventHistory&product_id=9MaNe52pNO&device_name=no001&start_time=1592811019119&end_time=1592811198213 | GET /common?version=1&action=DeviceEventHistory&product_id=9MaNe52pNO&device_name=no001&start_time=1592811019119&end_time=1592811198213 |
| 响应示例 | {     "data": {         "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "time":"1639381959167",                 "value":"{\"a\":11}",                 "event_type":1,                 "identifier":"sj01",                 "name":"sj01"             }         ]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "time":"1639381959167",                 "value":"{\"a\":11}",                 "event_type":1,                 "identifier":"sj01",                 "name":"sj01"             }         ]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "time":"1639381959167",                 "value":"{\"a\":11}",                 "event_type":1,                 "identifier":"sj01",                 "name":"sj01"             }         ]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "time":"1639381959167",                 "value":"{\"a\":11}",                 "event_type":1,                 "identifier":"sj01",                 "name":"sj01"             }         ]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备服务执行记录查询



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DeviceServiceHistory&version=1 | /common?action=DeviceServiceHistory&version=1 | /common?action=DeviceServiceHistory&version=1 | /common?action=DeviceServiceHistory&version=1 |
| 请求头 |  |  |  |  |
| URL参数 | product_id | string | 必填 | 产品id |
| URL参数 | device_name | string | 必填 | 设备名称 |
| URL参数 | start_time | string | 必填 | 查询起始时间，毫秒时间戳 |
| URL参数 | end_time | string | 必填 | 查询结束时间，毫秒时间戳 |
| URL参数 | offset | string | 可选 | 请求起始位置，默认0 |
| URL参数 | limit | string | 可选 | 每次请求记录数，默认10, 范围[1, 100] |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.list | array | array | 设备服务执行记录数据集合，如下的l表示 list 数组的单个对象标识 |
| 响应参数 | list.request_time | string | string | 调用服务的时间 |
| 响应参数 | list.function_name | string | string | 功能名称 |
| 响应参数 | list.identifier | string | string | 标识符 |
| 响应参数 | list.type | string | string | 服务调用类型，0为同步，1为异步 |
| 响应参数 | list.request_body | string | string | 服务调用时的请求参数 |
| 响应参数 | list.response_time | string | string | 返回时间 |
| 响应参数 | list.response_body | string | string | 输出参数，json string |
| 响应参数 | list.code | string | string | 执行结果code，200：执行成功，0：未执行，其他：执行异常 |
| 响应参数 | list.msg | string | string | 返回消息 |
| 响应参数 | data.meta | object | object | 分页信息 |
| 响应参数 | data.meta.limit | int | int | 每次请求记录数 |
| 响应参数 | data.meta.offset | int | int | 请求记录起始位置 |
| 请求示例 | GET /common?action=DeviceServiceHistory&version=1&product_id=7ubgKi1vhm&device_name=sb0011&start_time=1639050724393&end_time=1639381724393 | GET /common?action=DeviceServiceHistory&version=1&product_id=7ubgKi1vhm&device_name=sb0011&start_time=1639050724393&end_time=1639381724393 | GET /common?action=DeviceServiceHistory&version=1&product_id=7ubgKi1vhm&device_name=sb0011&start_time=1639050724393&end_time=1639381724393 | GET /common?action=DeviceServiceHistory&version=1&product_id=7ubgKi1vhm&device_name=sb0011&start_time=1639050724393&end_time=1639381724393 |
| 响应示例 | {     "data": {          "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "request_time":"1639383257642",                 "function_name":"s1",                 "identifier":"s1",                 "type":1,                 "request_body":"{\"id\":\"2\",\"params\":{\"identifier\":\"s1\",\"input\":{\"b\":2}},\"version\":\"1.0\"}",                 "response_time":"0",                 "response_body":"",                 "code":0,                 "msg":""             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "request_time":"1639383257642",                 "function_name":"s1",                 "identifier":"s1",                 "type":1,                 "request_body":"{\"id\":\"2\",\"params\":{\"identifier\":\"s1\",\"input\":{\"b\":2}},\"version\":\"1.0\"}",                 "response_time":"0",                 "response_body":"",                 "code":0,                 "msg":""             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "request_time":"1639383257642",                 "function_name":"s1",                 "identifier":"s1",                 "type":1,                 "request_body":"{\"id\":\"2\",\"params\":{\"identifier\":\"s1\",\"input\":{\"b\":2}},\"version\":\"1.0\"}",                 "response_time":"0",                 "response_body":"",                 "code":0,                 "msg":""             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "meta":{             "offset":0,             "limit":10         },         "list":[             {                 "request_time":"1639383257642",                 "function_name":"s1",                 "identifier":"s1",                 "type":1,                 "request_body":"{\"id\":\"2\",\"params\":{\"identifier\":\"s1\",\"input\":{\"b\":2}},\"version\":\"1.0\"}",                 "response_time":"0",                 "response_body":"",                 "code":0,                 "msg":""             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备操作记录



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DeviceOperateHistory&version=1 | /common?action=DeviceOperateHistory&version=1 | /common?action=DeviceOperateHistory&version=1 | /common?action=DeviceOperateHistory&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | product_id | string | 必填 | 产品id |
| URL参数 | device_name | string | 必填 | 设备名称 |
| URL参数 | start_time | string | 必填 | 开始时间，毫秒时间戳 |
| URL参数 | end_time | string | 必填 | 结束时间，毫秒时间戳 |
| URL参数 | limit | string | 可选 | 每次请求记录数，默认10, 范围[1, 100] |
| URL参数 | offset | string | 可选 | 请求起始位置，默认0 |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 错误码，code为“0”代表请求成功 |
| 响应参数 | msg | string | string | 错误消息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.list | array | array | 设备操作记录集合，如下的l表示 list 数组的单个对象标识 |
| 响应参数 | l.request_time | string | string | 请求时间 |
| 响应参数 | l.type | int | int | 请求类型 0-写 1-读 |
| 响应参数 | l.request_body | object | object | 请求内容 k=>v形式， k为属性功能点标识，v为功能点设置值 |
| 响应参数 | l.response_time | string | string | 响应时间 |
| 响应参数 | l.response_body | object | object | 响应结果, 设备回复响应中的msg字段 |
| 响应参数 | l.response_body.id | string | string | 响应结果中的id |
| 响应参数 | l.response_body.code | int | int | 响应结果中的code |
| 响应参数 | l.response_body.msg | string | string | 响应结果中信息 |
| 响应参数 | l.code | int | int | 执行结果code，200：执行成功 |
| 响应参数 | l.msg | string | string | 返回消息 |
| 响应参数 | data.meta | object | object | 分页信息 |
| 响应参数 | data.meta.limit | int | int | 每次请求记录数 |
| 响应参数 | data.meta.offset | int | int | 请求记录起始位置 |
| 请求示例 | GET /common?action=DeviceOperateHistory&version=1&product_id=9MaNe52pNO&device_name=no001 &start_time=1592398386297&end_time=1592398422297 | GET /common?action=DeviceOperateHistory&version=1&product_id=9MaNe52pNO&device_name=no001 &start_time=1592398386297&end_time=1592398422297 | GET /common?action=DeviceOperateHistory&version=1&product_id=9MaNe52pNO&device_name=no001 &start_time=1592398386297&end_time=1592398422297 | GET /common?action=DeviceOperateHistory&version=1&product_id=9MaNe52pNO&device_name=no001 &start_time=1592398386297&end_time=1592398422297 |
| 响应示例 | {     "data": {        "list":[             {                 "request_time":"1639382709533",                 "type":0,                 "request_body":"{\"tt\":1}",                 "response_time":"1639382709570",                 "response_body":{                     "id":"1",                     "code":200,                     "msg":"success"                 },                 "code":200,                 "msg":"success"             }         ],         "meta":{             "offset":0,             "limit":10         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {        "list":[             {                 "request_time":"1639382709533",                 "type":0,                 "request_body":"{\"tt\":1}",                 "response_time":"1639382709570",                 "response_body":{                     "id":"1",                     "code":200,                     "msg":"success"                 },                 "code":200,                 "msg":"success"             }         ],         "meta":{             "offset":0,             "limit":10         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {        "list":[             {                 "request_time":"1639382709533",                 "type":0,                 "request_body":"{\"tt\":1}",                 "response_time":"1639382709570",                 "response_body":{                     "id":"1",                     "code":200,                     "msg":"success"                 },                 "code":200,                 "msg":"success"             }         ],         "meta":{             "offset":0,             "limit":10         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {        "list":[             {                 "request_time":"1639382709533",                 "type":0,                 "request_body":"{\"tt\":1}",                 "response_time":"1639382709570",                 "response_body":{                     "id":"1",                     "code":200,                     "msg":"success"                 },                 "code":200,                 "msg":"success"             }         ],         "meta":{             "offset":0,             "limit":10         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备服务调用



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=CallService&version=1 | /common?action=CallService&version=1 | /common?action=CallService&version=1 | /common?action=CallService&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | device_name | string | 必填 | 设备名称 |
| 请求体 参数 | product_id | string | 必填 | 产品ID |
| 请求体 参数 | identifier | string | 必填 | 服务型功能点标识 |
| 请求体 参数 | params | object | 必填 | 输入参数的键值对，输入参数的唯一标识做键 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | ―― | ―― | 调用成功返回业务数据 |
| 请求示例 | {   "product_id":"B7EEW578EbRg5Y4K",   "device_name":"device3",   "identifier": "light",   "params":{     "Power1":"1",     "WF1":"2"   } } | {   "product_id":"B7EEW578EbRg5Y4K",   "device_name":"device3",   "identifier": "light",   "params":{     "Power1":"1",     "WF1":"2"   } } | {   "product_id":"B7EEW578EbRg5Y4K",   "device_name":"device3",   "identifier": "light",   "params":{     "Power1":"1",     "WF1":"2"   } } | {   "product_id":"B7EEW578EbRg5Y4K",   "device_name":"device3",   "identifier": "light",   "params":{     "Power1":"1",     "WF1":"2"   } } |
| 响应示例 | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{       "result1":"1",       "result2":"2"     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{       "result1":"1",       "result2":"2"     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{       "result1":"1",       "result2":"2"     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{       "result1":"1",       "result2":"2"     } } |



#### 设备链路日志查询



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DeviceTraceLog&version=1 | /common?action=DeviceTraceLog&version=1 | /common?action=DeviceTraceLog&version=1 | /common?action=DeviceTraceLog&version=1 |
| 请求头 |  |  |  |  |
| URL请求参数 | product_id | string | 可选 | 产品id |
| URL请求参数 | device_name | string | 可选 | 设备名称 |
| URL请求参数 | start_time | string | 必填 | 查询起始时间，毫秒时间戳 |
| URL请求参数 | end_time | string | 必填 | 查询结束时间，毫秒时间戳 |
| URL请求参数 | offset | string | 可选 | 请求起始位置，默认0 |
| URL请求参数 | limit | string | 可选 | 每次请求记录数，默认10, 范围[1, 100] |
| URL请求参数 | log_type | string | 可选 | 业务类型编码，参考备注 |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.list | array | array | 设备链接日志记录数据集合 |
| 响应参数 | data.meta | object | object | 分页信息 |
| 响应参数 | data.meta.limit | int | int | 每次请求记录数 |
| 响应参数 | data.meta.offset | int | int | 请求记录起始位置 |
| 请求示例 | GET /common?action=DeviceTraceLog&version=1start_time=1639050724393&end_time=1639381724393 | GET /common?action=DeviceTraceLog&version=1start_time=1639050724393&end_time=1639381724393 | GET /common?action=DeviceTraceLog&version=1start_time=1639050724393&end_time=1639381724393 | GET /common?action=DeviceTraceLog&version=1start_time=1639050724393&end_time=1639381724393 |
| 响应示例 | {     "data": {          "list":[             {                 "type":"1.1",                 "start_time":"2021-12-10T10:19:33.325Z",                 "pid":"7ubgKi1vhm",                 "status":"200",                 "trace_id":"ab2fc05759a211ecbfd023bbbfff50a4",                 "end_time":"2021-12-10T10:19:33.325Z",                 "env_type":"UNKNOWN",                 "uid":"5",                 "device_name":"400A002090011001",                 "content":"{\"protocol\":\"MQTT\",\"offline_time\":\"2021-12-10 18:19:33.325\",\"offline_reason\":\"CloseByPeer\"}",                 "create_time":"2021-12-10 18:19:33",                 "message_status":"0",                 "type_mean":"设备行为",                 "status_mean":"成功"             }         ],         "meta":{             "total":26,             "limit":"11",             "offset":"0"         }     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "list":[             {                 "type":"1.1",                 "start_time":"2021-12-10T10:19:33.325Z",                 "pid":"7ubgKi1vhm",                 "status":"200",                 "trace_id":"ab2fc05759a211ecbfd023bbbfff50a4",                 "end_time":"2021-12-10T10:19:33.325Z",                 "env_type":"UNKNOWN",                 "uid":"5",                 "device_name":"400A002090011001",                 "content":"{\"protocol\":\"MQTT\",\"offline_time\":\"2021-12-10 18:19:33.325\",\"offline_reason\":\"CloseByPeer\"}",                 "create_time":"2021-12-10 18:19:33",                 "message_status":"0",                 "type_mean":"设备行为",                 "status_mean":"成功"             }         ],         "meta":{             "total":26,             "limit":"11",             "offset":"0"         }     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "list":[             {                 "type":"1.1",                 "start_time":"2021-12-10T10:19:33.325Z",                 "pid":"7ubgKi1vhm",                 "status":"200",                 "trace_id":"ab2fc05759a211ecbfd023bbbfff50a4",                 "end_time":"2021-12-10T10:19:33.325Z",                 "env_type":"UNKNOWN",                 "uid":"5",                 "device_name":"400A002090011001",                 "content":"{\"protocol\":\"MQTT\",\"offline_time\":\"2021-12-10 18:19:33.325\",\"offline_reason\":\"CloseByPeer\"}",                 "create_time":"2021-12-10 18:19:33",                 "message_status":"0",                 "type_mean":"设备行为",                 "status_mean":"成功"             }         ],         "meta":{             "total":26,             "limit":"11",             "offset":"0"         }     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "list":[             {                 "type":"1.1",                 "start_time":"2021-12-10T10:19:33.325Z",                 "pid":"7ubgKi1vhm",                 "status":"200",                 "trace_id":"ab2fc05759a211ecbfd023bbbfff50a4",                 "end_time":"2021-12-10T10:19:33.325Z",                 "env_type":"UNKNOWN",                 "uid":"5",                 "device_name":"400A002090011001",                 "content":"{\"protocol\":\"MQTT\",\"offline_time\":\"2021-12-10 18:19:33.325\",\"offline_reason\":\"CloseByPeer\"}",                 "create_time":"2021-12-10 18:19:33",                 "message_status":"0",                 "type_mean":"设备行为",                 "status_mean":"成功"             }         ],         "meta":{             "total":26,             "limit":"11",             "offset":"0"         }     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |
| 备注 | 业务类型对照表：{   '1.1': '设备行为',   '1.2': '上行消息',   '1.3': '下行消息',   '2.1': '物模型调用',   '3.1': '数据存储',   '4.1': '规则引擎',   '5.1': 'MQ推送',   '6.1': 'HTTP推送',   '7.1': '开放API',   '8.1': 'RDS存储',   '9.1': '应用长连接' } | 业务类型对照表：{   '1.1': '设备行为',   '1.2': '上行消息',   '1.3': '下行消息',   '2.1': '物模型调用',   '3.1': '数据存储',   '4.1': '规则引擎',   '5.1': 'MQ推送',   '6.1': 'HTTP推送',   '7.1': '开放API',   '8.1': 'RDS存储',   '9.1': '应用长连接' } | 业务类型对照表：{   '1.1': '设备行为',   '1.2': '上行消息',   '1.3': '下行消息',   '2.1': '物模型调用',   '3.1': '数据存储',   '4.1': '规则引擎',   '5.1': 'MQ推送',   '6.1': 'HTTP推送',   '7.1': '开放API',   '8.1': 'RDS存储',   '9.1': '应用长连接' } | 业务类型对照表：{   '1.1': '设备行为',   '1.2': '上行消息',   '1.3': '下行消息',   '2.1': '物模型调用',   '3.1': '数据存储',   '4.1': '规则引擎',   '5.1': 'MQ推送',   '6.1': 'HTTP推送',   '7.1': '开放API',   '8.1': 'RDS存储',   '9.1': '应用长连接' } |



#### 设备上下行消息查询



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DeviceMessage&version=1&message_id=fe8e158c5cab11ecbfd05180177bf746 | /common?action=DeviceMessage&version=1&message_id=fe8e158c5cab11ecbfd05180177bf746 | /common?action=DeviceMessage&version=1&message_id=fe8e158c5cab11ecbfd05180177bf746 | /common?action=DeviceMessage&version=1&message_id=fe8e158c5cab11ecbfd05180177bf746 |
| 请求头 |  |  |  |  |
| URL参数 | message_id | string | 必填 | 消息id 通过接口【设备链路日志查询】获取（只存在部分类型的日志信息中） |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据，data为base64 字符串，可转义 |
| 请求示例 | GET /common?action=DeviceMessage&version=1&message_id=fe8e158c5cab11ecbfd05180177bf746 | GET /common?action=DeviceMessage&version=1&message_id=fe8e158c5cab11ecbfd05180177bf746 | GET /common?action=DeviceMessage&version=1&message_id=fe8e158c5cab11ecbfd05180177bf746 | GET /common?action=DeviceMessage&version=1&message_id=fe8e158c5cab11ecbfd05180177bf746 |
| 响应示例 | {     "data": "eyJpZCI6IjE2Mzk0NjU0MzIzOTMiLCJjb2RlIjoyMDAsIm1zZyI6InN1Y2Nlc3MifQ==",,     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": "eyJpZCI6IjE2Mzk0NjU0MzIzOTMiLCJjb2RlIjoyMDAsIm1zZyI6InN1Y2Nlc3MifQ==",,     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": "eyJpZCI6IjE2Mzk0NjU0MzIzOTMiLCJjb2RlIjoyMDAsIm1zZyI6InN1Y2Nlc3MifQ==",,     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": "eyJpZCI6IjE2Mzk0NjU0MzIzOTMiLCJjb2RlIjoyMDAsIm1zZyI6InN1Y2Nlc3MifQ==",,     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 设备转移



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=MoveProductDevice&version=1 | /common?action=MoveProductDevice&version=1 | /common?action=MoveProductDevice&version=1 | /common?action=MoveProductDevice&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体参数 | device_name | array | 必填 | 被转移设备的名称数组，如["name_1", "name_2"] |
| 请求体参数 | product_id | string | 必填 | 产品ID |
| 请求体参数 | target_user_tel | string | 必填 | 接收人电话 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 请求示例 | {     "product_id": "IOoSyVbY8q",     "device_name": ["SB00009"],     "target_user_tel": "17830021227" } | {     "product_id": "IOoSyVbY8q",     "device_name": ["SB00009"],     "target_user_tel": "17830021227" } | {     "product_id": "IOoSyVbY8q",     "device_name": ["SB00009"],     "target_user_tel": "17830021227" } | {     "product_id": "IOoSyVbY8q",     "device_name": ["SB00009"],     "target_user_tel": "17830021227" } |
| 响应示例 | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data": {       "move_id": "1317465"     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data": {       "move_id": "1317465"     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data": {       "move_id": "1317465"     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data": {       "move_id": "1317465"     } } |



#### 设备批量命令下发



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DeviceBatchOrder&version=1 | /common?action=DeviceBatchOrder&version=1 | /common?action=DeviceBatchOrder&version=1 | /common?action=DeviceBatchOrder&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | device_name | array | 必填 | 设备名称组成的数组 |
| 请求体 参数 | product_id | string | 必填 | 产品ID，只能对同一产品下的多个设备下发 |
| 请求体 参数 | type | string | 必填 | 可选['SET_PROPERTY', 'GET_PROPERTY','CALL_SERVICE']，依次为属性设置、属性获取、服务调用 |
| 请求体 参数 | mode | number | 必填 | 命令模式，1：串行；2：并行。 |
| 请求体 参数 | identifier | string |  | 参数type值为CALL_SERVICE时必填，服务型功能点标识 |
| 请求体 参数 | params | object 或者array | 必填 | 根据参数type值参考对应接口的params进行构造： SET_PROPERTY： 设备属性设置 GET_PROPERTY： 设备属性获取 CALL_SERVICE： 设备服务调用 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | ―― | ―― | 调用成功返回业务数据 |
| 请求示例 | { 	"type": "SET_PROPERTY", 	"mode": 1, 	"product_id": "fcvPpxC22R", 	"device_name": ["test9981121"], 	"params":{"a":1} } | { 	"type": "SET_PROPERTY", 	"mode": 1, 	"product_id": "fcvPpxC22R", 	"device_name": ["test9981121"], 	"params":{"a":1} } | { 	"type": "SET_PROPERTY", 	"mode": 1, 	"product_id": "fcvPpxC22R", 	"device_name": ["test9981121"], 	"params":{"a":1} } | { 	"type": "SET_PROPERTY", 	"mode": 1, 	"product_id": "fcvPpxC22R", 	"device_name": ["test9981121"], 	"params":{"a":1} } |
| 响应示例 | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{         "successCount": 0, // 命令成功数         "errorCount": 1, // 如果是并行命令则表示命令失败数，如果是串行命令表示剩余未下发命令的设备数         "errorDevs": [] // 命令下发失败的设备名称，只有并行命令时有值，串行命令时无数据值     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{         "successCount": 0, // 命令成功数         "errorCount": 1, // 如果是并行命令则表示命令失败数，如果是串行命令表示剩余未下发命令的设备数         "errorDevs": [] // 命令下发失败的设备名称，只有并行命令时有值，串行命令时无数据值     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{         "successCount": 0, // 命令成功数         "errorCount": 1, // 如果是并行命令则表示命令失败数，如果是串行命令表示剩余未下发命令的设备数         "errorDevs": [] // 命令下发失败的设备名称，只有并行命令时有值，串行命令时无数据值     } } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true,     "data":{         "successCount": 0, // 命令成功数         "errorCount": 1, // 如果是并行命令则表示命令失败数，如果是串行命令表示剩余未下发命令的设备数         "errorDevs": [] // 命令下发失败的设备名称，只有并行命令时有值，串行命令时无数据值     } } |



### 物模型管理


#### 物模型查询



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=QueryThingModel&version=1&product_id=lsibd9 | /common?action=QueryThingModel&version=1&product_id=lsibd9 | /common?action=QueryThingModel&version=1&product_id=lsibd9 | /common?action=QueryThingModel&version=1&product_id=lsibd9 |
| 请求头 |  |  |  |  |
| URL参数 | product_id | string | 必填 | 产品id |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | object | object | 调用成功时，返回的业务数据 |
| 响应参数 | data.properties | array | array | 数组对象 属性功能点 |
| 响应参数 | p.functionMode | string | string | 功能点类型，定值'property' |
| 响应参数 | p.identifier | string | string | 属性唯一标识符（产品下唯一） |
| 响应参数 | p.name | string | string | 属性名称 |
| 响应参数 | p.desc | string | string | 属性描述 |
| 响应参数 | p.accessMode | string | string | "属性读写类型：只读（r）或读写（rw） |
| 响应参数 | p.functionType | string | string | 是否是标准功能点，自定义（u）/系统（s）/标准（st） |
| 响应参数 | p.dataType | object | object | 属性功能点数据 |
| 响应参数 | p.dataType.type | string | string | 属性类型: int32（32位整数）、int64（64位整数）、float（单精度浮点）、double（双精度浮点型）、string（字符串）、date（String类型UTC秒）、bool（true或false）、enum（int类型）、bitMap（位图）、date（int64类型UTC时间戳毫秒）、struct（结构体类型）、array（数组） |
| 响应参数 | p.dataType.specs | object | object | 属性功能点数据 |
| 响应参数 | data.events | array | array | 数组对象 事件功能点 |
| 响应参数 | e.functionMode | string | string | 功能点类型，定值'event' |
| 响应参数 | e.identifier | string | string | 事件唯一标识符 |
| 响应参数 | e.name | string | string | 事件名称 |
| 响应参数 | e.desc | string | string | 事件描述 |
| 响应参数 | e.type | string | string | 事件类型（info、alert、error） |
| 响应参数 | e.fuctionType | string | string | 是否是标准功能点，自定义（u）/标准（s） |
| 响应参数 | e.outputData | array | array | 参数 |
| 响应参数 | e.outputData.identifier | string | string | 参数唯一标识符 |
| 响应参数 | e.outputData.name | string | string | 参数名称 |
| 响应参数 | e.outputData.dataType | object | object | 参数数据 |
| 响应参数 | e.outputData.dataType.type | string | string | 属性类型: int32（32位整数）、int64（64位整数）、float（单精度浮点）、double（双精度浮点型）、string（字符串）、bool（true或false）、enum（int类型）、bitMap（位图）、date（int64类型UTC时间戳毫秒）、struct（结构体类型）、array（数组） |
| 响应参数 | e.outputData.dataType.specs | object | object | 功能点数据 |
| 响应参数 | services | array | array | 数组对象 服务功能点 |
| 响应参数 | s.functionMode | string | string | 功能点类型，定值'service' |
| 响应参数 | s.identifier | string | string | 服务唯一标识符（产品下唯一） |
| 响应参数 | s.name | string | string | 服务名称 |
| 响应参数 | s.desc | string | string | 服务描述 |
| 响应参数 | s.callType | string | string | 调用方式,同步(s)/异步(a) |
| 响应参数 | s.fuctionType | string | string | 功能点类型，自定义（u）/系统（s） |
| 响应参数 | s.input | array | array | 输入参数 |
| 响应参数 | s.input.identifier | string | string | 参数唯一标识符 |
| 响应参数 | s.input.name | string | string | 参数名称 |
| 响应参数 | s.input.dataType | object | object | 参数数据 |
| 响应参数 | s.input.dataType.type | string | string | 属性类型: int32（32位整数）、int64（64位整数）、float（单精度浮点）、double（双精度浮点型）、string（字符串）、bool（true或false）、enum（int类型）、bitMap（位图）、date（int64类型UTC时间戳毫秒）、struct（结构体类型）、array（数组） |
| 响应参数 | s.input.dataType.specs | object | object | 参数功能点数据 |
| 响应参数 | s.output | array | array | 输出参数 |
| 响应参数 | s.output.identifier | string | string | 参数唯一标识符 |
| 响应参数 | s.output.name | string | string | 参数名称 |
| 响应参数 | s.output.dataType | object | object | 参数数据 |
| 响应参数 | s.output.dataType.type | string | string | 属性类型: int32（32位整数）、int64（64位整数）、float（单精度浮点）、double（双精度浮点型）、string（字符串）、bool（true或false）、enum（int类型）、bitMap（位图）、date（int64类型UTC时间戳毫秒）、struct（结构体类型）、array（数组） |
| 响应参数 | s.output.dataType.specs | object | object | 参数功能点数据 |
| 请求示例 | GET /common?action=QueryThingModel&version=1&product_id=lsibd9 | GET /common?action=QueryThingModel&version=1&product_id=lsibd9 | GET /common?action=QueryThingModel&version=1&product_id=lsibd9 | GET /common?action=QueryThingModel&version=1&product_id=lsibd9 |
| 响应示例 | {     "data": {          "properties": [             {                 "name": "模式",                 "identifier": "model",                 "functionType": "u",                 "functionMode": "property",                 "desc": "",                 "accessMode": "rw",                 "dataType": {                     "type": "enum",                     "specs": {                         "1": "模式1",                         "2": "模式2"                     }                 }             }         ],         "events": [             {                 "name": "test",                 "identifier": "test",                 "functionType": "u",                 "functionMode": "event",                 "desc": null,                 "eventType": "info",                 "outputData": [                     {                         "dataType": {                             "type": "bool",                             "specs": {                                 "false": "关",                                 "true": "开"                             }                         },                         "name": "开关",                         "identifier": "switch"                     }                 ]             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "properties": [             {                 "name": "模式",                 "identifier": "model",                 "functionType": "u",                 "functionMode": "property",                 "desc": "",                 "accessMode": "rw",                 "dataType": {                     "type": "enum",                     "specs": {                         "1": "模式1",                         "2": "模式2"                     }                 }             }         ],         "events": [             {                 "name": "test",                 "identifier": "test",                 "functionType": "u",                 "functionMode": "event",                 "desc": null,                 "eventType": "info",                 "outputData": [                     {                         "dataType": {                             "type": "bool",                             "specs": {                                 "false": "关",                                 "true": "开"                             }                         },                         "name": "开关",                         "identifier": "switch"                     }                 ]             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "properties": [             {                 "name": "模式",                 "identifier": "model",                 "functionType": "u",                 "functionMode": "property",                 "desc": "",                 "accessMode": "rw",                 "dataType": {                     "type": "enum",                     "specs": {                         "1": "模式1",                         "2": "模式2"                     }                 }             }         ],         "events": [             {                 "name": "test",                 "identifier": "test",                 "functionType": "u",                 "functionMode": "event",                 "desc": null,                 "eventType": "info",                 "outputData": [                     {                         "dataType": {                             "type": "bool",                             "specs": {                                 "false": "关",                                 "true": "开"                             }                         },                         "name": "开关",                         "identifier": "switch"                     }                 ]             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "properties": [             {                 "name": "模式",                 "identifier": "model",                 "functionType": "u",                 "functionMode": "property",                 "desc": "",                 "accessMode": "rw",                 "dataType": {                     "type": "enum",                     "specs": {                         "1": "模式1",                         "2": "模式2"                     }                 }             }         ],         "events": [             {                 "name": "test",                 "identifier": "test",                 "functionType": "u",                 "functionMode": "event",                 "desc": null,                 "eventType": "info",                 "outputData": [                     {                         "dataType": {                             "type": "bool",                             "specs": {                                 "false": "关",                                 "true": "开"                             }                         },                         "name": "开关",                         "identifier": "switch"                     }                 ]             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



### 文件管理


#### 设备文件上传



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=CreateDeviceFile&version=1 | /common?action=CreateDeviceFile&version=1 | /common?action=CreateDeviceFile&version=1 | /common?action=CreateDeviceFile&version=1 |
| 请求头 | Content-type: multipart/form-data | Content-type: multipart/form-data | Content-type: multipart/form-data | Content-type: multipart/form-data |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体参数 | device_name | string | 必填 | 设备名称 ,参数需构造在同一个 form-data 中 |
| 请求体参数 | product_id | string | 必填 | 产品ID ,参数需构造在同一个 form-data 中 |
| 请求体参数 | file | file | 必填 | 上传的图片文件(目前支持JPG、JPEG、PNG、BMP、GIF、WEBP、TIFF、TXT) |
| 请求体参数 | md5 | string | 必填 | 文件的MD5 |
| 请求体参数 | size | number | 必填 | 文件大小(字节) |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.fid | string | string | 文件上传成功后返回的文件ID |
| 请求示例 | {   "device_name": "device_name",   "product_id": "qwdfbht",   "md5": "f55c2e86ab864b64a6d939fbe3a7d65f",   "size": 12546,   "file": file } | {   "device_name": "device_name",   "product_id": "qwdfbht",   "md5": "f55c2e86ab864b64a6d939fbe3a7d65f",   "size": 12546,   "file": file } | {   "device_name": "device_name",   "product_id": "qwdfbht",   "md5": "f55c2e86ab864b64a6d939fbe3a7d65f",   "size": 12546,   "file": file } | {   "device_name": "device_name",   "product_id": "qwdfbht",   "md5": "f55c2e86ab864b64a6d939fbe3a7d65f",   "size": 12546,   "file": file } |
| 响应示例 | {     "data": {          "fid": "434fa51a170942c8a291be1e4b229582"     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "fid": "434fa51a170942c8a291be1e4b229582"     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "fid": "434fa51a170942c8a291be1e4b229582"     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "fid": "434fa51a170942c8a291be1e4b229582"     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 查看下载设备文件接口



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=GetDeviceFile&version=1 | /common?action=GetDeviceFile&version=1 | /common?action=GetDeviceFile&version=1 | /common?action=GetDeviceFile&version=1 |
| 请求头 |  |  |  |  |
| URL参数 | id | string | 必填 | 文件id |
| 请求体 | 无 | 无 | 无 | 无 |
| 响应参数 | file | file | file | 需要下载的文件 |
| 请求示例 | GET /common?action=GetDeviceFile&version=1&id=43bb54ac673f48c88300fa6e6d3c9481 | GET /common?action=GetDeviceFile&version=1&id=43bb54ac673f48c88300fa6e6d3c9481 | GET /common?action=GetDeviceFile&version=1&id=43bb54ac673f48c88300fa6e6d3c9481 | GET /common?action=GetDeviceFile&version=1&id=43bb54ac673f48c88300fa6e6d3c9481 |
| 响应示例 | file | file | file | file |



#### 文件删除接口



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=DeleteDeviceFile&version=1 | /common?action=DeleteDeviceFile&version=1 | /common?action=DeleteDeviceFile&version=1 | /common?action=DeleteDeviceFile&version=1 |
| 请求头 | Content-type: multipart/form-data | Content-type: multipart/form-data | Content-type: multipart/form-data | Content-type: multipart/form-data |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体参数 | id | string | 必填 | 文件ID |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 请求示例 | {   id：43bb54ac673f48c88300fa6e6d3c9481 } | {   id：43bb54ac673f48c88300fa6e6d3c9481 } | {   id：43bb54ac673f48c88300fa6e6d3c9481 } | {   id：43bb54ac673f48c88300fa6e6d3c9481 } |
| 响应示例 | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "code": "0",      "msg": "success",      "data": null,      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "code": "0",      "msg": "success",      "data": null,      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "code": "0",      "msg": "success",      "data": null,      "success": true } | {     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "code": "0",      "msg": "success",      "data": null,      "success": true } |



### 分组管理


#### 分组创建



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=GroupCreate&version=1 | /common?action=GroupCreate&version=1 | /common?action=GroupCreate&version=1 | /common?action=GroupCreate&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | name | string | 必填 | 分组名称 |
| 请求体 参数 | desc | string | 可选 | 分组描述 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | -- | -- | 调用成功时，返回的业务数据 |
| 响应参数 | data.group_id | string | string | 分组ID |
| 请求示例 | {     "name": "黄河大道东",     "desc": "group 1" } | {     "name": "黄河大道东",     "desc": "group 1" } | {     "name": "黄河大道东",     "desc": "group 1" } | {     "name": "黄河大道东",     "desc": "group 1" } |
| 响应示例 | {     "data": {         "group_id": "uwYqby"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "uwYqby"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "uwYqby"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "uwYqby"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 分组删除



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=OuterDeleteGroup&version=1 | /common?action=OuterDeleteGroup&version=1 | /common?action=OuterDeleteGroup&version=1 | /common?action=OuterDeleteGroup&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | group_id | string | 必填 | 分组ID |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | -- | -- | 调用成功时，返回的业务数据 |
| 请求示例 | {     "group_id": "3UfAWD" } | {     "group_id": "3UfAWD" } | {     "group_id": "3UfAWD" } | {     "group_id": "3UfAWD" } |
| 响应示例 | {     "data": null,     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": null,     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": null,     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": null,     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 分组编辑



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=OuterUpdateGroup&version=1 | /common?action=OuterUpdateGroup&version=1 | /common?action=OuterUpdateGroup&version=1 | /common?action=OuterUpdateGroup&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | group_id | string | 必填 | 分组ID |
| 请求体 参数 | tag | object | 可选 | 标签信息 |
| 请求体 参数 | desc | string | 可选 | 分组描述 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | -- | -- | 调用成功时，返回的业务数据 |
| 响应参数 | data.group_id | string | string | 分组ID |
| 请求示例 | {     "group_id": "3UfAWD",     "tag": {"key11":"dkmclg"},    #标签的键值对     "desc": "描述" } | {     "group_id": "3UfAWD",     "tag": {"key11":"dkmclg"},    #标签的键值对     "desc": "描述" } | {     "group_id": "3UfAWD",     "tag": {"key11":"dkmclg"},    #标签的键值对     "desc": "描述" } | {     "group_id": "3UfAWD",     "tag": {"key11":"dkmclg"},    #标签的键值对     "desc": "描述" } |
| 响应示例 | {     "data": {         "group_id": "diVGB3"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "diVGB3"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "diVGB3"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "diVGB3"     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 分组列表



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=OuterGroupList&version=1 | /common?action=OuterGroupList&version=1 | /common?action=OuterGroupList&version=1 | /common?action=OuterGroupList&version=1 |
| 请求头 |  |  |  |  |
| URL参数 | name | string | 可选 | 分组名称 |
| URL参数 | key | string | 可选 | 标签key（key、value需成对出现，否则没有效果） |
| URL参数 | value | string | 可选 | 标签value（key、value 需成对出现，否则没有效果） |
| URL参数 | offset | string | 可选 | 请求记录起始位置，默认 0 |
| URL参数 | limit | string | 可选 | 每次请求记录数，默认10 |
| 请求体 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时, 返回业务数据 |
| 响应参数 | data.list | array | array | 分组信息集合，如下的l表示 list 数组的单个对象标识 |
| 响应参数 | l.name | string | string | 分组名称 |
| 响应参数 | l.group_id | string | string | 分组id |
| 响应参数 | l.key | string | string | 分组key |
| 响应参数 | l.tag | object | object | 标签信息,健值对 |
| 响应参数 | l.created_time | string | string | 创建时间 |
| 响应参数 | l.device_count | int | int | 设备数 |
| 响应参数 | data.meta | object | object | 分页信息 |
| 响应参数 | data.meta.limit | int | int | 每次请求记录数 |
| 响应参数 | data.meta.offset | int | int | 请求记录起始位置 |
| 响应参数 | data.meta.total | int | int | 记录总数 |
| 请求示例 | GET   /common?action=OuterGroupList&version=1 | GET   /common?action=OuterGroupList&version=1 | GET   /common?action=OuterGroupList&version=1 | GET   /common?action=OuterGroupList&version=1 |
| 响应示例 | {     "data": {         "list": [             {                 "name": "xq_group1",                 "group_id": "qf6nAD",                 "key": "ZDM0MzA4MTA3MjQ4NzdlYzZjOGJlYzU1YmUwZTNhMmY=",                 "tag": {                     "xq": "123"                 },                 "created_time":"2020-08-13T01:49:17694,                 "device_count": 2             }         ],         "meta": {             "limit": 10,             "offset": 0,             "total": 1         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "list": [             {                 "name": "xq_group1",                 "group_id": "qf6nAD",                 "key": "ZDM0MzA4MTA3MjQ4NzdlYzZjOGJlYzU1YmUwZTNhMmY=",                 "tag": {                     "xq": "123"                 },                 "created_time":"2020-08-13T01:49:17694,                 "device_count": 2             }         ],         "meta": {             "limit": 10,             "offset": 0,             "total": 1         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "list": [             {                 "name": "xq_group1",                 "group_id": "qf6nAD",                 "key": "ZDM0MzA4MTA3MjQ4NzdlYzZjOGJlYzU1YmUwZTNhMmY=",                 "tag": {                     "xq": "123"                 },                 "created_time":"2020-08-13T01:49:17694,                 "device_count": 2             }         ],         "meta": {             "limit": 10,             "offset": 0,             "total": 1         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "list": [             {                 "name": "xq_group1",                 "group_id": "qf6nAD",                 "key": "ZDM0MzA4MTA3MjQ4NzdlYzZjOGJlYzU1YmUwZTNhMmY=",                 "tag": {                     "xq": "123"                 },                 "created_time":"2020-08-13T01:49:17694,                 "device_count": 2             }         ],         "meta": {             "limit": 10,             "offset": 0,             "total": 1         }     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 分组详情



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=OuterGroupDetail&version=1 | /common?action=OuterGroupDetail&version=1 | /common?action=OuterGroupDetail&version=1 | /common?action=OuterGroupDetail&version=1 |
| 请求头 |  |  |  |  |
| URL参数 | group_id | string | 必填 | 分组ID |
| 请求体 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时, 返回业务数据 |
| 响应参数 | data.activate_count | string | string | 激活设备数 |
| 响应参数 | data.online_count | string | string | 在线设备数 |
| 响应参数 | data.name | string | string | 分组名称 |
| 响应参数 | data.group_id | string | string | 分组ID |
| 响应参数 | data.key | string | string | 分组key |
| 响应参数 | data.tag | object | object | 分组标签 |
| 响应参数 | data.desc | string | string | 分组描述 |
| 响应参数 | data.device_count | string | string | 设备数量 |
| 响应参数 | data.create_time | string | string | 创建时间 |
| 请求示例 | GET  /common?action=OuterGroupDetail&version=1 | GET  /common?action=OuterGroupDetail&version=1 | GET  /common?action=OuterGroupDetail&version=1 | GET  /common?action=OuterGroupDetail&version=1 |
| 响应示例 | {     "data": {          "activate_count": 0,         "online_count": 0,         "name": "xq_group1",         "group_id": "qf6nAD",         "key": "ZDM0MzA4MTA3MjQ4NzdlYzZjOGJlYzU1YmUwZTNhMmY=",         "tag": {             "xq": "123"         },         "desc": "123",	         "created_time": "2020-08-13T01:49:17.694Z",         "device_count": 2     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "activate_count": 0,         "online_count": 0,         "name": "xq_group1",         "group_id": "qf6nAD",         "key": "ZDM0MzA4MTA3MjQ4NzdlYzZjOGJlYzU1YmUwZTNhMmY=",         "tag": {             "xq": "123"         },         "desc": "123",	         "created_time": "2020-08-13T01:49:17.694Z",         "device_count": 2     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "activate_count": 0,         "online_count": 0,         "name": "xq_group1",         "group_id": "qf6nAD",         "key": "ZDM0MzA4MTA3MjQ4NzdlYzZjOGJlYzU1YmUwZTNhMmY=",         "tag": {             "xq": "123"         },         "desc": "123",	         "created_time": "2020-08-13T01:49:17.694Z",         "device_count": 2     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "activate_count": 0,         "online_count": 0,         "name": "xq_group1",         "group_id": "qf6nAD",         "key": "ZDM0MzA4MTA3MjQ4NzdlYzZjOGJlYzU1YmUwZTNhMmY=",         "tag": {             "xq": "123"         },         "desc": "123",	         "created_time": "2020-08-13T01:49:17.694Z",         "device_count": 2     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 分组设备添加



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=OuterAddGroupDevice&version=1 | /common?action=OuterAddGroupDevice&version=1 | /common?action=OuterAddGroupDevice&version=1 | /common?action=OuterAddGroupDevice&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | group_id | string | 必填 | 分组ID |
| 请求体 参数 | product_id | string | 必填 | 产品ID |
| 请求体 参数 | devices | arrary | 必填 | 需要添加的设备集合 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | -- | -- | 调用成功时，返回的业务数据 |
| 响应参数 | data.error_data | array | array | 添加失败的错误信息集合，如下的e表示 error_data 数组的单个对象标识 |
| 响应参数 | e. device_name | string | string | 添加失败的设备集合 |
| 响应参数 | e. cause | string | string | 添加失败原因 |
| 请求示例 | {     "group_id": "Z1Pdei",     "product_id": "XVlg5CCSSj",     "devices": ["dev1", "dev2"] } | {     "group_id": "Z1Pdei",     "product_id": "XVlg5CCSSj",     "devices": ["dev1", "dev2"] } | {     "group_id": "Z1Pdei",     "product_id": "XVlg5CCSSj",     "devices": ["dev1", "dev2"] } | {     "group_id": "Z1Pdei",     "product_id": "XVlg5CCSSj",     "devices": ["dev1", "dev2"] } |
| 响应示例 | {     "data": {         "group_id": "qf6nAD",         "devices": ["dev1", "dev2"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "qf6nAD",         "devices": ["dev1", "dev2"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "qf6nAD",         "devices": ["dev1", "dev2"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "qf6nAD",         "devices": ["dev1", "dev2"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 分组设备移除



| 方法 | POST | POST | POST | POST |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=OuterRemoveGroupDevice&version=1 | /common?action=OuterRemoveGroupDevice&version=1 | /common?action=OuterRemoveGroupDevice&version=1 | /common?action=OuterRemoveGroupDevice&version=1 |
| 请求头 | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json | Content-Type : application/json |
| URL参数 | 无 | 无 | 无 | 无 |
| 请求体 参数 | group_id | string | 必填 | 分组ID |
| 请求体 参数 | product_id | string | 必填 | 产品ID |
| 请求体 参数 | devices | arrary | 必填 | 需要移除的设备集合 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | -- | -- | 调用成功时，返回的业务数据 |
| 响应参数 | data.error_data | array | array | 移除失败的错误信息集合，如下的e表示 error_data 数组的单个对象标识 |
| 响应参数 | e. device_name | string | string | 移除失败的设备集合 |
| 响应参数 | e. cause | string | string | 移除失败原因 |
| 请求示例 | {     "group_id": "Z1Pdei",     "product_id": "XVlg5CCSSj",     "devices": ["dev1", "dev2"] } | {     "group_id": "Z1Pdei",     "product_id": "XVlg5CCSSj",     "devices": ["dev1", "dev2"] } | {     "group_id": "Z1Pdei",     "product_id": "XVlg5CCSSj",     "devices": ["dev1", "dev2"] } | {     "group_id": "Z1Pdei",     "product_id": "XVlg5CCSSj",     "devices": ["dev1", "dev2"] } |
| 响应示例 | {     "data": {         "group_id": "qf6nAD",         "devices": ["dev1", "dev2"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "qf6nAD",         "devices": ["dev1", "dev2"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "qf6nAD",         "devices": ["dev1", "dev2"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {         "group_id": "qf6nAD",         "devices": ["dev1", "dev2"]     },     "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



### 用户管理


#### 用户下产品数量统计



| 方法 | GET | GET | GET |
| --- | --- | --- | --- |
| 路径URI | /common?action=ProductStatistics&version=1 | /common?action=ProductStatistics&version=1 | /common?action=ProductStatistics&version=1 |
| 请求头 |  |  |  |
| URL参数 | 无 | 无 | 无 |
| 请求体参数 | 无 | 无 | 无 |
| 响应参数 | code | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | 接口是否调用成功 |
| 响应参数 | data | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.product_aggregate.product_count | number | 产品数量 |
| 响应参数 | data.product_aggregate.ind_agg | array | 数组对象，行业类型统计，如下的ind表示ind_agg数组的单个对象标识 |
| 响应参数 | ind._id | string | 行业ID（自动生成） |
| 响应参数 | ind.count | string | 行业类别下产品数量 |
| 响应参数 | ind.name | string | 行业名称 |
| 响应参数 | data.product_aggregate.pt_agg | array | 数组对象，协议类型统计，如下的pt表示pt_agg数组的单个对象标识 |
| 响应参数 | pt._id | string | 协议ID（自动生成） |
| 响应参数 | pt.count | string | 同一协议下产品数量 |
| 响应参数 | pt.name | string | 协议名称 |
| 响应参数 | data.product_aggregate.net_agg | array | 数组对象，联网类型统计，如下的net表示net_agg数组的单个对象标识 |
| 响应参数 | net._id | string | 联网类型ID（自动生成） |
| 响应参数 | net.count | string | 同一联网类型下产品数量 |
| 响应参数 | net.name | string | 联网类型名称 |
| 响应参数 | data.product_aggregate.model_agg | array | 数组对象，物模型类型统计，如下的model表示model_agg数组的单个对象标识 |
| 响应参数 | model._id | string | 物模型类型ID（自动生成） |
| 响应参数 | model.count | string | 物模型类型下产品数量 |
| 响应参数 | model.name | string | 物模型类型名称 |
| 请求示例 | GET /common?action=ProductStatistics&version=1 | GET /common?action=ProductStatistics&version=1 | GET /common?action=ProductStatistics&version=1 |
| 响应示例 | {     "data": {            "product_aggregate":{             "ind_agg":[ // 行业类别                 {                     "_id":"1",                     "count":7,                     "name":"智慧城市"                 }             ],             "pt_agg":[ // 协议类型                 {                     "_id":'sub',                     "count":1,                     "name":‘网关子设备’                 },                 {                     "_id":4,                     "count":2,                     "name":'Lwm2m'                 },                 {                     "_id":2,                     "count":4,                     "name":"MQTT"                 }             ],             "net_agg":[ // 联网型类型                 {                     "_id":"1",                     "count":0,                     "name":"其他"                 },                 {                     "_id":"2",                     "count":0,                     "name":"蜂窝"                 },                 {                     "_id":"3",                     "count":5,                     "name":"wifi"                 },                 {                     "_id":"4",                     "count":0,                     "name":"以太网"                 },                 {                     "_id":"5",                     "count":1,                     "name":"NB"                 }             ],             "model_agg":[ // 物模型类型                 {                     "_id":"1",                     "count":2,                     "name":"标准"                 },                 {                     "_id":"2",                     "count":5,                     "name":"自定义"                 }             ]         },         "product_count":7 // 总数 } }          "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {            "product_aggregate":{             "ind_agg":[ // 行业类别                 {                     "_id":"1",                     "count":7,                     "name":"智慧城市"                 }             ],             "pt_agg":[ // 协议类型                 {                     "_id":'sub',                     "count":1,                     "name":‘网关子设备’                 },                 {                     "_id":4,                     "count":2,                     "name":'Lwm2m'                 },                 {                     "_id":2,                     "count":4,                     "name":"MQTT"                 }             ],             "net_agg":[ // 联网型类型                 {                     "_id":"1",                     "count":0,                     "name":"其他"                 },                 {                     "_id":"2",                     "count":0,                     "name":"蜂窝"                 },                 {                     "_id":"3",                     "count":5,                     "name":"wifi"                 },                 {                     "_id":"4",                     "count":0,                     "name":"以太网"                 },                 {                     "_id":"5",                     "count":1,                     "name":"NB"                 }             ],             "model_agg":[ // 物模型类型                 {                     "_id":"1",                     "count":2,                     "name":"标准"                 },                 {                     "_id":"2",                     "count":5,                     "name":"自定义"                 }             ]         },         "product_count":7 // 总数 } }          "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {            "product_aggregate":{             "ind_agg":[ // 行业类别                 {                     "_id":"1",                     "count":7,                     "name":"智慧城市"                 }             ],             "pt_agg":[ // 协议类型                 {                     "_id":'sub',                     "count":1,                     "name":‘网关子设备’                 },                 {                     "_id":4,                     "count":2,                     "name":'Lwm2m'                 },                 {                     "_id":2,                     "count":4,                     "name":"MQTT"                 }             ],             "net_agg":[ // 联网型类型                 {                     "_id":"1",                     "count":0,                     "name":"其他"                 },                 {                     "_id":"2",                     "count":0,                     "name":"蜂窝"                 },                 {                     "_id":"3",                     "count":5,                     "name":"wifi"                 },                 {                     "_id":"4",                     "count":0,                     "name":"以太网"                 },                 {                     "_id":"5",                     "count":1,                     "name":"NB"                 }             ],             "model_agg":[ // 物模型类型                 {                     "_id":"1",                     "count":2,                     "name":"标准"                 },                 {                     "_id":"2",                     "count":5,                     "name":"自定义"                 }             ]         },         "product_count":7 // 总数 } }          "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 账户下文件列表查询



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=GetDeviceFilesList&version=1 | /common?action=GetDeviceFilesList&version=1 | /common?action=GetDeviceFilesList&version=1 | /common?action=GetDeviceFilesList&version=1 |
| 请求头 |  |  |  |  |
| URL参数 | offset | number | 可选 | 请求起始位置，默认0 |
| URL参数 | limit | number | 可选 | 每次请求记录数，默认10 |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | 调用失败时，返回的错误码 | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | 调用失败时，返回的错误信息 | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | 调用API时生成的请求标识 | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | 接口是否调用成功 | 接口是否调用成功 |
| 响应参数 | data | － | 调用成功时，返回的业务数据 | 调用成功时，返回的业务数据 |
| 响应参数 | data.meta.total | number | 文件数量 | 文件数量 |
| 响应参数 | data.meta.limit | number | 每次请求的数据长度 | 每次请求的数据长度 |
| 响应参数 | data.meta.offset | number | 偏移量 | 偏移量 |
| 响应参数 | data.list.fid | string | 文件ID | 文件ID |
| 响应参数 | data.list.name | string | 文件名称 | 文件名称 |
| 响应参数 | data.list.file_size | number | 文件大小 | 文件大小 |
| 响应参数 | data.list.ct | string | 文件创建时间 | 文件创建时间 |
| 响应参数 | data.list.device_name | string | 文件所属设备名称 | 文件所属设备名称 |
| 响应参数 | data.list.product_id | string | 文件所属设备的产品ID | 文件所属设备的产品ID |
| 请求示例 | GET /common?action=GetDeviceFilesList&version=1 | GET /common?action=GetDeviceFilesList&version=1 | GET /common?action=GetDeviceFilesList&version=1 | GET /common?action=GetDeviceFilesList&version=1 |
| 响应示例 | {     "data": {          "meta": {             "limit": 10,             "offset": 0,             "total": 1         },         "list": [             {                 "fid": "98cfa6be79574f7eab98eb7b5222911a",                 "name": "28fpf.png",                 "file_size": 138683,                 "ct": "2020-12-16T09:30:18.419Z",                 "device_name": "ap-test-008",                 "product_id": "Bs1f6s5bhKP7rmfO"             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "meta": {             "limit": 10,             "offset": 0,             "total": 1         },         "list": [             {                 "fid": "98cfa6be79574f7eab98eb7b5222911a",                 "name": "28fpf.png",                 "file_size": 138683,                 "ct": "2020-12-16T09:30:18.419Z",                 "device_name": "ap-test-008",                 "product_id": "Bs1f6s5bhKP7rmfO"             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "meta": {             "limit": 10,             "offset": 0,             "total": 1         },         "list": [             {                 "fid": "98cfa6be79574f7eab98eb7b5222911a",                 "name": "28fpf.png",                 "file_size": 138683,                 "ct": "2020-12-16T09:30:18.419Z",                 "device_name": "ap-test-008",                 "product_id": "Bs1f6s5bhKP7rmfO"             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "meta": {             "limit": 10,             "offset": 0,             "total": 1         },         "list": [             {                 "fid": "98cfa6be79574f7eab98eb7b5222911a",                 "name": "28fpf.png",                 "file_size": 138683,                 "ct": "2020-12-16T09:30:18.419Z",                 "device_name": "ap-test-008",                 "product_id": "Bs1f6s5bhKP7rmfO"             }         ]     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 用户文件存储空间查询



| 方法 | GET | GET | GET |
| --- | --- | --- | --- |
| 路径URI | /common?action=GetDeviceFileSpace&version=1 | /common?action=GetDeviceFileSpace&version=1 | /common?action=GetDeviceFileSpace&version=1 |
| 请求头 |  |  |  |
| URL参数 | 无 | 无 | 无 |
| 请求体参数 | 无 | 无 | 无 |
| 响应参数 | code | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | 接口是否调用成功 |
| 响应参数 | data | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.useSize | number | 用户已使用的空间 |
| 响应参数 | data.hasSize | number | 用户剩余空间 |
| 响应参数 | data.totalSize | number | 用户分配的总空间 |
| 请求示例 | GET /common?action=GetDeviceFileSpace&version=1 | GET /common?action=GetDeviceFileSpace&version=1 | GET /common?action=GetDeviceFileSpace&version=1 |
| 响应示例 | {     "data": {          "useSize": 138683,         "hasSize": 1073603141,         "totalSize": 1073741824     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "useSize": 138683,         "hasSize": 1073603141,         "totalSize": 1073741824     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "useSize": 138683,         "hasSize": 1073603141,         "totalSize": 1073741824     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |



#### 用户设备文件数量查询



| 方法 | GET | GET | GET | GET |
| --- | --- | --- | --- | --- |
| 路径URI | /common?action=GetDeviceFileCount&version=1&device_name=ap-test-008&product_id=Bs1f6s5bhKP7rmfO | /common?action=GetDeviceFileCount&version=1&device_name=ap-test-008&product_id=Bs1f6s5bhKP7rmfO | /common?action=GetDeviceFileCount&version=1&device_name=ap-test-008&product_id=Bs1f6s5bhKP7rmfO | /common?action=GetDeviceFileCount&version=1&device_name=ap-test-008&product_id=Bs1f6s5bhKP7rmfO |
| 请求头 |  |  |  |  |
| URL请求参数 | product_id | string | 必填 | 产品id |
| URL请求参数 | device_name | string | 必填 | 设备名称 |
| 请求体参数 | 无 | 无 | 无 | 无 |
| 响应参数 | code | string | string | 调用失败时，返回的错误码 |
| 响应参数 | msg | string | string | 调用失败时，返回的错误信息 |
| 响应参数 | requestId | string | string | 调用API时生成的请求标识 |
| 响应参数 | success | boolean | boolean | 接口是否调用成功 |
| 响应参数 | data | － | － | 调用成功时，返回的业务数据 |
| 响应参数 | data.upperLimit | number | number | 设备允许的最大文件数量 |
| 响应参数 | data.filesTotal | number | number | 设备已存在的文件数量 |
| 请求示例 | GET /common?action=GetDeviceFileCount&version=1&device_name=ap-test-008&product_id=Bs1f6s5bhKP7rmfO | GET /common?action=GetDeviceFileCount&version=1&device_name=ap-test-008&product_id=Bs1f6s5bhKP7rmfO | GET /common?action=GetDeviceFileCount&version=1&device_name=ap-test-008&product_id=Bs1f6s5bhKP7rmfO | GET /common?action=GetDeviceFileCount&version=1&device_name=ap-test-008&product_id=Bs1f6s5bhKP7rmfO |
| 响应示例 | {     "data": {          "upperLimit": 10,         "filesTotal": 1     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "upperLimit": 10,         "filesTotal": 1     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "upperLimit": 10,         "filesTotal": 1     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } | {     "data": {          "upperLimit": 10,         "filesTotal": 1     }      "requestId": "a25087f46df04b69b29e90ef0acfd115",      "success": true } |


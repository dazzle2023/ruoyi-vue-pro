# OneNET 城市物联网平台 V3.0 公开接口文档
> 本文档由 PDF 自动转换生成
---

## 1. 公开 API
使用说明
1.1.
1.1.1. 公共请求说明
API接口请求参数包括公共参数和自定义业务参数两部分。公共请求参数是
调用每个API时都需要携带的请求参数, 包括服务命名空间、接口名称、版本信
息。自定义业务参数由各接口定义，根据调用方法不同，需要将参数携带至请求
路径或者请求体中。API接口公共参数调用如下所示：
https(http)://xxxx.com/{namespace}?action=xxxx&version=1
参数说明:
序 参数 类型 是否必 描述
号 选
1 namespace string 是 API接口类别, 目前支持common 设
备管理类
2 action string 是 API接口名称
3 version string 是 API版本号, 目前所有API接口版本均
为1
1.1.2. 公共响应说明
成功响应：
{
"requestId":"8906582E6722409AA6C40E7863B733A5",
"success":true,
"data":{
status:1
}
}
失败响应：

{
"requestId":"8906582E6722409AA6C40E7863B733A5",
"code": "iot.application.deviceNotFound",
"msg":"devicedoesnot exist",
"success":false
}
参数说明:
序号 参数 类型 描述
1 requestI string 请求ID，调用API 时由平台生成唯一请求标识
d
2 code string 调用失败时，返回的错误码
3 msg string 调用失败时，返回的错误信息
4 success boolea 接口是否调用成功
n
5 data object 调用成功时，返回的业务数据（接口无业务数
据返回，值为null）
安全鉴权
1.2.
平台需要对 API 调用方进行资源权限校验，使用 API 时，需要在请求
Header 中携带统一的安全鉴权信息。
(1)安全鉴权机制
安全鉴权 authorization 由多个参数构成，每个参数均采用 key = value 的
形式表示，并用&作为分隔符：
authorization:
version=2020-05-29&res=userid%2F38055&et=1623982416&method=sha1&sign=S0
4GcvafYIjtAMHJthkGPevbNwE%3D
参数说明：

序 参数 类型 说明 示例
号
1 version string 签名算法版 目前仅支持 2020-05-29
本
2 res string 访问资源信 支持主用户访问方式：
息 1）主用户访问res为：userid/{userid},
userid为平台用户id，参数在个人「账
号信息」中查看
3 et string 访问过期时 10位时间戳，1537255523 表示：北
间 京时间 2018-09-1815:25:23
4 method string 签名方法 目前支持md5、sha1、sha256
5 sign string 签名结果字 version、res、et、method参数计算生
符串 成
其中 sign 的生成算法为：
sign=base64(hmac_<method>(base64decode(accessKey),utf-8(StringForSignature)))
laccessKey为平台分配的访问密钥（用户访问权限页面查看），如果访问资源以
主用户形式访问, 使用主用户的accessKey，如果访问资源以项目群组方式访问，
使用群组的accessKey，且只能对群组内设备进行操作。
laccessKey参与计算前应先进行base64decode操作
l用于计算签名的字符串 StringForSignature 按照et、method、resource、version的
顺序，以"\n"作为分隔符进行排列，如下所示：
StringForSignature=et +"\n"+method +"\n"+ res+"\n" +version
(2)参数编码
authorization中key=value 的形式的value 部分需要经过URL编码，需要进行编码
的特殊符号如下：

序号 符号 编码
1 + %2B
2 空格 %20
3 / %2F
4 ? %3F
5 % %25
6 # %23
7 & %26
8 = %3D
(3)authorization生成示例
nodejs代码示例
Ø
'usestrict';
constcrypto=require('crypto');
/**
*authorization生成函数
*
*@param{String}method -hashmethod
*@param{String}res -resource
*@param{String}accessKey -accesskey
*@param{Number} et -effectivetime
*@return{String}-authorization
*/
functiongenerateAuthorization(method,res,accessKey,et){
constversion= '2020-05-29';
constet= Math.ceil((Date.now()+ et)/1000);//token 有效时间
constbase64Key= Buffer.from(accessKey,'base64'); //accessKeybase64编码

constStringForSignature=et +'\n'+method +'\n'+res+'\n'+ version;
constsign=encodeURIComponent(crypto.createHmac(method,
base64Key).update(StringForSignature).digest('base64'));
constencodeRes=encodeURIComponent(res);
return
`version=${version}&res=${encodeRes}&et=${et}&method=${method}&sign=${sign}`;
}
constmethod= 'sha1';
constaccessKey=
'mjgvkTCYTBF6DguxMmm+aV9EkDp2CYfL5jzRTph5Th6KhU8gqZz/cBivPTA7tfY5';
constres ='userid/130037';
constet= 365*24*3600*1000;// 有效时间 - 365天
constauthorization= generateAuthorization(method,res,accessKey,et);
python 代码示例
Ø
importbase64
importhmac
importtime
fromurllib.parseimport quote
deftoken(user_id,access_key):
version='2020-05-29'
res= 'userid/%s'%user_id
# 用户自定义token 过期时间
et=str(int(time.time())+ 3600)

# 签名方法，支持md5、sha1、sha256
method= 'sha1'
# 对access_key 进行decode
key= base64.b64decode(access_key)
# 计算sign
org=et +'\n'+method +'\n'+res +'\n'+ version
sign_b=hmac.new(key=key,msg=org.encode(), digestmod=method)
sign=base64.b64encode(sign_b.digest()).decode()
#value 部分进行url编码，method/res/version值较为简单无需编码
sign=quote(sign,safe='')
res= quote(res,safe='')
#token参数拼接
token= 'version=%s&res=%s&et=%s&method=%s&sign=%s'%(version, res,
et,method, sign)
returntoken
if__name__=='__main__':
user_id='37715'
access_key=
'mjgvkTCYTBF6DguxMmm+aV9EkDp2CYfL5jzRTph5Th6KhU8gqZz/cBivPTA7tfY5'
print(token(user_id,access_key))
Java 代码示例
Ø
importjavax.crypto.Mac;
importjavax.crypto.spec.SecretKeySpec;
importjava.io.UnsupportedEncodingException;

importjava.net.URLEncoder;
importjava.security.InvalidKeyException;
importjava.security.NoSuchAlgorithmException;
importjava.util.Base64;
publicclassToken{
publicstaticString assembleToken(Stringversion,StringresourceName,
StringexpirationTime, StringsignatureMethod,StringaccessKey)
throwsUnsupportedEncodingException,
NoSuchAlgorithmException,InvalidKeyException{
StringBuildersb=new StringBuilder();
Stringres= URLEncoder.encode(resourceName,"UTF-8");
Stringsig= URLEncoder.encode(generatorSignature(version,
resourceName,expirationTime, accessKey,signatureMethod),"UTF-8");
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
returnsb.toString();
}
publicstaticString generatorSignature(Stringversion, StringresourceName,
StringexpirationTime, StringaccessKey,StringsignatureMethod)

throwsNoSuchAlgorithmException,InvalidKeyException{
StringencryptText=expirationTime +"\n" +signatureMethod+"\n"+
resourceName+ "\n"+version;
Stringsignature;
byte[]bytes=HmacEncrypt(encryptText,accessKey,signatureMethod);
signature=Base64.getEncoder().encodeToString(bytes);
returnsignature;
}
publicstaticbyte[] HmacEncrypt(Stringdata, Stringkey,String
signatureMethod)
throwsNoSuchAlgorithmException,InvalidKeyException{
//根据给定的字节数组构造一个密钥,第二参数指定一个密钥算法
的名称
SecretKeySpecsigninKey =null;
signinKey= newSecretKeySpec(Base64.getDecoder().decode(key),
"Hmac"+ signatureMethod.toUpperCase());
//生成一个指定 Mac 算法 的 Mac 对象
Macmac=null;
mac=Mac.getInstance("Hmac"+signatureMethod.toUpperCase());
//用给定密钥初始化 Mac 对象
mac.init(signinKey);
//完成 Mac 操作
returnmac.doFinal(data.getBytes());
}
publicenum SignatureMethod{

SHA1,MD5,SHA256;
}
publicstaticvoid main(String[]args)throws UnsupportedEncodingException,
NoSuchAlgorithmException,InvalidKeyException{
Stringversion ="2020-05-29";
StringresourceName ="userid/12321";
StringexpirationTime =System.currentTimeMillis()/1000+100*24*
60*60+"";
StringsignatureMethod=SignatureMethod.SHA1.name().toLowerCase();
StringaccessKey=
"KuF3NT/jUBJ62LNBB/A8XZA9CqS3Cu79B/ABmfA1UCw=";
Stringtoken= assembleToken(version,resourceName, expirationTime,
signatureMethod,accessKey);
System.out.println("Authorization:"+token);
}
}
go代码示例
Ø
func (s*SignService) GenerateSign(params_mapmap[string]string,access_keystring)
(string,error){
signature_str:=params_map["et"]+ "\n"+ params_map["method"]+"\n"+
params_map["res"]+"\n"+ params_map["version"]
hmac_str:=""
switchstrings.ToLower(params_map["method"]) {
case"sha1":
hmac_str=tools.HmacSha1(signature_str,
tools.Base64Decode(access_key))
case"sha256":
hmac_str=tools.HmacSha256(signature_str,
tools.Base64Decode(access_key))
case"md5":

hmac_str=tools.HmacMd5(signature_str,
tools.Base64Decode(access_key))
default:
return"",errors.New("签名参数错误！")
}
sign:=tools.Base64Encode(hmac_str)
returnsign,nil
}
funcBase64Encode(messagestring)string{
returnbase64.StdEncoding.EncodeToString([]byte(message))
}
funcBase64Decode(message string)string {
decode_str,err:= base64.StdEncoding.DecodeString(message)
iferr!=nil{
return""
}
returnstring(decode_str)
}
funcHmacSha256(datastring, secretstring)string{
h:=hmac.New(sha256.New,[]byte(secret))
h.Write([]byte(data))
returnstring(h.Sum(nil))
//returnhex.EncodeToString(h.Sum(nil))
}
funcHmacMd5(datastring,secret string)string{

h:=hmac.New(md5.New,[]byte(secret))
h.Write([]byte(data))
returnstring(h.Sum(nil))
//returnhex.EncodeToString(h.Sum(nil))
}
funcHmacSha1(datastring, secretstring)string{
h:=hmac.New(sha1.New,[]byte(secret))
h.Write([]byte(data))
returnstring(h.Sum(nil))
//returnhex.EncodeToString(h.Sum(nil)) //不需以十六进制字符串输出
}
php代码示例
Ø
classSafetyAuth
{
private $_version= '2020-05-29';//版本
private $_method='sha1';//加密方法，还可以用md5、sha256
private $_access_key;//访问密钥
private $_res;//资源参数
private $_et;//到期时间戳
private $_expiration;//有效期，有效时间
publicfunction__construct($access_key,$expiration,$res){
$this->_expiration= $expiration;
$this->_access_key=$access_key;
$this->_res=$res;
}
//生成sign
privatefunction_makeSign(){

date_default_timezone_set('PRC');
$this->_et=time()+$this->_expiration;
$string_for_signature= $this->_et."\n" .$this->_method."\n".
$this->_res ."\n".$this->_version;
$b64_decode_acckey=base64_decode($this->_access_key);
$hmac_key= hash_hmac($this->_method,
$this->_strToUtf8($string_for_signature),$b64_decode_acckey, true);
$sign=base64_encode($hmac_key);
return$sign;
}
private function_strToUtf8($str){
$encode=mb_detect_encoding($str,
array("ASCII",'UTF-8',"GB2312","GBK",'BIG5'));
if($encode=='UTF-8'){
return$str;
}else{
returnmb_convert_encoding($str, 'UTF-8',$encode);
}
}
//生成token
public functionmakeToken(){
$sign=$this->_makeSign();
$token=
sprintf("version=2020-05-29&res=%s&et=%s&method=sha1&sign=%s",
urlencode($this->_res),$this->_et,urlencode($sign));
return$token;
}
}

错误码
1.3.
本文档列举API调用失败时，返回的错误码。出现缺少请求参数、不合法的
请求参数等错误时，请参见具体API描述进行修改。
资源权限相关错误码：
错误码 描述
authPermissionDeny 鉴权失败
resourePermissionDeny 无资源访问权限
parameterRequired 缺少请求参数
parameterMissing 缺少请求参数
invalidParameter 不合法的请求参数
产品相关错误码：
错误码 描述
productNotFound 产品不存在
productHasNoDevice 产品未创建设备
设备相关错误码：
错误码 描述
deviceNotFound 设备不存在
setPropertyFailed 设备属性设置失败
setDesiredPeropertyFailed 设备属性期望设置失败
queryDesiredProperyFailed 设备属性期望查询失败
getTmProperties 设备属性获取失败
callTmService 设备服务调用失败
deleteDesiredPeropertyFailed 设备属性期望删除失败

queryCurrentData 设备最新数据查询失败
queryPropertyHistoryData 设备属性历史数据查询失败
queryEventHistoryData 设备事件历史数据查询失败
queryOperationLog 设备操作记录查询失败
1.4. API 列表
1.4.1. 产品管理
1.4.1.1. 产品详情
方法 GET
路径 /common?action=ProductDetail&version=1&product_id=10132
URI
请求头
URL参 product_id string 必填 产品id
数
请求体 无
参数
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
响应参
data － 调用成功时，返回的业务数据
数
data.device_numb number 设备数量
er
data.product_id string 产品ID
data.name string 产品名称

data.desc string 产品描述
data.network string 联网方式
data.category string 产品所属分类ID
data.category_nam string 产品所属分类名称
e
data.protocol number 协议类型 1-泛协议 2-MQTT
3-CoAP
data.create_time string 创建时间
data.ind_title string 产品行业名称
data.prod_ind string 产品行业编码
data.prod_chain array 产品行业编码层级关系
data.uid string 产品用户ID
data.sec_key string 产品权限key
data.template_id string 模板id
data.template_info array 模板信息
请求示 GET/common?action=ProductDetail&version=1&product_id=10132
例
{
"data": {
"device_number":0,
"protocol":2,
响应示
"created_time":"2021-12-06T08:28:56.762Z",
例
"product_id":"wjrJjSRtsG",
"network":"1",
"category":"138",
"ind_title":"智慧城市",
"prod_ind":"1",

"uid":37782,
"sec_key":"vC3eX2gr8mapsNZ1zYVmtsFRMYaX953GbJiKlcAQTp4=",
"desc":"",
"name":"物模型",
"template_id": "6406f2ee9641f20035c53b12",
"template_info":[]
},
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.1.2. 产品列表
方法 GET
路径URI /common?action=ProductList&version=1
请求头
name string 可选 产品名称
manufacturer string 可选 厂商名称
protocol string 可选 接入协议，可选['1','2', '3','4','5', '6',
URL参
'7', '8','9','0']
数
industry string 可选 行业类型编码
offset string 可选 请求起始位置，默认0
limit string 可选 每次请求记录数，默认10
请求体 无
参数
code string 调用失败时，返回的错误码
响应参
msg string 调用失败时，返回的错误信息
数
requestId string 调用API时生成的请求标识

success boolean 接口是否调用成功
data － 调用成功时, 返回业务数据
data.list array 产品信息集合，如下的l表示 list 数
组的单个对象标识
l.total number 设备数量
l.desc string 描述
l.protocol number 协议 1-泛协议 2-MQTT3-CoAP
l.created_time string 创建时间
l.product_id string 产品ID
l.network string 联网模式 1-其他 2-蜂窝 3-wifi
4-以太网
l.ind_title string 产品行业名称
l.prod_ind string 产品行业编码
l.uid string 产品用户ID
l.sec_key string 产品权限KEY
l.name string 产品名称
l.manufacturer string 厂商名称
l.template_id string 模板id
l.prod_chain array 产品行业编码层级关系
l.category array 分类ID
l.category_nam string 分类名称
e
data.meta object 分页信息
data.meta.limit number 每次请求记录数
data.meta.offse number 请求记录起始位置
t

data.meta.total number 条数
请求示 GET/common?action=ProductList&version=1&product_id=wA10WBynvt
例
{
"data":{
"list":[
"total":2,
"protocol":4,
"created_time":"2021-08-31T08:00:12.846Z",
"product_id":"wA10WBynvt",
"network":"3",
"category":["66006c672de43d02590b098b"],
"ind_title":"智慧城市",
"prod_ind":"1",
"prod_chain":["3","9"],
响应示
"uid":5,
例
"template_id":"6687c206537561748c69f470",
"sec_key":"RJKrcCGT22DYGSQ4KVXslu/Jnh3bezHzvhqCTFMk05Q=",
"desc":"",
"name":"qwe123",
"manufacturer":"S1234567890",
"category_name":"智能后视镜"
],
"meta":{
"total":1,
"limit":10,
"offset":0
}

},
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.1.3. 产品设备列表
方法 GET
路径URI /common?action=DeviceList&version=1
请求头
name string 可选 设备名称
product_id string 可选 产品ID
URL参 status string 可选 设备状态，可选['1'未激活,'2'在线,'3'
数 离线]
offset string 可选 请求起始位置，默认0
limit string 可选 每次请求记录数，默认10
请求体 无
参数
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
响应参
data － 调用成功时, 返回业务数据
数
data.list array 产品信息集合，如下的l 表示 list 数
组的单个对象标识
l.product_id string 产品ID
l.name string 设备名称

l.node_type number 节点类型1：直连设备，2：网关设
备，3：网关子设备
l.status number 设备状态1：未激活，2：在线，3：
离线 【默认为未激活】
l.last_time string 设备最后一次在线时间
l.created_time string 创建时间
l.from string 设备来源(1:自主创建，2:他人转移)
l.lon string 经度
l.lat string 纬度
l.idid string 设备ID
l. string 产品名称
product_name
l.scene array 场景id
data.meta object 分页信息
data.meta.limit number 每次请求记录数
data.meta.offse number 请求记录起始位置
t
data.meta.total number 条数
请求示 GET/common?action=DeviceList&version=1
例
{
"data":{
响应示 "list":[
例 {
"pid":"7ubgKi1vhm",
"name":"400A002090011001",
"ct":"2021-11-30T08:22:53.519Z",

"node_type":1,
"status":3,
"last_time":"2021-12-10T10:19:33.327Z",
"from":1,
"lon":"",
"lat":"",
"idid":"10015446",
"product_id":"7ubgKi1vhm",
"created_time":"2021-11-30T08:22:53.519Z",
"id":10015446,
"product_name":"水电费",
"scene":["a25087f46df040ef0acfd115"]
}
],
"meta":{
"total":1,
"limit":10,
"offset":0
}
},
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.1.4. 产品设备数量统计
方法 GET
路径URI /common?action=ProductDeviceStatistics&version=1
请求头
URL参数 product_id string 必填 产品id

请求体参 无
数
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data － 调用成功时，返回的业务数据
响应参数
data.unactiv number 未激活设备数
e
data.online number 在线设备数
data.offline number 离线设备数
data.total number 总的设备数
GET
请求示例 /common?action=ProductDeviceStatistics&version=1&product_id=7ubgK
i1vhm
{
"data": {
"unactive":6,// 未激活数
"online":0,// 在线数
响应示例 "offline":8, // 离线数
"total":14// 总数
}
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}

1.4.2. 设备管理
1.4.2.1. 设备创建
方法 POST
路径 /common?action=CreateDevice&version=1
URI
请求头 Content-Type :application/json
URL参 无
数
device_name string 必填 设备名称
product_id string 必填 产品ID
imei string 可选 NB设备imei，15个数字组成
(LwM2M 的电子串号，设备所属产品为
协议时必 LwM2M 时，为必填
填)
imsi string 可选 NB设备imsi，不超过15个的
数字，设备所属产品为LwM2M
时，为必填
psk string 可选 NB设备所需属性，若创建未
请求体
填则平台随机生成，8-16 位数
参数
字字母组合
template_field object 可选 如产品有选择设备档案模版，
根据所选模版构造的json对象
auth_code string 可选 NB设备鉴权码，1-16 位数字
字母组合
desc string 可选 设备描述
tag object 可选 设备标签
scene string 必填 场景_id
supplier numbe 必填 供应商id

r
template_field object 可选 设备档案数据
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data ―― 调用成功返回业务数据
data.name string 设备名称
data.node_type string 节点类型 1-直连设备
data.desc string 设备描述
data.sec_key string 设备密钥
data.protocol int 协议 1-泛协议 2-MQTT
3-CoAP
响应参
数 data.created_tim string 创建时间
e
data.imei string NB设备imei，15个数字组成
的电子串号
data.imsi string NB设备imsi，不超过15个的
数字
data.auth_code string NB设备鉴权码
data.psk string NB设备所需属性
data.tag object 设备标签
data.template_fie object 设备档案数据
ld
data.template_id string 模板ID
请求示 {
例 "product_id": "9MaNe52pNO",

"device_name":"no003",
"imei":"366322456556584",
"imsi": "366322456556584",
"auth_code":"authcode",
"psk":"authcode",
"desc": "iotapplication",
"tag": {"tagkey":"tagvalue"},
"template_field":{"key":"value"}
}
{
"data": {
"name":"no003",
"node_type":1,
"desc": "iotapplication",
"sec_key":
"imQE5CGsIiT9ZMBMD/bSbqMnPIBwXXsYynQQsi/fimk=",
响应示
"created_time":"2020-06-08T10:33:30.442Z",
例
"protocol": 1,
"tag": {"tagkey":"tagvalue"},
"template_field":{"key":"value"}，
},
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.2.2. 批量创建设备
方法 POST
路径 /common?action=BatchCreateDevices&version=1
URI

请求头 Content-Type :application/json
URL 无
参数
product_id string 必填 产品ID
devices array 必填 批量创建的设备信息集合, 一次
最多创建500个设备。每个集合
元素为json对象，包括name、desc、
scene、supplier和档案数据属性值,
例如[{ "name":"no001","scene":
"660a1a925599c5007e1991cd"
请求体
，"supplier":5，"desc": "iot
参数
application","template_field":
{"key":"value"}}], 设备为LwM2M
协议时，增加imei、imsi、
auth_code、psk 属性，如产品有选
择设备档案模版增加
template_field属性，校验规则请参
考设备创建接口
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data ―― 调用成功返回业务数据
响应参
data.list array 创建成功设备信息集合，如下的l
数
表示 list 数组的单个对象标识
l.name string 设备名称
l.node_type Int 设备类型 1-直连设备
l.desc string 设备描述
l.sec_key string 设备密钥

l.protocol int 协议类型 1-泛协议 2-MQTT
3-CoAP
l.imei string imei
l.imsi string imsi
l.auth_code string auth_code
l.psk string psk
l.created_time string 创建时间
l.template_fiel object 设备档案数据
d
l.template_id string 模板ID
{
"product_id": "9MaNe52pNO",
"devices": [
{
"name":"no001",
请求示
"desc": "iotapplication",
例
"scene": "660a1a925599c5007e1991cd"，
"supplier":5，
"template_field":{"key":"value"}
}
]
}
{
"data": {
响应示
list: [{
例
"name":"no001",
"node_type":1,

"desc": "iotapplication",
"sec_key":
"imQE5CGsIiT9ZMBMD/bSbqMnPIBwXXsYynQQsi/fimk=",
"created_time":"2020-06-08T10:33:30.442Z",
"protocol": 1,
"template_id": "6406f2ee9641f20035c53b12",
"template_field":{"key":"value"}
}]
},
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.2.3. 设备编辑
方法 POST
路径 /common?action=UpdateDevice&version=1
URI
请求头 Content-Type :application/json
URL参 无
数
device_name string 必填 设备名称
product_id string 必填 产品ID
imsi string 可选 NB设备imsi，不超过15个的
请求体
数字，设备所属产品为LwM2M
参数
时，为必填
psk string 可选 NB设备所需属性，若创建未填
则平台随机生成，8-16 位数字
字母组合

auth_code string 可选 NB设备鉴权码，1-16 位数字字
母组合
desc string 可选 设备描述
tag object 可选 设备标签
template_field object 可选 设备档案数据
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
响应参 data ―― 调用成功返回业务数据
数
data.device_name string 设备名称
data.desc string 设备描述
data.tag object 设备标签
data.template_fiel object 设备档案数据
d
{
"product_id": "9MaNe52pNO",
"device_name":"no003",
请求示
"desc": "iotapplication",
例
"tag": {"tagkey":"tagvalue"},
"template_field":{"key":"value"}
}
{
"data": {
响应示
"device_name":"no003",
例
"desc": "iotapplication",
"tag": {"tagkey":"tagvalue"},

"template_field":{"key":"value"}
},
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.2.4. 设备删除
方法 POST
路径URI /common?action=DeleteDevice&version=1
请求头 Content-Type:application/json
URL参 无
数
device_name string 必填 设备名称
请求体
参数
product_id string 必填 产品ID
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信
息
响应参
requestId string 调用API时生成的请求标
数
识
success boolean 接口是否调用成功
{
请求示 "product_id": "9MaNe52pNO",
例 "device_name":"no003"
}
{
响应示
"requestId":"a25087f46df04b69b29e90ef0acfd115",
例
"success":true

}
1.4.2.5. 设备详情
方法 GET
/common?action=QueryDeviceDetail&version=1&product_id=lsibd9
路径URI
&device_name=no001
请求头
product_id string 必填 产品id
URL参数
device_name string 必填 设备名称
请求体参 无
数
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data － 调用成功时，返回的业务数据
data.device_name string 设备名称
data.product_id string 产品ID
响应参数
data.product_name string 产品名称
data.desc string 设备描述
data.status int 设备状态 1-未激活 2-在线 3-
离线
data.node_type int 节点类型 1-直连设备
data.protocol int 协议类型 1-泛协议 2-MQTT
3-CoAP
data.ip string 设备连接ip

data.create_time string 创建时间
data.last_time string 最后一次在线时间
data.active_time string 激活时间
data.sec_key string 设备密钥
data.template_id string 所用的模板id
data.template_field object 模板中添加的数据
GET/common?action=QueryDeviceDetail&version=1&product_id=lsibd9
请求示例
&device_name=no001
{
"data":{
"device_name":"no001",
"product_id":"9MaNe52pNO",
"product_name":"空气净化器",
"active_time":"2020-06-19T08:11:27.801Z",
"created_time":"2020-06-19T06:09:22.550Z",
"desc":"设备1",
"ip":"192.168.200.139",
响应示例 "last_time":"2020-06-19T09:48:15.027Z",
"node_type":1,
"protocol": 2,
"sec_key":"UQd3K9lXR/EbLXeJc50lJfvvkTVdu5uFgbfz48/fI5k=",
"status":3,
"template_id": "6406f2ee9641f20035c53b12",
"template_field":{},
"scene":["a25087f46df040ef0acfd115"]
},
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true

}
1.4.2.6. 设备状态查询
方法 GET
路径 /common?action=DeviceStatus&version=1
URI
请求头
product_id string 必填 产品ID
URL参
数
device_name string 必填 设备名称
请求体 无
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
响应参
success boolean 接口是否调用成功
数
data － 调用成功时, 返回业务数据
data.status int 设备状态 1-未激活 2-在线 3-
离线
GET
请求示
/common?action=DeviceStatus&version=1&product_id=9MaNe52pNO&
例
device_name=no001
{
"data": {
响应示 status:1
例 },
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}

1.4.2.7. 设备状态记录查询
方法 GET
路径URI /common?action=DeviceStatusHistory&version=1
请求头
product_id string 必填 产品ID
device_name string 必填 设备名称
start_time string 必填 查询起始时间，毫秒时间戳
URL参数
end_time string 必填 查询结束时间，毫秒时间戳
offset string 可选 请求起始位置，默认0
limit string 可选 每次请求记录数，默认10, 范围[1,100]
请求体 无
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data － 调用成功时, 返回业务数据
data.list array 设备状态历史数据集合，如下的l表示 list 数
响应参数
组的单个对象标识
l.status int 设备状态 0-离线 1-在线
l.time date 时间戳
data.meta object 分页信息
data.meta.limit int 每次请求记录数
data.meta.offset int 请求记录起始位置
GET
请求示例 url/common?action=QueryDeviceStatusHistory&version=1&product_id=9MaNe52p
NO&device_name=no001&start_time=1592795951065&end_time=1592795971065
{
"data":{
"list":[{
响应示例
"status":0,
"time":1592398421297,
}],
"meta":{

"limit":10,
"offset":0
}
},
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.2.8. 设备属性设置
方法 POST
路径URI /common?action=SetDeviceProperty&version=1
请求头 Content-Type :application/json
URL参 无
数
device_name string 必填 设备名称
product_id string 必填 产品ID
params object 必填 设置的属性值, 数据格式为
请求体
json对象, 形式为key:value,key
参数
为属性功能点标识,value 为属
性值, 取值符合物模型定义的
数据类型和取值范围, 例如
{"switch":true }
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
响应参
数
data -- 调用成功时，返回的业务数据
data.id string 设备端回复消息id
data.code int 设备端回复响应码
data.msg string 设备端回复响应消息

{
"product_id": "9MaNe52pNO",
"device_name":"no001",
"params": {
"switch":true, //bool
"text":"hello", //string
"humidity":12, //int32
"number":1564448722123, //int64
请求示 "temperature":30.2 //float
例 "lng": 3.1234567890123456789, //double
"type": 1, //enum
"error": 256, //bitmap
"event": { //struct
"a":1,
"b":true
}
}
}
{
"data": {
"id": "155",
"code": 200,
响应示
"msg": "success"
例
},
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}

1.4.2.9. 设备属性获取
方法 POST
路径URI /common?action=QueryDevicePropertyDetail&version=1
请求头 Content-Type :application/json
URL参数 无
device_name string 必填 设备唯一标识
请求体 product_id string 必填 产品ID
参数
params array 必填 功能点标识数组，expample:
["light","model"]
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
响应参数 requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data -- 调用成功时，返回的业务数据
{
"product_id":"B7EEW578EbRg5Y4K",
请求示例 "device_name":"device3",
"params":["light","model"]
}
{
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true,
"data":{
响应示例
"light":1,
"model":1
}
}

1.4.2.10.设备属性期望值设置
方法 POST
路径URI /common?action=SetDeviceDesiredProperty&version=1
请求头 Content-Type :application/json
URL参数 无
device_name string 必填 设备名称
product_id string 必填 产品ID
params object 必填 设置的属性期望值, 数据格式
请求体
为json对象, 形式为key:value,
参数
key为属性功能点标识,value
为属性值, 取值符合物模型定
义的数据类型和取值范围, 例
如{"switch":true}
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
响应参数
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
{
"product_id":"9MaNe52pNO",
"device_name":"no001",
"params":{
"switch":true, //bool
请求示例 "text":"hello", //string
"humidity":12, //int32
"number":1564448722123, //int64
"temperature":30.2 //float
"lng":3.1234567890123456789, //double
"type": 1, //enum

"error":256, //bitmap
"event": { //struct
"a":1,
"b":true
}
}
}
{
"requestId": "a25087f46df04b69b29e90ef0acfd115",
响应示例
"success":true
}
1.4.2.11.设备属性期望值查询
方法 POST
路径 /common?action=QueryDeviceDesiredProperty&version=1
URI
请求头 Content-Type :application/json
URL参 无
数
device_name string 必填 设备名称
product_id string 必填 产品ID
请求体
params array 必填 查询期望值的功能点标识集合，
参数
参数不传默认查询所有属性期
望，例如["switch", "temperature"]
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
响应参
数
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功

data ―― 调用成功返回业务数据
data.params object 属性功能点期望值
data.params. object 功能点标识为对象key
identify
data.params. string 期望值值
identify.value
{
"product_id":"9MaNe52pNO",
"device_name":"no001",
请求示 "params":[
例 "switch",
"temperature",
]
}
{
"data": {
"params":{
"switch":{
"value": "on"
},
响应示 "temperature":{
例 "value": 23
}
}
},
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}

1.4.2.12.设备属性期望删除
方法 POST
路径 /common?action=DeleteDeviceDesiredProperty&version=1
URI
请求头 Content-Type :application/json
URL参 无
数
device_name string 必填 设备名称
product_id string 必填 产品ID
请求体
params object 必填 删除的属性期望, 数据格式
参数
为json 对象, 形式为
key:value,key为属性功能点
标识,value 为空对象{}
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信
响应参
息
数
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
{
"product_id":"12909",
"device_name":"no001",
请求示
"params":{
例
"temperature":{}, // 删除期望值
}
}
{
响应示
"requestId": "a25087f46df04b69b29e90ef0acfd115",
例
"success":true

}
1.4.2.13.设备属性最新数据查询
方法 GET
路径URI /common?action=DevicePropertyData&version=1
请求头 Content-Type :application/json
product_id string 必填 产品id
URL参
数
device_name string 必填 设备名称
请求体 无
参数
code string 错误码，code为“0”代表请求
成功
msg string 错误消息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data － 调用成功时，返回的业务数据
data.list array 设备最新数据集合，如下的l
响应参 表示 list 数组的单个对象标
数 识
l.identifier string 功能点标识
l.time string 上报时间，毫秒时间戳
l.value string 功能点上报值，json 字符串
l.data_type string 数据类型 int32、int64、float、
double、enum、bool、string、
struct、bitMap
l.access_mode string 读写类型
l.expect_value string 期望值,json字符串，属性功能

点具有该字段
l.name string 功能点名称
l.description string 功能描述
GET
请求示
/common?action=DevicePropertyData&version=1&product_id=9MaNe52pNO&d
例
evice_name=no001
{
"data": {
"list": [{
{
"access_mode": "读写",
"data_type": "int32",
"description":"二氧化碳",
"expect_value":"800",
"identifier": "CO2",
"name":"二氧化碳",
响应示
"time":"1592797444539",
例
"value": "600"
},
{
"access_mode": "读写",
"data_type": "bool",
"description":"关",
"expect_value":"true",
"identifier": "fan",
"name":"风扇",
"time":"1592797444539",
"value": "false"

}
}]
},
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.2.14.设备属性功能点历史数据查询
方法 GET
路径 /common?action=DevicePropertyHistory&version=1
URI
请求头
product_id string 必填 产品id
device_name string 必填 设备名称
identifier string 必填 属性功能点标识
URL参 start_time string 必填 查询起始时间，毫秒时间戳
数
end_time string 必填 查询结束时间，毫秒时间戳
offset string 可选 请求起始位置，默认0
limit string 可选 每次请求记录数，默认10, 范
围[1,100]
请求体 无
参数
code string 错误码，code为“0”代表请
求成功
msg string 错误消息
响应参
数 requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data － 调用成功时，返回的业务数据

data.list array 设备属性记录集合，如下的l
表示 list 数组的单个对象标
识
l.value string 属性功能点上报值
l.time string 属性功能点上报时间
data.meta object 分页信息
data.meta.limit int 每次请求记录数
data.meta.offset int 请求记录起始位置
GET
请求示 /common?action=DevicePropertyHistory&version=1&product_id=9MaNe52
例 pNO&device_name=no001&identifier=fan&start_time=1615342778414&e
nd_time=1615342898096
{
"data":{
"meta":{
"offset":0,
"limit":10
},
"list":[
响应示 {
例 "time":"1639380798206",
"value":"qweasd"
},
{
"time":"1639380795091",
"value":"qweasd"
}
]
},

"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.2.15.设备事件功能点（单个）历史数据
方法 GET
路径 /common?version=1&action=DeviceEventHistory
URI
请求头
product_id string 必填 产品id
device_name string 必填 设备名称
identifier string 可选 事件功能点标识
URL参 start_time string 必填 查询起始时间，毫秒时间戳
数
end_time string 必填 查询结束时间，毫秒时间戳
offset string 可选 请求起始位置，默认0
limit string 可选 每次请求记录数，默认10, 范围[1,
100]
请求体 无
参数
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
响应参
data － 调用成功时，返回的业务数据
数
data.list array 设备事件记录历史数据集合，如下
的l表示 list 数组的单个对象标
识
l.event_type int 事件类型 1-信息 2-告警 3-故

障
l.identifier string 事件功能点标识
l.name string 事件功能点名称
l.time string 事件功能点上报时间
l.value string 事件功能点上报值，json字符串
data.meta object 分页信息
data.meta.limit int 每次请求记录数
data.meta.offset int 请求记录起始位置
GET
请求示 /common?version=1&action=DeviceEventHistory&product_id=9MaNe52pN
例 O&device_name=no001&start_time=1592811019119&end_time=1592811
198213
{
"data": {
"meta":{
"offset":0,
"limit":10
},
"list":[
响应示
{
例
"time":"1639381959167",
"value":"{\"a\":11}",
"event_type":1,
"identifier":"sj01",
"name":"sj01"
}
]
},

"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.2.16.设备服务执行记录查询
方法 GET
路径 /common?action=DeviceServiceHistory&version=1
URI
请求头
product_id string 必填 产品id
device_name string 必填 设备名称
start_time string 必填 查询起始时间，毫秒时间戳
URL参
end_time string 必填 查询结束时间，毫秒时间戳
数
offset string 可选 请求起始位置，默认0
limit string 可选 每次请求记录数，默认10, 范围[1,
100]
请求体 无
参数
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
响应参 success boolean 接口是否调用成功
数
data － 调用成功时，返回的业务数据
data.list array 设备服务执行记录数据集合，如下
的l表示 list 数组的单个对象标识
list.request_time string 调用服务的时间

list.function_na string 功能名称
me
list.identifier string 标识符
list.type string 服务调用类型，0为同步，1为异步
list.request_bod string 服务调用时的请求参数
y
list.response_tim string 返回时间
e
list.response_bo string 输出参数，jsonstring
dy
list.code string 执行结果code，200：执行成功，0：
未执行，其他：执行异常
list.msg string 返回消息
data.meta object 分页信息
data.meta.limit int 每次请求记录数
data.meta.offset int 请求记录起始位置
GET
请求示 /common?action=DeviceServiceHistory&version=1&product_id=7ubgKi1vh
例 m&device_name=sb0011&start_time=1639050724393&end_time=163938
1724393
{
"data":{
"meta":{
响应示
"offset":0,
例
"limit":10
},
"list":[
{

"request_time":"1639383257642",
"function_name":"s1",
"identifier":"s1",
"type":1,
"request_body":"{\"id\":\"2\",\"params\":{\"identifier\":\"s1\",\"input\":{\"b\"
:2}},\"version\":\"1.0\"}",
"response_time":"0",
"response_body":"",
"code":0,
"msg":""
}
]
}
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.2.17.设备操作记录
方法 GET
路径URI /common?action=DeviceOperateHistory&version=1
请求头 Content-Type:application/json
product_id string 必填 产品id
device_name string 必填 设备名称
start_time string 必填 开始时间，毫秒时间戳
URL参
end_time string 必填 结束时间，毫秒时间戳
数
limit string 可选 每次请求记录数，默认10, 范围
[1,100]
offset string 可选 请求起始位置，默认0

请求体 无
参数
code string 错误码，code为“0”代表请求成
功
msg string 错误消息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data － 调用成功时，返回的业务数据
data.list array 设备操作记录集合，如下的l 表示
list 数组的单个对象标识
l.request_time string 请求时间
l.type int 请求类型 0-写 1-读
l.request_body object 请求内容 k=>v形式， k为属性
响应参 功能点标识，v为功能点设置值
数
l.response_tim string 响应时间
e
l.response_bod object 响应结果, 设备回复响应中的
y msg字段
l.response_bod string 响应结果中的id
y.id
l.response_bod int 响应结果中的code
y.code
l.response_bod string 响应结果中信息
y.msg
l.code int 执行结果code，200：执行成功
l.msg string 返回消息
data.meta object 分页信息

data.meta.limit int 每次请求记录数
data.meta.offse int 请求记录起始位置
t
GET
/common?action=DeviceOperateHistory&version=1&product_id=9MaNe52p
请求示
NO&device_name=no001
例
&start_time=1592398386297&end_time=1592398422297
{
"data":{
"list":[
{
"request_time":"1639382709533",
"type":0,
"request_body":"{\"tt\":1}",
"response_time":"1639382709570",
"response_body":{
响应示 "id":"1",
例 "code":200,
"msg":"success"
},
"code":200,
"msg":"success"
}
],
"meta":{
"offset":0,
"limit":10
}

},
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.2.18.设备服务调用
方法 POST
路径 /common?action=CallService&version=1
URI
请求头 Content-Type :application/json
URL参 无
数
device_name string 必填 设备名称
product_id string 必填 产品ID
请求体
identifier string 必填 服务型功能点标识
参数
params object 必填 输入参数的键值对，输入参数
的唯一标识做键
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
响应参
requestId string 调用API时生成的请求标识
数
success boolean 接口是否调用成功
data ―― 调用成功返回业务数据
{
"product_id":"B7EEW578EbRg5Y4K",
请求示 "device_name":"device3",
例 "identifier":"light",
"params":{
"Power1":"1",

"WF1":"2"
}
}
{
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true,
响应示 "data":{
例 "result1":"1",
"result2":"2"
}
}
1.4.2.19.设备链路日志查询
方法 GET
路径 /common?action=DeviceTraceLog&version=1
URI
请求头
product_id string 可 产品id
选
device_name string 可 设备名称
选
start_time string 必 查询起始时间，毫秒时间戳
填
URL请
求参数
end_time string 必 查询结束时间，毫秒时间戳
填
offset string 可 请求起始位置，默认0
选
limit string 可 每次请求记录数，默认10, 范围[1,
选 100]

log_type string 可 业务类型编码，参考备注
选
请求体 无
参数
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
响应参 data － 调用成功时，返回的业务数据
数
data.list array 设备链接日志记录数据集合
data.meta object 分页信息
data.meta.limit int 每次请求记录数
data.meta.offse int 请求记录起始位置
t
GET
请求示
/common?action=DeviceTraceLog&version=1start_time=1639050724393&e
例
nd_time=1639381724393
{
"data":{
"list":[
{
响应示 "type":"1.1",
例 "start_time":"2021-12-10T10:19:33.325Z",
"pid":"7ubgKi1vhm",
"status":"200",
"trace_id":"ab2fc05759a211ecbfd023bbbfff50a4",
"end_time":"2021-12-10T10:19:33.325Z",
"env_type":"UNKNOWN",

"uid":"5",
"device_name":"400A002090011001",
"content":"{\"protocol\":\"MQTT\",\"offline_time\":\"2021-12-10
18:19:33.325\",\"offline_reason\":\"CloseByPeer\"}",
"create_time":"2021-12-1018:19:33",
"message_status":"0",
"type_mean":"设备行为",
"status_mean":"成功"
}
],
"meta":{
"total":26,
"limit":"11",
"offset":"0"
}
}
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
业务类型对照表：{
'1.1':'设备行为',
'1.2':'上行消息',
'1.3':'下行消息',
'2.1':'物模型调用',
备注
'3.1':'数据存储',
'4.1':'规则引擎',
'5.1':'MQ 推送',
'6.1':'HTTP推送',
'7.1':'开放API',

'8.1':'RDS 存储',
'9.1':'应用长连接'
}
1.4.2.20.设备上下行消息查询
方法 GET
路径 /common?action=DeviceMessage&version=1&message_id=fe8e158c5cab11
URI ecbfd05180177bf746
请求头
message_id string 必填 消息id 通过接口【设备链路日志
URL参
查询】获取（只存在部分类型的
数
日志信息中）
请求体 无
参数
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
响应参 requestId string 调用API时生成的请求标识
数
success boolean 接口是否调用成功
data － 调用成功时，返回的业务数据，
data 为base64 字符串，可转义
GET
请求示
/common?action=DeviceMessage&version=1&message_id=fe8e158c5cab11
例
ecbfd05180177bf746
{
"data":
响应示
"eyJpZCI6IjE2Mzk0NjU0MzIzOTMiLCJjb2RlIjoyMDAsIm1zZyI6InN1Y2Nl
例
c3MifQ==",,
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true

}
1.4.2.21.设备转移
方法 POST
路径 /common?action=MoveProductDevice&version=1
URI
请求头 Content-Type:application/json
URL参 无
数
device_name array 必填 被转移设备的名称数组，如["name_1",
"name_2"]
请求体 product_id strin 必填 产品ID
参数 g
target_user_t strin 必填 接收人电话
el g
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
响应参
requestId string 调用API时生成的请求标识
数
success boolean 接口是否调用成功
data － 调用成功时，返回的业务数据
{
"product_id":"IOoSyVbY8q",
请求示
"device_name":["SB00009"],
例
"target_user_tel":"17830021227"
}
{
响应示
"requestId":"a25087f46df04b69b29e90ef0acfd115",
例
"success":true,

"data":{
"move_id":"1317465"
}
}
1.4.2.22.设备批量命令下发
方法 POST
路径 /common?action=DeviceBatchOrder&version=1
URI
请求头 Content-Type :application/json
URL参 无
数
device_name array 必填 设备名称组成的数组
product_id string 必填 产品ID，只能对同一产品下
的多个设备下发
type string 必填 可选['SET_PROPERTY',
'GET_PROPERTY','CALL_SE
RVICE']，依次为属性设置、
属性获取、服务调用
mode number 必填 命令模式，1：串行；2：并行。
请求体
identifier string 参数type 值为
参数
CALL_SERVICE 时必填，服务
型功能点标识
params object 或 必填 根据参数type 值参考对应接
者array 口的params 进行构造：
SET_PROPERTY： 设备属性
设置
GET_PROPERTY： 设备属性
获取
CALL_SERVICE： 设备服务

调用
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
响应参
requestId string 调用API时生成的请求标识
数
success boolean 接口是否调用成功
data ―― 调用成功返回业务数据
{
"type": "SET_PROPERTY",
"mode":1,
请求示
"product_id":"fcvPpxC22R",
例
"device_name":["test9981121"],
"params":{"a":1}
}
{
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true,
"data":{
"successCount":0,// 命令成功数
响应示
"errorCount":1,// 如果是并行命令则表示命令失败数，如果
例
是串行命令表示剩余未下发命令的设备数
"errorDevs":[]// 命令下发失败的设备名称，只有并行命令时
有值，串行命令时无数据值
}
}

1.4.3. 物模型管理
1.4.3.1. 物模型查询
方法 GET
路径 /common?action=QueryThingModel&version=1&product_id=lsibd9
URI
请求头
URL参 product_id string 必 产品id
数 填
请求体 无
参数
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data object 调用成功时，返回的业务数据
data.properties array 数组对象 属性功能点
p.functionMod string 功能点类型，定值'property'
e
响应参
数
p.identifier string 属性唯一标识符（产品下唯一）
p.name string 属性名称
p.desc string 属性描述
p.accessMode string "属性读写类型：只读（r）或读写（rw）
p.functionType string 是否是标准功能点，自定义（u）/系统
（s）/标准（st）
p.dataType object 属性功能点数据
p.dataType.typ string 属性类型:int32（32位整数）、int64（64

e 位整数）、float（单精度浮点）、double
（双精度浮点型）、string（字符串）、
date（String类型UTC 秒）、bool（true
或false）、enum（int类型）、bitMap
（位图）、date（int64类型UTC 时间戳
毫秒）、struct（结构体类型）、array
（数组）
p.dataType.spe object 属性功能点数据
cs
data.events array 数组对象 事件功能点
e.functionMode string 功能点类型，定值'event'
e.identifier string 事件唯一标识符
e.name string 事件名称
e.desc string 事件描述
e.type string 事件类型（info、alert、error）
e.fuctionType string 是否是标准功能点，自定义（u）/标准
（s）
e.outputData array 参数
e.outputData.id string 参数唯一标识符
entifier
e.outputData.n string 参数名称
ame
e.outputData.d object 参数数据
ataType
e.outputData.d string 属性类型:int32（32位整数）、int64（64
ataType.type 位整数）、float（单精度浮点）、double
（双精度浮点型）、string（字符串）、
bool（true 或false）、enum（int 类型）、
bitMap（位图）、date（int64类型UTC
时间戳毫秒）、struct（结构体类型）、

array（数组）
e.outputData.d object 功能点数据
ataType.specs
services array 数组对象 服务功能点
s.functionMode string 功能点类型，定值'service'
s.identifier string 服务唯一标识符（产品下唯一）
s.name string 服务名称
s.desc string 服务描述
s.callType string 调用方式,同步(s)/异步(a)
s.fuctionType string 功能点类型，自定义（u）/系统（s）
s.input array 输入参数
s.input.identifi string 参数唯一标识符
er
s.input.name string 参数名称
s.input.dataTyp object 参数数据
e
s.input.dataTyp string 属性类型:int32（32位整数）、int64（64
e.type 位整数）、float（单精度浮点）、double
（双精度浮点型）、string（字符串）、
bool（true 或false）、enum（int 类型）、
bitMap（位图）、date（int64类型UTC
时间戳毫秒）、struct（结构体类型）、
array（数组）
s.input.dataTyp object 参数功能点数据
e.specs
s.output array 输出参数
s.output.identif string 参数唯一标识符
ier

s.output.name string 参数名称
s.output.dataTy object 参数数据
pe
s.output.dataTy string 属性类型:int32（32位整数）、int64（64
pe.type 位整数）、float（单精度浮点）、double
（双精度浮点型）、string（字符串）、
bool（true 或false）、enum（int 类型）、
bitMap（位图）、date（int64类型UTC
时间戳毫秒）、struct（结构体类型）、
array（数组）
s.output.dataTy object 参数功能点数据
pe.specs
请求示 GET /common?action=QueryThingModel&version=1&product_id=lsibd9
例
{
"data": {
"properties": [
{
"name":"模式",
"identifier": "model",
"functionType": "u",
响应示
"functionMode":"property",
例
"desc": "",
"accessMode": "rw",
"dataType": {
"type": "enum",
"specs":{
"1":"模式1",
"2":"模式2"
}

}
}
],
"events":[
{
"name":"test",
"identifier": "test",
"functionType": "u",
"functionMode":"event",
"desc": null,
"eventType":"info",
"outputData": [
{
"dataType": {
"type": "bool",
"specs":{
"false":"关",
"true": "开"
}
},
"name":"开关",
"identifier": "switch"
}
]
}
]
}
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true

}
1.4.4. 文件管理
1.4.4.1. 设备文件上传
方法 POST
路径URI /common?action=CreateDeviceFile&version=1
请求头 Content-type:multipart/form-data
URL参数 无
device_nam string 必 设备名称 ,参数需构造在同一个
e 填 form-data 中
product_id string 必 产品ID,参数需构造在同一个 form-data
填 中
file file 必 上传的图片文件(目前支持JPG、JPEG、
请求体参
填 PNG、BMP、GIF、WEBP、TIFF、TXT)
数
md5 string 必 文件的MD5
填
size numb 必 文件大小(字节)
er 填
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
响应参数
success boolean 接口是否调用成功
data － 调用成功时，返回的业务数据
data.fid string 文件上传成功后返回的文件ID
请求示例 {

"device_name":"device_name",
"product_id":"qwdfbht",
"md5":"f55c2e86ab864b64a6d939fbe3a7d65f",
"size":12546,
"file":file
}
{
"data":{
"fid":"434fa51a170942c8a291be1e4b229582"
响应示例 }
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.4.2. 查看下载设备文件接口
方法 GET
路径URI /common?action=GetDeviceFile&version=1
请求头
URL参数 id string 必填 文件id
请求体 无
响应参数 file file 需要下载的文件
GET
请求示例 /common?action=GetDeviceFile&version=1&id=43bb54ac673f48c88300
fa6e6d3c9481
响应示例 file
1.4.4.3. 文件删除接口
方法 POST
路径URI /common?action=DeleteDeviceFile&version=1

请求头 Content-type:multipart/form-data
URL参数 无
请求体参 id string 必填 文件ID
数
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
响应参数 requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data － 调用成功时，返回的业务数据
{
请求示例 id：43bb54ac673f48c88300fa6e6d3c9481
}
{
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"code":"0",
响应示例 "msg":"success",
"data":null,
"success":true
}
1.4.5. 分组管理
1.4.5.1. 分组创建
方法 POST
路径URI /common?action=GroupCreate&version=1
请求头 Content-Type :application/json
URL参 无
数

请求体 name string 必填 分组名称
参数 desc string 可选 分组描述
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
响应参
数
success boolean 接口是否调用成功
data -- 调用成功时，返回的业务数据
data.group_id string 分组ID
{
请求示 "name":"黄河大道东",
例 "desc": "group1"
}
{
"data": {
"group_id":"uwYqby"
响应示
},
例
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.5.2. 分组删除
方法 POST
路径URI /common?action=OuterDeleteGroup&version=1
请求头 Content-Type :application/json
URL参数 无
请求体 group_id string 必填 分组ID
参数

code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
响应参数 requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data -- 调用成功时，返回的业务数据
{
请求示例 "group_id":"3UfAWD"
}
{
"data": null,
响应示例 "requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.5.3. 分组编辑
方法 POST
路径URI /common?action=OuterUpdateGroup&version=1
请求头 Content-Type :application/json
URL参数 无
group_id string 必填 分组ID
请求体
tag object 可选 标签信息
参数
desc string 可选 分组描述
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
响应参数 requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data -- 调用成功时，返回的业务数据

data.group_id string 分组ID
{
"group_id":"3UfAWD",
请求示例 "tag": {"key11":"dkmclg"}, #标签的键值对
"desc":"描述"
}
{
"data": {
"group_id":"diVGB3"
响应示例 },
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.5.4. 分组列表
方法 GET
路径URI /common?action=OuterGroupList&version=1
请求头
name string 可选 分组名称
key string 可选 标签key（key、value 需成对出现，
否则没有效果）
URL参数 value string 可选 标签value（key、value 需成对出现，
否则没有效果）
offset string 可选 请求记录起始位置，默认 0
limit string 可选 每次请求记录数，默认10
请求体 无
code string 调用失败时，返回的错误码
响应参数
msg string 调用失败时，返回的错误信息

requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data － 调用成功时, 返回业务数据
data.list array 分组信息集合，如下的l表示 list 数
组的单个对象标识
l.name string 分组名称
l.group_id string 分组id
l.key string 分组key
l.tag object 标签信息,健值对
l.created_tim string 创建时间
e
l.device_coun int 设备数
t
data.meta object 分页信息
data.meta.limi int 每次请求记录数
t
data.meta.offs int 请求记录起始位置
et
data.meta.tota int 记录总数
l
请求示例 GET /common?action=OuterGroupList&version=1
{
响应示例 "data":{
"list":[
{

"name":"xq_group1",
"group_id":"qf6nAD",
"key":
"ZDM0MzA4MTA3MjQ4NzdlYzZjOGJlYzU1YmUwZTNhMmY=",
"tag":{
"xq":"123"
},
"created_time":"2020-08-13T01:49:17694,
"device_count": 2
}
],
"meta":{
"limit":10,
"offset": 0,
"total":1
}
},
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.5.5. 分组详情
方法 GET
路径URI /common?action=OuterGroupDetail&version=1
请求头
URL参数 group_id string 必填 分组ID
请求体 无
code string 调用失败时，返回的错误码
响应参数
msg string 调用失败时，返回的错误信息

requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data － 调用成功时, 返回业务数据
data.activate_co string 激活设备数
unt
data.online_cou string 在线设备数
nt
data.name string 分组名称
data.group_id string 分组ID
data.key string 分组key
data.tag object 分组标签
data.desc string 分组描述
data.device_cou string 设备数量
nt
data.create_time string 创建时间
请求示例 GET /common?action=OuterGroupDetail&version=1
{
"data":{
"activate_count":0,
"online_count":0,
"name":"xq_group1",
响应示例 "group_id":"qf6nAD",
"key":
"ZDM0MzA4MTA3MjQ4NzdlYzZjOGJlYzU1YmUwZTNhMmY=",
"tag":{
"xq":"123"
},
"desc":"123",

"created_time":"2020-08-13T01:49:17.694Z",
"device_count": 2
}
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.5.6. 分组设备添加
方法 POST
路径URI /common?action=OuterAddGroupDevice&version=1
请求头 Content-Type:application/json
URL参数 无
group_id string 必填 分组ID
请求体
product_id string 必填 产品ID
参数
devices arrary 必填 需要添加的设备集合
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data -- 调用成功时，返回的业务数据
响应参数
data.error_data array 添加失败的错误信息集合，如
下的e表示 error_data 数组的
单个对象标识
e.device_name string 添加失败的设备集合
e.cause string 添加失败原因
{
请求示例 "group_id":"Z1Pdei",
"product_id":"XVlg5CCSSj",

"devices":["dev1","dev2"]
}
{
"data":{
"group_id":"qf6nAD",
"devices":["dev1","dev2"]
响应示例
},
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.5.7. 分组设备移除
方法 POST
路径URI /common?action=OuterRemoveGroupDevice&version=1
请求头 Content-Type:application/json
URL参数 无
group_id string 必填 分组ID
请求体
product_id string 必填 产品ID
参数
devices arrary 必填 需要移除的设备集合
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
响应参数
data -- 调用成功时，返回的业务数据
data.error_d array 移除失败的错误信息集合，如
ata 下的e表示 error_data 数组的
单个对象标识
e. string 移除失败的设备集合

device_name
e.cause string 移除失败原因
{
"group_id":"Z1Pdei",
请求示例 "product_id":"XVlg5CCSSj",
"devices":["dev1","dev2"]
}
{
"data":{
"group_id":"qf6nAD",
"devices":["dev1","dev2"]
响应示例
},
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.6. 用户管理
1.4.6.1. 用户下产品数量统计
方法 GET
路径URI /common?action=ProductStatistics&version=1
请求头
URL参数 无
请求体参 无
数

code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolean 接口是否调用成功
data － 调用成功时，返回的业务数据
data.product_agg number 产品数量
regate.product_c
ount
data.product_agg array 数组对象，行业类型统计，如下的ind
regate.ind_agg 表示ind_agg 数组的单个对象标识
ind._id string 行业ID（自动生成）
ind.count string 行业类别下产品数量
ind.name string 行业名称
响应参数
data.product_agg array 数组对象，协议类型统计，如下的pt
regate.pt_agg 表示pt_agg 数组的单个对象标识
pt._id string 协议ID（自动生成）
pt.count string 同一协议下产品数量
pt.name string 协议名称
data.product_agg array 数组对象，联网类型统计，如下的net
regate.net_agg 表示net_agg数组的单个对象标识
net._id string 联网类型ID（自动生成）
net.count string 同一联网类型下产品数量
net.name string 联网类型名称
data.product_agg array 数组对象，物模型类型统计，如下的
regate.model_agg model表示model_agg数组的单个对象
标识
model._id string 物模型类型ID（自动生成）

model.count string 物模型类型下产品数量
model.name string 物模型类型名称
请求示例 GET /common?action=ProductStatistics&version=1
{
"data": {
"product_aggregate":{
"ind_agg":[ // 行业类别
{
"_id":"1",
"count":7,
"name":"智慧城市"
}
],
"pt_agg":[ // 协议类型
{
响应示例 "_id":'sub',
"count":1,
"name":‘网关子设备’
},
{
"_id":4,
"count":2,
"name":'Lwm2m'
},
{
"_id":2,
"count":4,
"name":"MQTT"
}

],
"net_agg":[ // 联网型类型
{
"_id":"1",
"count":0,
"name":"其他"
},
{
"_id":"2",
"count":0,
"name":"蜂窝"
},
{
"_id":"3",
"count":5,
"name":"wifi"
},
{
"_id":"4",
"count":0,
"name":"以太网"
},
{
"_id":"5",
"count":1,
"name":"NB"
}
],
"model_agg":[ // 物模型类型

{
"_id":"1",
"count":2,
"name":"标准"
},
{
"_id":"2",
"count":5,
"name":"自定义"
}
]
},
"product_count":7 // 总数
}
}
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.6.2. 账户下文件列表查询
方法 GET
路径URI /common?action=GetDeviceFilesList&version=1
请求头
offset numbe 可选 请求起始位置，默认0
r
URL参
数
limit numbe 可选 每次请求记录数，默认10
r
请求体 无
参数

code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
requestId string 调用API时生成的请求标识
success boolea 接口是否调用成功
n
data － 调用成功时，返回的业务数据
data.meta.total numbe 文件数量
r
data.meta.limit numbe 每次请求的数据长度
r
响应参
数
data.meta.offset numbe 偏移量
r
data.list.fid string 文件ID
data.list.name string 文件名称
data.list.file_size numbe 文件大小
r
data.list.ct string 文件创建时间
data.list.device_nam string 文件所属设备名称
e
data.list.product_id string 文件所属设备的产品ID
请求示 GET /common?action=GetDeviceFilesList&version=1
例
{
"data": {
响应示
"meta": {
例
"limit": 10,
"offset": 0,
"total":1

},
"list": [
{
"fid":"98cfa6be79574f7eab98eb7b5222911a",
"name":"28fpf.png",
"file_size":138683,
"ct": "2020-12-16T09:30:18.419Z",
"device_name":"ap-test-008",
"product_id": "Bs1f6s5bhKP7rmfO"
}
]
}
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.6.3. 用户文件存储空间查询
方法 GET
路径URI /common?action=GetDeviceFileSpace&version=1
请求头
URL参 无
数
请求体 无
参数
code string 调用失败时，返回的错误码
msg string 调用失败时，返回的错误信息
响应参
requestId string 调用API时生成的请求标识
数
success boolean 接口是否调用成功

data － 调用成功时，返回的业务数据
data.useSize number 用户已使用的空间
data.hasSize number 用户剩余空间
data.totalSize number 用户分配的总空间
请求示 GET/common?action=GetDeviceFileSpace&version=1
例
{
"data": {
"useSize":138683,
响应示 "hasSize":1073603141,
例 "totalSize":1073741824
}
"requestId": "a25087f46df04b69b29e90ef0acfd115",
"success":true
}
1.4.6.4. 用户设备文件数量查询
方法 GET
/common?action=GetDeviceFileCount&version=1&device_name=ap-test-0
路径URI
08&product_id=Bs1f6s5bhKP7rmfO
请求头
product_id string 必填 产品id
URL请
求参数
device_name string 必填 设备名称
请求体 无
参数
code string 调用失败时，返回的错误码
响应参
msg string 调用失败时，返回的错误信
数
息

requestId string 调用API时生成的请求标
识
success boolean 接口是否调用成功
data － 调用成功时，返回的业务数
据
data.upperLimit number 设备允许的最大文件数量
data.filesTotal number 设备已存在的文件数量
GET
请求示
/common?action=GetDeviceFileCount&version=1&device_name=ap-test-0
例
08&product_id=Bs1f6s5bhKP7rmfO
{
"data":{
"upperLimit":10,
响应示
"filesTotal": 1
例
}
"requestId":"a25087f46df04b69b29e90ef0acfd115",
"success":true
}

# IoT 设备管理模块能力文档

> yudao-module-iot 提供完整的IoT设备管理能力，包括产品管理、设备管理、物模型、规则引擎、OTA升级等。

## 一、核心功能

### 1.1 产品管理（Product）

**功能概述**：
- IoT产品定义和分类
- 产品物模型配置
- 产品设备统计

**关键API**：
```
POST   /iot/product/create   创建产品
PUT    /iot/product/update   更新产品
DELETE /iot/product/delete   删除产品
GET    /iot/product/page     产品分页
GET    /iot/product/get      获取产品详情
```

**核心实体**：
- `IotProductDO` (表名: `iot_product`) - IoT产品
- `IotProductCategoryDO` (表名: `iot_product_category`) - 产品分类

**产品关键字段**：
- `name` - 产品名称
- `categoryId` - 产品分类
- `deviceType` - 设备类型（直连设备、网关设备、网关子设备）
- `netType` - 联网方式（WiFi、蜂窝、以太网等）
- `protocolType` - 协议类型（MQTT、CoAP、HTTP等）
- `dataFormat` - 数据格式（JSON、透传）

### 1.2 设备管理（Device）

**功能概述**：
- 设备CRUD、设备分组
- 设备状态监控、设备认证
- 设备导入导出

**关键API**：
```
POST   /iot/device/create         创建设备
PUT    /iot/device/update         更新设备
DELETE /iot/device/delete         删除设备
GET    /iot/device/page           设备分页
GET    /iot/device/get            获取设备详情
PUT    /iot/device/update-group   更新设备分组
GET    /iot/device/get-auth-info  获取设备认证信息
POST   /iot/device/import         导入设备
GET    /iot/device/export-excel   导出设备
```

**核心实体**：`IotDeviceDO` (表名: `iot_device`)

**设备关键字段**：
- `deviceKey` - 设备唯一标识
- `deviceName` - 设备名称
- `productId` - 所属产品
- `deviceSecret` - 设备密钥
- `status` - 设备状态（未激活、在线、离线）
- `activeTime` - 激活时间
- `lastOnlineTime` - 最后在线时间
- `groupId` - 设备分组

**设备状态**：
- `0` - 未激活
- `1` - 在线
- `2` - 离线

### 1.3 物模型（Thing Model）

**功能概述**：
- 物模型定义（属性、服务、事件）
- 物模型版本管理

**核心实体**：`IotThingModelDO` (表名: `iot_thing_model`)

**物模型组件**：

1. **属性（Property）**：
   - 设备的状态和参数
   - 支持读写类型（只读、只写、读写）
   - 数据类型：int、float、double、text、date、bool、enum、struct、array

2. **服务（Service）**：
   - 设备可执行的操作
   - 包含输入参数和输出参数

3. **事件（Event）**：
   - 设备主动上报的信息
   - 包含事件类型和输出参数

**物模型示例**：
```json
{
  "properties": [
    {
      "identifier": "temperature",
      "name": "温度",
      "dataType": "float",
      "accessMode": "r",
      "unit": "℃",
      "min": -50,
      "max": 100
    }
  ],
  "services": [
    {
      "identifier": "reboot",
      "name": "重启设备",
      "inputParams": [],
      "outputParams": []
    }
  ],
  "events": [
    {
      "identifier": "alarm",
      "name": "告警事件",
      "eventType": "alert",
      "outputParams": [
        {
          "identifier": "alarmType",
          "name": "告警类型",
          "dataType": "text"
        }
      ]
    }
  ]
}
```

### 1.4 设备属性（Device Property）

**功能概述**：
- 设备属性上报记录
- 属性历史数据查询

**核心实体**：`IotDevicePropertyDO` (表名: `iot_device_property`)

**关键字段**：
- `deviceId` - 设备ID
- `identifier` - 属性标识符
- `value` - 属性值
- `reportTime` - 上报时间

### 1.5 设备消息（Device Message）

**功能概述**：
- 设备消息记录
- 消息查询和统计

**核心实体**：`IotDeviceMessageDO` (表名: `iot_device_message`)

**消息类型**：
- 属性上报
- 服务调用
- 事件上报

### 1.6 设备分组（Device Group）

**功能概述**：
- 设备分组管理
- 按分组批量操作

**核心实体**：`IotDeviceGroupDO` (表名: `iot_device_group`)

### 1.7 告警管理（Alert）

**功能概述**：
- 告警规则配置
- 告警记录查询
- 告警通知

**核心实体**：
- `IotAlertConfigDO` (表名: `iot_alert_config`) - 告警配置
- `IotAlertRecordDO` (表名: `iot_alert_record`) - 告警记录

**告警触发条件**：
- 属性值超过阈值
- 设备离线
- 事件触发

### 1.8 规则引擎（Rule）

**功能概述**：
- 数据规则：基于设备数据触发动作
- 场景规则：多条件联动
- 数据转发：将数据转发到其他系统

**核心实体**：
- `IotDataRuleDO` (表名: `iot_data_rule`) - 数据规则
- `IotSceneRuleDO` (表名: `iot_scene_rule`) - 场景规则
- `IotDataSinkDO` (表名: `iot_data_sink`) - 数据转发

**数据转发支持**：
- HTTP
- MQTT
- Kafka
- RabbitMQ
- RocketMQ
- Redis
- TCP
- WebSocket

**规则示例**：
```json
{
  "name": "温度告警规则",
  "conditions": [
    {
      "deviceId": "device001",
      "property": "temperature",
      "operator": ">",
      "value": 50
    }
  ],
  "actions": [
    {
      "type": "alert",
      "config": {
        "level": "high",
        "message": "温度过高"
      }
    },
    {
      "type": "forward",
      "config": {
        "sinkId": "sink001"
      }
    }
  ]
}
```

### 1.9 OTA升级（OTA）

**功能概述**：
- 固件管理
- 升级任务管理
- 升级进度跟踪

**核心实体**：
- `IotOtaFirmwareDO` (表名: `iot_ota_firmware`) - 固件
- `IotOtaTaskDO` (表名: `iot_ota_task`) - 升级任务
- `IotOtaTaskRecordDO` (表名: `iot_ota_task_record`) - 升级记录

**升级流程**：
```
1. 上传固件文件
   ↓
2. 创建升级任务（选择设备）
   ↓
3. 设备接收升级通知
   ↓
4. 设备下载固件
   ↓
5. 设备升级并上报进度
   ↓
6. 升级完成或失败
```

---

## 二、设备接入

### 2.1 设备认证

**认证方式**：
- 一机一密：每个设备有独立的密钥
- 一型一密：同一产品的设备共享密钥

**认证流程**：
```
1. 设备使用 deviceKey + deviceSecret 连接
   ↓
2. 平台验证设备身份
   ↓
3. 验证通过，设备上线
```

### 2.2 设备通信协议

**MQTT Topic 规范**：
```
属性上报：/sys/{productKey}/{deviceKey}/thing/property/post
属性设置：/sys/{productKey}/{deviceKey}/thing/property/set
服务调用：/sys/{productKey}/{deviceKey}/thing/service/{serviceId}
事件上报：/sys/{productKey}/{deviceKey}/thing/event/{eventId}/post
```

**消息格式**：
```json
{
  "id": "123456",
  "version": "1.0",
  "params": {
    "temperature": 25.5,
    "humidity": 60
  },
  "method": "thing.property.post"
}
```

---

## 三、业务集成

### 3.1 监测设备接入示例

**场景**：接入燃气监测设备

1. **创建产品**：
```java
IotProductSaveReqVO productReqVO = new IotProductSaveReqVO();
productReqVO.setName("燃气监测设备");
productReqVO.setCategoryId(1L);
productReqVO.setDeviceType(1); // 直连设备
productReqVO.setNetType(1); // WiFi
productReqVO.setProtocolType(1); // MQTT
Long productId = productService.createProduct(productReqVO);
```

2. **配置物模型**：
```java
// 定义属性：压力、浓度
IotThingModelSaveReqVO modelReqVO = new IotThingModelSaveReqVO();
modelReqVO.setProductId(productId);
modelReqVO.setProperties(Arrays.asList(
    new ThingModelProperty()
        .setIdentifier("pressure")
        .setName("压力")
        .setDataType("float")
        .setUnit("MPa"),
    new ThingModelProperty()
        .setIdentifier("concentration")
        .setName("浓度")
        .setDataType("float")
        .setUnit("ppm")
));
thingModelService.saveThingModel(modelReqVO);
```

3. **创建设备**：
```java
IotDeviceSaveReqVO deviceReqVO = new IotDeviceSaveReqVO();
deviceReqVO.setProductId(productId);
deviceReqVO.setDeviceName("监测点001");
deviceReqVO.setDeviceKey("device001");
Long deviceId = deviceService.createDevice(deviceReqVO);
```

4. **配置告警规则**：
```java
IotAlertConfigSaveReqVO alertReqVO = new IotAlertConfigSaveReqVO();
alertReqVO.setProductId(productId);
alertReqVO.setName("浓度超标告警");
alertReqVO.setCondition("concentration > 100");
alertReqVO.setLevel(2); // 高级别
alertConfigService.createAlertConfig(alertReqVO);
```

### 3.2 设备数据查询

```java
@Service
public class MonitoringService {

    @Resource
    private IotDevicePropertyService devicePropertyService;

    /**
     * 查询设备最新属性
     */
    public Map<String, Object> getDeviceLatestProperties(Long deviceId) {
        List<IotDevicePropertyDO> properties =
            devicePropertyService.getLatestProperties(deviceId);

        return properties.stream()
            .collect(Collectors.toMap(
                IotDevicePropertyDO::getIdentifier,
                IotDevicePropertyDO::getValue
            ));
    }

    /**
     * 查询设备历史数据
     */
    public List<IotDevicePropertyDO> getDevicePropertyHistory(
            Long deviceId, String identifier,
            LocalDateTime startTime, LocalDateTime endTime) {
        return devicePropertyService.getPropertyHistory(
            deviceId, identifier, startTime, endTime);
    }
}
```

---

## 四、配置要点

### 4.1 IoT模块配置

```yaml
yudao:
  iot:
    # 消息总线类型：redis, rocketmq, kafka
    message-bus:
      type: redis
    # MQTT配置
    mqtt:
      broker-url: tcp://localhost:1883
      username: admin
      password: admin
```

### 4.2 设备网关配置

```yaml
yudao:
  iot:
    gateway:
      # 是否启用网关
      enable: true
      # 网关端口
      port: 8883
```

---

## 五、最佳实践

### 5.1 产品设计

1. **物模型设计**：
   - 属性定义要清晰，包含单位和范围
   - 服务定义要明确输入输出参数
   - 事件定义要包含必要的上下文信息

2. **设备命名**：
   - 使用有意义的设备名称
   - deviceKey使用唯一标识（如MAC地址）

### 5.2 告警配置

1. **告警级别**：
   - 低：一般提示
   - 中：需要关注
   - 高：需要立即处理

2. **告警通知**：
   - 配置多种通知方式（短信、邮件、站内信）
   - 设置告警频率限制，避免告警风暴

### 5.3 数据管理

1. **数据存储**：
   - 热数据存储在数据库
   - 历史数据定期归档到时序数据库

2. **数据清理**：
   - 定期清理过期数据
   - 保留必要的统计数据

---

## 六、常见问题

### Q1: 如何实现设备离线告警？

**A**: 配置设备离线告警规则。

```java
IotAlertConfigSaveReqVO alertReqVO = new IotAlertConfigSaveReqVO();
alertReqVO.setName("设备离线告警");
alertReqVO.setTriggerType(2); // 设备离线
alertReqVO.setOfflineTimeout(300); // 5分钟离线触发
```

### Q2: 如何批量导入设备？

**A**: 使用Excel导入功能。

1. 下载导入模板
2. 填写设备信息
3. 上传Excel文件
4. 系统自动创建设备

### Q3: 如何实现设备数据转发到第三方系统？

**A**: 配置数据转发规则。

```java
IotDataSinkSaveReqVO sinkReqVO = new IotDataSinkSaveReqVO();
sinkReqVO.setName("转发到业务系统");
sinkReqVO.setType("http");
sinkReqVO.setConfig("{\"url\":\"http://api.example.com/data\"}");
dataSinkService.createDataSink(sinkReqVO);
```

---

## 七、参考资源

- [官方文档 - IoT模块](https://doc.iocoder.cn/iot/)
- [MQTT协议规范](https://mqtt.org/)

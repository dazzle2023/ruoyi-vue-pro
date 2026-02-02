# 监测预警域详细设计

> 松原市燃气安全监管平台 - 监测预警域
>
> 版本: 1.0.0
> 更新时间: 2026-01-27
> 状态: 规划中

---

## 一、领域概述

### 1.1 业务价值

监测预警域是松原市燃气安全监管平台的**核心域**，承担着燃气设备全面感知和智能预警的核心职责。通过实时采集监测设备数据，及时发现异常情况，触发报警并推动处置，是实现"可知、可感、可控、可预测"目标的关键支撑。

### 1.2 功能范围

| 功能模块 | 功能点 | 需求编号 |
|----------|--------|----------|
| 设备监测 | 设备状态监控、设备总览、设备搜索、设备详情 | 3, 33-35 |
| 数据采集 | 监测数据采集、实时监测 | 12, 25 |
| 报警管理 | 动态报警、报警概览、报警列表、报警详情、报警管理、报警研判分析、报警处置跟踪 | 37-43 |
| 风险预警 | 风险评估、风险预警服务 | 8, 31 |
| 视频监控 | 视频接入 | 36 |

**共覆盖15项功能需求**

### 1.3 核心角色

| 角色 | 职责 | 主要操作 |
|------|------|----------|
| 市级监管员 | 全市报警监控、督办处置 | 查看报警、督办处置、研判分析 |
| 县区监管员 | 辖区报警监控、督办处置 | 查看报警、督办处置 |
| 企业安全员 | 报警确认、处置执行 | 确认报警、执行处置、填写记录 |
| 企业运维工程师 | 设备维护、故障处理 | 设备巡检、故障维修 |
| 巡检员 | 现场核实、问题上报 | 现场确认、拍照上报 |

---

## 二、业务流程设计

### 2.1 核心业务流程总览

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           监测预警域核心业务流程                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ 设备接入  │───►│ 数据采集  │───►│ 规则判断  │───►│ 报警触发  │───►│ 报警处置  │ │
│  │          │    │          │    │          │    │          │    │          │ │
│  │ IoT设备  │    │ MQTT上报  │    │ 阈值判断  │    │ 生成报警  │    │ 闭环管理  │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│       │              │              │              │              │           │
│       ▼              ▼              ▼              ▼              ▼           │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐ │
│  │ 设备管理  │    │ 数据存储  │    │ 规则配置  │    │ 消息推送  │    │ 统计分析  │ │
│  └──────────┘    └──────────┘    └──────────┘    └──────────┘    └──────────┘ │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 报警处置流程（核心流程）

#### 2.2.1 流程图

```
┌─────────┐
│ 报警触发 │
└────┬────┘
     │
     ▼
┌─────────────┐    否    ┌─────────────┐
│ 自动研判    │─────────►│ 标记为疑似  │
│ (规则匹配)  │          │ 待人工确认  │
└──────┬──────┘          └──────┬──────┘
       │是                      │
       ▼                        ▼
┌─────────────┐          ┌─────────────┐
│ 生成报警工单 │◄─────────│ 人工确认    │
│             │          │ (企业安全员) │
└──────┬──────┘          └─────────────┘
       │
       ▼
┌─────────────┐
│ 推送通知    │
│ (短信/APP)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐    超时    ┌─────────────┐
│ 企业安全员  │──────────►│ 自动升级    │
│ 接单处置    │           │ 督办提醒    │
└──────┬──────┘           └──────┬──────┘
       │                         │
       ▼                         ▼
┌─────────────┐           ┌─────────────┐
│ 现场处置    │           │ 县区监管员  │
│ (可派巡检员)│           │ 介入督办    │
└──────┬──────┘           └─────────────┘
       │
       ▼
┌─────────────┐    不通过   ┌─────────────┐
│ 处置完成    │───────────►│ 退回重新    │
│ 提交审核    │            │ 处置        │
└──────┬──────┘            └─────────────┘
       │通过
       ▼
┌─────────────┐
│ 报警关闭    │
│ 归档统计    │
└─────────────┘
```

#### 2.2.2 流程节点详情

| 节点编号 | 节点名称 | 处理人 | 表单字段 | 时限要求 | 流转规则 |
|----------|----------|--------|----------|----------|----------|
| N1 | 报警触发 | 系统自动 | 设备ID、报警类型、报警值、报警时间、位置信息 | - | 自动流转到N2 |
| N2 | 自动研判 | 系统自动 | 研判结果、置信度、关联报警 | 实时 | 置信度≥80%→N3，否则→N2a |
| N2a | 人工确认 | 企业安全员 | 确认结果、确认说明 | 30分钟 | 确认为真→N3，确认为误报→结束 |
| N3 | 生成工单 | 系统自动 | 工单编号、优先级、处置要求 | - | 自动流转到N4 |
| N4 | 推送通知 | 系统自动 | 通知内容、通知对象、通知渠道 | - | 自动流转到N5 |
| N5 | 接单处置 | 企业安全员 | 接单时间、预计处置时间 | 15分钟接单 | 超时→N5a，正常→N6 |
| N5a | 督办升级 | 县区监管员 | 督办意见、督办时间 | - | 督办后→N5 |
| N6 | 现场处置 | 企业安全员/巡检员 | 处置措施、处置照片、处置结果 | 根据优先级 | 完成→N7 |
| N7 | 处置审核 | 企业安全管理员 | 审核意见、审核结果 | 2小时 | 通过→N8，不通过→N6 |
| N8 | 报警关闭 | 系统自动 | 关闭时间、处置时长、处置评价 | - | 结束 |

#### 2.2.3 异常处理规则

| 异常场景 | 处理规则 | 触发动作 |
|----------|----------|----------|
| 接单超时（15分钟） | 自动升级到县区监管员 | 发送督办通知 |
| 处置超时（根据优先级） | 自动升级到上级 | 发送催办通知 |
| 重复报警（同设备30分钟内） | 合并到原工单 | 更新报警次数 |
| 高危报警（浓度超限等） | 直接通知县区监管员 | 同步推送多人 |
| 设备离线 | 生成设备离线报警 | 通知运维人员 |

### 2.3 设备监测流程

#### 2.3.1 流程图

```
┌─────────────┐
│ 设备注册    │
│ (IoT平台)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 设备认证    │
│ (密钥验证)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 设备上线    │
│ (状态更新)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 数据上报    │◄──────┐
│ (周期/事件) │       │
└──────┬──────┘       │
       │              │
       ▼              │
┌─────────────┐       │
│ 数据解析    │       │
│ (物模型)    │       │
└──────┬──────┘       │
       │              │
       ▼              │
┌─────────────┐       │
│ 数据存储    │       │
│ (时序库)    │       │
└──────┬──────┘       │
       │              │
       ▼              │
┌─────────────┐       │
│ 规则引擎    │───────┘
│ (阈值判断)  │
└──────┬──────┘
       │触发报警
       ▼
┌─────────────┐
│ 报警处置流程│
└─────────────┘
```

#### 2.3.2 设备类型与监测指标

| 设备类型 | 监测指标 | 采集频率 | 报警阈值 | 说明 |
|----------|----------|----------|----------|------|
| 压力传感器 | 压力值(MPa) | 1分钟 | <0.1或>0.4 | 管网压力监测 |
| 流量计 | 流量值(m³/h) | 1分钟 | 异常波动>30% | 管网流量监测 |
| 浓度探测器 | 浓度值(ppm) | 10秒 | >100ppm | 泄漏检测 |
| 温度传感器 | 温度值(℃) | 1分钟 | >60℃ | 设备温度监测 |
| 阀门状态 | 开关状态 | 事件触发 | 异常开关 | 阀门状态监测 |
| 视频监控 | 视频流 | 实时 | AI识别异常 | 场站监控 |

### 2.4 风险评估流程

#### 2.4.1 流程说明

风险评估是对特定区域、设施或作业活动进行系统性的风险识别和评估，为预防性管理提供依据。

#### 2.4.2 评估流程

```
┌─────────────┐
│ 发起评估    │
│ (企业/政府) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 选择评估对象│
│ (区域/设施) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 填写评估表  │
│ (评估指标)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 系统计算    │
│ (评分模型)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 生成评估报告│
│ (风险等级)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐    高风险    ┌─────────────┐
│ 风险等级判定│───────────►│ 触发预警    │
└──────┬──────┘            └─────────────┘
       │中低风险
       ▼
┌─────────────┐
│ 归档备查    │
└─────────────┘
```

#### 2.4.3 风险评估指标

| 评估维度 | 评估指标 | 权重 | 评分标准 |
|----------|----------|------|----------|
| 设备状态 | 设备完好率、设备老化程度 | 25% | 完好率<80%为高风险 |
| 监测覆盖 | 监测点密度、监测数据完整性 | 20% | 覆盖率<60%为高风险 |
| 历史事故 | 近3年事故次数、事故严重程度 | 25% | 重大事故>0为高风险 |
| 周边环境 | 人口密度、重要设施距离 | 15% | 人口密集区为高风险 |
| 管理水平 | 制度完善度、人员资质 | 15% | 制度缺失为高风险 |

**风险等级划分**：
- 高风险：总分≥80分，需立即整改
- 中风险：60分≤总分<80分，需限期整改
- 低风险：总分<60分，持续监控

---

## 三、角色使用场景

### 3.1 市级监管员使用场景

#### 场景1：全市报警态势监控

**操作步骤**：
1. 登录系统，进入监测预警模块
2. 查看报警概览面板（今日报警数、未处理数、超期数）
3. 查看报警地图分布（GIS热力图）
4. 筛选高优先级报警进行重点关注
5. 对超期未处理报警进行督办

**涉及功能**：报警概览、报警列表、报警地图、督办功能

#### 场景2：报警研判分析

**操作步骤**：
1. 选择待研判的报警记录
2. 查看报警详情（设备信息、历史数据、现场视频）
3. 查看关联报警（同区域、同时段）
4. 结合专业知识进行研判
5. 填写研判意见（真实报警/误报/需进一步核实）
6. 提交研判结果

**涉及功能**：报警详情、报警研判、视频查看、历史数据查询

### 3.2 县区监管员使用场景

#### 场景1：辖区报警监控

**操作步骤**：
1. 登录系统，自动过滤显示本县区数据
2. 查看本县区报警概览
3. 查看各企业报警处置情况
4. 对处置不及时的报警进行督办
5. 查看督办记录和处置进度

**涉及功能**：报警列表（县区过滤）、督办管理、处置跟踪

#### 场景2：企业风险评估审核

**操作步骤**：
1. 接收企业提交的风险评估报告
2. 查看评估详情和评分结果
3. 审核评估内容的真实性和完整性
4. 对高风险项提出整改要求
5. 审核通过或退回修改

**涉及功能**：风险评估管理、审核流程

### 3.3 企业安全员使用场景

#### 场景1：报警接单处置

**操作步骤**：
1. 接收报警推送通知（短信/APP）
2. 登录系统查看报警详情
3. 点击"接单"按钮，开始处置
4. 根据报警类型选择处置方式：
   - 远程处置：调整设备参数、关闭阀门等
   - 现场处置：派遣巡检员到现场
5. 填写处置记录（处置措施、处置结果、现场照片）
6. 提交处置完成，等待审核

**涉及功能**：报警接单、处置记录、照片上传、任务派发

#### 场景2：报警规则配置

**操作步骤**：
1. 进入报警规则配置页面
2. 选择设备类型和监测指标
3. 设置报警阈值（上限、下限）
4. 设置报警等级（一般/重要/紧急）
5. 设置通知对象和通知方式
6. 保存规则并启用

**涉及功能**：报警规则配置、阈值设置、通知配置

### 3.4 企业运维工程师使用场景

#### 场景1：设备状态巡检

**操作步骤**：
1. 登录系统，查看设备总览
2. 筛选离线设备或故障设备
3. 查看设备详情和历史数据
4. 分析设备异常原因
5. 制定维修计划
6. 执行维修并更新设备状态

**涉及功能**：设备总览、设备搜索、设备详情、状态更新

#### 场景2：设备数据分析

**操作步骤**：
1. 选择需要分析的设备
2. 查看设备历史数据曲线
3. 分析数据趋势和异常波动
4. 导出数据进行深度分析
5. 根据分析结果调整设备参数

**涉及功能**：历史数据查询、数据曲线展示、数据导出

### 3.5 巡检员使用场景

#### 场景1：现场报警核实

**操作步骤**：
1. 接收安全员派发的现场核实任务（移动端）
2. 查看任务详情和报警位置
3. 使用导航功能前往现场
4. 到达现场后进行核实
5. 拍照记录现场情况
6. 填写核实结果（确认/误报/需进一步处理）
7. 提交核实报告

**涉及功能**：任务接收（移动端）、导航、拍照上传、核实记录

---

## 四、数据库设计

### 4.1 表清单

| 表名 | 说明 | 数据量级 | 备注 |
|------|------|----------|------|
| gas_monitor_device | 监测设备表 | 1万+ | 基于iot_device扩展 |
| gas_monitor_data | 监测数据表 | 千万+ | 时序数据，建议使用InfluxDB |
| gas_monitor_alarm | 报警记录表 | 10万+ | 核心业务表 |
| gas_monitor_alarm_rule | 报警规则表 | 1000+ | 配置表 |
| gas_monitor_alarm_handle | 报警处置记录表 | 10万+ | 关联报警表 |
| gas_monitor_risk_assess | 风险评估表 | 1万+ | 评估记录 |
| gas_monitor_video | 视频设备表 | 1000+ | 视频监控 |

### 4.2 核心表结构

#### 4.2.1 监测设备表（gas_monitor_device）

```sql
CREATE TABLE gas_monitor_device (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '设备ID',
    device_key VARCHAR(64) NOT NULL COMMENT '设备唯一标识',
    device_name VARCHAR(100) NOT NULL COMMENT '设备名称',
    device_type TINYINT NOT NULL COMMENT '设备类型：1-压力传感器 2-流量计 3-浓度探测器 4-温度传感器 5-阀门 6-视频',
    product_id BIGINT NOT NULL COMMENT '产品ID（关联iot_product）',
    enterprise_id BIGINT NOT NULL COMMENT '所属企业ID',
    facility_id BIGINT COMMENT '所属设施ID（场站、管段等）',
    install_location VARCHAR(200) COMMENT '安装位置描述',
    longitude DECIMAL(10,7) COMMENT '经度',
    latitude DECIMAL(10,7) COMMENT '纬度',
    status TINYINT DEFAULT 0 COMMENT '设备状态：0-未激活 1-在线 2-离线 3-故障',
    last_online_time DATETIME COMMENT '最后在线时间',
    install_date DATE COMMENT '安装日期',
    warranty_date DATE COMMENT '质保到期日期',
    maintenance_cycle INT COMMENT '维护周期（天）',
    last_maintenance_date DATE COMMENT '最后维护日期',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_device_key (device_key),
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_status (status),
    INDEX idx_device_type (device_type)
) COMMENT='监测设备表';
```

#### 4.2.2 报警记录表（gas_monitor_alarm）

```sql
CREATE TABLE gas_monitor_alarm (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '报警ID',
    alarm_no VARCHAR(32) NOT NULL COMMENT '报警编号',
    device_id BIGINT NOT NULL COMMENT '设备ID',
    device_name VARCHAR(100) COMMENT '设备名称（冗余）',
    enterprise_id BIGINT NOT NULL COMMENT '所属企业ID',
    enterprise_name VARCHAR(100) COMMENT '企业名称（冗余）',
    alarm_type TINYINT NOT NULL COMMENT '报警类型：1-压力异常 2-流量异常 3-浓度超标 4-温度异常 5-设备离线 6-其他',
    alarm_level TINYINT NOT NULL COMMENT '报警等级：1-一般 2-重要 3-紧急',
    alarm_value VARCHAR(50) COMMENT '报警值',
    threshold_value VARCHAR(50) COMMENT '阈值',
    alarm_time DATETIME NOT NULL COMMENT '报警时间',
    alarm_location VARCHAR(200) COMMENT '报警位置',
    longitude DECIMAL(10,7) COMMENT '经度',
    latitude DECIMAL(10,7) COMMENT '纬度',
    status TINYINT DEFAULT 0 COMMENT '状态：0-待确认 1-处置中 2-已完成 3-已关闭 4-误报',
    is_confirmed TINYINT DEFAULT 0 COMMENT '是否确认：0-未确认 1-已确认',
    confirm_user_id BIGINT COMMENT '确认人ID',
    confirm_time DATETIME COMMENT '确认时间',
    confirm_result TINYINT COMMENT '确认结果：1-真实报警 2-误报 3-需进一步核实',
    is_handled TINYINT DEFAULT 0 COMMENT '是否处置：0-未处置 1-已处置',
    handle_user_id BIGINT COMMENT '处置人ID',
    handle_start_time DATETIME COMMENT '处置开始时间',
    handle_end_time DATETIME COMMENT '处置结束时间',
    handle_duration INT COMMENT '处置时长（分钟）',
    is_timeout TINYINT DEFAULT 0 COMMENT '是否超时：0-否 1-是',
    is_escalated TINYINT DEFAULT 0 COMMENT '是否升级：0-否 1-是',
    escalate_level TINYINT COMMENT '升级层级：1-县区 2-市级',
    related_alarm_ids VARCHAR(200) COMMENT '关联报警ID（逗号分隔）',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_alarm_no (alarm_no),
    INDEX idx_device_id (device_id),
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_alarm_time (alarm_time),
    INDEX idx_status (status),
    INDEX idx_alarm_level (alarm_level)
) COMMENT='报警记录表';
```

#### 4.2.3 报警规则表（gas_monitor_alarm_rule）

```sql
CREATE TABLE gas_monitor_alarm_rule (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '规则ID',
    rule_name VARCHAR(100) NOT NULL COMMENT '规则名称',
    rule_code VARCHAR(50) NOT NULL COMMENT '规则编码',
    device_type TINYINT NOT NULL COMMENT '设备类型',
    monitor_indicator VARCHAR(50) NOT NULL COMMENT '监测指标',
    condition_type TINYINT NOT NULL COMMENT '条件类型：1-大于 2-小于 3-等于 4-区间 5-变化率',
    threshold_value VARCHAR(100) NOT NULL COMMENT '阈值（JSON格式）',
    alarm_level TINYINT NOT NULL COMMENT '报警等级：1-一般 2-重要 3-紧急',
    notify_users VARCHAR(500) COMMENT '通知人员ID（逗号分隔）',
    notify_roles VARCHAR(200) COMMENT '通知角色ID（逗号分隔）',
    notify_methods VARCHAR(50) COMMENT '通知方式：1-短信 2-APP 3-邮件（逗号分隔）',
    is_enabled TINYINT DEFAULT 1 COMMENT '是否启用：0-否 1-是',
    enterprise_id BIGINT COMMENT '所属企业ID（为空表示全局规则）',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    UNIQUE KEY uk_rule_code (rule_code),
    INDEX idx_device_type (device_type),
    INDEX idx_enterprise_id (enterprise_id)
) COMMENT='报警规则表';
```

#### 4.2.4 报警处置记录表（gas_monitor_alarm_handle）

```sql
CREATE TABLE gas_monitor_alarm_handle (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '处置记录ID',
    alarm_id BIGINT NOT NULL COMMENT '报警ID',
    handle_type TINYINT NOT NULL COMMENT '处置类型：1-远程处置 2-现场处置 3-派单处置',
    handle_user_id BIGINT NOT NULL COMMENT '处置人ID',
    handle_user_name VARCHAR(50) COMMENT '处置人姓名（冗余）',
    handle_time DATETIME NOT NULL COMMENT '处置时间',
    handle_measures TEXT COMMENT '处置措施',
    handle_result TINYINT COMMENT '处置结果：1-已解决 2-部分解决 3-未解决',
    handle_photos VARCHAR(500) COMMENT '处置照片（逗号分隔）',
    is_on_site TINYINT DEFAULT 0 COMMENT '是否现场：0-否 1-是',
    on_site_location VARCHAR(200) COMMENT '现场位置',
    on_site_longitude DECIMAL(10,7) COMMENT '现场经度',
    on_site_latitude DECIMAL(10,7) COMMENT '现场纬度',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    INDEX idx_alarm_id (alarm_id),
    INDEX idx_handle_user_id (handle_user_id),
    INDEX idx_handle_time (handle_time)
) COMMENT='报警处置记录表';
```

#### 4.2.5 风险评估表（gas_monitor_risk_assess）

```sql
CREATE TABLE gas_monitor_risk_assess (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '评估ID',
    assess_no VARCHAR(32) NOT NULL COMMENT '评估编号',
    assess_name VARCHAR(100) NOT NULL COMMENT '评估名称',
    assess_type TINYINT NOT NULL COMMENT '评估类型：1-区域评估 2-设施评估 3-作业评估',
    assess_object_id BIGINT COMMENT '评估对象ID',
    assess_object_name VARCHAR(100) COMMENT '评估对象名称',
    enterprise_id BIGINT NOT NULL COMMENT '所属企业ID',
    assess_date DATE NOT NULL COMMENT '评估日期',
    assess_user_id BIGINT COMMENT '评估人ID',
    assess_user_name VARCHAR(50) COMMENT '评估人姓名',
    device_score DECIMAL(5,2) COMMENT '设备状态得分',
    monitor_score DECIMAL(5,2) COMMENT '监测覆盖得分',
    history_score DECIMAL(5,2) COMMENT '历史事故得分',
    environment_score DECIMAL(5,2) COMMENT '周边环境得分',
    management_score DECIMAL(5,2) COMMENT '管理水平得分',
    total_score DECIMAL(5,2) NOT NULL COMMENT '总分',
    risk_level TINYINT NOT NULL COMMENT '风险等级：1-低风险 2-中风险 3-高风险',
    assess_content TEXT COMMENT '评估内容（JSON格式）',
    risk_points TEXT COMMENT '风险点描述',
    improvement_suggestions TEXT COMMENT '改进建议',
    status TINYINT DEFAULT 0 COMMENT '状态：0-草稿 1-已提交 2-已审核',
    audit_user_id BIGINT COMMENT '审核人ID',
    audit_time DATETIME COMMENT '审核时间',
    audit_opinion VARCHAR(500) COMMENT '审核意见',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_assess_no (assess_no),
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_assess_date (assess_date),
    INDEX idx_risk_level (risk_level)
) COMMENT='风险评估表';
```

---

## 五、API接口设计

### 5.1 接口清单

| 模块 | 接口路径 | 方法 | 说明 | 权限标识 |
|------|----------|------|------|----------|
| 设备管理 | /gas/monitor/device/page | GET | 设备分页查询 | gas:monitor:device:query |
| 设备管理 | /gas/monitor/device/get | GET | 获取设备详情 | gas:monitor:device:query |
| 设备管理 | /gas/monitor/device/create | POST | 创建设备 | gas:monitor:device:create |
| 设备管理 | /gas/monitor/device/update | PUT | 更新设备 | gas:monitor:device:update |
| 设备管理 | /gas/monitor/device/delete | DELETE | 删除设备 | gas:monitor:device:delete |
| 设备管理 | /gas/monitor/device/status | GET | 设备状态统计 | gas:monitor:device:query |
| 数据采集 | /gas/monitor/data/latest | GET | 获取最新数据 | gas:monitor:data:query |
| 数据采集 | /gas/monitor/data/history | GET | 获取历史数据 | gas:monitor:data:query |
| 数据采集 | /gas/monitor/data/curve | GET | 获取数据曲线 | gas:monitor:data:query |
| 报警管理 | /gas/monitor/alarm/page | GET | 报警分页查询 | gas:monitor:alarm:query |
| 报警管理 | /gas/monitor/alarm/get | GET | 获取报警详情 | gas:monitor:alarm:query |
| 报警管理 | /gas/monitor/alarm/confirm | POST | 确认报警 | gas:monitor:alarm:confirm |
| 报警管理 | /gas/monitor/alarm/accept | POST | 接单处置 | gas:monitor:alarm:handle |
| 报警管理 | /gas/monitor/alarm/handle | POST | 提交处置 | gas:monitor:alarm:handle |
| 报警管理 | /gas/monitor/alarm/close | POST | 关闭报警 | gas:monitor:alarm:close |
| 报警管理 | /gas/monitor/alarm/escalate | POST | 升级督办 | gas:monitor:alarm:escalate |
| 报警管理 | /gas/monitor/alarm/statistics | GET | 报警统计 | gas:monitor:alarm:query |
| 报警规则 | /gas/monitor/rule/page | GET | 规则分页查询 | gas:monitor:rule:query |
| 报警规则 | /gas/monitor/rule/create | POST | 创建规则 | gas:monitor:rule:create |
| 报警规则 | /gas/monitor/rule/update | PUT | 更新规则 | gas:monitor:rule:update |
| 报警规则 | /gas/monitor/rule/delete | DELETE | 删除规则 | gas:monitor:rule:delete |
| 报警规则 | /gas/monitor/rule/enable | PUT | 启用/停用规则 | gas:monitor:rule:update |
| 风险评估 | /gas/monitor/risk/page | GET | 评估分页查询 | gas:monitor:risk:query |
| 风险评估 | /gas/monitor/risk/create | POST | 创建评估 | gas:monitor:risk:create |
| 风险评估 | /gas/monitor/risk/submit | POST | 提交评估 | gas:monitor:risk:submit |
| 风险评估 | /gas/monitor/risk/audit | POST | 审核评估 | gas:monitor:risk:audit |
| 视频监控 | /gas/monitor/video/list | GET | 视频设备列表 | gas:monitor:video:query |
| 视频监控 | /gas/monitor/video/play | GET | 获取播放地址 | gas:monitor:video:play |

### 5.2 核心接口详情

#### 5.2.1 报警分页查询

**接口路径**：`GET /gas/monitor/alarm/page`

**请求参数**：
```json
{
  "pageNo": 1,
  "pageSize": 10,
  "deviceName": "压力传感器001",
  "enterpriseId": 1,
  "alarmType": 1,
  "alarmLevel": 2,
  "status": 0,
  "startTime": "2026-01-01 00:00:00",
  "endTime": "2026-01-27 23:59:59"
}
```

**响应结果**：
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "list": [
      {
        "id": 1,
        "alarmNo": "AL202601270001",
        "deviceId": 100,
        "deviceName": "压力传感器001",
        "enterpriseId": 1,
        "enterpriseName": "松原燃气公司",
        "alarmType": 1,
        "alarmTypeName": "压力异常",
        "alarmLevel": 2,
        "alarmLevelName": "重要",
        "alarmValue": "0.05",
        "thresholdValue": "0.1",
        "alarmTime": "2026-01-27 10:30:00",
        "alarmLocation": "宁江区中央大街100号",
        "longitude": 124.825,
        "latitude": 45.171,
        "status": 1,
        "statusName": "处置中",
        "isConfirmed": 1,
        "confirmUserName": "张三",
        "confirmTime": "2026-01-27 10:35:00",
        "handleUserName": "李四",
        "handleStartTime": "2026-01-27 10:40:00",
        "isTimeout": 0,
        "createTime": "2026-01-27 10:30:00"
      }
    ],
    "total": 100
  }
}
```

#### 5.2.2 接单处置

**接口路径**：`POST /gas/monitor/alarm/accept`

**请求参数**：
```json
{
  "alarmId": 1,
  "estimatedTime": 60
}
```

**响应结果**：
```json
{
  "code": 0,
  "msg": "接单成功",
  "data": {
    "alarmId": 1,
    "handleUserId": 10,
    "handleStartTime": "2026-01-27 10:40:00"
  }
}
```

#### 5.2.3 提交处置

**接口路径**：`POST /gas/monitor/alarm/handle`

**请求参数**：
```json
{
  "alarmId": 1,
  "handleType": 2,
  "handleMeasures": "现场检查发现阀门未完全关闭，已重新关闭阀门并检查密封性",
  "handleResult": 1,
  "handlePhotos": ["https://xxx.com/photo1.jpg", "https://xxx.com/photo2.jpg"],
  "isOnSite": 1,
  "onSiteLocation": "宁江区中央大街100号",
  "onSiteLongitude": 124.825,
  "onSiteLatitude": 45.171,
  "remark": "已恢复正常"
}
```

**响应结果**：
```json
{
  "code": 0,
  "msg": "处置提交成功，等待审核",
  "data": {
    "handleId": 100,
    "alarmId": 1,
    "handleTime": "2026-01-27 11:00:00"
  }
}
```

#### 5.2.4 创建报警规则

**接口路径**：`POST /gas/monitor/rule/create`

**请求参数**：
```json
{
  "ruleName": "压力传感器低压报警",
  "ruleCode": "PRESSURE_LOW",
  "deviceType": 1,
  "monitorIndicator": "pressure",
  "conditionType": 2,
  "thresholdValue": "{\"min\": 0.1}",
  "alarmLevel": 2,
  "notifyUsers": "10,20,30",
  "notifyRoles": "5,6",
  "notifyMethods": "1,2",
  "isEnabled": 1,
  "enterpriseId": 1,
  "remark": "管网压力低于0.1MPa时触发报警"
}
```

**响应结果**：
```json
{
  "code": 0,
  "msg": "规则创建成功",
  "data": {
    "id": 10
  }
}
```

#### 5.2.5 获取设备历史数据

**接口路径**：`GET /gas/monitor/data/history`

**请求参数**：
```
deviceId=100
indicator=pressure
startTime=2026-01-27 00:00:00
endTime=2026-01-27 23:59:59
interval=5m
```

**响应结果**：
```json
{
  "code": 0,
  "msg": "success",
  "data": {
    "deviceId": 100,
    "deviceName": "压力传感器001",
    "indicator": "pressure",
    "unit": "MPa",
    "dataPoints": [
      {
        "time": "2026-01-27 00:00:00",
        "value": 0.25
      },
      {
        "time": "2026-01-27 00:05:00",
        "value": 0.26
      }
    ]
  }
}
```

---

## 六、BPMN工作流设计

### 6.1 报警处置审批流程

#### 6.1.1 流程定义

**流程Key**：`alarm_handle_approval`

**流程名称**：报警处置审批流程

**适用场景**：企业安全员提交报警处置结果后，需要企业安全管理员审核

#### 6.1.2 BPMN流程图

```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:flowable="http://flowable.org/bpmn"
             targetNamespace="http://flowable.org/test">

  <process id="alarm_handle_approval" name="报警处置审批流程" isExecutable="true">

    <!-- 开始事件 -->
    <startEvent id="startEvent" name="开始"/>

    <!-- 用户任务：安全管理员审核 -->
    <userTask id="safetyManagerAudit" name="安全管理员审核"
              flowable:assignee="${safetyManagerId}">
      <extensionElements>
        <flowable:formProperty id="auditResult" name="审核结果" type="enum" required="true">
          <flowable:value id="approved" name="通过"/>
          <flowable:value id="rejected" name="不通过"/>
        </flowable:formProperty>
        <flowable:formProperty id="auditOpinion" name="审核意见" type="string"/>
      </extensionElements>
    </userTask>

    <!-- 排他网关：判断审核结果 -->
    <exclusiveGateway id="auditGateway" name="审核结果判断"/>

    <!-- 服务任务：审核通过，关闭报警 -->
    <serviceTask id="closeAlarm" name="关闭报警"
                 flowable:class="cn.iocoder.yudao.module.gas.service.alarm.AlarmCloseService"/>

    <!-- 服务任务：审核不通过，退回重新处置 -->
    <serviceTask id="returnHandle" name="退回重新处置"
                 flowable:class="cn.iocoder.yudao.module.gas.service.alarm.AlarmReturnService"/>

    <!-- 结束事件 -->
    <endEvent id="endEvent" name="结束"/>

    <!-- 流程连线 -->
    <sequenceFlow sourceRef="startEvent" targetRef="safetyManagerAudit"/>
    <sequenceFlow sourceRef="safetyManagerAudit" targetRef="auditGateway"/>
    <sequenceFlow sourceRef="auditGateway" targetRef="closeAlarm">
      <conditionExpression>${auditResult == 'approved'}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="auditGateway" targetRef="returnHandle">
      <conditionExpression>${auditResult == 'rejected'}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="closeAlarm" targetRef="endEvent"/>
    <sequenceFlow sourceRef="returnHandle" targetRef="endEvent"/>

  </process>
</definitions>
```

#### 6.1.3 流程变量

| 变量名 | 类型 | 说明 | 示例值 |
|--------|------|------|--------|
| alarmId | Long | 报警ID | 1 |
| handleId | Long | 处置记录ID | 100 |
| safetyManagerId | Long | 安全管理员ID | 20 |
| auditResult | String | 审核结果 | approved/rejected |
| auditOpinion | String | 审核意见 | 处置措施得当，同意关闭 |

#### 6.1.4 流程启动代码示例

```java
@Service
public class AlarmHandleService {

    @Resource
    private RuntimeService runtimeService;

    /**
     * 提交处置并启动审批流程
     */
    public void submitHandle(AlarmHandleSubmitReqVO reqVO) {
        // 1. 保存处置记录
        AlarmHandleDO handleDO = saveHandleRecord(reqVO);

        // 2. 更新报警状态为"待审核"
        updateAlarmStatus(reqVO.getAlarmId(), AlarmStatusEnum.PENDING_AUDIT);

        // 3. 启动审批流程
        Map<String, Object> variables = new HashMap<>();
        variables.put("alarmId", reqVO.getAlarmId());
        variables.put("handleId", handleDO.getId());
        variables.put("safetyManagerId", getSafetyManagerId(reqVO.getAlarmId()));

        ProcessInstance processInstance = runtimeService.startProcessInstanceByKey(
            "alarm_handle_approval",
            String.valueOf(reqVO.getAlarmId()),
            variables
        );

        // 4. 记录流程实例ID
        updateHandleProcessInstanceId(handleDO.getId(), processInstance.getId());
    }
}
```

### 6.2 风险评估审核流程

#### 6.2.1 流程定义

**流程Key**：`risk_assess_audit`

**流程名称**：风险评估审核流程

**适用场景**：企业提交风险评估报告后，需要县区监管员审核

#### 6.2.2 流程节点

| 节点ID | 节点名称 | 节点类型 | 处理人 | 说明 |
|--------|----------|----------|--------|------|
| startEvent | 开始 | 开始事件 | - | 流程开始 |
| countyAudit | 县区监管员审核 | 用户任务 | 县区监管员 | 审核评估报告 |
| auditGateway | 审核结果判断 | 排他网关 | - | 判断审核结果 |
| approveTask | 审核通过 | 服务任务 | - | 更新评估状态为已审核 |
| rejectTask | 审核不通过 | 服务任务 | - | 退回修改 |
| endEvent | 结束 | 结束事件 | - | 流程结束 |

---

## 七、技术实现要点

### 7.1 IoT设备接入

**基于ruoyi-vue-pro的iot模块**：

1. **产品定义**：为每种设备类型创建IoT产品
2. **物模型配置**：定义设备的属性、服务、事件
3. **设备注册**：批量导入或单个创建设备
4. **MQTT通信**：设备通过MQTT协议上报数据
5. **规则引擎**：配置报警规则，自动触发报警

### 7.2 时序数据存储

**使用InfluxDB存储监测数据**：

```java
@Service
public class MonitorDataService {

    @Resource
    private InfluxDBClient influxDBClient;

    /**
     * 保存监测数据
     */
    public void saveMonitorData(MonitorDataDTO data) {
        Point point = Point.measurement("monitor_data")
            .addTag("device_id", String.valueOf(data.getDeviceId()))
            .addTag("indicator", data.getIndicator())
            .addField("value", data.getValue())
            .time(data.getTimestamp(), WritePrecision.MS);

        influxDBClient.getWriteApiBlocking().writePoint(point);
    }

    /**
     * 查询历史数据
     */
    public List<MonitorDataDTO> queryHistoryData(Long deviceId, String indicator,
                                                   LocalDateTime start, LocalDateTime end) {
        String flux = String.format(
            "from(bucket: \"gas_monitor\") " +
            "|> range(start: %s, stop: %s) " +
            "|> filter(fn: (r) => r[\"device_id\"] == \"%d\" and r[\"indicator\"] == \"%s\")",
            start, end, deviceId, indicator
        );

        return influxDBClient.getQueryApi().query(flux, MonitorDataDTO.class);
    }
}
```

### 7.3 实时报警推送

**使用WebSocket推送报警**：

```java
@Component
public class AlarmPushService {

    @Resource
    private WebSocketMessageSender webSocketMessageSender;

    @Resource
    private SmsService smsService;

    /**
     * 推送报警通知
     */
    public void pushAlarm(AlarmDO alarm, List<Long> userIds) {
        // 1. WebSocket推送（在线用户）
        AlarmPushMessage message = buildAlarmMessage(alarm);
        userIds.forEach(userId -> {
            webSocketMessageSender.send(userId, "alarm", message);
        });

        // 2. 短信推送（紧急报警）
        if (alarm.getAlarmLevel() == AlarmLevelEnum.URGENT.getLevel()) {
            userIds.forEach(userId -> {
                String mobile = getUserMobile(userId);
                smsService.sendAlarmSms(mobile, alarm);
            });
        }

        // 3. APP推送
        userIds.forEach(userId -> {
            pushToApp(userId, alarm);
        });
    }
}
```

### 7.4 报警规则引擎

**基于IoT规则引擎实现**：

```java
@Service
public class AlarmRuleEngine {

    /**
     * 判断是否触发报警
     */
    public boolean shouldTriggerAlarm(MonitorDataDTO data, AlarmRuleDO rule) {
        String indicator = data.getIndicator();
        Double value = data.getValue();

        JSONObject threshold = JSON.parseObject(rule.getThresholdValue());

        switch (rule.getConditionType()) {
            case 1: // 大于
                return value > threshold.getDouble("max");
            case 2: // 小于
                return value < threshold.getDouble("min");
            case 3: // 等于
                return value.equals(threshold.getDouble("value"));
            case 4: // 区间
                return value < threshold.getDouble("min") || value > threshold.getDouble("max");
            case 5: // 变化率
                Double lastValue = getLastValue(data.getDeviceId(), indicator);
                Double changeRate = Math.abs((value - lastValue) / lastValue);
                return changeRate > threshold.getDouble("rate");
            default:
                return false;
        }
    }
}
```

---

## 八、附录

### 8.1 报警类型枚举

| 枚举值 | 名称 | 说明 |
|--------|------|------|
| 1 | 压力异常 | 管网压力超出正常范围 |
| 2 | 流量异常 | 管网流量异常波动 |
| 3 | 浓度超标 | 燃气浓度超过安全阈值 |
| 4 | 温度异常 | 设备温度过高 |
| 5 | 设备离线 | 监测设备失联 |
| 6 | 其他 | 其他类型报警 |

### 8.2 报警等级枚举

| 枚举值 | 名称 | 响应时限 | 处置时限 | 说明 |
|--------|------|----------|----------|------|
| 1 | 一般 | 30分钟 | 4小时 | 一般性异常 |
| 2 | 重要 | 15分钟 | 2小时 | 需要重点关注 |
| 3 | 紧急 | 5分钟 | 1小时 | 需要立即处置 |

### 8.3 参考文档

- [ruoyi-vue-pro IoT模块文档](https://doc.iocoder.cn/iot/)
- [Flowable工作流文档](https://www.flowable.com/open-source/docs/)
- [InfluxDB文档](https://docs.influxdata.com/)

---

*最后更新：2026-01-27*

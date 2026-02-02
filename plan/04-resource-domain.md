# 资源管理域详细设计

> 松原市燃气安全监管平台 - 资源管理域
>
> 版本: 1.0.0
> 更新时间: 2026-01-27
> 状态: 规划中

---

## 一、领域概述

### 1.1 业务价值

资源管理域是松原市燃气安全监管平台的**支撑域**，为其他业务领域提供基础数据支撑。通过对燃气企业、管网设施、场站设备、用户信息等核心资源的统一管理，实现燃气行业资源的全面掌控和精细化管理，为监测预警、巡查防控、应急调度等业务提供可靠的数据基础。

### 1.2 功能范围

| 功能模块 | 功能点 | 需求编号 |
|----------|--------|----------|
| 企业管理 | 燃气企业信息管理、企业资质管理、企业评价 | 基础功能 |
| 管网管理 | 管网档案、管网GIS、管网统计分析 | 基础功能 |
| 场站管理 | 场站信息、场站设备、场站监控 | 基础功能 |
| 用户管理 | 工商用户、居民用户、用户档案 | 基础功能 |
| 设施管理 | 调压设施、阀门井、监测点位 | 基础功能 |
| 专家资源 | 专家库管理（与应急域共享） | 73 |
| 物资资源 | 应急物资管理（与应急域共享） | 75 |

**共覆盖基础资源管理及部分应急资源功能**

### 1.3 核心角色

| 角色 | 职责 | 主要操作 |
|------|------|----------|
| 市级监管员 | 全市资源数据监管 | 查看统计、数据审核、导出报表 |
| 县区监管员 | 辖区资源数据管理 | 数据维护、审核企业资料 |
| 企业管理员 | 企业内部资源管理 | 维护企业信息、管网数据、设施台账 |
| 企业安全员 | 设施日常管理 | 更新设施状态、上报变更 |
| 数据管理员 | 数据质量管理 | 数据清洗、标准化、质量检查 |

---

## 二、业务流程设计

### 2.1 核心业务流程总览

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           资源管理域核心业务流程                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          企业入驻流程                                      │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │  │
│  │  │ 企业申请  │───►│ 资料审核  │───►│ 账号开通  │───►│ 数据录入  │          │  │
│  │  │ (注册)   │    │ (县区)   │    │ (系统)   │    │ (企业)   │          │  │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          资源数据管理                                      │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │  │
│  │  │ 管网录入  │    │ 场站录入  │    │ 设施录入  │    │ 用户录入  │          │  │
│  │  │ (GIS)    │    │ (台账)   │    │ (台账)   │    │ (档案)   │          │  │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          数据变更管理                                      │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │  │
│  │  │ 变更申请  │───►│ 变更审核  │───►│ 数据更新  │───►│ 变更记录  │          │  │
│  │  │ (企业)   │    │ (监管)   │    │ (系统)   │    │ (存档)   │          │  │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          数据应用服务                                      │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │  │
│  │  │ 监测预警  │    │ 巡查防控  │    │ 应急调度  │    │ 统计分析  │          │  │
│  │  │ (调用)   │    │ (调用)   │    │ (调用)   │    │ (调用)   │          │  │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 企业入驻流程

#### 2.2.1 流程图

```
┌─────────────┐
│ 燃气企业    │
│ 提交申请    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 填写企业    │
│ 基本信息    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 上传资质    │
│ 证照材料    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 县区监管员  │
│ 初审       │
└──────┬──────┘
       │
       ├─────────────────┐
       │初审通过         │初审不通过
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ 市级监管员  │   │ 退回修改    │
│ 复审       │   │ (补充材料)  │
└──────┬──────┘   └─────────────┘
       │
       ├─────────────────┐
       │复审通过         │复审不通过
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ 系统自动    │   │ 退回县区    │
│ 开通账号    │   │ 重新审核    │
└──────┬──────┘   └─────────────┘
       │
       ▼
┌─────────────┐
│ 企业登录    │
│ 完善资料    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 录入管网    │
│ 设施数据    │
└─────────────┘
```

#### 2.2.2 流程节点详情

| 节点编号 | 节点名称 | 处理人 | 表单字段 | 时限要求 | 流转规则 |
|----------|----------|--------|----------|----------|----------|
| N1 | 提交申请 | 企业申请人 | 企业名称、统一社会信用代码、法人代表、联系电话、注册地址、经营范围 | - | →N2 |
| N2 | 上传资质 | 企业申请人 | 营业执照、燃气经营许可证、安全生产许可证、法人身份证 | - | →N3 |
| N3 | 县区初审 | 县区监管员 | 审核意见、是否通过 | 3个工作日 | 通过→N4，不通过→退回N1 |
| N4 | 市级复审 | 市级监管员 | 审核意见、是否通过 | 2个工作日 | 通过→N5，不通过→退回N3 |
| N5 | 账号开通 | 系统自动 | 生成管理员账号、初始密码 | 即时 | →N6 |
| N6 | 完善资料 | 企业管理员 | 组织架构、安全人员、联系方式 | 7个工作日 | →完成 |

### 2.3 管网数据管理流程

#### 2.3.1 流程图

```
┌─────────────┐
│ 管网数据    │
│ 采集需求    │
└──────┬──────┘
       │
       ├─────────────────┬─────────────────┐
       │新建管网         │管网变更         │管网废弃
       ▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ GIS测绘     │   │ 变更申请    │   │ 废弃申请    │
│ 数据采集    │   │ (企业)     │   │ (企业)     │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │
       ▼                 ▼                 ▼
┌─────────────┐   ┌─────────────┐   ┌─────────────┐
│ 属性数据    │   │ 变更内容    │   │ 废弃原因    │
│ 录入       │   │ 填写       │   │ 说明       │
└──────┬──────┘   └──────┬──────┘   └──────┬──────┘
       │                 │                 │
       └─────────────────┼─────────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ 县区监管员  │
                  │ 审核       │
                  └──────┬──────┘
                         │
                         ├─────────────────┐
                         │通过             │不通过
                         ▼                 ▼
                  ┌─────────────┐   ┌─────────────┐
                  │ GIS数据    │   │ 退回修改    │
                  │ 更新       │   │            │
                  └──────┬──────┘   └─────────────┘
                         │
                         ▼
                  ┌─────────────┐
                  │ 变更记录    │
                  │ 归档       │
                  └─────────────┘
```

#### 2.3.2 管网属性要素

| 要素类型 | 属性字段 | 说明 |
|----------|----------|------|
| 管线基本信息 | 管线编号、管线名称、所属企业、所属区域 | 标识信息 |
| 管线技术参数 | 管径、材质、压力等级、敷设方式、埋深 | 技术规格 |
| 空间信息 | 起点坐标、终点坐标、长度、路由 | GIS数据 |
| 运行状态 | 投运日期、当前状态、使用年限 | 运行信息 |
| 关联信息 | 上游节点、下游节点、附属设施 | 拓扑关系 |

### 2.4 设施台账管理流程

#### 2.4.1 设施分类

```
燃气设施
├── 输配设施
│   ├── 门站
│   ├── 调压站/箱
│   ├── 阀门井
│   └── 凝水缸
├── 场站设施
│   ├── LNG储配站
│   ├── CNG加气站
│   ├── 储罐
│   └── 加臭装置
├── 监测设施
│   ├── 流量计
│   ├── 压力表
│   ├── 泄漏检测仪
│   └── 远传设备
└── 安全设施
    ├── 放散管
    ├── 安全阀
    ├── 紧急切断阀
    └── 消防设施
```

#### 2.4.2 设施生命周期

```
┌─────────────┐
│ 设施采购    │
│ 入库登记    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 安装调试    │
│ 投运验收    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 正常运行    │◄────────┐
│ 日常巡检    │         │
└──────┬──────┘         │
       │                │
       ▼                │
┌─────────────┐  正常    │
│ 定期检测    │─────────┘
│ 维护保养    │
└──────┬──────┘
       │异常
       ▼
┌─────────────┐
│ 维修处理    │
│ 或更换     │
└──────┬──────┘
       │
       ├─────────────────┐
       │维修后           │无法修复
       ▼                 ▼
┌─────────────┐   ┌─────────────┐
│ 恢复运行    │   │ 报废处理    │
│            │   │ 台账注销    │
└─────────────┘   └─────────────┘
```

### 2.5 用户档案管理流程

#### 2.5.1 用户分类

| 用户类型 | 说明 | 管理重点 |
|----------|------|----------|
| 居民用户 | 住宅燃气用户 | 入户安检、燃气表管理 |
| 工商用户 | 餐饮、商业用户 | 用气安全、设备检查 |
| 工业用户 | 工厂、企业用户 | 用气量监控、安全管理 |
| 公福用户 | 学校、医院等 | 重点保障、定期检查 |

#### 2.5.2 用户建档流程

```
┌─────────────┐
│ 用户报装    │
│ 申请       │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 现场勘查    │
│ 条件确认    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 签订合同    │
│ 安装施工    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 通气验收    │
│ 建立档案    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 档案信息    │
│ 录入系统    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 定期安检    │
│ 档案更新    │
└─────────────┘
```

---

## 三、角色使用场景

### 3.1 企业管理员使用场景

#### 场景1：完善企业信息

**操作步骤**：
1. 登录系统，进入企业管理模块
2. 查看企业基本信息
3. 补充完善信息：
   - 企业简介
   - 组织架构图
   - 安全管理人员
   - 应急联系人
   - 服务区域范围
4. 上传相关证照：
   - 营业执照（更新）
   - 燃气经营许可证
   - 安全生产许可证
5. 提交信息变更
6. 等待审核确认

**涉及功能**：企业信息编辑、证照上传、变更审批

#### 场景2：管理管网数据

**操作步骤**：
1. 进入管网管理模块
2. 查看现有管网数据（GIS地图）
3. 录入新建管网：
   - 导入GIS测绘数据
   - 填写管线属性信息
   - 标注附属设施位置
4. 更新已有管网：
   - 选择需要更新的管线
   - 修改属性信息
   - 提交变更申请
5. 查看管网统计：
   - 按压力等级统计
   - 按材质统计
   - 按使用年限统计

**涉及功能**：GIS数据管理、管网属性维护、统计分析

#### 场景3：设施台账管理

**操作步骤**：
1. 进入设施管理模块
2. 查看设施清单
3. 新增设施：
   - 选择设施类型
   - 填写设施基本信息
   - 关联所属管网/场站
   - 上传设施照片
   - 录入技术参数
4. 更新设施状态：
   - 记录维护保养
   - 更新运行状态
   - 记录检测结果
5. 导出设施台账报表

**涉及功能**：设施CRUD、状态管理、报表导出

### 3.2 县区监管员使用场景

#### 场景1：审核企业入驻

**操作步骤**：
1. 查看待审核企业列表
2. 点击进入审核详情
3. 核查企业资料：
   - 核实企业基本信息
   - 验证资质证照有效性
   - 确认经营范围
4. 填写审核意见
5. 选择审核结果（通过/不通过）
6. 提交审核

**涉及功能**：企业审核、资料核验

#### 场景2：管网数据审核

**操作步骤**：
1. 查看待审核的管网变更申请
2. 查看变更内容详情
3. 在GIS地图上查看管网位置
4. 核实变更合理性
5. 填写审核意见
6. 提交审核结果

**涉及功能**：管网变更审核、GIS查看

#### 场景3：辖区资源统计

**操作步骤**：
1. 进入统计分析模块
2. 选择辖区范围
3. 查看资源概览：
   - 企业数量及分布
   - 管网总里程及构成
   - 设施数量及类型分布
   - 用户数量及类型分布
4. 查看详细报表
5. 导出统计报告

**涉及功能**：统计分析、报表导出

### 3.3 市级监管员使用场景

#### 场景1：全市资源总览

**操作步骤**：
1. 进入资源总览页面
2. 查看全市燃气资源分布（GIS地图）
3. 按区域查看：
   - 各县区企业分布
   - 管网覆盖情况
   - 重点设施标注
4. 查看关键指标：
   - 总管网里程
   - 总用户数量
   - 设施完好率
5. 生成分析报告

**涉及功能**：资源总览、GIS可视化、报表生成

#### 场景2：企业复审

**操作步骤**：
1. 查看县区提交的企业审核
2. 复核企业资质材料
3. 确认审核结论
4. 批准或退回

**涉及功能**：企业审核、流程审批

### 3.4 企业安全员使用场景

#### 场景1：更新设施状态

**操作步骤**：
1. 移动端登录系统
2. 扫码或搜索设施
3. 查看设施信息
4. 更新设施状态：
   - 运行状态
   - 最近巡检时间
   - 发现的问题
5. 拍照上传现场照片
6. 提交状态更新

**涉及功能**：移动端设施管理、状态更新

#### 场景2：设施异常上报

**操作步骤**：
1. 发现设施异常
2. 打开移动APP
3. 选择异常上报
4. 填写异常信息：
   - 设施编号
   - 异常类型
   - 异常描述
   - 现场照片
5. 提交上报
6. 跟踪处理进度

**涉及功能**：异常上报、进度跟踪

---

## 四、数据库设计

### 4.1 表清单

| 表名 | 说明 | 数据量级 | 备注 |
|------|------|----------|------|
| gas_enterprise | 燃气企业表 | 100+ | 核心主数据 |
| gas_enterprise_cert | 企业资质证照表 | 500+ | 证照管理 |
| gas_pipeline | 管网管线表 | 1万+ | GIS数据 |
| gas_pipeline_node | 管网节点表 | 5万+ | 拓扑节点 |
| gas_station | 场站信息表 | 200+ | 场站台账 |
| gas_facility | 设施设备表 | 5万+ | 设施台账 |
| gas_facility_maint | 设施维护记录表 | 10万+ | 维护历史 |
| gas_user | 燃气用户表 | 50万+ | 用户档案 |
| gas_user_device | 用户设备表 | 50万+ | 燃气表等 |
| gas_region | 区域信息表 | 100+ | 区域配置 |

### 4.2 核心表结构

#### 4.2.1 燃气企业表（gas_enterprise）

```sql
CREATE TABLE gas_enterprise (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '企业ID',
    enterprise_no VARCHAR(32) NOT NULL COMMENT '企业编号',
    enterprise_name VARCHAR(200) NOT NULL COMMENT '企业名称',
    enterprise_short_name VARCHAR(50) COMMENT '企业简称',
    unified_code VARCHAR(18) NOT NULL COMMENT '统一社会信用代码',
    enterprise_type TINYINT NOT NULL COMMENT '企业类型：1-城镇燃气 2-管道燃气 3-LNG 4-CNG',
    business_scope VARCHAR(500) COMMENT '经营范围',
    legal_person VARCHAR(50) COMMENT '法定代表人',
    legal_person_phone VARCHAR(20) COMMENT '法人电话',
    legal_person_id_card VARCHAR(18) COMMENT '法人身份证号',
    registered_capital DECIMAL(12,2) COMMENT '注册资本(万元)',
    registered_address VARCHAR(200) COMMENT '注册地址',
    office_address VARCHAR(200) COMMENT '办公地址',
    service_area TEXT COMMENT '服务区域（JSON）',
    contact_person VARCHAR(50) COMMENT '联系人',
    contact_phone VARCHAR(20) COMMENT '联系电话',
    contact_email VARCHAR(100) COMMENT '联系邮箱',
    emergency_contact VARCHAR(50) COMMENT '应急联系人',
    emergency_phone VARCHAR(20) COMMENT '应急电话',
    safety_manager VARCHAR(50) COMMENT '安全管理员',
    safety_manager_phone VARCHAR(20) COMMENT '安全管理员电话',
    employee_count INT COMMENT '员工人数',
    safety_staff_count INT COMMENT '安全人员数量',
    establish_date DATE COMMENT '成立日期',
    business_start_date DATE COMMENT '开业日期',
    logo_url VARCHAR(500) COMMENT '企业LOGO',
    introduction TEXT COMMENT '企业简介',
    region_id BIGINT COMMENT '所属区域ID',
    region_name VARCHAR(100) COMMENT '所属区域名称',
    longitude DECIMAL(10,7) COMMENT '经度',
    latitude DECIMAL(10,7) COMMENT '纬度',
    status TINYINT DEFAULT 0 COMMENT '状态：0-待审核 1-正常 2-停业 3-注销',
    audit_status TINYINT DEFAULT 0 COMMENT '审核状态：0-待初审 1-待复审 2-已通过 3-已拒绝',
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
    INDEX idx_enterprise_no (enterprise_no),
    INDEX idx_unified_code (unified_code),
    INDEX idx_region_id (region_id),
    INDEX idx_status (status)
) COMMENT='燃气企业表';
```

#### 4.2.2 企业资质证照表（gas_enterprise_cert）

```sql
CREATE TABLE gas_enterprise_cert (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '证照ID',
    enterprise_id BIGINT NOT NULL COMMENT '企业ID',
    cert_type TINYINT NOT NULL COMMENT '证照类型：1-营业执照 2-燃气经营许可证 3-安全生产许可证 4-其他',
    cert_name VARCHAR(100) NOT NULL COMMENT '证照名称',
    cert_no VARCHAR(100) COMMENT '证照编号',
    issue_org VARCHAR(200) COMMENT '发证机关',
    issue_date DATE COMMENT '发证日期',
    expire_date DATE COMMENT '有效期至',
    cert_file VARCHAR(500) COMMENT '证照文件',
    status TINYINT DEFAULT 1 COMMENT '状态：1-有效 2-即将过期 3-已过期',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_cert_type (cert_type),
    INDEX idx_expire_date (expire_date)
) COMMENT='企业资质证照表';
```

#### 4.2.3 管网管线表（gas_pipeline）

```sql
CREATE TABLE gas_pipeline (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '管线ID',
    pipeline_no VARCHAR(32) NOT NULL COMMENT '管线编号',
    pipeline_name VARCHAR(100) COMMENT '管线名称',
    enterprise_id BIGINT NOT NULL COMMENT '所属企业ID',
    region_id BIGINT COMMENT '所属区域ID',
    pressure_level TINYINT NOT NULL COMMENT '压力等级：1-高压A 2-高压B 3-次高压A 4-次高压B 5-中压A 6-中压B 7-低压',
    diameter DECIMAL(10,2) COMMENT '管径(mm)',
    material TINYINT COMMENT '材质：1-钢管 2-PE管 3-铸铁管 4-其他',
    material_spec VARCHAR(50) COMMENT '材质规格',
    laying_method TINYINT COMMENT '敷设方式：1-直埋 2-架空 3-沟槽 4-顶管',
    burial_depth DECIMAL(5,2) COMMENT '埋深(m)',
    design_pressure DECIMAL(10,2) COMMENT '设计压力(MPa)',
    operating_pressure DECIMAL(10,2) COMMENT '运行压力(MPa)',
    design_flow DECIMAL(10,2) COMMENT '设计流量(m³/h)',
    length DECIMAL(10,2) COMMENT '长度(m)',
    start_point VARCHAR(200) COMMENT '起点描述',
    end_point VARCHAR(200) COMMENT '终点描述',
    start_node_id BIGINT COMMENT '起点节点ID',
    end_node_id BIGINT COMMENT '终点节点ID',
    geom_line TEXT COMMENT 'GIS线型数据(GeoJSON)',
    construct_date DATE COMMENT '建设日期',
    commission_date DATE COMMENT '投运日期',
    design_life INT COMMENT '设计寿命(年)',
    construct_unit VARCHAR(100) COMMENT '建设单位',
    construct_cost DECIMAL(12,2) COMMENT '建设成本(万元)',
    status TINYINT DEFAULT 1 COMMENT '状态：1-在用 2-停用 3-废弃 4-规划中',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_pipeline_no (pipeline_no),
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_region_id (region_id),
    INDEX idx_pressure_level (pressure_level),
    INDEX idx_status (status)
) COMMENT='管网管线表';
```

#### 4.2.4 管网节点表（gas_pipeline_node）

```sql
CREATE TABLE gas_pipeline_node (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '节点ID',
    node_no VARCHAR(32) NOT NULL COMMENT '节点编号',
    node_name VARCHAR(100) COMMENT '节点名称',
    node_type TINYINT NOT NULL COMMENT '节点类型：1-三通 2-四通 3-弯头 4-阀门 5-调压器 6-端点 7-分支点',
    enterprise_id BIGINT NOT NULL COMMENT '所属企业ID',
    region_id BIGINT COMMENT '所属区域ID',
    longitude DECIMAL(10,7) NOT NULL COMMENT '经度',
    latitude DECIMAL(10,7) NOT NULL COMMENT '纬度',
    elevation DECIMAL(8,2) COMMENT '高程(m)',
    address VARCHAR(200) COMMENT '位置描述',
    facility_id BIGINT COMMENT '关联设施ID',
    status TINYINT DEFAULT 1 COMMENT '状态：1-正常 2-异常 3-废弃',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_node_no (node_no),
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_node_type (node_type),
    INDEX idx_facility_id (facility_id)
) COMMENT='管网节点表';
```

#### 4.2.5 场站信息表（gas_station）

```sql
CREATE TABLE gas_station (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '场站ID',
    station_no VARCHAR(32) NOT NULL COMMENT '场站编号',
    station_name VARCHAR(100) NOT NULL COMMENT '场站名称',
    station_type TINYINT NOT NULL COMMENT '场站类型：1-门站 2-调压站 3-LNG储配站 4-CNG加气站 5-LPG灌装站',
    enterprise_id BIGINT NOT NULL COMMENT '所属企业ID',
    region_id BIGINT COMMENT '所属区域ID',
    address VARCHAR(200) COMMENT '场站地址',
    longitude DECIMAL(10,7) COMMENT '经度',
    latitude DECIMAL(10,7) COMMENT '纬度',
    area DECIMAL(10,2) COMMENT '占地面积(m²)',
    storage_capacity DECIMAL(12,2) COMMENT '储存能力(m³)',
    supply_capacity DECIMAL(12,2) COMMENT '供气能力(m³/h)',
    inlet_pressure DECIMAL(10,2) COMMENT '进站压力(MPa)',
    outlet_pressure DECIMAL(10,2) COMMENT '出站压力(MPa)',
    construct_date DATE COMMENT '建设日期',
    commission_date DATE COMMENT '投运日期',
    manager_name VARCHAR(50) COMMENT '站长姓名',
    manager_phone VARCHAR(20) COMMENT '站长电话',
    staff_count INT COMMENT '工作人员数量',
    has_fire_system TINYINT DEFAULT 0 COMMENT '是否有消防系统：0-否 1-是',
    has_video_monitor TINYINT DEFAULT 0 COMMENT '是否有视频监控：0-否 1-是',
    has_alarm_system TINYINT DEFAULT 0 COMMENT '是否有报警系统：0-否 1-是',
    status TINYINT DEFAULT 1 COMMENT '状态：1-运行中 2-停运 3-维护中 4-废弃',
    photos VARCHAR(1000) COMMENT '场站照片（逗号分隔）',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_station_no (station_no),
    INDEX idx_station_type (station_type),
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_region_id (region_id),
    INDEX idx_status (status)
) COMMENT='场站信息表';
```

#### 4.2.6 设施设备表（gas_facility）

```sql
CREATE TABLE gas_facility (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '设施ID',
    facility_no VARCHAR(32) NOT NULL COMMENT '设施编号',
    facility_name VARCHAR(100) NOT NULL COMMENT '设施名称',
    facility_type TINYINT NOT NULL COMMENT '设施类型：1-调压器 2-阀门 3-流量计 4-压力表 5-泄漏检测仪 6-安全阀 7-其他',
    facility_category VARCHAR(50) COMMENT '设施分类',
    enterprise_id BIGINT NOT NULL COMMENT '所属企业ID',
    station_id BIGINT COMMENT '所属场站ID',
    pipeline_id BIGINT COMMENT '关联管线ID',
    node_id BIGINT COMMENT '关联节点ID',
    region_id BIGINT COMMENT '所属区域ID',
    brand VARCHAR(50) COMMENT '品牌',
    model VARCHAR(50) COMMENT '型号',
    spec VARCHAR(100) COMMENT '规格参数',
    manufacturer VARCHAR(100) COMMENT '生产厂家',
    purchase_date DATE COMMENT '采购日期',
    install_date DATE COMMENT '安装日期',
    commission_date DATE COMMENT '投运日期',
    warranty_date DATE COMMENT '质保到期日',
    design_life INT COMMENT '设计寿命(年)',
    location VARCHAR(200) COMMENT '安装位置',
    longitude DECIMAL(10,7) COMMENT '经度',
    latitude DECIMAL(10,7) COMMENT '纬度',
    qr_code VARCHAR(100) COMMENT '二维码',
    photos VARCHAR(1000) COMMENT '设施照片（逗号分隔）',
    documents VARCHAR(1000) COMMENT '相关文档（逗号分隔）',
    last_maint_date DATE COMMENT '最近维护日期',
    next_maint_date DATE COMMENT '下次维护日期',
    maint_cycle INT COMMENT '维护周期(天)',
    status TINYINT DEFAULT 1 COMMENT '状态：1-正常 2-故障 3-维修中 4-报废',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_facility_no (facility_no),
    INDEX idx_facility_type (facility_type),
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_station_id (station_id),
    INDEX idx_pipeline_id (pipeline_id),
    INDEX idx_status (status)
) COMMENT='设施设备表';
```

#### 4.2.7 燃气用户表（gas_user）

```sql
CREATE TABLE gas_user (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '用户ID',
    user_no VARCHAR(32) NOT NULL COMMENT '用户编号',
    user_name VARCHAR(100) NOT NULL COMMENT '用户名称',
    user_type TINYINT NOT NULL COMMENT '用户类型：1-居民 2-工商 3-工业 4-公福',
    enterprise_id BIGINT NOT NULL COMMENT '供气企业ID',
    region_id BIGINT COMMENT '所属区域ID',
    address VARCHAR(200) COMMENT '用气地址',
    longitude DECIMAL(10,7) COMMENT '经度',
    latitude DECIMAL(10,7) COMMENT '纬度',
    contact_name VARCHAR(50) COMMENT '联系人',
    contact_phone VARCHAR(20) COMMENT '联系电话',
    id_card VARCHAR(18) COMMENT '身份证号/统一社会信用代码',
    contract_no VARCHAR(50) COMMENT '合同编号',
    contract_date DATE COMMENT '签约日期',
    open_date DATE COMMENT '开户日期',
    use_nature TINYINT COMMENT '用气性质：1-生活 2-商业 3-工业 4-采暖',
    meter_count INT DEFAULT 1 COMMENT '燃气表数量',
    design_flow DECIMAL(10,2) COMMENT '设计用气量(m³/h)',
    monthly_quota DECIMAL(10,2) COMMENT '月用气限额(m³)',
    last_check_date DATE COMMENT '最近安检日期',
    next_check_date DATE COMMENT '下次安检日期',
    check_cycle INT COMMENT '安检周期(月)',
    risk_level TINYINT DEFAULT 1 COMMENT '风险等级：1-低 2-中 3-高',
    status TINYINT DEFAULT 1 COMMENT '状态：1-正常 2-欠费 3-停用 4-销户',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_user_no (user_no),
    INDEX idx_user_type (user_type),
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_region_id (region_id),
    INDEX idx_status (status)
) COMMENT='燃气用户表';
```

#### 4.2.8 设施维护记录表（gas_facility_maint）

```sql
CREATE TABLE gas_facility_maint (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '记录ID',
    facility_id BIGINT NOT NULL COMMENT '设施ID',
    maint_type TINYINT NOT NULL COMMENT '维护类型：1-日常保养 2-定期检测 3-故障维修 4-更换部件',
    maint_date DATE NOT NULL COMMENT '维护日期',
    maint_content TEXT COMMENT '维护内容',
    maint_result TEXT COMMENT '维护结果',
    problem_found TEXT COMMENT '发现问题',
    solution TEXT COMMENT '处理措施',
    parts_replaced TEXT COMMENT '更换部件',
    maint_cost DECIMAL(10,2) COMMENT '维护费用',
    maint_user_id BIGINT COMMENT '维护人ID',
    maint_user_name VARCHAR(50) COMMENT '维护人姓名',
    maint_unit VARCHAR(100) COMMENT '维护单位',
    photos VARCHAR(1000) COMMENT '维护照片（逗号分隔）',
    next_maint_date DATE COMMENT '下次维护日期',
    status TINYINT DEFAULT 1 COMMENT '状态：1-正常 2-待复检',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_facility_id (facility_id),
    INDEX idx_maint_type (maint_type),
    INDEX idx_maint_date (maint_date)
) COMMENT='设施维护记录表';
```

---

## 五、API接口设计

### 5.1 接口总览

| 模块 | 接口数量 | 基础路径 |
|------|----------|----------|
| 企业管理 | 12个 | /admin-api/gas/resource/enterprise |
| 管网管理 | 10个 | /admin-api/gas/resource/pipeline |
| 场站管理 | 8个 | /admin-api/gas/resource/station |
| 设施管理 | 10个 | /admin-api/gas/resource/facility |
| 用户管理 | 8个 | /admin-api/gas/resource/user |
| 统计分析 | 6个 | /admin-api/gas/resource/statistics |

**共计54个API接口**

### 5.2 企业管理接口

#### 5.2.1 创建企业（入驻申请）

```
POST /admin-api/gas/resource/enterprise/create
```

**请求参数**：
```json
{
    "enterpriseName": "松原市XX燃气有限公司",
    "unifiedCode": "91220700XXXXXXXX",
    "enterpriseType": 1,
    "businessScope": "城镇燃气供应、燃气设施建设...",
    "legalPerson": "张三",
    "legalPersonPhone": "13800138000",
    "registeredAddress": "松原市宁江区XX路XX号",
    "officeAddress": "松原市宁江区XX路XX号",
    "contactPerson": "李四",
    "contactPhone": "13900139000",
    "contactEmail": "xxx@example.com",
    "regionId": 100
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": 1001,
    "msg": "success"
}
```

#### 5.2.2 提交企业审核

```
POST /admin-api/gas/resource/enterprise/submit/{id}
```

#### 5.2.3 审核企业

```
POST /admin-api/gas/resource/enterprise/audit
```

**请求参数**：
```json
{
    "id": 1001,
    "auditResult": 1,
    "auditOpinion": "审核通过"
}
```

#### 5.2.4 获取企业详情

```
GET /admin-api/gas/resource/enterprise/get/{id}
```

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "id": 1001,
        "enterpriseNo": "QY202601270001",
        "enterpriseName": "松原市XX燃气有限公司",
        "unifiedCode": "91220700XXXXXXXX",
        "enterpriseType": 1,
        "enterpriseTypeName": "城镇燃气",
        "legalPerson": "张三",
        "status": 1,
        "statusName": "正常",
        "certs": [
            {
                "certType": 1,
                "certName": "营业执照",
                "expireDate": "2030-12-31",
                "status": 1
            }
        ],
        "statistics": {
            "pipelineLength": 150.5,
            "stationCount": 3,
            "facilityCount": 200,
            "userCount": 50000
        }
    },
    "msg": "success"
}
```

#### 5.2.5 分页查询企业

```
GET /admin-api/gas/resource/enterprise/page
```

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNo | Integer | 否 | 页码，默认1 |
| pageSize | Integer | 否 | 每页条数，默认10 |
| enterpriseName | String | 否 | 企业名称（模糊查询） |
| enterpriseType | Integer | 否 | 企业类型 |
| regionId | Long | 否 | 区域ID |
| status | Integer | 否 | 状态 |

#### 5.2.6 上传企业证照

```
POST /admin-api/gas/resource/enterprise/cert/upload
```

**请求参数**：
```json
{
    "enterpriseId": 1001,
    "certType": 1,
    "certName": "营业执照",
    "certNo": "91220700XXXXXXXX",
    "issueOrg": "松原市市场监督管理局",
    "issueDate": "2020-01-01",
    "expireDate": "2030-12-31",
    "certFile": "cert/business_license.jpg"
}
```

### 5.3 管网管理接口

#### 5.3.1 创建管线

```
POST /admin-api/gas/resource/pipeline/create
```

**请求参数**：
```json
{
    "pipelineName": "XX路中压管线",
    "enterpriseId": 1001,
    "regionId": 100,
    "pressureLevel": 5,
    "diameter": 200,
    "material": 1,
    "layingMethod": 1,
    "burialDepth": 1.2,
    "designPressure": 0.4,
    "length": 1500,
    "startPoint": "XX路与XX街交汇处",
    "endPoint": "XX小区门口",
    "geomLine": "{\"type\":\"LineString\",\"coordinates\":[[124.82,45.17],[124.83,45.18]]}",
    "constructDate": "2020-06-01",
    "commissionDate": "2020-09-01"
}
```

#### 5.3.2 批量导入管线（GIS数据）

```
POST /admin-api/gas/resource/pipeline/import
```

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | MultipartFile | 是 | GIS数据文件（GeoJSON/Shapefile） |
| enterpriseId | Long | 是 | 企业ID |

#### 5.3.3 查询管线列表（带空间范围）

```
GET /admin-api/gas/resource/pipeline/list-by-bounds
```

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| minLng | Double | 是 | 最小经度 |
| minLat | Double | 是 | 最小纬度 |
| maxLng | Double | 是 | 最大经度 |
| maxLat | Double | 是 | 最大纬度 |
| enterpriseId | Long | 否 | 企业ID |
| pressureLevel | Integer | 否 | 压力等级 |

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "properties": {
                    "id": 1001,
                    "pipelineNo": "GX202601270001",
                    "pipelineName": "XX路中压管线",
                    "pressureLevel": 5,
                    "diameter": 200,
                    "material": 1,
                    "status": 1
                },
                "geometry": {
                    "type": "LineString",
                    "coordinates": [[124.82,45.17],[124.83,45.18]]
                }
            }
        ]
    },
    "msg": "success"
}
```

#### 5.3.4 管网统计

```
GET /admin-api/gas/resource/pipeline/statistics
```

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "totalLength": 1500.5,
        "byPressureLevel": {
            "highPressure": 50.2,
            "mediumPressure": 800.3,
            "lowPressure": 650.0
        },
        "byMaterial": {
            "steel": 500.0,
            "pe": 900.5,
            "castIron": 100.0
        },
        "byAge": {
            "lessThan5": 600.0,
            "5to10": 500.0,
            "10to20": 300.5,
            "moreThan20": 100.0
        }
    },
    "msg": "success"
}
```

### 5.4 场站管理接口

#### 5.4.1 创建场站

```
POST /admin-api/gas/resource/station/create
```

**请求参数**：
```json
{
    "stationName": "XX调压站",
    "stationType": 2,
    "enterpriseId": 1001,
    "regionId": 100,
    "address": "松原市宁江区XX路XX号",
    "longitude": 124.825,
    "latitude": 45.172,
    "area": 200,
    "supplyCapacity": 5000,
    "inletPressure": 0.4,
    "outletPressure": 0.2,
    "managerName": "王五",
    "managerPhone": "13700137000",
    "hasFireSystem": 1,
    "hasVideoMonitor": 1,
    "hasAlarmSystem": 1
}
```

#### 5.4.2 获取场站详情（含设施清单）

```
GET /admin-api/gas/resource/station/get/{id}
```

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "id": 2001,
        "stationNo": "CZ202601270001",
        "stationName": "XX调压站",
        "stationType": 2,
        "stationTypeName": "调压站",
        "address": "...",
        "status": 1,
        "statusName": "运行中",
        "facilities": [
            {
                "id": 3001,
                "facilityNo": "SS202601270001",
                "facilityName": "1#调压器",
                "facilityType": 1,
                "status": 1
            }
        ],
        "monitorDevices": [
            {
                "id": 4001,
                "deviceNo": "SB202601270001",
                "deviceName": "进口压力变送器",
                "latestValue": 0.38,
                "unit": "MPa"
            }
        ]
    },
    "msg": "success"
}
```

### 5.5 设施管理接口

#### 5.5.1 创建设施

```
POST /admin-api/gas/resource/facility/create
```

**请求参数**：
```json
{
    "facilityName": "1#调压器",
    "facilityType": 1,
    "enterpriseId": 1001,
    "stationId": 2001,
    "brand": "XX品牌",
    "model": "RTZ-50/0.4",
    "manufacturer": "XX阀门制造有限公司",
    "purchaseDate": "2020-01-01",
    "installDate": "2020-02-01",
    "commissionDate": "2020-03-01",
    "warrantyDate": "2022-03-01",
    "designLife": 15,
    "location": "XX调压站内",
    "longitude": 124.825,
    "latitude": 45.172,
    "maintCycle": 90
}
```

#### 5.5.2 更新设施状态

```
POST /admin-api/gas/resource/facility/update-status
```

**请求参数**：
```json
{
    "facilityId": 3001,
    "status": 2,
    "statusReason": "设备故障，待维修"
}
```

#### 5.5.3 记录设施维护

```
POST /admin-api/gas/resource/facility/maint/create
```

**请求参数**：
```json
{
    "facilityId": 3001,
    "maintType": 2,
    "maintDate": "2026-01-27",
    "maintContent": "定期检测调压器性能...",
    "maintResult": "设备运行正常",
    "problemFound": "无",
    "maintUserName": "张技术",
    "maintUnit": "XX维护公司",
    "photos": ["maint1.jpg", "maint2.jpg"],
    "nextMaintDate": "2026-04-27"
}
```

#### 5.5.4 查询设施维护历史

```
GET /admin-api/gas/resource/facility/maint/list
```

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| facilityId | Long | 是 | 设施ID |
| maintType | Integer | 否 | 维护类型 |
| startDate | String | 否 | 开始日期 |
| endDate | String | 否 | 结束日期 |

### 5.6 用户管理接口

#### 5.6.1 创建用户档案

```
POST /admin-api/gas/resource/user/create
```

**请求参数**：
```json
{
    "userName": "张三",
    "userType": 1,
    "enterpriseId": 1001,
    "regionId": 100,
    "address": "松原市宁江区XX小区3号楼101",
    "longitude": 124.825,
    "latitude": 45.172,
    "contactName": "张三",
    "contactPhone": "13800138000",
    "idCard": "220700199001011234",
    "contractNo": "HT202601270001",
    "contractDate": "2026-01-01",
    "openDate": "2026-01-15",
    "useNature": 1,
    "designFlow": 2.5,
    "checkCycle": 12
}
```

#### 5.6.2 批量导入用户

```
POST /admin-api/gas/resource/user/import
```

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| file | MultipartFile | 是 | Excel文件 |
| enterpriseId | Long | 是 | 企业ID |

#### 5.6.3 用户安检更新

```
POST /admin-api/gas/resource/user/check/update
```

**请求参数**：
```json
{
    "userId": 5001,
    "checkDate": "2026-01-27",
    "checkResult": 1,
    "checkContent": "入户安检，燃气设施正常",
    "problemFound": "无",
    "nextCheckDate": "2027-01-27"
}
```

### 5.7 统计分析接口

#### 5.7.1 资源总览统计

```
GET /admin-api/gas/resource/statistics/overview
```

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| regionId | Long | 否 | 区域ID |

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "enterpriseCount": 15,
        "pipelineLength": 1500.5,
        "stationCount": 50,
        "facilityCount": 5000,
        "userCount": 500000,
        "byRegion": [
            {
                "regionId": 100,
                "regionName": "宁江区",
                "enterpriseCount": 5,
                "pipelineLength": 500.0,
                "userCount": 200000
            }
        ]
    },
    "msg": "success"
}
```

#### 5.7.2 设施状态统计

```
GET /admin-api/gas/resource/statistics/facility-status
```

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "total": 5000,
        "byStatus": {
            "normal": 4800,
            "fault": 50,
            "maintenance": 100,
            "scrapped": 50
        },
        "byType": {
            "regulator": 500,
            "valve": 2000,
            "flowMeter": 1000,
            "pressureGauge": 1000,
            "other": 500
        },
        "overdueMaintenanceCount": 120,
        "upcomingMaintenanceCount": 200
    },
    "msg": "success"
}
```

---

## 六、技术实现要点

### 6.1 GIS数据管理

#### 6.1.1 管网空间数据存储

```java
/**
 * 管网GIS服务
 */
@Service
public class PipelineGisService {

    /**
     * 导入GeoJSON数据
     */
    @Transactional
    public ImportResult importGeoJson(Long enterpriseId, String geoJsonContent) {
        ImportResult result = new ImportResult();

        // 解析GeoJSON
        FeatureCollection featureCollection = GeoJsonUtils.parse(geoJsonContent);

        for (Feature feature : featureCollection.getFeatures()) {
            try {
                // 转换为管线实体
                PipelineDO pipeline = convertToPipeline(enterpriseId, feature);

                // 保存管线
                pipelineMapper.insert(pipeline);

                // 解析并保存节点
                saveNodes(pipeline, feature.getGeometry());

                result.addSuccess();
            } catch (Exception e) {
                result.addFail(feature.getId(), e.getMessage());
            }
        }

        return result;
    }

    /**
     * 按空间范围查询管线
     */
    public List<PipelineGisVO> getPipelinesByBounds(BoundsQuery query) {
        // 构建空间查询条件
        String boundsWkt = String.format(
            "POLYGON((%f %f, %f %f, %f %f, %f %f, %f %f))",
            query.getMinLng(), query.getMinLat(),
            query.getMaxLng(), query.getMinLat(),
            query.getMaxLng(), query.getMaxLat(),
            query.getMinLng(), query.getMaxLat(),
            query.getMinLng(), query.getMinLat()
        );

        // 查询相交的管线
        return pipelineMapper.selectByBounds(boundsWkt, query.getEnterpriseId(), query.getPressureLevel());
    }
}
```

#### 6.1.2 管网拓扑分析

```java
/**
 * 管网拓扑分析服务
 */
@Service
public class PipelineTopologyService {

    /**
     * 分析受影响的下游用户
     */
    public List<Long> analyzeAffectedUsers(Long pipelineId) {
        List<Long> affectedUserIds = new ArrayList<>();

        // 获取管线
        PipelineDO pipeline = pipelineMapper.selectById(pipelineId);

        // BFS遍历下游管线
        Queue<Long> queue = new LinkedList<>();
        Set<Long> visited = new HashSet<>();
        queue.offer(pipeline.getEndNodeId());

        while (!queue.isEmpty()) {
            Long nodeId = queue.poll();
            if (visited.contains(nodeId)) continue;
            visited.add(nodeId);

            // 查找从该节点出发的管线
            List<PipelineDO> downstreamPipelines = pipelineMapper.selectByStartNode(nodeId);
            for (PipelineDO downstream : downstreamPipelines) {
                queue.offer(downstream.getEndNodeId());
            }

            // 查找该节点关联的用户
            List<Long> nodeUsers = userMapper.selectUserIdsByNodeId(nodeId);
            affectedUserIds.addAll(nodeUsers);
        }

        return affectedUserIds;
    }
}
```

### 6.2 数据变更审计

#### 6.2.1 数据变更记录

```java
/**
 * 数据变更审计切面
 */
@Aspect
@Component
public class ResourceAuditAspect {

    @Resource
    private ResourceChangeLogMapper changeLogMapper;

    @Around("@annotation(resourceAudit)")
    public Object around(ProceedingJoinPoint point, ResourceAudit resourceAudit) throws Throwable {
        // 获取变更前数据
        Object oldData = getOldData(point, resourceAudit);

        // 执行方法
        Object result = point.proceed();

        // 获取变更后数据
        Object newData = getNewData(point, resourceAudit, result);

        // 记录变更日志
        saveChangeLog(resourceAudit, oldData, newData);

        return result;
    }

    private void saveChangeLog(ResourceAudit audit, Object oldData, Object newData) {
        ResourceChangeLogDO log = new ResourceChangeLogDO();
        log.setResourceType(audit.resourceType());
        log.setResourceId(getResourceId(newData));
        log.setChangeType(audit.changeType());
        log.setOldData(JsonUtils.toJsonString(oldData));
        log.setNewData(JsonUtils.toJsonString(newData));
        log.setChangeUserId(SecurityFrameworkUtils.getLoginUserId());
        log.setChangeTime(LocalDateTime.now());
        changeLogMapper.insert(log);
    }
}
```

### 6.3 证照到期预警

#### 6.3.1 证照监控任务

```java
/**
 * 证照到期监控任务
 */
@Component
public class CertExpireMonitorJob {

    @Resource
    private EnterpriseCertMapper certMapper;

    @Resource
    private NotifyService notifyService;

    /**
     * 每天检查即将过期的证照
     */
    @Scheduled(cron = "0 0 8 * * ?")
    public void checkCertExpire() {
        // 查询30天内即将过期的证照
        LocalDate expireDate = LocalDate.now().plusDays(30);
        List<EnterpriseCertDO> expiringSoon = certMapper.selectByExpireDateBefore(expireDate);

        for (EnterpriseCertDO cert : expiringSoon) {
            // 更新状态为即将过期
            if (cert.getStatus() == 1) {
                certMapper.updateStatus(cert.getId(), 2);
            }

            // 发送提醒通知
            long daysRemaining = ChronoUnit.DAYS.between(LocalDate.now(), cert.getExpireDate());
            notifyService.sendCertExpireReminder(cert, daysRemaining);
        }

        // 查询已过期的证照
        List<EnterpriseCertDO> expired = certMapper.selectByExpireDateBefore(LocalDate.now());
        for (EnterpriseCertDO cert : expired) {
            if (cert.getStatus() != 3) {
                certMapper.updateStatus(cert.getId(), 3);
                notifyService.sendCertExpiredAlert(cert);
            }
        }
    }
}
```

### 6.4 设施维护提醒

#### 6.4.1 维护计划任务

```java
/**
 * 设施维护提醒任务
 */
@Component
public class FacilityMaintenanceJob {

    /**
     * 每天检查需要维护的设施
     */
    @Scheduled(cron = "0 0 7 * * ?")
    public void checkMaintenanceDue() {
        // 查询7天内需要维护的设施
        LocalDate dueDate = LocalDate.now().plusDays(7);
        List<FacilityDO> facilities = facilityMapper.selectByNextMaintDateBefore(dueDate);

        // 按企业分组
        Map<Long, List<FacilityDO>> byEnterprise = facilities.stream()
            .collect(Collectors.groupingBy(FacilityDO::getEnterpriseId));

        // 发送维护提醒
        for (Map.Entry<Long, List<FacilityDO>> entry : byEnterprise.entrySet()) {
            notifyService.sendMaintenanceReminder(entry.getKey(), entry.getValue());
        }
    }
}
```

### 6.5 数据质量检查

#### 6.5.1 数据完整性检查

```java
/**
 * 数据质量检查服务
 */
@Service
public class DataQualityService {

    /**
     * 检查企业数据完整性
     */
    public DataQualityReport checkEnterpriseData(Long enterpriseId) {
        DataQualityReport report = new DataQualityReport();

        EnterpriseDO enterprise = enterpriseMapper.selectById(enterpriseId);

        // 检查必填字段
        if (StringUtils.isBlank(enterprise.getEmergencyContact())) {
            report.addIssue("enterprise", "应急联系人未填写");
        }
        if (StringUtils.isBlank(enterprise.getSafetyManager())) {
            report.addIssue("enterprise", "安全管理员未填写");
        }

        // 检查证照完整性
        List<EnterpriseCertDO> certs = certMapper.selectByEnterpriseId(enterpriseId);
        Set<Integer> certTypes = certs.stream()
            .map(EnterpriseCertDO::getCertType)
            .collect(Collectors.toSet());

        if (!certTypes.contains(1)) {
            report.addIssue("cert", "缺少营业执照");
        }
        if (!certTypes.contains(2)) {
            report.addIssue("cert", "缺少燃气经营许可证");
        }

        // 检查管网数据
        long pipelineCount = pipelineMapper.countByEnterpriseId(enterpriseId);
        if (pipelineCount == 0) {
            report.addIssue("pipeline", "未录入管网数据");
        }

        // 检查场站数据
        long stationCount = stationMapper.countByEnterpriseId(enterpriseId);
        if (stationCount == 0) {
            report.addIssue("station", "未录入场站数据");
        }

        return report;
    }
}
```

---

## 七、附录

### 7.1 错误码定义

```java
public interface ResourceErrorCodeConstants {

    // ========== 企业模块 1-006-001-xxx ==========
    ErrorCode ENTERPRISE_NOT_EXISTS = new ErrorCode(1_006_001_001, "企业不存在");
    ErrorCode ENTERPRISE_NAME_EXISTS = new ErrorCode(1_006_001_002, "企业名称已存在");
    ErrorCode ENTERPRISE_CODE_EXISTS = new ErrorCode(1_006_001_003, "统一社会信用代码已存在");
    ErrorCode ENTERPRISE_STATUS_ERROR = new ErrorCode(1_006_001_004, "企业状态错误");
    ErrorCode ENTERPRISE_AUDIT_ERROR = new ErrorCode(1_006_001_005, "企业审核状态错误");

    // ========== 管网模块 1-006-002-xxx ==========
    ErrorCode PIPELINE_NOT_EXISTS = new ErrorCode(1_006_002_001, "管线不存在");
    ErrorCode PIPELINE_NO_EXISTS = new ErrorCode(1_006_002_002, "管线编号已存在");
    ErrorCode PIPELINE_GEOM_INVALID = new ErrorCode(1_006_002_003, "管线空间数据无效");

    // ========== 场站模块 1-006-003-xxx ==========
    ErrorCode STATION_NOT_EXISTS = new ErrorCode(1_006_003_001, "场站不存在");
    ErrorCode STATION_NO_EXISTS = new ErrorCode(1_006_003_002, "场站编号已存在");

    // ========== 设施模块 1-006-004-xxx ==========
    ErrorCode FACILITY_NOT_EXISTS = new ErrorCode(1_006_004_001, "设施不存在");
    ErrorCode FACILITY_NO_EXISTS = new ErrorCode(1_006_004_002, "设施编号已存在");
    ErrorCode FACILITY_STATUS_ERROR = new ErrorCode(1_006_004_003, "设施状态错误");

    // ========== 用户模块 1-006-005-xxx ==========
    ErrorCode GAS_USER_NOT_EXISTS = new ErrorCode(1_006_005_001, "用户不存在");
    ErrorCode GAS_USER_NO_EXISTS = new ErrorCode(1_006_005_002, "用户编号已存在");
}
```

### 7.2 数据字典

| 字典编码 | 字典名称 | 字典值 |
|----------|----------|--------|
| gas_enterprise_type | 企业类型 | 1-城镇燃气, 2-管道燃气, 3-LNG, 4-CNG |
| gas_enterprise_status | 企业状态 | 0-待审核, 1-正常, 2-停业, 3-注销 |
| gas_cert_type | 证照类型 | 1-营业执照, 2-燃气经营许可证, 3-安全生产许可证, 4-其他 |
| gas_pressure_level | 压力等级 | 1-高压A, 2-高压B, 3-次高压A, 4-次高压B, 5-中压A, 6-中压B, 7-低压 |
| gas_pipe_material | 管材材质 | 1-钢管, 2-PE管, 3-铸铁管, 4-其他 |
| gas_laying_method | 敷设方式 | 1-直埋, 2-架空, 3-沟槽, 4-顶管 |
| gas_station_type | 场站类型 | 1-门站, 2-调压站, 3-LNG储配站, 4-CNG加气站, 5-LPG灌装站 |
| gas_facility_type | 设施类型 | 1-调压器, 2-阀门, 3-流量计, 4-压力表, 5-泄漏检测仪, 6-安全阀, 7-其他 |
| gas_facility_status | 设施状态 | 1-正常, 2-故障, 3-维修中, 4-报废 |
| gas_user_type | 用户类型 | 1-居民, 2-工商, 3-工业, 4-公福 |
| gas_use_nature | 用气性质 | 1-生活, 2-商业, 3-工业, 4-采暖 |

### 7.3 权限标识

| 模块 | 权限标识 | 说明 |
|------|----------|------|
| 企业管理 | gas:resource:enterprise:create | 创建企业 |
| 企业管理 | gas:resource:enterprise:update | 编辑企业 |
| 企业管理 | gas:resource:enterprise:delete | 删除企业 |
| 企业管理 | gas:resource:enterprise:query | 查询企业 |
| 企业管理 | gas:resource:enterprise:audit | 审核企业 |
| 管网管理 | gas:resource:pipeline:create | 创建管线 |
| 管网管理 | gas:resource:pipeline:update | 编辑管线 |
| 管网管理 | gas:resource:pipeline:delete | 删除管线 |
| 管网管理 | gas:resource:pipeline:query | 查询管线 |
| 管网管理 | gas:resource:pipeline:import | 导入管线 |
| 场站管理 | gas:resource:station:create | 创建场站 |
| 场站管理 | gas:resource:station:update | 编辑场站 |
| 场站管理 | gas:resource:station:delete | 删除场站 |
| 场站管理 | gas:resource:station:query | 查询场站 |
| 设施管理 | gas:resource:facility:create | 创建设施 |
| 设施管理 | gas:resource:facility:update | 编辑设施 |
| 设施管理 | gas:resource:facility:delete | 删除设施 |
| 设施管理 | gas:resource:facility:query | 查询设施 |
| 用户管理 | gas:resource:user:create | 创建用户 |
| 用户管理 | gas:resource:user:update | 编辑用户 |
| 用户管理 | gas:resource:user:delete | 删除用户 |
| 用户管理 | gas:resource:user:query | 查询用户 |
| 用户管理 | gas:resource:user:import | 导入用户 |
| 统计分析 | gas:resource:statistics:query | 查询统计 |

### 7.4 与其他领域的关系

| 关联领域 | 关联方式 | 说明 |
|----------|----------|------|
| 监测预警域 | 数据提供 | 提供设备关联的管网、场站信息 |
| 巡查防控域 | 数据提供 | 提供巡查对象（管网、设施、用户）信息 |
| 应急调度域 | 数据提供 | 提供应急资源（专家、队伍、物资）信息 |
| 统计分析域 | 数据提供 | 提供资源基础数据用于统计分析 |
| GIS可视化 | 数据提供 | 提供管网、场站、设施的空间数据 |

### 7.5 相关文档

- [ruoyi-vue-pro 系统模块](../skills/ruoyi-vue-pro/system.md)
- [ruoyi-vue-pro 基础设施](../skills/ruoyi-vue-pro/infra.md)
- [整体架构规划](./00-overall-architecture.md)
- [监测预警域设计](./01-monitoring-domain.md)
- [巡查防控域设计](./02-patrol-domain.md)
- [应急调度域设计](./03-emergency-domain.md)

---

*文档版本: 1.0.0*
*最后更新: 2026-01-27*
*状态: 规划中*


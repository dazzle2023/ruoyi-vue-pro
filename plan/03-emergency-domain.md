# 应急调度域详细设计

> 松原市燃气安全监管平台 - 应急调度域
>
> 版本: 1.0.0
> 更新时间: 2026-01-27
> 状态: 规划中

---

## 一、领域概述

### 1.1 业务价值

应急调度域是松原市燃气安全监管平台的**核心域**，承担着应急事件的快速响应、资源调度和协同处置的核心职责。通过预警发布、应急指挥、资源协调、预案管理和演练评估，构建"预防-响应-处置-恢复"全流程应急管理体系。

### 1.2 功能范围

| 功能模块 | 功能点 | 需求编号 |
|----------|--------|----------|
| 预警管理 | 预警编辑、预警发布、预警推送、预警附件、预警详情、预警升级、预警复核、预警解除 | 60-63, 69-72 |
| 事件处置 | 突发事件发布、事件处置、警情总览、预警事件统计 | 64-68 |
| 预案管理 | 总体预案制定、预案数据结构化 | 79-80 |
| 资源管理 | 专家资源、消防资源、物资资源、医疗队伍、应急队伍、资源统计 | 73-78 |
| 演练管理 | 应急演练管理 | 81 |
| 联动响应 | 跨地区联动响应 | 82 |
| 预警等级 | 预警等级管理 | 67 |

**共覆盖23项功能需求**

### 1.3 核心角色

| 角色 | 职责 | 主要操作 |
|------|------|----------|
| 市级调度员 | 全市应急指挥、资源协调 | 发布预警、指挥调度、跨区联动 |
| 市级监管员 | 预警审核、协调配合 | 编辑预警、审核预案、协调资源 |
| 县区调度员 | 辖区应急响应、资源调配 | 响应预警、调配资源、上报事件 |
| 企业负责人 | 企业应急响应、配合处置 | 审批预案、配合应急、组织演练 |
| 企业安全员 | 现场处置执行 | 上报事件、执行处置、记录过程 |
| 应急专家 | 技术支持、会商决策 | 参与会商、提供建议、分析事故 |

---

## 二、业务流程设计

### 2.1 核心业务流程总览

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           应急调度域核心业务流程                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          日常准备阶段                                      │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │  │
│  │  │ 预案制定  │    │ 资源管理  │    │ 队伍建设  │    │ 应急演练  │          │  │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼ 事件发生                                  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          应急响应阶段                                      │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │  │
│  │  │ 事件上报  │───►│ 等级研判  │───►│ 预警发布  │───►│ 启动预案  │          │  │
│  │  │ (企业)   │    │ (调度)   │    │ (审批)   │    │ (响应)   │          │  │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          应急处置阶段                                      │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │  │
│  │  │ 资源调度  │───►│ 现场处置  │───►│ 进度跟踪  │───►│ 专家会商  │          │  │
│  │  │ (调度)   │    │ (企业)   │    │ (监控)   │    │ (决策)   │          │  │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼ 情况控制                                  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          恢复结束阶段                                      │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │  │
│  │  │ 预警解除  │───►│ 事件结案  │───►│ 总结评估  │───►│ 归档备查  │          │  │
│  │  │ (审批)   │    │ (确认)   │    │ (分析)   │    │ (存档)   │          │  │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 预警发布流程（核心流程）

#### 2.2.1 流程图

```
┌─────────────┐
│ 风险事件    │
│ 触发       │
└──────┬──────┘
       │
       ├─────────────────────────────────┐
       │设备报警触发                      │人工上报
       ▼                                 ▼
┌─────────────┐                   ┌─────────────┐
│ 监测预警域  │                   │ 企业安全员  │
│ 自动推送    │                   │ 上报事件    │
└──────┬──────┘                   └──────┬──────┘
       │                                 │
       └──────────┬──────────────────────┘
                  ▼
           ┌─────────────┐
           │ 县区调度员  │
           │ 接收研判    │
           └──────┬──────┘
                  │
                  ▼
           ┌─────────────┐
           │ 判定预警等级│
           │ (四级标准)  │
           └──────┬──────┘
                  │
       ┌──────────┼──────────┬──────────┐
       │蓝色      │黄色      │橙色/红色 │
       ▼          ▼          ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ 县区发布    │ │ 市级审核    │ │ 市级领导    │
│ (县区权限) │ │ 后发布     │ │ 审批后发布  │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │              │              │
       └──────────────┼──────────────┘
                      ▼
               ┌─────────────┐
               │ 预警信息    │
               │ 正式发布    │
               └──────┬──────┘
                      │
                      ▼
               ┌─────────────┐
               │ 多渠道推送  │
               │ (短信/APP)  │
               └──────┬──────┘
                      │
                      ▼
               ┌─────────────┐
               │ 启动响应    │
               │ 调度资源    │
               └─────────────┘
```

#### 2.2.2 预警等级定义

| 等级 | 颜色 | 名称 | 定义 | 发布权限 | 响应级别 |
|------|------|------|------|----------|----------|
| Ⅳ级 | 蓝色 | 一般 | 可能发生一般燃气事故 | 县区调度员 | 县区响应 |
| Ⅲ级 | 黄色 | 较大 | 可能发生较大燃气事故 | 市级监管员审核 | 市县联动 |
| Ⅱ级 | 橙色 | 重大 | 可能发生重大燃气事故 | 市级领导审批 | 全市响应 |
| Ⅰ级 | 红色 | 特别重大 | 可能发生特别重大事故 | 市级领导审批 | 跨区联动 |

#### 2.2.3 流程节点详情

| 节点编号 | 节点名称 | 处理人 | 表单字段 | 时限要求 | 流转规则 |
|----------|----------|--------|----------|----------|----------|
| N1 | 事件上报 | 企业安全员 | 事件类型、事件描述、发生时间、位置信息、初步影响评估、现场照片 | 即时 | →N2 |
| N2 | 接收研判 | 县区调度员 | 确认情况、初步等级判定、预警建议 | 15分钟 | →N3 |
| N3 | 等级判定 | 县区/市级调度员 | 预警等级、判定依据、影响范围 | 10分钟 | 蓝色→N4a，黄色→N4b，橙红→N4c |
| N4a | 县区发布 | 县区调度员 | 预警标题、预警内容、应对措施、通知范围 | 10分钟 | →N5 |
| N4b | 市级审核 | 市级监管员 | 审核意见、是否调整等级 | 15分钟 | 通过→N5，调整→N3 |
| N4c | 市级审批 | 市级领导 | 审批意见、是否同意发布 | 20分钟 | 同意→N5，不同意→N4b |
| N5 | 正式发布 | 系统自动 | 发布时间、发布渠道 | - | →N6 |
| N6 | 消息推送 | 系统自动 | 推送对象、推送渠道、推送结果 | - | →N7 |
| N7 | 启动响应 | 相关人员 | 响应确认、资源调度 | 根据等级 | →处置流程 |

### 2.3 应急处置流程

#### 2.3.1 流程图

```
┌─────────────┐
│ 预警发布    │
│ 响应启动    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 启动应急预案│
│ (匹配预案)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 成立指挥部  │
│ (明确职责)  │
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────────────────┐
│                 资源调度                      │
│  ┌─────────┐ ┌─────────┐ ┌─────────┐       │
│  │ 人员调度 │ │ 物资调度 │ │ 设备调度 │       │
│  └─────────┘ └─────────┘ └─────────┘       │
└─────────────────────┬───────────────────────┘
                      │
                      ▼
               ┌─────────────┐
               │ 现场处置    │◄──────┐
               │ (企业执行)  │       │
               └──────┬──────┘       │
                      │              │
                      ▼              │
               ┌─────────────┐       │
               │ 进度上报    │       │
               │ (实时反馈)  │       │
               └──────┬──────┘       │
                      │              │
                      ▼              │
               ┌─────────────┐  需调整 │
               │ 情况评估    │───────┘
               │ (动态研判)  │
               └──────┬──────┘
                      │
       ┌──────────────┼──────────────┐
       │情况恶化      │情况可控      │情况消除
       ▼              ▼              ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│ 预警升级    │ │ 继续处置    │ │ 预警解除    │
│ 扩大响应    │ │ 持续监控    │ │ 恢复正常    │
└──────┬──────┘ └──────┬──────┘ └──────┬──────┘
       │              │              │
       └──────────────┴──────────────┘
                      │
                      ▼
               ┌─────────────┐
               │ 事件结案    │
               │ 总结归档    │
               └─────────────┘
```

#### 2.3.2 指挥层级

```
                    ┌─────────────────────┐
                    │     市级指挥部      │
                    │   (红色/橙色预警)   │
                    │ 市领导、市调度员    │
                    └──────────┬──────────┘
                               │
              ┌────────────────┼────────────────┐
              ▼                ▼                ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │  县区分部   │  │  县区分部   │  │  县区分部   │
     │ 县区调度员  │  │ 县区调度员  │  │ 县区调度员  │
     └──────┬──────┘  └──────┬──────┘  └──────┬──────┘
            │                │                │
            ▼                ▼                ▼
     ┌─────────────┐  ┌─────────────┐  ┌─────────────┐
     │ 企业现场组  │  │ 企业现场组  │  │ 企业现场组  │
     │ 企业负责人  │  │ 企业负责人  │  │ 企业负责人  │
     │ 安全员     │  │ 安全员     │  │ 安全员     │
     └─────────────┘  └─────────────┘  └─────────────┘
```

### 2.4 预案管理流程

#### 2.4.1 预案编制流程

```
┌─────────────┐
│ 编制需求    │
│ (新增/修订) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 起草预案    │
│ (企业/政府) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 预案结构化  │
│ (要素提取)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐    不通过    ┌─────────────┐
│ 初审       │───────────►│ 修改完善    │
│ (安全管理员)│            └─────────────┘
└──────┬──────┘
       │通过
       ▼
┌─────────────┐    不通过
│ 复审       │───────────►退回修改
│ (县区监管员)│
└──────┬──────┘
       │通过
       ▼
┌─────────────┐    不通过
│ 终审       │───────────►退回修改
│ (市级监管员)│
└──────┬──────┘
       │通过
       ▼
┌─────────────┐
│ 发布实施    │
│ (版本管理)  │
└─────────────┘
```

#### 2.4.2 预案结构化要素

| 要素类型 | 要素内容 | 说明 |
|----------|----------|------|
| 基本信息 | 预案名称、编号、版本、适用范围 | 预案标识 |
| 组织体系 | 指挥机构、工作组、职责分工 | 组织架构 |
| 响应程序 | 响应条件、响应级别、响应流程 | 响应规则 |
| 处置措施 | 先期处置、专业处置、恢复重建 | 操作指南 |
| 资源保障 | 人员队伍、物资装备、资金保障 | 资源清单 |
| 附则 | 名词解释、预案解释、实施日期 | 补充说明 |

### 2.5 应急演练流程

#### 2.5.1 流程图

```
┌─────────────┐
│ 制定演练计划│
│ (年度/专项) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 编制演练方案│
│ (脚本设计)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 方案审批    │
│ (领导审批)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 演练准备    │
│ (资源协调)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 演练实施    │
│ (按脚本)    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 过程记录    │
│ (照片/视频) │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 演练评估    │
│ (效果分析)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 总结改进    │
│ (完善预案)  │
└─────────────┘
```

#### 2.5.2 演练类型

| 演练类型 | 说明 | 频次 | 参与范围 |
|----------|------|------|----------|
| 桌面演练 | 室内推演，讨论式 | 每季度 | 指挥人员 |
| 实战演练 | 现场实操，全流程 | 每半年 | 全体人员 |
| 专项演练 | 针对特定场景 | 按需 | 相关人员 |
| 综合演练 | 多部门联合 | 每年 | 跨部门 |

### 2.6 跨地区联动流程

#### 2.6.1 流程说明

当应急事件影响范围超出本市或需要外部支援时，启动跨地区联动响应。

#### 2.6.2 联动流程

```
┌─────────────┐
│ 本市事件    │
│ 需外部支援  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 市级指挥部  │
│ 决策联动    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 向上级报告  │
│ 请求支援    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 省级协调    │
│ 调配资源    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 周边城市    │
│ 响应支援    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 资源到位    │
│ 协同处置    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 事件处置    │
│ 完成撤离    │
└─────────────┘
```

---

## 三、角色使用场景

### 3.1 市级调度员使用场景

#### 场景1：发布重大预警

**操作步骤**：
1. 接收县区上报的重大事件
2. 查看事件详情和现场信息
3. 组织专家进行等级研判
4. 确定预警等级（橙色/红色）
5. 编制预警信息：
   - 预警标题
   - 事件描述
   - 影响范围
   - 应对措施
   - 注意事项
6. 提交市级领导审批
7. 审批通过后正式发布
8. 系统自动推送给相关人员
9. 启动应急响应机制

**涉及功能**：预警编辑、等级判定、审批流程、消息推送

#### 场景2：应急资源调度

**操作步骤**：
1. 进入应急指挥界面
2. 查看事件位置和影响范围（GIS地图）
3. 查看周边可用资源：
   - 应急队伍位置和状态
   - 应急物资库存和位置
   - 专家资源和联系方式
4. 选择需要调度的资源
5. 下达调度指令：
   - 指定到达地点
   - 要求到达时间
   - 携带装备清单
6. 跟踪资源调度进度
7. 确认资源到位情况

**涉及功能**：GIS可视化、资源查询、调度指令、进度跟踪

#### 场景3：跨地区联动协调

**操作步骤**：
1. 判断需要外部支援
2. 编制支援请求：
   - 事件情况说明
   - 需要的支援类型
   - 需要的资源数量
3. 通过系统向省级平台发送请求
4. 接收省级协调结果
5. 与支援城市对接：
   - 确认支援资源
   - 协调到达时间
   - 安排接应事宜
6. 跟踪支援资源到位
7. 协同开展应急处置

**涉及功能**：联动请求、跨区协调、资源对接

### 3.2 县区调度员使用场景

#### 场景1：上报应急事件

**操作步骤**：
1. 接收企业上报的突发事件
2. 核实事件情况（电话/现场）
3. 进行初步等级研判
4. 填写事件上报表单：
   - 事件类型
   - 发生时间和地点
   - 事件描述
   - 初步影响评估
   - 已采取措施
   - 现场照片/视频
5. 判定预警等级建议
6. 提交给市级调度员
7. 等待市级指令
8. 执行应急响应

**涉及功能**：事件上报、等级研判、照片上传

#### 场景2：辖区应急响应

**操作步骤**：
1. 接收预警通知
2. 启动辖区应急预案
3. 成立现场指挥部
4. 调配辖区应急资源：
   - 通知应急队伍集结
   - 调拨应急物资
   - 联系相关专家
5. 指挥现场处置
6. 定时向市级上报进度
7. 根据市级指令调整措施
8. 事件结束后汇报结果

**涉及功能**：预警接收、预案启动、资源调度、进度上报

### 3.3 企业安全员使用场景

#### 场景1：上报突发事件

**操作步骤**：
1. 发现突发事件（泄漏、火灾等）
2. 立即采取先期处置措施
3. 打开移动APP上报事件
4. 填写事件信息：
   - 事件类型（下拉选择）
   - 发生时间（自动获取）
   - 发生地点（GPS定位）
   - 事件描述（语音输入）
   - 现场照片（拍照上传）
   - 人员伤亡情况
   - 已采取措施
5. 提交上报
6. 等待上级指令
7. 按指令执行处置

**涉及功能**：事件上报（移动端）、GPS定位、照片上传、语音输入

#### 场景2：执行应急处置

**操作步骤**：
1. 接收应急指令
2. 查看处置要求和注意事项
3. 组织人员执行处置：
   - 疏散人员
   - 关闭阀门
   - 设置警戒
   - 联系专业队伍
4. 实时上报处置进度（移动端）
5. 拍照记录处置过程
6. 填写处置记录
7. 提交处置报告

**涉及功能**：指令接收、进度上报、照片记录、报告提交

### 3.4 应急专家使用场景

#### 场景1：参与应急会商

**操作步骤**：
1. 接收会商邀请通知
2. 登录系统查看事件资料：
   - 事件基本情况
   - 现场照片/视频
   - 监测数据
   - 已采取措施
3. 进行专业分析和研判
4. 参加线上/线下会商会议
5. 提出专业意见和建议：
   - 风险分析
   - 处置建议
   - 注意事项
6. 填写专家意见表
7. 提交会商结论

**涉及功能**：会商邀请、资料查看、意见提交

#### 场景2：事故分析评估

**操作步骤**：
1. 接收事故分析任务
2. 查看事故完整资料
3. 进行技术分析：
   - 事故原因分析
   - 事故过程还原
   - 责任认定建议
   - 防范措施建议
4. 编写分析报告
5. 提交评估结论

**涉及功能**：资料查询、报告编写、结论提交

### 3.5 企业负责人使用场景

#### 场景1：审批应急预案

**操作步骤**：
1. 接收预案审批通知
2. 查看预案内容：
   - 预案适用范围
   - 组织体系
   - 响应程序
   - 处置措施
   - 资源保障
3. 评估预案可行性
4. 提出修改意见（如有）
5. 审批通过或退回修改
6. 签字确认

**涉及功能**：预案审批、意见反馈

#### 场景2：组织应急演练

**操作步骤**：
1. 审批演练计划
2. 协调演练资源
3. 参与演练实施
4. 观察演练过程
5. 评价演练效果
6. 提出改进要求

**涉及功能**：演练管理、效果评估

---

## 四、数据库设计

### 4.1 表清单

| 表名 | 说明 | 数据量级 | 备注 |
|------|------|----------|------|
| gas_emergency_warning | 预警信息表 | 1万+ | 核心业务表 |
| gas_emergency_event | 应急事件表 | 5000+ | 核心业务表 |
| gas_emergency_plan | 应急预案表 | 500+ | 配置表 |
| gas_emergency_plan_element | 预案要素表 | 5000+ | 结构化数据 |
| gas_emergency_resource | 应急资源表 | 1万+ | 资源台账 |
| gas_emergency_team | 应急队伍表 | 500+ | 队伍管理 |
| gas_emergency_expert | 应急专家表 | 200+ | 专家库 |
| gas_emergency_drill | 应急演练表 | 1000+ | 演练记录 |
| gas_emergency_dispatch | 资源调度记录表 | 1万+ | 调度记录 |
| gas_emergency_linkage | 跨区联动记录表 | 100+ | 联动记录 |

### 4.2 核心表结构

#### 4.2.1 预警信息表（gas_emergency_warning）

```sql
CREATE TABLE gas_emergency_warning (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '预警ID',
    warning_no VARCHAR(32) NOT NULL COMMENT '预警编号',
    warning_title VARCHAR(200) NOT NULL COMMENT '预警标题',
    warning_type TINYINT NOT NULL COMMENT '预警类型：1-泄漏 2-火灾 3-爆炸 4-中毒 5-其他',
    warning_level TINYINT NOT NULL COMMENT '预警等级：1-蓝色 2-黄色 3-橙色 4-红色',
    warning_content TEXT NOT NULL COMMENT '预警内容',
    event_location VARCHAR(200) COMMENT '事件位置',
    event_longitude DECIMAL(10,7) COMMENT '经度',
    event_latitude DECIMAL(10,7) COMMENT '纬度',
    influence_scope TEXT COMMENT '影响范围',
    response_measures TEXT COMMENT '应对措施',
    precautions TEXT COMMENT '注意事项',
    attachments VARCHAR(1000) COMMENT '附件（逗号分隔）',
    source_type TINYINT COMMENT '来源类型：1-监测报警 2-人工上报 3-其他',
    source_id BIGINT COMMENT '来源ID',
    report_user_id BIGINT COMMENT '上报人ID',
    report_time DATETIME COMMENT '上报时间',
    draft_user_id BIGINT COMMENT '编辑人ID',
    draft_time DATETIME COMMENT '编辑时间',
    publish_user_id BIGINT COMMENT '发布人ID',
    publish_time DATETIME COMMENT '发布时间',
    status TINYINT DEFAULT 0 COMMENT '状态：0-草稿 1-待审批 2-已发布 3-已升级 4-已解除',
    is_upgraded TINYINT DEFAULT 0 COMMENT '是否升级：0-否 1-是',
    upgrade_from_id BIGINT COMMENT '升级自预警ID',
    is_cancelled TINYINT DEFAULT 0 COMMENT '是否解除：0-否 1-是',
    cancel_time DATETIME COMMENT '解除时间',
    cancel_reason TEXT COMMENT '解除原因',
    notify_users TEXT COMMENT '通知人员ID（JSON数组）',
    notify_result TEXT COMMENT '通知结果（JSON）',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_warning_no (warning_no),
    INDEX idx_warning_level (warning_level),
    INDEX idx_status (status),
    INDEX idx_publish_time (publish_time)
) COMMENT='预警信息表';
```

#### 4.2.2 应急事件表（gas_emergency_event）

```sql
CREATE TABLE gas_emergency_event (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '事件ID',
    event_no VARCHAR(32) NOT NULL COMMENT '事件编号',
    event_title VARCHAR(200) NOT NULL COMMENT '事件标题',
    event_type TINYINT NOT NULL COMMENT '事件类型：1-泄漏 2-火灾 3-爆炸 4-中毒 5-其他',
    event_level TINYINT COMMENT '事件等级：1-一般 2-较大 3-重大 4-特别重大',
    event_description TEXT NOT NULL COMMENT '事件描述',
    event_location VARCHAR(200) COMMENT '事件位置',
    event_longitude DECIMAL(10,7) COMMENT '经度',
    event_latitude DECIMAL(10,7) COMMENT '纬度',
    occur_time DATETIME NOT NULL COMMENT '发生时间',
    report_time DATETIME NOT NULL COMMENT '上报时间',
    enterprise_id BIGINT COMMENT '涉及企业ID',
    facility_id BIGINT COMMENT '涉及设施ID',
    casualties TEXT COMMENT '人员伤亡情况（JSON）',
    property_loss TEXT COMMENT '财产损失情况',
    influence_scope TEXT COMMENT '影响范围',
    taken_measures TEXT COMMENT '已采取措施',
    event_photos VARCHAR(1000) COMMENT '现场照片（逗号分隔）',
    event_videos VARCHAR(1000) COMMENT '现场视频（逗号分隔）',
    report_user_id BIGINT NOT NULL COMMENT '上报人ID',
    report_user_name VARCHAR(50) COMMENT '上报人姓名',
    warning_id BIGINT COMMENT '关联预警ID',
    plan_id BIGINT COMMENT '启动预案ID',
    commander_id BIGINT COMMENT '现场指挥ID',
    status TINYINT DEFAULT 0 COMMENT '状态：0-待研判 1-处置中 2-已控制 3-已结案',
    close_time DATETIME COMMENT '结案时间',
    close_summary TEXT COMMENT '结案总结',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_event_no (event_no),
    INDEX idx_event_level (event_level),
    INDEX idx_status (status),
    INDEX idx_occur_time (occur_time)
) COMMENT='应急事件表';
```

#### 4.2.3 应急预案表（gas_emergency_plan）

```sql
CREATE TABLE gas_emergency_plan (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '预案ID',
    plan_no VARCHAR(32) NOT NULL COMMENT '预案编号',
    plan_name VARCHAR(200) NOT NULL COMMENT '预案名称',
    plan_type TINYINT NOT NULL COMMENT '预案类型：1-综合预案 2-专项预案 3-现场处置方案',
    plan_level TINYINT NOT NULL COMMENT '预案级别：1-市级 2-县区级 3-企业级',
    applicable_scope TEXT COMMENT '适用范围',
    plan_content TEXT COMMENT '预案内容',
    plan_file VARCHAR(500) COMMENT '预案文件',
    version VARCHAR(20) COMMENT '版本号',
    is_structured TINYINT DEFAULT 0 COMMENT '是否结构化：0-否 1-是',
    enterprise_id BIGINT COMMENT '所属企业ID（企业级预案）',
    draft_user_id BIGINT COMMENT '起草人ID',
    draft_time DATETIME COMMENT '起草时间',
    review_user_id BIGINT COMMENT '审核人ID',
    review_time DATETIME COMMENT '审核时间',
    approve_user_id BIGINT COMMENT '批准人ID',
    approve_time DATETIME COMMENT '批准时间',
    publish_time DATETIME COMMENT '发布时间',
    effective_date DATE COMMENT '生效日期',
    expire_date DATE COMMENT '失效日期',
    status TINYINT DEFAULT 0 COMMENT '状态：0-草稿 1-待审核 2-待批准 3-已发布 4-已失效',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_plan_no (plan_no),
    INDEX idx_plan_type (plan_type),
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_status (status)
) COMMENT='应急预案表';
```

#### 4.2.4 应急资源表（gas_emergency_resource）

```sql
CREATE TABLE gas_emergency_resource (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '资源ID',
    resource_no VARCHAR(32) COMMENT '资源编号',
    resource_name VARCHAR(100) NOT NULL COMMENT '资源名称',
    resource_type TINYINT NOT NULL COMMENT '资源类型：1-人员 2-车辆 3-物资 4-设备 5-场所',
    resource_category VARCHAR(50) COMMENT '资源分类',
    quantity DECIMAL(10,2) COMMENT '数量',
    unit VARCHAR(20) COMMENT '单位',
    location VARCHAR(200) COMMENT '存放位置',
    longitude DECIMAL(10,7) COMMENT '经度',
    latitude DECIMAL(10,7) COMMENT '纬度',
    owner_type TINYINT COMMENT '所属类型：1-政府 2-企业 3-第三方',
    owner_id BIGINT COMMENT '所属单位ID',
    owner_name VARCHAR(100) COMMENT '所属单位名称',
    contact_person VARCHAR(50) COMMENT '联系人',
    contact_phone VARCHAR(20) COMMENT '联系电话',
    status TINYINT DEFAULT 1 COMMENT '状态：1-可用 2-使用中 3-维护中 4-报废',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_resource_type (resource_type),
    INDEX idx_owner_id (owner_id),
    INDEX idx_status (status)
) COMMENT='应急资源表';
```

#### 4.2.5 应急队伍表（gas_emergency_team）

```sql
CREATE TABLE gas_emergency_team (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '队伍ID',
    team_no VARCHAR(32) COMMENT '队伍编号',
    team_name VARCHAR(100) NOT NULL COMMENT '队伍名称',
    team_type TINYINT NOT NULL COMMENT '队伍类型：1-消防队伍 2-抢修队伍 3-医疗队伍 4-应急抢险队 5-志愿者队伍',
    team_level TINYINT COMMENT '队伍级别：1-市级 2-县区级 3-企业级',
    member_count INT COMMENT '人员数量',
    leader_name VARCHAR(50) COMMENT '负责人姓名',
    leader_phone VARCHAR(20) COMMENT '负责人电话',
    address VARCHAR(200) COMMENT '驻地地址',
    longitude DECIMAL(10,7) COMMENT '经度',
    latitude DECIMAL(10,7) COMMENT '纬度',
    owner_type TINYINT COMMENT '所属类型：1-政府 2-企业 3-第三方',
    owner_id BIGINT COMMENT '所属单位ID',
    owner_name VARCHAR(100) COMMENT '所属单位名称',
    equipment_info TEXT COMMENT '装备配置',
    capability_info TEXT COMMENT '能力说明',
    status TINYINT DEFAULT 1 COMMENT '状态：1-待命 2-出勤中 3-休整',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_team_type (team_type),
    INDEX idx_owner_id (owner_id),
    INDEX idx_status (status)
) COMMENT='应急队伍表';
```

#### 4.2.6 应急专家表（gas_emergency_expert）

```sql
CREATE TABLE gas_emergency_expert (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '专家ID',
    expert_no VARCHAR(32) COMMENT '专家编号',
    expert_name VARCHAR(50) NOT NULL COMMENT '专家姓名',
    gender TINYINT COMMENT '性别：1-男 2-女',
    birth_date DATE COMMENT '出生日期',
    id_card VARCHAR(18) COMMENT '身份证号',
    phone VARCHAR(20) NOT NULL COMMENT '手机号码',
    email VARCHAR(100) COMMENT '电子邮箱',
    expert_type TINYINT NOT NULL COMMENT '专家类型：1-技术专家 2-管理专家 3-法律专家 4-安全专家',
    expert_level TINYINT COMMENT '专家级别：1-国家级 2-省级 3-市级',
    specialty VARCHAR(200) COMMENT '专业特长',
    work_unit VARCHAR(100) COMMENT '工作单位',
    work_position VARCHAR(50) COMMENT '职务',
    professional_title VARCHAR(50) COMMENT '职称',
    education VARCHAR(20) COMMENT '学历',
    major VARCHAR(100) COMMENT '专业',
    work_years INT COMMENT '从业年限',
    resume TEXT COMMENT '个人简介',
    achievements TEXT COMMENT '主要成果',
    certificates VARCHAR(1000) COMMENT '资质证书（逗号分隔）',
    photo VARCHAR(500) COMMENT '照片',
    status TINYINT DEFAULT 1 COMMENT '状态：1-在库 2-已出库',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_expert_type (expert_type),
    INDEX idx_expert_level (expert_level),
    INDEX idx_status (status)
) COMMENT='应急专家表';
```

#### 4.2.7 应急演练表（gas_emergency_drill）

```sql
CREATE TABLE gas_emergency_drill (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '演练ID',
    drill_no VARCHAR(32) NOT NULL COMMENT '演练编号',
    drill_name VARCHAR(200) NOT NULL COMMENT '演练名称',
    drill_type TINYINT NOT NULL COMMENT '演练类型：1-桌面演练 2-实战演练 3-专项演练 4-综合演练',
    drill_level TINYINT COMMENT '演练级别：1-市级 2-县区级 3-企业级',
    drill_scenario TEXT COMMENT '演练场景',
    drill_script TEXT COMMENT '演练脚本',
    plan_id BIGINT COMMENT '关联预案ID',
    organizer_id BIGINT COMMENT '组织单位ID',
    organizer_name VARCHAR(100) COMMENT '组织单位名称',
    leader_name VARCHAR(50) COMMENT '负责人姓名',
    leader_phone VARCHAR(20) COMMENT '负责人电话',
    participant_count INT COMMENT '参与人数',
    participant_units TEXT COMMENT '参与单位（JSON数组）',
    planned_date DATE COMMENT '计划日期',
    planned_location VARCHAR(200) COMMENT '计划地点',
    actual_start_time DATETIME COMMENT '实际开始时间',
    actual_end_time DATETIME COMMENT '实际结束时间',
    actual_location VARCHAR(200) COMMENT '实际地点',
    drill_photos VARCHAR(1000) COMMENT '演练照片（逗号分隔）',
    drill_videos VARCHAR(1000) COMMENT '演练视频（逗号分隔）',
    drill_result TEXT COMMENT '演练结果',
    evaluation_score INT COMMENT '评估得分',
    evaluation_content TEXT COMMENT '评估内容',
    problems_found TEXT COMMENT '发现问题',
    improvement_measures TEXT COMMENT '改进措施',
    status TINYINT DEFAULT 0 COMMENT '状态：0-计划中 1-待审批 2-已审批 3-进行中 4-已完成 5-已取消',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_drill_type (drill_type),
    INDEX idx_organizer_id (organizer_id),
    INDEX idx_status (status),
    INDEX idx_planned_date (planned_date)
) COMMENT='应急演练表';
```

#### 4.2.8 资源调度记录表（gas_emergency_dispatch）

```sql
CREATE TABLE gas_emergency_dispatch (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '调度ID',
    dispatch_no VARCHAR(32) NOT NULL COMMENT '调度编号',
    event_id BIGINT NOT NULL COMMENT '关联事件ID',
    warning_id BIGINT COMMENT '关联预警ID',
    resource_type TINYINT NOT NULL COMMENT '资源类型：1-人员 2-车辆 3-物资 4-设备 5-队伍',
    resource_id BIGINT NOT NULL COMMENT '资源ID',
    resource_name VARCHAR(100) COMMENT '资源名称',
    dispatch_quantity DECIMAL(10,2) COMMENT '调度数量',
    dispatch_unit VARCHAR(20) COMMENT '调度单位',
    dispatcher_id BIGINT NOT NULL COMMENT '调度人ID',
    dispatcher_name VARCHAR(50) COMMENT '调度人姓名',
    dispatch_time DATETIME NOT NULL COMMENT '调度时间',
    target_location VARCHAR(200) COMMENT '目标位置',
    target_longitude DECIMAL(10,7) COMMENT '目标经度',
    target_latitude DECIMAL(10,7) COMMENT '目标纬度',
    required_arrive_time DATETIME COMMENT '要求到达时间',
    actual_arrive_time DATETIME COMMENT '实际到达时间',
    return_time DATETIME COMMENT '归还时间',
    dispatch_instruction TEXT COMMENT '调度指令',
    execution_feedback TEXT COMMENT '执行反馈',
    status TINYINT DEFAULT 0 COMMENT '状态：0-已调度 1-在途中 2-已到达 3-执行中 4-已完成 5-已归还',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_event_id (event_id),
    INDEX idx_resource_id (resource_id),
    INDEX idx_dispatcher_id (dispatcher_id),
    INDEX idx_status (status)
) COMMENT='资源调度记录表';
```

#### 4.2.9 跨区联动记录表（gas_emergency_linkage）

```sql
CREATE TABLE gas_emergency_linkage (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '联动ID',
    linkage_no VARCHAR(32) NOT NULL COMMENT '联动编号',
    event_id BIGINT NOT NULL COMMENT '关联事件ID',
    linkage_type TINYINT NOT NULL COMMENT '联动类型：1-请求支援 2-提供支援',
    request_region VARCHAR(100) COMMENT '请求地区',
    support_region VARCHAR(100) COMMENT '支援地区',
    linkage_reason TEXT COMMENT '联动原因',
    support_content TEXT COMMENT '支援内容',
    support_resources TEXT COMMENT '支援资源（JSON）',
    request_user_id BIGINT COMMENT '请求人ID',
    request_time DATETIME COMMENT '请求时间',
    approve_user_id BIGINT COMMENT '审批人ID',
    approve_time DATETIME COMMENT '审批时间',
    approve_result TINYINT COMMENT '审批结果：1-同意 2-拒绝',
    coordinate_user_id BIGINT COMMENT '协调人ID',
    coordinate_result TEXT COMMENT '协调结果',
    start_time DATETIME COMMENT '联动开始时间',
    end_time DATETIME COMMENT '联动结束时间',
    linkage_result TEXT COMMENT '联动结果',
    evaluation_content TEXT COMMENT '评价内容',
    status TINYINT DEFAULT 0 COMMENT '状态：0-待审批 1-已批准 2-执行中 3-已完成 4-已拒绝',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_event_id (event_id),
    INDEX idx_linkage_type (linkage_type),
    INDEX idx_status (status)
) COMMENT='跨区联动记录表';
```

---

## 五、API接口设计

### 5.1 接口总览

| 模块 | 接口数量 | 基础路径 |
|------|----------|----------|
| 预警管理 | 12个 | /admin-api/gas/emergency/warning |
| 事件处置 | 10个 | /admin-api/gas/emergency/event |
| 预案管理 | 8个 | /admin-api/gas/emergency/plan |
| 资源管理 | 8个 | /admin-api/gas/emergency/resource |
| 队伍管理 | 6个 | /admin-api/gas/emergency/team |
| 专家管理 | 6个 | /admin-api/gas/emergency/expert |
| 演练管理 | 8个 | /admin-api/gas/emergency/drill |
| 调度记录 | 6个 | /admin-api/gas/emergency/dispatch |
| 跨区联动 | 4个 | /admin-api/gas/emergency/linkage |

**共计68个API接口**

### 5.2 预警管理接口

#### 5.2.1 创建预警（草稿）

```
POST /admin-api/gas/emergency/warning/create
```

**请求参数**：
```json
{
    "warningTitle": "XX区域燃气泄漏预警",
    "warningType": 1,
    "warningLevel": 2,
    "warningContent": "XX区域发现燃气泄漏...",
    "eventLocation": "松原市宁江区XX路XX号",
    "eventLongitude": 124.825,
    "eventLatitude": 45.172,
    "influenceScope": "影响周边500米范围",
    "responseMeasures": "1.立即疏散人员...",
    "precautions": "1.禁止明火...",
    "attachments": ["file1.jpg", "file2.pdf"],
    "sourceType": 2,
    "sourceId": null
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

#### 5.2.2 提交审批

```
POST /admin-api/gas/emergency/warning/submit/{id}
```

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | Long | 是 | 预警ID（路径参数） |

**响应结果**：
```json
{
    "code": 0,
    "data": true,
    "msg": "success"
}
```

#### 5.2.3 审批预警

```
POST /admin-api/gas/emergency/warning/approve
```

**请求参数**：
```json
{
    "id": 1001,
    "approveResult": 1,
    "approveOpinion": "同意发布",
    "adjustLevel": null
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": true,
    "msg": "success"
}
```

#### 5.2.4 发布预警

```
POST /admin-api/gas/emergency/warning/publish/{id}
```

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| id | Long | 是 | 预警ID（路径参数） |
| notifyUsers | List<Long> | 否 | 通知人员ID列表 |
| notifyChannels | List<String> | 否 | 通知渠道：sms/app/email |

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "publishTime": "2026-01-27 10:30:00",
        "notifyResult": {
            "sms": {"total": 100, "success": 98, "fail": 2},
            "app": {"total": 80, "success": 80, "fail": 0}
        }
    },
    "msg": "success"
}
```

#### 5.2.5 升级预警

```
POST /admin-api/gas/emergency/warning/upgrade
```

**请求参数**：
```json
{
    "id": 1001,
    "newLevel": 3,
    "upgradeReason": "事态扩大，影响范围增加...",
    "additionalMeasures": "1.扩大疏散范围..."
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": 1002,
    "msg": "success"
}
```

#### 5.2.6 解除预警

```
POST /admin-api/gas/emergency/warning/cancel
```

**请求参数**：
```json
{
    "id": 1001,
    "cancelReason": "险情已排除，恢复正常"
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": true,
    "msg": "success"
}
```

#### 5.2.7 获取预警详情

```
GET /admin-api/gas/emergency/warning/get/{id}
```

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "id": 1001,
        "warningNo": "YJ202601270001",
        "warningTitle": "XX区域燃气泄漏预警",
        "warningType": 1,
        "warningTypeName": "泄漏",
        "warningLevel": 2,
        "warningLevelName": "黄色预警",
        "warningContent": "...",
        "eventLocation": "...",
        "status": 2,
        "statusName": "已发布",
        "publishTime": "2026-01-27 10:30:00",
        "publishUserName": "张三",
        "notifyResult": {...}
    },
    "msg": "success"
}
```

#### 5.2.8 分页查询预警

```
GET /admin-api/gas/emergency/warning/page
```

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| pageNo | Integer | 否 | 页码，默认1 |
| pageSize | Integer | 否 | 每页条数，默认10 |
| warningLevel | Integer | 否 | 预警等级 |
| status | Integer | 否 | 状态 |
| publishTimeStart | String | 否 | 发布开始时间 |
| publishTimeEnd | String | 否 | 发布结束时间 |

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "list": [...],
        "total": 100
    },
    "msg": "success"
}
```

### 5.3 事件处置接口

#### 5.3.1 上报应急事件

```
POST /admin-api/gas/emergency/event/report
```

**请求参数**：
```json
{
    "eventTitle": "XX小区燃气泄漏事件",
    "eventType": 1,
    "eventDescription": "XX小区3号楼发生燃气泄漏...",
    "eventLocation": "松原市宁江区XX小区3号楼",
    "eventLongitude": 124.825,
    "eventLatitude": 45.172,
    "occurTime": "2026-01-27 09:30:00",
    "enterpriseId": 100,
    "facilityId": 200,
    "casualties": {
        "death": 0,
        "injury": 0,
        "trapped": 2
    },
    "propertyLoss": "暂无明显财产损失",
    "influenceScope": "影响3号楼及周边50米",
    "takenMeasures": "已关闭总阀门、疏散人员",
    "eventPhotos": ["photo1.jpg", "photo2.jpg"]
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "eventId": 2001,
        "eventNo": "SJ202601270001"
    },
    "msg": "success"
}
```

#### 5.3.2 事件等级研判

```
POST /admin-api/gas/emergency/event/assess
```

**请求参数**：
```json
{
    "eventId": 2001,
    "eventLevel": 2,
    "assessBasis": "根据泄漏量和影响范围判定...",
    "warningNeeded": true,
    "warningLevel": 2,
    "planNeeded": true,
    "planId": 301
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "assessResult": true,
        "warningId": 1002
    },
    "msg": "success"
}
```

#### 5.3.3 更新处置进度

```
POST /admin-api/gas/emergency/event/progress
```

**请求参数**：
```json
{
    "eventId": 2001,
    "progressContent": "消防队伍已到达现场...",
    "progressPhotos": ["progress1.jpg"],
    "currentStatus": "处置中",
    "nextSteps": "继续排查泄漏点"
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": true,
    "msg": "success"
}
```

#### 5.3.4 事件结案

```
POST /admin-api/gas/emergency/event/close
```

**请求参数**：
```json
{
    "eventId": 2001,
    "closeSummary": "事件处置完毕，泄漏点已修复...",
    "causeAnalysis": "管道老化导致...",
    "responsibilityAnalysis": "企业日常检查不到位...",
    "improvementMeasures": "1.加强日常巡检...",
    "lessonLearned": "..."
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": true,
    "msg": "success"
}
```

#### 5.3.5 获取警情总览

```
GET /admin-api/gas/emergency/event/overview
```

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| startDate | String | 否 | 开始日期 |
| endDate | String | 否 | 结束日期 |
| regionId | Long | 否 | 区域ID |

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "totalEvents": 50,
        "processingEvents": 3,
        "closedEvents": 47,
        "levelDistribution": {
            "level1": 2,
            "level2": 8,
            "level3": 15,
            "level4": 25
        },
        "typeDistribution": {
            "leak": 30,
            "fire": 5,
            "explosion": 1,
            "poisoning": 2,
            "other": 12
        },
        "trend": [...]
    },
    "msg": "success"
}
```

### 5.4 预案管理接口

#### 5.4.1 创建预案

```
POST /admin-api/gas/emergency/plan/create
```

**请求参数**：
```json
{
    "planName": "XX企业燃气泄漏现场处置方案",
    "planType": 3,
    "planLevel": 3,
    "applicableScope": "适用于XX企业所属站点...",
    "planContent": "...",
    "planFile": "plan.docx",
    "enterpriseId": 100
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": 301,
    "msg": "success"
}
```

#### 5.4.2 预案结构化

```
POST /admin-api/gas/emergency/plan/structure
```

**请求参数**：
```json
{
    "planId": 301,
    "elements": [
        {
            "elementType": "organization",
            "elementContent": {
                "commander": "XXX",
                "groups": [...]
            }
        },
        {
            "elementType": "response",
            "elementContent": {
                "conditions": [...],
                "procedures": [...]
            }
        }
    ]
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": true,
    "msg": "success"
}
```

#### 5.4.3 提交预案审核

```
POST /admin-api/gas/emergency/plan/submit/{id}
```

#### 5.4.4 审核预案

```
POST /admin-api/gas/emergency/plan/review
```

**请求参数**：
```json
{
    "planId": 301,
    "reviewResult": 1,
    "reviewOpinion": "审核通过"
}
```

#### 5.4.5 发布预案

```
POST /admin-api/gas/emergency/plan/publish/{id}
```

### 5.5 资源管理接口

#### 5.5.1 创建资源

```
POST /admin-api/gas/emergency/resource/create
```

**请求参数**：
```json
{
    "resourceName": "防护服",
    "resourceType": 3,
    "resourceCategory": "防护装备",
    "quantity": 100,
    "unit": "套",
    "location": "XX仓库",
    "longitude": 124.825,
    "latitude": 45.172,
    "ownerType": 1,
    "ownerId": 1,
    "ownerName": "市应急管理局",
    "contactPerson": "张三",
    "contactPhone": "13800138000"
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": 401,
    "msg": "success"
}
```

#### 5.5.2 查询周边资源

```
GET /admin-api/gas/emergency/resource/nearby
```

**请求参数**：
| 参数 | 类型 | 必填 | 说明 |
|------|------|------|------|
| longitude | Double | 是 | 中心点经度 |
| latitude | Double | 是 | 中心点纬度 |
| radius | Double | 否 | 搜索半径(km)，默认5 |
| resourceType | Integer | 否 | 资源类型 |

**响应结果**：
```json
{
    "code": 0,
    "data": [
        {
            "id": 401,
            "resourceName": "防护服",
            "resourceType": 3,
            "quantity": 100,
            "location": "XX仓库",
            "distance": 2.5,
            "status": 1
        }
    ],
    "msg": "success"
}
```

#### 5.5.3 资源统计

```
GET /admin-api/gas/emergency/resource/statistics
```

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "totalCount": 500,
        "typeDistribution": {
            "personnel": 200,
            "vehicle": 50,
            "material": 200,
            "equipment": 50
        },
        "statusDistribution": {
            "available": 450,
            "inUse": 30,
            "maintenance": 20
        },
        "ownerDistribution": {
            "government": 200,
            "enterprise": 280,
            "thirdParty": 20
        }
    },
    "msg": "success"
}
```

### 5.6 调度管理接口

#### 5.6.1 创建调度

```
POST /admin-api/gas/emergency/dispatch/create
```

**请求参数**：
```json
{
    "eventId": 2001,
    "warningId": 1001,
    "resourceType": 5,
    "resourceId": 501,
    "resourceName": "XX消防中队",
    "dispatchQuantity": 1,
    "dispatchUnit": "队",
    "targetLocation": "松原市宁江区XX小区",
    "targetLongitude": 124.825,
    "targetLatitude": 45.172,
    "requiredArriveTime": "2026-01-27 10:00:00",
    "dispatchInstruction": "携带防护装备，到达后立即设置警戒线..."
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "dispatchId": 601,
        "dispatchNo": "DD202601270001"
    },
    "msg": "success"
}
```

#### 5.6.2 更新调度状态

```
POST /admin-api/gas/emergency/dispatch/update-status
```

**请求参数**：
```json
{
    "dispatchId": 601,
    "status": 2,
    "actualArriveTime": "2026-01-27 09:55:00",
    "executionFeedback": "已到达现场，正在设置警戒线"
}
```

### 5.7 演练管理接口

#### 5.7.1 创建演练计划

```
POST /admin-api/gas/emergency/drill/create
```

**请求参数**：
```json
{
    "drillName": "2026年度燃气泄漏应急演练",
    "drillType": 2,
    "drillLevel": 2,
    "drillScenario": "模拟某小区发生燃气泄漏...",
    "drillScript": "...",
    "planId": 301,
    "organizerId": 100,
    "organizerName": "XX县应急管理局",
    "leaderName": "李四",
    "leaderPhone": "13900139000",
    "participantCount": 50,
    "participantUnits": ["XX消防大队", "XX燃气公司"],
    "plannedDate": "2026-03-15",
    "plannedLocation": "XX小区"
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": 701,
    "msg": "success"
}
```

#### 5.7.2 提交演练审批

```
POST /admin-api/gas/emergency/drill/submit/{id}
```

#### 5.7.3 演练评估

```
POST /admin-api/gas/emergency/drill/evaluate
```

**请求参数**：
```json
{
    "drillId": 701,
    "evaluationScore": 85,
    "evaluationContent": "本次演练总体组织有序...",
    "problemsFound": "1.部分人员响应不够及时...",
    "improvementMeasures": "1.加强日常培训..."
}
```

### 5.8 跨区联动接口

#### 5.8.1 发起联动请求

```
POST /admin-api/gas/emergency/linkage/request
```

**请求参数**：
```json
{
    "eventId": 2001,
    "linkageReason": "事态严重，本市资源不足...",
    "supportContent": "需要消防增援、专家支持",
    "supportResources": [
        {"type": "team", "name": "消防队伍", "quantity": 2},
        {"type": "expert", "name": "燃气专家", "quantity": 3}
    ]
}
```

**响应结果**：
```json
{
    "code": 0,
    "data": {
        "linkageId": 801,
        "linkageNo": "LD202601270001"
    },
    "msg": "success"
}
```

#### 5.8.2 响应联动请求

```
POST /admin-api/gas/emergency/linkage/respond
```

**请求参数**：
```json
{
    "linkageId": 801,
    "approveResult": 1,
    "supportRegion": "长春市",
    "confirmResources": [
        {"type": "team", "id": 502, "name": "XX消防大队"},
        {"type": "expert", "id": 201, "name": "张专家"}
    ],
    "estimatedArriveTime": "2026-01-27 14:00:00"
}
```

---

## 六、BPMN工作流设计

### 6.1 预警发布审批流程

#### 6.1.1 流程定义

**流程标识**：`warning_publish_approval`
**流程名称**：预警发布审批流程
**适用场景**：黄色及以上预警发布审批

#### 6.1.2 流程节点

| 节点ID | 节点名称 | 节点类型 | 处理人 | 表单 |
|--------|----------|----------|--------|------|
| start | 开始 | StartEvent | - | - |
| draft | 编辑预警 | UserTask | 申请人 | 预警编辑表单 |
| county_review | 县区审核 | UserTask | 县区监管员 | 审核表单 |
| city_review | 市级审核 | UserTask | 市级监管员 | 审核表单 |
| leader_approve | 领导审批 | UserTask | 市级领导 | 审批表单 |
| level_gateway | 等级判断 | ExclusiveGateway | - | - |
| approve_gateway | 审批判断 | ExclusiveGateway | - | - |
| publish | 发布预警 | ServiceTask | 系统 | - |
| notify | 消息推送 | ServiceTask | 系统 | - |
| end | 结束 | EndEvent | - | - |

#### 6.1.3 流程规则

```
1. 蓝色预警(level=1)：draft → publish → notify → end
2. 黄色预警(level=2)：draft → city_review → publish → notify → end
3. 橙色/红色预警(level=3,4)：draft → city_review → leader_approve → publish → notify → end
4. 审核不通过：退回draft节点修改
```

#### 6.1.4 BPMN XML定义

```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:flowable="http://flowable.org/bpmn"
             targetNamespace="http://www.flowable.org/processdef">

    <process id="warning_publish_approval" name="预警发布审批流程" isExecutable="true">

        <!-- 开始事件 -->
        <startEvent id="start" name="开始"/>

        <!-- 编辑预警 -->
        <userTask id="draft" name="编辑预警"
                  flowable:assignee="${initiator}">
            <extensionElements>
                <flowable:formProperty id="warningTitle" name="预警标题" type="string" required="true"/>
                <flowable:formProperty id="warningLevel" name="预警等级" type="long" required="true"/>
                <flowable:formProperty id="warningContent" name="预警内容" type="string" required="true"/>
            </extensionElements>
        </userTask>

        <!-- 等级判断网关 -->
        <exclusiveGateway id="level_gateway" name="等级判断"/>

        <!-- 市级审核 -->
        <userTask id="city_review" name="市级审核"
                  flowable:candidateGroups="city_supervisor">
            <extensionElements>
                <flowable:formProperty id="reviewResult" name="审核结果" type="long" required="true"/>
                <flowable:formProperty id="reviewOpinion" name="审核意见" type="string"/>
            </extensionElements>
        </userTask>

        <!-- 审核判断网关 -->
        <exclusiveGateway id="review_gateway" name="审核判断"/>

        <!-- 领导审批 -->
        <userTask id="leader_approve" name="领导审批"
                  flowable:candidateGroups="city_leader">
            <extensionElements>
                <flowable:formProperty id="approveResult" name="审批结果" type="long" required="true"/>
                <flowable:formProperty id="approveOpinion" name="审批意见" type="string"/>
            </extensionElements>
        </userTask>

        <!-- 审批判断网关 -->
        <exclusiveGateway id="approve_gateway" name="审批判断"/>

        <!-- 发布预警（服务任务） -->
        <serviceTask id="publish" name="发布预警"
                     flowable:delegateExpression="${warningPublishDelegate}"/>

        <!-- 消息推送（服务任务） -->
        <serviceTask id="notify" name="消息推送"
                     flowable:delegateExpression="${warningNotifyDelegate}"/>

        <!-- 结束事件 -->
        <endEvent id="end" name="结束"/>

        <!-- 流程连线 -->
        <sequenceFlow id="flow1" sourceRef="start" targetRef="draft"/>
        <sequenceFlow id="flow2" sourceRef="draft" targetRef="level_gateway"/>

        <!-- 蓝色预警直接发布 -->
        <sequenceFlow id="flow3" sourceRef="level_gateway" targetRef="publish">
            <conditionExpression xsi:type="tFormalExpression">
                ${warningLevel == 1}
            </conditionExpression>
        </sequenceFlow>

        <!-- 黄色及以上需要审核 -->
        <sequenceFlow id="flow4" sourceRef="level_gateway" targetRef="city_review">
            <conditionExpression xsi:type="tFormalExpression">
                ${warningLevel >= 2}
            </conditionExpression>
        </sequenceFlow>

        <sequenceFlow id="flow5" sourceRef="city_review" targetRef="review_gateway"/>

        <!-- 审核通过 -->
        <sequenceFlow id="flow6" sourceRef="review_gateway" targetRef="publish">
            <conditionExpression xsi:type="tFormalExpression">
                ${reviewResult == 1 &amp;&amp; warningLevel == 2}
            </conditionExpression>
        </sequenceFlow>

        <!-- 橙色/红色需领导审批 -->
        <sequenceFlow id="flow7" sourceRef="review_gateway" targetRef="leader_approve">
            <conditionExpression xsi:type="tFormalExpression">
                ${reviewResult == 1 &amp;&amp; warningLevel >= 3}
            </conditionExpression>
        </sequenceFlow>

        <!-- 审核不通过退回 -->
        <sequenceFlow id="flow8" sourceRef="review_gateway" targetRef="draft">
            <conditionExpression xsi:type="tFormalExpression">
                ${reviewResult == 0}
            </conditionExpression>
        </sequenceFlow>

        <sequenceFlow id="flow9" sourceRef="leader_approve" targetRef="approve_gateway"/>

        <!-- 审批通过 -->
        <sequenceFlow id="flow10" sourceRef="approve_gateway" targetRef="publish">
            <conditionExpression xsi:type="tFormalExpression">
                ${approveResult == 1}
            </conditionExpression>
        </sequenceFlow>

        <!-- 审批不通过退回 -->
        <sequenceFlow id="flow11" sourceRef="approve_gateway" targetRef="city_review">
            <conditionExpression xsi:type="tFormalExpression">
                ${approveResult == 0}
            </conditionExpression>
        </sequenceFlow>

        <sequenceFlow id="flow12" sourceRef="publish" targetRef="notify"/>
        <sequenceFlow id="flow13" sourceRef="notify" targetRef="end"/>

    </process>
</definitions>
```

### 6.2 应急预案审批流程

#### 6.2.1 流程定义

**流程标识**：`emergency_plan_approval`
**流程名称**：应急预案审批流程
**适用场景**：应急预案的新增、修订审批

#### 6.2.2 流程节点

| 节点ID | 节点名称 | 节点类型 | 处理人 | 表单 |
|--------|----------|----------|--------|------|
| start | 开始 | StartEvent | - | - |
| draft | 起草预案 | UserTask | 申请人 | 预案编辑表单 |
| level_gateway | 级别判断 | ExclusiveGateway | - | - |
| enterprise_review | 企业审核 | UserTask | 企业负责人 | 审核表单 |
| county_review | 县区审核 | UserTask | 县区监管员 | 审核表单 |
| city_review | 市级审核 | UserTask | 市级监管员 | 审核表单 |
| publish | 发布预案 | ServiceTask | 系统 | - |
| end | 结束 | EndEvent | - | - |

#### 6.2.3 流程规则

```
1. 企业级预案(level=3)：draft → enterprise_review → county_review → publish → end
2. 县区级预案(level=2)：draft → county_review → city_review → publish → end
3. 市级预案(level=1)：draft → city_review → publish → end
4. 审核不通过：退回上一节点修改
```

### 6.3 应急演练审批流程

#### 6.3.1 流程定义

**流程标识**：`emergency_drill_approval`
**流程名称**：应急演练审批流程
**适用场景**：应急演练计划审批

#### 6.3.2 流程节点

| 节点ID | 节点名称 | 节点类型 | 处理人 |
|--------|----------|----------|--------|
| start | 开始 | StartEvent | - |
| create_plan | 创建计划 | UserTask | 申请人 |
| level_gateway | 级别判断 | ExclusiveGateway | - |
| enterprise_approve | 企业审批 | UserTask | 企业负责人 |
| county_approve | 县区审批 | UserTask | 县区调度员 |
| city_approve | 市级审批 | UserTask | 市级调度员 |
| prepare | 演练准备 | UserTask | 组织人员 |
| execute | 演练实施 | UserTask | 组织人员 |
| evaluate | 演练评估 | UserTask | 评估人员 |
| archive | 归档 | ServiceTask | 系统 |
| end | 结束 | EndEvent | - |

### 6.4 跨区联动审批流程

#### 6.4.1 流程定义

**流程标识**：`cross_region_linkage`
**流程名称**：跨区联动审批流程
**适用场景**：请求外部支援审批

#### 6.4.2 流程节点

| 节点ID | 节点名称 | 节点类型 | 处理人 |
|--------|----------|----------|--------|
| start | 开始 | StartEvent | - |
| request | 发起请求 | UserTask | 市级调度员 |
| city_approve | 市级审批 | UserTask | 市级领导 |
| submit_province | 上报省级 | ServiceTask | 系统 |
| province_coordinate | 省级协调 | UserTask | 省级协调员 |
| support_confirm | 支援确认 | UserTask | 支援方调度员 |
| execute | 执行联动 | UserTask | 相关人员 |
| complete | 完成评价 | UserTask | 双方调度员 |
| end | 结束 | EndEvent | - |

---

## 七、技术实现要点

### 7.1 预警发布与推送

#### 7.1.1 多渠道推送

```java
/**
 * 预警推送服务
 */
@Service
public class WarningNotifyService {

    @Resource
    private SmsSendApi smsSendApi;

    @Resource
    private WebSocketMessageSender webSocketMessageSender;

    @Resource
    private AppPushService appPushService;

    /**
     * 多渠道推送预警
     */
    public NotifyResult notifyWarning(Long warningId, List<Long> userIds, List<String> channels) {
        WarningDO warning = warningMapper.selectById(warningId);
        NotifyResult result = new NotifyResult();

        for (String channel : channels) {
            switch (channel) {
                case "sms":
                    // 短信推送
                    SmsSendResult smsResult = sendSmsNotify(warning, userIds);
                    result.setSmsResult(smsResult);
                    break;
                case "app":
                    // APP推送
                    AppPushResult appResult = sendAppNotify(warning, userIds);
                    result.setAppResult(appResult);
                    break;
                case "websocket":
                    // WebSocket实时推送
                    sendWebSocketNotify(warning, userIds);
                    result.setWsResult(true);
                    break;
            }
        }

        return result;
    }

    /**
     * 短信推送
     */
    private SmsSendResult sendSmsNotify(WarningDO warning, List<Long> userIds) {
        // 获取用户手机号
        List<String> phones = userService.getPhonesByUserIds(userIds);

        // 构建短信内容
        String content = buildSmsContent(warning);

        // 批量发送
        return smsSendApi.sendBatch(phones, content);
    }
}
```

#### 7.1.2 预警等级自动判定

```java
/**
 * 预警等级自动判定服务
 */
@Service
public class WarningLevelAssessService {

    /**
     * 根据事件信息自动判定预警等级
     */
    public Integer assessWarningLevel(EventReportReqVO event) {
        int score = 0;

        // 1. 事件类型评分
        score += getEventTypeScore(event.getEventType());

        // 2. 人员伤亡评分
        score += getCasualtiesScore(event.getCasualties());

        // 3. 影响范围评分
        score += getInfluenceScopeScore(event.getInfluenceScope());

        // 4. 泄漏量评分（如果是泄漏事件）
        if (event.getEventType() == 1) {
            score += getLeakageScore(event.getLeakageAmount());
        }

        // 根据得分判定等级
        if (score >= 80) {
            return 4; // 红色
        } else if (score >= 60) {
            return 3; // 橙色
        } else if (score >= 40) {
            return 2; // 黄色
        } else {
            return 1; // 蓝色
        }
    }
}
```

### 7.2 应急资源调度

#### 7.2.1 就近资源查询

```java
/**
 * 应急资源服务
 */
@Service
public class EmergencyResourceService {

    /**
     * 查询周边资源（基于空间距离）
     */
    public List<ResourceNearbyRespVO> getNearbyResources(
            Double longitude, Double latitude, Double radius, Integer resourceType) {

        // 计算范围边界
        double[] bounds = GeoUtils.getBounds(longitude, latitude, radius);

        // 查询范围内的资源
        List<ResourceDO> resources = resourceMapper.selectByBounds(
            bounds[0], bounds[1], bounds[2], bounds[3], resourceType);

        // 计算实际距离并排序
        return resources.stream()
            .map(r -> {
                ResourceNearbyRespVO vo = BeanUtils.toBean(r, ResourceNearbyRespVO.class);
                double distance = GeoUtils.calculateDistance(
                    longitude, latitude, r.getLongitude(), r.getLatitude());
                vo.setDistance(distance);
                return vo;
            })
            .filter(r -> r.getDistance() <= radius)
            .sorted(Comparator.comparing(ResourceNearbyRespVO::getDistance))
            .collect(Collectors.toList());
    }
}
```

#### 7.2.2 资源调度状态跟踪

```java
/**
 * 资源调度服务
 */
@Service
public class DispatchService {

    @Resource
    private WebSocketMessageSender webSocketMessageSender;

    /**
     * 创建调度并实时推送
     */
    @Transactional
    public Long createDispatch(DispatchCreateReqVO reqVO) {
        // 1. 创建调度记录
        DispatchDO dispatch = BeanUtils.toBean(reqVO, DispatchDO.class);
        dispatch.setDispatchNo(generateDispatchNo());
        dispatch.setDispatchTime(LocalDateTime.now());
        dispatch.setStatus(0); // 已调度
        dispatchMapper.insert(dispatch);

        // 2. 更新资源状态
        resourceMapper.updateStatus(reqVO.getResourceId(), 2); // 使用中

        // 3. 推送调度通知
        pushDispatchNotify(dispatch);

        // 4. 推送到指挥大屏
        pushToCommandScreen(dispatch);

        return dispatch.getId();
    }

    /**
     * 更新调度状态
     */
    @Transactional
    public void updateDispatchStatus(DispatchStatusUpdateReqVO reqVO) {
        DispatchDO dispatch = dispatchMapper.selectById(reqVO.getDispatchId());

        // 更新状态
        dispatch.setStatus(reqVO.getStatus());
        if (reqVO.getStatus() == 2) { // 已到达
            dispatch.setActualArriveTime(LocalDateTime.now());
        } else if (reqVO.getStatus() == 5) { // 已归还
            dispatch.setReturnTime(LocalDateTime.now());
            // 恢复资源状态
            resourceMapper.updateStatus(dispatch.getResourceId(), 1);
        }
        dispatch.setExecutionFeedback(reqVO.getExecutionFeedback());
        dispatchMapper.updateById(dispatch);

        // 实时推送状态变更
        pushStatusChange(dispatch);
    }
}
```

### 7.3 GIS可视化集成

#### 7.3.1 应急指挥大屏数据接口

```java
/**
 * 应急指挥大屏服务
 */
@Service
public class CommandScreenService {

    /**
     * 获取大屏数据
     */
    public CommandScreenDataVO getCommandScreenData(Long eventId) {
        CommandScreenDataVO data = new CommandScreenDataVO();

        // 1. 事件信息
        EventDO event = eventMapper.selectById(eventId);
        data.setEventInfo(BeanUtils.toBean(event, EventInfoVO.class));

        // 2. 预警信息
        if (event.getWarningId() != null) {
            WarningDO warning = warningMapper.selectById(event.getWarningId());
            data.setWarningInfo(BeanUtils.toBean(warning, WarningInfoVO.class));
        }

        // 3. 资源分布（GIS图层数据）
        List<ResourceGisVO> resources = getResourcesForGis(event);
        data.setResourceLayer(resources);

        // 4. 队伍位置（实时位置）
        List<TeamGisVO> teams = getTeamPositions(eventId);
        data.setTeamLayer(teams);

        // 5. 调度轨迹
        List<DispatchTrackVO> tracks = getDispatchTracks(eventId);
        data.setDispatchTracks(tracks);

        // 6. 影响范围（圆形/多边形）
        data.setInfluenceArea(calculateInfluenceArea(event));

        // 7. 处置进度
        List<ProgressVO> progressList = getProgressList(eventId);
        data.setProgressList(progressList);

        return data;
    }
}
```

#### 7.3.2 实时位置推送

```java
/**
 * 实时位置服务
 */
@Service
public class RealtimeLocationService {

    @Resource
    private WebSocketMessageSender webSocketMessageSender;

    @Resource
    private StringRedisTemplate redisTemplate;

    /**
     * 更新队伍位置（移动端上报）
     */
    public void updateTeamLocation(Long teamId, Double longitude, Double latitude) {
        String key = "emergency:team:location:" + teamId;

        // 存储到Redis
        Map<String, String> location = new HashMap<>();
        location.put("longitude", String.valueOf(longitude));
        location.put("latitude", String.valueOf(latitude));
        location.put("updateTime", LocalDateTime.now().toString());
        redisTemplate.opsForHash().putAll(key, location);
        redisTemplate.expire(key, 5, TimeUnit.MINUTES);

        // 推送到指挥大屏
        TeamLocationVO vo = new TeamLocationVO();
        vo.setTeamId(teamId);
        vo.setLongitude(longitude);
        vo.setLatitude(latitude);
        webSocketMessageSender.send("command_screen", "team_location", JsonUtils.toJsonString(vo));
    }
}
```

### 7.4 预案结构化存储

#### 7.4.1 预案要素提取

```java
/**
 * 预案结构化服务
 */
@Service
public class PlanStructureService {

    /**
     * 结构化预案内容
     */
    @Transactional
    public void structurePlan(Long planId, List<PlanElementReqVO> elements) {
        // 删除旧的要素
        planElementMapper.deleteByPlanId(planId);

        // 保存新的要素
        for (PlanElementReqVO element : elements) {
            PlanElementDO elementDO = new PlanElementDO();
            elementDO.setPlanId(planId);
            elementDO.setElementType(element.getElementType());
            elementDO.setElementContent(JsonUtils.toJsonString(element.getElementContent()));
            elementDO.setOrderNo(element.getOrderNo());
            planElementMapper.insert(elementDO);
        }

        // 更新预案状态
        planMapper.updateStructured(planId, true);
    }

    /**
     * 根据事件匹配预案
     */
    public List<PlanMatchVO> matchPlans(Long eventId) {
        EventDO event = eventMapper.selectById(eventId);

        // 查询匹配的预案
        List<PlanDO> plans = planMapper.selectByConditions(
            event.getEventType(),
            event.getEventLevel(),
            event.getEnterpriseId()
        );

        // 计算匹配度
        return plans.stream()
            .map(plan -> {
                PlanMatchVO vo = BeanUtils.toBean(plan, PlanMatchVO.class);
                vo.setMatchScore(calculateMatchScore(event, plan));
                return vo;
            })
            .sorted(Comparator.comparing(PlanMatchVO::getMatchScore).reversed())
            .collect(Collectors.toList());
    }
}
```

### 7.5 跨系统联动

#### 7.5.1 与省级平台对接

```java
/**
 * 省级平台对接服务
 */
@Service
public class ProvincePlatformService {

    @Resource
    private RestTemplate restTemplate;

    @Value("${province.platform.url}")
    private String provincePlatformUrl;

    /**
     * 上报事件到省级平台
     */
    public void reportEventToProvince(EventDO event) {
        ProvinceEventReportDTO dto = convertToProvinceDTO(event);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("Authorization", getProvinceToken());

        HttpEntity<ProvinceEventReportDTO> request = new HttpEntity<>(dto, headers);

        try {
            restTemplate.postForEntity(
                provincePlatformUrl + "/api/event/report",
                request,
                ProvinceResponseDTO.class
            );
        } catch (Exception e) {
            log.error("上报省级平台失败", e);
            // 记录失败，后续重试
            saveReportFailRecord(event.getId(), e.getMessage());
        }
    }

    /**
     * 发起跨区联动请求
     */
    public void requestCrossRegionLinkage(LinkageDO linkage) {
        ProvinceLinkageRequestDTO dto = convertToLinkageDTO(linkage);

        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_JSON);
        headers.set("Authorization", getProvinceToken());

        HttpEntity<ProvinceLinkageRequestDTO> request = new HttpEntity<>(dto, headers);

        ResponseEntity<ProvinceResponseDTO> response = restTemplate.postForEntity(
            provincePlatformUrl + "/api/linkage/request",
            request,
            ProvinceResponseDTO.class
        );

        // 更新联动状态
        if (response.getBody().isSuccess()) {
            linkageMapper.updateStatus(linkage.getId(), 1); // 已提交
        }
    }
}
```

### 7.6 定时任务

#### 7.6.1 预警超时监控

```java
/**
 * 预警超时监控任务
 */
@Component
public class WarningTimeoutJob {

    @Resource
    private WarningMapper warningMapper;

    @Resource
    private WarningNotifyService warningNotifyService;

    /**
     * 每5分钟检查预警审批超时
     */
    @Scheduled(cron = "0 */5 * * * ?")
    public void checkWarningApprovalTimeout() {
        // 查询待审批超时的预警
        List<WarningDO> timeoutWarnings = warningMapper.selectApprovalTimeout();

        for (WarningDO warning : timeoutWarnings) {
            // 根据预警等级判断超时时间
            int timeoutMinutes = getTimeoutMinutes(warning.getWarningLevel());
            LocalDateTime deadline = warning.getDraftTime().plusMinutes(timeoutMinutes);

            if (LocalDateTime.now().isAfter(deadline)) {
                // 发送催办通知
                warningNotifyService.sendUrgeNotify(warning);

                // 自动升级处理（如果配置了）
                if (isAutoEscalate(warning)) {
                    escalateWarning(warning);
                }
            }
        }
    }
}
```

#### 7.6.2 演练计划提醒

```java
/**
 * 演练计划提醒任务
 */
@Component
public class DrillReminderJob {

    /**
     * 每天早上9点检查即将开始的演练
     */
    @Scheduled(cron = "0 0 9 * * ?")
    public void remindUpcomingDrills() {
        // 查询3天内即将开始的演练
        LocalDate startDate = LocalDate.now();
        LocalDate endDate = startDate.plusDays(3);

        List<DrillDO> upcomingDrills = drillMapper.selectByDateRange(startDate, endDate);

        for (DrillDO drill : upcomingDrills) {
            // 发送提醒通知
            sendDrillReminder(drill);
        }
    }
}
```

---

## 八、附录

### 8.1 错误码定义

```java
public interface EmergencyErrorCodeConstants {

    // ========== 预警模块 1-005-001-xxx ==========
    ErrorCode WARNING_NOT_EXISTS = new ErrorCode(1_005_001_001, "预警不存在");
    ErrorCode WARNING_STATUS_ERROR = new ErrorCode(1_005_001_002, "预警状态错误");
    ErrorCode WARNING_LEVEL_INVALID = new ErrorCode(1_005_001_003, "预警等级无效");
    ErrorCode WARNING_ALREADY_PUBLISHED = new ErrorCode(1_005_001_004, "预警已发布");
    ErrorCode WARNING_ALREADY_CANCELLED = new ErrorCode(1_005_001_005, "预警已解除");

    // ========== 事件模块 1-005-002-xxx ==========
    ErrorCode EVENT_NOT_EXISTS = new ErrorCode(1_005_002_001, "事件不存在");
    ErrorCode EVENT_STATUS_ERROR = new ErrorCode(1_005_002_002, "事件状态错误");
    ErrorCode EVENT_ALREADY_CLOSED = new ErrorCode(1_005_002_003, "事件已结案");

    // ========== 预案模块 1-005-003-xxx ==========
    ErrorCode PLAN_NOT_EXISTS = new ErrorCode(1_005_003_001, "预案不存在");
    ErrorCode PLAN_STATUS_ERROR = new ErrorCode(1_005_003_002, "预案状态错误");
    ErrorCode PLAN_VERSION_EXISTS = new ErrorCode(1_005_003_003, "预案版本已存在");

    // ========== 资源模块 1-005-004-xxx ==========
    ErrorCode RESOURCE_NOT_EXISTS = new ErrorCode(1_005_004_001, "资源不存在");
    ErrorCode RESOURCE_NOT_AVAILABLE = new ErrorCode(1_005_004_002, "资源不可用");
    ErrorCode RESOURCE_IN_USE = new ErrorCode(1_005_004_003, "资源使用中");

    // ========== 演练模块 1-005-005-xxx ==========
    ErrorCode DRILL_NOT_EXISTS = new ErrorCode(1_005_005_001, "演练不存在");
    ErrorCode DRILL_STATUS_ERROR = new ErrorCode(1_005_005_002, "演练状态错误");

    // ========== 调度模块 1-005-006-xxx ==========
    ErrorCode DISPATCH_NOT_EXISTS = new ErrorCode(1_005_006_001, "调度记录不存在");
    ErrorCode DISPATCH_STATUS_ERROR = new ErrorCode(1_005_006_002, "调度状态错误");

    // ========== 联动模块 1-005-007-xxx ==========
    ErrorCode LINKAGE_NOT_EXISTS = new ErrorCode(1_005_007_001, "联动记录不存在");
    ErrorCode LINKAGE_STATUS_ERROR = new ErrorCode(1_005_007_002, "联动状态错误");
}
```

### 8.2 数据字典

| 字典编码 | 字典名称 | 字典值 |
|----------|----------|--------|
| emergency_warning_type | 预警类型 | 1-泄漏, 2-火灾, 3-爆炸, 4-中毒, 5-其他 |
| emergency_warning_level | 预警等级 | 1-蓝色, 2-黄色, 3-橙色, 4-红色 |
| emergency_warning_status | 预警状态 | 0-草稿, 1-待审批, 2-已发布, 3-已升级, 4-已解除 |
| emergency_event_type | 事件类型 | 1-泄漏, 2-火灾, 3-爆炸, 4-中毒, 5-其他 |
| emergency_event_level | 事件等级 | 1-一般, 2-较大, 3-重大, 4-特别重大 |
| emergency_event_status | 事件状态 | 0-待研判, 1-处置中, 2-已控制, 3-已结案 |
| emergency_plan_type | 预案类型 | 1-综合预案, 2-专项预案, 3-现场处置方案 |
| emergency_plan_level | 预案级别 | 1-市级, 2-县区级, 3-企业级 |
| emergency_resource_type | 资源类型 | 1-人员, 2-车辆, 3-物资, 4-设备, 5-场所 |
| emergency_team_type | 队伍类型 | 1-消防队伍, 2-抢修队伍, 3-医疗队伍, 4-应急抢险队, 5-志愿者队伍 |
| emergency_expert_type | 专家类型 | 1-技术专家, 2-管理专家, 3-法律专家, 4-安全专家 |
| emergency_drill_type | 演练类型 | 1-桌面演练, 2-实战演练, 3-专项演练, 4-综合演练 |
| emergency_dispatch_status | 调度状态 | 0-已调度, 1-在途中, 2-已到达, 3-执行中, 4-已完成, 5-已归还 |
| emergency_linkage_type | 联动类型 | 1-请求支援, 2-提供支援 |

### 8.3 权限标识

| 模块 | 权限标识 | 说明 |
|------|----------|------|
| 预警管理 | gas:emergency:warning:create | 创建预警 |
| 预警管理 | gas:emergency:warning:update | 编辑预警 |
| 预警管理 | gas:emergency:warning:delete | 删除预警 |
| 预警管理 | gas:emergency:warning:query | 查询预警 |
| 预警管理 | gas:emergency:warning:publish | 发布预警 |
| 预警管理 | gas:emergency:warning:approve | 审批预警 |
| 预警管理 | gas:emergency:warning:cancel | 解除预警 |
| 事件处置 | gas:emergency:event:report | 上报事件 |
| 事件处置 | gas:emergency:event:assess | 事件研判 |
| 事件处置 | gas:emergency:event:close | 事件结案 |
| 事件处置 | gas:emergency:event:query | 查询事件 |
| 预案管理 | gas:emergency:plan:create | 创建预案 |
| 预案管理 | gas:emergency:plan:update | 编辑预案 |
| 预案管理 | gas:emergency:plan:delete | 删除预案 |
| 预案管理 | gas:emergency:plan:query | 查询预案 |
| 预案管理 | gas:emergency:plan:approve | 审批预案 |
| 资源管理 | gas:emergency:resource:create | 创建资源 |
| 资源管理 | gas:emergency:resource:update | 编辑资源 |
| 资源管理 | gas:emergency:resource:delete | 删除资源 |
| 资源管理 | gas:emergency:resource:query | 查询资源 |
| 资源调度 | gas:emergency:dispatch:create | 创建调度 |
| 资源调度 | gas:emergency:dispatch:query | 查询调度 |
| 演练管理 | gas:emergency:drill:create | 创建演练 |
| 演练管理 | gas:emergency:drill:update | 编辑演练 |
| 演练管理 | gas:emergency:drill:query | 查询演练 |
| 演练管理 | gas:emergency:drill:approve | 审批演练 |
| 跨区联动 | gas:emergency:linkage:request | 发起联动 |
| 跨区联动 | gas:emergency:linkage:respond | 响应联动 |
| 跨区联动 | gas:emergency:linkage:query | 查询联动 |

### 8.4 相关文档

- [ruoyi-vue-pro 工作流模块](../skills/ruoyi-vue-pro/bpm.md)
- [ruoyi-vue-pro 消息通知](../skills/ruoyi-vue-pro/system.md)
- [ruoyi-vue-pro WebSocket](../skills/ruoyi-vue-pro/framework.md)
- [整体架构规划](./00-overall-architecture.md)
- [监测预警域设计](./01-monitoring-domain.md)
- [巡查防控域设计](./02-patrol-domain.md)

---

*文档版本: 1.0.0*
*最后更新: 2026-01-27*
*状态: 规划中*


# 巡查防控域详细设计

> 松原市燃气安全监管平台 - 巡查防控域
>
> 版本: 1.0.0
> 更新时间: 2026-01-27
> 状态: 规划中

---

## 一、领域概述

### 1.1 业务价值

巡查防控域是松原市燃气安全监管平台的**核心域**，承担着燃气设施日常巡查、隐患发现与整改的核心职责。通过规范化的巡查流程配置、任务自动生成与分派、移动端现场执行、隐患闭环管理，实现"人防+技防"相结合的安全防控体系。

### 1.2 功能范围

| 功能模块 | 功能点 | 需求编号 |
|----------|--------|----------|
| 周期规则管理 | 周期规则配置、新增修改、停用删除、执行监控 | 44-47 |
| 作业内容管理 | 作业内容配置、检查范围设置、新增修改、停用删除 | 48-51 |
| 流程配置 | 流程节点配置、流程规则设置、新增修改、停用删除 | 52-55 |
| 计划任务管理 | 计划查询、区域分派、企业分派 | 56-58 |
| 巡查执行 | 巡查运维、巡查路线 | 26-27 |
| 隐患管理 | 隐患排查、隐患整改跟踪 | 28 |
| 疑难案件 | 疑难案件管理 | 59 |

**共覆盖19项功能需求**

### 1.3 核心角色

| 角色 | 职责 | 主要操作 |
|------|------|----------|
| 市级监管员 | 全市巡查监督、疑难案件处理 | 查看巡查统计、处理疑难案件、督办整改 |
| 县区监管员 | 辖区巡查监督、问题督办 | 查看辖区巡查、督办隐患整改、上报疑难案件 |
| 企业安全管理员 | 巡查计划制定、配置管理 | 配置周期规则、制定计划、审核隐患 |
| 巡检班长 | 任务分派、质量检查 | 分派任务、审核巡检结果、跟踪整改 |
| 巡检员 | 现场巡检执行 | 执行巡检、上报隐患、填写记录 |
| 乡镇安监员 | 辖区巡查配合 | 参与巡查、上报问题、协调整改 |

---

## 二、业务流程设计

### 2.1 核心业务流程总览

```
┌─────────────────────────────────────────────────────────────────────────────────┐
│                           巡查防控域核心业务流程                                  │
├─────────────────────────────────────────────────────────────────────────────────┤
│                                                                                 │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          配置层（一次性配置）                              │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐                           │  │
│  │  │ 周期规则  │    │ 作业内容  │    │ 流程配置  │                           │  │
│  │  │ 配置     │    │ 配置     │    │          │                           │  │
│  │  └──────────┘    └──────────┘    └──────────┘                           │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼                                           │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          执行层（周期性执行）                              │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │  │
│  │  │ 计划生成  │───►│ 任务分派  │───►│ 现场执行  │───►│ 结果审核  │          │  │
│  │  │ (自动)   │    │ (班长)   │    │ (巡检员) │    │ (班长)   │          │  │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼ 发现隐患                                  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          隐患层（闭环管理）                                │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐    ┌──────────┐          │  │
│  │  │ 隐患上报  │───►│ 隐患确认  │───►│ 整改执行  │───►│ 整改验收  │          │  │
│  │  │ (巡检员) │    │ (班长)   │    │ (责任人) │    │ (多级)   │          │  │
│  │  └──────────┘    └──────────┘    └──────────┘    └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                    │                                           │
│                                    ▼ 疑难问题                                  │
│  ┌──────────────────────────────────────────────────────────────────────────┐  │
│  │                          升级层（疑难处理）                                │  │
│  │  ┌──────────┐    ┌──────────┐    ┌──────────┐                           │  │
│  │  │ 案件上报  │───►│ 专家会商  │───►│ 处理结案  │                           │  │
│  │  │ (县区)   │    │ (市级)   │    │          │                           │  │
│  │  └──────────┘    └──────────┘    └──────────┘                           │  │
│  └──────────────────────────────────────────────────────────────────────────┘  │
│                                                                                 │
└─────────────────────────────────────────────────────────────────────────────────┘
```

### 2.2 巡查任务执行流程（核心流程）

#### 2.2.1 流程图

```
┌─────────────┐
│ 定时触发    │
│ (Cron表达式)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 读取周期规则│
│ 和作业内容  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 自动生成    │
│ 巡查计划    │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 生成巡查任务│
│ (按区域/企业)│
└──────┬──────┘
       │
       ▼
┌─────────────┐    自动分派    ┌─────────────┐
│ 巡检班长    │───────────────►│ 按规则自动  │
│ 分派任务    │               │ 分配给巡检员│
└──────┬──────┘               └─────────────┘
       │手动分派
       ▼
┌─────────────┐
│ 巡检员接收  │
│ 任务(移动端)│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 查看任务详情│
│ 和巡查路线  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 到达现场    │
│ (GPS签到)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 逐项检查    │◄──────┐
│ 填写结果    │       │
└──────┬──────┘       │
       │              │
       ▼              │
┌─────────────┐  有   │
│ 发现隐患？  │───────┘
└──────┬──────┘  上报隐患后继续检查
       │无
       ▼
┌─────────────┐
│ 完成签退    │
│ (GPS签退)   │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 提交巡查报告│
└──────┬──────┘
       │
       ▼
┌─────────────┐    不通过    ┌─────────────┐
│ 巡检班长    │─────────────►│ 退回补充    │
│ 审核       │              └─────────────┘
└──────┬──────┘
       │通过
       ▼
┌─────────────┐
│ 任务完成    │
│ 归档统计    │
└─────────────┘
```

#### 2.2.2 流程节点详情

| 节点编号 | 节点名称 | 处理人 | 表单字段 | 时限要求 | 流转规则 |
|----------|----------|--------|----------|----------|----------|
| N1 | 计划生成 | 系统自动 | 计划名称、计划周期、巡查范围、作业内容 | - | 按Cron表达式触发 |
| N2 | 任务生成 | 系统自动 | 任务编号、巡查对象、检查项列表、计划时间 | - | 自动流转到N3 |
| N3 | 任务分派 | 巡检班长 | 执行人、计划开始时间、计划结束时间 | 计划前1天 | 分派后→N4 |
| N4 | 任务接收 | 巡检员 | 确认接收 | 30分钟内 | 接收后→N5 |
| N5 | 现场签到 | 巡检员 | 签到时间、签到位置、签到照片 | 计划时间内 | 签到后→N6 |
| N6 | 执行检查 | 巡检员 | 检查项结果、现场照片、备注说明 | 根据检查项数量 | 完成后→N7 |
| N7 | 现场签退 | 巡检员 | 签退时间、签退位置 | - | 签退后→N8 |
| N8 | 提交报告 | 巡检员 | 巡查总结、问题汇总 | 当天内 | 提交后→N9 |
| N9 | 班长审核 | 巡检班长 | 审核意见、审核结果 | 2小时内 | 通过→结束，不通过→N6 |

#### 2.2.3 检查项类型

| 检查类型 | 检查内容 | 结果选项 | 是否必填 |
|----------|----------|----------|----------|
| 选择题 | 设备运行状态 | 正常/异常/不适用 | 是 |
| 数值题 | 压力表读数 | 数值输入 | 是 |
| 拍照题 | 现场环境照片 | 照片上传 | 是 |
| 文本题 | 问题描述 | 文本输入 | 否 |
| 签名题 | 负责人签字 | 手写签名 | 否 |

### 2.3 隐患整改流程

#### 2.3.1 流程图

```
┌─────────────┐
│ 巡检员发现  │
│ 隐患并上报  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 填写隐患信息│
│ (类型/等级) │
└──────┬──────┘
       │
       ▼
┌─────────────┐    不确认    ┌─────────────┐
│ 巡检班长    │─────────────►│ 退回修改    │
│ 确认隐患    │              │ 或标记无效  │
└──────┬──────┘              └─────────────┘
       │确认
       ▼
┌─────────────┐
│ 判定隐患等级│
└──────┬──────┘
       │
       ├─────────────────────────────────┐
       │一般隐患                         │重大隐患
       ▼                                 ▼
┌─────────────┐                   ┌─────────────┐
│ 企业内部    │                   │ 上报县区    │
│ 整改流程    │                   │ 监管部门    │
└──────┬──────┘                   └──────┬──────┘
       │                                 │
       ▼                                 ▼
┌─────────────┐                   ┌─────────────┐
│ 指定整改    │                   │ 县区监管员  │
│ 责任人/时限 │                   │ 督办跟踪    │
└──────┬──────┘                   └──────┬──────┘
       │                                 │
       ▼                                 ▼
┌─────────────┐                   ┌─────────────┐
│ 责任人执行  │                   │ 企业执行    │
│ 整改措施    │                   │ 整改措施    │
└──────┬──────┘                   └──────┬──────┘
       │                                 │
       ▼                                 ▼
┌─────────────┐                   ┌─────────────┐
│ 提交整改    │                   │ 提交整改    │
│ 完成报告    │                   │ 完成报告    │
└──────┬──────┘                   └──────┬──────┘
       │                                 │
       ▼                                 ▼
┌─────────────┐                   ┌─────────────┐
│ 巡检班长    │                   │ 企业安全    │
│ 验收       │                   │ 管理员验收  │
└──────┬──────┘                   └──────┬──────┘
       │                                 │
       ▼                                 ▼
┌─────────────┐                   ┌─────────────┐
│ 企业安全    │                   │ 县区监管员  │
│ 管理员复核  │                   │ 复核验收    │
└──────┬──────┘                   └──────┬──────┘
       │                                 │
       ▼                                 ▼
┌─────────────┐                   ┌─────────────┐
│ 隐患关闭    │                   │ 市级监管员  │
│ 归档       │                   │ 终审(可选)  │
└─────────────┘                   └──────┬──────┘
                                         │
                                         ▼
                                  ┌─────────────┐
                                  │ 隐患关闭    │
                                  │ 归档       │
                                  └─────────────┘
```

#### 2.3.2 隐患等级定义

| 等级 | 名称 | 定义 | 整改时限 | 审批层级 |
|------|------|------|----------|----------|
| 1 | 一般隐患 | 危害较小，不会造成人员伤亡或重大财产损失 | 7天 | 企业内部 |
| 2 | 较大隐患 | 可能造成人员伤亡或较大财产损失 | 3天 | 企业+县区 |
| 3 | 重大隐患 | 可能造成重大人员伤亡或重大财产损失 | 24小时 | 企业+县区+市级 |

#### 2.3.3 隐患类型分类

| 一级分类 | 二级分类 | 说明 |
|----------|----------|------|
| 设备隐患 | 设备老化、设备损坏、设备缺失 | 监测设备、阀门等 |
| 管网隐患 | 管道腐蚀、管道泄漏、管道占压 | 燃气管线 |
| 场站隐患 | 消防设施、安全标识、通风设施 | 场站设施 |
| 用户隐患 | 私接乱改、超期未检、违规使用 | 用户端 |
| 环境隐患 | 第三方施工、地质灾害、其他 | 外部环境 |

### 2.4 周期规则配置流程

#### 2.4.1 周期规则说明

周期规则用于定义巡查任务的自动生成规则，支持灵活的周期配置。

#### 2.4.2 周期类型

| 周期类型 | Cron表达式示例 | 说明 | 适用场景 |
|----------|----------------|------|----------|
| 每日 | 0 0 8 * * ? | 每天8点生成 | 重点区域日巡 |
| 每周 | 0 0 8 ? * MON | 每周一8点生成 | 常规设施周巡 |
| 每月 | 0 0 8 1 * ? | 每月1日8点生成 | 全面检查月巡 |
| 每季度 | 0 0 8 1 1,4,7,10 * ? | 每季度首日8点生成 | 季度专项检查 |
| 自定义 | 用户自定义 | 灵活配置 | 特殊巡查需求 |

#### 2.4.3 规则配置要素

```
周期规则 = {
    规则名称: "重点场站日巡规则",
    规则编码: "DAILY_KEY_STATION",
    周期类型: "每日",
    Cron表达式: "0 0 8 * * ?",
    巡查范围: {
        范围类型: "设施类型",
        设施类型: ["场站"],
        设施等级: ["重点"],
        区域范围: ["宁江区", "前郭县"]
    },
    作业内容: {
        作业模板ID: 10,
        检查项数量: 20
    },
    任务分派: {
        分派方式: "自动分派",
        分派规则: "按设施所属企业"
    },
    有效期: {
        开始日期: "2026-01-01",
        结束日期: "2026-12-31"
    },
    状态: "启用"
}
```

### 2.5 疑难案件处理流程

#### 2.5.1 流程图

```
┌─────────────┐
│ 县区监管员  │
│ 上报疑难案件│
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 填写案件信息│
│ (问题描述)  │
└──────┬──────┘
       │
       ▼
┌─────────────┐
│ 市级监管员  │
│ 接收案件    │
└──────┬──────┘
       │
       ▼
┌─────────────┐    需要    ┌─────────────┐
│ 是否需要    │───────────►│ 邀请专家    │
│ 专家会商？  │            │ 参与会商    │
└──────┬──────┘            └──────┬──────┘
       │不需要                    │
       │                          │
       └──────────┬───────────────┘
                  ▼
           ┌─────────────┐
           │ 组织会商    │
           │ 研究方案    │
           └──────┬──────┘
                  │
                  ▼
           ┌─────────────┐
           │ 形成处理意见│
           │ 和解决方案  │
           └──────┬──────┘
                  │
                  ▼
           ┌─────────────┐
           │ 下发处理指令│
           │ 给县区/企业 │
           └──────┬──────┘
                  │
                  ▼
           ┌─────────────┐
           │ 县区/企业   │
           │ 执行处理    │
           └──────┬──────┘
                  │
                  ▼
           ┌─────────────┐
           │ 反馈处理结果│
           └──────┬──────┘
                  │
                  ▼
           ┌─────────────┐    不满意    ┌─────────────┐
           │ 市级监管员  │─────────────►│ 继续跟进    │
           │ 验收结果    │              └─────────────┘
           └──────┬──────┘
                  │满意
                  ▼
           ┌─────────────┐
           │ 案件结案    │
           │ 归档总结    │
           └─────────────┘
```

---

## 三、角色使用场景

### 3.1 企业安全管理员使用场景

#### 场景1：配置周期规则

**操作步骤**：
1. 登录系统，进入巡查防控模块
2. 点击"周期规则配置"
3. 新增规则，填写规则信息：
   - 规则名称：重点场站日巡
   - 周期类型：每日
   - Cron表达式：0 0 8 * * ?
   - 巡查范围：选择本企业的重点场站
   - 作业内容：选择"场站日常检查"模板
4. 设置任务分派规则（自动分派给巡检班长）
5. 设置有效期
6. 保存并启用规则

**涉及功能**：周期规则配置、作业内容选择、分派规则设置

#### 场景2：制定巡查计划

**操作步骤**：
1. 进入"巡查计划管理"
2. 查看系统自动生成的计划
3. 根据实际情况调整计划：
   - 增加临时巡查任务
   - 调整巡查时间
   - 修改巡查范围
4. 提交计划审批（如需要）
5. 计划生效后，系统自动生成任务

**涉及功能**：计划查询、计划调整、计划审批

#### 场景3：审核隐患整改

**操作步骤**：
1. 接收隐患整改完成通知
2. 查看隐患详情和整改记录
3. 查看整改前后对比照片
4. 判断整改是否合格：
   - 合格：审核通过，关闭隐患
   - 不合格：退回重新整改，说明原因
5. 填写审核意见
6. 提交审核结果

**涉及功能**：隐患审核、整改验收、照片对比

### 3.2 巡检班长使用场景

#### 场景1：分派巡查任务

**操作步骤**：
1. 登录系统，查看待分派任务列表
2. 选择一个或多个任务
3. 查看任务详情（巡查对象、检查项、计划时间）
4. 选择执行人（巡检员）
5. 设置计划开始和结束时间
6. 添加任务说明（如有特殊要求）
7. 确认分派，系统推送通知给巡检员

**涉及功能**：任务列表、任务分派、人员选择、消息推送

#### 场景2：审核巡查报告

**操作步骤**：
1. 接收巡检员提交的巡查报告
2. 查看报告详情：
   - 签到签退记录（时间、位置）
   - 检查项完成情况
   - 现场照片
   - 问题汇总
3. 判断报告质量：
   - 检查项是否全部完成
   - 照片是否清晰完整
   - 问题描述是否准确
4. 审核结果：
   - 通过：任务完成
   - 不通过：退回补充，说明原因
5. 填写审核意见
6. 提交审核

**涉及功能**：报告审核、照片查看、退回补充

#### 场景3：确认隐患等级

**操作步骤**：
1. 接收巡检员上报的隐患
2. 查看隐患详情和现场照片
3. 根据隐患定义判定等级：
   - 一般隐患：企业内部整改
   - 较大隐患：上报县区监管
   - 重大隐患：立即上报并采取临时措施
4. 指定整改责任人和时限
5. 确认隐患并启动整改流程

**涉及功能**：隐患确认、等级判定、责任人指定

### 3.3 巡检员使用场景（移动端）

#### 场景1：执行巡查任务

**操作步骤**：
1. 打开移动APP，查看今日任务
2. 选择一个任务，查看详情
3. 点击"开始巡查"
4. 使用导航功能前往巡查地点
5. 到达后点击"现场签到"（自动获取GPS位置）
6. 拍摄现场环境照片
7. 逐项完成检查：
   - 选择题：选择检查结果
   - 数值题：输入测量数值
   - 拍照题：拍摄设备照片
   - 文本题：填写问题描述
8. 如发现隐患，点击"上报隐患"
9. 完成所有检查项后，点击"现场签退"
10. 填写巡查总结
11. 提交巡查报告

**涉及功能**：任务查看、导航、签到签退、检查项填写、照片上传、隐患上报

#### 场景2：上报隐患

**操作步骤**：
1. 在巡查过程中发现隐患
2. 点击"上报隐患"按钮
3. 填写隐患信息：
   - 隐患类型（一级、二级分类）
   - 隐患描述
   - 初步判断的等级
   - 建议整改措施
4. 拍摄隐患照片（多角度）
5. 标注隐患位置（自动获取GPS）
6. 提交隐患报告
7. 继续完成巡查任务

**涉及功能**：隐患上报、分类选择、照片上传、位置标注

### 3.4 县区监管员使用场景

#### 场景1：督办隐患整改

**操作步骤**：
1. 登录系统，查看辖区隐患列表
2. 筛选"重大隐患"或"超期未整改"
3. 选择需要督办的隐患
4. 查看隐患详情和整改进度
5. 填写督办意见：
   - 要求限期整改
   - 明确整改要求
   - 必要时要求停产整改
6. 发送督办通知给企业
7. 跟踪整改进度
8. 整改完成后进行验收

**涉及功能**：隐患查询、督办管理、进度跟踪、整改验收

#### 场景2：上报疑难案件

**操作步骤**：
1. 发现疑难复杂问题
2. 进入"疑难案件管理"
3. 新增案件，填写信息：
   - 案件标题
   - 问题描述
   - 涉及企业/设施
   - 已采取的措施
   - 遇到的困难
   - 需要的支持
4. 上传相关资料（照片、文档）
5. 提交给市级监管员
6. 等待市级处理意见
7. 执行处理方案
8. 反馈处理结果

**涉及功能**：案件上报、资料上传、处理跟踪

### 3.5 市级监管员使用场景

#### 场景1：处理疑难案件

**操作步骤**：
1. 接收县区上报的疑难案件
2. 查看案件详情和相关资料
3. 判断是否需要专家会商
4. 如需要，邀请相关专家：
   - 选择专家（按专业领域）
   - 发送会商邀请
   - 安排会商时间
5. 组织会商会议（线上/线下）
6. 讨论形成处理意见
7. 编制处理方案
8. 下发处理指令给县区/企业
9. 跟踪处理进度
10. 验收处理结果
11. 案件结案归档

**涉及功能**：案件管理、专家邀请、会商组织、方案编制、进度跟踪

---

## 四、数据库设计

### 4.1 表清单

| 表名 | 说明 | 数据量级 | 备注 |
|------|------|----------|------|
| gas_patrol_cycle_rule | 周期规则表 | 1000+ | 配置表 |
| gas_patrol_work_content | 作业内容表 | 500+ | 配置表 |
| gas_patrol_check_item | 检查项表 | 5000+ | 配置表 |
| gas_patrol_plan | 巡查计划表 | 1万+ | 业务表 |
| gas_patrol_task | 巡查任务表 | 10万+ | 核心业务表 |
| gas_patrol_record | 巡查记录表 | 10万+ | 执行记录 |
| gas_patrol_check_result | 检查结果表 | 100万+ | 检查明细 |
| gas_patrol_hazard | 隐患表 | 5万+ | 核心业务表 |
| gas_patrol_hazard_rectify | 隐患整改记录表 | 5万+ | 整改记录 |
| gas_patrol_difficult_case | 疑难案件表 | 1000+ | 案件管理 |
| gas_patrol_route | 巡查路线表 | 1000+ | 路线规划 |

### 4.2 核心表结构

#### 4.2.1 周期规则表（gas_patrol_cycle_rule）

```sql
CREATE TABLE gas_patrol_cycle_rule (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '规则ID',
    rule_name VARCHAR(100) NOT NULL COMMENT '规则名称',
    rule_code VARCHAR(50) NOT NULL COMMENT '规则编码',
    cycle_type TINYINT NOT NULL COMMENT '周期类型：1-每日 2-每周 3-每月 4-每季度 5-自定义',
    cron_expression VARCHAR(50) NOT NULL COMMENT 'Cron表达式',
    scope_type TINYINT NOT NULL COMMENT '范围类型：1-区域 2-企业 3-设施类型 4-自定义',
    scope_config TEXT COMMENT '范围配置（JSON格式）',
    work_content_id BIGINT NOT NULL COMMENT '作业内容ID',
    assign_type TINYINT DEFAULT 1 COMMENT '分派方式：1-自动分派 2-手动分派',
    assign_rule TEXT COMMENT '分派规则（JSON格式）',
    start_date DATE COMMENT '有效开始日期',
    end_date DATE COMMENT '有效结束日期',
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
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_is_enabled (is_enabled)
) COMMENT='周期规则表';
```

#### 4.2.2 作业内容表（gas_patrol_work_content）

```sql
CREATE TABLE gas_patrol_work_content (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '作业内容ID',
    content_name VARCHAR(100) NOT NULL COMMENT '作业内容名称',
    content_code VARCHAR(50) NOT NULL COMMENT '作业内容编码',
    content_type TINYINT NOT NULL COMMENT '内容类型：1-场站巡查 2-管网巡查 3-用户巡查 4-专项检查',
    target_type TINYINT NOT NULL COMMENT '目标类型：1-场站 2-管段 3-用户 4-设备',
    check_item_count INT DEFAULT 0 COMMENT '检查项数量',
    estimated_duration INT COMMENT '预计耗时（分钟）',
    is_enabled TINYINT DEFAULT 1 COMMENT '是否启用：0-否 1-是',
    enterprise_id BIGINT COMMENT '所属企业ID（为空表示通用模板）',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    UNIQUE KEY uk_content_code (content_code),
    INDEX idx_content_type (content_type),
    INDEX idx_enterprise_id (enterprise_id)
) COMMENT='作业内容表';
```

#### 4.2.3 检查项表（gas_patrol_check_item）

```sql
CREATE TABLE gas_patrol_check_item (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '检查项ID',
    work_content_id BIGINT NOT NULL COMMENT '作业内容ID',
    item_name VARCHAR(200) NOT NULL COMMENT '检查项名称',
    item_code VARCHAR(50) COMMENT '检查项编码',
    item_type TINYINT NOT NULL COMMENT '检查项类型：1-选择题 2-数值题 3-拍照题 4-文本题 5-签名题',
    item_options TEXT COMMENT '选项配置（JSON格式）',
    is_required TINYINT DEFAULT 1 COMMENT '是否必填：0-否 1-是',
    sort_order INT DEFAULT 0 COMMENT '排序',
    remark VARCHAR(500) COMMENT '备注说明',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    INDEX idx_work_content_id (work_content_id),
    INDEX idx_sort_order (sort_order)
) COMMENT='检查项表';
```

#### 4.2.4 巡查任务表（gas_patrol_task）

```sql
CREATE TABLE gas_patrol_task (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '任务ID',
    task_no VARCHAR(32) NOT NULL COMMENT '任务编号',
    plan_id BIGINT COMMENT '计划ID',
    cycle_rule_id BIGINT COMMENT '周期规则ID',
    work_content_id BIGINT NOT NULL COMMENT '作业内容ID',
    work_content_name VARCHAR(100) COMMENT '作业内容名称（冗余）',
    target_type TINYINT NOT NULL COMMENT '巡查对象类型：1-场站 2-管段 3-用户 4-设备',
    target_id BIGINT NOT NULL COMMENT '巡查对象ID',
    target_name VARCHAR(200) COMMENT '巡查对象名称（冗余）',
    target_location VARCHAR(200) COMMENT '巡查对象位置',
    target_longitude DECIMAL(10,7) COMMENT '经度',
    target_latitude DECIMAL(10,7) COMMENT '纬度',
    enterprise_id BIGINT NOT NULL COMMENT '所属企业ID',
    enterprise_name VARCHAR(100) COMMENT '企业名称（冗余）',
    assign_user_id BIGINT COMMENT '分派人ID',
    assign_time DATETIME COMMENT '分派时间',
    executor_id BIGINT COMMENT '执行人ID',
    executor_name VARCHAR(50) COMMENT '执行人姓名（冗余）',
    plan_start_time DATETIME COMMENT '计划开始时间',
    plan_end_time DATETIME COMMENT '计划结束时间',
    actual_start_time DATETIME COMMENT '实际开始时间',
    actual_end_time DATETIME COMMENT '实际结束时间',
    status TINYINT DEFAULT 0 COMMENT '状态：0-待分派 1-待执行 2-执行中 3-待审核 4-已完成 5-已逾期',
    is_timeout TINYINT DEFAULT 0 COMMENT '是否超时：0-否 1-是',
    check_item_total INT DEFAULT 0 COMMENT '检查项总数',
    check_item_completed INT DEFAULT 0 COMMENT '已完成检查项数',
    hazard_count INT DEFAULT 0 COMMENT '发现隐患数',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_task_no (task_no),
    INDEX idx_plan_id (plan_id),
    INDEX idx_executor_id (executor_id),
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_status (status),
    INDEX idx_plan_start_time (plan_start_time)
) COMMENT='巡查任务表';
```

#### 4.2.5 隐患表（gas_patrol_hazard）

```sql
CREATE TABLE gas_patrol_hazard (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '隐患ID',
    hazard_no VARCHAR(32) NOT NULL COMMENT '隐患编号',
    task_id BIGINT COMMENT '巡查任务ID',
    hazard_type_1 TINYINT NOT NULL COMMENT '隐患一级分类：1-设备 2-管网 3-场站 4-用户 5-环境',
    hazard_type_2 TINYINT NOT NULL COMMENT '隐患二级分类',
    hazard_level TINYINT NOT NULL COMMENT '隐患等级：1-一般 2-较大 3-重大',
    hazard_title VARCHAR(200) NOT NULL COMMENT '隐患标题',
    hazard_description TEXT COMMENT '隐患描述',
    hazard_location VARCHAR(200) COMMENT '隐患位置',
    hazard_longitude DECIMAL(10,7) COMMENT '经度',
    hazard_latitude DECIMAL(10,7) COMMENT '纬度',
    hazard_photos VARCHAR(1000) COMMENT '隐患照片（逗号分隔）',
    enterprise_id BIGINT NOT NULL COMMENT '所属企业ID',
    enterprise_name VARCHAR(100) COMMENT '企业名称（冗余）',
    report_user_id BIGINT NOT NULL COMMENT '上报人ID',
    report_user_name VARCHAR(50) COMMENT '上报人姓名（冗余）',
    report_time DATETIME NOT NULL COMMENT '上报时间',
    confirm_user_id BIGINT COMMENT '确认人ID',
    confirm_time DATETIME COMMENT '确认时间',
    confirm_result TINYINT COMMENT '确认结果：1-确认 2-无效',
    rectify_user_id BIGINT COMMENT '整改责任人ID',
    rectify_user_name VARCHAR(50) COMMENT '整改责任人姓名',
    rectify_deadline DATETIME COMMENT '整改期限',
    rectify_measures TEXT COMMENT '整改措施',
    rectify_complete_time DATETIME COMMENT '整改完成时间',
    rectify_photos VARCHAR(1000) COMMENT '整改照片（逗号分隔）',
    status TINYINT DEFAULT 0 COMMENT '状态：0-待确认 1-待整改 2-整改中 3-待验收 4-已完成 5-已关闭',
    is_timeout TINYINT DEFAULT 0 COMMENT '是否超期：0-否 1-是',
    audit_level TINYINT COMMENT '审核层级：1-企业 2-县区 3-市级',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_hazard_no (hazard_no),
    INDEX idx_task_id (task_id),
    INDEX idx_enterprise_id (enterprise_id),
    INDEX idx_hazard_level (hazard_level),
    INDEX idx_status (status),
    INDEX idx_report_time (report_time)
) COMMENT='隐患表';
```

#### 4.2.6 疑难案件表（gas_patrol_difficult_case）

```sql
CREATE TABLE gas_patrol_difficult_case (
    id BIGINT PRIMARY KEY AUTO_INCREMENT COMMENT '案件ID',
    case_no VARCHAR(32) NOT NULL COMMENT '案件编号',
    case_title VARCHAR(200) NOT NULL COMMENT '案件标题',
    case_description TEXT NOT NULL COMMENT '问题描述',
    related_type TINYINT COMMENT '关联类型：1-隐患 2-报警 3-其他',
    related_id BIGINT COMMENT '关联对象ID',
    enterprise_id BIGINT COMMENT '涉及企业ID',
    facility_id BIGINT COMMENT '涉及设施ID',
    taken_measures TEXT COMMENT '已采取措施',
    difficulties TEXT COMMENT '遇到的困难',
    support_needed TEXT COMMENT '需要的支持',
    attachments VARCHAR(1000) COMMENT '附件（逗号分隔）',
    report_user_id BIGINT NOT NULL COMMENT '上报人ID',
    report_user_name VARCHAR(50) COMMENT '上报人姓名',
    report_dept_id BIGINT COMMENT '上报部门ID',
    report_time DATETIME NOT NULL COMMENT '上报时间',
    accept_user_id BIGINT COMMENT '受理人ID',
    accept_time DATETIME COMMENT '受理时间',
    is_expert_consult TINYINT DEFAULT 0 COMMENT '是否专家会商：0-否 1-是',
    expert_ids VARCHAR(200) COMMENT '参与专家ID（逗号分隔）',
    consult_time DATETIME COMMENT '会商时间',
    consult_summary TEXT COMMENT '会商纪要',
    solution TEXT COMMENT '解决方案',
    instruction TEXT COMMENT '处理指令',
    execute_result TEXT COMMENT '执行结果',
    status TINYINT DEFAULT 0 COMMENT '状态：0-待受理 1-处理中 2-待验收 3-已结案',
    close_time DATETIME COMMENT '结案时间',
    remark VARCHAR(500) COMMENT '备注',
    creator BIGINT COMMENT '创建人',
    create_time DATETIME DEFAULT CURRENT_TIMESTAMP COMMENT '创建时间',
    updater BIGINT COMMENT '更新人',
    update_time DATETIME DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP COMMENT '更新时间',
    deleted TINYINT DEFAULT 0 COMMENT '是否删除：0-否 1-是',
    tenant_id BIGINT COMMENT '租户ID',
    INDEX idx_case_no (case_no),
    INDEX idx_report_user_id (report_user_id),
    INDEX idx_status (status),
    INDEX idx_report_time (report_time)
) COMMENT='疑难案件表';
```

---

## 五、API接口设计

### 5.1 接口清单

| 模块 | 接口路径 | 方法 | 说明 | 权限标识 |
|------|----------|------|------|----------|
| 周期规则 | /gas/patrol/rule/page | GET | 规则分页查询 | gas:patrol:rule:query |
| 周期规则 | /gas/patrol/rule/create | POST | 创建规则 | gas:patrol:rule:create |
| 周期规则 | /gas/patrol/rule/update | PUT | 更新规则 | gas:patrol:rule:update |
| 周期规则 | /gas/patrol/rule/delete | DELETE | 删除规则 | gas:patrol:rule:delete |
| 周期规则 | /gas/patrol/rule/enable | PUT | 启用/停用规则 | gas:patrol:rule:update |
| 作业内容 | /gas/patrol/work/page | GET | 作业内容分页 | gas:patrol:work:query |
| 作业内容 | /gas/patrol/work/create | POST | 创建作业内容 | gas:patrol:work:create |
| 作业内容 | /gas/patrol/work/update | PUT | 更新作业内容 | gas:patrol:work:update |
| 检查项 | /gas/patrol/item/list | GET | 检查项列表 | gas:patrol:item:query |
| 检查项 | /gas/patrol/item/create | POST | 创建检查项 | gas:patrol:item:create |
| 巡查任务 | /gas/patrol/task/page | GET | 任务分页查询 | gas:patrol:task:query |
| 巡查任务 | /gas/patrol/task/assign | POST | 分派任务 | gas:patrol:task:assign |
| 巡查任务 | /gas/patrol/task/accept | POST | 接收任务 | gas:patrol:task:accept |
| 巡查任务 | /gas/patrol/task/start | POST | 开始任务 | gas:patrol:task:execute |
| 巡查任务 | /gas/patrol/task/checkin | POST | 现场签到 | gas:patrol:task:execute |
| 巡查任务 | /gas/patrol/task/checkout | POST | 现场签退 | gas:patrol:task:execute |
| 巡查任务 | /gas/patrol/task/submit | POST | 提交报告 | gas:patrol:task:execute |
| 巡查任务 | /gas/patrol/task/audit | POST | 审核报告 | gas:patrol:task:audit |
| 隐患管理 | /gas/patrol/hazard/page | GET | 隐患分页查询 | gas:patrol:hazard:query |
| 隐患管理 | /gas/patrol/hazard/report | POST | 上报隐患 | gas:patrol:hazard:report |
| 隐患管理 | /gas/patrol/hazard/confirm | POST | 确认隐患 | gas:patrol:hazard:confirm |
| 隐患管理 | /gas/patrol/hazard/rectify | POST | 提交整改 | gas:patrol:hazard:rectify |
| 隐患管理 | /gas/patrol/hazard/verify | POST | 验收整改 | gas:patrol:hazard:verify |
| 隐患管理 | /gas/patrol/hazard/supervise | POST | 督办隐患 | gas:patrol:hazard:supervise |
| 疑难案件 | /gas/patrol/case/page | GET | 案件分页查询 | gas:patrol:case:query |
| 疑难案件 | /gas/patrol/case/report | POST | 上报案件 | gas:patrol:case:report |
| 疑难案件 | /gas/patrol/case/accept | POST | 受理案件 | gas:patrol:case:accept |
| 疑难案件 | /gas/patrol/case/consult | POST | 组织会商 | gas:patrol:case:consult |
| 疑难案件 | /gas/patrol/case/close | POST | 结案 | gas:patrol:case:close |

### 5.2 核心接口详情

#### 5.2.1 分派任务

**接口路径**：`POST /gas/patrol/task/assign`

**请求参数**：
```json
{
  "taskIds": [1, 2, 3],
  "executorId": 100,
  "planStartTime": "2026-01-28 08:00:00",
  "planEndTime": "2026-01-28 18:00:00",
  "remark": "注意检查重点设备"
}
```

**响应结果**：
```json
{
  "code": 0,
  "msg": "分派成功",
  "data": {
    "assignedCount": 3,
    "notifyResult": "已推送通知"
  }
}
```

#### 5.2.2 现场签到

**接口路径**：`POST /gas/patrol/task/checkin`

**请求参数**：
```json
{
  "taskId": 1,
  "checkinTime": "2026-01-28 08:30:00",
  "longitude": 124.825,
  "latitude": 45.171,
  "checkinPhoto": "https://xxx.com/checkin.jpg"
}
```

**响应结果**：
```json
{
  "code": 0,
  "msg": "签到成功",
  "data": {
    "recordId": 1000,
    "checkItems": [
      {
        "id": 1,
        "itemName": "压力表读数",
        "itemType": 2,
        "isRequired": 1
      }
    ]
  }
}
```

#### 5.2.3 上报隐患

**接口路径**：`POST /gas/patrol/hazard/report`

**请求参数**：
```json
{
  "taskId": 1,
  "hazardType1": 1,
  "hazardType2": 2,
  "hazardLevel": 2,
  "hazardTitle": "阀门老化严重",
  "hazardDescription": "现场检查发现阀门锈蚀严重，存在泄漏风险",
  "hazardLocation": "宁江区中央大街100号",
  "longitude": 124.825,
  "latitude": 45.171,
  "hazardPhotos": ["https://xxx.com/photo1.jpg", "https://xxx.com/photo2.jpg"],
  "suggestedMeasures": "建议立即更换阀门"
}
```

**响应结果**：
```json
{
  "code": 0,
  "msg": "隐患上报成功",
  "data": {
    "hazardId": 100,
    "hazardNo": "HZ202601280001"
  }
}
```

---

## 六、BPMN工作流设计

### 6.1 隐患整改审批流程

#### 6.1.1 流程定义

**流程Key**：`hazard_rectify_approval`

**流程名称**：隐患整改审批流程

**适用场景**：隐患整改完成后的多级验收审批

#### 6.1.2 BPMN流程图（重大隐患）

```xml
<?xml version="1.0" encoding="UTF-8"?>
<definitions xmlns="http://www.omg.org/spec/BPMN/20100524/MODEL"
             xmlns:flowable="http://flowable.org/bpmn"
             targetNamespace="http://flowable.org/test">

  <process id="hazard_rectify_approval" name="隐患整改审批流程" isExecutable="true">

    <!-- 开始事件 -->
    <startEvent id="startEvent" name="开始"/>

    <!-- 用户任务：巡检班长验收 -->
    <userTask id="leaderVerify" name="巡检班长验收"
              flowable:assignee="${patrolLeaderId}">
      <extensionElements>
        <flowable:formProperty id="verifyResult" name="验收结果" type="enum" required="true">
          <flowable:value id="approved" name="通过"/>
          <flowable:value id="rejected" name="不通过"/>
        </flowable:formProperty>
        <flowable:formProperty id="verifyOpinion" name="验收意见" type="string"/>
      </extensionElements>
    </userTask>

    <!-- 排他网关：判断验收结果 -->
    <exclusiveGateway id="leaderGateway" name="班长验收判断"/>

    <!-- 用户任务：企业安全管理员复核 -->
    <userTask id="safetyManagerReview" name="安全管理员复核"
              flowable:assignee="${safetyManagerId}">
      <extensionElements>
        <flowable:formProperty id="reviewResult" name="复核结果" type="enum" required="true">
          <flowable:value id="approved" name="通过"/>
          <flowable:value id="rejected" name="不通过"/>
        </flowable:formProperty>
        <flowable:formProperty id="reviewOpinion" name="复核意见" type="string"/>
      </extensionElements>
    </userTask>

    <!-- 排他网关：判断复核结果 -->
    <exclusiveGateway id="safetyGateway" name="安全管理员判断"/>

    <!-- 排他网关：判断隐患等级 -->
    <exclusiveGateway id="levelGateway" name="隐患等级判断"/>

    <!-- 用户任务：县区监管员审核（重大隐患） -->
    <userTask id="countyAudit" name="县区监管员审核"
              flowable:candidateGroups="role:GOV_COUNTY_SUPERVISOR">
      <extensionElements>
        <flowable:formProperty id="auditResult" name="审核结果" type="enum" required="true">
          <flowable:value id="approved" name="通过"/>
          <flowable:value id="rejected" name="不通过"/>
        </flowable:formProperty>
        <flowable:formProperty id="auditOpinion" name="审核意见" type="string"/>
      </extensionElements>
    </userTask>

    <!-- 排他网关：判断县区审核结果 -->
    <exclusiveGateway id="countyGateway" name="县区审核判断"/>

    <!-- 用户任务：市级监管员终审（重大隐患） -->
    <userTask id="cityAudit" name="市级监管员终审"
              flowable:candidateGroups="role:GOV_CITY_SUPERVISOR">
      <extensionElements>
        <flowable:formProperty id="finalResult" name="终审结果" type="enum" required="true">
          <flowable:value id="approved" name="通过"/>
          <flowable:value id="rejected" name="不通过"/>
        </flowable:formProperty>
        <flowable:formProperty id="finalOpinion" name="终审意见" type="string"/>
      </extensionElements>
    </userTask>

    <!-- 排他网关：判断终审结果 -->
    <exclusiveGateway id="cityGateway" name="市级审核判断"/>

    <!-- 服务任务：关闭隐患 -->
    <serviceTask id="closeHazard" name="关闭隐患"
                 flowable:class="cn.iocoder.yudao.module.gas.service.hazard.HazardCloseService"/>

    <!-- 服务任务：退回整改 -->
    <serviceTask id="returnRectify" name="退回整改"
                 flowable:class="cn.iocoder.yudao.module.gas.service.hazard.HazardReturnService"/>

    <!-- 结束事件 -->
    <endEvent id="endEvent" name="结束"/>

    <!-- 流程连线 -->
    <sequenceFlow sourceRef="startEvent" targetRef="leaderVerify"/>
    <sequenceFlow sourceRef="leaderVerify" targetRef="leaderGateway"/>
    <sequenceFlow sourceRef="leaderGateway" targetRef="safetyManagerReview">
      <conditionExpression>${verifyResult == 'approved'}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="leaderGateway" targetRef="returnRectify">
      <conditionExpression>${verifyResult == 'rejected'}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="safetyManagerReview" targetRef="safetyGateway"/>
    <sequenceFlow sourceRef="safetyGateway" targetRef="levelGateway">
      <conditionExpression>${reviewResult == 'approved'}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="safetyGateway" targetRef="returnRectify">
      <conditionExpression>${reviewResult == 'rejected'}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="levelGateway" targetRef="closeHazard">
      <conditionExpression>${hazardLevel == 1}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="levelGateway" targetRef="countyAudit">
      <conditionExpression>${hazardLevel >= 2}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="countyAudit" targetRef="countyGateway"/>
    <sequenceFlow sourceRef="countyGateway" targetRef="cityAudit">
      <conditionExpression>${auditResult == 'approved' &amp;&amp; hazardLevel == 3}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="countyGateway" targetRef="closeHazard">
      <conditionExpression>${auditResult == 'approved' &amp;&amp; hazardLevel == 2}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="countyGateway" targetRef="returnRectify">
      <conditionExpression>${auditResult == 'rejected'}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="cityAudit" targetRef="cityGateway"/>
    <sequenceFlow sourceRef="cityGateway" targetRef="closeHazard">
      <conditionExpression>${finalResult == 'approved'}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="cityGateway" targetRef="returnRectify">
      <conditionExpression>${finalResult == 'rejected'}</conditionExpression>
    </sequenceFlow>
    <sequenceFlow sourceRef="closeHazard" targetRef="endEvent"/>
    <sequenceFlow sourceRef="returnRectify" targetRef="endEvent"/>

  </process>
</definitions>
```

---

## 七、技术实现要点

### 7.1 定时任务自动生成巡查计划

```java
@Component
public class PatrolPlanGenerateJob {

    @Resource
    private PatrolCycleRuleService cycleRuleService;

    @Resource
    private PatrolTaskService taskService;

    /**
     * 每小时执行一次，检查是否有需要生成的计划
     */
    @Scheduled(cron = "0 0 * * * ?")
    public void generatePatrolPlan() {
        // 1. 获取所有启用的周期规则
        List<PatrolCycleRuleDO> rules = cycleRuleService.getEnabledRules();

        for (PatrolCycleRuleDO rule : rules) {
            // 2. 判断是否需要触发（根据Cron表达式）
            if (shouldTrigger(rule.getCronExpression())) {
                // 3. 根据规则生成任务
                generateTasksByRule(rule);
            }
        }
    }

    private void generateTasksByRule(PatrolCycleRuleDO rule) {
        // 解析范围配置
        JSONObject scopeConfig = JSON.parseObject(rule.getScopeConfig());

        // 获取巡查对象列表
        List<PatrolTarget> targets = getPatrolTargets(scopeConfig);

        // 为每个对象生成任务
        for (PatrolTarget target : targets) {
            PatrolTaskCreateReqVO taskReqVO = new PatrolTaskCreateReqVO();
            taskReqVO.setCycleRuleId(rule.getId());
            taskReqVO.setWorkContentId(rule.getWorkContentId());
            taskReqVO.setTargetType(target.getType());
            taskReqVO.setTargetId(target.getId());
            // ... 设置其他字段

            taskService.createTask(taskReqVO);
        }
    }
}
```

### 7.2 移动端GPS签到签退

```java
@Service
public class PatrolRecordService {

    /**
     * 现场签到
     */
    public void checkin(PatrolCheckinReqVO reqVO) {
        // 1. 验证任务状态
        PatrolTaskDO task = validateTask(reqVO.getTaskId());

        // 2. 验证GPS位置（是否在巡查对象附近）
        if (!isNearTarget(reqVO.getLongitude(), reqVO.getLatitude(),
                         task.getTargetLongitude(), task.getTargetLatitude())) {
            throw new ServiceException("签到位置距离巡查对象过远");
        }

        // 3. 创建巡查记录
        PatrolRecordDO record = new PatrolRecordDO();
        record.setTaskId(reqVO.getTaskId());
        record.setCheckinTime(reqVO.getCheckinTime());
        record.setCheckinLongitude(reqVO.getLongitude());
        record.setCheckinLatitude(reqVO.getLatitude());
        record.setCheckinPhoto(reqVO.getCheckinPhoto());
        patrolRecordMapper.insert(record);

        // 4. 更新任务状态为"执行中"
        updateTaskStatus(reqVO.getTaskId(), PatrolTaskStatusEnum.IN_PROGRESS);
    }

    /**
     * 判断是否在目标附近（500米内）
     */
    private boolean isNearTarget(Double lng1, Double lat1, Double lng2, Double lat2) {
        double distance = GeoUtils.getDistance(lng1, lat1, lng2, lat2);
        return distance <= 500; // 500米
    }
}
```

### 7.3 隐患超期预警

```java
@Component
public class HazardTimeoutCheckJob {

    @Resource
    private HazardService hazardService;

    @Resource
    private NotifyService notifyService;

    /**
     * 每小时检查一次隐患是否超期
     */
    @Scheduled(cron = "0 0 * * * ?")
    public void checkHazardTimeout() {
        // 1. 查询所有未完成的隐患
        List<HazardDO> hazards = hazardService.getUncompletedHazards();

        for (HazardDO hazard : hazards) {
            // 2. 判断是否超期
            if (isTimeout(hazard)) {
                // 3. 标记超期
                hazardService.markTimeout(hazard.getId());

                // 4. 发送预警通知
                sendTimeoutNotify(hazard);

                // 5. 自动升级督办
                if (shouldEscalate(hazard)) {
                    hazardService.escalate(hazard.getId());
                }
            }
        }
    }

    private boolean isTimeout(HazardDO hazard) {
        if (hazard.getRectifyDeadline() == null) {
            return false;
        }
        return LocalDateTime.now().isAfter(hazard.getRectifyDeadline());
    }
}
```

---

## 八、附录

### 8.1 隐患等级与时限对照表

| 隐患等级 | 整改时限 | 验收层级 | 超期处理 |
|----------|----------|----------|----------|
| 一般隐患 | 7天 | 企业内部（班长+安全管理员） | 县区督办 |
| 较大隐患 | 3天 | 企业+县区（安全管理员+县区监管员） | 市级督办 |
| 重大隐患 | 24小时 | 企业+县区+市级（三级审核） | 立即上报 |

### 8.2 检查项类型说明

| 类型 | 说明 | 移动端展示 | 数据格式 |
|------|------|------------|----------|
| 选择题 | 单选或多选 | 单选框/复选框 | 选项值 |
| 数值题 | 数值输入 | 数字键盘 | 数值 |
| 拍照题 | 照片上传 | 相机调用 | 图片URL |
| 文本题 | 文本输入 | 文本框 | 文本 |
| 签名题 | 手写签名 | 签名板 | 签名图片 |

### 8.3 参考文档

- [ruoyi-vue-pro 定时任务文档](https://doc.iocoder.cn/job/)
- [Flowable工作流文档](https://www.flowable.com/open-source/docs/)
- [uni-app移动开发文档](https://uniapp.dcloud.net.cn/)

---

*最后更新：2026-01-27*



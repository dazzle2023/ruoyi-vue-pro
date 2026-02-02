# CLAUDE.md - 工作空间导航

> 松原市燃气安全监管平台项目工作空间
>
> 本文档是整个工作空间的导航索引，指引到各个板块

---

## 📋 项目概述

**项目名称**：松原市市政基础设施生命线（燃气）安全监管平台

**核心目标**：
- 全面感知：燃气管网、场站、用户侧的全方位实时监测
- 智能预警：基于多源数据融合的风险识别和预警
- 协同处置：市-县-乡三级联动的问题处置闭环
- 应急调度：快速响应的应急指挥调度体系
- 数据驱动：燃气安全态势感知和决策支持

**技术栈**：基于 **ruoyi-vue-pro** 框架（Spring Boot + MyBatis-Plus + Flowable + Vue3）

---

## 🎯 核心思路

### 设计理念

1. **DDD领域驱动**：按业务领域划分模块，清晰的限界上下文
2. **业务流优先**：任何功能设计前先梳理业务流程和角色
3. **BPMN 2.0流程**：复杂审批流程使用Flowable工作流引擎
4. **框架能力复用**：充分利用ruoyi-vue-pro的现有能力
5. **GIS一体化**：所有空间数据统一通过GIS模块管理

### 核心领域

- **监测预警**：设备数据采集 → 规则判断 → 触发报警 → 推送通知 → 处置流转
- **巡查防控**：制定计划 → 生成任务 → 现场巡查 → 发现问题 → 整改验收
- **应急调度**：事件上报 → 等级研判 → 启动预案 → 资源调度 → 现场处置
- **资源管理**：企业、管网、设施、专家等基础资源管理
- **督查检查**：督查计划 → 现场检查 → 问题整改 → 复查验收
- **安全培训**：培训计划 → 课程实施 → 考试考核 → 证书颁发

---

## 📁 工作空间结构

### 1. Constitution（规则）

**路径**：[constitution/](./constitution/)

**说明**：所有Agent、所有对话必须遵循的原则

**核心文档**：
- [rules.md](./constitution/rules.md) - 开发原则、角色定位、工作规范

**关键规则**：
- 深度遵循DDD思想
- 业务流 + 数字流是数字化基础
- 重视BPMN 2.0流程和流程表单
- 规划不做简化和妥协

### 2. Skills（技能）

**路径**：[skills/](./skills/)

**说明**：框架能力文档，快速了解和使用ruoyi-vue-pro

**核心文档**：
- [ruoyi-vue-pro/README.md](./skills/ruoyi-vue-pro/README.md) - 框架能力索引
- [ruoyi-vue-pro/system.md](./skills/ruoyi-vue-pro/system.md) - 用户权限、组织架构
- [ruoyi-vue-pro/bpm.md](./skills/ruoyi-vue-pro/bpm.md) - 工作流引擎（Flowable）
- [ruoyi-vue-pro/infra.md](./skills/ruoyi-vue-pro/infra.md) - 代码生成、文件存储、定时任务
- [ruoyi-vue-pro/iot.md](./skills/ruoyi-vue-pro/iot.md) - IoT设备管理
- [ruoyi-vue-pro/framework.md](./skills/ruoyi-vue-pro/framework.md) - 数据权限、多租户、通用工具

**使用场景**：
- 新增业务模块时，查看框架提供了哪些能力
- 实现权限控制时，参考system模块
- 设计审批流程时，参考bpm模块
- 接入监测设备时，参考iot模块

### 3. Requirements（需求）

**路径**：[requirements/](./requirements/)

**说明**：项目需求文档

**核心文档**：
- [松原市市政基础设施生命线（燃气）安全监管平台建设项目初步设计.md](./requirements/松原市市政基础设施生命线（燃气）安全监管平台建设项目初步设计.md)

**内容概要**：
- 设备数据概览（24项功能）
- 设备实时监测（人防、技防、报警研判）
- 巡查防控（周期规则、作业内容、流程配置）
- 决策调度中心（预警发布、资源管理、预案管理）

### 4. Plan（规划）

**路径**：[plan/](./plan/)

**说明**：基于DDD和业务流的详细架构设计

**核心文档**：

#### 增强版架构设计（Enhanced）- 推荐使用

**路径**：[plan/enhanced/](./plan/enhanced/)

- [00-overall-architecture-enhanced.md](./plan/enhanced/00-overall-architecture-enhanced.md) - **增强版整体架构**（包含燃气专题+第一版需求融合）
  - 第一章：文档说明
  - 第二章：功能清单总览
  - 第三章：DDD领域划分
  - 第四章：技术架构设计
  - **第五章：用户角色与权限设计**（22个角色+完整权限矩阵）
  - 第六章：模块结构设计
  - 第七章：数据库设计
  - 第八章：迭代规划
  - 第九章：附录

- [燃气专题应用架构图.drawio](./plan/enhanced/燃气专题应用架构图.drawio) - **可视化架构图**
- [燃气专题应用架构图-说明.md](./plan/enhanced/燃气专题应用架构图-说明.md) - 架构图配套说明
- [规则引擎方案说明.md](./plan/enhanced/规则引擎方案说明.md) - 自研规则引擎设计（复用IoT模块）
- [角色权限矩阵补充说明.md](./plan/enhanced/角色权限矩阵补充说明.md) - 角色权限详细说明

#### 原始架构设计（待废弃）

- [00-overall-architecture.md](./plan/00-overall-architecture.md) - 原始整体架构规划
- [01-monitoring-domain.md](./plan/01-monitoring-domain.md) - 监测预警域（待创建）
- [02-patrol-domain.md](./plan/02-patrol-domain.md) - 巡查防控域（待创建）
- [03-emergency-domain.md](./plan/03-emergency-domain.md) - 应急调度域（待创建）
- [04-resource-domain.md](./plan/04-resource-domain.md) - 资源管理域（待创建）
- [05-inspection-domain.md](./plan/05-inspection-domain.md) - 督查检查域（待创建）
- [06-training-domain.md](./plan/06-training-domain.md) - 安全培训域（待创建）
- [07-analytics-domain.md](./plan/07-analytics-domain.md) - 统计分析域（待创建）
- [08-gis-visualization.md](./plan/08-gis-visualization.md) - GIS可视化（待创建）

**设计特点**：
- ✅ 完整的DDD领域划分（核心域、支撑域、高级域）
- ✅ 22个角色定义 + 7个子系统权限矩阵
- ✅ 自研规则引擎设计（复用IoT模块架构）
- ✅ 可视化架构图（drawio格式）
- ✅ 每个领域包含完整的业务流程设计
- ✅ 明确角色、流程节点、流转规则
- ✅ 基于ruoyi-vue-pro能力进行设计
- ✅ 包含数据库设计、API设计、工作流设计

---

## 🚀 快速开始

### 对于新加入的开发者

1. **阅读规则**：先阅读 [constitution/rules.md](./constitution/rules.md)
2. **了解框架**：浏览 [skills/ruoyi-vue-pro/](./skills/ruoyi-vue-pro/)
3. **理解需求**：阅读 [requirements/](./requirements/) 目录
4. **查看设计**：参考 [plan/](./plan/) 目录的领域设计

### 对于AI Agent

1. **必读规则**：每次对话开始前，读取 [constitution/rules.md](./constitution/rules.md)
2. **查询能力**：需要使用框架能力时，查询 [skills/](./skills/) 目录
3. **参考设计**：实现功能时，参考 [plan/](./plan/) 目录的设计文档
4. **遵循原则**：始终遵循DDD、业务流优先、BPMN 2.0原则

---

## OneNet物联网平台信息
### OneNet物联网平台文档地址
./对接/11-OneNET城市物联网平台V3.0公开接口文档-完整版本.pdf
### OneNet平台地址 和账号密码
http://36.139.141.197:20080 admin iot@10086

## 📊 项目进度

### 已完成

- ✅ Constitution规则文档
- ✅ Skills框架能力文档
- ✅ Plan整体架构规划

### 进行中

- 🔄 各领域详细设计文档
- 🔄 数据库设计
- 🔄 API接口设计
- 🔄 工作流设计

### 待开始

- ⏳ 代码实现
- ⏳ 测试验证
- ⏳ 部署上线

---

## 🔗 相关资源

### 官方文档

- [ruoyi-vue-pro 官方文档](https://doc.iocoder.cn/)
- [ruoyi-vue-pro GitHub](https://github.com/YunaiV/ruoyi-vue-pro)
- [Flowable 官方文档](https://www.flowable.com/open-source/docs/)
- [Cesium 官方文档](https://cesium.com/learn/)
- [GeoServer 官方文档](https://docs.geoserver.org/)

### 技术规范

- [BPMN 2.0 规范](https://www.omg.org/spec/BPMN/2.0/)
- [阿里巴巴Java开发手册](https://github.com/alibaba/p3c)

---

## 📝 文档维护

**更新原则**：
- 需求变更时，更新 requirements 目录
- 设计调整时，更新 plan 目录
- 框架升级时，更新 skills 目录
- 规则调整时，更新 constitution 目录

**版本管理**：
- 所有文档包含版本号和更新时间
- 重大变更记录在文档底部的版本历史

---

*最后更新：2026-01-27*

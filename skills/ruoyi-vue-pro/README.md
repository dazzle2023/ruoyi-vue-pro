# ruoyi-vue-pro 框架能力索引

> 本目录包含ruoyi-vue-pro框架各模块的能力文档，帮助开发者快速了解和使用框架功能。

## 技术栈

| 层次 | 技术 | 版本 |
|------|------|------|
| 后端框架 | Spring Boot | 3.x |
| ORM | MyBatis Plus | 3.5.x |
| 工作流 | Flowable | 7.x |
| 安全 | Spring Security + JWT | - |
| 缓存 | Redis | 7.x |
| 数据库 | MySQL | 8.x |

## 模块索引

| 模块 | 文档 | 说明 |
|------|------|------|
| 系统管理 | [system.md](./system.md) | 用户、角色、权限、组织架构、字典、通知等 |
| 工作流 | [bpm.md](./bpm.md) | 流程定义、流程实例、任务管理、表单设计 |
| 基础设施 | [infra.md](./infra.md) | 代码生成、文件存储、配置管理、定时任务 |
| IoT设备 | [iot.md](./iot.md) | 产品管理、设备管理、物模型、规则引擎 |
| 框架能力 | [framework.md](./framework.md) | 数据权限、多租户、操作日志、通用工具 |

## 快速开始

1. **新增业务模块**：参考 `yudao-module-*` 的结构创建新模块
2. **代码生成**：使用 infra 模块的代码生成器快速生成 CRUD
3. **权限配置**：在 system 模块配置菜单和权限
4. **审批流程**：使用 bpm 模块设计和部署工作流

## 官方资源

- [官方文档](https://doc.iocoder.cn/)
- [GitHub仓库](https://github.com/YunaiV/ruoyi-vue-pro)
- [Gitee仓库](https://gitee.com/zhijiantianya/ruoyi-vue-pro)

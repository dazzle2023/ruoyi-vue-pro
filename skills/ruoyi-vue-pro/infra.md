# Infra 基础设施模块能力文档

> yudao-module-infra 提供代码生成、文件存储、配置管理、定时任务等基础设施能力。

## 一、核心功能

### 1.1 代码生成（Codegen）

**功能概述**：
- 基于数据库表自动生成 CRUD 代码
- 支持生成 Controller、Service、Mapper、VO、前端页面
- 支持自定义模板

**关键API**：
```
GET    /infra/codegen/db/table/list   获取数据库表列表
POST   /infra/codegen/create-list     创建代码生成配置
PUT    /infra/codegen/update          更新代码生成配置
DELETE /infra/codegen/delete          删除配置
PUT    /infra/codegen/sync-from-db    从数据库同步字段
GET    /infra/codegen/preview         预览生成代码
GET    /infra/codegen/download        下载生成代码
```

**核心实体**：
- `CodegenTableDO` (表名: `infra_codegen_table`) - 表配置
- `CodegenColumnDO` (表名: `infra_codegen_column`) - 字段配置

**代码生成流程**：
```
1. 选择数据库表
   ↓
2. 创建代码生成配置（自动解析字段）
   ↓
3. 配置表信息（模块名、业务名、类名等）
   ↓
4. 配置字段属性（显示类型、查询方式、必填等）
   ↓
5. 预览/下载生成代码
   ↓
6. 将代码复制到项目中
```

**生成文件清单**：
```
后端代码：
├── controller/
│   └── XxxController.java
├── service/
│   ├── XxxService.java
│   └── XxxServiceImpl.java
├── dal/
│   ├── dataobject/XxxDO.java
│   └── mysql/XxxMapper.java
└── vo/
    ├── XxxSaveReqVO.java
    ├── XxxRespVO.java
    └── XxxPageReqVO.java

前端代码：
├── api/xxx.ts
├── views/xxx/
│   └── index.vue
└── form/XxxForm.vue
```

**配置要点**：
```yaml
yudao:
  codegen:
    base-package: cn.iocoder.yudao.module
    front-type: 20  # 前端类型：10=Vue2 20=Vue3
    vo-type: 10     # VO类型：10=普通 20=树形
```

### 1.2 文件存储（File）

**功能概述**：
- 文件上传、下载、删除
- 支持多种存储方式（本地、OSS、S3等）
- 支持前端直传（预签名URL）

**关键API**：
```
POST /infra/file/upload           上传文件（后端上传）
GET  /infra/file/presigned-url    获取预签名URL（前端直传）
POST /infra/file/create           创建文件记录
GET  /infra/file/{configId}/get/** 下载文件
DELETE /infra/file/delete         删除文件
GET  /infra/file/page             文件分页
```

**核心实体**：
- `FileDO` (表名: `infra_file`) - 文件记录
- `FileConfigDO` (表名: `infra_file_config`) - 存储配置

**支持的存储类型**：
| 类型 | 说明 | 配置类 |
|------|------|--------|
| 本地存储 | 存储在服务器本地 | `LocalFileClientConfig` |
| FTP | FTP服务器 | `FtpFileClientConfig` |
| SFTP | SFTP服务器 | `SftpFileClientConfig` |
| 数据库 | 存储在数据库 | `DBFileClientConfig` |
| S3 | AWS S3 及兼容存储 | `S3FileClientConfig` |

**使用示例**：
```java
@Resource
private FileApi fileApi;

// 上传文件
public String uploadFile(MultipartFile file) {
    return fileApi.createFile(file.getOriginalFilename(),
                              null,
                              file.getBytes());
}

// 获取预签名URL（前端直传）
public FilePresignedUrlRespDTO getPresignedUrl(String fileName) {
    return fileApi.getPresignedUrl(fileName);
}
```

**前端直传流程**：
```
1. 前端请求预签名URL
   ↓
2. 后端返回上传URL和访问URL
   ↓
3. 前端直接上传到存储服务
   ↓
4. 前端调用创建文件记录接口
```

### 1.3 配置管理（Config）

**功能概述**：
- 系统配置参数管理
- 支持动态修改配置
- 配置缓存

**关键API**：
```
POST   /infra/config/create   创建配置
PUT    /infra/config/update   更新配置
DELETE /infra/config/delete   删除配置
GET    /infra/config/page     配置分页
GET    /infra/config/get      获取配置
GET    /infra/config/get-value-by-key 根据Key获取值
```

**核心实体**：`ConfigDO` (表名: `infra_config`)

**使用示例**：
```java
@Resource
private ConfigService configService;

// 获取配置值
String value = configService.getConfigValueByKey("sys.user.initPassword");
```

### 1.4 定时任务（Job）

**功能概述**：
- 定时任务管理
- 任务执行日志
- 支持 Cron 表达式

**关键API**：
```
POST   /infra/job/create      创建任务
PUT    /infra/job/update      更新任务
DELETE /infra/job/delete      删除任务
GET    /infra/job/page        任务分页
PUT    /infra/job/update-status 更新状态
PUT    /infra/job/trigger     立即执行
GET    /infra/job-log/page    任务日志分页
```

**核心实体**：
- `JobDO` (表名: `infra_job`) - 定时任务
- `JobLogDO` (表名: `infra_job_log`) - 任务日志

**创建定时任务步骤**：

1. **编写任务处理器**：
```java
@Component("demoJob")
public class DemoJob implements JobHandler {

    @Override
    public String execute(String param) throws Exception {
        // 任务逻辑
        log.info("执行定时任务，参数：{}", param);
        return "执行成功";
    }
}
```

2. **在管理后台配置任务**：
- 处理器名称：`demoJob`
- Cron 表达式：`0 0 * * * ?`（每小时执行）
- 参数：自定义参数

**Cron 表达式示例**：
| 表达式 | 说明 |
|--------|------|
| `0 0 * * * ?` | 每小时执行 |
| `0 0 0 * * ?` | 每天0点执行 |
| `0 0 0 1 * ?` | 每月1号0点执行 |
| `0 */5 * * * ?` | 每5分钟执行 |

### 1.5 API日志（Logger）

**功能概述**：
- API访问日志记录
- API错误日志记录
- 支持日志查询和导出

**核心实体**：
- `ApiAccessLogDO` (表名: `infra_api_access_log`) - 访问日志
- `ApiErrorLogDO` (表名: `infra_api_error_log`) - 错误日志

**日志记录内容**：
- 请求URL、方法、参数
- 响应结果、耗时
- 用户信息、IP地址
- 异常信息（错误日志）

**配置要点**：
```yaml
yudao:
  access-log:
    enable: true  # 是否开启访问日志
  error-log:
    enable: true  # 是否开启错误日志
```

### 1.6 数据源管理（DataSource）

**功能概述**：
- 多数据源配置管理
- 动态数据源切换
- 用于代码生成连接不同数据库

**核心实体**：`DataSourceConfigDO` (表名: `infra_data_source_config`)

**支持的数据库**：
- MySQL
- PostgreSQL
- Oracle
- SQL Server

---

## 二、代码生成详解

### 2.1 表配置说明

| 配置项 | 说明 | 示例 |
|--------|------|------|
| 表名 | 数据库表名 | `patrol_task` |
| 表描述 | 表的中文描述 | `巡查任务` |
| 模块名 | 模块包名 | `patrol` |
| 业务名 | 业务包名 | `task` |
| 类名 | 实体类名 | `PatrolTask` |
| 类描述 | 类的中文描述 | `巡查任务` |
| 作者 | 代码作者 | `admin` |

### 2.2 字段配置说明

| 配置项 | 说明 | 选项 |
|--------|------|------|
| 字段名 | 数据库字段名 | - |
| 字段描述 | 字段中文描述 | - |
| Java类型 | Java数据类型 | String, Integer, Long, Date等 |
| 显示类型 | 前端组件类型 | 输入框、下拉框、日期选择等 |
| 查询方式 | 查询条件类型 | =, LIKE, BETWEEN等 |
| 是否列表 | 是否在列表显示 | 是/否 |
| 是否查询 | 是否作为查询条件 | 是/否 |
| 是否必填 | 是否必填字段 | 是/否 |

### 2.3 显示类型对照

| 显示类型 | 前端组件 | 适用场景 |
|----------|----------|----------|
| 输入框 | `<el-input>` | 普通文本 |
| 文本域 | `<el-input type="textarea">` | 长文本 |
| 下拉框 | `<el-select>` | 枚举选择 |
| 单选框 | `<el-radio>` | 二选一 |
| 复选框 | `<el-checkbox>` | 多选 |
| 日期选择 | `<el-date-picker>` | 日期 |
| 日期时间 | `<el-date-picker type="datetime">` | 日期时间 |
| 图片上传 | `<ImageUpload>` | 图片 |
| 文件上传 | `<FileUpload>` | 文件 |
| 富文本 | `<Editor>` | 富文本内容 |

---

## 三、配置要点

### 3.1 代码生成配置

```yaml
yudao:
  codegen:
    base-package: cn.iocoder.yudao.module
    front-type: 20  # 10=Vue2 Element UI, 20=Vue3 Element Plus
    vo-type: 10     # 10=普通, 20=树形
    delete-batch-enable: true  # 是否生成批量删除
    unit-test-enable: false    # 是否生成单元测试
```

### 3.2 文件存储配置

```yaml
yudao:
  file:
    # 默认存储配置ID
    default-config-id: 1
```

**本地存储配置示例**：
```json
{
  "basePath": "/data/files",
  "domain": "http://localhost:8080"
}
```

**S3存储配置示例**：
```json
{
  "endpoint": "https://s3.amazonaws.com",
  "bucket": "my-bucket",
  "accessKey": "xxx",
  "accessSecret": "xxx"
}
```

### 3.3 定时任务配置

```yaml
yudao:
  job:
    # 是否开启定时任务
    enable: true
```

---

## 四、最佳实践

### 4.1 代码生成最佳实践

1. **表设计规范**：
   - 表名使用小写下划线，带模块前缀（如`patrol_task`）
   - 必须包含`id`、`creator`、`create_time`、`updater`、`update_time`、`deleted`字段
   - 字段注释要清晰完整

2. **生成后调整**：
   - 检查生成的VO字段是否需要调整
   - 添加业务校验逻辑
   - 调整前端页面布局

3. **增量生成**：
   - 表结构变更后使用"同步"功能
   - 只重新生成变更的部分

### 4.2 文件存储最佳实践

1. **存储选择**：
   - 开发环境：本地存储
   - 生产环境：OSS/S3存储

2. **大文件处理**：
   - 使用前端直传，减轻服务器压力
   - 配置合理的文件大小限制

3. **安全考虑**：
   - 敏感文件使用私有读写
   - 配置文件类型白名单

### 4.3 定时任务最佳实践

1. **任务设计**：
   - 任务要支持幂等性
   - 添加执行日志便于排查
   - 设置合理的超时时间

2. **异常处理**：
   - 捕获异常并记录
   - 关键任务配置告警

3. **性能考虑**：
   - 避免任务执行时间过长
   - 大数据量任务分批处理

---

## 五、常见问题

### Q1: 代码生成后如何添加到项目？

**A**:
1. 下载生成的代码压缩包
2. 将后端代码复制到对应模块目录
3. 将前端代码复制到前端项目
4. 执行SQL脚本创建菜单
5. 重启后端服务

### Q2: 如何自定义代码生成模板？

**A**: 修改 `resources/codegen/` 目录下的模板文件，模板使用 Velocity 语法。

### Q3: 文件上传大小限制如何配置？

**A**:
```yaml
spring:
  servlet:
    multipart:
      max-file-size: 100MB
      max-request-size: 100MB
```

### Q4: 定时任务不执行怎么排查？

**A**:
1. 检查任务状态是否为"开启"
2. 检查Cron表达式是否正确
3. 查看任务日志是否有异常
4. 检查`yudao.job.enable`配置

---

## 六、参考资源

- [官方文档 - 代码生成](https://doc.iocoder.cn/codegen/)
- [官方文档 - 文件存储](https://doc.iocoder.cn/file/)
- [官方文档 - 定时任务](https://doc.iocoder.cn/job/)

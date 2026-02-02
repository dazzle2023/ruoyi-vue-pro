# System 模块能力文档

> yudao-module-system 提供了用户、角色、权限、组织架构等核心系统管理能力。

## 一、核心功能

### 1.1 用户管理（User）

**功能概述**：
- 用户CRUD、密码管理、状态管理
- 用户导入导出
- 用户与角色、部门、岗位的关联

**关键API**：
```
POST   /system/user/create          创建用户
PUT    /system/user/update          更新用户
DELETE /system/user/delete          删除用户
GET    /system/user/page            分页查询
PUT    /system/user/update-password 重置密码
PUT    /system/user/update-status   修改状态
POST   /system/user/import          导入用户
GET    /system/user/export-excel    导出用户
```

**核心实体**：`AdminUserDO` (表名: `system_users`)

**关键字段**：
- `username` - 用户名（唯一）
- `password` - 密码（加密存储）
- `nickname` - 昵称
- `deptId` - 部门ID
- `postIds` - 岗位ID列表
- `mobile` - 手机号
- `status` - 状态（0正常 1停用）

### 1.2 角色管理（Role）

**功能概述**：
- 角色CRUD、权限分配
- **数据权限配置**（核心能力）

**关键API**：
```
POST   /system/role/create     创建角色
PUT    /system/role/update     更新角色
DELETE /system/role/delete     删除角色
GET    /system/role/page       分页查询
GET    /system/role/simple-list 精简列表
```

**核心实体**：`RoleDO` (表名: `system_role`)

**数据权限范围**（`dataScope`字段）：
- `1` - 全部数据权限
- `2` - 指定部门数据权限（配合`dataScopeDeptIds`）
- `3` - 本部门数据权限
- `4` - 本部门及以下数据权限
- `5` - 仅本人数据权限

**使用示例**：
```java
// 创建角色并配置数据权限
RoleSaveReqVO reqVO = new RoleSaveReqVO();
reqVO.setName("区域管理员");
reqVO.setCode("area_admin");
reqVO.setDataScope(2); // 指定部门
reqVO.setDataScopeDeptIds(Arrays.asList(100L, 101L)); // 指定部门ID
```

### 1.3 菜单管理（Menu）

**功能概述**：
- 菜单树管理、权限标识
- 支持目录、菜单、按钮三种类型

**关键API**：
```
POST   /system/menu/create          创建菜单
PUT    /system/menu/update          更新菜单
DELETE /system/menu/delete          删除菜单
GET    /system/menu/list            菜单列表
GET    /system/menu/list-all-simple 精简菜单树
```

**核心实体**：`MenuDO` (表名: `system_menu`)

**菜单类型**：
- `1` - 目录
- `2` - 菜单
- `3` - 按钮

**权限标识示例**：
- `system:user:create` - 创建用户
- `system:user:update` - 更新用户
- `system:user:delete` - 删除用户
- `system:user:query` - 查询用户

### 1.4 部门管理（Dept）

**功能概述**：
- 部门树管理、组织架构
- 支持多级部门

**关键API**：
```
POST   /system/dept/create 创建部门
PUT    /system/dept/update 更新部门
DELETE /system/dept/delete 删除部门
GET    /system/dept/list   部门列表
```

**核心实体**：`DeptDO` (表名: `system_dept`)

**关键字段**：
- `parentId` - 父部门ID（0表示根部门）
- `name` - 部门名称
- `sort` - 排序
- `leaderUserId` - 负责人ID
- `status` - 状态

### 1.5 岗位管理（Post）

**功能概述**：
- 岗位CRUD
- 用户可关联多个岗位

**核心实体**：`PostDO` (表名: `system_post`)

### 1.6 字典管理（Dict）

**功能概述**：
- 字典类型、字典数据管理
- 用于枚举值的配置化管理

**核心实体**：
- `DictTypeDO` (表名: `system_dict_type`) - 字典类型
- `DictDataDO` (表名: `system_dict_data`) - 字典数据

**使用场景**：
- 性别、状态等枚举值
- 业务类型、等级等配置项

**使用示例**：
```java
// 获取字典数据
List<DictDataDO> dictDataList = dictDataService.getDictDataList("sys_common_status");
```

### 1.7 认证授权（Auth & OAuth2）

**功能概述**：
- 登录、登出、Token管理
- OAuth2授权（授权码模式、密码模式等）
- 社交登录（微信、QQ等）

**关键API**：
```
POST /system/auth/login           用户登录
POST /system/auth/logout          用户登出
POST /system/auth/refresh-token   刷新Token
GET  /system/auth/get-permission-info 获取权限信息
```

**核心实体**：
- `OAuth2AccessTokenDO` - 访问令牌
- `OAuth2RefreshTokenDO` - 刷新令牌
- `OAuth2ClientDO` - OAuth2客户端

**Token机制**：
- Access Token：有效期2小时
- Refresh Token：有效期30天
- 支持Token续期

### 1.8 租户管理（Tenant）

**功能概述**：
- 多租户管理、租户套餐
- 自动租户隔离

**核心实体**：
- `TenantDO` (表名: `system_tenant`) - 租户
- `TenantPackageDO` (表名: `system_tenant_package`) - 租户套餐

**使用要点**：
- 新增实体继承`TenantBaseDO`自动支持租户隔离
- 使用`@TenantIgnore`注解忽略租户过滤

### 1.9 通知管理

#### 短信（SMS）
**功能**：短信渠道、短信模板、短信发送、短信日志

**核心实体**：
- `SmsChannelDO` - 短信渠道（阿里云、腾讯云等）
- `SmsTemplateDO` - 短信模板
- `SmsLogDO` - 短信日志

#### 邮件（Mail）
**功能**：邮件账号、邮件模板、邮件发送、邮件日志

**核心实体**：
- `MailAccountDO` - 邮件账号
- `MailTemplateDO` - 邮件模板
- `MailLogDO` - 邮件日志

#### 站内信（Notify）
**功能**：站内信模板、站内信发送

**核心实体**：
- `NotifyTemplateDO` - 站内信模板
- `NotifyMessageDO` - 站内信消息

### 1.10 日志管理（Logger）

**功能概述**：
- 登录日志、操作日志

**核心实体**：
- `LoginLogDO` (表名: `system_login_log`) - 登录日志
- `OperateLogDO` (表名: `system_operate_log`) - 操作日志

**操作日志注解**：
```java
@OperateLog(type = EXPORT)
public void exportUserExcel() {
    // 导出逻辑
}
```

---

## 二、权限控制

### 2.1 菜单权限

**使用方式**：在Controller方法上使用`@PreAuthorize`注解

```java
@PreAuthorize("@ss.hasPermission('system:user:create')")
@PostMapping("/create")
public CommonResult<Long> createUser(@Valid @RequestBody UserSaveReqVO reqVO) {
    return success(userService.createUser(reqVO));
}
```

### 2.2 数据权限

**使用方式**：在Service方法上使用`@DataPermission`注解

```java
@DataPermission(enable = true)
public PageResult<UserDO> getUserPage(UserPageReqVO reqVO) {
    return userMapper.selectPage(reqVO);
}
```

**工作原理**：
- 通过AOP拦截SQL
- 根据角色的`dataScope`自动添加WHERE条件
- 支持自定义数据权限规则

---

## 三、配置要点

### 3.1 数据权限配置

```yaml
yudao:
  security:
    enable: true
  data-permission:
    enable: true
```

### 3.2 多租户配置

```yaml
yudao:
  tenant:
    enable: true
    ignore-urls: # 忽略租户的URL
      - /admin-api/system/tenant/get-id-by-name
    ignore-tables: # 忽略租户的表
      - system_tenant
      - system_tenant_package
```

### 3.3 Token配置

```yaml
yudao:
  security:
    token-header: Authorization
    token-secret: your-secret-key
    token-timeout: 7200 # 2小时
    refresh-token-timeout: 2592000 # 30天
```

---

## 四、最佳实践

### 4.1 新增业务模块权限

1. **创建菜单**：在菜单管理中创建目录、菜单、按钮
2. **配置权限标识**：按钮配置权限标识（如`patrol:task:create`）
3. **分配角色**：将菜单权限分配给角色
4. **代码使用**：在Controller中使用`@PreAuthorize`

### 4.2 数据权限设计

1. **确定数据范围**：明确哪些数据需要权限控制
2. **配置角色数据权限**：设置角色的`dataScope`
3. **实体关联部门**：确保实体有`deptId`字段
4. **Service启用数据权限**：使用`@DataPermission`注解

### 4.3 多租户设计

1. **实体继承**：新实体继承`TenantBaseDO`
2. **忽略配置**：系统级表配置`@TenantIgnore`
3. **测试验证**：确保租户数据隔离正确

---

## 五、常见问题

### Q1: 如何实现自定义数据权限？

**A**: 实现`DataPermissionRule`接口，注册为Spring Bean。

```java
@Component
public class CustomDataPermissionRule implements DataPermissionRule {
    @Override
    public void addWhere(String tableName, String tableAlias,
                         StringBuilder where, Object... args) {
        // 自定义权限逻辑
    }
}
```

### Q2: 如何禁用某个接口的租户隔离？

**A**: 使用`@TenantIgnore`注解。

```java
@TenantIgnore
@GetMapping("/list-all")
public CommonResult<List<UserDO>> getAllUsers() {
    return success(userService.getAllUsers());
}
```

### Q3: 如何实现部门树查询？

**A**: 使用`DeptService.buildDeptTree()`方法。

```java
List<DeptDO> deptList = deptService.getDeptList();
List<DeptRespVO> deptTree = DeptConvert.INSTANCE.convertList(deptList);
return success(deptTree);
```

---

## 六、参考资源

- [官方文档 - 权限管理](https://doc.iocoder.cn/system-permission/)
- [官方文档 - 数据权限](https://doc.iocoder.cn/data-permission/)
- [官方文档 - 多租户](https://doc.iocoder.cn/tenant/)

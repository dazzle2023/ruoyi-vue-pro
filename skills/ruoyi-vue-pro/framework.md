# Framework 框架层能力文档

> yudao-framework 提供数据权限、多租户、操作日志、缓存、消息队列等通用能力。

## 一、核心能力

### 1.1 数据权限（Data Permission）

**位置**：`yudao-spring-boot-starter-biz-data-permission`

**功能概述**：
- 基于部门的数据权限过滤
- 自动拦截SQL添加权限条件
- 支持自定义数据权限规则

**使用方式**：

1. **启用数据权限**：
```java
@DataPermission(enable = true)
public PageResult<UserDO> getUserPage(UserPageReqVO reqVO) {
    return userMapper.selectPage(reqVO);
}
```

2. **禁用数据权限**：
```java
@DataPermission(enable = false)
public List<UserDO> getAllUsers() {
    return userMapper.selectList();
}
```

**工作原理**：
```
1. AOP拦截带@DataPermission注解的方法
   ↓
2. 获取当前用户的角色和数据权限范围
   ↓
3. 根据数据权限范围生成SQL条件
   ↓
4. 通过MyBatis拦截器添加WHERE条件
```

**数据权限范围**：
| 范围 | 说明 | SQL条件示例 |
|------|------|-------------|
| 全部 | 无限制 | 无 |
| 本部门 | 只看本部门数据 | `dept_id = 100` |
| 本部门及子部门 | 看本部门和下级部门 | `dept_id IN (100, 101, 102)` |
| 仅本人 | 只看自己的数据 | `creator = 1` |
| 自定义 | 指定部门 | `dept_id IN (100, 200)` |

**配置要点**：
```yaml
yudao:
  data-permission:
    enable: true
```

### 1.2 多租户（Tenant）

**位置**：`yudao-spring-boot-starter-biz-tenant`

**功能概述**：
- 自动租户隔离
- 租户数据自动过滤
- 支持忽略租户配置

**使用方式**：

1. **实体继承TenantBaseDO**：
```java
@TableName("patrol_task")
public class PatrolTaskDO extends TenantBaseDO {
    private Long id;
    private String taskName;
    // ...
}
```

2. **忽略租户过滤**：
```java
@TenantIgnore
@GetMapping("/list-all")
public CommonResult<List<TenantDO>> getAllTenants() {
    return success(tenantService.getTenantList());
}
```

**配置要点**：
```yaml
yudao:
  tenant:
    enable: true
    ignore-urls:
      - /admin-api/system/tenant/get-id-by-name
    ignore-tables:
      - system_tenant
      - system_tenant_package
```

### 1.3 操作日志（Operate Log）

**位置**：`yudao-spring-boot-starter-biz-operatelog`

**功能概述**：
- 自动记录操作日志
- 支持自定义日志内容
- 支持日志查询

**使用方式**：

1. **自动记录**（Controller方法自动记录）：
```java
@PostMapping("/create")
@Operation(summary = "创建用户")
public CommonResult<Long> createUser(@Valid @RequestBody UserSaveReqVO reqVO) {
    return success(userService.createUser(reqVO));
}
```

2. **自定义日志内容**：
```java
@OperateLog(type = EXPORT, content = "导出用户数据")
@GetMapping("/export")
public void exportUsers(HttpServletResponse response) {
    // ...
}
```

**日志类型**：
- `CREATE` - 创建
- `UPDATE` - 更新
- `DELETE` - 删除
- `EXPORT` - 导出
- `IMPORT` - 导入
- `OTHER` - 其他

### 1.4 Redis缓存

**位置**：`yudao-spring-boot-starter-redis`

**功能概述**：
- Redis缓存管理
- 分布式锁
- 缓存过期时间配置

**使用方式**：

1. **缓存注解**：
```java
@Cacheable(value = "user", key = "#id")
public UserDO getUser(Long id) {
    return userMapper.selectById(id);
}

@CacheEvict(value = "user", key = "#reqVO.id")
public void updateUser(UserSaveReqVO reqVO) {
    userMapper.updateById(convert(reqVO));
}
```

2. **RedisTemplate使用**：
```java
@Resource
private StringRedisTemplate stringRedisTemplate;

public void setCache(String key, String value, long timeout) {
    stringRedisTemplate.opsForValue().set(key, value, timeout, TimeUnit.SECONDS);
}

public String getCache(String key) {
    return stringRedisTemplate.opsForValue().get(key);
}
```

3. **分布式锁**：
```java
@Resource
private RedissonClient redissonClient;

public void doWithLock(String lockKey) {
    RLock lock = redissonClient.getLock(lockKey);
    try {
        lock.lock(10, TimeUnit.SECONDS);
        // 业务逻辑
    } finally {
        lock.unlock();
    }
}
```

### 1.5 MyBatis增强

**位置**：`yudao-spring-boot-starter-mybatis`

**功能概述**：
- MyBatis Plus集成
- 逻辑删除
- 自动填充
- 分页插件

**自动填充字段**：
- `creator` - 创建人
- `createTime` - 创建时间
- `updater` - 更新人
- `updateTime` - 更新时间

**基础实体类**：
```java
// 基础实体（不含租户）
public class BaseDO {
    private Long creator;
    private LocalDateTime createTime;
    private Long updater;
    private LocalDateTime updateTime;
    private Boolean deleted;
}

// 租户实体
public class TenantBaseDO extends BaseDO {
    private Long tenantId;
}
```

**分页查询**：
```java
public PageResult<UserDO> getUserPage(UserPageReqVO reqVO) {
    return userMapper.selectPage(reqVO, new LambdaQueryWrapperX<UserDO>()
        .likeIfPresent(UserDO::getUsername, reqVO.getUsername())
        .eqIfPresent(UserDO::getStatus, reqVO.getStatus())
        .betweenIfPresent(UserDO::getCreateTime, reqVO.getCreateTime())
        .orderByDesc(UserDO::getId));
}
```

### 1.6 安全框架（Security）

**位置**：`yudao-spring-boot-starter-security`

**功能概述**：
- Spring Security集成
- JWT Token认证
- 权限校验

**权限校验**：
```java
// 单个权限
@PreAuthorize("@ss.hasPermission('system:user:create')")

// 任一权限
@PreAuthorize("@ss.hasAnyPermissions('system:user:create', 'system:user:update')")

// 角色校验
@PreAuthorize("@ss.hasRole('admin')")

// 任一角色
@PreAuthorize("@ss.hasAnyRoles('admin', 'manager')")
```

**获取当前用户**：
```java
// 获取当前用户ID
Long userId = SecurityFrameworkUtils.getLoginUserId();

// 获取当前用户信息
LoginUser loginUser = SecurityFrameworkUtils.getLoginUser();
```

### 1.7 消息队列（MQ）

**位置**：`yudao-spring-boot-starter-mq`

**功能概述**：
- 支持Redis、RocketMQ、Kafka、RabbitMQ
- 统一消息发送接口

**使用方式**：

1. **定义消息**：
```java
@Data
public class UserCreateMessage {
    private Long userId;
    private String username;
}
```

2. **发送消息**：
```java
@Resource
private RedisMQTemplate redisMQTemplate;

public void sendUserCreateMessage(Long userId, String username) {
    UserCreateMessage message = new UserCreateMessage();
    message.setUserId(userId);
    message.setUsername(username);
    redisMQTemplate.send(message);
}
```

3. **消费消息**：
```java
@Component
public class UserCreateMessageConsumer extends AbstractRedisMessageListener<UserCreateMessage> {

    @Override
    public void onMessage(UserCreateMessage message) {
        // 处理消息
        log.info("收到用户创建消息：{}", message);
    }
}
```

### 1.8 Excel导入导出

**位置**：`yudao-spring-boot-starter-excel`

**功能概述**：
- 基于EasyExcel
- 支持导入导出
- 支持模板下载

**使用方式**：

1. **定义导出VO**：
```java
@Data
public class UserExcelVO {
    @ExcelProperty("用户名")
    private String username;

    @ExcelProperty("昵称")
    private String nickname;

    @ExcelProperty(value = "状态", converter = DictConvert.class)
    @DictFormat("sys_common_status")
    private Integer status;
}
```

2. **导出Excel**：
```java
@GetMapping("/export")
public void exportUsers(HttpServletResponse response) {
    List<UserDO> users = userService.getUserList();
    List<UserExcelVO> excelVOs = UserConvert.INSTANCE.convertList(users);
    ExcelUtils.write(response, "用户列表.xlsx", "用户", UserExcelVO.class, excelVOs);
}
```

3. **导入Excel**：
```java
@PostMapping("/import")
public CommonResult<Boolean> importUsers(@RequestParam("file") MultipartFile file) {
    List<UserExcelVO> list = ExcelUtils.read(file, UserExcelVO.class);
    userService.importUsers(list);
    return success(true);
}
```

### 1.9 WebSocket

**位置**：`yudao-spring-boot-starter-websocket`

**功能概述**：
- WebSocket支持
- 消息推送

**使用方式**：

1. **发送消息**：
```java
@Resource
private WebSocketMessageSender webSocketMessageSender;

public void sendMessage(Long userId, String message) {
    webSocketMessageSender.send(userId, "notify", message);
}
```

2. **广播消息**：
```java
public void broadcast(String message) {
    webSocketMessageSender.send("notify", message);
}
```

### 1.10 防护（Protection）

**位置**：`yudao-spring-boot-starter-protection`

**功能概述**：
- 限流
- 幂等性
- 分布式锁

**限流使用**：
```java
@RateLimiter(count = 10, time = 60) // 60秒内最多10次
@PostMapping("/send-sms")
public CommonResult<Boolean> sendSms(@RequestBody SmsSendReqVO reqVO) {
    // ...
}
```

**幂等性使用**：
```java
@Idempotent(timeout = 10, timeUnit = TimeUnit.SECONDS)
@PostMapping("/create")
public CommonResult<Long> createOrder(@RequestBody OrderCreateReqVO reqVO) {
    // ...
}
```

---

## 二、通用工具类

**位置**：`yudao-common/src/main/java/cn/iocoder/yudao/framework/common/util/`

### 2.1 BeanUtils

```java
// 对象转换
UserRespVO respVO = BeanUtils.toBean(userDO, UserRespVO.class);

// 列表转换
List<UserRespVO> respVOs = BeanUtils.toBean(userDOs, UserRespVO.class);
```

### 2.2 CollectionUtils

```java
// 提取ID列表
List<Long> ids = CollectionUtils.convertList(users, UserDO::getId);

// 转换为Map
Map<Long, UserDO> userMap = CollectionUtils.convertMap(users, UserDO::getId);

// 过滤
List<UserDO> activeUsers = CollectionUtils.filterList(users, u -> u.getStatus() == 1);
```

### 2.3 DateUtils

```java
// 格式化日期
String dateStr = DateUtils.format(date, "yyyy-MM-dd HH:mm:ss");

// 解析日期
LocalDateTime dateTime = DateUtils.parse(dateStr, "yyyy-MM-dd HH:mm:ss");

// 获取当天开始时间
LocalDateTime startOfDay = DateUtils.getStartOfDay(LocalDateTime.now());
```

### 2.4 JsonUtils

```java
// 对象转JSON
String json = JsonUtils.toJsonString(user);

// JSON转对象
UserDO user = JsonUtils.parseObject(json, UserDO.class);

// JSON转列表
List<UserDO> users = JsonUtils.parseArray(json, UserDO.class);
```

---

## 三、通用POJO

### 3.1 CommonResult

```java
// 成功响应
return CommonResult.success(data);

// 失败响应
return CommonResult.error(ErrorCodeConstants.USER_NOT_EXISTS);

// 自定义错误
return CommonResult.error(500, "操作失败");
```

### 3.2 PageResult

```java
// 分页结果
PageResult<UserDO> pageResult = new PageResult<>();
pageResult.setList(users);
pageResult.setTotal(total);
return pageResult;
```

### 3.3 PageParam

```java
// 分页参数
public class UserPageReqVO extends PageParam {
    private String username;
    private Integer status;
}
```

---

## 四、异常处理

### 4.1 ServiceException

```java
// 抛出业务异常
throw new ServiceException(ErrorCodeConstants.USER_NOT_EXISTS);

// 带参数的异常
throw new ServiceException(ErrorCodeConstants.USER_USERNAME_EXISTS.getCode(),
    String.format("用户名 %s 已存在", username));
```

### 4.2 错误码定义

```java
public interface ErrorCodeConstants {
    // 用户模块错误码
    ErrorCode USER_NOT_EXISTS = new ErrorCode(1_001_000_001, "用户不存在");
    ErrorCode USER_USERNAME_EXISTS = new ErrorCode(1_001_000_002, "用户名已存在");
    ErrorCode USER_PASSWORD_ERROR = new ErrorCode(1_001_000_003, "密码错误");
}
```

---

## 五、配置总览

```yaml
yudao:
  # 数据权限
  data-permission:
    enable: true

  # 多租户
  tenant:
    enable: true
    ignore-urls: []
    ignore-tables: []

  # 安全配置
  security:
    token-header: Authorization
    token-secret: your-secret-key
    token-timeout: 7200
    permit-all-urls: []

  # 访问日志
  access-log:
    enable: true

  # 错误日志
  error-log:
    enable: true

  # WebSocket
  websocket:
    enable: true
    path: /infra/ws
```

---

## 六、最佳实践

### 6.1 数据权限设计

1. **实体设计**：需要数据权限的实体要有`deptId`字段
2. **Mapper设计**：查询方法要支持数据权限过滤
3. **Service设计**：在需要的方法上添加`@DataPermission`注解

### 6.2 多租户设计

1. **实体继承**：业务实体继承`TenantBaseDO`
2. **忽略配置**：系统级表配置忽略租户
3. **跨租户操作**：使用`@TenantIgnore`注解

### 6.3 缓存设计

1. **缓存粒度**：根据业务场景选择合适的缓存粒度
2. **缓存更新**：数据变更时及时清除缓存
3. **缓存穿透**：使用空值缓存防止穿透

### 6.4 异常处理

1. **业务异常**：使用`ServiceException`抛出业务异常
2. **错误码规范**：按模块定义错误码，避免冲突
3. **异常日志**：关键异常要记录日志

---

## 七、参考资源

- [官方文档 - 数据权限](https://doc.iocoder.cn/data-permission/)
- [官方文档 - 多租户](https://doc.iocoder.cn/tenant/)
- [官方文档 - 操作日志](https://doc.iocoder.cn/operate-log/)

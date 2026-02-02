# BPM 工作流模块能力文档

> yudao-module-bpm 基于 Flowable 引擎提供完整的工作流能力，支持流程设计、部署、执行和监控。

## 一、核心功能

### 1.1 流程模型（Model）

**功能概述**：
- 流程模型设计（BPMN 2.0）
- 流程部署和版本管理
- 流程分类管理

**关键API**：
```
GET    /bpm/model/page              流程模型分页
GET    /bpm/model/get               获取模型详情
POST   /bpm/model/create            创建模型
PUT    /bpm/model/update            更新模型
DELETE /bpm/model/delete            删除模型
POST   /bpm/model/deploy            部署流程
PUT    /bpm/model/update-state      更新状态
GET    /bpm/model/get-bpmn-xml      获取BPMN XML
```

**流程设计器**：
- 前端集成 bpmn.js 设计器
- 支持可视化拖拽设计
- 支持导入/导出 BPMN XML

### 1.2 流程实例（Process Instance）

**功能概述**：
- 发起流程、取消流程
- 流程进度查询、流程详情
- 审批记录查看

**关键API**：
```
POST   /bpm/process-instance/create                创建流程实例
GET    /bpm/process-instance/my-page               我的流程分页
GET    /bpm/process-instance/manager-page          管理流程分页
GET    /bpm/process-instance/get                   获取流程详情
DELETE /bpm/process-instance/cancel-by-start-user  用户取消流程
DELETE /bpm/process-instance/cancel-by-admin       管理员取消流程
GET    /bpm/process-instance/get-approval-detail   获取审批详情
GET    /bpm/process-instance/get-bpmn-model-view   获取BPMN视图
```

**发起流程示例**：
```java
// 创建流程实例
BpmProcessInstanceCreateReqVO reqVO = new BpmProcessInstanceCreateReqVO();
reqVO.setProcessDefinitionId("leave:1:xxx"); // 流程定义ID
reqVO.setVariables(new HashMap<String, Object>() {{
    put("days", 3);
    put("reason", "年假");
}}); // 流程变量

String processInstanceId = processInstanceService.createProcessInstance(userId, reqVO);
```

### 1.3 任务管理（Task）

**功能概述**：
- 待办任务、已办任务查询
- 任务审批（通过/拒绝）
- 任务退回、委派、转派
- 加签、减签

**关键API**：
```
GET    /bpm/task/todo-page      待办任务分页
GET    /bpm/task/done-page      已办任务分页
GET    /bpm/task/manager-page   全部任务分页
PUT    /bpm/task/approve        通过任务
PUT    /bpm/task/reject         拒绝任务
PUT    /bpm/task/return         退回任务
PUT    /bpm/task/delegate       委派任务
PUT    /bpm/task/transfer       转派任务
PUT    /bpm/task/create-sign    加签
DELETE /bpm/task/delete-sign    减签
PUT    /bpm/task/withdraw       撤回任务
```

**任务审批示例**：
```java
// 通过任务
BpmTaskApproveReqVO approveReqVO = new BpmTaskApproveReqVO();
approveReqVO.setId(taskId);
approveReqVO.setReason("同意申请");
taskService.approveTask(userId, approveReqVO);

// 拒绝任务
BpmTaskRejectReqVO rejectReqVO = new BpmTaskRejectReqVO();
rejectReqVO.setId(taskId);
rejectReqVO.setReason("资料不完整");
taskService.rejectTask(userId, rejectReqVO);

// 退回任务
BpmTaskReturnReqVO returnReqVO = new BpmTaskReturnReqVO();
returnReqVO.setId(taskId);
returnReqVO.setTargetTaskDefinitionKey("userTask1"); // 退回到的节点
returnReqVO.setReason("需要补充材料");
taskService.returnTask(userId, returnReqVO);
```

### 1.4 表单管理（Form）

**功能概述**：
- 动态表单设计
- 表单与流程节点绑定
- 表单数据存储

**关键API**：
```
POST   /bpm/form/create   创建表单
PUT    /bpm/form/update   更新表单
DELETE /bpm/form/delete   删除表单
GET    /bpm/form/page     表单分页
GET    /bpm/form/get      获取表单详情
GET    /bpm/form/simple-list 表单精简列表
```

**核心实体**：`BpmFormDO` (表名: `bpm_form`)

**表单配置**：
- 支持 JSON Schema 定义表单结构
- 支持表单字段校验规则
- 支持表单与流程变量映射

### 1.5 用户组（User Group）

**功能概述**：
- 用户组管理
- 用于流程节点的候选人配置

**关键API**：
```
POST   /bpm/user-group/create   创建用户组
PUT    /bpm/user-group/update   更新用户组
DELETE /bpm/user-group/delete   删除用户组
GET    /bpm/user-group/page     用户组分页
GET    /bpm/user-group/simple-list 用户组精简列表
```

**核心实体**：`BpmUserGroupDO` (表名: `bpm_user_group`)

### 1.6 流程分类（Category）

**功能概述**：
- 流程分类管理
- 用于流程的分类展示

**核心实体**：`BpmCategoryDO` (表名: `bpm_category`)

### 1.7 流程监听器（Listener）

**功能概述**：
- 流程监听器配置
- 支持执行监听器和任务监听器

**核心实体**：`BpmProcessListenerDO` (表名: `bpm_process_listener`)

**监听器类型**：
- `execution` - 执行监听器（流程启动、结束等）
- `task` - 任务监听器（任务创建、完成等）

### 1.8 流程表达式（Expression）

**功能概述**：
- 流程表达式管理
- 用于条件网关、任务分配等

**核心实体**：`BpmProcessExpressionDO` (表名: `bpm_process_expression`)

---

## 二、流程设计

### 2.1 BPMN 2.0 元素支持

| 元素类型 | 支持情况 | 说明 |
|----------|----------|------|
| 开始事件 | ✅ | 支持普通开始、定时开始 |
| 结束事件 | ✅ | 支持普通结束、终止结束 |
| 用户任务 | ✅ | 支持多种分配方式 |
| 服务任务 | ✅ | 支持HTTP调用、表达式 |
| 排他网关 | ✅ | 条件分支 |
| 并行网关 | ✅ | 并行执行 |
| 包容网关 | ✅ | 条件并行 |
| 子流程 | ✅ | 嵌入式子流程 |
| 调用活动 | ✅ | 调用其他流程 |

### 2.2 任务分配方式

**支持的分配方式**：

1. **指定用户**：直接指定处理人ID
2. **指定角色**：角色下所有用户作为候选人
3. **指定部门**：部门下所有用户作为候选人
4. **指定用户组**：用户组成员作为候选人
5. **发起人自选**：发起时选择处理人
6. **发起人本人**：发起人自己处理
7. **发起人部门负责人**：发起人所在部门的负责人
8. **表达式**：通过表达式动态计算

**配置示例**（BPMN XML）：
```xml
<!-- 指定用户 -->
<userTask id="task1" flowable:assignee="1"/>

<!-- 指定角色（候选组） -->
<userTask id="task2" flowable:candidateGroups="role:1"/>

<!-- 指定部门 -->
<userTask id="task3" flowable:candidateGroups="dept:100"/>

<!-- 表达式 -->
<userTask id="task4" flowable:assignee="${assignee}"/>
```

### 2.3 条件表达式

**网关条件示例**：
```xml
<sequenceFlow id="flow1" sourceRef="gateway1" targetRef="task1">
    <conditionExpression xsi:type="tFormalExpression">
        ${days <= 3}
    </conditionExpression>
</sequenceFlow>

<sequenceFlow id="flow2" sourceRef="gateway1" targetRef="task2">
    <conditionExpression xsi:type="tFormalExpression">
        ${days > 3}
    </conditionExpression>
</sequenceFlow>
```

---

## 三、流程集成

### 3.1 业务流程集成步骤

1. **设计流程**：使用流程设计器创建BPMN流程
2. **部署流程**：将流程部署到引擎
3. **发起流程**：业务代码调用API发起流程
4. **处理任务**：用户在待办中处理任务
5. **流程结束**：流程完成或终止

### 3.2 业务代码集成示例

```java
@Service
public class LeaveService {

    @Resource
    private BpmProcessInstanceService processInstanceService;

    /**
     * 提交请假申请
     */
    public String submitLeave(LeaveCreateReqVO reqVO) {
        // 1. 保存业务数据
        LeaveDO leave = LeaveConvert.INSTANCE.convert(reqVO);
        leaveMapper.insert(leave);

        // 2. 发起流程
        Map<String, Object> variables = new HashMap<>();
        variables.put("days", reqVO.getDays());
        variables.put("leaveId", leave.getId());

        BpmProcessInstanceCreateReqVO createReqVO = new BpmProcessInstanceCreateReqVO();
        createReqVO.setProcessDefinitionKey("leave"); // 流程定义Key
        createReqVO.setVariables(variables);
        createReqVO.setBusinessKey(String.valueOf(leave.getId())); // 业务主键

        String processInstanceId = processInstanceService.createProcessInstance(
            SecurityFrameworkUtils.getLoginUserId(), createReqVO);

        // 3. 更新业务数据的流程实例ID
        leaveMapper.updateById(new LeaveDO()
            .setId(leave.getId())
            .setProcessInstanceId(processInstanceId));

        return processInstanceId;
    }
}
```

### 3.3 流程监听器集成

```java
@Component
public class LeaveProcessListener implements ExecutionListener {

    @Resource
    private LeaveService leaveService;

    @Override
    public void notify(DelegateExecution execution) {
        String eventName = execution.getEventName();
        String businessKey = execution.getProcessInstanceBusinessKey();

        if ("end".equals(eventName)) {
            // 流程结束时更新业务状态
            Long leaveId = Long.parseLong(businessKey);
            leaveService.updateLeaveStatus(leaveId, LeaveStatusEnum.APPROVED);
        }
    }
}
```

---

## 四、配置要点

### 4.1 Flowable 配置

```yaml
flowable:
  # 数据库表自动更新
  database-schema-update: true
  # 启用历史记录
  db-history-used: true
  # 历史级别：none, activity, audit, full
  history-level: audit
  # 不自动部署流程
  check-process-definitions: false
  # 异步执行器
  async-executor-activate: true
```

### 4.2 BPM 模块配置

```yaml
yudao:
  bpm:
    # 流程定义缓存时间（秒）
    process-definition-cache-limit: 100
```

---

## 五、最佳实践

### 5.1 流程设计原则

1. **流程粒度**：一个流程对应一个业务场景，避免过于复杂
2. **节点命名**：使用清晰的中文名称，便于理解
3. **条件设计**：条件表达式要覆盖所有情况，避免死锁
4. **异常处理**：设计异常分支和超时处理

### 5.2 任务分配建议

1. **避免单点**：尽量使用角色/部门分配，避免指定单个用户
2. **候选人机制**：使用候选人而非直接分配，提高灵活性
3. **动态分配**：复杂场景使用表达式动态计算处理人

### 5.3 流程变量使用

1. **命名规范**：使用驼峰命名，如`leaveId`、`approveResult`
2. **类型选择**：优先使用基本类型，避免复杂对象
3. **变量范围**：区分流程变量和局部变量

### 5.4 性能优化

1. **历史级别**：生产环境使用`audit`级别，避免`full`
2. **异步执行**：耗时操作使用异步任务
3. **定期清理**：定期清理历史数据

---

## 六、常见问题

### Q1: 如何实现会签（多人审批）？

**A**: 使用多实例任务配置。

```xml
<userTask id="multiTask" name="会签审批">
    <multiInstanceLoopCharacteristics isSequential="false">
        <loopCardinality>${assigneeList.size()}</loopCardinality>
        <completionCondition>${nrOfCompletedInstances/nrOfInstances >= 0.5}</completionCondition>
    </multiInstanceLoopCharacteristics>
</userTask>
```

### Q2: 如何实现流程超时自动处理？

**A**: 使用边界定时事件。

```xml
<userTask id="task1" name="审批任务">
    <boundaryEvent id="timeout" attachedToRef="task1">
        <timerEventDefinition>
            <timeDuration>PT24H</timeDuration> <!-- 24小时超时 -->
        </timerEventDefinition>
    </boundaryEvent>
</userTask>
```

### Q3: 如何获取流程审批记录？

**A**: 使用审批详情API。

```java
// 获取审批详情
BpmApprovalDetailRespVO detail = processInstanceService.getApprovalDetail(
    userId, processInstanceId);

// 审批记录列表
List<BpmApprovalNodeInfo> nodes = detail.getApprovalNodes();
```

### Q4: 如何实现流程抄送？

**A**: 在流程中添加抄送节点或使用监听器发送通知。

```java
@Component
public class CopyTaskListener implements TaskListener {
    @Override
    public void notify(DelegateTask delegateTask) {
        // 发送抄送通知
        notifyService.sendCopyNotify(delegateTask);
    }
}
```

---

## 七、参考资源

- [官方文档 - 工作流](https://doc.iocoder.cn/bpm/)
- [Flowable 官方文档](https://www.flowable.com/open-source/docs/)
- [BPMN 2.0 规范](https://www.omg.org/spec/BPMN/2.0/)

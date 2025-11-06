# 任务提交流程后端Debug指南

## 📍 任务提交接口

### 接口信息

**主要接口**：
- **HTTP POST**: `/api/nae-deep-research/v1/deep-research/search`
- **完整URL**: `http://localhost:7788/api/nae-deep-research/v1/deep-research/search`

**WebSocket入口**（前端通过WebSocket提交）：
- **WebSocket**: `/api/openans-support-chatbot/v1/robot/wss/messages`
- 然后内部调用上述HTTP接口

---

## 🔄 完整流程概览

```
前端提交任务
    ↓
方式1: WebSocket → websocket_manager.py → search接口
方式2: 直接HTTP POST → search接口
    ↓
search.py: search() 函数（第325行）
    ↓
创建workspace、plan_id
    ↓
generator_func() 异步生成器（第360行）
    ↓
run_manus() 线程函数（第507行）
    ↓
CoSight.execute() 执行任务（第531行）
    ↓
TaskPlannerAgent 创建计划
    ↓
TaskActorAgent 执行步骤
    ↓
流式返回结果给前端
```

---

## 🔴 关键断点位置（按执行顺序）

### 断点1：WebSocket消息接收（如果是通过WebSocket）

**文件**: `cosight_server/deep_research/routers/websocket_manager.py`

**位置**: 第110行
```python
while True:
    data = await websocket.receive_json()  # ← 在这里打断点，查看前端发送的消息
    logger.info(f"receive >>>>>>>>>>>>>> {data}")
```

**调试信息**：
- `data` - 完整的WebSocket消息
- `data.get("action")` - 应该是 "message"
- `data.get("data")` - 包含任务内容的JSON字符串

---

### 断点2：WebSocket消息处理

**文件**: `cosight_server/deep_research/routers/websocket_manager.py`

**位置**: 第118-139行
```python
if data.get("action") == "message":
    message = json.loads(data.get("data"))  # ← 在这里打断点，查看解析后的消息
    logger.info(f"message >>>>>>>>>>>>>> {message}")
    
    # 绑定当前 topic 到该 websocket
    manager.bind_topic(data.get("topic"), websocket)
    
    # 推送时间更新的消息给前端
    await manager.send_json_to_topic(...)  # ← 在这里打断点
    
    await _send_resp(websocket, cookie, data.get("topic"), message, lang)  # ← 在这里打断点，准备调用search接口
```

**关键变量**：
- `message` - 解析后的任务消息
- `message.get("initData")` - 任务内容（用户输入）
- `data.get("topic")` - 会话主题ID

---

### 断点3：准备HTTP请求参数（WebSocket方式）

**文件**: `cosight_server/deep_research/routers/websocket_manager.py`

**位置**: 第150-192行
```python
async def _send_resp(websocket, cookie, topic, message, lang):  # ← 在这里打断点
    cookie_str = "; ".join([f"{key}={value}" for key, value in cookie.items()])
    assistants = [mention['name'] for mention in message['mentions']]
    params = {
        "content": message.get("initData"),  # ← 在这里打断点，查看任务内容
        "history": [],
        "sessionInfo": {
            "locale": lang,
            "sessionId": topic,
            "username": message.get("roleInfo").get("name"),
            "assistantNames": assistants
        },
        "stream": True,
        "contentProperties": message.get("extra", {}).get("fromBackEnd", {}).get("actualPrompt")
    }
    # ... 处理replay参数 ...
    
    url = f'http://127.0.0.1:{custom_config.get("search_port")}{custom_config.get("base_api_url")}/deep-research/search'  # ← 在这里打断点，查看完整URL
```

**关键变量**：
- `params` - 传递给search接口的参数
- `params["content"]` - 用户输入的任务内容
- `url` - 完整的API地址

---

### 断点4：搜索接口入口（核心入口）⭐

**文件**: `cosight_server/deep_research/routers/search.py`

**位置**: 第325-327行
```python
@searchRouter.post("/deep-research/search")
async def search(request: Request, params: Any = Body(None)):  # ← 在这里打断点（最重要！）
    logger.info(f"=====params:{params}")
```

**这是最关键的断点！** 无论通过WebSocket还是HTTP，都会到达这里。

**调试信息**：
- `params` - 完整的请求参数
- `params.get("content")` - 任务内容数组
- `params.get("sessionInfo")` - 会话信息

---

### 断点5：提取任务内容

**文件**: `cosight_server/deep_research/routers/search.py`

**位置**: 第335-344行
```python
session_info = params.get("sessionInfo", {})
plan_id = session_info.get("messageSerialNumber", "")  # ← 在这里打断点，查看plan_id
if not plan_id:
    plan_id = f"plan_{datetime.now().strftime('%Y%m%d_%H%M%S_%f')}"

# 获取查询内容
content_array = params.get('content', [])  # ← 在这里打断点，查看content数组
query_content = content_array[0]['value'] if content_array and isinstance(
    content_array, list) and len(content_array) > 0 and 'value' in content_array[0] else ""  # ← 在这里打断点，查看提取的任务文本
```

**关键变量**：
- `plan_id` - 计划ID（任务的唯一标识）
- `content_array` - 内容数组（可能包含文本、图片等）
- `query_content` - 提取的任务文本（用户输入的问题）

---

### 断点6：创建工作空间

**文件**: `cosight_server/deep_research/routers/search.py`

**位置**: 第350-358行
```python
# 构造路径：/xxx/xxx/work_space/work_space_时间戳
timestamp = datetime.now().strftime('%Y%m%d_%H%M%S_%f')
work_space_path_time = os.path.join(work_space_path, f'work_space_{timestamp}')  # ← 在这里打断点，查看工作空间路径
print(f"work_space_path_time:{work_space_path_time}")
os.makedirs(work_space_path_time, exist_ok=True)

# 将工作空间路径存储到环境变量，供RecordGenerator使用
os.environ['WORKSPACE_PATH'] = work_space_path_time  # ← 在这里打断点
```

**关键变量**：
- `work_space_path_time` - 任务的工作空间路径
- `os.environ['WORKSPACE_PATH']` - 环境变量中的路径

---

### 断点7：异步生成器入口

**文件**: `cosight_server/deep_research/routers/search.py`

**位置**: 第360行
```python
async def generator_func():  # ← 在这里打断点，进入异步生成器
    # 清空之前可能存在的队列数据并保存当前事件循环
    plan_queue = asyncio.Queue()
    main_loop = asyncio.get_running_loop()
```

**关键变量**：
- `plan_queue` - 用于流式传输的计划队列
- `main_loop` - 主事件循环

---

### 断点8：事件订阅和CoSight初始化（核心）

**文件**: `cosight_server/deep_research/routers/search.py`

**位置**: 第507-532行
```python
def run_manus():  # ← 在这里打断点，进入任务执行函数
    try:
        os.environ['WORKSPACE_PATH'] = work_space_path_time
        
        # 先订阅事件，关联plan_id
        logger.info(f"Subscribing to events for plan_id: {plan_id}")  # ← 在这里打断点
        plan_report_event_manager.subscribe("plan_created", plan_id, append_create_plan_local)
        plan_report_event_manager.subscribe("plan_updated", plan_id, append_create_plan_local)
        plan_report_event_manager.subscribe("plan_process", plan_id, append_create_plan_local)
        plan_report_event_manager.subscribe("plan_result", plan_id, append_create_plan_local)
        plan_report_event_manager.subscribe("tool_event", plan_id, append_create_plan_local)
        logger.info(f"Event subscription completed for plan_id: {plan_id}")

        # 初始化CoSight并传入plan_id
        logger.info(f"llm is {llm_for_plan.model}, {llm_for_plan.base_url}, {llm_for_plan.api_key}")  # ← 在这里打断点，查看LLM配置
        cosight = CoSight(  # ← 在这里打断点，查看CoSight初始化
            llm_for_plan,
            llm_for_act,
            llm_for_tool,
            llm_for_vision,
            work_space_path=work_space_path_time,
            message_uuid = plan_id
        )
        result = cosight.execute(query_content)  # ← 在这里打断点，开始执行任务（最重要！）
        logger.info(f"final result is {result}")
```

**关键变量**：
- `plan_id` - 计划ID
- `cosight` - CoSight实例
- `query_content` - 要执行的任务内容
- `result` - 最终执行结果

---

### 断点9：CoSight执行任务（核心业务逻辑）

**文件**: `CoSight.py`

**位置**: 第47行
```python
def execute(self, question, output_format=""):  # ← 在这里打断点，进入任务执行
    create_task = question
    retry_count = 0
    while not self.plan.get_ready_steps() and retry_count < 3:
        create_result = self.task_planner_agent.create_plan(create_task, output_format)  # ← 在这里打断点，创建计划
```

**关键变量**：
- `question` - 用户输入的任务
- `self.task_planner_agent` - 规划Agent
- `self.plan` - 计划对象

---

### 断点10：计划创建

**文件**: `app/cosight/agent/planner/task_plannr_agent.py`

**查找**: `create_plan` 方法

**关键变量**：
- 计划步骤列表
- 步骤依赖关系

---

### 断点11：步骤执行

**文件**: `CoSight.py`

**位置**: 第93行
```python
def _execute_single_step(self, question, step_index):  # ← 在这里打断点，执行单个步骤
    try:
        logger.info(f"Starting execution of step {step_index}")
        task_actor_agent = TaskActorAgent(...)  # ← 在这里打断点
        result = task_actor_agent.act(question=question, step_index=step_index)  # ← 在这里打断点，执行步骤
```

**关键变量**：
- `step_index` - 当前执行的步骤索引
- `task_actor_agent` - 执行Agent
- `result` - 步骤执行结果

---

## 🎯 推荐调试流程

### 步骤1：设置入口断点（必设）

1. 打开 `cosight_server/deep_research/routers/search.py`
2. 在第326行 `async def search(...)` 设置断点 ⭐
3. 这是最关键的入口，所有任务都会经过这里

### 步骤2：检查任务参数

1. 在第342行 `content_array = params.get('content', [])` 设置断点
2. 在第343行 `query_content = ...` 设置断点
3. 查看用户输入的任务内容

### 步骤3：检查CoSight执行

1. 在第523行 `cosight = CoSight(...)` 设置断点
2. 在第531行 `result = cosight.execute(query_content)` 设置断点
3. 这是实际执行任务的地方

### 步骤4：深入CoSight内部

1. 打开 `CoSight.py`
2. 在第47行 `def execute(...)` 设置断点
3. 跟踪计划创建和执行过程

---

## 📊 关键变量监控

建议在Watch面板添加以下表达式：

```python
# 任务内容
params.get("content")
query_content

# 计划信息
plan_id
work_space_path_time

# 执行状态
TaskManager.is_running(plan_id)

# CoSight状态
self.plan.get_ready_steps()
self.plan.get_progress()
```

---

## 🔍 调试技巧

### 1. 查看完整的请求参数
在断点4（search函数入口）暂停时：
- 查看 `params` 的完整结构
- 检查 `params.get("content")` - 用户输入
- 检查 `params.get("sessionInfo")` - 会话信息

### 2. 跟踪任务执行流程
- 从 `search()` → `generator_func()` → `run_manus()` → `CoSight.execute()`
- 使用 `F11` 进入函数，`F10` 跳过函数

### 3. 查看工作空间文件
- 在断点6暂停时，查看 `work_space_path_time`
- 执行过程中，可以查看该目录下生成的文件

### 4. 监控事件流
- 在 `append_create_plan_local` 函数（第370行）设置断点
- 可以查看每个计划更新和工具事件

---

## 🚀 快速开始调试

1. **启动Debug**：
   - 在VS Code中按 `F5`
   - 选择 "Python: Co-Sight Server (FastAPI)"

2. **设置断点**：
   - `search.py` 第326行（必须）
   - `search.py` 第531行（CoSight执行）
   - `CoSight.py` 第47行（任务执行入口）

3. **触发任务**：
   - 在前端输入任务并提交
   - 程序会在断点处暂停

4. **开始调试**：
   - 查看变量值
   - 单步执行跟踪流程
   - 监控任务执行过程

---

## 📝 接口信息总结

### 接口路径
- **HTTP POST**: `/api/nae-deep-research/v1/deep-research/search`
- **完整URL**: `http://localhost:7788/api/nae-deep-research/v1/deep-research/search`

### 请求参数格式
```json
{
    "content": [
        {
            "type": "text",
            "value": "用户输入的任务内容"
        }
    ],
    "history": [],
    "sessionInfo": {
        "locale": "zh",
        "sessionId": "会话ID",
        "username": "admin",
        "assistantNames": []
    },
    "stream": true,
    "contentProperties": "{\"deepResearchEnabled\":true}"
}
```

### 响应格式
- 流式响应（StreamingResponse）
- 每行是一个JSON对象
- 包含计划更新、步骤状态、工具事件等

---

**祝你调试顺利！** 🎉


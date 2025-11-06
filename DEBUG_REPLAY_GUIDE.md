# 回放流程后端Debug指南

## 📍 回放流程概览

当用户在前端触发回放时，后端处理流程如下：

1. **WebSocket接收消息** → `websocket_manager.py`
2. **提取replay参数** → `websocket_manager.py`
3. **调用搜索接口** → `search.py`
4. **检测回放模式** → `search.py` - `RecordGenerator`
5. **读取回放文件** → `search.py` - 回放逻辑

---

## 🔴 关键断点位置

### 断点1：WebSocket消息接收（入口）

**文件**: `cosight_server/deep_research/routers/websocket_manager.py`

**位置**: 第150行
```python
async def _send_resp(websocket, cookie, topic, message, lang):  # ← 在这里打断点
```

**调试信息**：
- `message` - 完整的WebSocket消息
- `message.get("extra")` - 包含replay相关参数

---

### 断点2：提取replay参数（重要）

**文件**: `cosight_server/deep_research/routers/websocket_manager.py`

**位置**: 第165-191行
```python
# 第165行 - 开始提取replay参数
# 支持回放控制字段：replay、replayWorkspace、replayPlanId  # ← 在这里打断点
try:
    extra = message.get("extra", {}) or {}
    from_back_end = (extra.get("fromBackEnd") or {}) if isinstance(extra, dict) else {}
    
    # 第170行 - 提取replay标志
    replay_flag = extra.get("replay")  # ← 在这里打断点，查看replay_flag的值
    if replay_flag is None:
        replay_flag = from_back_end.get("replay")
    if isinstance(replay_flag, bool) and replay_flag:
        params["replay"] = True  # ← 在这里打断点，确认replay被设置
    
    # 第177行 - 提取replayWorkspace
    replay_workspace = extra.get("replayWorkspace")  # ← 在这里打断点，查看工作区路径
    if replay_workspace is None:
        replay_workspace = from_back_end.get("replayWorkspace")
    if isinstance(replay_workspace, str) and replay_workspace:
        params["replayWorkspace"] = replay_workspace  # ← 在这里打断点，确认路径被设置
```

**关键变量**：
- `replay_flag` - 是否为回放模式
- `replay_workspace` - 工作区路径（如：`work_space/work_space_20251104_215551_317171`）
- `params["replay"]` - 最终传递给搜索接口的参数

---

### 断点3：搜索接口入口

**文件**: `cosight_server/deep_research/routers/search.py`

**位置**: 第325-327行
```python
@searchRouter.post("/deep-research/search")
async def search(request: Request, params: Any = Body(None)):  # ← 在这里打断点
    logger.info(f"=====params:{params}")
```

**调试信息**：
- `params` - 完整的请求参数
- `params.get("replay")` - 应该是 `True`
- `params.get("replayWorkspace")` - 工作区路径

---

### 断点4：回放模式检测（核心）

**文件**: `cosight_server/deep_research/routers/search.py`

**位置**: 第762-772行
```python
async def RecordGenerator(workspace_path=None):  # ← 在这里打断点
    """两种模式的生成器：
    - 记录模式（默认）：将 generate_stream_response 产生的每一行写入当前 WORKSPACE_PATH 下的 replay.json，同时正常向前端 yield
    - 回放模式：从 replay.json 读取历史数据，按行每 2 秒 yield 一次
    
    回放模式触发条件：params 中存在键 'replay' 且为真值
    """
    try:
        replay_mode = bool(params.get("replay", False)) if isinstance(params, dict) else False  # ← 在这里打断点，确认replay_mode为True
    except Exception:
        replay_mode = False
```

**关键变量**：
- `replay_mode` - 应该是 `True`（回放模式）
- `params` - 请求参数

---

### 断点5：提取工作区路径

**文件**: `cosight_server/deep_research/routers/search.py`

**位置**: 第774-812行
```python
# 第774行 - 获取显式传入的工作区路径
explicit_workspace = None
try:
    if isinstance(params, dict):
        explicit_workspace = params.get('replayWorkspace')  # ← 在这里打断点，查看工作区路径
except Exception:
    explicit_workspace = None

# 第798行 - 处理显式指定的工作区路径
elif explicit_workspace and isinstance(explicit_workspace, str) and len(explicit_workspace) > 0:
    # 处理显式指定的工作区路径
    # 如果是相对路径(如 work_space/work_space_xxx)，需要转换为绝对路径
    if not os.path.isabs(explicit_workspace):
        curr_workspace = os.path.join(os.getcwd(), explicit_workspace)  # ← 在这里打断点，查看转换后的绝对路径
    else:
        curr_workspace = explicit_workspace
    logger.info(f"使用显式工作区路径: {curr_workspace}")
```

**关键变量**：
- `explicit_workspace` - 从参数中提取的工作区路径
- `curr_workspace` - 转换后的绝对路径

---

### 断点6：读取回放文件（核心逻辑）

**文件**: `cosight_server/deep_research/routers/search.py`

**位置**: 第825-865行
```python
if replay_mode:  # ← 在这里打断点，确认进入回放模式
    # 回放模式：逐行读取历史记录
    try:
        # 确保路径是绝对路径
        if replay_file_path and not os.path.isabs(replay_file_path):
            replay_file_path = os.path.join(os.getcwd(), replay_file_path)  # ← 在这里打断点
        
        logger.info(f"========== 回放模式 ==========")
        logger.info(f"接收到的工作区路径: {explicit_workspace}")
        logger.info(f"解析后的工作区路径: {curr_workspace}")
        logger.info(f"回放文件完整路径: {replay_file_path}")  # ← 在这里打断点，查看文件路径
        logger.info(f"当前工作目录: {os.getcwd()}")
        logger.info(f"文件是否存在: {os.path.exists(replay_file_path) if replay_file_path else False}")  # ← 在这里打断点，确认文件存在
        
        if replay_file_path and os.path.exists(replay_file_path):  # ← 在这里打断点，确认文件存在
            with open(replay_file_path, 'r', encoding='utf-8') as rf:
                for line in rf:  # ← 在这里打断点，逐行读取
                    line = line.rstrip('\n')
                    if not line:
                        await asyncio.sleep(0.3)
                        continue
                    try:
                        yield line.encode('utf-8') + b'\n'  # ← 在这里打断点，查看每行内容
                    except Exception:
                        pass
                    await asyncio.sleep(0.3)  # 每行延迟0.3秒
            return
```

**关键变量**：
- `replay_file_path` - 回放文件的完整路径（如：`/path/to/work_space/work_space_20251104_215551_317171/replay.json`）
- `os.path.exists(replay_file_path)` - 文件是否存在
- `line` - 每行读取的内容

---

## 🎯 推荐调试流程

### 步骤1：设置入口断点
1. 打开 `websocket_manager.py`
2. 在第150行 `async def _send_resp` 设置断点
3. 启动Debug（F5）
4. 在前端触发回放

### 步骤2：检查参数提取
1. 在第165行（提取replay参数）设置断点
2. 检查 `message.get("extra")` 的内容
3. 单步执行，确认 `params["replay"]` 和 `params["replayWorkspace"]` 被正确设置

### 步骤3：检查搜索接口
1. 打开 `search.py`
2. 在第326行 `async def search` 设置断点
3. 检查 `params` 参数，确认 `replay=True` 和 `replayWorkspace` 存在

### 步骤4：检查回放逻辑
1. 在第762行 `RecordGenerator` 函数入口设置断点
2. 在第770行检查 `replay_mode` 是否为 `True`
3. 在第778行检查 `explicit_workspace` 的值
4. 在第825行进入回放模式分支
5. 在第839行检查文件是否存在
6. 在第841行查看逐行读取的内容

---

## 🔍 调试技巧

### 查看变量值
在断点暂停时，在VS Code的调试面板查看：
- **Locals** - 当前函数的所有局部变量
- **Watch** - 添加要监控的表达式

### 关键变量监控
建议添加以下监控表达式：
```python
params.get("replay")
params.get("replayWorkspace")
replay_mode
explicit_workspace
curr_workspace
replay_file_path
os.path.exists(replay_file_path) if replay_file_path else False
```

### 单步执行
- **F10** - Step Over（跳过函数调用）
- **F11** - Step Into（进入函数内部）
- **Shift+F11** - Step Out（跳出当前函数）
- **F5** - Continue（继续执行）

---

## ⚠️ 常见问题排查

### 问题1：replay参数未传递
- **检查点**: 断点2（websocket_manager.py 第170行）
- **排查**: 检查 `message.get("extra")` 是否包含 `replay: true`

### 问题2：工作区路径错误
- **检查点**: 断点5（search.py 第798行）
- **排查**: 检查 `explicit_workspace` 和 `curr_workspace` 的值
- **注意**: 路径可能是相对路径，需要转换为绝对路径

### 问题3：回放文件不存在
- **检查点**: 断点6（search.py 第839行）
- **排查**: 检查 `replay_file_path` 的完整路径
- **检查**: `os.path.exists(replay_file_path)` 是否为 `True`
- **验证**: 手动检查文件是否真的存在

### 问题4：回放模式未触发
- **检查点**: 断点4（search.py 第770行）
- **排查**: 检查 `replay_mode` 是否为 `True`
- **检查**: `params.get("replay")` 的值

---

## 📝 调试日志位置

后端日志会输出到控制台，关键日志包括：
- `========== 回放模式 ==========`
- `接收到的工作区路径: ...`
- `解析后的工作区路径: ...`
- `回放文件完整路径: ...`
- `文件是否存在: ...`

---

## 🚀 快速开始

1. **在VS Code中打开项目**
2. **按F5启动Debug**（选择 "Python: Co-Sight Server (FastAPI)"）
3. **设置第一个断点**：`websocket_manager.py` 第150行
4. **在前端触发回放**
5. **程序会在断点处暂停，开始调试**

---

**祝你调试顺利！** 🎉


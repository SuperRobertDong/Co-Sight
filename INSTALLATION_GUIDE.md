# Co-Sight 本地Debug环境安装指南

这是一份详细的、一步一步的安装指南，帮助你搭建Co-Sight的本地开发调试环境。

## 📋 前置准备清单

- [ ] Python 3.11 或更高版本
- [ ] pip（Python包管理器，通常随Python安装）
- [ ] 代码编辑器（VS Code、PyCharm等）
- [ ] 浏览器（Chrome、Firefox、Edge等）

---

## 步骤1️⃣：检查Python版本

### 1.1 检查Python是否已安装

打开终端（macOS/Linux）或命令提示符（Windows），运行：

```bash
python --version
```

或者：

```bash
python3 --version
```

**预期输出**：`Python 3.11.x` 或更高版本（如 `Python 3.12.0`）

### 1.2 如果Python版本不符合要求

**macOS:**
```bash
# 使用Homebrew安装Python 3.11
brew install python@3.11
```

**Linux (Ubuntu/Debian):**
```bash
# 添加deadsnakes PPA并安装
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt update
sudo apt install python3.11 python3.11-venv python3.11-pip
```

**Windows:**
1. 访问 [Python官网](https://www.python.org/downloads/)
2. 下载Python 3.11或更高版本
3. 运行安装程序，**勾选"Add Python to PATH"**

### 1.3 使用pyenv管理Python版本（推荐）

如果你使用 `pyenv` 来管理Python版本：

```bash
# 查看已安装的Python版本
pyenv versions

# 为项目设置本地Python版本（项目根目录会自动创建.python-version文件）
pyenv local 3.12.5

# 确认当前使用的Python版本
python --version
```

---

## ✅ 步骤1执行记录

**执行时间**: 2025年1月

**实际执行的操作**:
1. ✅ 检查pyenv已安装的Python版本：
   - 发现已安装: 3.8.18, 3.9.18, 3.10.13, 3.11.6, 3.12.5
   - 项目已设置使用: Python 3.12.5（通过 `.python-version` 文件）

2. ✅ 确认Python版本符合要求：
   - 当前使用: Python 3.12.5
   - 符合要求: ✅ (需要 >= 3.11)

3. ✅ 创建项目虚拟环境：
   ```bash
   python -m venv venv
   ```
   - 虚拟环境位置: `./venv/`
   - 使用的Python: `/Users/dongrobert/.pyenv/versions/3.12.5/bin/python`

**状态**: ✅ 步骤1完成，已准备好进行下一步

---

## 步骤2️⃣：进入项目目录

```bash
# 切换到项目根目录
cd /Users/dongrobert/Documents/Robert/ClearFreight/code/Co-Sight
```

**确认你在正确的目录**：你应该能看到 `requirements.txt` 和 `cosight_server` 文件夹。

---

## ✅ 步骤2执行记录

**执行时间**: 2025年1月

**实际执行的操作**:
1. ✅ 确认当前目录：
   - 执行命令: `ls -la | grep -E "(requirements.txt|cosight_server|venv)"`
   - 确认结果:
     - ✅ `cosight_server/` 目录存在
     - ✅ `requirements.txt` 文件存在  
     - ✅ `venv/` 目录存在（步骤1已创建）
   - 当前目录: `/Users/dongrobert/Documents/Robert/ClearFreight/code/Co-Sight` ✅

**状态**: ✅ 步骤2完成，已在正确的项目根目录

---

## 步骤3️⃣：创建Python虚拟环境（推荐）

### 为什么使用虚拟环境？
- 隔离项目依赖，避免与系统Python包冲突
- 方便管理不同项目的不同依赖版本
- 便于清理和重建环境

### 3.1 创建虚拟环境

```bash
# 创建虚拟环境（在项目根目录下创建 venv 文件夹）
python3 -m venv venv
```

或者（如果python3命令不可用）：
```bash
python -m venv venv
```

### 3.2 激活虚拟环境

**macOS/Linux:**
```bash
source venv/bin/activate
```

**Windows:**
```bash
# Command Prompt
venv\Scripts\activate

# PowerShell
venv\Scripts\Activate.ps1
```

**激活成功的标志**：你的命令行提示符前面会显示 `(venv)`

```
(venv) user@computer:~/Co-Sight$ 
```

### 3.3 升级pip（可选但推荐）

```bash
pip install --upgrade pip
```

---

## ✅ 步骤3执行记录

**执行时间**: 2025年1月

**实际执行的操作**:
1. ✅ 激活虚拟环境：
   ```bash
   source venv/bin/activate
   ```
   - 激活成功：提示符显示 `(venv) (base)`

2. ✅ 升级pip：
   ```bash
   pip install --upgrade pip
   ```
   - 升级结果：从 pip 24.2 升级到 pip 25.3 ✅
   - 使用镜像源：阿里云镜像（https://mirrors.aliyun.com/pypi/simple/）

**状态**: ✅ 步骤3完成，虚拟环境已激活，pip已升级

---

## 步骤4️⃣：安装项目依赖

### 4.1 安装requirements.txt中的依赖

在激活虚拟环境后，运行：

```bash
pip install -r requirements.txt
```

**这个过程可能需要几分钟**，取决于你的网络速度和系统性能。

### 4.2 验证关键包是否安装成功

```bash
# 检查FastAPI
python -c "import fastapi; print(f'FastAPI版本: {fastapi.__version__}')"

# 检查uvicorn
python -c "import uvicorn; print('Uvicorn已安装')"
```

**预期输出：**
```
FastAPI版本: 0.115.12
Uvicorn已安装
```

### 4.2 验证安装是否成功

```bash
# 检查FastAPI
python -c "import fastapi; print(f'FastAPI版本: {fastapi.__version__}')"

# 检查uvicorn
python -c "import uvicorn; print('Uvicorn已安装')"
```

**预期输出：**
```
FastAPI版本: 0.115.12
Uvicorn已安装
```

---

## ✅ 步骤4执行记录

**执行时间**: 2025年1月

**实际执行的操作**:
1. ✅ 安装项目依赖：
   ```bash
   pip install -r requirements.txt
   ```
   - 所有依赖包安装成功 ✅

2. ✅ 验证关键依赖：
   - FastAPI版本: 0.115.12 ✅
   - Uvicorn已安装 ✅
   - 关键依赖验证通过 ✅

**状态**: ✅ 步骤4完成，所有依赖已安装

---

### 4.3 如果安装遇到问题

**问题1: 网络超时**
```bash
# 使用国内镜像源（如果在中国）
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

**问题2: 权限错误（Linux/macOS）**
- 确保已经激活虚拟环境
- 不要使用 `sudo pip install`

**问题3: 特定包安装失败**
- 检查错误信息，可能需要安装系统级别的依赖
- 例如：某些包可能需要 `gcc`、`python3-dev` 等

---

## 步骤5️⃣：配置环境变量

### 5.1 复制环境变量模板

```bash
# 在项目根目录下执行
cp .env_template .env
```

### 5.2 编辑.env文件

使用你喜欢的文本编辑器打开 `.env` 文件：

```bash
# macOS/Linux
nano .env
# 或
vim .env
# 或直接用编辑器打开（VS Code）
code .env

# Windows
notepad .env
```

### 5.3 配置必需参数

**至少需要配置以下参数才能运行：**

```env
# ===== MODEL =====
API_KEY=你的API密钥（如：sk-e3fba700e89140408078debbc9fa9c0c）
API_BASE_URL=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
MAX_TOKENS=4096
TEMPERATURE=0.0
PROXY=
```

**示例配置（DeepSeek）：**
```env
API_KEY=sk-你的实际API密钥
API_BASE_URL=https://api.deepseek.com/v1
MODEL_NAME=deepseek-chat
MAX_TOKENS=4096
TEMPERATURE=0.0
```

**示例配置（OpenAI兼容的本地模型）：**
```env
API_KEY=随便填（本地模型可能不需要）
API_BASE_URL=http://localhost:11434/v1
MODEL_NAME=llama3
MAX_TOKENS=4096
TEMPERATURE=0.0
```

### 5.4 配置可选参数（推荐）

**搜索引擎配置（可选但推荐）：**

```env
# TAVILY（推荐，免费额度较高）
TAVILY_API_KEY=你的Tavily API密钥

# Google（可选）
GOOGLE_API_KEY=你的Google API密钥
SEARCH_ENGINE_ID=你的搜索引擎ID
```

**代理配置（如果需要）：**
```env
PROXY=http://proxy.example.com:8080
```

### 5.5 保存并关闭文件

- **nano**: 按 `Ctrl+O` 保存，`Ctrl+X` 退出
- **vim**: 按 `Esc`，然后输入 `:wq` 保存退出
- **VS Code**: `Cmd+S` (macOS) 或 `Ctrl+S` (Windows/Linux)

---

## ✅ 步骤5执行记录

**执行时间**: 2025年1月

**实际执行的操作**:
1. ✅ 复制环境变量模板：
   ```bash
   cp .env_template .env
   ```

2. ✅ 配置通义千问Plus模型：
   - `API_KEY`: sk-461c5d91eb9e4fe98f415dce089244fa ✅
   - `API_BASE_URL`: https://dashscope.aliyuncs.com/compatible-mode/v1 ✅
   - `MODEL_NAME`: qwen-plus ✅
   - `MAX_TOKENS`: 4096 ✅
   - `TEMPERATURE`: 0.7 ✅
   - `PROXY`: (空，不需要代理) ✅

3. ✅ 配置验证：
   - 所有必需参数已配置 ✅
   - API地址格式正确 ✅
   - 模型名称正确 ✅

**状态**: ✅ 步骤5完成，环境变量配置完成

---

## 步骤6️⃣：验证配置

### 6.1 检查.env文件是否存在

```bash
# 确认.env文件存在（不要意外提交到Git）
ls -la .env
```

**注意**：`.env` 文件应该已经在 `.gitignore` 中，不会被提交到版本控制。

### 6.2 验证Python路径

确保你在项目根目录，并且虚拟环境已激活：

```bash
# 检查当前目录
pwd

# 检查Python路径（应该指向虚拟环境）
which python
# macOS/Linux应该显示: /path/to/Co-Sight/venv/bin/python

# Windows应该显示虚拟环境路径
```

---

## ✅ 步骤6执行记录

**执行时间**: 2025年1月

**实际执行的操作**:
1. ✅ 确认.env文件存在
2. ✅ 确认所有配置已完成：
   - MODEL配置：通义千问Plus ✅
   - 搜索引擎API：已留空（使用内置百度搜索）✅
   - Browser Use Config：使用默认值 ✅
   - 数据库和其他中间件：不需要配置 ✅

**状态**: ✅ 步骤6完成，配置验证通过

---

## 步骤7️⃣：启动服务

### 7.1 激活虚拟环境

**重要**：启动服务前，必须先激活虚拟环境！

在项目根目录执行：

```bash
source venv/bin/activate
```

**激活成功的标志**：你的命令行提示符前面会显示 `(venv)`

```
(venv) user@computer:~/Co-Sight$ 
```

### 7.2 启动FastAPI服务器

确保虚拟环境已激活后，执行启动命令：

```bash
python cosight_server/deep_research/main.py
```

**或者，如果你想一次性执行（推荐）**：

```bash
source venv/bin/activate && python cosight_server/deep_research/main.py
```

### 7.3 查看启动日志

启动成功后，你应该看到类似以下的输出：

```
已成功加载.env配置文件
=== 环境变量检查 ===
✓ API_KEY = sk-****
✓ API_BASE_URL = https://dashscope.aliyuncs.com/compatible-mode/v1
✓ MODEL_NAME = qwen-plus
✓ MAX_TOKENS = 4096
✓ TEMPERATURE = 0.2
...
INFO:     Started server process [xxxxx]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:7788 (Press CTRL+C to quit)
【提示】请在浏览器访问: http://localhost:7788/cosight/
```

**关键信息**：
- ✅ 看到"已成功加载.env配置文件" - 说明配置加载成功
- ✅ 看到环境变量检查的✓标记 - 说明配置正确
- ✅ 看到"Uvicorn running on http://0.0.0.0:7788" - 说明服务启动成功
- ✅ 看到访问地址提示 - 可以打开浏览器访问

### 7.4 如果启动失败

**常见问题排查**：

**错误1: ModuleNotFoundError**
```bash
# 检查是否在虚拟环境中
which python

# 如果不在虚拟环境，先激活
source venv/bin/activate

# 重新安装依赖
pip install -r requirements.txt
```

**错误2: 端口被占用**
```bash
# macOS/Linux: 查看占用7788端口的进程
lsof -i :7788

# 终止占用端口的进程（替换xxxxx为实际进程ID）
kill -9 xxxxx

# 或者修改端口（编辑 cosight_server/deep_research/common/config.py）
# 将 "search_port": "7788" 改为其他端口，如 "8080"
```

**错误3: 环境变量未加载**
- 确认 `.env` 文件在项目根目录
- 检查 `.env` 文件格式是否正确（没有多余的空格或引号）
- 确认 API_KEY 已正确配置

**错误4: API连接失败**
- 检查网络连接
- 确认 API_KEY 是否正确
- 确认 API_BASE_URL 是否正确（通义千问应该是：https://dashscope.aliyuncs.com/compatible-mode/v1）

### 7.5 停止服务

当需要停止服务时，在运行服务的终端窗口按：

```
Ctrl+C
```

服务会优雅地停止。

---

# 重新安装依赖
pip install -r requirements.txt
```

**错误2: 端口被占用**
```bash
# macOS/Linux: 查看占用7788端口的进程
lsof -i :7788

# 终止进程或修改端口（见下文）
```

**错误3: 环境变量未加载**
- 确认 `.env` 文件在项目根目录
- 检查 `.env` 文件格式是否正确（没有多余的空格或引号）

---

## 步骤8️⃣：访问前端界面

### 8.1 打开浏览器

启动成功后，在浏览器中访问：

```
http://localhost:7788/cosight/
```

### 8.2 验证服务运行正常

你应该能看到：
- ✅ Co-Sight的欢迎界面
- ✅ 输入框和发送按钮
- ✅ 页面正常加载，没有错误

### 8.3 测试基本功能

1. 在输入框中输入一个简单的任务，例如：
   ```
   请介绍一下Python编程语言
   ```
2. 点击发送按钮
3. 观察是否有响应（可能需要几秒钟）

---

## 步骤9️⃣：验证安装完成

### 检查清单

- [x] Python 3.11+ 已安装
- [x] 虚拟环境已创建并激活
- [x] 所有依赖已安装（无错误）
- [x] `.env` 文件已配置
- [x] 服务成功启动（无错误）
- [x] 浏览器能正常访问 `http://localhost:7788/cosight/`
- [x] 能正常发送测试请求

---

## 🔧 常见问题排查

### Q1: 如何停止服务？
在运行服务的终端窗口按 `Ctrl+C`

### Q2: 如何重新启动？
```bash
# 1. 激活虚拟环境（如果还没激活）
source venv/bin/activate  # macOS/Linux
# 或
venv\Scripts\activate  # Windows

# 2. 启动服务
python cosight_server/deep_research/main.py
```

### Q3: 如何修改端口？
编辑 `cosight_server/deep_research/common/config.py`，修改：
```python
"search_port": "7788"  # 改为其他端口，如 "8080"
```

或者使用uvicorn直接指定：
```bash
uvicorn cosight_server.deep_research.main:app --host 0.0.0.0 --port 8080
```

### Q4: 如何查看详细日志？
日志会直接输出到控制台。如果需要保存日志：
```bash
python cosight_server/deep_research/main.py 2>&1 | tee cosight.log
```

### Q5: 依赖安装很慢怎么办？
使用国内镜像源：
```bash
pip install -r requirements.txt -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### Q6: 虚拟环境激活失败？
**macOS/Linux**: 可能需要运行 `chmod +x venv/bin/activate`

**Windows PowerShell**: 可能需要修改执行策略：
```powershell
Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
```

---

## 📝 下一步

安装完成后，你可以：

1. **阅读代码**：查看 `PROJECT_ANALYSIS.md` 了解项目结构
2. **修改配置**：根据需要调整 `.env` 中的模型配置
3. **开始开发**：修改代码，重启服务查看效果
4. **查看文档**：阅读 `README.md` 了解更多功能

---

## 🆘 需要帮助？

如果遇到问题：
1. 检查错误日志输出
2. 确认所有步骤都已正确执行
3. 查看项目的 Issues 或文档
4. 检查网络连接和API密钥是否有效

---

**祝安装顺利！** 🎉

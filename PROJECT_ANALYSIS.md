# Co-Sight 项目技术分析报告

## 1. 前端和后端技术栈

### 后端技术栈

**核心框架：**
- **Python**: 版本 >= 3.11（根据README要求）
- **FastAPI**: 0.115.12 - 主要Web框架
- **Uvicorn**: ASGI服务器（用于运行FastAPI应用）
- **Bottle**: 0.13.2 - 可能用于某些旧服务

**主要依赖（关键版本）：**
- `aiohttp` - 异步HTTP客户端
- `fastapi==0.115.12`
- `bottle==0.13.2`
- `requests==2.32.3`
- `websockets` - WebSocket支持
- `lagent==0.2.4` - Agent框架
- `browser-use==0.7.9` - 浏览器自动化
- `tavily-python==0.7.2` - 搜索引擎
- `mcp` - Model Context Protocol
- `docx2markdown==0.1.1`
- `ffmpeg-python==0.2.0`
- `seaborn==0.13.2`
- `markdown==3.8`
- `plotly==6.0.1`
- `python-dotenv` - 环境变量管理

**服务端口：**
- 默认端口：**7788**

### 前端技术栈

**核心技术：**
- **HTML5** / **CSS3** / **原生JavaScript**（无前端框架）
- **D3.js v7** (`d3.v7.min.js`) - 用于DAG图可视化
- **Marked.js** (`marked.min.js`) - Markdown渲染
- **Font Awesome 6.7.2** - 图标库

**前端特性：**
- WebSocket通信（原生WebSocket API）
- 响应式布局
- 实时数据可视化（DAG流程图）
- 国际化支持（i18n）

**前端文件位置：**
- `cosight_server/web/` - 前端静态文件目录

## 2. 本地Debug环境设置方法

### 前置要求
1. **Python环境**: Python >= 3.11
2. **安装依赖**:
   ```bash
   pip install -r requirements.txt
   ```

### 配置步骤

#### 步骤1: 配置环境变量
1. 复制环境变量模板：
   ```bash
   cp .env_template .env
   ```

2. 编辑 `.env` 文件，配置以下关键参数：
   - **大模型配置**（必需）：
     ```
     API_KEY=你的API密钥
     API_BASE_URL=模型API地址（如：https://api.deepseek.com/v1）
     MODEL_NAME=模型名称（如：deepseek-chat）
     MAX_TOKENS=4096
     TEMPERATURE=0.0
     ```
   
   - **搜索引擎配置**（可选）：
     ```
     TAVILY_API_KEY=你的Tavily API密钥
     GOOGLE_API_KEY=你的Google API密钥
     SEARCH_ENGINE_ID=你的搜索引擎ID
     ```
   
   - **代理配置**（如需要）：
     ```
     PROXY=代理地址
     ```

#### 步骤2: 启动后端服务
```bash
# 方式1: 直接运行主文件
python cosight_server/deep_research/main.py

# 方式2: 使用uvicorn（如果需要自定义端口）
uvicorn cosight_server.deep_research.main:app --host 0.0.0.0 --port 7788
```

#### 步骤3: 访问前端界面
启动成功后，在浏览器访问：
```
http://localhost:7788/cosight/
```

### Debug模式说明
- 服务默认运行在 `0.0.0.0:7788`
- WebSocket连接地址：`ws://localhost:7788/api/openans-support-chatbot/v1/robot/wss/messages`
- 日志会在控制台输出，包含环境变量检查和错误信息

## 3. 项目依赖组件

### 必需组件

**Python包依赖：**
- 所有 `requirements.txt` 中列出的包（已自动安装）

**系统工具（可选，根据功能使用）：**
- **FFmpeg**: 如果使用视频/音频处理功能
- **浏览器**: 如果使用浏览器自动化功能（browser-use）

### 可选组件

**数据库（可选）：**
- 项目配置中提到了 **PostgreSQL**（在 `cosight_server/deep_research/common/config.py` 中）
- 同时包含 `pysqlite3==0.5.4`，说明可能使用 **SQLite** 作为轻量级替代
- **注意**: 从 `.env_template` 中看，数据库配置不在环境变量中，说明数据库可能是可选的，或者仅在某些特定部署场景中使用

**搜索引擎API（可选，但推荐）：**
- **Tavily Search**: 用于增强搜索功能
- **Google Custom Search**: 用于Web搜索

**其他可选服务：**
- 如果配置了数据库，需要确保PostgreSQL服务运行（默认配置：127.0.0.1:5432）

### 工作目录自动创建
启动时会自动创建以下目录（如果不存在）：
- `work_space/` - 工作空间目录
- `work_space/plans/` - 计划文件目录
- `upload_files/` - 文件上传目录

## 4. 项目文件层级结构

```
Co-Sight/
├── app/                          # 核心应用代码
│   ├── agent_dispatcher/         # Agent调度器
│   │   ├── domain/              # 领域层
│   │   │   ├── llm/             # LLM相关
│   │   │   └── plan/            # 计划相关
│   │   ├── infrastructure/      # 基础设施层
│   │   │   ├── entity/          # 实体定义
│   │   │   └── util/            # 工具类
│   │   └── application/         # 应用层
│   ├── common/                   # 通用模块
│   │   ├── domain/              # 通用领域逻辑
│   │   └── logger_util.py       # 日志工具
│   └── cosight/                  # Co-Sight核心模块
│       ├── agent/                # Agent相关
│       │   ├── actor/           # 执行Agent
│       │   ├── planner/         # 规划Agent
│       │   └── base/            # Agent基类
│       ├── llm/                  # LLM封装
│       ├── task/                 # 任务管理
│       ├── tool/                 # 工具集
│       │   ├── deep_search/     # 深度搜索
│       │   └── interpreters/    # 解释器
│       └── record/               # 记录数据
├── config/                       # 配置文件
│   ├── config.py                # 主配置文件
│   └── mcp_server_config.json   # MCP服务器配置
├── cosight_server/               # 服务器代码
│   ├── deep_research/           # 深度研究服务
│   │   ├── main.py             # 服务入口（⭐启动文件）
│   │   ├── routers/            # 路由定义
│   │   │   ├── search.py       # 搜索路由
│   │   │   ├── websocket_manager.py  # WebSocket管理
│   │   │   ├── user_manager.py       # 用户管理
│   │   │   ├── chat_manager.py       # 聊天管理
│   │   │   └── feedback.py           # 反馈路由
│   │   ├── services/           # 业务服务
│   │   │   ├── i18n_service.py       # 国际化服务
│   │   │   └── credibility_analyzer.py # 可信度分析
│   │   └── common/             # 公共模块
│   │       └── config.py       # 服务配置
│   ├── sdk/                     # SDK代码
│   │   ├── common/             # 通用SDK
│   │   ├── entities/           # 实体定义
│   │   └── services/           # SDK服务
│   └── web/                     # 前端静态文件（⭐前端代码）
│       ├── index.html          # 主页面
│       ├── js/                 # JavaScript文件
│       │   ├── main.js         # 主逻辑
│       │   ├── websocket.js    # WebSocket客户端
│       │   ├── dag.js          # DAG图可视化
│       │   ├── message.js      # 消息处理
│       │   └── steps.js        # 步骤管理
│       ├── styles/             # 样式文件
│       ├── libs/               # 第三方库
│       │   ├── d3.v7.min.js    # D3.js
│       │   ├── marked.min.js   # Markdown解析
│       │   └── fontawesome-6.7.2/ # 图标库
│       └── data/               # 数据文件
├── tools/                       # 构建工具
│   └── build.py                # 构建脚本
├── .env_template                # 环境变量模板
├── requirements.txt             # Python依赖列表
├── setup.py                     # 安装配置
├── CoSight.py                   # CoSight核心类
├── llm.py                       # LLM封装
└── README.md / README-zh.md     # 项目文档
```

### 关键文件说明

**后端入口：**
- `cosight_server/deep_research/main.py` - **主启动文件**

**前端入口：**
- `cosight_server/web/index.html` - **前端主页**

**配置文件：**
- `.env` - 环境变量配置（需要从 `.env_template` 复制）
- `config/config.py` - 应用配置
- `cosight_server/deep_research/common/config.py` - 服务配置

**核心业务逻辑：**
- `app/cosight/` - Co-Sight核心功能模块
- `CoSight.py` - CoSight主类
- `llm.py` - LLM接口封装

## 5. 项目架构特点

### 架构模式
- **统一FastAPI应用**: 这是一个**单一的FastAPI项目**，同时提供：
  - RESTful API服务（后端业务逻辑）
  - WebSocket服务（实时通信）
  - 静态文件服务（前端页面）
- **分层架构**: Domain/Application/Infrastructure三层架构
- **Agent架构**: 使用Planner-Actor模式，规划Agent和执行Agent分离
- **前后端一体化**: 前端静态文件被FastAPI统一服务，无需单独的前端服务器

### 关键架构说明
**重要**: 这不是传统的前后端分离架构，而是一个**统一的FastAPI应用**：
- **后端**: FastAPI应用（`cosight_server/deep_research/main.py`）
  - 提供REST API路由（`/api/...`）
  - 提供WebSocket服务（`/api/.../wss/...`）
  - **挂载静态文件目录**：`app.mount(f"/cosight", StaticFiles(...))` 
- **前端**: 静态文件（`cosight_server/web/`）
  - HTML/CSS/JavaScript文件
  - **由FastAPI的StaticFiles提供**，访问路径：`http://localhost:7788/cosight/`

### 通信方式
- **HTTP REST API**: 用于常规API调用
- **WebSocket**: 用于实时消息推送和流式响应
- **静态文件服务**: FastAPI通过`StaticFiles`中间件提供前端文件

### 数据流
1. 用户访问 `http://localhost:7788/cosight/` → FastAPI返回前端静态文件（HTML）
2. 前端JavaScript加载后 → 通过WebSocket/HTTP API与同一FastAPI服务通信
3. FastAPI接收请求 → Planner Agent生成计划
4. Actor Agent执行具体步骤
5. 结果通过WebSocket实时推送前端
6. 前端使用D3.js可视化DAG流程

### 项目组织
```
cosight_server/
├── deep_research/          # FastAPI应用核心
│   ├── main.py            # ⭐ 单一入口：同时提供API + WebSocket + 静态文件服务
│   ├── routers/           # API路由
│   └── services/          # 业务服务
├── web/                   # 前端静态文件（由main.py挂载）
│   ├── index.html
│   ├── js/
│   └── styles/
└── sdk/                   # SDK代码（被deep_research使用）
```

**总结**: 这是一个**单体FastAPI应用**，前端静态文件由FastAPI统一提供服务，无需Nginx等反向代理（开发环境）。

---

**生成时间**: 2025年1月
**分析基于**: Co-Sight项目代码库

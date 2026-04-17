# LangChain ReAct Agent — 扫地机器人智能客服

基于 LangChain ReAct 框架构建的智能客服系统，集成 RAG 知识库检索、外部数据查询与动态 Prompt 切换，提供 Streamlit 对话界面。

---

## 核心特性

- **ReAct Agent**：基于 LangChain `create_react_agent`，支持多轮推理与工具调用
- **RAG 知识库**：使用 ChromaDB 向量存储，支持 PDF/TXT 文档增量入库（MD5 去重）
- **动态 Prompt 切换**：通过 Middleware 机制，在报告生成场景自动切换系统提示词
- **外部数据集成**：从 CSV 文件读取用户使用记录，支持按用户 ID + 月份查询
- **流式输出**：Agent 响应逐字符流式渲染，打字机效果
- **结构化日志**：按日期滚动的文件日志 + 控制台双输出

---

## 项目结构

```
langchain_ReAct_Agent/
├── app.py                        # Streamlit 入口，对话 UI
├── requirements.txt              # 依赖列表
├── .env.example                  # 环境变量模板
├── agent/
│   ├── react_agent.py            # ReactAgent 核心类
│   └── tools/
│       ├── agent_tools.py        # 7 个工具函数定义
│       └── middleware.py         # 工具监控、日志、动态 Prompt 中间件
├── config/
│   ├── agent.yaml                # Agent 配置（外部数据路径）
│   ├── chroma.yaml               # ChromaDB 向量库配置
│   ├── prompts.yaml              # Prompt 文件路径配置
│   └── rag.yaml                  # 模型名称与 Provider 配置
├── data/
│   ├── *.pdf / *.txt             # 知识库原始文档（扫地机器人相关）
│   └── external/
│       └── records.csv           # 用户使用记录（1001–1010，2025 全年）
├── model/
│   └── factory.py                # ChatModel / EmbeddingsModel 工厂类
├── prompts/
│   ├── main_prompt.txt           # 默认系统提示词
│   ├── rag_summarize.txt         # RAG 摘要子链提示词
│   └── report_prompt.txt         # 报告生成专用提示词
├── rag/
│   ├── vector_store.py           # ChromaDB 向量库服务（入库 + 检索）
│   └── rag_service.py            # RAG 摘要链（检索 + 生成）
├── utils/
│   ├── config_handler.py         # YAML 配置统一加载
│   ├── env_utils.py              # .env 环境变量加载
│   ├── file_handler.py           # 文件 MD5、目录扫描、PDF/TXT 加载
│   ├── logger_handler.py         # 日志工厂（文件 + 控制台）
│   ├── path_tool.py              # 项目根路径工具
│   └── prompt_loader.py          # Prompt 文件读取
├── chroma_db/                    # ChromaDB 持久化目录（自动生成）
├── md5.txt                       # 已入库文件的 MD5 记录（增量去重）
└── logs/                         # 运行日志（按日期命名）
```

---

## 核心流程

### 知识库存储流程

```
data/ 目录文件
    │
    ▼
file_handler.get_file_md5_hex()
    │  计算文件 MD5
    ▼
md5.txt 比对
    │  已存在 → 跳过（增量去重）
    │  不存在 ↓
    ▼
file_handler.pdf_loader / txt_loader
    │  加载文档内容
    ▼
RecursiveCharacterTextSplitter
    │  chunk_size=200, chunk_overlap=20
    ▼
EmbeddingsModelFactory (DashScope text-embedding-v4)
    │  向量化
    ▼
ChromaDB.add_documents()
    │  持久化到 chroma_db/
    ▼
md5.txt 追加记录
```

### 知识库查询流程（RAG）

```
用户问题 (query)
    │
    ▼
Agent 调用 rag_summarize 工具
    │
    ▼
VectorStoreService.get_retriever()
    │  相似度检索，返回 top-k=3 文档
    ▼
PromptTemplate 格式化
    │  {input: query, context: 参考资料1/2/3}
    ▼
DeepSeek Chat Model
    │  仅基于检索内容回答
    ▼
StrOutputParser → 返回文本
```

### Agent 完整对话流程

```
用户输入
    │
    ▼
ReactAgent.execute_stream(query)
    │
    ▼
Middleware: log_before_model（记录消息数量与预览）
    │
    ▼
Middleware: report_prompt_switch（检查 context["report"]，动态切换系统提示词）
    │
    ▼
LangChain ReAct 推理循环
    ├── 调用工具 → Middleware: monitor_tool（日志 + 触发报告上下文标记）
    └── 继续推理...
    │
    ▼
流式输出 → Streamlit 逐字渲染
```

### 报告生成专用流程

```
用户请求生成报告
    │
    ▼
Agent 按顺序调用：
  1. get_user_id()        → 随机用户 ID
  2. get_current_month()  → 随机月份
  3. fill_context_for_report()  → 触发 Middleware 设置 context["report"]=True
  4. fetch_external_data(user_id, month)  → 从 records.csv 读取数据
    │
    ▼
report_prompt_switch Middleware 切换为 report_prompt.txt
    │
    ▼
生成 Markdown 格式使用报告（含保养建议）
```

---

## 工具说明

| 工具 | 功能 |
|------|------|
| `rag_summarize` | 基于知识库回答扫地机器人相关问题 |
| `get_weather` | 获取城市天气（Mock 数据） |
| `get_user_location` | 获取用户所在城市（Mock） |
| `get_user_id` | 获取用户 ID（Mock，1001–1010） |
| `get_current_month` | 获取当前月份（Mock，2025 全年） |
| `fetch_external_data` | 按用户 ID + 月份查询使用记录 |
| `fill_context_for_report` | 触发报告模式（Middleware 哨兵工具） |

---

## 配置说明

### `config/rag.yaml` — 模型配置

```yaml
embedding_model_name: text-embedding-v4   # 阿里云 DashScope 嵌入模型
chat_model_name: deepseek-chat            # DeepSeek 对话模型
deepseek_base_url: https://api.deepseek.com
model_provider: deepseek
```

### `config/chroma.yaml` — 向量库配置

```yaml
collection_name: agent          # ChromaDB 集合名
persist_directory: chroma_db    # 持久化目录
k: 3                            # 检索返回文档数
data_path: data                 # 知识库文档目录
md5_hex_store: md5.txt          # MD5 去重记录文件
allow_knowledge_file_type: ["txt", "pdf"]
chunk_size: 200                 # 文本分块大小
chunk_overlap: 20               # 分块重叠字符数
```

### `config/agent.yaml` — Agent 配置

```yaml
external_data_path: data/external/records.csv
```

### `config/prompts.yaml` — Prompt 路径配置

```yaml
main_prompt_path: prompts/main_prompt.txt
rag_summarize_prompt_path: prompts/rag_summarize.txt
report_prompt_path: prompts/report_prompt.txt
```

### 环境变量（`.env`）

参考 `.env.example`：

```env
DEEPSEEK_API_KEY=sk-xxxx              # DeepSeek API Key
DEEPSEEK_BASE_URL=https://api.deepseek.com

# 阿里云 DashScope（嵌入模型）
DASHSCOPE_API_KEY=sk-xxxx

PYTHONPATH=.
```

---

## 快速开始

### 1. 安装依赖

```bash
pip install -r requirements.txt
```

### 2. 配置环境变量

```bash
cp .env.example .env
# 编辑 .env，填入 API Key
```

### 3. 初始化知识库

知识库在首次运行时自动入库，也可单独执行：

```bash
python -c "from rag.vector_store import VectorStoreService; VectorStoreService().load_document()"
```

### 4. 启动应用

```bash
streamlit run app.py
```

### 5. 直接运行 Agent（命令行）

```bash
python agent/react_agent.py
```

---

## 依赖环境

- Python 3.11+
- 详见 `requirements.txt`

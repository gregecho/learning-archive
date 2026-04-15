# 服装智能客服 RAG 系统

基于 LangChain + Streamlit 构建的服装领域 RAG（检索增强生成）智能客服应用。用户可以上传知识库文档，系统将其向量化存储，并通过自然语言对话检索相关内容，结合 DeepSeek 大模型生成专业回答。

---

## 整体架构

系统由两条独立流程组成，共享同一个向量数据库。

```
┌─────────────────────────────────────────────────────────────────┐
│                      知识库构建流程                               │
│                   （app_file_uploader.py）                       │
│                                                                  │
│   运营人员上传 .txt 文件                                          │
│          ↓                                                       │
│   MD5 去重校验（data/md5.txt）                                    │
│          ↓                                                       │
│   RecursiveCharacterTextSplitter 分块                            │
│   （chunk_size=1000 / overlap=100）                              │
│          ↓                                                       │
│   DashScope text-embedding-v4 向量化                             │
│          ↓                                                       │
│   写入 Chroma 向量数据库（chroma_db/）                            │
│   附带元数据：source / create_time / operator                     │
└──────────────────────────┬──────────────────────────────────────┘
                           │
                    共享向量数据库
                           │
┌──────────────────────────▼──────────────────────────────────────┐
│                      对话检索流程                                 │
│                      （app_chat.py）                             │
│                                                                  │
│   用户输入问题                                                    │
│          ↓                                                       │
│   Chroma 相似度检索（k=1）                                        │
│          ↓                                                       │
│   拼装 context + 对话历史（file_history_store.py）                │
│          ↓                                                       │
│   Prompt Template 注入 System Prompt                             │
│          ↓                                                       │
│   DeepSeek Chat 模型推理                                         │
│          ↓                                                       │
│   流式输出回答 → 保存至对话历史                                    │
└─────────────────────────────────────────────────────────────────┘
```

---

## 目录结构

```
langchain_project/
├── app_chat.py              # 聊天主界面（Streamlit 入口）
├── app_file_uploader.py     # 知识库上传界面（Streamlit 入口）
├── rag.py                   # RAG 核心链
├── knowledge_base.py        # 知识库管理（文档分块、去重、写入向量库）
├── vector_stores.py         # 向量存储封装（Chroma）
├── file_history_store.py    # 对话历史持久化（JSON 文件）
├── env_utils.py             # 环境变量加载
├── config_data.py           # 全局配置
├── data/
│   ├── 尺码推荐.txt          # 知识库：尺码对照表
│   ├── 颜色推荐.txt          # 知识库：颜色搭配指南
│   ├── 洗涤养护.txt          # 知识库：洗涤养护指南
│   ├── md5.txt              # 已上传文件 MD5 记录（去重）
│   └── chat_history/        # 对话历史 JSON（按 session_id 存储）
└── chroma_db/               # Chroma 向量数据库持久化目录
```

---

## 主要模块

### `rag.py` — RAG 核心链
使用 LangChain LCEL 构建完整的 RAG 链，用 `RunnableWithMessageHistory` 包装以自动注入和保存多轮对话历史。

### `knowledge_base.py` — 知识库管理
上传文本时先计算 MD5 去重，超过 1000 字符则用 `RecursiveCharacterTextSplitter` 分块，写入 Chroma 时附带 `source`、`create_time`、`operator` 元数据。

### `vector_stores.py` — 向量存储封装
对 Chroma 的薄封装，`get_retriever()` 返回相似度检索器（`k=1`）。

### `file_history_store.py` — 对话历史持久化
实现 `BaseChatMessageHistory`，以 JSON 文件形式按 `session_id` 存储对话记录到 `./data/chat_history/`。

### `app_chat.py` — 聊天界面
Streamlit 聊天页面，维护 `st.session_state` 消息历史，调用 `RagService.chain.stream()` 实现流式输出。

### `app_file_uploader.py` — 知识库上传界面
Streamlit 页面，支持上传 `.txt` 文件，调用 `KnowledgeBaseService.upload_by_str()` 写入向量库。

---

## 配置

| 配置项 | 值 |
|---|---|
| Embedding 模型 | `text-embedding-v4`（阿里 DashScope）|
| Chat 模型 | `deepseek-chat` |
| chunk_size | 1000 |
| chunk_overlap | 100 |
| 检索 k 值 | 1 |
| 默认 session_id | `user_001` |

---

## 快速开始

**1. 配置环境变量**

创建 `.env` 文件：

```
DEEPSEEK_API_KEY=your_key
DEEPSEEK_BASE_URL=https://api.deepseek.com
ALI_API_KEY=your_key
```

**2. 安装依赖**

```bash
pip install langchain langchain-chroma langchain-community langchain-text-splitters streamlit python-dotenv
```

**3. 启动应用**

```bash
# 上传知识库文档
streamlit run app_file_uploader.py

# 启动智能客服聊天
streamlit run app_chat.py
```

---

## 内置知识库

项目预置了三个服装领域知识文件：

- 尺码推荐：身高/体重 → S~5XL 对照表
- 颜色推荐：肤色、场合、体型、季节的配色建议
- 洗涤养护：各材质（纯棉、真丝、羽绒服等）的洗涤和收纳指南

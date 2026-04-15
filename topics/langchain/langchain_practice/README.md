# LangChain Practice

Hands-on exercises covering individual LangChain concepts. Each script is self-contained and numbered in learning order.

## Setup

```bash
cp .env.example .env
# Fill in your API keys in .env
python <script>.py
```

## Subfolders

| Folder          | What's inside                                                        |
| --------------- | -------------------------------------------------------------------- |
| `agents/`       | Agent demos — tool-calling agents and reasoning loops                |
| `embeddings/`   | Embedding demos — turning text into vectors                          |
| `models/`       | Structured output and tool calling with LLMs                         |
| `models/tools/` | Multi-tool calling patterns                                          |
| `rags/`         | RAG pipeline demos — prompt templates, retrievers, runnables (01–13) |
| `data/`         | Sample data files used by scripts                                    |
| `chroma_db/`    | Local vector store (generated at runtime, not source code)           |
| `chat_history/` | Persisted chat history (generated at runtime)                        |

## Shared Utilities

- `init_llm.py` — initializes the LLM client
- `env_utils.py` — loads environment variables from `.env`

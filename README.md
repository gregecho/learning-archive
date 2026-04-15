# Learning Archive

A personal archive for tracking learning progress across different technologies. Everything lives in one repo — open `learning-archive.code-workspace` in VS Code to get a clean per-topic view in the sidebar.

## Structure

```
learning-archive/
├── learning-archive.code-workspace   ← open this in VS Code
└── topics/
    └── <tech-name>/
        ├── README.md
        ├── <tech>_practice/           # Hands-on exercises and concept demos
        └── <tech>_project/            # End-to-end project applying the tech
```

## Topics

| Topic | Practice | Project |
|---|---|---|
| [LangChain](topics/langchain/) | [langchain_practice](topics/langchain/langchain_practice/) | [langchain_project](topics/langchain/langchain_project/) |

## Adding a New Topic

1. Create `topics/<name>/`
2. Add `<name>_practice/` and `<name>_project/` subfolders
3. Add a `README.md` to each
4. Add the new folders to `learning-archive.code-workspace`

# Argus - GitHub仓库监控工具

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/yan97ao/argus)

利用 GitHub Actions 自动跟踪开源项目的每日更新，并使用 AI 分析代码变更。

## 功能特点

- **自动监控**：每日自动检查指定仓库的提交
- **报告归档**：生成 Markdown 格式的报告文件，按年份和仓库组织
- **AI 分析**：使用 DeepSeek 模型分析代码变更（可选）

## 报告文件结构

```
reports/
├── 2026/
│   ├── vllm/
│   │   └── 2026-01-01.md
│   └── sglang/
│       └── 2026-01-01.md
```

## 快速开始

### 1. Fork 本仓库并配置 Secrets

在仓库的 `Settings` → `Secrets and variables` → `Actions` 中添加：

| Secret | 说明 |
|--------|------|
| `TOKEN` | GitHub 访问令牌（需要 `repo` 权限） |
| `LLM_API_KEY` | DeepSeek API 密钥 |
| `LLM_MODEL` | 模型名称（如 `deepseek-chat`） |
| `LLM_BASE_URL` | API 端点（如 `https://api.deepseek.com/chat/completions`） |

### 2. 启用 GitHub Actions

在 `Settings` → `Actions` → `General` 中启用 Actions，工作流会自动运行。

### 3. 本地调试

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# 运行（--dry-run 只输出不创建文件）
source .env
python src/monitor.py --dry-run
```

## 配置

### 必需环境变量

| 变量 | 说明 |
|------|------|
| `TOKEN` | GitHub 访问令牌 |
| `REPOSITORY` | 目标仓库（如 `owner/repo`） |
| `LLM_API_KEY` | LLM API 密钥 |
| `LLM_MODEL` | LLM 模型名称 |
| `LLM_BASE_URL` | LLM API 端点 |

### 命令行参数

| 参数 | 说明 |
|------|------|
| `--debug` | 启用详细日志 |
| `--dry-run` | 只输出报告，不创建文件 |
| `--enable-analysis` | 启用 AI 分析 |

### 自定义监控仓库

编辑 `src/monitor.py` 中的 `REPOSITORIES` 列表：

```python
REPOSITORIES = [
    "vllm-project/vllm",
    "你的仓库",
]
```

## 运行机制

1. GitHub Actions 每天凌晨 2 点（CST）自动运行
2. 获取监控仓库过去 24 小时的提交
3. 生成 Markdown 报告
4. 提交报告文件到 `reports/` 目录

## 常见问题

**Q: 如何在不创建文件的情况下测试？**
A: 使用 `--dry-run` 参数。

**Q: `--debug` 和 `--dry-run` 有什么区别？**
A:
- `--debug`：详细日志，仍会创建文件
- `--dry-run`：不创建文件，只输出到控制台
- 两者可同时使用：`--dry-run --debug`

**Q: 报告文件保存在哪里？**
A: `reports/YYYY/repo-name/YYYY-MM-DD.md`

## 许可证

MIT License

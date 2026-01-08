# Argus - GitHub仓库监控工具

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/yan97ao/argus)

利用 GitHub Actions 自动跟踪开源项目的每日更新，并使用 AI 分析代码变更。

## 功能特点

- **自动监控**：每日自动检查指定仓库的提交
- **报告归档**：生成 Markdown 格式的报告文件，按年份和仓库组织
- **AI 分析**：使用 DeepSeek 模型分析代码变更（可选）
- **🆓 重要性评分**：智能评估提交影响，自动分级（高/中/低）
- **🆓 分级分析**：根据重要性动态调整分析深度，节省 Token 消耗
- **🆓 智能速率控制**：根据 API 响应时间动态调整请求频率
- **🆓 增强报告格式**：支持目录、统计摘要、按重要性分组展示

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

#### 使用 uv（推荐）

```bash
# 安装 uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# 安装依赖
uv sync

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# （可选）配置文件
cp config.yaml.example config.yaml
# 根据需要编辑 config.yaml

# 运行（--dry-run 只输出不创建文件）
source .env
uv run python src/monitor.py --dry-run
```

#### 使用 pip（传统方式，已弃用）

```bash
# 安装依赖
pip install -r requirements.txt

# 配置环境变量
cp .env.example .env
# 编辑 .env 文件

# （可选）配置文件
cp config.yaml.example config.yaml
# 根据需要编辑 config.yaml

# 运行（--dry-run 只输出不创建文件）
source .env
python src/monitor.py --dry-run
```

## 配置

### 配置文件 (config.yaml)

`config.yaml` 是一个可选的配置文件，用于自定义重要性评分、速率限制和报告格式等行为。

```bash
# 复制示例配置
cp config.yaml.example config.yaml
```

#### 重要性评分配置

控制如何评估提交的重要性：

```yaml
importance:
  # 提交类型权重（权重越高越重要）
  commit_types:
    feat: 8          # 新功能
    fix: 7           # Bug 修复
    docs: 2          # 文档更新
    # ... 更多类型

  # 重要性等级阈值（总分）
  thresholds:
    high: 10         # >=10 为高重要度
    medium: 6        # 6-9 为中重要度
    # <6 为低重要度
```

#### 速率限制配置

控制 API 请求频率：

```yaml
rate_limit:
  delays:
    fast: 5          # API 响应快时的延迟（秒）
    normal: 10       # 默认延迟
    slow: 15         # API 响应慢时的延迟
```

#### 报告格式配置

控制报告输出格式：

```yaml
format:
  enable_toc: true         # 启用目录（TOC）
  enable_grouping: true    # 按重要程度分组
  enable_stats: true       # 显示统计摘要
```

**注意**：如果 `config.yaml` 不存在，程序会使用内置的默认配置。

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
| `--config <path>` | 指定配置文件路径（默认：项目根目录的 config.yaml） |

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

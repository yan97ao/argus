# Argus - GitHub仓库监控工具

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/yan97ao/argus)

利用GitHub Actions自动跟踪开源项目的每日更新，并使用AI分析代码变更

## 功能特点

- **自动监控**: 每日自动检查指定GitHub仓库的更新
- **定时运行**: 每天凌晨2点（CST）自动执行监控任务
- **格式化报告**: 生成结构化的更新报告，包含详细的提交信息
- **自动记录**: 自动创建GitHub Issue记录每日更新内容
- **AI分析**: 使用DeepSeek大模型分析代码变更，提供技术洞察
- **智能筛选**: 按文件类型和重要性分类展示变更内容
- **灵活配置**: 支持命令行参数和环境变量配置

## 监控目标

当前配置监控以下开源项目：
- [vllm-project/vllm](https://github.com/vllm-project/vllm) - 高性能大语言模型推理引擎
- [sgl-project/sglang](https://github.com/sgl-project/sglang) - 结构化生成语言
- [ai-dynamo/dynamo](https://github.com/ai-dynamo/dynamo) - AI动态优化框架

## 项目架构

```
argus/
├── src/
│   ├── monitor.py          # 主程序入口，协调各模块完成监控任务
│   ├── github_utils.py     # GitHub API操作工具函数
│   └── llm.py             # LLM集成模块，提供AI分析功能
├── .github/workflows/
│   └── daily-update.yml   # GitHub Actions工作流定义
├── requirements.txt        # Python依赖包列表
└── README.md              # 项目说明文档
```

### 核心模块说明

- **`monitor.py`**: 主控制器，负责参数解析、流程控制和结果整合
- **`github_utils.py`**: GitHub API封装，处理仓库访问、提交获取、Issue创建等
- **`llm.py`**: AI分析引擎，使用DeepSeek API对代码变更进行智能分析

### 技术依赖

- **PyGithub 2.1.1**: GitHub API的Python封装库，提供完整的GitHub API访问
- **python-dateutil 2.8.2**: 日期时间处理库，支持复杂的时间计算
- **pytz 2024.1**: 时区处理库，确保准确的时间转换（Asia/Shanghai）
- **requests 2.31.0**: HTTP请求库，用于调用DeepSeek API

## 快速开始

### 1. 部署到GitHub

1. **Fork本仓库**到你的GitHub账号
2. **启用Actions**: 在仓库的 `Settings` → `Actions` → `General` 中启用Actions
3. **配置密钥**: 在 `Settings` → `Secrets and variables` → `Actions` 中添加：
   - `TOKEN`: GitHub个人访问令牌（需要repo和issues权限）
   - `LLM_API_KEY`: DeepSeek API密钥
   - `LLM_MODEL`: （可选）模型名称，默认为 `deepseek-chat`

#### GitHub Actions配置详情
- **运行环境**: Ubuntu Latest
- **Python版本**: 3.10
- **调度时间**: 每天18:00 UTC（北京时间凌晨2:00）
- **权限要求**: 
  - `issues: write` - 创建监控报告Issue
  - `contents: write` - 访问仓库内容
  - `pull-requests: write` - 处理PR相关操作
- **Git设置**: `fetch-depth: 0` 获取完整历史记录

### 2. 本地开发调试

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/argus.git
cd argus

# 2. 创建虚拟环境（推荐Python 3.10+）
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行调试模式（只输出日志，不创建Issue）
python src/monitor.py \
  --debug \
  --github-token "你的GitHub Token" \
  --enable-analysis \
  --repo "你的用户名/argus" \
  --llm-api-key "你的DeepSeek API密钥" \
  --llm-model "deepseek-chat"
```

## 配置选项

### 命令行参数

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--github-token` | GitHub个人访问令牌 | 是 | - |
| `--repo` | 目标仓库（格式：owner/repo） | 是 | - |
| `--debug` | 启用调试模式，输出详细日志信息 | 否 | False |
| `--enable-analysis` | 启用LLM分析功能 | 否 | False |
| `--llm-api-key` | DeepSeek API密钥 | 否* | - |
| `--llm-model` | 指定LLM模型名称 | 否 | deepseek-chat |

*注：启用LLM分析时必需

### 环境变量

- `GITHUB_TOKEN`: GitHub访问令牌
- `GITHUB_REPOSITORY`: 目标仓库名称（用于当前仓库识别）
- `GITHUB_REPOSITORY_NAME`: 目标仓库名称（优先级高于GITHUB_REPOSITORY）
- `LLM_API_KEY`: DeepSeek API密钥
- `LLM_MODEL`: LLM模型名称

#### 参数优先级说明
- **GitHub Token**: 命令行参数 `--github-token` > 环境变量 `GITHUB_TOKEN` > 无认证模式
- **目标仓库**: 命令行参数 `--repo` > 环境变量 `GITHUB_REPOSITORY_NAME` > 环境变量 `GITHUB_REPOSITORY`
- **LLM API密钥**: 命令行参数 `--llm-api-key` > 环境变量 `LLM_API_KEY`
- **LLM模型**: 命令行参数 `--llm-model` > 环境变量 `LLM_MODEL` > 默认值 `deepseek-chat`

### 自定义监控仓库

修改 `src/monitor.py` 中的 `REPOSITORIES` 列表：

```python
REPOSITORIES = [
    "vllm-project/vllm",
    "sgl-project/sglang", 
    "ai-dynamo/dynamo",
    "你的组织/你的项目",  # 添加新的监控目标
]
```

## AI分析功能

启用LLM分析后，系统将使用DeepSeek API对每个提交进行深度分析，提供专业的技术洞察。

### API配置
- **服务端点**: https://api.deepseek.com/chat/completions
- **默认模型**: deepseek-chat
- **温度参数**: 1.0（保证分析的创造性和多样性）
- **最大令牌数**: 2048（确保详尽的分析内容）
- **超时设置**: 30秒

### 分析维度
系统按照标准化格式为每个提交提供以下维度的分析：

- **🎯 变更类型**: 功能增强、Bug修复、性能优化、重构、文档、测试、配置、依赖更新等
- **⚡ 重要程度**: 高🔴/中🟡/低🟢三级评估
- **📋 变更摘要**: 2-3句话概括变更的核心内容、目标和预期效果
- **🎯 影响范围**: 受影响的主要模块或组件
- **🔍 技术洞察**: 
  - 架构影响：模块关系、设计模式变化
  - 性能影响：时间和空间复杂度分析
  - 安全考虑：安全相关变更或风险点
- **⚠️ 潜在风险**: 破坏性变更、性能回归、兼容性问题
- **💡 关注建议**: 测试场景建议、升级注意事项

### 智能特性
- **文件分类**: 按源代码、测试、配置等自动分类分析
- **代码差异**: 提取并分析关键代码变更（大文件自动截断前10K字符）
- **变更统计**: 显示文件增删改统计（+增加/-删除行数）
- **多语言支持**: 智能识别不同编程语言的变更模式
- **上下文理解**: 结合提交消息和代码变更进行综合分析

## 运行机制

1. **定时触发**: GitHub Actions每天18:00 UTC（北京时间凌晨2:00）自动运行
2. **数据收集**: 获取各监控仓库过去24小时的所有提交（基于北京时间）
3. **时间计算**: 使用Asia/Shanghai时区，获取昨日00:00:00至23:59:59的提交
4. **信息整理**: 将提交信息按时间排序，格式化为Markdown表格
5. **AI分析**: （可选）使用DeepSeek API逐个分析提交，包含代码差异
6. **报告生成**: 创建标题为"仓库更新报告 (YYYY-MM-DD)"的Issue
7. **内容包含**:
   - 提交时间（自动转换为北京时间显示）
   - 提交作者信息
   - 完整的提交消息（支持多行，使用HTML<br>标签）
   - 文件变更统计
   - AI分析结果（如启用）

## 手动操作

- **手动触发**: 在仓库的Actions页面点击"Run workflow"按钮
- **查看日志**: 在Actions页面查看详细的运行日志和调试信息
- **修改调度**: 编辑`.github/workflows/daily-update.yml`中的cron表达式（当前为`0 18 * * *`）
- **测试配置**: 使用workflow_dispatch手动触发来验证配置正确性

## 注意事项

### 权限要求
- GitHub Token需要以下权限：
  - `repo`: 访问仓库内容
  - `issues`: 创建和管理Issues
  - `metadata`: 读取仓库元数据

### API限制
- **GitHub API**: 认证用户每小时5000次请求，未认证用户每小时60次
- **DeepSeek API**: 根据订阅计划限制，单次请求最大2048 tokens
- **大文件处理**: 超过100KB的文件差异自动截断至前10KB用于分析
- **请求超时**: LLM API调用设置30秒超时，避免长时间等待

### 性能考虑
- 大量提交时LLM分析可能耗时较长
- 建议在非高峰时段运行以避免API限制
- 调试模式下会输出详细日志，正式运行时建议关闭

### 安全建议
- 妥善保管API密钥，不要在代码中硬编码
- 定期轮换GitHub Token和API密钥
- 监控API使用量，避免意外的高额费用

## 故障排除

### 常见问题

**Q: Actions运行失败，提示权限不足**
A: 检查GitHub Token权限，确保包含repo和issues权限。查看Actions权限设置，确保具有issues: write, contents: write, pull-requests: write权限

**Q: LLM分析返回错误**
A: 验证DeepSeek API密钥是否正确，检查账户余额。确认API端点可访问（https://api.deepseek.com）

**Q: 调试模式下也创建了Issue**
A: 注意：--debug标志只影响日志详细程度，不会阻止Issue创建。如需避免创建Issue，请在测试环境中运行

**Q: 提交信息显示不完整或时间错误**
A: 检查时区设置，系统使用Asia/Shanghai时区。验证GitHub API速率限制状态，认证用户限制为每小时5000次请求

**Q: 大文件变更分析不完整**
A: 系统会自动截断超过100KB的文件差异，只保留前10KB用于LLM分析，这是正常的性能优化

**Q: 环境变量未生效**
A: 检查变量名拼写，注意优先级：命令行参数 > 特定环境变量 > 通用环境变量 > 默认值

### 调试技巧

```bash
# 启用详细日志（注意：仍会创建Issue）
python src/monitor.py --debug --github-token "token" --repo "owner/repo"

# 测试单个模块加载
python -c "from src.github_utils import *; print('GitHub utils loaded')"
python -c "from src.llm import *; print('LLM module loaded')"

# 验证GitHub连接和权限
python -c "
from src.github_utils import init_github_client
client = init_github_client('your_token')
print(f'Rate limit: {client.get_rate_limit().core.remaining}/5000')
"

# 测试仓库访问
python -c "
from src.github_utils import init_github_client, get_repository
client = init_github_client('your_token')
repo = get_repository(client, 'owner/repo')
print(f'Repository: {repo.full_name}, Stars: {repo.stargazers_count}')
"
```

## 许可证

本项目采用MIT许可证，详见[LICENSE](LICENSE)文件。

## 贡献

欢迎提交Issue和Pull Request来改进这个项目！

---

如果这个项目对你有帮助，请给个Star支持一下！

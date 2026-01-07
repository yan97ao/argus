# Argus - GitHub仓库监控工具

[![Ask DeepWiki](https://deepwiki.com/badge.svg)](https://deepwiki.com/yan97ao/argus)

🔍 利用GitHub Actions自动跟踪开源项目的每日更新，并使用AI分析代码变更

## ✨ 功能特点

- 🤖 **自动监控**: 每日自动检查指定GitHub仓库的更新
- ⏰ **定时运行**: 每天凌晨2点（CST）自动执行监控任务
- 📊 **格式化报告**: 生成结构化的更新报告，包含详细的提交信息
- 📝 **自动记录**: 自动创建GitHub Issue记录每日更新内容
- 🧠 **AI分析**: 使用DeepSeek大模型分析代码变更，提供技术洞察
- 🎯 **智能筛选**: 按文件类型和重要性分类展示变更内容
- 🔧 **灵活配置**: 支持命令行参数和环境变量配置

## 🎯 监控目标

当前配置监控以下开源项目：
- [vllm-project/vllm](https://github.com/vllm-project/vllm) - 高性能大语言模型推理引擎
- [sgl-project/sglang](https://github.com/sgl-project/sglang) - 结构化生成语言
- [ai-dynamo/dynamo](https://github.com/ai-dynamo/dynamo) - AI动态优化框架

## 🏗️ 项目架构

```
argus/
├── src/
│   ├── monitor.py          # 主程序入口，协调各模块完成监控任务
│   ├── github_utils.py     # GitHub API操作工具函数
│   └── llm.py             # LLM集成模块，提供AI分析功能
├── .github/workflows/
│   ├── daily-update.yml   # GitHub Actions工作流定义 - 每日监控
│   └── stale.yml          # GitHub Actions过期Issue/PR管理
├── requirements.txt        # Python依赖包列表
└── README.md              # 项目说明文档
```

### 核心模块说明

- **`monitor.py`**: 主控制器，负责参数解析、流程控制和结果整合
- **`github_utils.py`**: GitHub API封装，处理仓库访问、提交获取、Issue创建等
- **`llm.py`**: AI分析引擎，使用DeepSeek API对代码变更进行智能分析

## 🚀 快速开始

### 1. 部署到GitHub

1. **Fork本仓库**到你的GitHub账号
2. **启用Actions**: 在仓库的 `Settings` → `Actions` → `General` 中启用Actions
3. **配置密钥**: 在 `Settings` → `Secrets and variables` → `Actions` 中添加：
   - `TOKEN`: GitHub个人访问令牌（需要repo和issues权限）
   - `LLM_API_KEY`: DeepSeek API密钥
   - `LLM_MODEL`: （可选）模型名称，默认为 `deepseek-chat`

4. **工作流说明**: 默认配置会创建Issues记录监控结果

### 2. 本地开发调试

```bash
# 1. 克隆仓库
git clone https://github.com/你的用户名/argus.git
cd argus

# 2. 创建虚拟环境（推荐）
python -m venv .venv
source .venv/bin/activate  # Linux/Mac
# 或 .venv\Scripts\activate  # Windows

# 3. 安装依赖
pip install -r requirements.txt

# 4. 运行调试模式
python src/monitor.py \
  --debug \
  --github-token "你的GitHub Token" \
  --enable-analysis \
  --repo "你的用户名/argus" \
  --llm-api-key "你的DeepSeek API密钥" \
  --llm-model "deepseek-chat"
```

## ⚙️ 配置选项

### 命令行参数

| 参数 | 说明 | 必需 | 默认值 |
|------|------|------|--------|
| `--github-token` | GitHub个人访问令牌 | 是 | - |
| `--repo` | 目标仓库（格式：owner/repo） | 是 | - |
| `--debug` | 启用详细日志输出（DEBUG级别） | 否 | False |
| `--dry-run` | dry-run模式：只输出报告到控制台，不创建GitHub Issue | 否 | False |
| `--enable-analysis` | 启用LLM分析功能 | 否 | False |
| `--llm-api-key` | DeepSeek API密钥 | 否* | - |
| `--llm-model` | 指定LLM模型名称 | 否 | deepseek-chat |

*注：启用LLM分析时必需

### 环境变量

- `GITHUB_TOKEN`: GitHub访问令牌
- `GITHUB_REPOSITORY`: 目标仓库名称
- `GITHUB_REPOSITORY_NAME`: 目标仓库名称（备用）
- `LLM_API_KEY`: DeepSeek API密钥
- `LLM_MODEL`: LLM模型名称

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

## 🧠 AI分析功能

启用LLM分析后，系统将为每个提交提供：

### 📊 分析维度
- **🎯 变更类型**: 功能增强、Bug修复、性能优化等
- **⚡ 重要程度**: 高/中/低三级评估
- **🎯 影响范围**: 核心模块、API变更、用户体验影响
- **📋 变更摘要**: 简洁的变更内容总结
- **🔍 技术洞察**: 架构、性能、安全等多维度分析
- **⚠️ 潜在风险**: 识别可能的风险点
- **💡 关注建议**: 给开发者的具体建议

### 🎨 智能特性
- **文件分类**: 自动按源代码、测试、配置等分类
- **重要性评估**: 智能识别关键文件和变更
- **代码差异**: 提取并展示关键代码变更
- **影响分析**: 评估变更对系统的潜在影响

## 🔄 运行机制

1. **定时触发**: GitHub Actions每天凌晨2点（CST）自动运行
2. **数据收集**: 获取各监控仓库过去24小时的所有提交
3. **信息整理**: 将提交信息按时间排序，格式化为表格
4. **AI分析**: （可选）使用DeepSeek API分析代码变更
5. **报告生成**: 为每个监控仓库分别创建一个 Issue，标题格式为“(YYYY-MM-DD): (owner/repo) 仓库更新报告”
6. **内容包含**:
   - 📅 提交时间（北京时间）
   - 👤 提交作者信息
   - 📝 完整的提交消息
   - 📊 文件变更统计
   - 🧠 AI分析结果（如启用）

## 🎮 手动操作

- **手动触发**: 在仓库的Actions页面点击"Run workflow"
- **查看日志**: 在Actions页面查看详细的运行日志
- **详细日志**: 使用`--debug`参数启用详细日志输出
- **Dry-run测试**: 使用`--dry-run`参数只输出报告内容，不创建Issue

## 🗂️ 自动化管理

### 过期Issue清理
仓库配置了自动化的过期Issue和PR管理机制：

- **检测频率**: 每日凌晨运行自动检查
- **标记为过期**: 30天无活动的Issue/PR会被标记为`stale`
- **自动关闭**: 标记为过期后7天内无新活动将自动关闭
- **豁免标签**: 带有`keep-alive`、`pinned`、`enhancement`标签的Issue不会被自动处理
- **手动触发**: 可在Actions页面手动触发"Stale Issues and PRs"工作流

## ⚠️ 注意事项

### 安全测试建议
- **使用--dry-run模式**：在测试时建议使用 `--dry-run` 参数，只输出报告内容而不创建Issue
- **使用专用测试仓库**：如需测试Issue创建功能，建议在自己拥有的测试仓库中进行
- **模块测试**：使用 `PYTHONPATH=src python -c "from github_utils import *; print('GitHub utils loaded')"` 测试模块导入
- **CLI验证**：使用 `python src/monitor.py --help` 验证命令行功能

### 权限要求
- GitHub Token需要以下权限：
  - `repo`: 访问仓库内容
  - `issues`: 创建和管理Issues
  - `metadata`: 读取仓库元数据

### API限制
- **GitHub API**: 注意速率限制，认证用户每小时5000次请求
- **DeepSeek API**: 根据你的订阅计划有不同的调用限制
- **大文件处理**: 超过1000行变更的文件会被智能截断

### 性能考虑
- 大量提交时LLM分析可能耗时较长
- 建议在非高峰时段运行以避免API限制
- 调试模式下会输出详细日志，正式运行时建议关闭

### 安全建议
- 妥善保管API密钥，不要在代码中硬编码
- 定期轮换GitHub Token和API密钥
- 监控API使用量，避免意外的高额费用

## 🔧 故障排除

### 常见问题

**Q: Actions运行失败，提示权限不足**
A: 检查GitHub Token权限，确保包含repo和issues权限

**Q: LLM分析返回错误**
A: 验证DeepSeek API密钥是否正确，检查账户余额

**Q: 如何在不创建Issue的情况下测试？**
A: 使用 `--dry-run` 参数，报告内容将输出到控制台，不会创建任何Issue

**Q: `--debug` 和 `--dry-run` 有什么区别？**
A:
- `--debug`: 只控制日志详细级别（DEBUG vs INFO），仍然会创建Issue
- `--dry-run`: 跳过Issue创建，将报告内容输出到控制台
- 两者可以同时使用：`--dry-run --debug` 会输出详细日志但不创建Issue

**Q: 提交信息显示不完整**
A: 可能是API限制导致，检查GitHub API速率限制状态

### 调试技巧

```bash
# 测试模块导入（安全，不会创建Issue）
PYTHONPATH=src python -c "from github_utils import *; print('GitHub utils loaded')"
PYTHONPATH=src python -c "from llm import *; print('LLM module loaded')"

# 验证CLI功能（安全，不会创建Issue）
python src/monitor.py --help

# Dry-run模式（安全，只输出报告，不创建Issue）
python src/monitor.py --dry-run --github-token "token" --repo "your-repo/test"

# Dry-run + 详细日志（安全，输出详细日志和报告，不创建Issue）
python src/monitor.py --dry-run --debug --github-token "token" --repo "your-repo/test"

# 启用详细日志（会创建Issue，建议在测试仓库使用）
python src/monitor.py --debug --github-token "token" --repo "your-test-repo/test"
```

## 📄 许可证

本项目采用MIT许可证，详见[LICENSE](LICENSE)文件。

## 🤝 贡献

欢迎提交Issue和Pull Request来改进这个项目！

---

⭐ 如果这个项目对你有帮助，请给个Star支持一下！

# argus

利用github actions跟踪一些仓库的每日更新

## 功能特点

1. 自动监控指定GitHub仓库的每日更新
2. 每天凌晨2点（CST）自动运行检查
3. 生成格式化的更新报告
4. 自动创建issue记录更新内容
5. 使用LLM分析提交内容，提供技术洞察

## 技术细节

1. 该项目目前用于监控以下项目的更新
   1. https://github.com/vllm-project/vllm
   2. https://github.com/sgl-project/sglang
   3. https://github.com/ai-dynamo/dynamo
2. 利用github action，每日2:00 CST拉取代码，并列出所有的commit msg
3. 将commit msg列表组织成表格，新建一个以当前日期为题目的issue中
4. 可选择使用OpenRouter API调用LLM对提交内容进行分析

## 代码结构

- `src/github_utils.py` - GitHub API操作相关的工具函数
- `src/monitor.py` - 主程序，负责调用工具函数完成监控任务
- `src/llm.py` - LLM集成相关功能，用于分析代码变更
- `.github/workflows/daily-update.yml` - GitHub Actions工作流定义

## 使用方法

1. Fork 本仓库到你的GitHub账号
2. 在仓库的 Settings -> Actions -> General 中启用 Actions
3. 在仓库的 Settings -> Secrets -> Actions 中设置以下密钥：
   - `TOKEN`: GitHub个人访问令牌（PAT）
   - `OPENROUTER_API_KEY`: OpenRouter API密钥
   - `OPENROUTER_MODEL`: (可选) 使用的模型，默认为"anthropic/claude-3-haiku"

## 本地调试

1. 克隆仓库到本地：
   ```bash
   git clone https://github.com/你的用户名/argus.git
   cd argus
   ```

2. 安装依赖：
   ```bash
   pip install -r requirements.txt
   ```

3. 运行调试模式：
   ```bash
   python src/monitor.py --debug --token "你的GitHub Token" --enable-analysis --repo "你的用户名/argus" --openrouter-api-key "你的OpenRouter API密钥" --openrouter-model "anthropic/claude-3-haiku"
   ```

4. 命令行参数说明：
   - `--token`: GitHub个人访问令牌（PAT）
   - `--repo`: 目标仓库（格式：owner/repo）
   - `--debug`: 启用调试模式，只显示结果不创建issue
   - `--enable-analysis`: 启用LLM分析功能
   - `--openrouter-api-key`: OpenRouter API密钥
   - `--openrouter-model`: 指定LLM模型名称

## 自定义配置

如果你想监控其他仓库，可以修改 `src/monitor.py` 文件中的 `REPOSITORIES` 列表：

```python
REPOSITORIES = [
    "vllm-project/vllm",
    "sgl-project/sglang",
    "你的用户名/你的仓库名"
]
```

## LLM分析功能

当启用LLM分析功能时，系统会：

1. 收集提交的代码变更信息，包括文件修改、添加和删除
2. 将这些信息发送到OpenRouter API进行分析
3. 获取对所有仓库更新的整体分析
4. 为每个仓库提供详细的技术洞察
5. 将这些分析结果添加到issue中

## 运行机制

1. GitHub Actions 会在每天凌晨2点（CST）自动运行
2. 脚本会检查配置的仓库在过去24小时内的所有提交
3. 将提交信息整理成表格形式，包括多行提交信息
4. 可选地使用LLM分析提交内容
5. 创建一个新的issue，标题格式为"仓库更新报告 (YYYY-MM-DD)"
6. issue内容包含每个仓库的更新情况，包括：
   - 提交时间（北京时间）
   - 提交作者
   - 完整的提交信息
   - LLM分析结果（如果启用）

## 手动触发

除了自动运行外，你也可以在仓库的 Actions 标签页中手动触发工作流。

## 注意事项

1. 确保Actions有足够的权限（issues: write, contents: write, pull-requests: write）
2. 使用LLM分析功能会消耗API额度，请注意OpenRouter的使用限制
3. 对于非常大的提交或大量文件变更，LLM分析可能不完整
4. 建议定期检查Actions的运行状态，确保监控正常工作
5. 本地调试时，请确保你的GitHub Token有足够的权限
6. API密钥和模型名称可以通过命令行参数或环境变量传递，命令行参数优先级更高

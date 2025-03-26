# argus

利用github actions跟踪一些仓库的每日更新

## 功能特点

1. 自动监控指定GitHub仓库的每日更新
2. 每天凌晨2点（CST）自动运行检查
3. 生成格式化的更新报告
4. 自动创建issue记录更新内容

## 技术细节

1. 该项目目前用于监控以下项目的更新
   1. https://github.com/vllm-project/vllm
   2. https://github.com/sgl-project/sglang
2. 利用github action，每日2:00 CST拉取代码，并列出所有的commit msg
3. 将commit msg列表组织成表格，新建一个以当前日期为题目的issue中

## 使用方法

1. Fork 本仓库到你的GitHub账号
2. 在仓库的 Settings -> Actions -> General 中启用 Actions

## 自定义配置

如果你想监控其他仓库，可以修改 `src/monitor.py` 文件中的 `REPOSITORIES` 列表：

```python
REPOSITORIES = [
    "vllm-project/vllm",
    "sgl-project/sglang",
    "你的用户名/你的仓库名"
]
```

## 运行机制

1. GitHub Actions 会在每天凌晨2点（CST）自动运行
2. 脚本会检查配置的仓库在过去24小时内的所有提交
3. 将提交信息整理成表格形式
4. 创建一个新的issue，标题格式为"仓库更新报告 (YYYY-MM-DD)"
5. issue内容包含每个仓库的更新情况，包括：
   - 提交时间
   - 提交作者
   - 提交信息

## 手动触发

除了自动运行外，你也可以在仓库的 Actions 标签页中手动触发工作流。

## 注意事项

1. 确保Actions有足够的权限（issues: write, contents: read）
2. 建议定期检查Actions的运行状态，确保监控正常工作

# Argus - GitHub Repository Monitoring Tool

Argus is a Python-based GitHub repository monitoring tool that tracks daily commits across specified repositories and generates automated reports using GitHub Issues. It includes optional AI analysis via DeepSeek API.

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Setup
- Set up Python environment and install dependencies:
  - `python -m venv .venv` -- create virtual environment (recommended)
  - `source .venv/bin/activate` -- Linux/Mac activation
  - `.venv\Scripts\activate` -- Windows activation  
  - `pip install -r requirements.txt` -- takes 30-60 seconds. NEVER CANCEL. Set timeout to 120+ seconds.
  
### Build and Test
- Validate the installation:
  - `PYTHONPATH=src python -c "from github_utils import *; print('GitHub utils loaded')"` -- test module imports
  - `PYTHONPATH=src python -c "from llm import *; print('LLM module loaded')"` -- test LLM module  
  - `python -m py_compile src/monitor.py src/github_utils.py src/llm.py` -- validate syntax
  - `python src/monitor.py --help` -- verify CLI functionality

### Run the Application
- **Local debugging mode** (enables verbose logging but still creates GitHub issues):
  ```bash
  python src/monitor.py \
    --debug \
    --github-token "your_github_token" \
    --repo "owner/repo" \
    --enable-analysis \
    --llm-api-key "your_deepseek_key" \
    --llm-model "deepseek-chat"
  ```
- **Production mode** (creates GitHub issues):
  ```bash
  python src/monitor.py \
    --github-token "your_github_token" \
    --repo "owner/repo" \
    --enable-analysis \
    --llm-api-key "your_deepseek_key"
  ```

### GitHub Actions Deployment
- Configure repository secrets in `Settings` → `Secrets and variables` → `Actions`:
  - `TOKEN`: GitHub personal access token (requires repo and issues permissions)
  - `LLM_API_KEY`: DeepSeek API key for AI analysis
  - `LLM_MODEL`: (optional) Model name, defaults to `deepseek-chat`
- Enable GitHub Actions in `Settings` → `Actions` → `General`
- Workflow runs daily at 2 AM CST (18:00 UTC) or can be triggered manually

## Validation

### Manual Testing Scenarios
- **ALWAYS validate module imports** before making changes to ensure no syntax errors:
  ```bash
  PYTHONPATH=src python -c "from github_utils import *; print('GitHub utils loaded')"
  PYTHONPATH=src python -c "from llm import *; print('LLM module loaded')"
  python -m py_compile src/monitor.py src/github_utils.py src/llm.py
  ```
- **Test CLI functionality** with `--help` to verify argument parsing:
  ```bash
  python src/monitor.py --help
  ```
- **Validate GitHub Actions workflow syntax**:
  ```bash
  python3 -c "
  import yaml
  with open('.github/workflows/daily-update.yml', 'r') as f:
      workflow = yaml.safe_load(f.read())
      print('✓ GitHub Actions workflow syntax is valid')
      print(f'✓ Workflow name: {workflow.get(\"name\")}')
      triggers = workflow.get(True, {})  # 'on' becomes True in YAML parsing
      if isinstance(triggers, dict):
          print(f'✓ Has schedule: {\"schedule\" in triggers}')
          print(f'✓ Has manual trigger: {\"workflow_dispatch\" in triggers}')
      print(f'✓ Jobs: {list(workflow.get(\"jobs\", {}).keys())}')
  "
  ```
- **Run debug mode** to test the workflow with verbose logging (NOTE: currently still creates GitHub issues due to implementation bug):
  - Monitor logs for successful GitHub API connections
  - Verify commit data retrieval from monitored repositories  
  - Check LLM analysis integration (when enabled)
  - Confirm issue content generation and formatting
- **Test production mode** only with test repositories to avoid spam in real projects

### Required Testing Steps
- **Import validation**: Test all Python modules to check for syntax errors
- **CLI validation**: Run the application with `--help` to verify argument parsing
- **GitHub Actions validation**: Check workflow file syntax with YAML parser
- **Debug mode testing**: Run the application in debug mode with valid credentials
- **API connectivity**: Verify the application can connect to GitHub API and retrieve repository data
- **Report generation**: Test the complete report generation workflow
- **Output validation**: Check that generated reports contain expected sections and formatting

## Common Tasks

### Repository Structure
```
argus/
├── src/
│   ├── monitor.py          # Main entry point and workflow orchestration
│   ├── github_utils.py     # GitHub API wrapper functions
│   └── llm.py             # DeepSeek AI integration for commit analysis
├── .github/workflows/
│   ├── daily-update.yml   # GitHub Actions workflow (runs daily at 2 AM CST)
│   └── stale.yml          # Stale issues/PRs management workflow
├── requirements.txt        # Python dependencies
└── README.md              # Comprehensive documentation
```

### Key Configuration Files
- **requirements.txt**: Python dependencies
  ```
  PyGithub==2.1.1
  python-dateutil==2.8.2
  pytz==2024.1
  requests==2.31.0
  ```

### Monitored Repositories
Current configuration monitors these repositories (defined in `src/monitor.py`):
- `vllm-project/vllm` - High-performance large language model inference engine
- `sgl-project/sglang` - Structured generation language
- `ai-dynamo/dynamo` - AI dynamic optimization framework

To add new repositories, modify the `REPOSITORIES` list in `src/monitor.py`:
```python
REPOSITORIES = [
    "vllm-project/vllm",
    "sgl-project/sglang", 
    "ai-dynamo/dynamo",
    "your-org/your-project",  # Add new monitoring targets
]
```

### Command Line Arguments
| Argument | Description | Required | Default |
|----------|-------------|----------|---------|
| `--github-token` | GitHub personal access token | Yes | - |
| `--repo` | Target repository for creating issues (format: owner/repo) | Yes | - |
| `--debug` | Enable verbose logging (NOTE: still creates issues due to bug) | No | False |
| `--enable-analysis` | Enable AI analysis using DeepSeek | No | False |
| `--llm-api-key` | DeepSeek API key (required if --enable-analysis) | No* | - |
| `--llm-model` | DeepSeek model name | No | deepseek-chat |

*Required when `--enable-analysis` is enabled

### Environment Variables
Alternative to command line arguments:
- `GITHUB_TOKEN`: GitHub access token
- `GITHUB_REPOSITORY`: Target repository name  
- `GITHUB_REPOSITORY_NAME`: Target repository name (fallback used by the code)
- `LLM_API_KEY`: DeepSeek API key
- `LLM_MODEL`: LLM model name

## Timing and Performance

### Expected Execution Times
- **Dependency installation**: 30-60 seconds (first time), 5-10 seconds (subsequent)
- **Module validation**: 1-2 seconds per module
- **Application startup**: 2-5 seconds
- **Repository monitoring**: 10-30 seconds per repository (depends on commit volume)
- **AI analysis**: 5-15 seconds per commit (when enabled)
- **Complete workflow**: 1-5 minutes total (3 repositories, with AI analysis)

### Timeout Recommendations
- `pip install -r requirements.txt` -- Set timeout to 120+ seconds. NEVER CANCEL.
- Repository data fetching -- Set timeout to 60+ seconds per repository. NEVER CANCEL.
- AI analysis requests -- Set timeout to 30+ seconds per commit. NEVER CANCEL.

### Performance Considerations
- GitHub API rate limits: 5000 requests/hour (authenticated), 60/hour (unauthenticated)
- DeepSeek API rate limits: varies by plan and model
- Application processes repositories sequentially, not in parallel
- Commit analysis time scales with diff size and complexity

## Troubleshooting

### Common Issues
- **"Unable to initialize GitHub client"**: Check GitHub token validity and permissions
- **"TypeError: Object of type bytes is not JSON serializable"**: PyGitHub exception handling issue with invalid tokens - check token format and permissions
- **API rate limit exceeded**: Wait for rate limit reset or use authenticated requests
- **Module import errors**: Verify dependencies are installed: `pip install -r requirements.txt`
- **Permission denied for issue creation**: Ensure GitHub token has `repo` and `issues` permissions
- **LLM analysis failures**: Verify DeepSeek API key and check API status
- **Debug mode still creates issues**: Current implementation has a bug where `--debug` mode still creates GitHub issues. The debug flag only enables verbose logging but doesn't prevent issue creation

### Safer Testing Approach
Since `--debug` mode still creates issues, use these strategies for safe testing:
- **Test with a dedicated test repository** that you own and can safely create issues in
- **Test module imports and CLI help** without running the full monitoring workflow
- **Use token validation** by running without the `--repo` parameter to test GitHub connectivity
- **Validate individual functions** by importing modules in Python REPL

### Debug Commands
```bash
# Test individual module loading
PYTHONPATH=src python -c "from github_utils import *; print('GitHub utils loaded')"
PYTHONPATH=src python -c "from llm import *; print('LLM module loaded')"

# Enable verbose logging
python src/monitor.py --debug --github-token "token" --repo "owner/repo"

# Test without AI analysis
python src/monitor.py --debug --github-token "token" --repo "owner/repo"
```

### Notes on Workflows
- Daily monitoring runs with `--debug` enabled by default and still creates issues (current behavior).
- A separate `stale.yml` workflow manages stale Issues/PRs daily and can be triggered manually.

## Important Notes
- **No build process required** - Pure Python application with no compilation
- **No test suite exists** - Validate changes through manual testing scenarios above
- **No linting configuration** - Follow PEP 8 style guidelines manually
- **Beijing timezone used** for date calculations (Asia/Shanghai)
- **Debug mode bug**: `--debug` flag enables verbose logging but still creates GitHub issues
- **Use test repositories** for validation to avoid creating unwanted issues in production repos
- **Virtual environment recommended** to isolate dependencies
- **NEVER CANCEL long-running operations** - GitHub API calls and dependency installation may take several minutes
- **Timeout considerations**: Always set timeouts of 60+ seconds for GitHub API operations and 120+ seconds for dependency installation
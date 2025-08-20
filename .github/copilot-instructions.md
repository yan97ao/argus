# Argus - GitHub Repository Monitoring Tool

Always reference these instructions first and fallback to search or bash commands only when you encounter unexpected information that does not match the info here.

## Working Effectively

### Bootstrap and Setup
- **Check Python version**: `python3 --version` (requires Python 3.10+, tested with Python 3.12.3)
- **Create virtual environment** (recommended): 
  - `python3 -m venv .venv` -- takes 3 seconds. NEVER CANCEL.
  - `source .venv/bin/activate` (Linux/Mac) or `.venv\Scripts\activate` (Windows)
- **Install dependencies**: `pip install -r requirements.txt` -- takes 10-30 seconds depending on network. NEVER CANCEL. Set timeout to 3+ minutes for fresh installs.
- **Validate installation**: 
  - `python3 src/monitor.py --help` -- takes 0.2 seconds. Should show usage information.
  - `python3 -c "from src.github_utils import *; print('GitHub utils loaded')"` -- takes 0.2 seconds
  - `python3 -c "from src.llm import *; print('LLM module loaded')"` -- takes 0.1 seconds

### Run the Application
- **Debug mode (no Issues created)**: `python3 src/monitor.py --debug --github-token "your_token" --repo "owner/repo"` -- takes 1-5 seconds for basic validation, 30+ seconds for full run with API calls. NEVER CANCEL.
- **Full monitoring with LLM analysis**: `python3 src/monitor.py --github-token "your_token" --repo "owner/repo" --enable-analysis --llm-api-key "your_deepseek_key"` -- takes 1-10 minutes depending on commit volume. NEVER CANCEL. Set timeout to 15+ minutes.
- **GitHub Actions deployment**: Workflow runs automatically at 2 AM CST (18:00 UTC) daily

### Validation and Testing
- **Test core functionality without API**: All module imports and basic functions work without external API calls
- **GitHub API requirements**: Requires valid GitHub Personal Access Token with `repo` and `issues` permissions
- **LLM analysis requirements**: Requires DeepSeek API key when using `--enable-analysis` flag
- **Error handling**: Application properly handles API authentication failures but may show stack traces (expected behavior)

## Important Project Information

### Dependencies (requirements.txt)
- PyGithub==2.1.1 - GitHub API client
- python-dateutil==2.8.2 - Date manipulation
- pytz==2024.1 - Timezone handling (Asia/Shanghai default)
- requests==2.31.0 - HTTP requests for LLM API

### Project Structure
```
argus/
├── src/
│   ├── monitor.py          # Main entry point - orchestrates monitoring workflow
│   ├── github_utils.py     # GitHub API operations (repo access, commit fetching, issue creation)
│   └── llm.py              # DeepSeek LLM integration for code analysis
├── .github/workflows/
│   └── daily-update.yml    # GitHub Actions workflow (runs daily at 2 AM CST)
├── requirements.txt        # Python dependencies
└── README.md               # Comprehensive documentation in Chinese
```

### Core Modules
- **monitor.py**: Main controller with argument parsing and workflow orchestration
- **github_utils.py**: GitHub API wrapper handling authentication, repository access, and issue creation
- **llm.py**: AI analysis engine using DeepSeek API for intelligent code change analysis

### Configuration Options
| Parameter | Description | Required | Default |
|-----------|-------------|----------|---------|
| `--github-token` | GitHub Personal Access Token | Yes | - |
| `--repo` | Target repository (format: owner/repo) | Yes | - |
| `--debug` | Enable debug mode (no Issues created) | No | False |
| `--enable-analysis` | Enable LLM analysis | No | False |
| `--llm-api-key` | DeepSeek API key | No* | - |
| `--llm-model` | LLM model name | No | deepseek-chat |

*Required when using `--enable-analysis`

### Environment Variables
- `GITHUB_TOKEN`: GitHub access token
- `GITHUB_REPOSITORY`: Target repository name  
- `LLM_API_KEY`: DeepSeek API key
- `LLM_MODEL`: LLM model name

## Common Development Tasks

### Monitoring Repository Changes
1. **Manual execution**: `python3 src/monitor.py --debug --github-token "token" --repo "owner/repo"`
2. **With AI analysis**: Add `--enable-analysis --llm-api-key "key"` flags
3. **GitHub Actions**: Deploy to GitHub with proper secrets configured

### Customizing Monitored Repositories
Edit `REPOSITORIES` list in `src/monitor.py`:
```python
REPOSITORIES = [
    "vllm-project/vllm",
    "sgl-project/sglang", 
    "ai-dynamo/dynamo",
    "your-org/your-repo",  # Add new monitoring targets
]
```

### Testing and Validation
- **Test GitHub API connection**: Use debug mode with valid token
- **Test LLM functionality**: Enable analysis with valid DeepSeek API key
- **Validate GitHub Actions**: Check workflow YAML syntax and secrets configuration

## API and Performance Considerations

### Rate Limits and Timing
- **GitHub API**: 5000 requests/hour for authenticated users
- **DeepSeek API**: Varies by subscription plan
- **Application execution**: 1-10 minutes for typical runs. NEVER CANCEL long-running operations.
- **Large repositories**: May take longer due to commit volume

### Known Issues and Limitations
- **GitHub API error handling**: May show detailed stack traces for authentication failures (not a bug)
- **Large file processing**: Files over 1000 lines are intelligently truncated in LLM analysis
- **Network connectivity**: pip install may timeout in restricted environments -- use system packages when available

## Troubleshooting

### Common Issues
- **"Module not found" errors**: Ensure you're running from repository root with `python3 src/monitor.py`
- **GitHub API failures**: Verify token permissions (repo, issues, metadata)
- **LLM analysis errors**: Check DeepSeek API key validity and account balance
- **No Issues created**: Check if using `--debug` mode (intended behavior)

### Debug Commands
```bash
# Enable verbose logging
python3 src/monitor.py --debug --github-token "token" --repo "owner/repo"

# Test individual modules
python3 -c "from src.github_utils import *; print('GitHub utils loaded')"
python3 -c "from src.llm import *; print('LLM module loaded')"

# Validate GitHub Actions workflow
python3 -c "import yaml; yaml.safe_load(open('.github/workflows/daily-update.yml'))"
```

### GitHub Actions Deployment
1. Fork repository to your GitHub account
2. Enable Actions in repository settings
3. Configure secrets in repository settings → Secrets and variables → Actions:
   - `TOKEN`: GitHub Personal Access Token
   - `LLM_API_KEY`: DeepSeek API key  
   - `LLM_MODEL`: (optional) Model name

## Security and Best Practices

### API Key Management
- Never hardcode API keys in source code
- Use GitHub Secrets for Actions deployment
- Regularly rotate GitHub tokens and API keys
- Monitor API usage to avoid unexpected charges

### Development Workflow
- Always test changes in debug mode first
- Validate all commands before committing instructions
- Use virtual environments for dependency isolation
- Check GitHub Actions logs for deployment issues

## Time Expectations and Timeouts

### Critical Timing Information
- **NEVER CANCEL**: All operations below should be allowed to complete fully
- **Dependency installation**: 10-30 seconds fresh, 1-3 seconds cached. Set timeout to 5+ minutes.
- **Application startup**: 0.2 seconds for help, 1-5 seconds for validation. Set timeout to 30+ seconds.
- **Full monitoring run**: 1-10 minutes depending on repository size and API responses. Set timeout to 15+ minutes.
- **Virtual environment creation**: 3 seconds. Set timeout to 30+ seconds.
- **GitHub Actions workflow**: 2-5 minutes typical. Set timeout to 10+ minutes.

### When Operations May Take Longer
- First-time dependency installation in clean environment
- Large repositories with many commits
- LLM analysis of complex code changes
- Network latency to GitHub/DeepSeek APIs

Always err on the side of longer timeouts rather than canceling operations prematurely.
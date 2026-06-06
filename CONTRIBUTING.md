# Contributing

## Development Setup

1. Clone the repository
2. Create a virtual environment: `python -m venv venv`
3. Activate it: `source venv/bin/activate`
4. Install dependencies: `pip install -r requirements.txt`
5. Copy `.env.example` to `.env` and fill in your API keys
6. Run the development server: `uvicorn backend.main:app --reload`

## Code Style

- Python: Follow PEP 8
- JavaScript/React: Follow ESLint config
- Use meaningful variable names
- Write docstrings for functions and classes
- Add tests for new features

## Pull Request Process

1. Create a feature branch from `main`
2. Write tests for your changes
3. Ensure all tests pass
4. Update documentation if needed
5. Submit a PR with a clear description

## Reporting Issues

- Use GitHub Issues
- Include steps to reproduce
- Include relevant logs and environment details

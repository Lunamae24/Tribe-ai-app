# Contributing to Tribe AI App

Thank you for your interest in contributing to the Tribe AI App!

## Development Setup

1. Fork the repository
2. Clone your fork
3. Create a virtual environment
4. Install dependencies: `pip install -r requirements.txt`
5. Create a `.env` file based on `.env.example`
6. Run tests: `pytest`

## Code Style

- We use `black` for code formatting
- We use `flake8` for linting
- We use `mypy` for type checking

Run these before committing:
```bash
black app tests
flake8 app tests
mypy app
```

## Testing

- Write tests for all new features
- Ensure all tests pass before submitting PR
- Maintain or improve code coverage

## Pull Request Process

1. Create a feature branch from `develop`
2. Make your changes
3. Add/update tests
4. Update documentation if needed
5. Ensure all tests and checks pass
6. Submit PR with clear description
7. Address review feedback

## Commit Messages

Use clear, descriptive commit messages:
- `feat: Add new feature`
- `fix: Fix bug in component`
- `docs: Update documentation`
- `test: Add tests for feature`
- `refactor: Refactor code`

## Code of Conduct

- Be respectful and inclusive
- Focus on constructive feedback
- Help create a welcoming environment

## Questions?

Open an issue or reach out to the maintainers.

Thank you for contributing!

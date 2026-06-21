# Contributing

Thank you for your interest in contributing to this project!

## How to Contribute

### Reporting Issues

- Check existing issues before creating a new one
- Use the issue templates when available
- Provide clear reproduction steps for bugs
- Include relevant logs, screenshots, or error messages

### Pull Requests

1. **Fork and clone** the repository
2. **Create a branch** for your changes: `git checkout -b feature/your-feature-name`
3. **Make your changes** following the project's code style
4. **Add tests** for new functionality
5. **Run `make pre-commit`** to format, lint, and test everything
6. **Update documentation** (README, CHANGELOG, etc.)
7. **Commit** with clear, descriptive messages
8. **Push** to your fork and **submit a pull request**

### Pull Request Guidelines

- Fill out the PR template completely
- Link related issues
- Keep changes focused and atomic
- Ensure all CI checks pass
- Respond to review feedback promptly

### Code Style

- Follow existing code conventions
- Run `make pre-commit` before committing (formats, lints, and tests in one step)
- Write clear, self-documenting code
- Add comments for complex logic

### Testing

- Write unit tests for new features
- Ensure existing tests pass
- Aim for good test coverage
- Test edge cases and error conditions

## 🏗️ Project Structure

```
saxml2aws-multi/
├── .github/
│   ├── workflows/        # CI/CD workflows
│   └── dependabot.yml    # Dependency updates config
├── saml2awsmulti/        # Main Python package
│   ├── __init__.py
│   ├── aws_login.py      # Main CLI logic
│   ├── file_io.py
│   ├── saml2aws_helper.py
│   └── selector.py
├── tests/                # Unit tests
│   ├── test_aws_login.py
│   ├── test_file_io.py
│   ├── test_saml2aws_helper.py
│   └── test_selector.py
├── pyproject.toml        # Project metadata and dependencies
├── Makefile              # Build and test commands
├── CHANGELOG.md          # Version history and changes
├── CODE_OF_CONDUCT.md    # Community guidelines
├── CONTRIBUTING.md       # Contribution guidelines
├── SECURITY.md           # Security policy
└── README.md
```

## Development Workflow

### First-time Setup

```bash
make setup-init         # Configure venv, lock, install all dependencies
```

### Common Commands

```bash
make help               # Show all available commands
make install-all        # Install all dependencies (main, dev, test)
make test               # Run tests without coverage
make test-with-coverage # Run tests with coverage
make format-python      # Auto-format Python code with black
make lint-python        # Lint Python code with flake8
make lint-yaml          # Lint YAML files with yamllint
make pre-commit         # Run all quality checks (format, lint, test)
make build              # Build the package
make clean              # Clean build artifacts
```

### Running Tests

```bash
# Run all quality checks before committing
make pre-commit

# Run tests with coverage
make test-with-coverage

# Run tests only
make test
```

### Managing Dependencies

```bash
# Update dependencies to latest compatible versions
make update-deps

# Regenerate lock file
make lock
```

## Questions?

If you have questions, please open an issue or reach out to the maintainers.

## Code of Conduct

Please note that this project follows a [Code of Conduct](CODE_OF_CONDUCT.md). By participating, you agree to uphold this code.

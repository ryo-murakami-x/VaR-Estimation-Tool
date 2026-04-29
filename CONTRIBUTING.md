# Contributing to VaR Estimation Tool

Thank you for your interest in contributing! This document provides guidelines and instructions for contributing.

## Code of Conduct

This project is committed to providing a welcoming and inclusive environment for all contributors.
Please be respectful and constructive in all interactions.

## How to Contribute

### Reporting Bugs

Before submitting a bug report, please check the issue tracker to avoid duplicates.

When reporting bugs, please include:
- Clear description of the problem
- Steps to reproduce
- Expected vs. actual behavior
- Python version and OS
- Relevant error messages or logs

**Example bug report:**
```
Title: Data reader fails with Asian character tickers

Description:
When loading stock data for ticker "133a", the reader throws an error.

Steps to reproduce:
1. Run python3 main.py
2. Enter ticker: 133a
3. Click "Load Data"

Expected: Data loads successfully
Actual: FileNotFoundError

Environment:
- Python 3.9
- macOS 12.5
- Error: Stock data file not found for ticker: 133a
```

### Suggesting Enhancements

Enhancements should be submitted as GitHub issues with:
- Clear title and description
- Use case/motivation
- Proposed implementation (if applicable)
- Related issues or PRs

**Example enhancement:**
```
Title: Add portfolio-level VaR calculation

Description:
Currently the tool supports single-stock VaR. It would be valuable
to support portfolio-level VaR with correlation matrices.

Use case:
Risk managers need to analyze diversified portfolios, not just
individual stocks.

Proposed features:
- Load multiple stocks
- Input correlation matrix or auto-calculate
- Generate portfolio VaR
```

### Pull Requests

1. **Fork** the repository
2. **Create a feature branch**: `git checkout -b feature/my-feature`
3. **Make your changes** with clear commit messages
4. **Add tests** for new functionality
5. **Run tests**: `python3 integration_test.py`
6. **Update documentation** if needed
7. **Push to your fork**: `git push origin feature/my-feature`
8. **Submit a Pull Request** with detailed description

#### Pull Request Guidelines

- Title should be descriptive
- Include reference to related issues (e.g., "Fixes #123")
- Provide clear description of changes
- Include before/after examples if applicable
- Ensure all tests pass
- Code should follow project style

**Example PR description:**
```
## Description
Adds historical VaR comparison feature to track VaR changes over time.

## Type of Change
- [x] New feature
- [ ] Bug fix
- [ ] Documentation
- [ ] Performance improvement

## Related Issues
Fixes #42

## Changes
- Added `calculate_historical_var()` method to var_calculator.py
- Created historical comparison chart in GUI
- Added 3 new test cases

## Testing
- [x] Unit tests pass
- [x] Integration tests pass
- [x] Tested with 5 different stocks
- [x] GUI responsive with large datasets

## Screenshots (if applicable)
[Add screenshots of new features]
```

## Development Setup

### Prerequisites
- Python 3.7+
- pip or conda

### Local Development

1. **Clone the repository**:
   ```bash
   git clone https://github.com/yourusername/VaR-Estimation-Tool.git
   cd VaR-Estimation-Tool
   ```

2. **Create virtual environment**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run tests**:
   ```bash
   python3 integration_test.py
   ```

5. **Launch GUI**:
   ```bash
   python3 main.py
   ```

## Coding Standards

### Style Guide

- Follow PEP 8 conventions
- Use meaningful variable names
- Maximum line length: 100 characters
- Use type hints for functions
- Write docstrings for all public methods

### Example Code Style

```python
def calculate_var_comprehensive(self,
                               num_simulations: int = 10000,
                               time_horizon: int = 10,
                               confidence_levels: Optional[List[float]] = None
                               ) -> VaRResults:
    """
    Calculate comprehensive VaR at multiple confidence levels.
    
    Args:
        num_simulations (int): Number of Monte Carlo simulations
        time_horizon (int): Time horizon in trading days
        confidence_levels (Optional[List[float]]): Confidence levels to calculate
    
    Returns:
        VaRResults: Object containing all VaR calculations
    """
    if confidence_levels is None:
        confidence_levels = [0.90, 0.95, 0.99]
    
    # Implementation here
    return results
```

### Naming Conventions

- **Classes**: PascalCase (e.g., `MonteCarloVaR`)
- **Functions/Methods**: snake_case (e.g., `calculate_var`)
- **Constants**: UPPER_SNAKE_CASE (e.g., `DEFAULT_SIMULATIONS`)
- **Private methods**: Leading underscore (e.g., `_calculate_skewness`)

### Documentation

All modules should have:
- Module-level docstring
- Class docstrings
- Function/method docstrings with Args, Returns, Raises sections

## Testing

### Writing Tests

Tests should be in `integration_test.py` or separate `test_*.py` files.

```python
def test_data_reader():
    """Test data reading functionality"""
    reader = StooqDataReader()
    success, message, df = reader.load_stock_data("1301")
    
    assert success, "Data loading should succeed"
    assert len(df) > 0, "DataFrame should not be empty"
    assert 'CLOSE' in df.columns, "CLOSE column should exist"
```

### Test Coverage

- Aim for >80% code coverage
- Test both success and failure cases
- Include edge cases
- Test with real data when possible

### Running Tests

```bash
# Run integration tests
python3 integration_test.py

# Run individual module tests
python3 data_reader.py
python3 var_calculator.py
```

## Documentation Contributions

Documentation improvements are always welcome!

- Update README.md for major feature changes
- Add docstrings to new code
- Update QUICKSTART.md with new workflows
- Create examples for complex features

## Commit Message Guidelines

Use clear, descriptive commit messages:

```
[TYPE] Description of changes

- Detailed point 1
- Detailed point 2

Fixes #issue_number
```

**Types**:
- `feat`: New feature
- `fix`: Bug fix
- `docs`: Documentation
- `test`: Tests
- `refactor`: Code refactoring
- `perf`: Performance improvement

**Example**:
```
feat: Add portfolio VaR calculation

- Implement multi-stock VaR method
- Add correlation matrix support
- Create portfolio results visualization

Fixes #42
```

## Release Process

1. Update version in `setup.py`
2. Update `CHANGELOG.md` with changes
3. Merge to `main` branch
4. Tag release: `git tag v1.0.0`
5. Push tags: `git push --tags`
6. Publish to PyPI (for maintainers)

## Questions?

- Check README.md for common questions
- Review existing issues and PRs
- Start a discussion if you have questions

## Recognition

Contributors will be recognized in:
- README.md contributors section
- Release notes
- GitHub contributors page

Thank you for contributing to make VaR Estimation Tool better! 🚀

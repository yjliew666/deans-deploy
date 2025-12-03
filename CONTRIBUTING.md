# Contributing Guide

## Development Workflow

### 1. Setup Environment

```bash
git clone <repository>
cd deans-deploy
make install
```

### 2. Create Feature Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Make Changes

```bash
# Write code
# Add tests
# Run checks
make lint
make format
make test
```

### 4. Commit Changes

```bash
git add .
git commit -m "feat: describe your changes"
```

### 5. Push and Create PR

```bash
git push origin feature/your-feature-name
```

## Code Standards

### Python

- Follow PEP 8
- Line length: 120 characters
- Use type hints
- Add docstrings

```python
def create_crisis(name: str, description: str) -> Crisis:
    """
    Create a new crisis record.
    
    Args:
        name: Crisis name
        description: Crisis description
        
    Returns:
        Crisis: Created crisis instance
    """
    return Crisis.objects.create(name=name, description=description)
```

### JavaScript/React

- Use ESLint
- Follow Airbnb style guide
- Functional components
- Hooks for state management

### Git Commits

```
feat: Add new feature
fix: Fix bug
docs: Update documentation
style: Code formatting
test: Add tests
chore: Maintenance
```

## Testing Requirements

- Minimum 80% code coverage
- All new features must have tests
- All tests must pass before PR approval

## PR Review Process

1. Automated checks must pass
2. At least 2 approvals required
3. No unresolved conversations
4. Merge to `develop` first, then `main`

## Deployment Process

Only project maintainers can deploy:

1. **Staging**: Deploy every commit to `develop`
2. **Production**: Deploy tagged releases from `main`

## Questions or Issues?

- Open an issue on GitHub
- Contact: team@deans.com

# Contributing to Dublin Bus RTPI

Thank you for your interest in contributing to the Dublin Bus RTPI Home Assistant integration! 

## How to Contribute

### Reporting Bugs

If you find a bug, please open an issue on GitHub with:
- A clear, descriptive title
- Steps to reproduce the issue
- Expected behavior
- Actual behavior
- Your Home Assistant version
- Integration version
- Relevant logs (if applicable)

### Suggesting Enhancements

We welcome suggestions! Please open an issue with:
- A clear description of the enhancement
- Why this would be useful
- Any implementation ideas you have

### Pull Requests

1. Fork the repository
2. Create a new branch (`git checkout -b feature/amazing-feature`)
3. Make your changes
4. Test your changes thoroughly
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

## Development Setup

### Prerequisites

- Python 3.11 or higher
- Home Assistant development environment
- NTA API key for testing

### Local Development

1. Clone the repository:
```bash
git clone https://github.com/joshS28/north-dublin-dog-walker.git
cd north-dublin-dog-walker
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Copy to your Home Assistant custom_components:
```bash
ln -s $(pwd)/custom_components/dublin_bus ~/.homeassistant/custom_components/dublin_bus
```

4. Restart Home Assistant

### Testing

Before submitting a PR, ensure:
- [ ] Code follows Home Assistant coding standards
- [ ] All Python files pass syntax checks
- [ ] The integration loads without errors
- [ ] Sensors update correctly
- [ ] Configuration flow works
- [ ] No new warnings in logs

### Code Style

- Follow [PEP 8](https://www.python.org/dev/peps/pep-0008/)
- Use type hints where appropriate
- Add docstrings to functions and classes
- Keep functions focused and small
- Use meaningful variable names

### Commit Messages

- Use clear, descriptive commit messages
- Start with a verb (Add, Fix, Update, etc.)
- Reference issue numbers when applicable

Example:
```
Add support for bus route colors (#123)

- Fetch route color from GTFS static data
- Add color attribute to sensor
- Update documentation
```

## Project Structure

```
dublin_bus/
├── custom_components/
│   └── dublin_bus/
│       ├── __init__.py          # Integration setup
│       ├── api.py               # API client
│       ├── config_flow.py       # Configuration UI
│       ├── const.py             # Constants
│       ├── manifest.json        # Integration metadata
│       ├── sensor.py            # Sensor platform
│       ├── strings.json         # UI strings
│       └── translations/
│           └── en.json          # English translations
├── .github/
│   └── workflows/               # CI/CD workflows
├── CHANGELOG.md                 # Version history
├── INSTALLATION.md              # Installation guide
├── LOVELACE_EXAMPLES.md        # Card examples
├── README.md                    # Main documentation
└── requirements.txt             # Python dependencies
```

## Adding New Features

### Adding a New Sensor Attribute

1. Update `api.py` to fetch the new data
2. Modify `sensor.py` to expose the attribute
3. Update documentation
4. Add example usage in LOVELACE_EXAMPLES.md

### Adding Configuration Options

1. Update `const.py` with new constants
2. Modify `config_flow.py` to add UI fields
3. Update `strings.json` and translations
4. Update `__init__.py` to use new options
5. Document in README.md and INSTALLATION.md

## Release Process

Releases are managed by maintainers:

1. Update version in `manifest.json`
2. Update `CHANGELOG.md`
3. Create a git tag: `git tag v1.x.x`
4. Push tag: `git push origin v1.x.x`
5. GitHub Actions will create the release

## Questions?

Feel free to:
- Open an issue for questions
- Start a discussion on GitHub
- Ask in the Home Assistant community forum

## Code of Conduct

Be respectful and constructive. We're all here to make this integration better!

## License

By contributing, you agree that your contributions will be licensed under the MIT License.

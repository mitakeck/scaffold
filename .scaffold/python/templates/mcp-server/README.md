# {{name}} MCP Server

{{description}}

*Generated on {{date}} by {{author}}*

## Overview

This is a Python implementation of a Model Context Protocol (MCP) server that provides {{name}} functionality to Claude and other MCP-compatible clients.

## Features

{{#if tools}}
- **Tools**: Interactive tools for {{name}} operations
{{/if}}
{{#if resources}}
- **Resources**: Access to {{name}} resources
{{/if}}
{{#if prompts}}
- **Prompts**: Pre-configured prompts for {{name}} tasks
{{/if}}
- **Modern Python**: Uses Python {{python_version}} with type hints
- **mise + uv**: Modern Python environment management
- **Structured Logging**: JSON structured logging with structlog
- **Type Safety**: Full type checking with mypy
- **Testing**: Comprehensive test suite with pytest

## Requirements

- Python {{python_version}}+
- [mise](https://mise.jdx.dev/) - Environment management
- [uv](https://docs.astral.sh/uv/) - Package management

## Installation

### Using mise (Recommended)

1. **Install mise and uv**:
```bash
# Install mise
curl https://mise.run | sh
# Or use your package manager

# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh
```

2. **Clone and setup**:
```bash
git clone <repository-url>
cd {{name}}-mcp-server

# Install Python and dependencies
mise install
mise run install
```

### Manual Installation

```bash
# Create virtual environment
python{{python_version}} -m venv venv
source venv/bin/activate

# Install with uv
uv sync --dev
```

## Usage

### With Claude Desktop

Add to your Claude Desktop configuration (`~/Library/Application Support/Claude/claude_desktop_config.json`):

```json
{
  "mcpServers": {
    "{{name}}": {
      "command": "uv",
      "args": ["run", "{{name}}-mcp-server"],
      "cwd": "/path/to/{{name}}-mcp-server",
      "env": {
        "LOG_LEVEL": "INFO"
      }
    }
  }
}
```

### Standalone Testing

```bash
# Run the server
mise run dev

# Or with uv directly
uv run {{name}}-mcp-server

# Run with debug logging
LOG_LEVEL=DEBUG uv run {{name}}-mcp-server
```

## Development

### Setup Development Environment

```bash
# Install all dependencies including dev dependencies
mise run install

# Install pre-commit hooks
mise run install-pre-commit
```

### Available Commands

```bash
# Run tests
mise run test

# Run tests with coverage
mise run test-cov

# Format code
mise run format

# Lint code
mise run lint

# Build package
mise run build

# Clean build artifacts
mise run clean
```

### Code Quality

The project uses several tools for code quality:

- **Black**: Code formatting
- **isort**: Import sorting
- **flake8**: Linting
- **mypy**: Type checking
- **pytest**: Testing

### Testing

```bash
# Run all tests
mise run test

# Run with coverage
mise run test-cov

# Run specific test file
uv run pytest tests/test_main.py

# Run with verbose output
uv run pytest -v
```

## Configuration

The server can be configured through environment variables:

```bash
# Server configuration
MCP_SERVER_NAME={{name}}-mcp-server
MCP_SERVER_VERSION={{version}}
MCP_SERVER_DESCRIPTION={{description}}

# Logging
LOG_LEVEL=INFO

# Custom configuration
# Add your environment variables here
```

## API Reference

{{#if tools}}
### Tools

#### `example_tool`
- **Description**: An example tool for {{name}}
- **Parameters**:
  - `input` (string, required): Input parameter for the tool

**Usage**:
```json
{
  "name": "example_tool",
  "arguments": {
    "input": "Hello, World!"
  }
}
```

**Response**:
```json
{
  "content": [
    {
      "type": "text",
      "text": "Processed: Hello, World!"
    }
  ]
}
```
{{/if}}

{{#if resources}}
### Resources

#### `{{name}}://example`
- **Description**: An example resource for {{name}}
- **MIME Type**: text/plain

**Usage**:
```json
{
  "uri": "{{name}}://example"
}
```

**Response**:
```json
{
  "contents": [
    {
      "type": "text",
      "text": "This is an example resource from {{name}} MCP server"
    }
  ]
}
```
{{/if}}

{{#if prompts}}
### Prompts

#### `example_prompt`
- **Description**: An example prompt for {{name}}
- **Arguments**:
  - `topic` (string, required): Topic for the prompt

**Usage**:
```json
{
  "name": "example_prompt",
  "arguments": {
    "topic": "machine learning"
  }
}
```

**Response**:
```json
{
  "messages": [
    {
      "role": "user",
      "content": {
        "type": "text",
        "text": "Please provide information about: machine learning"
      }
    }
  ]
}
```
{{/if}}

## Error Handling

The server implements proper error handling with detailed logging:

```python
# Example error response
{
  "error": {
    "code": "INVALID_REQUEST",
    "message": "Unknown tool: invalid_tool",
    "data": {
      "tool_name": "invalid_tool",
      "available_tools": ["example_tool"]
    }
  }
}
```

## Deployment

### Docker

```dockerfile
FROM python:{{python_version}}-slim

WORKDIR /app

# Install uv
RUN pip install uv

# Copy project files
COPY . .

# Install dependencies
RUN uv sync --frozen

# Run the server
CMD ["uv", "run", "{{name}}-mcp-server"]
```

### Systemd Service

```ini
[Unit]
Description={{name}} MCP Server
After=network.target

[Service]
Type=simple
User=mcp
WorkingDirectory=/opt/{{name}}-mcp-server
ExecStart=/usr/local/bin/uv run {{name}}-mcp-server
Restart=always
RestartSec=10
Environment=LOG_LEVEL=INFO

[Install]
WantedBy=multi-user.target
```

## Troubleshooting

### Common Issues

1. **Import Errors**:
   - Ensure `PYTHONPATH` includes the `src` directory
   - Check that all dependencies are installed: `uv sync`

2. **Permission Errors**:
   - Ensure the server has appropriate file system permissions
   - Check that the user running the server has access to required resources

3. **Connection Issues**:
   - Verify that the MCP client is configured correctly
   - Check that the server is running on the expected port/socket

### Debug Mode

```bash
# Run with debug logging
LOG_LEVEL=DEBUG uv run {{name}}-mcp-server

# Run with Python debugger
uv run python -m pdb -m {{name}}_mcp_server.main
```

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature/amazing-feature`
3. Make your changes
4. Run tests: `mise run test`
5. Run linting: `mise run lint`
6. Commit your changes: `git commit -m 'Add amazing feature'`
7. Push to the branch: `git push origin feature/amazing-feature`
8. Open a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create an issue in the repository
- Check the MCP documentation: https://modelcontextprotocol.io
- Claude Desktop configuration: https://claude.ai/docs
# {{name}} MCP Server

{{description}}

*Generated on {{date}} by {{author}}*

## Overview

This is a Model Context Protocol (MCP) server that provides {{name}} functionality to Claude and other MCP-compatible clients.

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

## Installation

```bash
npm install
npm run build
```

## Usage

### With Claude Desktop

Add to your Claude Desktop configuration:

```json
{
  "mcpServers": {
    "{{name}}": {
      "command": "node",
      "args": ["path/to/{{name}}-mcp-server/dist/index.js"],
      "env": {
        "NODE_ENV": "production"
      }
    }
  }
}
```

### Standalone Testing

```bash
# Start the server
npm start

# Test with MCP client
npx @modelcontextprotocol/inspector
```

## Development

```bash
# Install dependencies
npm install

# Start development server
npm run dev

# Run tests
npm test

# Lint code
npm run lint

# Format code
npm run format
```

## Configuration

The server can be configured through environment variables:

- `NODE_ENV`: Environment (development/production)
- `LOG_LEVEL`: Logging level (debug/info/warn/error)

## API Reference

{{#if tools}}
### Tools

#### `example_tool`
- **Description**: An example tool for {{name}}
- **Parameters**:
  - `input` (string, required): Input parameter

**Example**:
```json
{
  "name": "example_tool",
  "arguments": {
    "input": "Hello World"
  }
}
```
{{/if}}

{{#if resources}}
### Resources

#### `example://resource`
- **Description**: An example resource for {{name}}
- **MIME Type**: text/plain

**Example**:
```json
{
  "uri": "example://resource"
}
```
{{/if}}

{{#if prompts}}
### Prompts

#### `example_prompt`
- **Description**: An example prompt for {{name}}
- **Arguments**:
  - `topic` (string, required): Topic to generate prompt for

**Example**:
```json
{
  "name": "example_prompt",
  "arguments": {
    "topic": "machine learning"
  }
}
```
{{/if}}

## Error Handling

The server implements proper error handling with MCP error codes:

- `MethodNotFound`: Unknown tool/prompt/resource
- `InvalidRequest`: Malformed request
- `InternalError`: Server internal errors

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests
5. Submit a pull request

## License

MIT License - see LICENSE file for details.

## Support

For issues and questions:
- Create an issue in the repository
- Check the MCP documentation: https://modelcontextprotocol.io
- Claude Desktop configuration: https://claude.ai/docs
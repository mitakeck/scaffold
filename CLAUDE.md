# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Universal Scaffold Tool, a cross-platform code generation tool written in Go that provides Rails/Laravel-style scaffolding for any technology stack. The tool uses plain text templates and TOML configuration to generate files with variable expansion.

## Development Setup

### Build and Run
```bash
# Use mise for Go version management
mise install
mise exec -- go build -o scaffold main.go

# Or with mise activated in shell
go build -o scaffold main.go
```

### Testing the Tool
```bash
# List available templates
./scaffold list

# Show template details
./scaffold info [template-name]

# Generate files from template
./scaffold generate [template] [namespace] [domain] [name] [key=value...]

# Example C# UseCase generation
./scaffold generate csharp-usecase Application Users CreateUser author="Developer Name"
```

## Architecture

### Core Components

**ScaffoldTool struct** (`main.go`): Main application logic
- `loadConfig()`: Searches for `.scaffold.toml` in order: current dir, home dir, `~/.config/scaffold/`
- `expandVariables()`: Template variable expansion with `{{variable}}` syntax
- `generateTemplate()`: File generation with directory creation and overwrite protection

**Configuration System**: TOML-based template definitions
- **Template structure**: `required_args`, `optional_args`, `files` mapping
- **Variable expansion**: Special vars (`{{current_date}}`, `{{current_time}}`, `{{current_datetime}}`) + user-defined
- **File generation**: Source templates → destination paths with variable substitution

### Template Architecture

Templates are organized by technology stack in `templates/` directory:
- `templates/csharp/` - C#/.NET Domain-Driven Design patterns
- `templates/react/` - React TypeScript components
- `templates/go/` - Go services
- `templates/mvc/` - ASP.NET MVC

### C# Templates Design Pattern

C# templates follow Domain-Driven Design and Clean Architecture principles:

**Argument Order**: All C# templates use consistent pattern: `namespace domain name [additional-args...]`
- `csharp-usecase`: `namespace domain name` → Generates UseCase, Request, Response
- `csharp-entity`: `namespace domain name` → Domain entity with DDD patterns
- `csharp-valueobject`: `namespace domain name` → Record-based value objects
- `csharp-repository`: `namespace domain entity` → Interface + Implementation
- `csharp-exception`: `namespace domain code name` → Domain exception with error codes
- `csharp-webapi-controller`: `namespace domain name` → REST API controller

**Directory Structure Generated**:
```
{namespace}/
├── {domain}/
│   ├── Usecases/{name}/     # UseCase pattern
│   ├── Entities/            # Domain entities
│   ├── ValueObjects/        # Value objects
│   ├── Repositories/        # Repository interfaces
│   └── Exceptions/          # Domain exceptions
└── Infrastructure/{domain}/Repositories/  # Repository implementations
```

### Configuration File Structure

`.scaffold.toml` defines templates with:
- `required_args`: Positional arguments (order matters)
- `optional_args`: Key=value arguments with defaults
- `files`: Source template → destination mapping with variable expansion

Variable expansion supports:
- User arguments: `{{namespace}}`, `{{domain}}`, `{{name}}`
- Special variables: `{{current_date}}`, `{{current_time}}`, `{{current_datetime}}`
- Optional arguments with defaults: `{{author}}`, `{{date}}`

## Key Implementation Details

### Template Variable System
- Uses regex `\{\{(\w+)\}\}` for variable matching
- Variables resolved in order: special vars, user args, optional args with defaults
- File paths and content both support variable expansion

### File Generation Process
1. Parse command-line arguments (positional + key=value)
2. Load and validate template configuration
3. Build variable map from arguments + defaults
4. For each template file: read source, expand variables, write to destination
5. Directory creation and overwrite protection included

### Dependencies
- `github.com/BurntSushi/toml` - TOML configuration parsing
- `github.com/spf13/cobra` - CLI framework
- Go 1.23+ managed via mise (`.mise.toml`)

## Template Development

When adding new templates:
1. Add template definition to `.scaffold.toml`
2. Create template files in `templates/{category}/`
3. Use consistent argument ordering (namespace first for C# templates)
4. Include variable expansion for dynamic content
5. Follow existing patterns for file organization

Template files support full variable expansion in both file content and destination paths. Use `{{variable}}` syntax for all substitutions.
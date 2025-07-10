# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

This is the Universal Scaffold Tool, a cross-platform code generation tool written in Go that provides Rails/Laravel-style scaffolding for any technology stack. The tool uses a hierarchical category-based structure with plain text templates and TOML configuration to generate files with variable expansion.

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
# List available categories
./scaffold

# List templates in a category
./scaffold <category> list

# Show template details
./scaffold <category> info <template>

# Generate files from template
./scaffold <category> <template> [args...] [key=value...]

# Examples
./scaffold csharp usecase Application Users CreateUser author="Developer Name"
./scaffold web react-component UserProfile
./scaffold devtools makefile-advanced my-project type=node
./scaffold ai claude-multiagent my-team
./scaffold go service UserService internal/services
```

## Architecture

### Core Components

**ScaffoldTool struct** (`main.go`): Main application logic
- `findScaffoldDir()`: Searches for `.scaffold/` directory in order: current dir, home dir, `~/.config/scaffold/`
- `loadConfig(category)`: Loads category-specific `.scaffold.toml` configuration
- `expandVariables()`: Template variable expansion with `{{variable}}` syntax
- `generateTemplate()`: File generation with directory creation and overwrite protection

**Configuration System**: Hierarchical TOML-based template definitions
- **Category structure**: Each category has its own `.scaffold.toml` and `templates/` directory
- **Template structure**: `required_args`, `optional_args`, `files` mapping
- **Variable expansion**: Special vars (`{{current_date}}`, `{{current_time}}`, `{{current_datetime}}`) + user-defined
- **File generation**: Source templates → destination paths with variable substitution

### Template Architecture

Templates are organized by category in `.scaffold/` directory:

```
.scaffold/
├── csharp/          # C#/.NET Domain-Driven Design patterns
│   ├── .scaffold.toml
│   └── templates/
├── web/             # React TypeScript & Vite templates
│   ├── .scaffold.toml
│   └── templates/
├── devtools/        # Makefile & GitHub Actions CI/CD
│   ├── .scaffold.toml
│   └── templates/
├── ai/              # Claude Code development tools
│   ├── .scaffold.toml
│   └── templates/
└── go/              # Go service patterns
    ├── .scaffold.toml
    └── templates/
```

### Template Categories

#### C# (.NET) Category (`csharp`)
Domain-Driven Design and Clean Architecture patterns:

**Argument Order**: All C# templates use consistent pattern: `namespace domain name [additional-args...]`
- `usecase`: `namespace domain name` → Generates UseCase, Request, Response
- `entity`: `namespace domain name` → Domain entity with DDD patterns
- `valueobject`: `namespace domain name` → Record-based value objects
- `repository`: `namespace domain entity` → Interface + Implementation
- `exception`: `namespace domain code name` → Domain exception with error codes
- `webapi-controller`: `namespace domain name` → REST API controller

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

#### Web Development Category (`web`)
Modern frontend development patterns:
- `react-component`: React TypeScript component with tests
- `vite-react-ts`: Complete Vite + React + TypeScript project setup

#### Development Tools Category (`devtools`)
Development efficiency tools:
- `makefile-advanced`: Self-documenting Makefile with colored output and task grouping
- `github-actions-ci`: Multi-language CI/CD workflows (node, go, python, dotnet)

#### AI Development Category (`ai`)
Claude Code integration and AI development tools:
- `claude-commands`: Custom slash commands for Claude Code
- `claude-project-init`: AI-powered project initialization with CLAUDE.md
- `claude-multiagent`: tmux-based multi-agent communication system

#### Go Development Category (`go`)
Go service patterns:
- `service`: Go service with interface, implementation, and tests

### Configuration File Structure

Each category has its own `.scaffold.toml` defining templates with:
- `required_args`: Positional arguments (order matters)
- `optional_args`: Key=value arguments with defaults
- `files`: Source template → destination mapping with variable expansion

Variable expansion supports:
- User arguments: `{{namespace}}`, `{{domain}}`, `{{name}}`
- Special variables: `{{current_date}}`, `{{current_time}}`, `{{current_datetime}}`
- Optional arguments with defaults: `{{author}}`, `{{date}}`

## Key Implementation Details

### Hierarchical Category System
- Categories are discovered by scanning `.scaffold/` directory for subdirectories containing `.scaffold.toml`
- Each category is loaded independently with its own configuration and templates
- Template file paths are resolved relative to the category directory

### Template Variable System
- Uses regex `\{\{(\w+)\}\}` for variable matching
- Variables resolved in order: special vars, user args, optional args with defaults
- File paths and content both support variable expansion

### File Generation Process
1. Parse command-line arguments (category, template, positional + key=value)
2. Load category-specific template configuration
3. Build variable map from arguments + defaults
4. For each template file: read source, expand variables, write to destination
5. Directory creation and overwrite protection included

### Dependencies
- `github.com/BurntSushi/toml` - TOML configuration parsing
- `github.com/spf13/cobra` - CLI framework
- Go 1.23+ managed via mise (`.mise.toml`)

## Template Development

When adding new templates:

### Adding to Existing Category
1. Add template definition to `.scaffold/{category}/.scaffold.toml`
2. Create template files in `.scaffold/{category}/templates/`
3. Use consistent argument ordering (namespace first for C# templates)
4. Include variable expansion for dynamic content
5. Follow existing patterns for file organization

### Creating New Category
1. Create `.scaffold/{new-category}/` directory
2. Add `.scaffold/{new-category}/.scaffold.toml` with template definitions
3. Create `.scaffold/{new-category}/templates/` directory with template files
4. Follow naming conventions and patterns from existing categories

Template files support full variable expansion in both file content and destination paths. Use `{{variable}}` syntax for all substitutions.

## Testing Templates

Always test new templates across different scenarios:
```bash
# Test basic generation
./scaffold {category} {template} [required-args...]

# Test with optional arguments
./scaffold {category} {template} [required-args...] author="Test Author"

# Test file overwrite protection
./scaffold {category} {template} [required-args...]  # Run twice
```

## CI/CD Integration

The project includes GitHub Actions workflows:
- `build.yml`: Multi-platform builds and testing
- `release.yml`: Automated releases with cross-platform binaries

Templates are excluded from Go testing to avoid syntax errors during CI builds.
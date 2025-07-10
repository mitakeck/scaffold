#!/usr/bin/env python3
"""
{{name}} MCP Server
{{description}}

Generated on {{date}} by {{author}}
"""

import asyncio
import logging
import os
from typing import Any, Dict, List, Optional, Sequence

import click
import structlog
from dotenv import load_dotenv
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import (
    CallToolResult,
    GetPromptResult,
    ListPromptsResult,
    ListResourcesResult,
    ListToolsResult,
    PromptMessage,
    ReadResourceResult,
    Resource,
    Tool,
    TextContent,
    Prompt,
    PromptArgument,
)
from pydantic import BaseModel, Field

# Load environment variables
load_dotenv()

# Configure structured logging
structlog.configure(
    processors=[
        structlog.stdlib.filter_by_level,
        structlog.stdlib.add_logger_name,
        structlog.stdlib.add_log_level,
        structlog.stdlib.PositionalArgumentsFormatter(),
        structlog.processors.TimeStamper(fmt="iso"),
        structlog.processors.StackInfoRenderer(),
        structlog.processors.format_exc_info,
        structlog.processors.UnicodeDecoder(),
        structlog.processors.JSONRenderer(),
    ],
    context_class=dict,
    logger_factory=structlog.stdlib.LoggerFactory(),
    wrapper_class=structlog.stdlib.BoundLogger,
    cache_logger_on_first_use=True,
)

logger = structlog.get_logger()


class ServerConfig(BaseModel):
    """Server configuration model."""
    name: str = Field(default="{{name}}-mcp-server")
    version: str = Field(default="{{version}}")
    description: str = Field(default="{{description}}")
    log_level: str = Field(default="INFO")
    

class {{name | title}}McpServer:
    """{{name}} MCP Server implementation."""
    
    def __init__(self, config: ServerConfig):
        self.config = config
        self.server = Server(name=config.name, version=config.version)
        self.logger = logger.bind(server=config.name)
        
        # Setup handlers
        self._setup_handlers()
        
    def _setup_handlers(self) -> None:
        """Setup MCP server handlers."""
        {{#if tools}}
        # Tools
        self.server.list_tools = self._list_tools
        self.server.call_tool = self._call_tool
        {{/if}}
        
        {{#if resources}}
        # Resources
        self.server.list_resources = self._list_resources
        self.server.read_resource = self._read_resource
        {{/if}}
        
        {{#if prompts}}
        # Prompts
        self.server.list_prompts = self._list_prompts
        self.server.get_prompt = self._get_prompt
        {{/if}}
        
        self.logger.info("MCP server handlers configured")
    
    {{#if tools}}
    async def _list_tools(self) -> ListToolsResult:
        """List available tools."""
        tools = [
            Tool(
                name="example_tool",
                description="An example tool for {{name}}",
                inputSchema={
                    "type": "object",
                    "properties": {
                        "input": {
                            "type": "string",
                            "description": "Input parameter for the tool"
                        }
                    },
                    "required": ["input"]
                }
            )
        ]
        
        self.logger.info("Listed tools", count=len(tools))
        return ListToolsResult(tools=tools)
    
    async def _call_tool(self, name: str, arguments: Dict[str, Any]) -> CallToolResult:
        """Call a tool."""
        self.logger.info("Tool called", tool_name=name, arguments=arguments)
        
        if name == "example_tool":
            return await self._handle_example_tool(arguments)
        else:
            raise ValueError(f"Unknown tool: {name}")
    
    async def _handle_example_tool(self, arguments: Dict[str, Any]) -> CallToolResult:
        """Handle example tool call."""
        input_value = arguments.get("input", "")
        result = f"Processed: {input_value}"
        
        self.logger.info("Example tool executed", input=input_value, result=result)
        
        return CallToolResult(
            content=[
                TextContent(
                    type="text",
                    text=result
                )
            ]
        )
    {{/if}}
    
    {{#if resources}}
    async def _list_resources(self) -> ListResourcesResult:
        """List available resources."""
        resources = [
            Resource(
                uri="{{name}}://example",
                name="Example Resource",
                description="An example resource for {{name}}",
                mimeType="text/plain"
            )
        ]
        
        self.logger.info("Listed resources", count=len(resources))
        return ListResourcesResult(resources=resources)
    
    async def _read_resource(self, uri: str) -> ReadResourceResult:
        """Read a resource."""
        self.logger.info("Resource read", uri=uri)
        
        if uri == "{{name}}://example":
            return ReadResourceResult(
                contents=[
                    TextContent(
                        type="text",
                        text="This is an example resource from {{name}} MCP server"
                    )
                ]
            )
        else:
            raise ValueError(f"Unknown resource: {uri}")
    {{/if}}
    
    {{#if prompts}}
    async def _list_prompts(self) -> ListPromptsResult:
        """List available prompts."""
        prompts = [
            Prompt(
                name="example_prompt",
                description="An example prompt for {{name}}",
                arguments=[
                    PromptArgument(
                        name="topic",
                        description="Topic for the prompt",
                        required=True
                    )
                ]
            )
        ]
        
        self.logger.info("Listed prompts", count=len(prompts))
        return ListPromptsResult(prompts=prompts)
    
    async def _get_prompt(self, name: str, arguments: Dict[str, Any]) -> GetPromptResult:
        """Get a prompt."""
        self.logger.info("Prompt requested", prompt_name=name, arguments=arguments)
        
        if name == "example_prompt":
            topic = arguments.get("topic", "general")
            return GetPromptResult(
                messages=[
                    PromptMessage(
                        role="user",
                        content=TextContent(
                            type="text",
                            text=f"Please provide information about: {topic}"
                        )
                    )
                ]
            )
        else:
            raise ValueError(f"Unknown prompt: {name}")
    {{/if}}
    
    async def run(self) -> None:
        """Run the MCP server."""
        self.logger.info("Starting MCP server", config=self.config.dict())
        
        try:
            async with stdio_server() as (read_stream, write_stream):
                await self.server.run(
                    read_stream=read_stream,
                    write_stream=write_stream,
                    initialization_options={}
                )
        except Exception as e:
            self.logger.error("Server error", error=str(e), exc_info=True)
            raise
        finally:
            self.logger.info("MCP server stopped")


def create_config() -> ServerConfig:
    """Create server configuration from environment variables."""
    return ServerConfig(
        name=os.getenv("MCP_SERVER_NAME", "{{name}}-mcp-server"),
        version=os.getenv("MCP_SERVER_VERSION", "{{version}}"),
        description=os.getenv("MCP_SERVER_DESCRIPTION", "{{description}}"),
        log_level=os.getenv("LOG_LEVEL", "INFO"),
    )


@click.command()
@click.option(
    "--log-level",
    default="INFO",
    help="Log level (DEBUG, INFO, WARNING, ERROR, CRITICAL)",
)
@click.option(
    "--config-file",
    type=click.Path(exists=True),
    help="Path to configuration file",
)
def main(log_level: str, config_file: Optional[str]) -> None:
    """Run the {{name}} MCP server."""
    # Set up logging
    logging.basicConfig(level=getattr(logging, log_level.upper()))
    
    # Create configuration
    config = create_config()
    config.log_level = log_level
    
    # Create and run server
    server = {{name | title}}McpServer(config)
    
    try:
        asyncio.run(server.run())
    except KeyboardInterrupt:
        logger.info("Server stopped by user")
    except Exception as e:
        logger.error("Server failed", error=str(e), exc_info=True)
        raise


if __name__ == "__main__":
    main()
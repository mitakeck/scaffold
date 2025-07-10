"""
Tests for {{name}} MCP Server
Generated on {{date}} by {{author}}
"""

import pytest
from unittest.mock import AsyncMock, MagicMock, patch

from {{name}}_mcp_server.main import {{name | title}}McpServer, ServerConfig, create_config


class TestServerConfig:
    """Test ServerConfig model."""
    
    def test_default_config(self):
        """Test default configuration."""
        config = ServerConfig()
        assert config.name == "{{name}}-mcp-server"
        assert config.version == "{{version}}"
        assert config.description == "{{description}}"
        assert config.log_level == "INFO"
    
    def test_custom_config(self):
        """Test custom configuration."""
        config = ServerConfig(
            name="custom-server",
            version="1.0.0",
            description="Custom description",
            log_level="DEBUG"
        )
        assert config.name == "custom-server"
        assert config.version == "1.0.0"
        assert config.description == "Custom description"
        assert config.log_level == "DEBUG"


class TestCreateConfig:
    """Test create_config function."""
    
    def test_create_config_default(self):
        """Test create_config with default values."""
        config = create_config()
        assert config.name == "{{name}}-mcp-server"
        assert config.version == "{{version}}"
        assert config.description == "{{description}}"
        assert config.log_level == "INFO"
    
    @patch.dict('os.environ', {
        'MCP_SERVER_NAME': 'test-server',
        'MCP_SERVER_VERSION': '2.0.0',
        'MCP_SERVER_DESCRIPTION': 'Test description',
        'LOG_LEVEL': 'DEBUG'
    })
    def test_create_config_from_env(self):
        """Test create_config with environment variables."""
        config = create_config()
        assert config.name == "test-server"
        assert config.version == "2.0.0"
        assert config.description == "Test description"
        assert config.log_level == "DEBUG"


class Test{{name | title}}McpServer:
    """Test {{name | title}}McpServer class."""
    
    def setup_method(self):
        """Setup test fixtures."""
        self.config = ServerConfig()
        self.server = {{name | title}}McpServer(self.config)
    
    def test_init(self):
        """Test server initialization."""
        assert self.server.config == self.config
        assert self.server.server.name == self.config.name
        assert self.server.server.version == self.config.version
        assert self.server.logger is not None
    
    {{#if tools}}
    @pytest.mark.asyncio
    async def test_list_tools(self):
        """Test listing tools."""
        result = await self.server._list_tools()
        assert len(result.tools) > 0
        assert any(tool.name == "example_tool" for tool in result.tools)
    
    @pytest.mark.asyncio
    async def test_call_tool_example(self):
        """Test calling example tool."""
        arguments = {"input": "test input"}
        result = await self.server._call_tool("example_tool", arguments)
        assert len(result.content) == 1
        assert "Processed: test input" in result.content[0].text
    
    @pytest.mark.asyncio
    async def test_call_tool_unknown(self):
        """Test calling unknown tool."""
        with pytest.raises(ValueError, match="Unknown tool: unknown_tool"):
            await self.server._call_tool("unknown_tool", {})
    
    @pytest.mark.asyncio
    async def test_handle_example_tool(self):
        """Test handling example tool."""
        arguments = {"input": "hello world"}
        result = await self.server._handle_example_tool(arguments)
        assert len(result.content) == 1
        assert result.content[0].text == "Processed: hello world"
    {{/if}}
    
    {{#if resources}}
    @pytest.mark.asyncio
    async def test_list_resources(self):
        """Test listing resources."""
        result = await self.server._list_resources()
        assert len(result.resources) > 0
        assert any(resource.uri == "{{name}}://example" for resource in result.resources)
    
    @pytest.mark.asyncio
    async def test_read_resource_example(self):
        """Test reading example resource."""
        result = await self.server._read_resource("{{name}}://example")
        assert len(result.contents) == 1
        assert "example resource" in result.contents[0].text.lower()
    
    @pytest.mark.asyncio
    async def test_read_resource_unknown(self):
        """Test reading unknown resource."""
        with pytest.raises(ValueError, match="Unknown resource: unknown://resource"):
            await self.server._read_resource("unknown://resource")
    {{/if}}
    
    {{#if prompts}}
    @pytest.mark.asyncio
    async def test_list_prompts(self):
        """Test listing prompts."""
        result = await self.server._list_prompts()
        assert len(result.prompts) > 0
        assert any(prompt.name == "example_prompt" for prompt in result.prompts)
    
    @pytest.mark.asyncio
    async def test_get_prompt_example(self):
        """Test getting example prompt."""
        arguments = {"topic": "machine learning"}
        result = await self.server._get_prompt("example_prompt", arguments)
        assert len(result.messages) == 1
        assert "machine learning" in result.messages[0].content.text
    
    @pytest.mark.asyncio
    async def test_get_prompt_unknown(self):
        """Test getting unknown prompt."""
        with pytest.raises(ValueError, match="Unknown prompt: unknown_prompt"):
            await self.server._get_prompt("unknown_prompt", {})
    {{/if}}
    
    @pytest.mark.asyncio
    async def test_run_server(self):
        """Test running the server."""
        # Mock the stdio_server and server.run
        with patch('{{name}}_mcp_server.main.stdio_server') as mock_stdio:
            mock_context = AsyncMock()
            mock_stdio.return_value.__aenter__.return_value = (
                MagicMock(), MagicMock()
            )
            
            # Mock the server.run method
            self.server.server.run = AsyncMock()
            
            # Run the server
            await self.server.run()
            
            # Verify that the server.run was called
            self.server.server.run.assert_called_once()


class TestIntegration:
    """Integration tests."""
    
    @pytest.mark.asyncio
    async def test_server_lifecycle(self):
        """Test complete server lifecycle."""
        config = ServerConfig(
            name="test-server",
            version="1.0.0",
            description="Test server",
            log_level="DEBUG"
        )
        
        server = {{name | title}}McpServer(config)
        
        # Test that server is properly initialized
        assert server.config.name == "test-server"
        assert server.server.name == "test-server"
        assert server.server.version == "1.0.0"
        
        {{#if tools}}
        # Test tools functionality
        tools = await server._list_tools()
        assert len(tools.tools) > 0
        
        # Test calling a tool
        result = await server._call_tool("example_tool", {"input": "test"})
        assert len(result.content) > 0
        {{/if}}
        
        {{#if resources}}
        # Test resources functionality
        resources = await server._list_resources()
        assert len(resources.resources) > 0
        
        # Test reading a resource
        result = await server._read_resource("{{name}}://example")
        assert len(result.contents) > 0
        {{/if}}
        
        {{#if prompts}}
        # Test prompts functionality
        prompts = await server._list_prompts()
        assert len(prompts.prompts) > 0
        
        # Test getting a prompt
        result = await server._get_prompt("example_prompt", {"topic": "test"})
        assert len(result.messages) > 0
        {{/if}}


if __name__ == "__main__":
    pytest.main([__file__])
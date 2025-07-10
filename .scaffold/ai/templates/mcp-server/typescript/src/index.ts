#!/usr/bin/env node
/**
 * {{name}} MCP Server
 * {{description}}
 * 
 * Generated on {{date}} by {{author}}
 */

import { Server } from '@modelcontextprotocol/sdk/server/index.js';
import { StdioServerTransport } from '@modelcontextprotocol/sdk/server/stdio.js';
import {
  CallToolRequestSchema,
  ErrorCode,
  ListToolsRequestSchema,
  McpError,
} from '@modelcontextprotocol/sdk/types.js';
import { z } from 'zod';

interface ServerConfig {
  name: string;
  version: string;
  description: string;
}

class {{name | title}}McpServer {
  private server: Server;
  private config: ServerConfig;

  constructor() {
    this.config = {
      name: '{{name}}-mcp-server',
      version: '{{version}}',
      description: '{{description}}',
    };

    this.server = new Server(
      {
        name: this.config.name,
        version: this.config.version,
      },
      {
        capabilities: {
          {{#if tools}}
          tools: {},
          {{/if}}
          {{#if resources}}
          resources: {},
          {{/if}}
          {{#if prompts}}
          prompts: {},
          {{/if}}
        },
      }
    );

    this.setupHandlers();
  }

  private setupHandlers(): void {
    {{#if tools}}
    // List available tools
    this.server.setRequestHandler(ListToolsRequestSchema, async () => {
      return {
        tools: [
          {
            name: 'example_tool',
            description: 'An example tool for {{name}}',
            inputSchema: {
              type: 'object',
              properties: {
                input: {
                  type: 'string',
                  description: 'Input parameter',
                },
              },
              required: ['input'],
            },
          },
        ],
      };
    });

    // Handle tool calls
    this.server.setRequestHandler(CallToolRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case 'example_tool':
          return this.handleExampleTool(args);
        default:
          throw new McpError(
            ErrorCode.MethodNotFound,
            `Unknown tool: ${name}`
          );
      }
    });
    {{/if}}

    {{#if resources}}
    // List available resources
    this.server.setRequestHandler(ListResourcesRequestSchema, async () => {
      return {
        resources: [
          {
            uri: 'example://resource',
            name: 'Example Resource',
            description: 'An example resource for {{name}}',
            mimeType: 'text/plain',
          },
        ],
      };
    });

    // Handle resource reads
    this.server.setRequestHandler(ReadResourceRequestSchema, async (request) => {
      const { uri } = request.params;
      
      switch (uri) {
        case 'example://resource':
          return {
            contents: [
              {
                uri,
                mimeType: 'text/plain',
                text: 'This is an example resource from {{name}} MCP server',
              },
            ],
          };
        default:
          throw new McpError(
            ErrorCode.InvalidRequest,
            `Unknown resource: ${uri}`
          );
      }
    });
    {{/if}}

    {{#if prompts}}
    // List available prompts
    this.server.setRequestHandler(ListPromptsRequestSchema, async () => {
      return {
        prompts: [
          {
            name: 'example_prompt',
            description: 'An example prompt for {{name}}',
            arguments: [
              {
                name: 'topic',
                description: 'Topic to generate prompt for',
                required: true,
              },
            ],
          },
        ],
      };
    });

    // Handle prompt gets
    this.server.setRequestHandler(GetPromptRequestSchema, async (request) => {
      const { name, arguments: args } = request.params;

      switch (name) {
        case 'example_prompt':
          return this.handleExamplePrompt(args);
        default:
          throw new McpError(
            ErrorCode.MethodNotFound,
            `Unknown prompt: ${name}`
          );
      }
    });
    {{/if}}
  }

  {{#if tools}}
  private async handleExampleTool(args: any): Promise<any> {
    const schema = z.object({
      input: z.string(),
    });

    const parsed = schema.parse(args);
    
    // Implement your tool logic here
    const result = `Processed input: ${parsed.input}`;
    
    return {
      content: [
        {
          type: 'text',
          text: result,
        },
      ],
    };
  }
  {{/if}}

  {{#if prompts}}
  private async handleExamplePrompt(args: any): Promise<any> {
    const schema = z.object({
      topic: z.string(),
    });

    const parsed = schema.parse(args);
    
    return {
      messages: [
        {
          role: 'user',
          content: {
            type: 'text',
            text: `Generate content about: ${parsed.topic}`,
          },
        },
      ],
    };
  }
  {{/if}}

  public async run(): Promise<void> {
    const transport = new StdioServerTransport();
    await this.server.connect(transport);
    
    console.error(`{{name}} MCP Server v${this.config.version} started`);
    console.error(`Description: ${this.config.description}`);
  }
}

// Start the server
const server = new {{name | title}}McpServer();
server.run().catch((error) => {
  console.error('Server error:', error);
  process.exit(1);
});
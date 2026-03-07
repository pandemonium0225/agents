import mcp
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters
from agents import FunctionTool
import json

params = StdioServerParameters(command="uv", args=["run", "pdf_server.py"], env=None)


async def list_pdf_tools():
    """List all available tools from the PDF MCP server."""
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            tools_result = await session.list_tools()
            return tools_result.tools


async def call_pdf_tool(tool_name, tool_args):
    """Call a specific tool on the PDF MCP server."""
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.call_tool(tool_name, tool_args)
            return result


async def read_pdf_info_resource(file_path: str):
    """Read PDF info resource from the MCP server."""
    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            result = await session.read_resource(f"pdf://info/{file_path}")
            return result.contents[0].text


async def get_pdf_tools_openai():
    """Convert MCP tools to OpenAI Agents SDK FunctionTools."""
    openai_tools = []
    for tool in await list_pdf_tools():
        schema = {**tool.inputSchema, "additionalProperties": False}
        openai_tool = FunctionTool(
            name=tool.name,
            description=tool.description,
            params_json_schema=schema,
            on_invoke_tool=lambda ctx, args, toolname=tool.name: call_pdf_tool(toolname, json.loads(args))
        )
        openai_tools.append(openai_tool)
    return openai_tools

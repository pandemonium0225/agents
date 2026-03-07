"""
直接呼叫 MCP 工具的低階封裝範例
不透過 Agent，直接使用 stdio_client 呼叫 PDF Server 的工具
"""

import asyncio
import mcp
from mcp.client.stdio import stdio_client
from mcp import StdioServerParameters

# MCP Server 啟動參數
params = StdioServerParameters(
    command="uv",
    args=["run", "pdf_server.py"],
    env=None
)


async def demo_list_tools():
    """列出所有可用的工具"""
    print("=" * 50)
    print("1. 列出所有工具")
    print("=" * 50)

    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()
            tools = await session.list_tools()

            for tool in tools.tools:
                print(f"\n工具名稱: {tool.name}")
                print(f"說明: {tool.description}")
                print(f"參數: {tool.inputSchema}")


async def demo_call_tool():
    """直接呼叫工具"""
    print("\n" + "=" * 50)
    print("2. 直接呼叫工具")
    print("=" * 50)

    # 測試用的 PDF 檔案路徑（請替換成實際存在的檔案）
    test_pdf = "me/linkedin.pdf"

    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()

            # 呼叫 get_pdf_info 工具
            print(f"\n呼叫 get_pdf_info('{test_pdf}'):")
            result = await session.call_tool("get_pdf_info", {"file_path": test_pdf})
            print(f"結果: {result.content}")

            # 呼叫 extract_pdf_text 工具（只取第 1 頁）
            print(f"\n呼叫 extract_pdf_text('{test_pdf}', page_number=1):")
            result = await session.call_tool("extract_pdf_text", {
                "file_path": test_pdf,
                "page_number": 1
            })
            # 只顯示前 500 字
            text = result.content[0].text if result.content else "無內容"
            print(f"結果（前 500 字）: {text[:500]}...")

            # 呼叫 search_pdf 工具
            keyword = "experience"
            print(f"\n呼叫 search_pdf('{test_pdf}', keyword='{keyword}'):")
            result = await session.call_tool("search_pdf", {
                "file_path": test_pdf,
                "keyword": keyword
            })
            print(f"結果: {result.content}")


async def demo_read_resource():
    """讀取 Resource"""
    print("\n" + "=" * 50)
    print("3. 讀取 Resource")
    print("=" * 50)

    test_pdf = "me/linkedin.pdf"

    async with stdio_client(params) as streams:
        async with mcp.ClientSession(*streams) as session:
            await session.initialize()

            # 讀取 PDF info resource
            print(f"\n讀取 resource: pdf://info/{test_pdf}")
            result = await session.read_resource(f"pdf://info/{test_pdf}")
            print(f"結果:\n{result.contents[0].text}")


async def main():
    """主程式"""
    print("\n🔧 MCP 低階封裝範例 - 直接呼叫工具\n")

    await demo_list_tools()
    await demo_call_tool()
    await demo_read_resource()

    print("\n" + "=" * 50)
    print("✅ 範例執行完成")
    print("=" * 50)


if __name__ == "__main__":
    asyncio.run(main())

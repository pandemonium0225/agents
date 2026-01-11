from mcp.server.fastmcp import FastMCP
from datetime import datetime

mcp = FastMCP("date_server")


@mcp.tool()
async def get_current_date() -> str:
    """Get the current date in YYYY-MM-DD format.

    Returns:
        The current date as a string.
    """
    return datetime.now().strftime("%Y-%m-%d")


@mcp.tool()
async def get_current_datetime() -> str:
    """Get the current date and time in YYYY-MM-DD HH:MM:SS format.

    Returns:
        The current date and time as a string.
    """
    return datetime.now().strftime("%Y-%m-%d %H:%M:%S")


@mcp.resource("date://today")
async def read_today_resource() -> str:
    """Resource that provides today's date."""
    return f"Today is {datetime.now().strftime('%Y-%m-%d')}"


if __name__ == "__main__":
    mcp.run(transport='stdio')

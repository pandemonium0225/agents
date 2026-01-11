from mcp.server.fastmcp import FastMCP
import pypdf
import os

mcp = FastMCP("pdf_server")


@mcp.tool()
async def get_pdf_info(file_path: str) -> dict:
    """Get metadata and basic information about a PDF file.

    Args:
        file_path: The path to the PDF file.

    Returns:
        A dictionary containing PDF metadata (title, author, pages, etc.)
    """
    if not os.path.exists(file_path):
        return {"error": f"File not found: {file_path}"}

    try:
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            metadata = reader.metadata

            return {
                "file_path": file_path,
                "num_pages": len(reader.pages),
                "title": metadata.title if metadata else None,
                "author": metadata.author if metadata else None,
                "subject": metadata.subject if metadata else None,
                "creator": metadata.creator if metadata else None,
            }
    except Exception as e:
        return {"error": str(e)}


@mcp.tool()
async def extract_pdf_text(file_path: str, page_number: int = None) -> str:
    """Extract text content from a PDF file.

    Args:
        file_path: The path to the PDF file.
        page_number: Optional specific page number to extract (1-indexed).
                     If not provided, extracts all pages.

    Returns:
        The extracted text content from the PDF.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"

    try:
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            total_pages = len(reader.pages)

            if page_number is not None:
                if page_number < 1 or page_number > total_pages:
                    return f"Error: Page {page_number} out of range. PDF has {total_pages} pages."

                page = reader.pages[page_number - 1]
                return f"=== Page {page_number} ===\n{page.extract_text()}"

            # Extract all pages
            text_content = []
            for i, page in enumerate(reader.pages, 1):
                page_text = page.extract_text()
                text_content.append(f"=== Page {i} ===\n{page_text}")

            return "\n\n".join(text_content)

    except Exception as e:
        return f"Error: {str(e)}"


@mcp.tool()
async def search_pdf(file_path: str, keyword: str) -> str:
    """Search for a keyword in a PDF file and return matching pages.

    Args:
        file_path: The path to the PDF file.
        keyword: The keyword to search for (case-insensitive).

    Returns:
        Pages containing the keyword with surrounding context.
    """
    if not os.path.exists(file_path):
        return f"Error: File not found: {file_path}"

    try:
        with open(file_path, "rb") as f:
            reader = pypdf.PdfReader(f)
            results = []

            for i, page in enumerate(reader.pages, 1):
                text = page.extract_text()
                if keyword.lower() in text.lower():
                    # Find the context around the keyword
                    lines = text.split('\n')
                    matching_lines = [
                        line.strip() for line in lines
                        if keyword.lower() in line.lower()
                    ]
                    results.append(f"=== Page {i} ===\n" + "\n".join(matching_lines[:5]))

            if not results:
                return f"No matches found for '{keyword}'"

            return f"Found '{keyword}' in {len(results)} page(s):\n\n" + "\n\n".join(results)

    except Exception as e:
        return f"Error: {str(e)}"


@mcp.resource("pdf://info/{file_path}")
async def read_pdf_info_resource(file_path: str) -> str:
    """Resource that provides PDF file information."""
    info = await get_pdf_info(file_path)
    if "error" in info:
        return info["error"]

    return f"""PDF Information:
- File: {info['file_path']}
- Pages: {info['num_pages']}
- Title: {info['title'] or 'N/A'}
- Author: {info['author'] or 'N/A'}
"""


if __name__ == "__main__":
    mcp.run(transport='stdio')

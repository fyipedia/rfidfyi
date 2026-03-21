"""MCP server for rfidfyi — AI assistant tools for rfidfyi.com.

Run: uvx --from "rfidfyi[mcp]" python -m rfidfyi.mcp_server
"""
from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("RFIDFYI")


@mcp.tool()
def list_frequency_bands(limit: int = 20, offset: int = 0) -> str:
    """List frequency_bands from rfidfyi.com.

    Args:
        limit: Maximum number of results. Default 20.
        offset: Number of results to skip. Default 0.
    """
    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        data = api.list_frequency_bands(limit=limit, offset=offset)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return "No frequency_bands found."
        items = results[:limit] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


@mcp.tool()
def get_frequency_band(slug: str) -> str:
    """Get detailed information about a specific frequency_band.

    Args:
        slug: URL slug identifier for the frequency_band.
    """
    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        data = api.get_frequency_band(slug)
        return str(data)


@mcp.tool()
def list_readers(limit: int = 20, offset: int = 0) -> str:
    """List readers from rfidfyi.com.

    Args:
        limit: Maximum number of results. Default 20.
        offset: Number of results to skip. Default 0.
    """
    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        data = api.list_readers(limit=limit, offset=offset)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return "No readers found."
        items = results[:limit] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


@mcp.tool()
def search_rfid(query: str) -> str:
    """Search rfidfyi.com for RFID frequency bands, readers, and EPC schemes.

    Args:
        query: Search query string.
    """
    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        data = api.search(query)
        results = data.get("results", data) if isinstance(data, dict) else data
        if not results:
            return f"No results found for \"{query}\"."
        items = results[:10] if isinstance(results, list) else []
        return "\n".join(f"- {item.get('name', item.get('slug', '?'))}" for item in items)


def main() -> None:
    """Run the MCP server."""
    mcp.run()


if __name__ == "__main__":
    main()

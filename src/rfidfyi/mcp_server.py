"""MCP server for rfidfyi — RFID tag and frequency band tools for AI assistants.

Requires the ``mcp`` extra: ``pip install rfidfyi[mcp]``

Run as a standalone server::

    python -m rfidfyi.mcp_server

Or configure in ``claude_desktop_config.json``::

    {
        "mcpServers": {
            "rfidfyi": {
                "command": "python",
                "args": ["-m", "rfidfyi.mcp_server"]
            }
        }
    }
"""

from __future__ import annotations

from mcp.server.fastmcp import FastMCP

mcp = FastMCP("rfidfyi")


@mcp.tool()
def rfid_search(query: str) -> str:
    """Search for RFID tags, readers, standards, and terminology on RFIDFYI.

    Search across RFID tags (passive, active, semi-passive), readers, frequency bands
    (LF, HF, UHF, SHF), standards (ISO 18000, EPC Gen2), and glossary terms.

    Args:
        query: Search term (e.g. "uhf", "epc gen2", "impinj", "backscatter").
    """
    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        results = api.search(query)

    items = results.get("results", [])
    if not items:
        return f"No results found for '{query}'."

    lines = [
        f"## RFID Search: {query}",
        "",
        f"Found {len(items)} result(s):",
        "",
        "| Type | Name | Slug |",
        "|------|------|------|",
    ]

    for item in items:
        t, n, s = item.get("type", ""), item.get("name", ""), item.get("slug", "")
        lines.append(f"| {t} | {n} | {s} |")

    return "\n".join(lines)


@mcp.tool()
def rfid_lookup(slug: str) -> str:
    """Look up a specific RFID tag by slug.

    Returns full specifications including tag type (passive/active/semi-passive),
    frequency band, protocol, memory size, read range, and EPC length.

    Args:
        slug: Tag slug (e.g. "impinj-monza-r6", "alien-squiggle", "nxp-ucode-8").
    """
    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        data = api.tag(slug)

    lines = [
        f"## {data.get('name', slug)}",
        "",
        data.get("description", ""),
        "",
        f"- **Type**: {data.get('tag_type', 'N/A')}",
        f"- **Frequency**: {data.get('frequency', 'N/A')}",
        f"- **Protocol**: {data.get('protocol', 'N/A')}",
        f"- **Memory**: {data.get('memory', 'N/A')}",
        f"- **Read Range**: {data.get('read_range', 'N/A')}",
        f"- **EPC Length**: {data.get('epc_length', 'N/A')}",
        f"- **Manufacturer**: {data.get('manufacturer', 'N/A')}",
    ]

    standards = data.get("standards", [])
    if standards:
        lines.append("")
        lines.append("### Standards")
        for st in standards:
            lines.append(f"- {st.get('name', '')} ({st.get('issuing_body', '')})")

    return "\n".join(lines)


@mcp.tool()
def rfid_compare(slug_a: str, slug_b: str) -> str:
    """Compare two RFID tags side by side.

    Args:
        slug_a: First tag slug (e.g. "impinj-monza-r6").
        slug_b: Second tag slug (e.g. "alien-higgs-ec").
    """
    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        data = api.compare(slug_a, slug_b)

    a = data.get("a", {})
    b = data.get("b", {})
    a_name = a.get("name", slug_a)
    b_name = b.get("name", slug_b)

    lines = [
        f"## {a_name} vs {b_name}",
        "",
        f"| Property | {a_name} | {b_name} |",
        "|----------|" + "-" * len(a_name) + "--|" + "-" * len(b_name) + "--|",
    ]

    fields = [
        ("Type", "tag_type"),
        ("Frequency", "frequency"),
        ("Protocol", "protocol"),
        ("Memory", "memory"),
        ("Read Range", "read_range"),
        ("EPC Length", "epc_length"),
    ]
    for label, key in fields:
        lines.append(f"| {label} | {a.get(key, '-')} | {b.get(key, '-')} |")

    return "\n".join(lines)


if __name__ == "__main__":
    mcp.run()

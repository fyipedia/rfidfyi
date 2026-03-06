"""Command-line interface for rfidfyi.

Requires the ``cli`` extra: ``pip install rfidfyi[cli]``

Usage::

    rfidfyi search "uhf"
    rfidfyi tag impinj-monza-r6
    rfidfyi compare impinj-monza-r6 alien-higgs-ec
    rfidfyi random
"""

from __future__ import annotations

import typer
from rich.console import Console
from rich.table import Table

app = typer.Typer(
    name="rfidfyi",
    help="RFID tag encyclopedia — look up tags, readers, and standards from RFIDFYI.",
    no_args_is_help=True,
)
console = Console()


@app.command()
def search(
    query: str = typer.Argument(help="Search term (e.g. 'uhf', 'epc gen2', 'impinj')"),
) -> None:
    """Search across tags, readers, standards, frequency bands, and glossary."""
    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        results = api.search(query)

    table = Table(title=f"Search: {query}")
    table.add_column("Type", style="cyan", no_wrap=True)
    table.add_column("Name")
    table.add_column("Slug")

    items = results.get("results", [])
    if not items:
        console.print(f"[yellow]No results found for '{query}'[/yellow]")
        return

    for item in items:
        table.add_row(item.get("type", ""), item.get("name", ""), item.get("slug", ""))

    console.print(table)


@app.command()
def tag(
    slug: str = typer.Argument(help="Tag slug (e.g. 'impinj-monza-r6', 'alien-squiggle')"),
) -> None:
    """Look up an RFID tag with full specifications."""
    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        data = api.tag(slug)

    console.print(f"\n[bold]{data.get('name', slug)}[/bold]")
    if data.get("description"):
        console.print(f"  {data['description'][:200]}")
    console.print()

    table = Table(title="Specifications")
    table.add_column("Property", style="cyan")
    table.add_column("Value")

    specs = [
        ("Type", data.get("tag_type")),
        ("Frequency", data.get("frequency")),
        ("Protocol", data.get("protocol")),
        ("Memory", data.get("memory")),
        ("Read Range", data.get("read_range")),
        ("EPC Length", data.get("epc_length")),
        ("Manufacturer", data.get("manufacturer")),
        ("Chip", data.get("chip")),
    ]
    for label, value in specs:
        if value is not None:
            table.add_row(label, str(value))

    console.print(table)


@app.command()
def compare(
    slug_a: str = typer.Argument(help="First tag slug"),
    slug_b: str = typer.Argument(help="Second tag slug"),
) -> None:
    """Compare two RFID tags side by side."""
    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        data = api.compare(slug_a, slug_b)

    a = data.get("a", {})
    b = data.get("b", {})

    table = Table(title=f"{a.get('name', slug_a)} vs {b.get('name', slug_b)}")
    table.add_column("Property", style="cyan")
    table.add_column(a.get("name", slug_a), style="green")
    table.add_column(b.get("name", slug_b), style="yellow")

    fields = [
        ("Type", "tag_type"),
        ("Frequency", "frequency"),
        ("Protocol", "protocol"),
        ("Memory", "memory"),
        ("Read Range", "read_range"),
        ("EPC Length", "epc_length"),
    ]
    for label, key in fields:
        table.add_row(label, str(a.get(key, "-")), str(b.get(key, "-")))

    console.print(table)


@app.command()
def random() -> None:
    """Discover a random RFID tag."""
    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        data = api.random()

    console.print(f"\n[bold]{data.get('name', 'Unknown')}[/bold]")
    if data.get("description"):
        console.print(f"  {data['description'][:200]}")
    console.print(f"  Type: {data.get('tag_type', 'N/A')}")
    console.print(f"  Frequency: {data.get('frequency', 'N/A')}")
    console.print(f"  Read Range: {data.get('read_range', 'N/A')}")
    console.print()


if __name__ == "__main__":
    app()

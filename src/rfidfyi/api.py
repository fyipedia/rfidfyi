"""HTTP API client for rfidfyi.com REST endpoints.

Requires the ``api`` extra: ``pip install rfidfyi[api]``

Usage::

    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        results = api.search("uhf")
        tag = api.tag("alien-squiggle")
        comparison = api.compare("impinj-monza-r6", "alien-higgs-ec")
"""

from __future__ import annotations

from typing import Any

import httpx


class RFIDFYI:
    """API client for the rfidfyi.com REST API.

    Provides access to 12 endpoints covering RFID tags, readers, tag families,
    frequency bands, standards, EPC schemes, use cases, glossary terms, search,
    comparison, and random discovery.

    Args:
        base_url: API base URL. Defaults to ``https://rfidfyi.com``.
        timeout: Request timeout in seconds. Defaults to ``10.0``.
    """

    def __init__(
        self,
        base_url: str = "https://rfidfyi.com",
        timeout: float = 10.0,
    ) -> None:
        self._client = httpx.Client(base_url=base_url, timeout=timeout)

    # -- HTTP helpers ----------------------------------------------------------

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(path, params={k: v for k, v in params.items() if v is not None})
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -------------------------------------------------------------

    def tag(self, slug: str) -> dict[str, Any]:
        """Get RFID tag detail with specifications, frequency, and read range.

        Args:
            slug: Tag URL slug (e.g. ``"impinj-monza-r6"``, ``"alien-squiggle"``).
        """
        return self._get(f"/api/tag/{slug}/")

    def reader(self, slug: str) -> dict[str, Any]:
        """Get RFID reader detail with supported protocols and frequencies.

        Args:
            slug: Reader URL slug (e.g. ``"impinj-speedway-r420"``, ``"zebra-fx9600"``).
        """
        return self._get(f"/api/reader/{slug}/")

    def family(self, slug: str) -> dict[str, Any]:
        """Get tag family with member tags and specifications.

        Args:
            slug: Family URL slug (e.g. ``"passive-uhf"``, ``"active-wifi"``).
        """
        return self._get(f"/api/family/{slug}/")

    def frequency(self, slug: str) -> dict[str, Any]:
        """Get frequency band detail with regional allocations and tag types.

        Args:
            slug: Frequency band URL slug (e.g. ``"uhf-860-960"``, ``"hf-13-56"``).
        """
        return self._get(f"/api/frequency/{slug}/")

    def standard(self, slug: str) -> dict[str, Any]:
        """Get RFID standard detail with linked tags and protocols.

        Args:
            slug: Standard URL slug (e.g. ``"iso-18000-63"``, ``"epc-gen2"``).
        """
        return self._get(f"/api/standard/{slug}/")

    def epc(self, slug: str) -> dict[str, Any]:
        """Get EPC scheme detail with encoding structure and usage.

        Args:
            slug: EPC scheme URL slug (e.g. ``"sgtin-96"``, ``"sscc-96"``).
        """
        return self._get(f"/api/epc/{slug}/")

    def use_case(self, slug: str) -> dict[str, Any]:
        """Get RFID use case detail with recommended tags and frequencies.

        Args:
            slug: Use case URL slug (e.g. ``"retail-inventory"``, ``"asset-tracking"``).
        """
        return self._get(f"/api/use-case/{slug}/")

    def glossary_term(self, slug: str) -> dict[str, Any]:
        """Get glossary term definition for tooltips and reference.

        Args:
            slug: Term URL slug (e.g. ``"backscatter"``, ``"epc"``, ``"interrogator"``).
        """
        return self._get(f"/api/term/{slug}/")

    def search(self, query: str) -> dict[str, Any]:
        """Search across tags, readers, standards, frequency bands, and glossary terms.

        Args:
            query: Search term (minimum 2 characters).
        """
        return self._get("/api/search/", q=query)

    def compare(self, slug_a: str, slug_b: str) -> dict[str, Any]:
        """Compare two RFID tags side by side.

        Args:
            slug_a: First tag slug (e.g. ``"impinj-monza-r6"``).
            slug_b: Second tag slug (e.g. ``"alien-higgs-ec"``).
        """
        return self._get("/api/compare/", a=slug_a, b=slug_b)

    def random(self) -> dict[str, Any]:
        """Get a random RFID tag with full detail."""
        return self._get("/api/random/")

    def openapi(self) -> dict[str, Any]:
        """Get the OpenAPI 3.1.0 specification."""
        return self._get("/api/openapi.json")

    # -- Context manager -------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP connection."""
        self._client.close()

    def __enter__(self) -> RFIDFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

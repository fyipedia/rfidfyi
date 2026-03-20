"""HTTP API client for rfidfyi.com REST endpoints.

Requires the ``api`` extra: ``pip install rfidfyi[api]``

Usage::

    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        items = api.list_antenna_types()
        detail = api.get_antenna_type("example-slug")
        results = api.search("query")
"""

from __future__ import annotations

from typing import Any

import httpx


class RFIDFYI:
    """API client for the rfidfyi.com REST API.

    Provides typed access to all rfidfyi.com endpoints including
    list, detail, and search operations.

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

    def _get(self, path: str, **params: Any) -> dict[str, Any]:
        resp = self._client.get(
            path,
            params={k: v for k, v in params.items() if v is not None},
        )
        resp.raise_for_status()
        result: dict[str, Any] = resp.json()
        return result

    # -- Endpoints -----------------------------------------------------------

    def list_antenna_types(self, **params: Any) -> dict[str, Any]:
        """List all antenna types."""
        return self._get("/api/v1/antenna-types/", **params)

    def get_antenna_type(self, slug: str) -> dict[str, Any]:
        """Get antenna type by slug."""
        return self._get(f"/api/v1/antenna-types/" + slug + "/")

    def list_epc_schemes(self, **params: Any) -> dict[str, Any]:
        """List all epc schemes."""
        return self._get("/api/v1/epc-schemes/", **params)

    def get_epc_scheme(self, slug: str) -> dict[str, Any]:
        """Get epc scheme by slug."""
        return self._get(f"/api/v1/epc-schemes/" + slug + "/")

    def list_faqs(self, **params: Any) -> dict[str, Any]:
        """List all faqs."""
        return self._get("/api/v1/faqs/", **params)

    def get_faq(self, slug: str) -> dict[str, Any]:
        """Get faq by slug."""
        return self._get(f"/api/v1/faqs/" + slug + "/")

    def list_frequency_bands(self, **params: Any) -> dict[str, Any]:
        """List all frequency bands."""
        return self._get("/api/v1/frequency-bands/", **params)

    def get_frequency_band(self, slug: str) -> dict[str, Any]:
        """Get frequency band by slug."""
        return self._get(f"/api/v1/frequency-bands/" + slug + "/")

    def list_glossary(self, **params: Any) -> dict[str, Any]:
        """List all glossary."""
        return self._get("/api/v1/glossary/", **params)

    def get_term(self, slug: str) -> dict[str, Any]:
        """Get term by slug."""
        return self._get(f"/api/v1/glossary/" + slug + "/")

    def list_guides(self, **params: Any) -> dict[str, Any]:
        """List all guides."""
        return self._get("/api/v1/guides/", **params)

    def get_guide(self, slug: str) -> dict[str, Any]:
        """Get guide by slug."""
        return self._get(f"/api/v1/guides/" + slug + "/")

    def list_industries(self, **params: Any) -> dict[str, Any]:
        """List all industries."""
        return self._get("/api/v1/industries/", **params)

    def get_industry(self, slug: str) -> dict[str, Any]:
        """Get industry by slug."""
        return self._get(f"/api/v1/industries/" + slug + "/")

    def list_manufacturers(self, **params: Any) -> dict[str, Any]:
        """List all manufacturers."""
        return self._get("/api/v1/manufacturers/", **params)

    def get_manufacturer(self, slug: str) -> dict[str, Any]:
        """Get manufacturer by slug."""
        return self._get(f"/api/v1/manufacturers/" + slug + "/")

    def list_readers(self, **params: Any) -> dict[str, Any]:
        """List all readers."""
        return self._get("/api/v1/readers/", **params)

    def get_reader(self, slug: str) -> dict[str, Any]:
        """Get reader by slug."""
        return self._get(f"/api/v1/readers/" + slug + "/")

    def list_standards(self, **params: Any) -> dict[str, Any]:
        """List all standards."""
        return self._get("/api/v1/standards/", **params)

    def get_standard(self, slug: str) -> dict[str, Any]:
        """Get standard by slug."""
        return self._get(f"/api/v1/standards/" + slug + "/")

    def list_tag_families(self, **params: Any) -> dict[str, Any]:
        """List all tag families."""
        return self._get("/api/v1/tag-families/", **params)

    def get_tag_family(self, slug: str) -> dict[str, Any]:
        """Get tag family by slug."""
        return self._get(f"/api/v1/tag-families/" + slug + "/")

    def list_tags(self, **params: Any) -> dict[str, Any]:
        """List all tags."""
        return self._get("/api/v1/tags/", **params)

    def get_tag(self, slug: str) -> dict[str, Any]:
        """Get tag by slug."""
        return self._get(f"/api/v1/tags/" + slug + "/")

    def list_use_cases(self, **params: Any) -> dict[str, Any]:
        """List all use cases."""
        return self._get("/api/v1/use-cases/", **params)

    def get_use_case(self, slug: str) -> dict[str, Any]:
        """Get use case by slug."""
        return self._get(f"/api/v1/use-cases/" + slug + "/")

    def search(self, query: str, **params: Any) -> dict[str, Any]:
        """Search across all content."""
        return self._get(f"/api/v1/search/", q=query, **params)

    # -- Lifecycle -----------------------------------------------------------

    def close(self) -> None:
        """Close the underlying HTTP client."""
        self._client.close()

    def __enter__(self) -> RFIDFYI:
        return self

    def __exit__(self, *_: object) -> None:
        self.close()

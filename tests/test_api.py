"""Tests for rfidfyi API client."""

from __future__ import annotations

from rfidfyi.api import RFIDFYI


def test_client_init() -> None:
    client = RFIDFYI()
    assert client._client.base_url == "https://rfidfyi.com"
    client.close()


def test_client_custom_base_url() -> None:
    client = RFIDFYI(base_url="https://test.example.com")
    assert client._client.base_url == "https://test.example.com"
    client.close()


def test_client_context_manager() -> None:
    with RFIDFYI() as api:
        assert api._client.base_url == "https://rfidfyi.com"


def test_version() -> None:
    from rfidfyi import __version__

    assert __version__ == "0.1.0"

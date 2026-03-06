"""rfidfyi — RFID tag and frequency band encyclopedia API client for developers.

Look up RFID tags, readers, frequency bands, EPC schemes, standards, and use cases from RFIDFYI.

Usage::

    from rfidfyi.api import RFIDFYI

    with RFIDFYI() as api:
        results = api.search("uhf")
        print(results)
"""

__version__ = "0.1.0"

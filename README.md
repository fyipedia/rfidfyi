# rfidfyi

[![PyPI](https://img.shields.io/pypi/v/rfidfyi)](https://pypi.org/project/rfidfyi/)
[![Python](https://img.shields.io/pypi/pyversions/rfidfyi)](https://pypi.org/project/rfidfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

RFID tag and frequency band encyclopedia API client for Python. Look up passive, active, and semi-passive RFID tags, readers, EPC Gen2 encoding schemes, ISO 18000-series standards, and frequency band specifications from [RFIDFYI](https://rfidfyi.com) -- the comprehensive RFID reference covering tag ICs, reader hardware, air interface protocols, and real-world deployment use cases across retail, logistics, healthcare, and industrial automation.

> **Explore RFID at [rfidfyi.com](https://rfidfyi.com)** -- [Tag Explorer](https://rfidfyi.com/tag/) | [Standards Reference](https://rfidfyi.com/standard/) | [Frequency Bands](https://rfidfyi.com/frequency/) | [EPC Schemes](https://rfidfyi.com/epc/)

## Install

```bash
pip install rfidfyi[api]     # API client (httpx)
pip install rfidfyi[cli]     # + CLI (typer, rich)
pip install rfidfyi[mcp]     # + MCP server
pip install rfidfyi[all]     # Everything
```

## Quick Start

```python
from rfidfyi.api import RFIDFYI

with RFIDFYI() as api:
    # Search tags, readers, standards, frequency bands
    results = api.search("uhf")
    print(results)

    # Look up a specific RFID tag
    tag = api.tag("impinj-monza-r6")
    print(tag["name"], tag["frequency"])

    # Compare two tags
    diff = api.compare("impinj-monza-r6", "alien-higgs-ec")
    print(diff)

    # Discover a random tag
    surprise = api.random()
    print(surprise["name"])
```

## What You'll Find on RFIDFYI

RFIDFYI is a comprehensive RFID encyclopedia covering tags, readers, frequency bands, air interface protocols, EPC encoding schemes, and industry standards. Radio-Frequency Identification (RFID) uses electromagnetic fields to automatically identify and track tags attached to objects -- powering supply chain visibility, inventory management, access control, and asset tracking across every major industry.

### RFID Tag Types

| Type | Power Source | Read Range | Examples |
|------|-------------|------------|----------|
| Passive | Harvested from reader RF field | LF: <10 cm, HF: <1 m, UHF: 1-12 m | Impinj Monza, NXP UCODE, Alien Higgs |
| Semi-Passive (BAP) | Battery-assisted backscatter | 15-30 m | ON Semiconductor Magnus S3 |
| Active | Internal battery + transmitter | 30-100+ m | Zebra WhereTag, Confidex Ironside |

Passive tags dominate commercial deployments (90%+ of all RFID tags shipped) due to their low cost ($0.03-0.15 per tag), no maintenance requirements, and effectively unlimited lifespan. Active tags serve specialized long-range applications like real-time location systems (RTLS) and container tracking.

### Frequency Bands

| Band | Frequency | Range | Standards | Primary Use |
|------|-----------|-------|-----------|-------------|
| LF (Low Frequency) | 125-134.2 kHz | <10 cm | ISO 11784/11785 | Animal tracking, access control |
| HF (High Frequency) | 13.56 MHz | <1 m | ISO 14443, ISO 15693 | NFC payments, library books, laundry |
| UHF (Ultra-High Frequency) | 860-960 MHz | 1-12 m | ISO 18000-63, EPC Gen2 | Retail inventory, supply chain, logistics |
| SHF (Super-High Frequency) | 2.45 GHz | 1-2 m | ISO 18000-4 | Industrial automation, toll collection |

UHF RFID (860-960 MHz) is the fastest-growing segment, driven by EPC Gen2 standardization and retail mandates from Walmart, Target, and major European retailers. Regional frequency allocations vary: 902-928 MHz (Americas), 865-868 MHz (Europe), 920-925 MHz (China/Japan).

### Key Standards

| Standard | Organization | Scope |
|----------|-------------|-------|
| ISO/IEC 18000-63 | ISO | UHF RFID air interface (EPC Gen2 aligned) |
| EPC Gen2 v2.1 | GS1/EPCglobal | UHF Class 1 Gen 2 air interface protocol |
| ISO/IEC 14443 | ISO | HF proximity cards (NFC-A/B, <10 cm) |
| ISO/IEC 15693 | ISO | HF vicinity cards (up to 1 m) |
| ISO 11784/11785 | ISO | LF animal identification |
| EPC TDS 2.0 | GS1 | EPC Tag Data Standard -- encoding schemes |

### EPC Encoding Schemes

The Electronic Product Code (EPC) is a universal identifier for physical objects, encoded on UHF RFID tags. Common EPC schemes include SGTIN-96 (serialized trade items), SSCC-96 (shipping containers), GRAI-96 (returnable assets), GIAI-96 (individual assets), and SGLN-96 (locations). Each scheme encodes a GS1 Company Prefix, item reference, and unique serial number into a 96-bit or 128-bit EPC memory bank.

### Read Range Factors

RFID read range depends on multiple factors: tag antenna design and gain, reader transmit power (typically 1-4W EIRP for UHF), operating frequency, tag IC sensitivity (typically -17 to -22 dBm for modern UHF chips), environmental conditions (metal, liquids, multi-path interference), and regulatory power limits per region. Modern UHF tag ICs like the Impinj Monza R6 achieve -22.1 dBm sensitivity, enabling reliable reads at 9-12 meters in open-air deployments.

Learn more: [Tag Explorer](https://rfidfyi.com/tag/) | [Frequency Guide](https://rfidfyi.com/frequency/) | [EPC Schemes](https://rfidfyi.com/epc/)

## API Endpoints

Free, no authentication required. JSON responses with CORS enabled.

| Method | Endpoint | Description |
|--------|----------|-------------|
| GET | `/api/tag/{slug}/` | RFID tag detail with specs |
| GET | `/api/reader/{slug}/` | Reader detail with protocols |
| GET | `/api/family/{slug}/` | Tag family with member tags |
| GET | `/api/frequency/{slug}/` | Frequency band with regional allocations |
| GET | `/api/standard/{slug}/` | Standard detail with linked tags |
| GET | `/api/epc/{slug}/` | EPC scheme encoding structure |
| GET | `/api/use-case/{slug}/` | Use case with recommended tags |
| GET | `/api/term/{slug}/` | Glossary term definition |
| GET | `/api/search/?q={query}` | Search across all content types |
| GET | `/api/compare/?a={slug}&b={slug}` | Compare two tags |
| GET | `/api/random/` | Random tag discovery |
| GET | `/api/openapi.json` | OpenAPI 3.1.0 specification |

```bash
# Example: search for UHF tags
curl -s "https://rfidfyi.com/api/search/?q=uhf" | python -m json.tool
```

## Command-Line Interface

```bash
rfidfyi search "epc gen2"
rfidfyi tag impinj-monza-r6
rfidfyi compare impinj-monza-r6 alien-higgs-ec
rfidfyi random
```

## MCP Server (Claude, Cursor, Windsurf)

```json
{
    "mcpServers": {
        "rfidfyi": {
            "command": "python",
            "args": ["-m", "rfidfyi.mcp_server"]
        }
    }
}
```

Tools: `rfid_search`, `rfid_lookup`, `rfid_compare`

## API Client

```python
from rfidfyi.api import RFIDFYI

with RFIDFYI() as api:
    # All 12 endpoints
    api.search("uhf")
    api.tag("impinj-monza-r6")
    api.reader("impinj-speedway-r420")
    api.family("passive-uhf")
    api.frequency("uhf-860-960")
    api.standard("iso-18000-63")
    api.epc("sgtin-96")
    api.use_case("retail-inventory")
    api.glossary_term("backscatter")
    api.compare("impinj-monza-r6", "alien-higgs-ec")
    api.random()
    api.openapi()
```

## Also Available

| Language | Package | Install |
|----------|---------|---------|
| Python | [rfidfyi](https://pypi.org/project/rfidfyi/) | `pip install rfidfyi` |
| TypeScript | [rfidfyi](https://www.npmjs.com/package/rfidfyi) | `npm install rfidfyi` |
| Go | [rfidfyi-go](https://pkg.go.dev/github.com/fyipedia/rfidfyi-go) | `go get github.com/fyipedia/rfidfyi-go` |
| Rust | [rfidfyi](https://crates.io/crates/rfidfyi) | `cargo add rfidfyi` |
| Ruby | [rfidfyi](https://rubygems.org/gems/rfidfyi) | `gem install rfidfyi` |

## Code FYI Family

| Site | Domain | Focus |
|------|--------|-------|
| BarcodeFYI | [barcodefyi.com](https://barcodefyi.com) | Barcode symbologies & standards |
| QRCodeFYI | [qrcodefyi.com](https://qrcodefyi.com) | QR code types & encoding |
| NFCFYI | [nfcfyi.com](https://nfcfyi.com) | NFC tags & NDEF records |
| BLEFYI | [blefyi.com](https://blefyi.com) | Bluetooth Low Energy profiles |
| RFIDFYI | [rfidfyi.com](https://rfidfyi.com) | RFID tags & frequency bands |
| SmartCardFYI | [smartcardfyi.com](https://smartcardfyi.com) | Smart card types & platforms |

## License

MIT

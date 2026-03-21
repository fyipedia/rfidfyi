# rfidfyi

[![PyPI version](https://agentgif.com/badge/pypi/rfidfyi/version.svg)](https://pypi.org/project/rfidfyi/)
[![Python](https://img.shields.io/pypi/pyversions/rfidfyi)](https://pypi.org/project/rfidfyi/)
[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)

RFID tag and frequency band encyclopedia API client for Python. Look up passive, active, and semi-passive RFID tags, readers from Impinj, Zebra, and Alien Technology, EPC Gen2 encoding schemes, ISO 18000-series standards, and frequency band specifications from [RFIDFYI](https://rfidfyi.com) -- the comprehensive RFID reference with 318 records covering tag ICs, reader hardware, air interface protocols, and real-world deployment use cases across retail, logistics, healthcare, and industrial automation.

Extracted from [RFIDFYI](https://rfidfyi.com), an RFID technology platform with 318 records spanning tag specifications, reader hardware, frequency regulations, EPC encoding, antenna types, and industry deployment guides used by supply chain engineers, inventory management architects, and IoT developers worldwide.

> **Explore RFID at [rfidfyi.com](https://rfidfyi.com)** -- [Tag Explorer](https://rfidfyi.com/tag/) | [Standards Reference](https://rfidfyi.com/standard/) | [Frequency Bands](https://rfidfyi.com/frequency/) | [EPC Schemes](https://rfidfyi.com/epc/)

<p align="center">
  <img src="https://raw.githubusercontent.com/fyipedia/rfidfyi/main/demo.gif" alt="rfidfyi demo -- RFID tag lookup, frequency band reference, and tag comparison in Python" width="800">
</p>

## Table of Contents

- [Install](#install)
- [Quick Start](#quick-start)
- [What You'll Find on RFIDFYI](#what-youll-find-on-rfidfyi)
  - [RFID Tag Types](#rfid-tag-types)
  - [Frequency Bands](#frequency-bands)
  - [EPC Encoding Schemes](#epc-encoding-schemes)
  - [Tag IC Families](#tag-ic-families)
  - [Reader Hardware](#reader-hardware)
  - [Read Range Factors](#read-range-factors)
  - [Key RFID Standards](#key-rfid-standards)
- [API Endpoints](#api-endpoints)
- [Command-Line Interface](#command-line-interface)
- [MCP Server (Claude, Cursor, Windsurf)](#mcp-server-claude-cursor-windsurf)
- [REST API Client](#rest-api-client)
- [Learn More About RFID](#learn-more-about-rfid)
- [Also Available](#also-available)
- [Tag FYI Family](#tag-fyi-family)
- [FYIPedia Developer Tools](#fyipedia-developer-tools)
- [License](#license)

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

    # Look up a specific RFID tag IC
    tag = api.tag("impinj-monza-r6")
    print(tag["name"], tag["frequency"])  # Impinj Monza R6 UHF

    # Compare two RFID tags side-by-side
    diff = api.compare("impinj-monza-r6", "alien-higgs-ec")
    print(diff)

    # Discover a random tag
    surprise = api.random()
    print(surprise["name"])
```

## What You'll Find on RFIDFYI

RFIDFYI is a comprehensive RFID encyclopedia covering tags, readers, frequency bands, air interface protocols, EPC encoding schemes, and industry standards. Radio-Frequency Identification (RFID) uses electromagnetic fields to automatically identify and track tags attached to objects -- powering supply chain visibility, inventory management, access control, asset tracking, and anti-counterfeiting across every major industry.

### RFID Tag Types

RFID tags are classified by their power source, which fundamentally determines read range, cost, size, and application suitability:

| Type | Power Source | Read Range | Cost | Battery Life | Examples |
|------|-------------|------------|------|-------------|----------|
| Passive | Harvested from reader RF field | LF: <10 cm, HF: <1 m, UHF: 1-12 m | $0.03-0.15 | Unlimited | Impinj Monza, NXP UCODE, Alien Higgs |
| Semi-Passive (BAP) | Battery-assisted backscatter | 15-30 m | $2-10 | 3-5 years | ON Semiconductor Magnus S3 |
| Active | Internal battery + transmitter | 30-100+ m | $10-50+ | 3-7 years | Zebra WhereTag, Confidex Ironside |

Passive tags dominate commercial deployments (90%+ of all RFID tags shipped) due to their low cost, no maintenance requirements, and effectively unlimited lifespan. Active tags serve specialized long-range applications like real-time location systems (RTLS) and container tracking.

Learn more: [Tag Explorer](https://rfidfyi.com/tag/) | [Glossary](https://rfidfyi.com/glossary/)

### Frequency Bands

RFID operates across four primary frequency bands, each with distinct physics governing read range, data rate, and material penetration:

| Band | Frequency | Range | Data Rate | Penetration | Primary Use |
|------|-----------|-------|-----------|-------------|-------------|
| LF | 125-134.2 kHz | <10 cm | <1 kbps | Excellent (water, metal) | Animal tracking, access cards |
| HF | 13.56 MHz | <1 m | 25-424 kbps | Good (water), poor (metal) | NFC payments, library books |
| UHF | 860-960 MHz | 1-12 m | 40-640 kbps | Poor (water), fair (metal) | Retail, logistics, supply chain |
| SHF (Microwave) | 2.45 GHz | 1-2 m | High | Poor | Toll collection, industrial |

**UHF regional allocations**: UHF RFID frequencies vary by region due to regulatory differences -- 902-928 MHz (Americas, FCC Part 15), 865-868 MHz (Europe, ETSI EN 302 208), 920-925 MHz (China, MIIT), 916-921 MHz (Japan, ARIB). Tags must be designed for the target market's frequency range, and multi-region tags use broadband antenna designs covering 860-960 MHz.

Learn more: [Frequency Bands](https://rfidfyi.com/frequency/) | [Standards](https://rfidfyi.com/standard/)

### EPC Encoding Schemes

The Electronic Product Code (EPC) is a universal identifier for physical objects, encoded in the EPC memory bank of UHF RFID tags. GS1's EPC Tag Data Standard (TDS) defines encoding schemes that map existing GS1 identifiers to binary tag formats:

| Scheme | Bits | Encodes | Use Case |
|--------|------|---------|----------|
| SGTIN-96 | 96 | GS1 Company Prefix + Item Ref + Serial | Retail items (most common) |
| SGTIN-198 | 198 | Same + alphanumeric serial | Pharmaceutical serialization |
| SSCC-96 | 96 | GS1 CP + Serial Reference | Shipping containers, pallets |
| GRAI-96 | 96 | GS1 CP + Asset Type + Serial | Returnable assets (totes, kegs) |
| GIAI-96 | 96 | GS1 CP + Individual Asset Ref | Fixed assets (equipment, tools) |
| SGLN-96 | 96 | GS1 CP + Location Ref + Extension | Physical locations (warehouses) |
| GDTI-96 | 96 | GS1 CP + Document Type + Serial | Documents, certificates |

**SGTIN-96** is the most widely deployed EPC scheme, used in Walmart, Target, and Zara item-level tagging mandates. It encodes a 14-digit GTIN plus a 38-bit serial number, enabling unique identification of every individual item (not just SKU-level).

Learn more: [EPC Schemes](https://rfidfyi.com/epc/) | [Industry Applications](https://rfidfyi.com/use-case/)

### Tag IC Families

Major RFID tag IC product lines from leading semiconductor manufacturers:

| Family | Manufacturer | Band | Sensitivity | Memory | Key Feature |
|--------|-------------|------|-------------|--------|-------------|
| Monza R6 | Impinj | UHF | -22.1 dBm | 96-bit EPC | Industry-best sensitivity |
| Monza R6-P | Impinj | UHF | -20.5 dBm | 96-bit + 32-bit user | Read-only access password |
| UCODE 8 | NXP | UHF | -22.5 dBm | 96-bit EPC | Smallest IC die (0.33 mm2) |
| UCODE 9 | NXP | UHF | -23.0 dBm | 128-bit EPC | AES-128 authentication |
| Higgs EC | Alien Technology | UHF | -20.5 dBm | 96-bit + 128-bit user | Extended memory for encoding |
| Magnus S3 | ON Semiconductor | UHF | -8.2 dBm (BAP) | 512-bit | Battery-assisted, temperature sensor |

### Reader Hardware

RFID readers transmit RF energy to power passive tags and decode their backscattered responses. Fixed readers mount at dock doors, conveyor belts, and portals; handheld readers serve inventory counting and asset verification:

| Reader | Manufacturer | Ports | Max Power | Interface | Use Case |
|--------|-------------|-------|-----------|-----------|----------|
| Speedway R420 | Impinj | 4 | 32.5 dBm | Ethernet, USB | Dock door portals |
| FX9600 | Zebra | 4/8 | 33 dBm | Ethernet, USB | Warehouse, distribution |
| ALR-F800 | Alien Technology | 4 | 33 dBm | Ethernet, GPIO | Manufacturing, logistics |
| MC3330xR | Zebra | Integrated | 24 dBm | Wi-Fi, BT | Handheld inventory |

### Read Range Factors

RFID read range depends on physics and environmental conditions:

| Factor | Impact | Optimization |
|--------|--------|-------------|
| Tag IC sensitivity | -22 dBm IC reads at 2x distance vs -18 dBm | Choose latest-gen ICs |
| Reader TX power | +3 dBm = ~40% range increase | Max regional EIRP limits |
| Tag antenna gain | Higher gain = longer range, narrower beam | Match antenna to orientation |
| Frequency | UHF travels farther than HF/LF | UHF for long-range applications |
| Material interference | Water absorbs UHF, metal reflects | Specialized on-metal tag designs |
| Multi-path | Reflections cause null zones | Antenna placement, circular polarization |

Learn more: [Tag Explorer](https://rfidfyi.com/tag/) | [Frequency Guide](https://rfidfyi.com/frequency/)

### Key RFID Standards

| Standard | Organization | Scope |
|----------|-------------|-------|
| ISO/IEC 18000-63 | ISO | UHF RFID air interface (EPC Gen2 aligned) |
| EPC Gen2 v2.1 | GS1/EPCglobal | UHF Class 1 Gen 2 protocol |
| ISO/IEC 14443 A/B | ISO | HF proximity cards (NFC compatible) |
| ISO/IEC 15693 | ISO | HF vicinity cards (up to 1 m) |
| ISO 11784/11785 | ISO | LF animal identification |
| EPC TDS 2.0 | GS1 | Tag Data Standard -- encoding schemes |
| RAIN RFID | RAIN Alliance | UHF RFID ecosystem certification |

Learn more: [Standards Reference](https://rfidfyi.com/standard/) | [EPC Schemes](https://rfidfyi.com/epc/)

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

### Example

```bash
# Search for UHF RFID tags
curl -s "https://rfidfyi.com/api/search/?q=uhf" | python -m json.tool
```

Full API documentation at [rfidfyi.com/api/](https://rfidfyi.com/api/).
OpenAPI 3.1.0 spec: [rfidfyi.com/api/openapi.json](https://rfidfyi.com/api/openapi.json).

## Command-Line Interface

```bash
rfidfyi search "epc gen2"                     # Search all content
rfidfyi tag impinj-monza-r6                   # Tag detail
rfidfyi compare impinj-monza-r6 alien-higgs-ec  # Side-by-side comparison
rfidfyi random                                # Discover a random tag
```

## MCP Server (Claude, Cursor, Windsurf)

```json
{
    "mcpServers": {
        "rfidfyi": {
            "command": "uvx",
            "args": ["--from", "rfidfyi[mcp]", "python", "-m", "rfidfyi.mcp_server"]
        }
    }
}
```

Tools: `rfid_search`, `rfid_lookup`, `rfid_compare`

## REST API Client

```python
from rfidfyi.api import RFIDFYI

with RFIDFYI() as api:
    api.search("uhf")                          # Full-text search
    api.tag("impinj-monza-r6")                 # Tag detail
    api.reader("impinj-speedway-r420")         # Reader detail
    api.family("passive-uhf")                  # Tag family
    api.frequency("uhf-860-960")               # Frequency band
    api.standard("iso-18000-63")               # Standard detail
    api.epc("sgtin-96")                        # EPC scheme
    api.use_case("retail-inventory")           # Use case
    api.glossary_term("backscatter")           # Glossary term
    api.compare("impinj-monza-r6", "alien-higgs-ec")  # Compare
    api.random()                               # Random discovery
    api.openapi()                              # OpenAPI 3.1.0 spec
```

## Learn More About RFID

- **Browse**: [Tag Explorer](https://rfidfyi.com/tag/) · [Frequency Bands](https://rfidfyi.com/frequency/) · [EPC Schemes](https://rfidfyi.com/epc/)
- **Reference**: [Standards](https://rfidfyi.com/standard/) · [Use Cases](https://rfidfyi.com/use-case/) · [Glossary](https://rfidfyi.com/glossary/)
- **API**: [REST API Docs](https://rfidfyi.com/api/) · [OpenAPI Spec](https://rfidfyi.com/api/openapi.json)

## Also Available

| Platform | Install | Link |
|----------|---------|------|
| **npm** | `npm install rfidfyi` | [npm](https://www.npmjs.com/package/rfidfyi) |
| **Go** | `go get github.com/fyipedia/rfidfyi-go` | [pkg.go.dev](https://pkg.go.dev/github.com/fyipedia/rfidfyi-go) |
| **Rust** | `cargo add rfidfyi` | [crates.io](https://crates.io/crates/rfidfyi) |
| **Ruby** | `gem install rfidfyi` | [rubygems.org](https://rubygems.org/gems/rfidfyi) |
| **MCP** | `uvx --from "rfidfyi[mcp]" python -m rfidfyi.mcp_server` | [Config](#mcp-server-claude-cursor-windsurf) |

## Tag FYI Family

Part of the [FYIPedia](https://fyipedia.com) open-source developer tools ecosystem -- automatic identification and data capture technologies.

| Site | Domain | Focus |
|------|--------|-------|
| BarcodeFYI | [barcodefyi.com](https://barcodefyi.com) | 518 records -- barcode symbologies, standards, GS1 prefixes |
| QRCodeFYI | [qrcodefyi.com](https://qrcodefyi.com) | 425 records -- QR code types, versions, encoding modes |
| NFCFYI | [nfcfyi.com](https://nfcfyi.com) | 288 records -- NFC chips, NDEF records, standards |
| BLEFYI | [blefyi.com](https://blefyi.com) | 261 records -- BLE chips, GATT profiles, beacons |
| **RFIDFYI** | [rfidfyi.com](https://rfidfyi.com) | **318 records -- RFID tags, frequency bands, EPC schemes** |
| SmartCardFYI | [smartcardfyi.com](https://smartcardfyi.com) | 280 records -- smart cards, EMV, Java Card, platforms |

## FYIPedia Developer Tools

| Package | PyPI | npm | Description |
|---------|------|-----|-------------|
| barcodefyi | [PyPI](https://pypi.org/project/barcodefyi/) | [npm](https://www.npmjs.com/package/barcodefyi) | Barcode symbologies, standards -- [barcodefyi.com](https://barcodefyi.com) |
| qrcodefyi | [PyPI](https://pypi.org/project/qrcodefyi/) | [npm](https://www.npmjs.com/package/qrcodefyi) | QR code types, versions, encoding -- [qrcodefyi.com](https://qrcodefyi.com) |
| nfcfyi | [PyPI](https://pypi.org/project/nfcfyi/) | [npm](https://www.npmjs.com/package/nfcfyi) | NFC chips, NDEF, standards -- [nfcfyi.com](https://nfcfyi.com) |
| blefyi | [PyPI](https://pypi.org/project/blefyi/) | [npm](https://www.npmjs.com/package/blefyi) | BLE profiles, beacons, chips -- [blefyi.com](https://blefyi.com) |
| **rfidfyi** | [PyPI](https://pypi.org/project/rfidfyi/) | [npm](https://www.npmjs.com/package/rfidfyi) | **RFID tags, readers, frequencies -- [rfidfyi.com](https://rfidfyi.com)** |
| smartcardfyi | [PyPI](https://pypi.org/project/smartcardfyi/) | [npm](https://www.npmjs.com/package/smartcardfyi) | Smart cards, EMV, platforms -- [smartcardfyi.com](https://smartcardfyi.com) |

## License

MIT

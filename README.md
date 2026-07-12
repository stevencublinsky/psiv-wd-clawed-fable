# Phantasy Star IV: Clawed Fable Five - Graphical Enhancement Rebuild

> **Project Status**: Phase 1 Complete (ROM Analysis & Extraction) | Phase 2 Ready (Graphical Rebuild)

A complete reverse-engineering, extraction, and graphical enhancement project for *Phantasy Star IV: The End of the Millennium* (Working Designs 6.01 patch) on the Sega Genesis/Mega Drive.

---

## Quick Start

```bash
# Clone the repo
git clone https://github.com/stevencublinsky/psiv-wd-clawed-fable.git
cd psiv-wd-clawed-fable

# Regenerate ALL extracted assets from your ROM
python scripts/regenerate_all.py "path/to/rom.bin" ./

# Decode any .b64 binary files
python scripts/decode_b64.py --all
```

---

## Table of Contents

- [Project Overview](#project-overview)
- [Major Discoveries](#major-discoveries)
- [Repository Structure](#repository-structure)
- [Binary File Handling](#binary-file-handling)
- [Character Encoding Table](#character-encoding-table)
- [Control Codes Reference](#control-codes-reference)
- [Dialogue Extraction](#dialogue-extraction)
- [Font & Graphics](#font--graphics)
- [Rebuild Toolkit](#rebuild-toolkit)
- [Advanced Graphics Options](#advanced-graphics-options)
- [Handoff to Phase 2](#handoff-to-phase-2)
- [License](#license)

---

## Project Overview

| Property | Value |
|----------|-------|
| **Game** | Phantasy Star IV: The End of the Millennium |
| **Version** | Working Designs 6.01 (Fan Patch) |
| **Platform** | Sega Genesis/Mega Drive |
| **Serial** | GM MK-1307 |
| **ROM Size** | 3,209,748 bytes (3.06 MB) |
| **Format** | Raw Binary (.bin) |
| **Status** | Phase 1 Complete - All assets extracted and documented |

### Dual Text Encoding System (Critical Discovery)

This ROM uses **two different text encodings**:

1. **Dialogue Text**: Custom encoding where bytes `0x01-0x1F` represent lowercase letters
2. **Menu/Name Text**: Standard ASCII lowercase (`0x61-0x7A`)

Character names (Chaz, Alys, Hahn, etc.) use **standard ASCII** in menu data, while dialogue uses the custom encoding. This discovery was essential for successful text extraction.

### Dynamic Text Insertion System

Character names **never appear literally** in dialogue. Instead, runtime insertion symbols are used:

| Symbol | Function | Frequency |
|--------|----------|-----------|
| `!` | Insert hero name (Chaz) | 1,934x |
| `"` | Insert party member name | 5,143x |
| `#` | Insert item name | 5,880x |
| `&` | Insert monster/entity name | 4,483x |
| `'` | Insert technique/spell name | 2,329x |

### Page Break Code

The `555` sequence (`0x35 0x35 0x35`) appears 1,550 times and functions as a **dialogue box transition** indicator:
- Before `[CLEAR]` (82x) = "Clear box and continue"
- Before `[END]` (36x) = "End after this box"
- Before `[BR]` (31x) = "New page/new box"

---

## Major Discoveries

| # | Discovery | Impact |
|---|-----------|--------|
| 1 | **Dual Encoding** | Dialogue and menus use different character sets |
| 2 | **Dynamic Insertion** | Names use `!"#&'` symbols, not literal text |
| 3 | **555 Page Break** | Box transition code for Working Designs expanded text |
| 4 | **Font at 0x117603** | 1,024 tiles (1bpp) / 256 tiles (4bpp) confirmed |
| 5 | **Dialogue Regions** | 25 regions totaling ~152 KB in 0x200000+ |
| 6 | **212 Pointers** | References to 0x200000 found throughout ROM |
| 7 | **ASCII Names** | Character names found in standard ASCII at 0x09C3FE+ |
| 8 | **17 Dialogue Regions** | 64KB each at 0x200000-0x310000 |
| 9 | **~1,000 Palette Sets** | Auto-detected across full ROM |

---

## Repository Structure

```
psiv-wd-clawed-fable/
|
|-- Documentation
|   |-- README.md                      # This file
|   |-- HANDOFF.md                     # Phase 1 -> Phase 2 handoff guide
|   |-- PLAN.md                        # 24-hour production rebuild plan
|   |-- CLAUDE_FABLE_PROMPT.md         # AI auditor/implementer prompt
|   |-- REBUILD_GUIDE.md               # Technical rebuild documentation
|   |-- MASTER_INDEX.md                # Complete ROM offset map (0x000000-0x310494)
|   |-- FINAL_SUMMARY.md               # Complete extraction report
|   |-- ROM_Reverse_Engineering_Skill_Set_v1.0.0.md
|   |-- graphics_index.md              # Graphics asset catalog
|   |-- palettes_refined.md            # Refined palette catalog
|
|-- Character Encoding
|   |-- psiv.tbl                       # Complete 0x00-0xFF character table
|
|-- Data Tables (CSV)
|   |-- data_tables/
|   |   |-- items.csv                  # 162 item entries
|   |   |-- enemies.csv                # 256 enemy entries
|   |   |-- techniques.csv             # 40 techniques
|   |   |-- skills.csv                 # 47 skills
|
|-- Graphics Assets
|   |-- graphics_raw/                  # Raw binary dumps from ROM
|   |   |-- dungeon_data_0x24B2BC.bin.b64    # 2001 bytes, offset 0x24B2BC
|   |   |-- font_tiles_0x117603.bin.b64      # 8196 bytes, offset 0x117603
|   |   |-- menu_ui_patterns_0x00C3EA.bin.b64 # 2941 bytes, offset 0x00C3EA
|   |   |-- structured_data_0_0x2AA29E.bin.b64 # 2169 bytes, offset 0x2AA29E
|   |   |-- tile_patterns_0_0x1155C4.bin.b64  # 8206 bytes, offset 0x1155C4
|   |   |-- compressed_graphics_0_0x24EF1D.bin # 2004 bytes, offset 0x24EF1D
|   |
|   |-- font_raw_4bpp.bin.b64          # Raw font tile data (8196 bytes)
|   |-- font_preview_1bpp.png          # Font tile visualization (1bpp)
|   |-- font_preview_4bpp.png.b64      # Font tile visualization (4bpp)
|   |-- font_row_0.png ... font_row_7.png    # Individual font rows
|   |-- font_row0_zoom.png             # Zoomed Row 0 (custom chars)
|   |-- font_row3_zoom.png             # Zoomed Row 3 (lowercase)
|   |-- font_tiles_00-1F.png           # First 32 tiles
|   |-- font_tiles_01-1F_labeled.png   # Custom character set labeled
|   |-- palettes_raw.bin.b64           # All extracted palettes (~922 KB)
|   |-- palettes.txt.b64               # Human-readable palette list
|
|-- Dialogue (Generated by Script)
|   |-- dialogue_by_scene/             # 35 individual scene files
|   |   |-- scene_000.txt              # (placeholder - run regenerate_all.py)
|   |   |-- scene_001.txt              # ...
|   |   |-- ...                        # scene_002 through scene_034
|   |-- dialogue_full.txt              # All dialogue merged (~219 KB)
|
|-- Python Toolkit
|   |-- scripts/
|   |   |-- regenerate_all.py          # Master: regenerates ALL assets from ROM
|   |   |-- decode_b64.py              # Decodes .b64 files back to binary
|   |   |-- extract_text.py            # Dialogue dumper with custom encoding
|   |   |-- extract_tiles.py           # 4bpp/1bpp tile extractor + PNG
|   |   |-- insert_text.py             # Text inserter with checksum fix
|
|-- Legacy / Reference
    |-- push_binaries.sh               # Binary push helper (development use)
```

---

## Binary File Handling

**Important**: The GitHub MCP upload tool cannot store raw binary files correctly (they get corrupted during UTF-8 encoding). Therefore, all binary files in this repository are stored as **base64-encoded text files** with a `.b64` extension.

### To Decode .b64 Files

```bash
# Decode a single file
python scripts/decode_b64.py graphics_raw/font_tiles_0x117603.bin.b64

# Decode ALL .b64 files in the repository
python scripts/decode_b64.py --all
```

### To Regenerate Everything from ROM

The recommended approach is to use `regenerate_all.py`, which extracts all assets directly from your ROM file:

```bash
# Regenerate all extracted assets
python scripts/regenerate_all.py "Phantasy Star Gen4.bin" ./

# Output includes:
#   - graphics_raw/*.bin (all binary dumps)
#   - font_preview_4bpp.png
#   - palettes_raw.bin + palettes.txt
#   - dialogue_by_scene/scene_000.txt through scene_034.txt
#   - dialogue_full.txt
```

---

## Character Encoding Table

### Confirmed Mappings (21/26 letters)

| Byte | Char | Confidence | Evidence |
|------|------|------------|----------|
| 0x0F | **y** | HIGH | "My" pattern at 0x09C3FE |
| 0x17 | **h** | Medium-High | "he" bigram 44x |
| 0x1B | **a** | HIGH | 457 single-word uses |
| 0x1C | **i** | Medium-High | Frequency rank 5 |
| 0x1D | **o** | Medium-High | Frequency rank 4 |
| 0x1E | **t** | HIGH | Frequency rank 3, "tea" pattern |
| 0x1F | **e** | HIGH | 9,017 occurrences (most frequent) |

Full table in [`psiv.tbl`](psiv.tbl).

### Unconfirmed (5/26 letters)

| Byte | Status | Occurrences |
|------|--------|-------------|
| 0x15 | UNCONFIRMED | 20x |
| 0x16 | UNCONFIRMED | 16x |
| 0x18 | UNCONFIRMED | 2x |
| 0x19 | UNCONFIRMED | 112x |
| 0x1A | UNCONFIRMED | 89x |

---

## Control Codes Reference

| Code | Name | Function |
|------|------|----------|
| 0x00 | SEP | Word/phrase separator |
| 0x20 | SPC | Literal space |
| 0xFC | BR | Line break |
| 0xFD | CLEAR | Clear text window |
| 0xFB | SPACE | Add vertical spacing |
| 0xFE | FE | Unknown formatting |
| 0xFF | END | End of string |

### Portrait Codes

| Code | Portrait | Frequency |
|------|----------|-----------|
| `0)/` | Portrait 0 | Rare |
| `1)/` | Portrait 1 | 77x |
| `3)/` | Portrait 3 | 1,175x (most common) |
| `5)/` | Portrait 5 | 6x |

---

## Dialogue Extraction

- **17 dialogue regions** extracted totaling ~219 KB
- **79.8% decoding success rate** with current character map
- Full dialogue regenerated by `scripts/regenerate_all.py`
- Per-scene files in `dialogue_by_scene/` (generated by script)

### Extraction Method

```bash
# Extract all dialogue + assets
python scripts/regenerate_all.py "rom.bin" ./

# Or extract specific region with original tool
python scripts/extract_text.py "rom.bin" output/
```

### Dialogue Region Map

| Scene | Offset | Description |
|-------|--------|-------------|
| 000 | 0x200000 | Prologue / Opening |
| 001 | 0x210000 | Early Game |
| 002 | 0x220000 | Mid Game A |
| 003 | 0x230000 | Mid Game B |
| 004 | 0x240000 | Late Game |
| 005 | 0x250000 | Endgame |
| 006-010 | 0x260000-0x2A0000 | Side Quests, NPC Dialogue |
| 011-015 | 0x2B0000-0x2F0000 | Battle Text, Items, Enemies |
| 016 | 0x300000 | Credits / Ending |

---

## Font & Graphics

### Font Location

| Property | Value |
|----------|-------|
| **Offset** | 0x117603 |
| **Size** | 8,196 bytes |
| **1bpp Tiles** | 1,024 (8x8 pixels) |
| **4bpp Tiles** | 256 (8x8 pixels) |
| **Layout** | 256x256 pixel sheet |

### Character Set Distribution

| Row | Range | Content |
|-----|-------|---------|
| Row 0 | 0x00-0x1F | Custom characters + control glyphs |
| Row 1 | 0x20-0x3F | ASCII punctuation and digits |
| Row 2 | 0x40-0x5F | ASCII uppercase A-Z |
| Row 3 | 0x60-0x7F | ASCII lowercase a-z |
| Rows 4-7 | 0x80-0xFF | Extended/special characters |

### Graphics Extraction

```bash
# Extract font as 1bpp PNG
python scripts/extract_tiles.py "rom.bin" 0x117603 8196 1 font_1bpp.png

# Extract font as 4bpp PNG
python scripts/extract_tiles.py "rom.bin" 0x117603 8196 4 font_4bpp.png

# Extract any tile region
python scripts/extract_tiles.py "rom.bin" 0x1155C4 8196 4 tiles.png
```

---

## Rebuild Toolkit

### Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `regenerate_all.py` | **Master extraction** - generates all assets | `python regenerate_all.py rom.bin ./` |
| `decode_b64.py` | Decode .b64 files back to binary | `python decode_b64.py --all` |
| `extract_text.py` | Dump dialogue with custom encoding | `python extract_text.py rom.bin output/` |
| `extract_tiles.py` | Extract graphics to PNG | `python extract_tiles.py rom.bin offset size bpp output.png` |
| `insert_text.py` | Insert text + fix checksum | `python insert_text.py text.txt rom.bin offset` |

### Checksum Fix

```python
def update_checksum(rom_path):
    with open(rom_path, 'r+b') as f:
        f.seek(0x200)
        data = f.read()
        checksum = sum(data) & 0xFFFF
        f.seek(0x18E)
        f.write(checksum.to_bytes(2, 'big'))
    return checksum
```

---

## Advanced Graphics Options

### Option 1: 4x AI-Upscaled Tiles (Recommended)
- **Technique**: Extract all 4bpp tiles -> AI upscale 4x -> reconvert to Genesis 4bpp
- **Tools**: ESRGAN/Real-ESRGAN for pixel art, tile-specific models
- **VRAM Impact**: Original tiles load unchanged; enhanced versions need bankswitching
- **Effort**: High (each tileset needs individual processing)

### Option 2: Expanded Color Palettes
- **Technique**: Optimize Genesis 4-palette system (64 colors total)
- **Method**: Increase color depth within 0x000-0xEEE range, add intermediate shades
- **VRAM Impact**: None (palette data is tiny)
- **Effort**: Low (automated palette enhancement)

### Option 3: HD Font Replacement
- **Technique**: Replace 8x8 font with enhanced 8x16 or variable-width font
- **Method**: Redesign font tiles at 0x117603 with sharper glyphs
- **VRAM Impact**: Minimal (font is small)
- **Effort**: Medium (font design + width table adjustments)

### Option 4: Widescreen Hack (16:9)
- **Technique**: Expand viewport, adjust tilemap loading for wider screen
- **Method**: Modify VDP register settings, adjust camera code
- **VRAM Impact**: Requires more tile loading per frame
- **Effort**: Very High (engine-level modifications)

### Option 5: Full Sprite Enhancement
- **Technique**: AI-upscale all character and enemy sprites
- **Tools**: Sprite-focused GAN models, manual cleanup
- **VRAM Impact**: May require sprite multiplexing or reduced on-screen count
- **Effort**: Very High (hundreds of sprites to process)

### Recommended Implementation Order
1. **Option 3** (HD Font) - Quick win, minimal risk
2. **Option 2** (Color Enhancement) - Automated, instant improvement
3. **Option 1** (AI Upscale) - Major visual upgrade for backgrounds
4. **Option 5** (Sprite Enhancement) - Character-focused upgrade
5. **Option 4** (Widescreen) - Long-term stretch goal

---

## Handoff to Phase 2

See [`HANDOFF.md`](HANDOFF.md) for complete Phase 1 -> Phase 2 transition documentation.

See [`PLAN.md`](PLAN.md) for the production rebuild plan (24-hour 5-phase approach).

See [`CLAUDE_FABLE_PROMPT.md`](CLAUDE_FABLE_PROMPT.md) for the AI auditor/implementer prompt.

See [`REBUILD_GUIDE.md`](REBUILD_GUIDE.md) for technical rebuild documentation with VRAM constraints and format specifications.

---

## Technical Notes

### Genesis Graphics Formats

| Format | Spec | Used For |
|--------|------|----------|
| 4bpp Tile | 32 bytes, 8x8px, packed pixels | Backgrounds, font, UI |
| 1bpp Tile | 8 bytes, 8x8px, 1 bit/pixel | Simplified graphics |
| Palette | 32 bytes, 16 colors, 0BGR 9-bit | Color lookup |
| VRAM | 64 KB total | Tile storage + nametables |

### ROM Header Info

| Field | Offset | Value |
|-------|--------|-------|
| Console | 0x100 | "SEGA GENESIS" |
| Serial | 0x180 | "GM MK-1307 " |
| Checksum | 0x18E | 0xNNNN (recalculate after edits) |
| ROM Start | 0x1A0 | 0x000000 |
| ROM End | 0x1A4 | 0x3101FF |

---

## Credits

- **ROM Analysis & Extraction**: Automated tooling with manual verification
- **Working Designs**: Original localization style being preserved
- **Sega**: Original game (C)SEGA 1994
- **Tools**: Python, PIL, custom Genesis format decoders

---

*This is a fan project for preservation and educational purposes. All game content copyright Sega.*

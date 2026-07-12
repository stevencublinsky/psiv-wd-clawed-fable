# Phantasy Star IV: Clawed Fable - Graphical Enhancement Rebuild

> **Project Status**: Phase 1 Complete (ROM Analysis & Extraction) | Phase 2 In Progress (Graphical Rebuild)

A complete reverse-engineering, extraction, and graphical enhancement project for *Phantasy Star IV: The End of the Millennium* (Working Designs 6.01 patch) on the Sega Genesis/Mega Drive.

---

## Table of Contents

- [Project Overview](#project-overview)
- [Major Discoveries](#major-discoveries)
- [Repository Structure](#repository-structure)
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
| **Status** | Phase 1 Complete - Extraction |

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

---

## Repository Structure

```
psiv-wd-clawed-fable/
├── README.md                      # This file
├── HANDOFF.md                     # Phase 1 -> Phase 2 handoff
├── PLAN.md                        # Production rebuild plan
├── CLAUDE_FABLE_PROMPT.md         # Prompt for AI auditor/implementer
├── psiv.tbl                       # Character encoding table
├── FINAL_SUMMARY.md               # Complete extraction report
├── REBUILD_GUIDE.md               # Rebuild documentation
├── MASTER_INDEX.md                # Full ROM offset map
├── dialogue_full.txt              # All extracted dialogue (~219 KB)
├── dialogue_by_scene/             # 35 individual scene files
├── graphics_raw/                  # Raw graphics dumps
│   ├── font_tiles_0x117603.bin
│   ├── tile_patterns_0x1155C4.bin
│   ├── menu_ui_patterns_0x00C3EA.bin
│   ├── structured_data_0_0x2AA29E.bin
│   ├── compressed_graphics_0_0x24EF1D.bin
│   └── dungeon_data_0_0x24B2BC.bin
├── graphics_previews/             # Visual font previews
│   ├── font_preview_1bpp.png
│   ├── font_preview_4bpp.png
│   ├── font_row_0.png ... font_row_7.png
│   ├── font_row0_zoom.png
│   ├── font_row3_zoom.png
│   └── font_tiles_01-1F_labeled.png
├── palettes_raw.bin               # Extracted palette data
├── palettes.txt                   # Human-readable palettes
├── data_tables/
│   ├── items.csv                  # 162 item entries
│   ├── enemies.csv                # 256 enemy entries
│   ├── techniques.csv             # 40 techniques
│   └── skills.csv                 # 47 skills
└── scripts/                       # Python toolkit
    ├── extract_text.py            # Dialogue dumper
    ├── extract_tiles.py           # Graphics extractor
    └── insert_text.py             # Text inserter + checksum fix
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

- **25 dialogue regions** extracted totaling ~152 KB
- **79.8% decoding success rate** with current character map
- Full dialogue in [`dialogue_full.txt`](dialogue_full.txt)
- Per-scene files in [`dialogue_by_scene/`](dialogue_by_scene/)

### Extraction Method

```bash
# Extract all dialogue
python scripts/extract_text.py "rom.bin" output/

# Extract specific region
python scripts/extract_text.py "rom.bin" output/ --offset 0x200000
```

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
```

---

## Rebuild Toolkit

### Scripts

| Script | Purpose | Usage |
|--------|---------|-------|
| `extract_text.py` | Dump dialogue | `python extract_text.py rom.bin output/` |
| `extract_tiles.py` | Extract graphics | `python extract_tiles.py rom.bin offset size bpp output.png` |
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

See [`PLAN.md`](PLAN.md) for the production rebuild plan.

See [`CLAUDE_FABLE_PROMPT.md`](CLAUDE_FABLE_PROMPT.md) for the AI auditor/implementer prompt.

---

## Credits

- **ROM Analysis & Extraction**: Automated tooling with manual verification
- **Working Designs**: Original localization style being preserved
- **Sega**: Original game (C)SEGA 1994
- **Tools**: Python, PIL, custom Genesis format decoders

---

*This is a fan project for preservation and educational purposes. All game content copyright Sega.*

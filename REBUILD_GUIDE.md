# Phantasy Star IV: Working Designs 6.01 - Rebuild Guide v2.0

## ROM Information

| Property | Value |
|----------|-------|
| **Game** | Phantasy Star IV: The End of the Millennium |
| **Version** | Working Designs 6.01 (Fan Patch) |
| **Platform** | Sega Genesis/Mega Drive |
| **Serial** | GM MK-1307 |
| **Size** | 3,209,748 bytes (3.06 MB / ~3134 KB) |
| **Format** | Raw Binary (.bin) |
| **Header** | 0x100 (Standard Sega header) |
| **Checksum (stored)** | 0x16F7 |
| **Checksum (actual)** | 0xA496 [MODIFIED - Working Designs Patch] |

## Text Encoding System (v2.0)

### CRITICAL DISCOVERY: Dual Encoding System

The ROM uses **TWO DIFFERENT** text encodings:

1. **Dialogue Text**: Custom encoding (0x01-0x1F for lowercase)
2. **Menu/Name Text**: Standard ASCII lowercase (0x61-0x7A)

Character names (Chaz, Alys, Hahn, etc.) use **standard ASCII** in menu data, while dialogue uses the custom encoding.

### Custom Character Table (Dialogue Text Only)

| Byte | Char | Confidence | Evidence |
|------|------|------------|----------|
| 0x01 | n | Medium | Freq rank 6 |
| 0x02 | c | Medium | Freq rank 12 |
| 0x03 | m | Medium | Freq rank 14 |
| 0x04 | l | Medium | Freq rank 11 |
| 0x05 | j | Medium | Freq rank 24 |
| 0x06 | p | Medium | Freq rank 16 |
| 0x07 | b | Medium | Freq rank 20 |
| 0x08 | d | Medium | Freq rank 10 |
| 0x09 | s | Medium | Freq rank 7 |
| 0x0A | q | Medium | Freq rank 25 |
| 0x0B | z | Medium | Freq rank 26 |
| 0x0C | v | Medium | Freq rank 21 |
| 0x0D | w | Medium | Freq rank 18 |
| 0x0E | x | Medium | Freq rank 23 |
| **0x0F** | **y** | **HIGH** | **Confirmed from \"My\" pattern** |
| 0x10 | g | Medium | Freq rank 17 |
| 0x11 | k | Medium | Freq rank 22 |
| 0x12 | f | Medium | Freq rank 19 |
| 0x13 | u | Medium | Freq rank 13 |
| 0x14 | r | Medium | Freq rank 9 |
| **0x15** | **?** | **UNCONFIRMED** | Rare (20x) |
| **0x16** | **?** | **UNCONFIRMED** | Rare (16x) |
| **0x17** | **h** | **Medium-High** | **0x17 0x1F = \"he\" (44x, common bigram)** |
| **0x18** | **?** | **UNCONFIRMED** | Extremely rare (2x) |
| **0x19** | **?** | **UNCONFIRMED** | Rare (112x) |
| **0x1A** | **?** | **UNCONFIRMED** | Rare (89x) |
| **0x1B** | **a** | **HIGH** | **Most common single-byte word (457x)** |
| **0x1C** | **i** | **Medium-High** | **Frequency rank 5** |
| **0x1D** | **o** | **Medium-High** | **Frequency rank 4** |
| **0x1E** | **t** | **HIGH** | **Frequency rank 3, \"tea\" pattern** |
| **0x1F** | **e** | **HIGH** | **Most common (9017x) = most common letter** |

### Control Codes

| Code | Function | Context |
|------|----------|---------|
| 0x00 | Word/phrase separator | Between words |
| 0x20 | Space | Literal space |
| 0xFC | Line break | New line in text box |
| 0xFD | Clear window | Clear text and continue |
| 0xFB | Add spacing | Vertical spacing |
| 0xFE | Unknown control | Formatting control |
| 0xFF | End of string | Terminates text |

### Page Break Code (NEW DISCOVERY)

| Pattern | Function | Frequency |
|---------|----------|-----------|
| `555` (0x35 0x35 0x35) | **Dialogue box transition** | 1,550x |

The `555` code appears:
- Before `[CLEAR]` (82x) = "Clear box and continue"
- Before `[END]` (36x) = "End after this box"
- Before line break (31x) = "New page"

This is the **dialogue page break** indicator used when text fills a box.

### Dynamic Text Insertion (NEW DISCOVERY)

Character names do NOT appear literally in dialogue. They use **insertion codes**:

| Symbol | Function | Frequency |
|--------|----------|------|
| `!` | Insert hero name (Chaz) | 1,934x |
| `"` | Insert party member | 5,143x |
| `#` | Insert item name | 5,880x |
| `&` | Insert monster name | 4,483x |
| `'` | Insert technique | 2,329x |

The game replaces these symbols at runtime with the appropriate name from a lookup table.

### Portrait Codes

| Code | Portrait | Frequency |
|------|----------|------|
| `0)/` | Portrait 0 | Rare |
| `1)/` | Portrait 1 | 77x |
| `3)/` | Portrait 3 | 1,175x (most common) |
| `5)/` | Portrait 5 | 6x |

## Graphics Format

### Font Tiles
- **Location**: 0x117603-0x119607 (8,196 bytes)
- **Format**: 1bpp (8 bytes per 8x8 tile) = 1,024 tiles
- **Alternative**: 4bpp (32 bytes per 8x8 tile) = 256 tiles
- **Layout**: 16x16 grid of character tiles (256x256 pixels)

**Character Set Distribution:**
- Row 0 (0x00-0x1F): Custom characters + control glyphs
- Row 1 (0x20-0x3F): ASCII punctuation and digits
- Row 2 (0x40-0x5F): ASCII uppercase A-Z + more punctuation
- Row 3 (0x60-0x7F): ASCII lowercase a-z + punctuation
- Rows 4-7 (0x80-0xFF): Extended/special characters

### Tile Data Format
- **4bpp Packed Pixel**: 32 bytes per 8x8 tile
  - Each byte: [pixel0 (high nibble), pixel1 (low nibble)]
  - Linear storage: row 0, row 1, ..., row 7
- **1bpp**: 8 bytes per 8x8 tile, 1 bit per pixel

### Palette Format
- **Size**: 32 bytes per palette (16 colors x 2 bytes)
- **Color Format**: 0BGR (9-bit color, each channel 0-0xE)
- **RGB Conversion**: R=(color&0xF)*17, G=((color>>4)&0xF)*17, B=((color>>8)&0xF)*17

## Dialogue Text Regions

| Region | Offset Range | Size | Notes |
|--------|-------------|------|-------|
| 0 | 0x200000-0x200515 | 1,301 | |
| 1 | 0x20076D-0x201BDC | 5,231 | |
| 2 | 0x201CA4-0x203063 | 5,055 | |
| 3 | 0x2030C7-0x204527 | 5,216 | |
| 4 | 0x2045EF-0x2060CE | 6,879 | |
| ... | ... | ... | 25 total regions |
| **Total** | **0x200000-0x310494** | **~152 KB** | Working Designs expanded script |

## VRAM Constraints

- **Total VRAM**: 64 KB
- **Tile Memory**: ~32 KB loadable at once
- **Max Tiles**: ~1,024 (8x8 4bpp)
- **Palettes**: 4 lines of 16 colors each

## Pointer Tables (Partial Data)

- **212 references** to 0x200000 found in ROM
- Pointer format: Likely 3-byte (24-bit) or 4-byte (32-bit) big-endian addresses
- Common location for pointer tables: Near start of ROM (0x000000-0x010000)
- Dialogue pointer tables may be interleaved with code

## Rebuild Checklist

### Before Modifying
- [ ] Make backup of original ROM
- [ ] Verify checksum mismatch indicates patch (not corruption)
- [ ] Document all changes

### Text Modifications
- [ ] Edit `dialogue_by_scene/*.txt` files
- [ ] **Preserve all control codes**: `[BR]`, `[CLEAR]`, `[END]`, `[555]`
- [ ] **Preserve dynamic insertion symbols**: `!`, `"`, `#`, `&`, `'``
- [ ] **Preserve portrait codes**: `X)/` format
- [ ] Ensure new text fits within original region size
- [ ] Use lowercase mapping from `psiv.tbl` for new dialogue text

### Graphics Modifications
- [ ] Use `extract_tiles.py` to dump current tiles
- [ ] Edit tiles (maintain 4bpp Genesis format)
- [ ] Re-insert tiles at original offsets
- [ ] Update palette data if colors change

### Critical: Working Designs Style Notes
- Dialogue is **heavily expanded** compared to original Sega translation
- Contains **pop culture references** and **snarky humor**
- Text uses **lots of punctuation** for comedic timing
- **555 codes** indicate where the original had shorter text
- Preserve the WD humor style when editing

### After Modifications
- [ ] Recalculate ROM checksum at offset 0x18E
- [ ] Formula: `(sum of all bytes from 0x200 to end) & 0xFFFF`
- [ ] Update ROM end address at 0x1A4 if size changed
- [ ] Test in emulator (BlastEm, Genesis Plus GX, Kega Fusion)

### Testing Checklist
- [ ] Verify title screen displays correctly
- [ ] Check all dialogue boxes for formatting
- [ ] Test all portrait codes display correct faces
- [ ] Verify dynamic name insertion works (`!`, `"`, `#`, `&`)
- [ ] Verify item/technique names appear correctly
- [ ] Check for text overflow in dialogue windows
- [ ] Test 555 page break transitions
- [ ] Play through first dungeon to verify all text

## File Structure

```
/mnt/agents/output/
├── psiv.tbl                    # Character encoding table v2.0
├── dialogue_full.txt           # All extracted dialogue
├── dialogue_by_scene/          # Per-scene dialogue files (35 scenes)
├── graphics_raw/               # Raw graphics regions
│   ├── tile_patterns_0x1155C4.bin
│   ├── font_tiles_0x117603.bin
│   └── ...
├── graphics_index.md           # Graphics region catalog
├── palettes_raw.bin            # Extracted palette data
├── palettes.txt                # Human-readable palettes
├── palettes_refined.txt        # Filtered palette list
├── font_preview_1bpp.png       # Font tile visualization (1bpp)
├── font_preview_4bpp.png       # Font tile visualization (4bpp)
├── font_row_*.png              # Individual font rows
├── items.csv                   # Item data table (placeholder)
├── enemies.csv                 # Enemy data table (placeholder)
├── techniques.csv              # Technique data table
├── skills.csv                  # Skill data table
├── scripts/                    # Python toolkit
│   ├── extract_text.py         # Dialogue dumper
│   ├── extract_tiles.py        # Graphics extractor
│   └── insert_text.py         # Text inserter
├── REBUILD_GUIDE.md            # This file
└── MASTER_INDEX.md             # Complete offset map
```

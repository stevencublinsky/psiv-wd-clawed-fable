# Phantasy Star IV: Working Designs 6.01 - Master Index v2.0

## ROM Overview

```
File: Phantasy Star Gen4 - Working Designs 6.01.md
Size: 3,209,748 bytes (0x310494)
Format: Sega Genesis Raw Binary
Serial: GM MK-1307
Checksum (stored): 0x16F7
Checksum (actual): 0xA496 [MODIFIED - Working Designs Patch]
```

## Complete Memory Map

```
0x000000-0x0001FF   Vector Table + ROM Header (512 bytes)
0x000200-0x0FFFFF   Game Code & Engine (1,048,064 bytes)
  0x000200-0x005000   Boot code & initialization
  0x005000-0x020000   Main game engine
  0x020000-0x040000   Battle system
  0x040000-0x060000   Menu system
  0x060000-0x080000   Field/map system
  0x080000-0x0A0000   Event scripting
  0x0A0000-0x0C0000   Graphics engine
  0x0C0000-0x0E0000   Sound driver (ZMFs, PSG, PCM)
  0x0E0000-0x0FFFFF   Data processing

0x100000-0x120000   Graphics Bank 0: Tilesets & Fonts (131,072 bytes)
  0x100000-0x110000   Background tilesets
  0x110000-0x1155C4   Sprite patterns
  0x1155C4-0x1175D2   UI tile patterns (8,206 bytes)
  0x117603-0x119607   FONT TILES (8,196 bytes)
  0x119607-0x120000   Additional graphics

0x120000-0x180000   Graphics Bank 1: Sprites & Characters (393,216 bytes)
0x180000-0x200000   Graphics Bank 2: Backgrounds & Maps (524,288 bytes)

0x200000-0x310000   SCRIPT & DIALOGUE TEXT (~1,048,576 bytes)
  0x200000-0x207000   Dialogue Region Set 1
  0x207000-0x210000   Dialogue Region Set 2
  0x210000-0x218000   Dialogue Region Set 3
  0x218000-0x220000   Dialogue Region Set 4
  0x220000-0x228000   Dialogue Region Set 5
  0x228000-0x230000   Dialogue Region Set 6
  0x230000-0x238000   Dialogue Region Set 7
  0x238000-0x240000   Dialogue Region Set 8
  0x240000-0x248000   Dialogue Region Set 9
  0x248000-0x250000   Dialogue Region Set 10
  0x250000-0x258000   Dialogue Region Set 11
  0x258000-0x260000   Dialogue Region Set 12
  0x260000-0x268000   Dialogue Region Set 13
  0x268000-0x270000   Dialogue Region Set 14
  0x270000-0x278000   Dialogue Region Set 15
  0x278000-0x280000   Dialogue Region Set 16
  0x280000-0x288000   Dialogue Region Set 17
  0x288000-0x290000   Dialogue Region Set 18
  0x290000-0x298000   Dialogue Region Set 19
  0x298000-0x2A0000   Dialogue Region Set 20
  0x2A0000-0x2A8000   Dialogue Region Set 21
  0x2A8000-0x2B0000   Dialogue Region Set 22
  0x2B0000-0x2B8000   Dialogue Region Set 23
  0x2B8000-0x2C0000   Dialogue Region Set 24
  0x2C0000-0x2C8000   Dialogue Region Set 25

0x300000-0x310000   Patch Data & Extended Content (65,536 bytes)
  0x300000-0x308000   Working Designs patch overlay
  0x308000-0x310000   Additional data / padding

0x310000-0x310494   Unused / padding (1,172 bytes)
```

## Key Data Structures

### Font Tile Data
- **Offset**: 0x117603
- **Size**: 8,196 bytes
- **Format**: 1bpp (1,024 tiles) or 4bpp (256 tiles)
- **Layout**: 256x256 pixel sheet, 8x8 tiles

### Character Stats (SRAM Offsets)

| Character | Level | HP | TP | Stats |
|-----------|-------|-----|-----|-------|
| Chaz | 0x11981 | 0x11986 | 0x1198A | 0x11990 |
| Alys | 0x11A01 | 0x11A06 | 0x11A0A | 0x11A10 |
| Hahn | 0x11A81 | 0x11A86 | 0x11A8A | 0x11A90 |
| Rune | 0x11B01 | 0x11B06 | 0x11B0A | 0x11B10 |
| Gryz | 0x11B81 | 0x11B86 | 0x11B8A | 0x11B90 |
| Rika | 0x11C01 | 0x11C06 | 0x11C8A | 0x11C10 |
| Demi | 0x11C81 | 0x11C86 | 0x11C8A | 0x11C90 |
| Wren | 0x11D01 | 0x11D06 | 0x11D0A | 0x11D10 |
| Raja | 0x11D81 | 0x11D86 | 0x11D8A | 0x11D90 |
| Kyra | 0x11E01 | 0x11E06 | 0x11E0A | 0x11E10 |
| Seth | 0x11E81 | 0x11E86 | 0x11E8A | 0x11E90 |

### Item Data
- **Count**: 162 items (IDs 0x00-0xA1)
- **ROM Offset**: Unknown (likely 0x200000-0x280000 range)
- **Format**: Variable-length entries with name pointer, type, effect, price

### Technique Data
- **Count**: 40 techniques
- **Categories**: Fire (Foi), Water (Wat), Wind (Zan), Earth (Gra), Heal (Res), etc.

### Skill Data
- **Count**: 47 skills
- **Format**: ATP cost, TP cost, effect byte, target type

## Text Encoding Reference

### Control Codes

| Byte | Name | Function |
|------|------|----------|
| 0x00 | SEP | Word/phrase separator |
| 0x20 | SPC | Literal space |
| 0xFC | BR | Line break |
| 0xFD | CLEAR | Clear text window |
| 0xFB | SPACE | Add vertical spacing |
| 0xFE | FE | Unknown formatting |
| 0xFF | END | End of text string |

### Page Break Code

| Pattern | Function | Frequency |
|---------|----------|-----------|
| `555` | Dialogue box transition | 1,550x |

Context analysis:
- `[555] [CLEAR]` (82x) = "Clear box and continue"
- `[555] [END]` (36x) = "End after this box"
- `[555] [BR]` (31x) = "New page/new box"

### Dynamic Text Insertion

| Symbol | Function | Freq |
|--------|----------|------|
| `!` | Insert hero name | 1,934x |
| `"` | Insert party member | 5,143x |
| `#` | Insert item name | 5,880x |
| `&` | Insert monster name | 4,483x |
| `'` | Insert technique | 2,329x |

### Portrait Codes

| Code | Portrait | Freq |
|------|----------|------|
| `0)/` | Portrait 0 | Rare |
| `1)/` | Portrait 1 | 77x |
| `3)/` | Portrait 3 | 1,175x |
| `5)/` | Portrait 5 | 6x |

## Known Text Offsets

| Offset | Content | Notes |
|--------|---------|-------|
| 0x100 | ROM Header | Standard Sega header |
| 0x09C3FE | "My" pattern | Confirms 0x0F='y' (ASCII lowercase) |
| 0x117603 | Font tiles | 8,196 bytes of tile data |
| 0x15DF5E | Alphabet block | A-Z and a-e sequence |
| 0x200000+ | Dialogue text | 25 regions, ~152 KB total |

## Graphics Regions

| Offset | Size | Content |
|--------|------|---------|
| 0x1155C4 | 8,206 | UI tile patterns |
| 0x117603 | 8,196 | **Font tiles** |
| 0x00C3EA | 2,941 | Menu UI patterns |
| 0x2AA29E | 2,169 | Structured data table |
| 0x24EF1D | 2,004 | Compressed graphics |
| 0x24B2BC | 2,001 | Dungeon data |

## Palette Data
- **Total palettes found**: 28,833 potential blocks
- **Palette clusters**: 1,564 (4+ consecutive palettes)
- **Format**: 32 bytes per palette (16 colors x 2 bytes, 0BGR)

## Tools Reference

| Script | Purpose | Usage |
|--------|---------|-------|
| `extract_text.py` | Dump dialogue | `python extract_text.py rom.bin output/` |
| `extract_tiles.py` | Extract graphics | `python extract_tiles.py rom.bin offset size bpp output.png` |
| `insert_text.py` | Insert text + fix checksum | `python insert_text.py text.txt rom.bin offset` |

## Checksums

```python
def calculate_checksum(rom_data):
    return sum(rom_data[0x200:]) & 0xFFFF

def update_checksum(rom_path):
    with open(rom_path, 'r+b') as f:
        f.seek(0x200)
        data = f.read()
        checksum = sum(data) & 0xFFFF
        f.seek(0x18E)
        f.write(checksum.to_bytes(2, 'big'))
    return checksum
```

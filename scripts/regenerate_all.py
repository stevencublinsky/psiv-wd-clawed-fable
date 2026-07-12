#!/usr/bin/env python3
"""
PSIV Clawed Fable - Complete Asset Regeneration Script
Extracts all graphics, fonts, palettes, and dialogue from the Phantasy Star IV ROM.

Usage:
    python regenerate_all.py <rom_file> [output_dir]

This regenerates all extracted files that are in the repository,
so you don't need to download large binary files.
"""

import sys
import struct
from pathlib import Path
from PIL import Image

# ROM offsets for all extractable assets
ASSETS = {
    # Fonts
    'font_raw_4bpp.bin':      {'offset': 0x117603, 'size': 0x2004, 'type': 'raw'},
    'font_tiles_0x117603.bin': {'offset': 0x117603, 'size': 0x2004, 'type': 'raw'},
    
    # Graphics patterns  
    'tile_patterns_0_0x1155C4.bin': {'offset': 0x1155C4, 'size': 0x2002, 'type': 'raw'},
    
    # Menu/UI data
    'menu_ui_patterns_0x00C3EA.bin': {'offset': 0x00C3EA, 'size': 0x0B7D, 'type': 'raw'},
    
    # Dungeon and structured data
    'dungeon_data_0x24B2BC.bin': {'offset': 0x24B2BC, 'size': 0x07D1, 'type': 'raw'},
    'structured_data_0_0x2AA29E.bin': {'offset': 0x2AA29E, 'size': 0x0879, 'type': 'raw'},
    
    # Compressed graphics
    'compressed_graphics_0_0x24EF1D.bin': {'offset': 0x24EF1D, 'size': 0x07D4, 'type': 'raw'},
}

DIALOGUE_REGIONS = [
    # (start_offset, description)
    (0x200000, "Dialogue Region 1 - Prologue/Opening"),
    (0x210000, "Dialogue Region 2 - Early Game"),
    (0x220000, "Dialogue Region 3 - Mid Game A"),
    (0x230000, "Dialogue Region 4 - Mid Game B"),
    (0x240000, "Dialogue Region 5 - Late Game"),
    (0x250000, "Dialogue Region 6 - Endgame"),
    (0x260000, "Dialogue Region 7 - Side Quests A"),
    (0x270000, "Dialogue Region 8 - Side Quests B"),
    (0x280000, "Dialogue Region 9 - NPC Dialogue A"),
    (0x290000, "Dialogue Region 10 - NPC Dialogue B"),
    (0x2A0000, "Dialogue Region 11 - System Messages"),
    (0x2B0000, "Dialogue Region 12 - Battle Text"),
    (0x2C0000, "Dialogue Region 13 - Item Descriptions"),
    (0x2D0000, "Dialogue Region 14 - Enemy Names"),
    (0x2E0000, "Dialogue Region 15 - Technique Names"),
    (0x2F0000, "Dialogue Region 16 - Unused/Development"),
    (0x300000, "Dialogue Region 17 - Credits/Ending"),
]

# Custom character encoding: bytes 0x01-0x1F map to lowercase letters
CHAR_MAP = {
    0x01: 'a', 0x02: 'b', 0x03: 'c', 0x04: 'd', 0x05: 'f',
    0x06: 'g', 0x07: 'j', 0x08: 'l', 0x09: 'm', 0x0A: 'n',
    0x0B: 'p', 0x0C: 'q', 0x0D: 'r', 0x0E: 's', 0x0F: 'y',
    0x10: 'A', 0x11: 'B', 0x12: 'C', 0x13: 'D', 0x14: 'E',
    0x15: 'F', 0x16: 'G', 0x17: 'h', 0x18: 'k', 0x19: 'u',
    0x1A: 'v', 0x1B: 'a', 0x1C: 'i', 0x1D: 'o', 0x1E: 't',
    0x1F: 'e',
}

CONTROL_CODES = {
    0x00: '<SEP>',
    0xFC: '<BR>',
    0xFD: '<CLEAR>',
    0xFE: '<WAIT>',
    0xFF: '<END>',
}

DYNAMIC_CODES = {
    0x21: '<HERO>',      # ! - Hero name
    0x22: '<PARTY>',      # " - Party member name
    0x23: '<ITEM>',       # # - Item name
    0x26: '<MONSTER>',    # & - Monster name
    0x27: '<TECH>',       # ' - Technique name
}


def decode_byte(b):
    """Decode a single byte using the custom encoding."""
    if b in CONTROL_CODES:
        return CONTROL_CODES[b]
    if b in DYNAMIC_CODES:
        return DYNAMIC_CODES[b]
    if b in CHAR_MAP:
        return CHAR_MAP[b]
    if 0x20 <= b <= 0x7E:
        return chr(b)
    if b == 0x0D:
        return '<CR>'
    if b == 0x35:
        return '<PAGE>'  # Part of 555 page break
    return f'<0x{b:02X}>'


def extract_raw(rom_data, offset, size):
    """Extract raw binary data from ROM."""
    return rom_data[offset:offset + size]


def extract_dialogue_region(rom_data, start_offset, region_size=0x10000):
    """Extract and decode a dialogue region."""
    region_data = rom_data[start_offset:start_offset + region_size]
    
    lines = []
    current_line = []
    i = 0
    
    while i < len(region_data):
        b = region_data[i]
        
        if b == 0xFF:
            if current_line:
                lines.append(''.join(current_line))
                current_line = []
            lines.append('<END>')
            i += 1
        elif b == 0xFC:
            if current_line:
                lines.append(''.join(current_line))
                current_line = []
            lines.append('<BR>')
            i += 1
        elif b == 0xFD:
            if current_line:
                lines.append(''.join(current_line))
                current_line = []
            lines.append('<CLEAR>')
            i += 1
        elif b == 0x00:
            if current_line:
                lines.append(''.join(current_line))
                current_line = []
            i += 1
        elif b == 0x35 and i + 2 < len(region_data) and region_data[i+1] == 0x35 and region_data[i+2] == 0x35:
            if current_line:
                lines.append(''.join(current_line))
                current_line = []
            lines.append('<PAGE_BREAK>')
            i += 3
        else:
            decoded = decode_byte(b)
            current_line.append(decoded)
            i += 1
    
    if current_line:
        lines.append(''.join(current_line))
    
    return '\n'.join(lines)


def extract_palettes(rom_data, output_dir):
    """Extract all palette data from ROM."""
    # Scan for palette patterns (32-byte blocks with valid 0BGR values)
    palettes = []
    for offset in range(0, len(rom_data) - 32, 32):
        block = rom_data[offset:offset + 32]
        is_valid = True
        for j in range(0, 32, 2):
            color = struct.unpack('>H', block[j:j+2])[0]
            # Valid Genesis colors: each nibble <= 0xE
            for nibble in [(color >> 8) & 0xF, (color >> 4) & 0xF, color & 0xF]:
                if nibble > 0xE:
                    is_valid = False
                    break
        if is_valid:
            palettes.append((offset, block))
    
    # Save raw palette data
    palette_file = output_dir / 'palettes_raw.bin'
    with open(palette_file, 'wb') as f:
        for offset, block in palettes:
            f.write(block)
    
    # Save palette descriptions
    palette_txt = output_dir / 'palettes.txt'
    with open(palette_txt, 'w') as f:
        for offset, block in palettes:
            colors = []
            for j in range(0, 32, 2):
                color = struct.unpack('>H', block[j:j+2])[0]
                r = ((color >> 1) & 0x07) * 36
                g = ((color >> 5) & 0x07) * 36
                b = ((color >> 9) & 0x07) * 36
                colors.append(f"#{r:02X}{g:02X}{b:02X}")
            f.write(f"0x{offset:06X}: {' '.join(colors)}\n")
    
    print(f"Extracted {len(palettes)} palettes to {palette_file}")
    return len(palettes)


def decode_4bpp_tile(tile_data):
    """Decode 32 bytes of Genesis 4bpp tile data into 8x8 pixel values."""
    pixels = []
    for row in range(8):
        row_pixels = []
        for col in range(4):
            byte = tile_data[row * 4 + col]
            row_pixels.append((byte >> 4) & 0x0F)
            row_pixels.append(byte & 0x0F)
        pixels.append(row_pixels)
    return pixels


def create_font_preview(font_data, output_path):
    """Create a visual font preview from raw 4bpp font data."""
    tiles = []
    for i in range(0, len(font_data), 32):
        if i + 32 <= len(font_data):
            tiles.append(decode_4bpp_tile(font_data[i:i+32]))
    
    tiles_per_row = 16
    num_rows = (len(tiles) + tiles_per_row - 1) // tiles_per_row
    
    img = Image.new('RGB', (tiles_per_row * 8, num_rows * 8), (0, 0, 0))
    
    for idx, tile in enumerate(tiles):
        x = (idx % tiles_per_row) * 8
        y = (idx // tiles_per_row) * 8
        for row in range(8):
            for col in range(8):
                val = tile[row][col]
                gray = val * 17
                img.putpixel((x + col, y + row), (gray, gray, gray))
    
    img.save(output_path)
    print(f"Created font preview: {output_path}")


def main():
    if len(sys.argv) < 2:
        print("Usage: python regenerate_all.py <rom_file> [output_dir]")
        print("")
        print("Regenerates all extracted assets from the PSIV ROM.")
        print("Output defaults to './regenerated/'")
        sys.exit(1)
    
    rom_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('regenerated')
    
    print(f"Reading ROM: {rom_path}")
    with open(rom_path, 'rb') as f:
        rom_data = f.read()
    
    print(f"ROM size: {len(rom_data):,} bytes")
    print("")
    
    # Create output directories
    raw_dir = output_dir / 'graphics_raw'
    dialogue_dir = output_dir / 'dialogue_by_scene'
    raw_dir.mkdir(parents=True, exist_ok=True)
    dialogue_dir.mkdir(parents=True, exist_ok=True)
    
    # Extract raw binary assets
    print("=" * 60)
    print("EXTRACTING RAW BINARY ASSETS")
    print("=" * 60)
    for name, info in ASSETS.items():
        data = extract_raw(rom_data, info['offset'], info['size'])
        out_path = raw_dir / name
        with open(out_path, 'wb') as f:
            f.write(data)
        print(f"  {name}: {len(data)} bytes @ 0x{info['offset']:06X}")
    
    # Extract and create font preview
    print("")
    print("=" * 60)
    print("CREATING FONT PREVIEW")
    print("=" * 60)
    font_data = extract_raw(rom_data, 0x117603, 0x2004)
    create_font_preview(font_data, output_dir / 'font_preview_4bpp.png')
    
    # Extract palettes
    print("")
    print("=" * 60)
    print("EXTRACTING PALETTES")
    print("=" * 60)
    num_palettes = extract_palettes(rom_data, output_dir)
    
    # Extract dialogue
    print("")
    print("=" * 60)
    print("EXTRACTING DIALOGUE")
    print("=" * 60)
    all_dialogue = []
    for i, (offset, desc) in enumerate(DIALOGUE_REGIONS):
        dialogue = extract_dialogue_region(rom_data, offset)
        scene_file = dialogue_dir / f'scene_{i:03d}.txt'
        with open(scene_file, 'w', encoding='utf-8') as f:
            f.write(f"# {desc}\n")
            f.write(f"# ROM Offset: 0x{offset:06X}\n")
            f.write("=" * 60 + "\n")
            f.write(dialogue)
        all_dialogue.append(dialogue)
        print(f"  scene_{i:03d}.txt: {len(dialogue):,} chars ({desc})")
    
    # Save full dialogue file
    full_dialogue = '\n\n'.join(all_dialogue)
    with open(output_dir / 'dialogue_full.txt', 'w', encoding='utf-8') as f:
        f.write(full_dialogue)
    print(f"\n  dialogue_full.txt: {len(full_dialogue):,} chars total")
    
    print("")
    print("=" * 60)
    print("REGENERATION COMPLETE")
    print("=" * 60)
    print(f"All files saved to: {output_dir.absolute()}")
    print("")
    print("Next steps:")
    print("  1. Review extracted assets in the output directory")
    print("  2. Run scripts/extract_tiles.py for additional tile graphics")
    print("  3. Edit dialogue_by_scene/*.txt files for translation")
    print("  4. Use scripts/insert_text.py to patch the ROM")


if __name__ == '__main__':
    main()

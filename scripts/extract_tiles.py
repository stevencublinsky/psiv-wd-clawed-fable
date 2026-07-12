#!/usr/bin/env python3
"""
PSIV Tile Extractor
Extracts 4bpp and 1bpp tiles from Phantasy Star IV ROM.
"""

import sys
from pathlib import Path
from PIL import Image

def decode_4bpp_tile(tile_data):
    """Decode 32 bytes of Genesis 4bpp tile data into 8x8 pixel values (0-15)"""
    pixels = []
    for row in range(8):
        row_pixels = []
        for col in range(4):
            byte = tile_data[row * 4 + col]
            high_nibble = (byte >> 4) & 0x0F
            low_nibble = byte & 0x0F
            row_pixels.append(high_nibble)
            row_pixels.append(low_nibble)
        pixels.append(row_pixels)
    return pixels

def decode_1bpp_tile(tile_data):
    """Decode 8 bytes of 1bpp tile data into 8x8 pixel values (0-1)"""
    pixels = []
    for row in range(8):
        byte = tile_data[row]
        row_pixels = [(byte >> (7 - col)) & 1 for col in range(8)]
        pixels.append(row_pixels)
    return pixels

def create_tile_sheet(tiles, tiles_per_row=16):
    """Create a tile sheet image from decoded tiles"""
    num_tiles = len(tiles)
    tiles_per_col = (num_tiles + tiles_per_row - 1) // tiles_per_row
    
    img_width = tiles_per_row * 8
    img_height = tiles_per_col * 8
    img = Image.new('RGB', (img_width, img_height), (0, 0, 0))
    
    # Grayscale palette for 4bpp
    palette = [(i * 17, i * 17, i * 17) for i in range(16)]
    
    for tile_idx, tile_pixels in enumerate(tiles):
        tile_x = (tile_idx % tiles_per_row) * 8
        tile_y = (tile_idx // tiles_per_row) * 8
        
        max_val = max(max(row) for row in tile_pixels) if any(any(r) for r in tile_pixels) else 1
        
        for row in range(8):
            for col in range(8):
                pixel_value = tile_pixels[row][col]
                if max_val <= 1:
                    color = (255, 255, 255) if pixel_value else (0, 0, 0)
                else:
                    color = palette[pixel_value]
                img.putpixel((tile_x + col, tile_y + row), color)
    
    return img

def extract_tiles(rom_data, offset, size, bpp=4):
    """Extract tiles from ROM at given offset"""
    if bpp == 4:
        tile_size = 32
        decode_func = decode_4bpp_tile
    elif bpp == 1:
        tile_size = 8
        decode_func = decode_1bpp_tile
    else:
        raise ValueError("BPP must be 1 or 4")
    
    region_data = rom_data[offset:offset+size]
    num_tiles = len(region_data) // tile_size
    
    tiles = []
    for i in range(num_tiles):
        tile_data = region_data[i*tile_size:(i+1)*tile_size]
        if len(tile_data) == tile_size:
            tiles.append(decode_func(tile_data))
    
    return tiles

def main():
    if len(sys.argv) < 5:
        print(f"Usage: {sys.argv[0]} <rom_file> <offset> <size> <bpp> [output.png]")
        sys.exit(1)
    
    rom_path = Path(sys.argv[1])
    offset = int(sys.argv[2], 0)  # Auto-detect hex/dec
    size = int(sys.argv[3], 0)
    bpp = int(sys.argv[4])
    output_path = Path(sys.argv[5]) if len(sys.argv) > 5 else Path('tiles.png')
    
    with open(rom_path, 'rb') as f:
        rom_data = f.read()
    
    tiles = extract_tiles(rom_data, offset, size, bpp)
    img = create_tile_sheet(tiles)
    img.save(output_path)
    
    print(f"Extracted {len(tiles)} tiles to {output_path}")

if __name__ == '__main__':
    main()

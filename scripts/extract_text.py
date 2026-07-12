#!/usr/bin/env python3
"""
PSIV Text Extractor
Extracts dialogue text from Phantasy Star IV ROM using custom character table.
"""

import sys
import re
from pathlib import Path

# Character mapping (best-guess based on frequency analysis)
CHAR_MAP = {
    0x01: 'n', 0x02: 'c', 0x03: 'm', 0x04: 'l', 0x05: 'j',
    0x06: 'p', 0x07: 'b', 0x08: 'd', 0x09: 's', 0x0A: 'q',
    0x0B: 'z', 0x0C: 'v', 0x0D: 'w', 0x0E: 'x', 0x0F: 'y',
    0x10: 'g', 0x11: 'k', 0x12: 'f', 0x13: 'u', 0x14: 'r',
    0x15: '?', 0x16: '?', 0x17: 'h', 0x18: '?', 0x19: '?',
    0x1A: '?', 0x1B: 'a', 0x1C: 'i', 0x1D: 'o', 0x1E: 't', 0x1F: 'e',
}

CONTROL_CODES = {
    0x00: ' ',      # Word separator
    0x20: ' ',      # Space
    0xFC: '\n',    # Line break
    0xFF: '<END>',  # String terminator
    0xFD: '<CLEAR>',# Clear window
    0xFB: '<SPACE>',# Add space
    0xFE: '<FE>',   # Unknown control
}

PORTRAIT_CODES = [
    b'\x30\x29\x2F',  # 0)/
    b'\x31\x29\x2F',  # 1)/
    b'\x33\x29\x2F',  # 3)/
    b'\x35\x29\x2F',  # 5)/
]

def decode_byte(b):
    """Decode a single byte using the character map"""
    if b in CONTROL_CODES:
        return CONTROL_CODES[b]
    if b in CHAR_MAP:
        char = CHAR_MAP[b]
        return char if char != '?' else f'[{b:02X}]'
    if 0x21 <= b <= 0x5A or 0x30 <= b <= 0x39:
        return chr(b)
    if 0x61 <= b <= 0x7A:
        return chr(b)
    return f'[{b:02X}]'

def extract_dialogue(rom_data, start_offset=0x200000):
    """Extract dialogue regions from ROM"""
    dialogue_regions = []
    i = start_offset
    
    while i < len(rom_data) - 50:
        window = rom_data[i:i+200]
        printable = sum(1 for b in window if 32 <= b <= 126)
        ratio = printable / len(window)
        
        if ratio > 0.6:
            end = i
            while end < len(rom_data) and end < i + 10000:
                block = rom_data[end:end+100]
                p = sum(1 for b in block if 32 <= b <= 126)
                if p / len(block) < 0.3:
                    break
                end += 100
            
            while end < len(rom_data) and rom_data[end] != 0xFF and end < i + 10000:
                end += 1
            if end < len(rom_data) and rom_data[end] == 0xFF:
                end += 1
            
            region_len = end - i
            if region_len >= 50:
                dialogue_regions.append((i, end))
                i = end
                continue
        
        i += 100
    
    return dialogue_regions

def decode_region(rom_data, start, end):
    """Decode a dialogue region to text"""
    result = ''
    i = start
    while i < end:
        b = rom_data[i]
        
        # Check for portrait codes
        found_portrait = False
        for j, pc in enumerate(PORTRAIT_CODES):
            if rom_data[i:i+3] == pc:
                result += f'[PORTRAIT:{j}]'
                i += 3
                found_portrait = True
                break
        if found_portrait:
            continue
        
        # 555 pattern
        if b == 0x35 and i+2 < end and rom_data[i+1] == 0x35 and rom_data[i+2] == 0x35:
            result += '[555]'
            i += 3
            continue
        
        result += decode_byte(b)
        i += 1
    
    return result

def main():
    if len(sys.argv) < 2:
        print(f"Usage: {sys.argv[0]} <rom_file> [output_dir]")
        sys.exit(1)
    
    rom_path = Path(sys.argv[1])
    output_dir = Path(sys.argv[2]) if len(sys.argv) > 2 else Path('extracted')
    output_dir.mkdir(exist_ok=True)
    
    with open(rom_path, 'rb') as f:
        rom_data = f.read()
    
    print(f"ROM size: {len(rom_data)} bytes")
    
    regions = extract_dialogue(rom_data)
    print(f"Found {len(regions)} dialogue regions")
    
    # Save full dialogue
    with open(output_dir / 'dialogue_full.txt', 'w', encoding='utf-8') as f:
        for idx, (start, end) in enumerate(regions):
            decoded = decode_region(rom_data, start, end)
            f.write(f"=== Region {idx} (0x{start:06X}) ===\n")
            f.write(decoded)
            f.write("\n\n")
    
    print(f"Saved: {output_dir / 'dialogue_full.txt'}")

if __name__ == '__main__':
    main()

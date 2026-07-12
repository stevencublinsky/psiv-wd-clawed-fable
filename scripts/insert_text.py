#!/usr/bin/env python3
"""
PSIV Text Inserter
Inserts modified text back into Phantasy Star IV ROM.
WARNING: This will modify the ROM file. Make a backup first!
"""

import sys
from pathlib import Path

# Reverse character map (char -> byte)
REVERSE_CHAR_MAP = {
    'n': 0x01, 'c': 0x02, 'm': 0x03, 'l': 0x04, 'j': 0x05,
    'p': 0x06, 'b': 0x07, 'd': 0x08, 's': 0x09, 'q': 0x0A,
    'z': 0x0B, 'v': 0x0C, 'w': 0x0D, 'x': 0x0E, 'y': 0x0F,
    'g': 0x10, 'k': 0x11, 'f': 0x12, 'u': 0x13, 'r': 0x14,
    'h': 0x17, 'a': 0x1B, 'i': 0x1C, 'o': 0x1D, 't': 0x1E, 'e': 0x1F,
}

def encode_text(text):
    """Encode text string to ROM bytes"""
    result = bytearray()
    i = 0
    while i < len(text):
        char = text[i]
        
        # Handle control codes
        if char == '\n':
            result.append(0xFC)
        elif char == ' ':
            result.append(0x20)  # Use space, not separator
        elif char in REVERSE_CHAR_MAP:
            result.append(REVERSE_CHAR_MAP[char])
        elif char.isupper() and 'A' <= char <= 'Z':
            result.append(ord(char))
        elif char.isdigit():
            result.append(ord(char))
        elif char in '!"#$%&\\'()*+,-./:;<=>?':
            result.append(ord(char))
        elif char == '[':
            # Skip bracketed control codes
            end = text.find(']', i)
            if end != -1:
                i = end + 1
                continue
        else:
            # Unknown character - use literal if ASCII
            if ord(char) < 128:
                result.append(ord(char))
        
        i += 1
    
    return bytes(result)

def main():
    if len(sys.argv) < 4:
        print(f"Usage: {sys.argv[0]} <text_file> <rom_file> <offset>")
        sys.exit(1)
    
    text_path = Path(sys.argv[1])
    rom_path = Path(sys.argv[2])
    offset = int(sys.argv[3], 0)
    
    with open(text_path, 'r', encoding='utf-8') as f:
        text = f.read()
    
    encoded = encode_text(text)
    
    # Read ROM, modify, and write back
    with open(rom_path, 'r+b') as f:
        f.seek(offset)
        old_data = f.read(len(encoded))
        f.seek(offset)
        f.write(encoded)
    
    print(f"Inserted {len(encoded)} bytes at 0x{offset:06X}")
    print(f"Previous data: {old_data.hex()}")
    print(f"New data: {encoded.hex()}")

def recalculate_checksum(rom_path):
    """Recalculate the ROM checksum after modifications"""
    with open(rom_path, 'r+b') as f:
        f.seek(0x200)
        data = f.read()
        checksum = sum(data) & 0xFFFF
        f.seek(0x18E)
        f.write(checksum.to_bytes(2, 'big'))
    print(f"Checksum updated to 0x{checksum:04X}")

if __name__ == '__main__':
    main()

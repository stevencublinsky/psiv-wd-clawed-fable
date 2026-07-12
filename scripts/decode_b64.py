#!/usr/bin/env python3
"""
Decode base64-encoded binary files pushed to the repository.
The MCP GitHub tool cannot handle raw binary uploads, so binaries are stored
as .b64 text files. This script decodes them back to their original form.

Usage:
    python decode_b64.py <file.b64> [output_file]
    python decode_b64.py --all        # Decode all .b64 files in repo
"""

import base64
import sys
from pathlib import Path


def decode_b64_file(b64_path: Path, output_path: Path = None):
    """Decode a .b64 file back to binary."""
    with open(b64_path, 'r') as f:
        b64_content = f.read().strip()
    
    binary_data = base64.b64decode(b64_content)
    
    if output_path is None:
        # Remove .b64 extension
        output_path = b64_path.with_suffix('')
        # Handle double extensions like .bin.b64 -> .bin
        if output_path.suffix == '.bin' and b64_path.name.endswith('.bin.b64'):
            output_path = b64_path.parent / b64_path.name.replace('.bin.b64', '.bin')
        elif output_path.suffix == '.png' and b64_path.name.endswith('.png.b64'):
            output_path = b64_path.parent / b64_path.name.replace('.png.b64', '.png')
    
    with open(output_path, 'wb') as f:
        f.write(binary_data)
    
    print(f"Decoded: {b64_path} -> {output_path} ({len(binary_data)} bytes)")
    return output_path


def decode_all_b64_files(repo_root: Path = None):
    """Find and decode all .b64 files in the repository."""
    if repo_root is None:
        repo_root = Path(__file__).parent.parent
    
    b64_files = list(repo_root.rglob('*.b64'))
    print(f"Found {len(b64_files)} .b64 file(s) to decode:")
    
    for b64_file in sorted(b64_files):
        try:
            decode_b64_file(b64_file)
        except Exception as e:
            print(f"ERROR decoding {b64_file}: {e}")


def main():
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)
    
    if sys.argv[1] == '--all':
        decode_all_b64_files()
    else:
        b64_path = Path(sys.argv[1])
        output_path = Path(sys.argv[2]) if len(sys.argv) > 2 else None
        decode_b64_file(b64_path, output_path)


if __name__ == '__main__':
    main()

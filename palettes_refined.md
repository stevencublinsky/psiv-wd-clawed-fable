# Refined Palette Data

Total valid palettes: 28,833
Palette clusters: 1,564

## Palettes Near Graphics Regions

See `palettes_raw.bin` for raw data and `palettes.txt` for full RGB breakdown.

## Sample Palettes

Palette clusters found near graphics regions:
- Cluster at 0x0009E9 - 0x000A89 (6 palettes) - Boot code
- Cluster at 0x006227 - 0x0063CA (12 palettes) - Engine data
- Cluster at 0x006F05 - 0x00740F (39 palettes) - Graphics data

## Format

32 bytes per palette (16 colors x 2 bytes)
Color Format: 0BGR (9-bit, each channel 0-0xE)
RGB Conversion: R=(color&0xF)*17, G=((color>>4)&0xF)*17, B=((color>>8)&0xF)*17

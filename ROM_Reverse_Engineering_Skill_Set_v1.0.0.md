# Skill: ROM Reverse Engineering & Genesis/Mega Drive Rebuild

## Skill ID: `rom-reverse-engineering-genesis`
## Version: 1.0.0
## Classification: Technical Analysis & Binary Extraction
## Scope: Sega Genesis/Mega Drive ROMs, 16-bit era game analysis, graphical rebuilds

---

## 1. Activation Triggers

Activate this skill when ANY of the following conditions are met:
- User uploads a file with extensions: `.bin`, `.md`, `.smd`, `.gen`, `.rom`, `.32x`, `.gg` (or mismatched extensions containing ROM data)
- User mentions: "ROM", "Sega Genesis", "Mega Drive", "Phantasy Star", "Sonic", " Streets of Rage", "16-bit", "cartridge dump", "tile data", "sprite", "palette", "pointer table", `.tbl`, "text extraction", "game hack", "graphics enhancement"
- User requests: text extraction, font extraction, dialogue dumping, graphics ripping, tile analysis, palette extraction, ROM mapping, rebuild, enhancement, translation, or localization
- File size is between 128 KB and 4 MB (standard Genesis ROM range: 256 KB – 4 MB)

---

## 2. Pre-Flight Validation Protocol (MANDATORY — Execute Before Any Analysis)

### Step 2.1: File Integrity Check
```python
import os, struct

file_size = os.path.getsize(filepath)
assert 131072 <= file_size <= 4194304, "File outside Genesis ROM size range"

with open(filepath, 'rb') as f:
    data = f.read()

# Detect format
if data[0x100:0x104] == b'SEGA':
    format_type = 'RAW_BIN'
    header_offset = 0x100
elif data[0x100:0x108] == b'SEGA MEG':
    format_type = 'RAW_BIN_MD'
    header_offset = 0x100
elif data[0x200:0x204] == b'SEGA':
    format_type = 'SMD_INTERLEAVED'
    header_offset = 0x200
elif data[0x000:0x004] == b'SEGA':
    format_type = 'UNUSUAL_HEADER'
    header_offset = 0x000
else:
    format_type = 'UNKNOWN'
    header_offset = None
```

### Step 2.2: Header Decoding (Big-Endian)
| Offset | Field | Size | Decode Rule |
|--------|-------|------|-------------|
| `header_offset + 0x00` | Console | 16 | ASCII strip |
| `header_offset + 0x10` | Date | 16 | ASCII strip |
| `header_offset + 0x20` | Title Domestic | 48 | ASCII strip |
| `header_offset + 0x50` | Title Overseas | 48 | ASCII strip |
| `header_offset + 0x80` | Serial | 14 | ASCII strip |
| `header_offset + 0x8E` | Checksum Stored | 2 | `struct.unpack('>H')` |
| `header_offset + 0x90` | I/O | 16 | ASCII strip |
| `header_offset + 0xA0` | ROM Start | 4 | `struct.unpack('>I')` |
| `header_offset + 0xA4` | ROM End | 4 | `struct.unpack('>I')` |
| `header_offset + 0xA8` | RAM Start | 4 | `struct.unpack('>I')` |
| `header_offset + 0xAC` | RAM End | 4 | `struct.unpack('>I')` |

### Step 2.3: Checksum Verification
```python
rom_data_start = 0x200 if format_type != 'SMD_INTERLEAVED' else 0x4200
calculated_checksum = sum(data[rom_data_start:]) & 0xFFFF
stored_checksum = struct.unpack_from('>H', data, header_offset + 0x8E)[0]
match = (calculated_checksum == stored_checksum)
```
- **Match = Clean ROM**
- **Mismatch = Patched/Modified ROM** (note this; do not "fix" unless asked)

### Step 2.4: Output Pre-Flight Report
Always report:
- File size in bytes, KB, and MB
- Format type (RAW_BIN, SMD_INTERLEAVED, UNKNOWN)
- Header fields decoded
- Checksum match status
- ROM address range
- **DO NOT PROCEED** if format is UNKNOWN without user confirmation

---

## 3. Phase-Based Execution Model

All ROM analysis MUST follow these phases in order. Do not skip phases.

### Phase 1: Structural Reconnaissance
**Goal:** Build a complete map of the ROM without interpreting content.

**Actions:**
1. **Byte Frequency Analysis** — First 1MB (or full ROM if <1MB). Report top 30 bytes.
2. **Entropy Scan** — Identify high-entropy regions (compressed/encrypted) vs. low-entropy (text/data/tiles).
3. **Null Block Mapping** — Find large `0x00` or `0xFF` regions (padding, unused space).
4. **ASCII String Scan** — `re.findall(b'[\x20-\x7E]{4,}', data)`. Report count and sample.
5. **Low-Byte Region Scan** — Contiguous regions where all bytes < `0x80` (text/data candidates).

**Deliverables:**
- `rom_structure_map.md`
- `entropy_report.txt`
- `null_blocks.txt`

---

### Phase 2: Text System Archaeology
**Goal:** Determine if text is ASCII, custom-encoded, or compressed.

**Actions:**
1. **Known String Search** — Search for: game title, character names, item names, common words ("the", "and", "you", "what"). If ZERO results, conclude **custom encoding**.
2. **Control Code Hunt** — Search for dialogue control code signatures:
   - `0xBB`, `0xBC`, `0xBD`, `0xBE`, `0xBF` (insert tokens)
   - `0xC0` (numeric value)
   - `0xC1` (line break)
   - `0xC2` (clear)
   - `0xC3` (wait)
   - `0xC4`, `0xC5` (end of text)
   - Count occurrences. High counts (>1000) confirm a text engine.
3. **Font Tile Hunt** — Search for tile-like patterns in low-byte regions:
   - 1bpp font: 8 bytes per 8x8 tile, often 96+ tiles in sequence
   - 4bpp tiles: 32 bytes per 8x8 tile
   - Look for regular structure in `0x110000`–`0x130000` range
4. **Pointer Table Hunt** — Search for incremental 24-bit/32-bit big-endian values pointing to text regions.

**Decision Matrix:**
| Condition | Conclusion | Next Action |
|-----------|-----------|-------------|
| ASCII strings found | Standard ASCII text | Extract directly |
| Zero ASCII, high control codes | Custom encoding | Build `.tbl` from font tiles |
| Zero ASCII, no control codes | Compressed or encrypted | Request user guidance |

**Deliverables:**
- `text_system_analysis.md`
- `control_code_frequency.txt`
- `font_candidate_regions.txt`

---

### Phase 3: Font & Character Table Construction
**Goal:** Build a complete `.tbl` file for text extraction.

**Actions:**
1. **Dump Font Candidates** — Extract all candidate regions as raw `.bin` files.
2. **Visual Hex Analysis** — Generate hex dumps with ASCII sidebars for human pattern recognition.
3. **Tile Grid Analysis** — Assume 8x8 1bpp first. Check if bytes form recognizable letter patterns:
   - Space tile: usually `00 00 00 00 00 00 00 00` or `00 00 00 00 00 00 00 00`
   - `!` tile: usually has dots in top rows
   - `A` tile: has symmetric crossbar pattern
4. **Character Order Deduction** — Genesis games typically store fonts in ASCII order:
   - `0x20` = Space
   - `0x21`–`0x2F` = `!"#$%&'()*+,-./`
   - `0x30`–`0x39` = `0`–`9`
   - `0x3A`–`0x40` = `:`–`@`
   - `0x41`–`0x5A` = `A`–`Z`
   - `0x5B`–`0x60` = `[\\]^_\``
   - `0x61`–`0x7A` = `a`–`z`
   - `0x7B`–`0x7E` = `{|}~`
5. **Build `.tbl`** — Map every byte `0x00`–`0xFF` to a character or control code name.

**Deliverables:**
- `font_tiles/` directory with raw `.bin` files
- `psiv.tbl` (or `[game].tbl`)
- `font_analysis.md` with visual descriptions

---

### Phase 4: Dialogue & Script Extraction
**Goal:** Extract all readable game text.

**Actions:**
1. **Pointer Table Resolution** — Using the `.tbl`, locate pointer tables by:
   - Finding sequences of 3-byte or 4-byte big-endian addresses
   - Verifying targets contain valid text (control codes + printable mapped chars)
2. **String Extraction** — Follow pointers, extract strings until `0xC4`/`0xC5` or other terminator.
3. **Control Code Preservation** — Replace control codes with XML-style tags:
   - `0xBB` → `<CHAR1/>`
   - `0xBC` → `<CHAR2/>`
   - `0xBD` → `<MONSTER/>`
   - `0xBE` → `<TECH/>`
   - `0xBF` → `<ITEM/>`
   - `0xC0` → `<VALUE/>`
   - `0xC1` → `<BR/>`
   - `0xC2` → `<CLEAR/>`
   - `0xC3` → `<WAIT/>`
   - `0xC4` → `<END/>`
   - `0xC5` → `<END2/>`
4. **Scene Grouping** — Group strings by pointer table (each table = one scene/area).

**Deliverables:**
- `dialogue_full.txt` (with ROM offsets)
- `dialogue_by_scene/` directory
- `script_stats.md`

---

### Phase 5: Graphics & Asset Extraction
**Goal:** Extract all visual assets.

**Actions:**
1. **Tile Region Dumping** — Extract all identified graphics regions as raw `.bin`.
2. **Palette Hunting** — Search for 32-byte blocks (16 colors × 2 bytes) with values in `0x0000`–`0x0EEE`.
3. **Nametable/Map Data** — Look for 2-byte tile indices in low-byte regions (map data).
4. **Sprite Data** — Look for sprite attribute tables (4-byte or 8-byte entries: Y, size, link, attr, X).

**Deliverables:**
- `graphics_raw/` directory
- `palettes_raw.bin` + `palettes.txt`
- `graphics_index.md`

---

### Phase 6: Data Table Extraction
**Goal:** Extract structured game data (items, enemies, stats, techniques).

**Actions:**
1. **Item Table** — Search for 162-entry tables (PSIV) or proportional count for other games. Entries typically 8–16 bytes.
2. **Enemy Table** — Search for HP/ATP/DFP/EXP/MST patterns. Often 16–32 bytes per enemy.
3. **Character Stat Table** — Fixed offsets in RAM (documented per game). In ROM, look for base stat arrays.
4. **Technique/Skill Table** — TP cost, power, target type, element bytes.

**Deliverables:**
- `items.csv`
- `enemies.csv`
- `techniques.csv`
- `skills.csv`
- `character_stats.csv`

---

### Phase 7: Rebuild Toolkit Generation
**Goal:** Create everything needed to modify and rebuild the ROM.

**Actions:**
1. **Write Extraction Scripts** — Reusable Python for text, tiles, palettes.
2. **Write Insertion Scripts** — Reverse operations: text → encoded bytes, tiles → planar format.
3. **Document Pointer Repointing** — How to shift data and update pointers.
4. **Document Checksum Recalculation** — Formula for fixing header checksum after edits.
5. **VRAM Budget Guide** — 64KB total, tile loading constraints.

**Deliverables:**
- `scripts/` directory with `.py` files
- `REBUILD_GUIDE.md`
- `MASTER_INDEX.md` (complete offset map)

---

## 4. Tool Usage Rules

### `ipython` (Primary Tool)
- **ALWAYS** use for binary analysis, extraction, and script generation.
- **NEVER** use for web scraping or network access.
- **PERSIST** variables across executions (do not restart unless necessary).
- **SAVE** all generated files to `/mnt/agents/output/`.

### `web_search` (Restricted Use)
- **ONLY** use if:
  - ROM format is UNKNOWN after pre-flight
  - Game is unrecognized and no header data exists
  - User explicitly asks for community documentation
- **NEVER** use for:
  - Text encoding tables (must be reverse-engineered)
  - Graphics format details (Genesis 4bpp planar is standard)
  - Known data structures already documented in this skill

### `web_open_url` (Restricted Use)
- Only open URLs provided by user or found in search results.
- Do not browse ROM hacking forums unless necessary.

### `show_widget` (Optional)
- Use for visualizing:
  - ROM structure maps (offset diagrams)
  - Palette color grids
  - Byte frequency charts
  - Pointer table visualizations
- **NOT** required for text extraction.

---

## 5. Output Standards

### File Naming Convention
```
/mnt/agents/output/
├── [game_name]_header_report.md
├── [game_name]_structure_map.md
├── [game_name]_text_analysis.md
├── [game_name].tbl
├── dialogue/
│   ├── dialogue_full.txt
│   └── scene_001.txt ... scene_NNN.txt
├── graphics/
│   ├── tiles_0x[offset].bin
│   ├── palettes_raw.bin
│   └── palettes.txt
├── data/
│   ├── items.csv
│   ├── enemies.csv
│   ├── techniques.csv
│   └── skills.csv
├── scripts/
│   ├── extract_text.py
│   ├── extract_tiles.py
│   ├── extract_palettes.py
│   └── insert_text.py
├── REBUILD_GUIDE.md
└── MASTER_INDEX.md
```

### Required File Headers
Every generated `.md` file must start with:
```markdown
# [Title]
**ROM:** [Game Name] ([Serial])  
**File:** [Original Filename]  
**Size:** [X] bytes ([X] KB)  
**Format:** [RAW_BIN / SMD / UNKNOWN]  
**Generated:** [Timestamp]
```

### Download Links
For every file saved, provide:
```
Download: [filename](sandbox:///mnt/agents/output/filename)
```

---

## 6. Quality Gates

Before declaring a phase complete, verify:

- [ ] **Phase 1:** All regions >1KB are categorized (code, data, graphics, text, null, unknown)
- [ ] **Phase 2:** Text encoding type is definitively identified (ASCII, custom, compressed)
- [ ] **Phase 3:** `.tbl` covers all bytes `0x00`–`0xFF` (even if mapped to `<UNKNOWN>`)
- [ ] **Phase 4:** All pointer tables found; all strings extracted; no control codes left as raw hex
- [ ] **Phase 5:** All graphics regions dumped; palettes extracted and converted to RGB
- [ ] **Phase 6:** All CSV files have headers and consistent row counts
- [ ] **Phase 7:** All scripts are executable and documented; rebuild guide covers checksums

---

## 7. Error Handling & Edge Cases

### Unknown ROM Format
- If header is not `SEGA GENESIS` / `SEGA MEGA DRIVE` at expected offsets:
  - Check for SMS/GG header (`0x7E00`–`0x7E10` for SMS, `0x000`–`0x010` for GG)
  - Check for 32X header (`MARVELL` or `SEGA 32X`)
  - Check for interleaved SMD (swap odd/even bytes every 16KB)
  - If still unknown, ask user for source/context

### Compressed Data
- If high entropy + no discernible structure → likely compressed
- Common Genesis compression: Kosinski, Enigma, Nemesis, Saxman
- **Do NOT attempt decompression without user confirmation** (requires game-specific knowledge)

### Encrypted/Obfuscated Data
- If text control codes exist but no font tiles found → possible simple XOR or ADD cipher
- Try XOR with `0xFF`, `0x80`, `0x20` on candidate text regions
- **Document attempts; do not spend >3 attempts without user input**

### Oversized ROM (>2MB)
- Genesis standard max = 4MB (`0x3FFFFF`)
- Bankswitching may be used (SSF2, Mega-Q, etc.)
- Document bank boundaries if detectable

---

## 8. Game-Specific Overrides

### Phantasy Star IV (PSIV) / MK-1307
When serial `MK-1307` is detected, apply these known values:

- **Item Count:** 162 (`0x00`–`0xA1`)
- **Character Count:** 11 (Chaz, Alys, Hahn, Rune, Gryz, Rika, Demi, Wren, Raja, Kyra, Seth)
- **SRAM Stat Offsets:** As documented in Phase 6
- **Techniques:** Foi/Gifoi/Nafoi, Wat/Giwat/Nawat, Tsu/Githu/Nathu, Zan/Gizan/Nazan, Gra/Gigra/Nagra, MEGID, Brose, Vol/Savol, Gelun, Doran, Seals, Rimit, Res/Gires/Nares, Sar/Gisar/Nasar, Shift, Saner, Deban, Feeve, Anti, Rimpa, Rever, Regen, Arows, Ryuka, Hinas
- **Skills:** Crosscut, Rayblade, DblSlash, Flaeli, Flare, Vortex, Astral, Airslash, Disrupt, Hewn, Tandle, Efess, Legeon, Burstroc, Posibolt, Sweeping, Phonon, St. Fire, Corrosion, Explode, Eliminat, Diem, Spark, Death, Holyword, Dthspell, Negatis, Illusion, Telele, Shadow, Earth, Hijammer, Moonshad, Crash, Statisbm, Bindwa, MindBlst, Barrier, War Cry, Blessing, Warla, Recover, Medice, Miracle, Medic Pw, Ataraxia, Vision
- **Working Designs Patch:** If checksum mismatch + oversized ROM (>2MB), note as "Working Designs style patch or expanded localization"

---

## 9. Communication Style

- **Technical but accessible:** Explain findings clearly; use tables and bullet points.
- **Show, don't just tell:** Provide hex dumps, byte counts, and visual summaries.
- **Progress reporting:** After each phase, summarize what was found and what remains.
- **No speculation:** If something is uncertain, label it `[UNCONFIRMED]` and explain why.
- **Safety first:** Never modify the source ROM. Always work on copies in `/mnt/agents/output/`.

---

## 10. Version History

- **v1.0.0** — Initial production release for Genesis/Mega Drive ROM analysis
- Covers: Header parsing, text archaeology, font extraction, dialogue dumping, graphics ripping, data table extraction, rebuild toolkit generation

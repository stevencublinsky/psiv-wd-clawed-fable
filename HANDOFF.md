# HANDOFF: Phase 1 (Extraction) -> Phase 2 (Graphical Rebuild)

## Handoff Date: 2026-07-12
## From: ROM Analysis Agent
## To: Claude Fable Five (Audit & Rebuild Agent)

---

## What Was Completed

### Extraction Status: 85% Complete

| Component | Status | Notes |
|-----------|--------|-------|
| Character Encoding Table | 85% | 21/26 letters confirmed, 5 need validation |
| Dialogue Extraction | 90% | 25 regions, 79.8% decode rate |
| Font Tiles | 95% | Located and visualized, needs enhanced redesign |
| Graphics Regions | 70% | Raw dumps complete, need decompression/format analysis |
| Palette Data | 60% | Found 28K+ blocks, need assignment to graphics |
| Item/Enemy Tables | 20% | Placeholder CSVs, need ROM offset location |
| Pointer Tables | 10% | 212 references found, need structure analysis |
| Rebuild Scripts | 80% | 3 Python scripts, need testing |

### Key Files Delivered

- `psiv.tbl` - Character encoding table (load this first!)
- `dialogue_full.txt` - All extracted dialogue (~219 KB)
- `dialogue_by_scene/` - 35 scene files for editing
- `graphics_raw/` - 6 raw binary dumps
- `graphics_previews/` - Font visualizations
- `scripts/` - Python extraction/insertion toolkit
- `REBUILD_GUIDE.md` - Complete rebuild documentation
- `MASTER_INDEX.md` - ROM offset map

---

## Critical Context for Next Agent

### 1. Character Map Needs Validation

The 5 unconfirmed letters (0x15, 0x16, 0x18, 0x19, 0x1A) need validation:

**Method**: Compare decoded dialogue with actual game screenshots
1. Load ROM in emulator (BlastEm recommended)
2. Navigate to dialogue sections
3. Screenshot text boxes
4. Compare with extracted text
5. Adjust `psiv.tbl` mapping where text doesn't match

**Expected corrections**: Likely 1-2 letters need swapping (e.g., 0x19 might be 'k' not '?')

### 2. Dynamic Insertion System

When editing dialogue, **preserve these symbols exactly**:
- `!` = hero name (Chaz)
- `"` = party member (context-dependent)
- `#` = item name
- `&` = monster/NPC name
- `'` = technique name

These are NOT punctuation - they're **runtime function calls**. Removing them breaks name display.

### 3. 555 Page Break Code

The `555` sequence indicates a dialogue box transition. When editing:
- Keep `555` at the same relative positions
- If adding text, you may need to add `555` where a box fills up
- If removing text, you may be able to remove a `555`
- Typical box capacity: ~45 characters x 3 lines = ~135 chars per box

### 4. Working Designs Style Notes

This is a **Working Designs-style localization**:
- Lots of pop culture references
- Snarky humor and breaking the fourth wall
- Heavy use of punctuation for comedic timing
- Longer text than original Sega translation
- Character voices are distinct and exaggerated

**When editing**: Maintain the WD humor style. Don't make it generic RPG text.

---

## Immediate Next Steps

### Priority 1: Validate Character Map (1-2 hours)
- [ ] Load ROM in BlastEm emulator
- [ ] Navigate to early game dialogue
- [ ] Compare 5-10 dialogue boxes with extracted text
- [ ] Update `psiv.tbl` for any mismatches
- [ ] Re-run `extract_text.py` to regenerate clean dialogue

### Priority 2: Implement HD Font (2-3 hours)
- [ ] Extract font tiles with `extract_tiles.py`
- [ ] Design enhanced 8x8 font (or 8x16 with width table)
- [ ] Re-encode to Genesis 4bpp format
- [ ] Insert at 0x117603
- [ ] Test in emulator

### Priority 3: Enhanced Color Palettes (1-2 hours)
- [ ] Parse `palettes_raw.bin`
- [ ] Apply color curve enhancement (increase saturation, add midtones)
- [ ] Keep within Genesis 0x000-0xEEE color range
- [ ] Re-insert palette data
- [ ] Test visual result

### Priority 4: AI Tile Upscaling (4-8 hours)
- [ ] Extract all background tilesets
- [ ] Run through Real-ESRGAN or similar (pixel art model)
- [ ] Downscale and requantize to Genesis 4bpp
- [ ] Handle color reduction carefully (16 colors per tile)
- [ ] Re-insert and test

---

## Known Issues & Warnings

### ROM Size Constraints
- Genesis max addressable: 4MB (0x3FFFFF)
- Current ROM: 3.2MB (3,209,748 bytes)
- Available expansion: ~900KB
- **Cannot exceed 4MB without bankswitching hardware support**

### VRAM Constraints
- Total VRAM: 64KB
- Tile memory: ~32KB loadable at once
- Max tiles: ~1,024 (8x8 4bpp)
- **Enhanced graphics must fit within these limits**

### Text Expansion Limits
- Original dialogue: ~152KB
- Working Designs already expanded text significantly
- Further expansion may require:
  - Pointer table relocation
  - ROM expansion to 4MB
  - Text compression

### Checksum
- Stored checksum at 0x18E: 0x16F7
- Actual checksum: 0xA496
- **Any modification requires checksum recalculation**
- Use `scripts/insert_text.py` which auto-fixes checksum

---

## File Priority for Rebuild

| Priority | File | Action |
|----------|------|--------|
| P0 | `psiv.tbl` | Validate and correct character map |
| P0 | `scripts/extract_text.py` | Test and fix extraction |
| P1 | `graphics_raw/font_tiles_0x117603.bin` | Design enhanced font |
| P1 | `palettes_raw.bin` | Enhance color palettes |
| P2 | `dialogue_by_scene/*.txt` | Edit and improve dialogue |
| P2 | `scripts/insert_text.py` | Test text insertion |
| P3 | `graphics_raw/*.bin` | AI upscale background tiles |
| P4 | `REBUILD_GUIDE.md` | Update with rebuild notes |

---

## Questions for Next Agent

1. Can you confirm the 5 unmapped letters by comparing with emulator output?
2. What's your preferred AI upscaling pipeline for Genesis tiles?
3. Do you want to maintain exact Working Designs text, or enhance/expand it?
4. Should we implement 8x16 font or stick with 8x8 for VRAM efficiency?
5. Any interest in the widescreen hack (Option 4 in REBUILD_GUIDE)?

---

## Contact & Context

- Original ROM: `Phantasy Star Gen4 - Working Designs 6.01.md` (3,209,748 bytes)
- All output: `/mnt/agents/output/` (73 files, 23.38 MB)
- This handoff was generated by automated ROM analysis tooling
- Expected Phase 2 duration: 8-16 hours for full graphical rebuild

---

*Phase 1 Agent signing off. Good luck, Phase 2!*

# Production Rebuild Plan: Clawed Fable Graphical Enhancement

## Version: 1.0
## Date: 2026-07-12
## Scope: Full graphical rebuild of PSIV: Working Designs 6.01

---

## Executive Summary

Rebuild Phantasy Star IV: Working Designs 6.01 with enhanced graphics using the extracted data and tools from Phase 1. Target: Modern visual quality while maintaining Genesis authenticity.

---

## Phase 2A: Audit & Fix (Hours 1-4)

### 2A.1: Character Map Validation
- Load ROM in BlastEm emulator
- Capture 20+ dialogue screenshots
- Compare with `dialogue_full.txt` extraction
- Fix any incorrect letter mappings in `psiv.tbl`
- Re-extract dialogue with corrected table

### 2A.2: Script Audit
- Review `extract_text.py` for edge cases
- Test on clean PSIV ROM (verify no hardcoded offsets)
- Handle edge cases: multi-byte control sequences, unusual byte patterns
- Add error handling for malformed input

### 2A.3: Build System Setup
- Create `Makefile` or build script for rebuild pipeline
- Set up directory structure for build artifacts
- Version control all changes
- Document build dependencies

### Deliverables:
- Validated `psiv.tbl` (100% confirmed)
- Tested extraction scripts
- Working build pipeline

---

## Phase 2B: Font Enhancement (Hours 4-8)

### 2B.1: Font Analysis
- Extract all font variants (dialogue, menu, title)
- Document current font characteristics
- Measure text metrics (width, height, baseline)

### 2B.2: HD Font Design
- Design enhanced 8x8 font ( sharper, more readable )
- Alternative: Design 8x16 font with width table
- Ensure all 256 characters maintain Genesis constraints
- Preview font in context (mock dialogue boxes)

### 2B.3: Font Implementation
- Convert designed font to Genesis 1bpp format
- Pack into tile data (8 bytes per 8x8 character)
- Insert at 0x117603
- Update any width tables if needed
- Test in emulator

### Deliverables:
- Enhanced font binary
- Font insertion script
- Before/after comparison screenshots

---

## Phase 2C: Color Enhancement (Hours 8-12)

### 2C.1: Palette Analysis
- Parse all palette data from `palettes_raw.bin`
- Categorize palettes by use (BG, sprites, UI, portraits)
- Document current color distributions

### 2C.2: Color Enhancement Algorithm
- Design color curve (increase saturation, add midtones)
- Implement within Genesis 0x000-0xEEE constraints
- Preserve original color relationships
- Handle transparency (color 0) correctly

### 2C.3: Palette Application
- Apply enhancement to all palette blocks
- Re-insert into ROM at correct offsets
- Test visual appearance in emulator
- Iterate on color curve based on results

### Deliverables:
- Enhanced palette data
- Palette enhancement script
- Visual comparison screenshots

---

## Phase 2D: Tile Enhancement (Hours 12-20)

### 2D.1: Tile Categorization
- Categorize all tiles by type:
  - Background tiles (field, dungeon, town)
  - UI tiles (menus, windows, frames)
  - Effect tiles (spells, transitions)
- Determine which tiles benefit most from enhancement

### 2D.2: AI Upscaling Pipeline
- Set up Real-ESRGAN or equivalent (pixel art model)
- Batch process background tilesets
- Quality control: review each enhanced tileset
- Handle color reduction to Genesis 4bpp constraints

### 2D.3: Sprite Enhancement
- Extract character battle sprites
- Extract enemy sprites
- AI upscale with sprite-specific settings
- Downscale and requantize to 4bpp
- Maintain animation frame consistency

### 2D.4: Insertion & Testing
- Insert enhanced tiles at correct ROM offsets
- Verify VRAM constraints (64KB total)
- Test all affected scenes in emulator
- Fix any tile corruption or color issues

### Deliverables:
- Enhanced tilesets
- AI upscaling pipeline documentation
- Before/after comparison gallery

---

## Phase 2E: Final Integration (Hours 20-24)

### 2E.1: Integration Testing
- Full playthrough of opening sequence
- Verify all text displays correctly
- Check all graphics load without corruption
- Test save/load functionality

### 2E.2: Polish
- Fine-tune any problematic tiles
- Adjust color balance based on full game context
- Fix any remaining text extraction issues
- Ensure checksum is correct

### 2E.3: Distribution Prep
- Generate IPS/BPS patch from original ROM
- Create distribution README
- Package enhanced ROM with documentation
- Verify patch applies cleanly

### Deliverables:
- Enhanced ROM file
- IPS/BPS patch for distribution
- Complete documentation
- Playtesting report

---

## Risk Assessment

| Risk | Probability | Impact | Mitigation |
|------|-------------|--------|------------|
| VRAM overflow from enhanced tiles | Medium | High | Test incrementally, optimize tile count |
| Character map errors in dialogue | Medium | High | Validate with emulator screenshots |
| AI upscale quality inconsistent | Medium | Medium | Manual review pipeline, selective enhancement |
| ROM size exceeds 4MB | Low | High | Compress data, prioritize essential enhancements |
| Emulator compatibility issues | Low | Medium | Test in multiple emulators |

---

## Tools Required

| Tool | Purpose |
|------|---------|
| BlastEm / Genesis Plus GX | Emulator for testing |
| Real-ESRGAN / ESRGAN | AI tile upscaling |
| Python 3.10+ | Script execution |
| PIL/Pillow | Image processing |
| numpy | Data manipulation |
| Tile editing tool (YY-CHR, Tile Layer Pro) | Manual tile editing |
| Hex editor | ROM binary editing |

---

## Success Criteria

- [ ] All dialogue text displays correctly (100% decode accuracy)
- [ ] Enhanced font is clearly readable in dialogue boxes
- [ ] Color palettes show visible improvement
- [ ] Background tiles show enhanced detail
- [ ] Character sprites maintain animation consistency
- [ ] ROM functions identically to original (no crashes)
- [ ] Checksum is valid
- [ ] IPS patch applies cleanly to original ROM

---

## Timeline

| Phase | Duration | Cumulative |
|-------|----------|------------|
| 2A: Audit & Fix | 4 hours | 4 hours |
| 2B: Font Enhancement | 4 hours | 8 hours |
| 2C: Color Enhancement | 4 hours | 12 hours |
| 2D: Tile Enhancement | 8 hours | 20 hours |
| 2E: Integration | 4 hours | 24 hours |

**Total Estimated Duration: 24 hours**

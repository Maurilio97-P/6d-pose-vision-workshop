# Notebook Section Quality Audit — NB05 to NB25

**Standard:** Every section should follow: *problem → why it matters → what breaks if ignored → fix/API*
**Reference:** NB04 BGR vs RGB section is the gold standard.

---

## Summary

| Category | Count | Notes |
|---|---|---|
| API-first (no problem intro) | 5 | Lead with code signature before explaining why |
| Bare headings (no prose) | 6 | Section heading only, nothing before the code |
| Bare recap cells (no Next pointer) | 4 | Table but no "Next:" or context sentence |
| Actually good | ~85 | Most sections are fine |
| Exercises headers (all bare, low priority) | ~20 | Self-explanatory from code cell comments |

---

## Issues & Progress

### Priority 1 — API-first sections

| # | Notebook | Cell ID | Section | Status |
|---|---|---|---|---|
| 1 | NB05 | `resize-section` | 1. Resize and Interpolation | ✅ DONE |
| 2 | NB07 | `calibration` | 3. Running Camera Calibration | ✅ DONE |
| 3 | NB08 | `undistort-methods` | 2. Undistortion Methods | ✅ DONE |
| 4 | NB09 | `solvepnp-api` | 3. cv2.solvePnP — The API | ✅ DONE |
| 5 | NB14 | `api-header` | 2. estimatePoseSingleMarkers API | ✅ DONE |

### Priority 2 — Bare headings (no prose at all)

| # | Notebook | Cell ID | Section | Status |
|---|---|---|---|---|
| 6 | NB12 | `imports-header` | 1. Imports | ✅ DONE |
| 7 | NB13 | `draw-results-header` | 4. Drawing Detection Results | ✅ DONE |
| 8 | NB15 | `setup-pipeline-header` | 4. Full Pipeline Setup | ✅ DONE |
| 9 | NB15 | `viz-header` | 5. HUD Overlay — Robot's View | ✅ DONE |
| 10 | NB15 | `realtime-script-header` | 8. Real-Time Docking Script | ✅ DONE |
| 11 | NB17 | `steps34-header` | Steps 3 & 4: Individual Camera Calibration | ✅ DONE |

### Priority 3 — Recap cells missing "Next" pointer

| # | Notebook | Cell ID | Issue | Status |
|---|---|---|---|---|
| 12 | NB21 | `recap` | Table only, no "Next:" line | ✅ DONE |
| 13 | NB22 | `recap` | Table only, no "Next:" line | ✅ DONE |
| 14 | NB23 | `recap` | Table only, no "Next:" line | ✅ DONE |
| 15 | NB24 | `recap` | Table only, no "Next:" line | ✅ DONE |

### SKIP (fine as-is)

- All `## Exercises` headers (20+ notebooks) — code cells have full instructions
- NB05 sections 2–8 — already have problem→solution structure
- NB06 all sections — excellent context throughout
- NB07 `corner-detection` — has adequate explanation
- NB08, NB09, NB10 other sections — good
- NB11 all — good
- NB12 sections 2–9 — good
- NB13 sections 1,3,5,6,7,8 — good
- NB14 sections 1,3–8 — good
- NB15 sections 1,2,3,6,7 — good
- NB16 all — good
- NB17 most — good
- NB18–22 most — good
- NB23–25 most — good

---

## Notebooks with NO issues

- NB06 ✅ — camera model theory, excellent prose throughout
- NB10 ✅ — pose with chessboard, good pipeline overview
- NB11 ✅ — ArUco theory, good context
- NB16 ✅ — stereo theory, excellent context
- NB18 ✅ — DL intro, good explanations
- NB19 ✅ — MediaPipe Objectron, good
- NB20 ✅ — EfficientPose, good
- NB25 ✅ — capstone template, self-directing by design

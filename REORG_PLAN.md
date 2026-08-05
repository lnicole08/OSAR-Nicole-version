# OSAR repo reorganisation plan

Status: **planning only — nothing moved or edited yet.**

## Scope guardrails

Set by D3 and applying to everything below:

- **No new functions.** Not in the notebooks, not in the NL modules, not in new modules.
- **No rewriting existing functions.** Anything already written stays as written.
- **This phase is moving things around only** — relocating notebooks and cells between files
  and repos, merging/archiving whole notebooks, deleting genuinely dead code.
- Configuration such as exclusion lists lives **in the notebook that uses it**, as a plain
  editable list — not centralised into a module.
- Anything that would require writing or refactoring code is recorded as a *later* phase and
  is not part of this reorg. §6 in particular is diagnostic only for now.

## Decision log

Worked through one at a time. Answers recorded here as they are settled.

| # | Question | Answer |
|---|---|---|
| D1 | Do `1.`/`2.`/`3.` move into `01_pipeline/`? | **No — everything stays in the root folder for now.** No folder restructure; §2 is deferred. Reorg proceeds as content work: merges, splits, moves to other repos, dedup. |
| D2 | `Osar Phenomics` cells 13–19 — copy out and delete here, or duplicate? | **Move out.** All 5 figures there plot climbing on an axis; cell 14 is only their shared prep. `Osar Phenomics` keeps cells 0–12 and becomes purely OSAR. In the **new repo**, merge with `Falling-OSAR NT` section 4 — same analysis cut by neurotransmitter. |
| D3 | Merge `R76B09` exclusion across both stats outputs? | **Exclusion list in every notebook, defined in the notebook itself** as a plain editable list — not moved into `NLProcessing` or any function. Sets the scope guardrails above: no new functions, no rewriting existing ones, this phase is moving things around only. |
| D4 | Two copies of `NLCLIMB`/`NLMATH`/`NLGRAPHS` (here and DrosoClimb) have drifted | **Leave it.** Only real differences: `NLMATH.separation` and `NLMATH.maxvelocity`, where DrosoClimb's handle a Recovery phase and these don't. Falling-only code, nothing here calls it. DrosoClimb's copy is the live one; this repo's is a snapshot. Also: `fivesecondrule` was renamed `timerule` here (commit `652f479`) but not there — same body, `number = 20.0` in both. |
| D5 | `NLMATH.deltaversion` — called 6× in DrosoClimb, exists in neither copy | DrosoClimb's problem, not this repo's. Noted, no action here. |
| D8 | Where does climbing code ultimately live? | **`CLOSAR`** — `C:\Users\user\Documents\GitHub\CLOSAR` (CLimbing + OSAR), created 2026-08-05, currently empty. OSAR stays in OSAR; anything climbing-related, and anything comparing the two assays, goes to CLOSAR. `NLCLIMB`/`NLGRAPHS`/`NLMATH` go too — all three are climbing-only. Only `NLProcessing.py` stays here. |
| D9 | Terminology | **"Falling" → "Climbing"** in comments/variables/labels, notebook filenames, and the `_Falling` column suffix. **Not** in NL function names (`fallcalc`, `fallso`, `fallingocc`) — DrosoClimb calls those. |
| D9a | Dropbox renames | **DONE 2026-08-05.** `Data Compilation\`: `Falling_New`→`Climbing_New`, `Totalosarfalling`→`Totalosarclimbing`, `2025 Complete raw values osar falling`→`…osar climbing`, and `Falling_2026*.xlsx`→`Climbing_2026*.xlsx` (4 files). `DATA\` and `Raw data files\Falling`→`Climbing` also done. Code updated: 75 + 5 refs here, 2 in DrosoClimb. All notebooks parse. |
| D9b | Dropbox access rule | **Never use Git Bash `ls` on Dropbox** — Cygwin `ls` opens every entry to test for symlinks, which hydrates online-only placeholders (this is what downloaded `chambervideo.mp4` etc). **Use PowerShell `Get-ChildItem -Directory -Name`** — verified safe: after a recursive `-File` enumeration of `DATA\`, files still had `OFFLINE`+`UNPINNED`+`RECALL_ON_DATA_ACCESS` set (attr `5248544`). Renames via `Rename-Item` are metadata-only and safe. |
| D10 | Conflicting NL function bodies | **Follow the DrosoClimb version** — but confirm each function individually before changing it. Only 2 conflicts exist: `NLMATH.separation`, `NLMATH.maxvelocity`. |
| D6 | Vortex maps — where do they live? | **DONE.** The code is settled and unlikely to change, so a copy of `vortexmap.py` sits in each of the three repos (OSAR-Nicole-version, CLOSAR, DrosoClimb) — 202 lines, 14 functions, extracted verbatim from the byte-identical 7.5 KB cell. `Vortex Maps.ipynb` and `Climbing-OSAR vortexmaps.ipynb` now just do `from vortexmap import *`. `Light Intensity Summary`'s drifted copy left alone. |
| D7 | `Linregonly` vs `Linregonly - new` | **DONE — kept `Linregonly.ipynb`**, deleted `- new`. Ported one thing across: the `## Neurotransmitter separation` scatter (Δ LAI by NT, GtACR1 vs CsChrimson). Needed `import NLProcessing` and `mbonlist_csv`, which were added to the existing imports and paths cells. |
| D11 | How to apply the `_Falling`→`_Climbing` column rename | **DONE — rewrote existing xlsx headers in place.** 5 × `Totalcomparisonofallmetrics-*.xlsx`, 14 headers each (header row only, all other cells untouched; files were already local so nothing hydrated). Backups in the session scratchpad under `xlsx_backup\`. Code updated: 223 refs across 8 notebooks, including notebook 3's `col + '_Falling'` line so regeneration stays consistent. Verified: workbook reads back 78×26 with 14 `_Climbing` and 0 `_Falling`. |
| Q1–Q37 | NL stale-function review queue (§12) | **Actioned 2026-08-06 in CLOSAR.** Deleted: `NLGRAPHS.py` entirely (8/8 unused, 816 lines; identical copy still in DrosoClimb) and `NLMATH.violinfall` / `timetoreach` / `positional_arguments` (author-marked `#obsolete`). The other 26 moved into an `# OBSOLETE / UNUSED` section at the bottom of `NLMATH.py` (25) and `NLCLIMB.py` (1 — `timerule`, flagged as DrosoClimb's `fivesecondrule` twin). Nothing deleted outright beyond the safest set. |
| D12 | Splits and moves | **DONE 2026-08-06.** See §14. |

---

## 14. What was executed

**Splits.** `Falling-OSAR heatmaps only` → `OSAR heatmaps.ipynb` (19 cells: OSAR clustering,
all-PI heatmap, valence reversal) + `Climbing-OSAR heatmaps.ipynb` (25 cells).
`Falling-OSAR NT` → `OSAR neurotransmitters.ipynb` (16 cells: NT swarms, pref-vs-loco,
GtACR1-vs-CsChrimson, OSAR heatmaps) + `Climbing-OSAR NT.ipynb` (14 cells).
`Osar Phenomics` trimmed 21→13 cells; the combined block became `Climbing-OSAR phenomics.ipynb`.
Each half carries its own preamble and was checked to define every helper it calls.

Two cells were reassigned after inspection: heatmaps cell 18 is a `data_mode` switch reading
OSAR-only data, so it stayed; NT cell 22 is a climbing clustermap (height climbed, bout speed,
straightness) that my column-suffix heuristic missed, so it moved.

**Moved to CLOSAR** (renamed on the way): `Climbing-OSAR heatmaps / NT / phenomics /
Linreg / classification / comparison / clustering / vortexmaps`, `Metric_Clustering_Analysis`,
and `NLCLIMB.py` / `NLGRAPHS.py` / `NLMATH.py`.

**Cleanups.** Removed 6 dead `import NLCLIMB` / `import NLMATH` lines (3 notebooks) — they
would now fail and were never called. Renamed 106 remaining "falling"/"Falling" occurrences in
comments, labels and headings. Added `.gitignore` to both repos; untracked `__pycache__` and
`.tmp_rerun.txt`.

**State.** OSAR repo: 21 notebooks + `NLProcessing.py`. CLOSAR: 9 notebooks + 3 NL modules.
Both parse clean; no "falling" remains in either; no broken NL references.

Scope rule (D8): **OSAR stays in OSAR.** Anything falling/climbing-related, and anything
comparing the two assays, moves to a **new repo** you'll create. Where a notebook currently
does both, this repo keeps the OSAR half and the combined half is extracted.

**Open tension to resolve:** D4 kept `NLCLIMB`/`NLGRAPHS`/`NLMATH` here, but they are pure
falling code (they read `ExperimentState`, which no OSAR file has) and no OSAR notebook calls
them. Under D8 they belong in the new repo. Only `NLProcessing.py` is genuinely OSAR-side.

---

## 1. Inventory and classification

27 notebooks, 4 `.py` modules, all in a flat root. Nothing writes into the repo — every input
and output lives under Dropbox (`Data Compilation\...`), so this reorg is purely about code
layout.

Data sources, which is what actually decides where a notebook belongs:

| Source file | Content |
|---|---|
| `osar_compiled\2025collection\<MBON> x <resp>.csv` | per-genotype raw OSAR (from nb 2) |
| `*_totalcompilation.csv` | all-genotype OSAR compilation (from nb 2) |
| `OSAR_bothresponders_Full*.xlsx` | OSAR effect sizes, both responders (from nb 3) |
| `Falling_2026*.xlsx` | falling/climbing effect sizes (from nb 3) |
| `Totalcomparisonofallmetrics-Full.xlsx` | **combined** OSAR + falling workbook (from nb 3) |
| `Bootstrapped stats\*_bootstrap.csv` | per-genotype bootstrap draws (from *Bootstrap values*) |
| `thesis_stats\*_thesis_stats.csv` | per-genotype appendix table (from *Appendix csv generation*) |
| `MBONlist.csv` | MBON metadata: number, lobe, neurotransmitter |

| Notebook | Reads | Verdict |
|---|---|---|
| `1. Initial file processing` | raw tracking | **stay** (locked) |
| `2. Multi-OSAR file processing new` | raw → compiled | **stay** (locked) |
| `2. Multi-OSAR file processing` | raw → compiled | superseded by "new" → archive (locked, so: flag only) |
| `3. Complete file generation` | compiled → OSAR / Falling / Combined xlsx | **stay** (locked) — it is the *producer* of the combined workbook the other repo will consume |
| `Appendix csv generation` | 2025collection | **stay**, merge with Bootstrap values (§5) |
| `Bootstrap values` | 2025collection | **stay**, merge with Appendix (§5) |
| `Multi and single dabest OSAR plots` | totalcompilation, 2025collection | stay — OSAR only |
| `Single dabest plot` | 2025collection | **stay** (explicitly) — OSAR only |
| `Osar Phenomics` | combined xlsx | **stay** (explicitly) — but cells 13–19 are combined (§4) |
| `Directionality Analysis` | OSAR_bothresponders, MBONlist | stay — OSAR only |
| `Light Intensity Summary` | bootstrap csv, MBONlist | stay — OSAR only (contains its own vortex code, §5c) |
| `Four light intensities` | osar package | stay — OSAR only |
| `Reverse order` | osar package | stay — OSAR only |
| `Linregonly - new` | totalcompilation, MBONlist | stay — OSAR only; supersedes `Linregonly` |
| `Linregonly` | totalcompilation | archive — subset of "- new" (§5b) |
| `Asovalencevsme` | combined xlsx | stay — loads the combined workbook but only uses `_OSAR` columns (Aso published data vs ours) |
| `Fly Track Demo` | raw tracking | **stay** (explicitly) — demo/QC |
| `Control fly analysis` | 2025collection | stay — OSAR control QC |
| `Vortex Maps` | bootstrap csv, MBONlist | OSAR only, but earmarked to leave (§5c) |
| `Metric_Clustering_Analysis` | combined xlsx | **move** — resolved, see §10 |
| `Falling-OSAR heatmaps only` | combined + OSAR + falling | **split** (§4) — OSAR half stays as `OSAR heatmaps.ipynb` |
| `Falling-OSAR NT` | combined + OSAR + falling + MBONlist | **split** (§4) — OSAR half stays as `OSAR neurotransmitters.ipynb` |
| `Falling-OSAR Linreg` | combined + OSAR + falling | **move**, except the "Lin reg of OSAR" section |
| `Falling-OSAR comparison` | falling xlsx + totalcompilation | **move** |
| `Falling-OSAR classification` | falling raw + totalcompilation | **move** (its "Code - OSAR" section duplicates work already in the OSAR notebooks) |
| `Falling-OSAR Clusteringrelated` | combined xlsx | **move** |
| `Falling-osar vortexmaps` | bootstrap + thesis_stats + falling | **move** |

---

## 2. Target layout for this repo

> **Deferred by D1 — the flat root stays for now.** Everything below is kept as a sketch for
> later; nothing in the rest of this plan depends on it. With no folders, `lib/` is dropped
> and the NL modules stay at the root, which also means no notebook needs a `sys.path` edit
> (§11). The reorg proceeds as content work instead: merge §5a, split §4, move §3, dedup §6,
> NL cleanup §12.

```
OSAR-Nicole-version/
├── README.md                     NEW - what each folder does, pipeline order, where data lives
├── .gitignore                    NEW - __pycache__, .tmp_*, .ipynb_checkpoints
├── lib/
│   ├── NLCLIMB.py                moved as-is, no edits
│   ├── NLGRAPHS.py               moved as-is, no edits
│   ├── NLMATH.py                 moved as-is, no edits
│   ├── NLProcessing.py           moved as-is; grows over time (§6)
│   ├── paths.py                  NEW - the officecomp/labcomp/homecomp switch, once (§6)
│   └── mbon_labels.py            NEW - find_number / wrap_labels / parse_lobes / ... (§6)
├── 01_pipeline/                  raw -> compiled -> effect-size workbooks
│   ├── 1. Initial file processing.ipynb
│   ├── 2. Multi-OSAR file processing new.ipynb
│   └── 3. Complete file generation.ipynb
├── 02_stats_export/
│   └── 4. OSAR stats export.ipynb        Appendix csv + Bootstrap values, merged (§5a)
├── 03_figures/
│   ├── Multi and single dabest OSAR plots.ipynb
│   ├── Single dabest plot.ipynb
│   ├── OSAR heatmaps.ipynb               extracted (§4)
│   ├── OSAR neurotransmitters.ipynb      extracted (§4)
│   ├── Osar Phenomics.ipynb
│   ├── Linreg OSAR only.ipynb            = "Linregonly - new"
│   ├── Directionality Analysis.ipynb
│   ├── Light Intensity Summary.ipynb
│   ├── Four light intensities.ipynb
│   ├── Reverse order.ipynb
│   └── Vortex Maps.ipynb                 unless it leaves (§5c)
├── 04_qc/
│   ├── Fly Track Demo.ipynb
│   └── Control fly analysis.ipynb
├── 05_exploratory/
│   ├── Asovalencevsme.ipynb
│   └── Metric_Clustering_Analysis.ipynb  unless it leaves
└── _archive/
    ├── 2. Multi-OSAR file processing.ipynb
    └── Linregonly.ipynb
```

Two notes on this:

- `1.`/`2.`/`3.` keep their names and numbering; putting them in `01_pipeline/` is a move, not
  an edit. If even moving them is unwanted, leave all three at the root and drop the folder —
  everything else in the plan is unaffected.
- Notebooks import `NLCLIMB` etc. by bare name, so moving them into `lib/` needs a one-line
  `sys.path` addition per notebook (or a `.pth`/`conda develop`). That is the only code change
  the move forces. Alternative: leave the four `.py` files at the root and skip `lib/`.

---

## 3. What goes to the **new repo**

Whole notebooks:

- `Falling-OSAR comparison.ipynb`
- `Falling-OSAR classification.ipynb`
- `Falling-OSAR Clusteringrelated.ipynb`
- `Falling-OSAR Linreg.ipynb`
- `Falling-osar vortexmaps.ipynb`
- `Metric_Clustering_Analysis.ipynb` (§10)

Extracted halves (see §4):

- combined sections of `Falling-OSAR heatmaps only.ipynb`
- combined sections of `Falling-OSAR NT.ipynb`
- `Osar Phenomics.ipynb` cells 13–19 ("combined phenomics") — the notebook itself stays here,
  a *copy* of that section seeds the other repo

The interface between the two repos is a file, not code: `3. Complete file generation.ipynb`
stays here and writes `Totalcomparisonofallmetrics-Full.xlsx` + `Falling_<date>.xlsx` to
Dropbox; the **new repo** reads them. Nothing needs to be importable across repos.
`lib/` (the NL modules + helpers) will need to be duplicated or pip-installed in the second
repo — `Falling-OSAR classification` and `comparison` both import `NLCLIMB`/`NLMATH`.

---

## 4. Notebooks that need splitting

### `Falling-OSAR heatmaps only.ipynb` (36 cells)

| Cells | Section | Goes to |
|---|---|---|
| 1–7 | Basics / Function / Formulas to run | duplicated into **both** |
| 9–12 | Heatmap for specific MBONs comparing PI etc. | falling-osar (cell 11 is the falling metric list) |
| 14–15 | Vertical vs horizontal diff | falling-osar |
| 17–21 | **OSAR Clustering** | **stays** → `OSAR heatmaps.ipynb` |
| 23–25 | Falling | falling-osar |
| 27–30 | OSAR + Falling clustering | falling-osar |
| 32–33 | **Heatmap comparing all PIs of OSAR conditions** | **stays** |
| 35 | **Valence signs reversal** | **stays** (OSAR valence) |

So `OSAR heatmaps.ipynb` = preamble + cells 17–21, 32–33, 35. Verify cell 35 first; it reads
the combined workbook but appears to use OSAR columns only.

### `Falling-OSAR NT.ipynb` (24 cells)

| Cells | Section | Goes to |
|---|---|---|
| 0–3 | loaders | both |
| 6 | 1. NT separation — preference swarms | **stays** |
| 8 | 2. Pref vs Loco by NT (OSAR only) | **stays** |
| 10 | 2a. GtACR1 vs CsChrimson (OSAR) | **stays** |
| 12 | 2b. Climbing locomotor by NT (Falling only) | falling-osar |
| 14 | 3. Locomotion only by NT (OSAR) | **stays** |
| 16–17 | 4. Combined phenomics by NT | falling-osar |
| 19–22 | Heatmaps | 20 and 22 stay; 21 is falling → falling-osar |

### `Osar Phenomics.ipynb` (21 cells)

Stays whole (your call), but cells 14–15 under "combined phenomics" mix falling columns in.
Copy 13–19 into the **new repo**; decide separately whether to delete them here or keep
them as a duplicate.

---

## 5. Merge / dedup decisions

### 5a. `Appendix csv generation` + `Bootstrap values` → one notebook

**What they are.** Both are batch stats exporters, not figure notebooks. Both walk the same
input (`osar_compiled\2025collection\*.csv`), and for each *genotype × responder × light
intensity × metric* they run the same `dabest.load(...).hedges_g`. They differ only in what
they write out of that one result:

| | Appendix csv generation | Bootstrap values |
|---|---|---|
| Output | `thesis_stats\<MBON> x <resp>_thesis_stats.csv` + `<date>_all_osar_thesis_stats.csv` | `Bootstrapped stats\<MBON> x <resp>_bootstrap.csv` |
| Row grain | 1 row per intensity × group (Control/Test) | 1 row per bootstrap draw |
| Columns | genotype string, n, mean + 95% CI, Hedges' g + CI, metric | Hedges' g, CI, single bootstrap value |
| Extra work | `summary_ci_1group` per group (5000 resamples) for the mean CI | keeps the full `bootstraps` array |
| Metric list | same 9 metrics | same 9 metrics |
| Metric naming | `pi`, `speed_ratio`, … | `PI_Hg_OSAR`, `Speed ratio_Hg_OSAR`, … |
| Exclusions | drops `R76B09` | drops nothing |
| Paths | `specifiedpath` switch | hardcoded `D:\` |

**Verdict: merge into one file — but as two sections, not one fused loop.** Under the scope
guardrails, the merge is a *file* merge: the two notebooks become
`4. OSAR stats export.ipynb`, with `thesis_osar_hedgesg` and `extract_bootstrap_stats` kept
exactly as written and their loops left intact. One file, one place to look, both outputs.

Fusing them into a single dabest pass — the two notebooks run ~3 000 dabest fits each over the
same inputs, so a shared pass would roughly halve the runtime — **is a later phase**, since it
means rewriting the loops.

Also deferred to later, for the same reason:

- **Metric naming.** Two hand-maintained lists (`pi` / `speed_ratio` … vs `PI_Hg_OSAR` /
  `Speed ratio_Hg_OSAR` …) kept aligned by position. They currently match; nothing to do now,
  but it is a live trip hazard when either list is edited.
- **Rounding.** Appendix rounds to 2 dp at write time, bootstrap keeps full precision.
- **The two "total file" cells** at the end of Appendix are the same concat against two
  different drives — redundant, but leave both until paths are dealt with.

Do now, in-notebook: put the exclusion list at the top of the merged notebook as a plain
editable list (per D3) and have both sections read it, so the appendix and bootstrap outputs
stop disagreeing about `R76B09` / `VT999036`.

Downstream consumers to re-check after the merge:
`_bootstrap.csv` → `Vortex Maps`, `Light Intensity Summary`, `Falling-osar vortexmaps`.
`_thesis_stats.csv` → `Falling-osar vortexmaps` (and the written appendix).

### 5b. `Linregonly` vs `Linregonly - new`

`- new` is a strict superset: same five sections plus "Plotting PI against metrics" and
"Plotting PI GtACR1 vs PI CsChrimson", and it already imports `NLProcessing`. Keep `- new`,
rename it `Linreg OSAR only.ipynb`, archive the old one. (`Linregonly.ipynb` has the later
mtime, so confirm you didn't fix something in it after branching.)

Both also duplicate `chartplottingdabest` / `multiresponder_osar` / `omission` /
`get_best_position` from other notebooks in mutually incompatible versions — see §6.

### 5c. The vortex map code exists in three places

`Vortex Maps.ipynb` and `Falling-osar vortexmaps.ipynb` share a **byte-identical 7.5 KB
function cell** (`load_bootstrap_data`, `build_vortex_df`, `vortex_map`, `_spiralize`,
`_sample_bootstrap`, `create_labels`, …). `Light Intensity Summary.ipynb` carries a third,
lightly-drifted copy (`create_vortexmap`, `create_multi_vortexmap`).

Destination decided but **deferred to a later phase** — the shared cell becomes a function
inside `NLMATH.py` once the NL cleanup and renaming are done (§12 step 5). Nothing to write
now. What is still open in this phase is where the notebooks live:

- **A.** All vortex work leaves → new `vortexmaps` repo gets both notebooks, and `Light
  Intensity Summary` loses its vortex sections (it keeps bubble matrix, curve classification,
  pairwise correlation, bidirectionality).
- **B.** Split by data: `Vortex Maps` (OSAR only) stays here, `Falling-osar vortexmaps` goes
  to the **new repo** — consistent with the rule used everywhere else in this plan.
- **C.** Vortex rendering becomes `lib/vortexmap.py` here, and every repo imports it. Removes
  the triplication regardless of which notebooks live where.

C is compatible with A or B and is the one worth doing first: pull the shared cell into a
module, then moving notebooks becomes trivial.

---

## 6. Duplication survey — diagnostic only, no action this phase

> Under the scope guardrails, nothing here gets extracted, centralised or rewritten now. It is
> recorded because it explains why edits have to be repeated across notebooks, and because it
> is the argument for a later cleanup phase. Read it as a map, not a task list.

Function-level duplication measured across the 27 notebooks:

| Function | Copies | Distinct versions |
|---|---|---|
| `find_number` | 12 | 3 |
| `wrap_labels` | 8 | 4 |
| `multiresponder_osar` | 6 | 4 |
| `chartplottingdabest` | 6 | 4 |
| `MBONnamefile` | 5 | 3 |
| `matchingdfs` | 5 | 2 |
| `matchinglobesets` | 5 | 1 |
| `matchingcomp` | 5 | 3 |
| `omission` | 5 | **5 — every copy differs** |
| `shorten_mbon_numbers` | 5 | 2 |
| `parse_lobes` | 4 | 3 |
| `twolightdabest` | 4 | 3 |
| vortex helpers (`load_bootstrap_data`, `build_vortex_df`, `vortex_map`, `_spiralize`, …) | 2–3 each | 1–2 |
| `forestplot_multiplot` | 3 | 1 |

What this means in practice, with no action implied:

- **Paths.** The `officecomp` / `labcomp` / `computer2` / `homecomp` block is copy-pasted into
  ~15 notebooks, plus 12 hardcoded `D:\` paths in `Light Intensity Summary` alone and 8 in
  `Falling-OSAR NT`. Changing machine means editing every one of them. Largest single source
  of repeated manual edits in the repo.
- **Version drift is real, not cosmetic.** `omission` has 5 copies and 5 *different* bodies;
  `chartplottingdabest` 6 copies / 4 versions; `multiresponder_osar` 6 / 4; `wrap_labels`
  8 / 4. So "fix it in the notebook" already means "fix it in up to 6 places, which have
  quietly diverged". Worth knowing which copy a given figure actually used.
- **`omission` is not really a shared function.** The five bodies are per-analysis exclusion
  lists. Consistent with D3, they belong in their notebooks — this is the one duplication here
  that is arguably correct as-is.
- **Genotype exclusions** (`R76B09` / `VT999036` / `R58` / `Th-Gal4`) appear in 14 notebooks in
  6 different syntaxes. Per D3 they stay in-notebook; the only thing worth doing is making the
  lists agree with each other where they are meant to.
- The vortex duplication (§5c) is the one case where two copies are still byte-identical, so
  it has not drifted yet.

The NL modules are untouched by this section.

---

## 7. Repo hygiene (independent of everything above)

- No `.gitignore`; `__pycache__/*.pyc` (5 files) and `.tmp_rerun.txt` are committed. Add a
  `.gitignore` and `git rm --cached` them.
- ~22 MB of notebooks, nearly all of it embedded outputs (`Falling-OSAR Linreg` alone is
  1.9 MB, `Light Intensity Summary` 4.0 MB). Consider `nbstripout` on a filter, or at minimum
  clearing outputs before commit on the heaviest ones. This also makes diffs readable.
- `.gitattributes` sets `* text=auto`, which will rewrite line endings inside `.ipynb` JSON.
  Worth adding `*.ipynb -text` (or `binary`) so notebooks aren't normalised.
- `.claude/settings.local.json` is deleted in the working tree but still tracked — commit the
  deletion or restore it.

---

## 8. Suggested order of execution

Each step is independently useful; stop at any point. Flat root throughout (D1), no new
functions and no rewriting of existing ones (D3).

**This phase — moving things around**

1. Hygiene: `.gitignore`, untrack `__pycache__` and `.tmp_rerun.txt`, `.gitattributes` fix.
2. Archive the two superseded duplicates (`Linregonly` → D7, `2. Multi-OSAR file processing`).
3. Merge `Appendix csv generation` + `Bootstrap values` into `4. OSAR stats export.ipynb` as
   two unchanged sections in one file, with the exclusion list at the top (D3). Run once and
   diff the outputs against the existing Dropbox files before deleting anything.
4. Split `Falling-OSAR heatmaps only` and `Falling-OSAR NT`; the OSAR halves stay (§4).
   Split `Osar Phenomics` cells 13–19 out (D2).
5. Delete the dead code agreed in the §12 review queue.
6. Drop the seven no-op `import NLCLIMB` / `import NLMATH` lines.
7. Create the **new repo**; move the combined notebooks and extracted halves across,
   with a copy of the NL modules they need.
8. README describing the pipeline order and where data lives.

**Later phases — require writing code, explicitly out of scope for now**

9. Reconcile the `NLMATH` / `NLCLIMB` fork with DrosoClimb (§12 steps 1–2, D4/D5).
10. Fuse the two stats-export loops into a single dabest pass (§5a).
11. Vortex map into `NLMATH` (§12 step 5), and whatever renaming precedes it.
12. Anything from the duplication survey (§6) — paths, label helpers, dabest plot helpers.

---

## 9. Open decisions

1. Are the numbered notebooks allowed to *move* into `01_pipeline/`? (Import mechanics: §11.)
2. `Osar Phenomics` "combined phenomics" cells 13–19 — copy to the other repo and delete here,
   or keep duplicated?
3. After the merge in §5a, should `R76B09` be excluded from the bootstrap outputs as well?
4. Which NLMATH/NLCLIMB fork is canonical? (§12 step 1)
5. Work through the 37-item review queue (§12).

---

## 10. Resolved: `Metric_Clustering_Analysis` moves

Checked. Cell 7 builds its metric list as *everything except three metadata columns*:

```python
metadata_cols = ['MBON', 'genotypeandresponder', 'responder']
metric_cols = [col for col in df.columns if col not in metadata_cols]
```

applied to `Totalcomparisonofallmetrics-Full.xlsx`, so every falling metric is in the
correlation matrix and the dendrogram. It is a combined-assay analysis — it goes to the
**new repo**.

---

## 11. How folders affect `import NLMATH`

Every notebook uses the bare form — there is not a single `from NLMATH import ...` anywhere:

```python
import NLCLIMB
import NLMATH
import NLProcessing
```

Bare `import X` searches `sys.path`, and for a Jupyter kernel entry 0 of `sys.path` is the
directory the notebook lives in. That is the only reason it currently works: the notebook and
`NLMATH.py` are in the same folder.

So the rule is simple — **a notebook can only bare-import a module that sits beside it.**

| Move | Result |
|---|---|
| Notebook → `03_figures/`, NL stays at root | breaks: `ModuleNotFoundError: No module named 'NLMATH'` |
| Both notebook and NL move into the same folder | works, no change |
| NL → `lib/`, notebooks anywhere | breaks unless the notebook adds the path |

If you do want `lib/`, the fix is two lines at the top of each notebook that needs it:

```python
import sys, pathlib
sys.path.insert(0, str(pathlib.Path.cwd().parent / "lib"))
import NLMATH
```

`Fly Track Demo.ipynb` already does exactly this to reach the sibling `osar` package:
`sys.path.insert(0, r'C:\Users\user\Documents\GitHub\OSAR')`.

Given §12 below, the cheapest correct answer is: **leave the NL files at the repo root and
skip `lib/` for now.** They are the one thing nothing here actually imports, so there is no
benefit to hiding them, and no notebook needs a `sys.path` edit.

---

## 12. The NL modules are not used by this repo at all

This came out of the dead-code audit you asked for, and it is bigger than stale functions.

**Nothing in this repo calls them.** Seven notebooks write `import NLCLIMB` / `import NLMATH`,
but across all 27 notebooks there are **zero** `NLMATH.<something>` or `NLCLIMB.<something>`
call sites. `NLGRAPHS.py` is not even imported. The only live NL code here is
`NLProcessing.generate_lobelocation` (8 call sites) and `NLProcessing.find_number`.

| Module | Functions | Called from this repo |
|---|---|---|
| `NLCLIMB.py` | 16 | 0 |
| `NLGRAPHS.py` | 8 | 0 (never imported) |
| `NLMATH.py` | 42 | 0 |
| `NLProcessing.py` | 2 | 2 |

**The live copies are in `../DrosoClimb`, and the two copies have forked.** DrosoClimb calls
20 distinct NL functions across 8 notebooks; that is the climbing/falling analysis engine.
Comparing the two checkouts:

| Module | Same? | Divergence |
|---|---|---|
| `NLGRAPHS.py` | identical | — |
| `NLCLIMB.py` | 18 differing lines | this repo has `timerule`; DrosoClimb has `fivesecondrule` and *calls* it |
| `NLMATH.py` | 592 differing lines | this repo has 42 functions, DrosoClimb 30 |

They diverged in **both** directions. This repo's `NLMATH` has 16 functions DrosoClimb's
lacks (`deltaversion_deltag`, `deltaversion_meandiff`, `log2speedratio`, `singledelta`,
`boutanalysis`, `timespentabovemeanline`, …); DrosoClimb's has 4 this one lacks (the
`deltaversion_*_multistate` family). Neither is a superset. DrosoClimb also calls a
`NLMATH.deltaversion` that exists in *neither* file — so at least one of its notebooks is
already broken against the current module.

**Consequence for the audit: "never called in any notebook" has to be measured across both
repos.** Judged against this repo alone, all 68 functions look stale and the cleanup would
delete the entire climbing engine. The scan below therefore covers every repo under
`Documents\GitHub\`. Result: 20 NL functions are called anywhere, all from DrosoClimb, plus
`NLProcessing.generate_lobelocation` from here. Nothing outside those two repos touches NL.

### Cleanup sequence

1. **Reconcile the fork first**, before deleting anything — otherwise "stale here" and "stale
   there" disagree. Candidate split: DrosoClimb is canonical for `NLCLIMB` (it has
   `fivesecondrule` and calls it 29×; this repo's `timerule` looks like the orphaned
   ancestor); this repo is canonical for the `NLMATH` delta/effect-size additions
   (`deltaversion_deltag`, `deltaversion_meandiff`, `log2speedratio`, `singledelta`) and
   DrosoClimb for the `deltaversion_*_multistate` family. Neither `NLMATH` is a superset, so
   this is a merge, not a pick.
2. **Resolve `NLMATH.deltaversion`** — DrosoClimb calls it 6× and it exists in neither copy.
   Either it was renamed or those cells are already broken. Resolving it may retire a
   duplicate.
3. **Work the review queue below**, one function at a time.
4. **Drop the seven no-op `import NLCLIMB` / `import NLMATH` lines** from this repo's
   notebooks. Free, and it stops the next reader assuming a dependency exists.
5. **Later phase — vortex map into `NLMATH.py`.** Not part of this reorg: it means writing a
   function, which the guardrails defer until the cleanup and renaming are done. Recorded so
   the decision isn't relitigated: destination is `NLMATH`, which already holds the plotting
   functions (`calcgraph`, `meangraph`, `rastergraph`, `violinfall`); `NLCLIMB` is
   file-processing only and would be the wrong home. The material is the byte-identical 7.5 KB
   cell — `load_bootstrap_data`, `build_vortex_df`, `vortex_map`, `_spiralize`,
   `_sample_bootstrap`, `create_labels`, `get_effect`, `get_bootstrap` — shared by
   `Vortex Maps` and `Falling-osar vortexmaps`, with a drifted third copy in
   `Light Intensity Summary`. Two constraints when it happens: it must land on the reconciled
   `NLMATH` (step 1) rather than deepening the fork, and it makes `NLMATH` a dependency of the
   **new repo**.

### Review queue — functions with no caller in any repo

Each below is unreachable from every call site found anywhere, including transitively through
other NL functions. To be discussed and decided one at a time.

**`NLCLIMB.py` — 1 of 16 stale.** The other 15 are live: 3 called directly (`trans`,
`control`, `generation`) and 12 reached through them.

| # | Function | Lines | Note |
|---|---|---|---|
| 1 | `timerule` | 11 | 20-second window slicer. Occupies the slot where DrosoClimb has `fivesecondrule`, which *is* called 29× — likely its renamed successor. Settle with step 1. |

**`NLMATH.py` — 28 of 42 stale.** Live: 11 called directly (`calcgraph`, `meangraph`,
`fallcalc`, `rastergraph`, `velodabest`, `maxvelocity`, `bspeed`, `boutspeed`, `fallingocc`,
`totalheight`, `ospeed`) plus 3 helpers (`frames`, `speedcalc`, `separation`).

*Group A — already marked obsolete in the source:*

| # | Function | Lines | Comment in source |
|---|---|---|---|
| 2 | `violinfall` | 28 | `#obsolete` |
| 3 | `timetoreach` | 53 | `#obsolete` |
| 4 | `positional_arguments` | 56 | `#obsolete now` |

*Group B — displacement / distance metrics:*

| # | Function | Lines |
|---|---|---|
| 5 | `displacementbetweenpauses` | 40 |
| 6 | `boutdisplacement` | 30 |
| 7 | `distpersec` | 24 |
| 8 | `disppersec` | 20 |
| 9 | `sectioneddispchunks` | 31 |
| 10 | `disptravel` | 25 |
| 11 | `totaldisp` | 18 |
| 12 | `straightnessindexmeter` | 25 |

*Group C — height metrics:*

| # | Function | Lines | Note |
|---|---|---|---|
| 13 | `maxheight` | 24 | |
| 14 | `boutheight` | 28 | |
| 15 | `pauseheight` | 28 | |
| 16 | `bheight` | 14 | calls the live `velodabest` |
| 17 | `timespentabovemeanline` | 37 | only caller is `timetype`, itself stale |
| 18 | `timetype` | 17 | calls `timespentabovemeanline`; dead pair |

*Group D — pause/bout behaviour chain. A connected cluster (`pausecomp` → `boutanalysis` →
`behavior`, `countval`); they live or die together:*

| # | Function | Lines |
|---|---|---|
| 19 | `pausecomp` | 31 |
| 20 | `boutanalysis` | 25 |
| 21 | `behavior` | 24 |
| 22 | `countval` | 18 |
| 23 | `pausenumber` | 27 |

*Group E — effect-size / dabest helpers. Handle with most care: these are the OSAR-era
additions absent from DrosoClimb's copy, so "no caller" may mean "written for an analysis not
yet wired up" rather than "abandoned":*

| # | Function | Lines |
|---|---|---|
| 24 | `deltaversion_deltag` | 21 |
| 25 | `deltaversion_meandiff` | 32 |
| 26 | `singledelta` | 9 |
| 27 | `log2speedratio` | 16 |

*Group F — remainder:*

| # | Function | Lines |
|---|---|---|
| 28 | `avgmean` | 13 |
| 29 | `falldbest` | 22 |

**`NLProcessing.py` — 0 of 2 stale.** `generate_lobelocation` is called 8×, `find_number` is
its helper. Nothing to remove. This is also the module that should absorb the 12 duplicated
notebook copies of `find_number` (§6).

**`NLGRAPHS.py` — 8 of 8 stale, 816 lines, never imported by any notebook in any repo.** Not
among the three you named, but it is the largest single block of unreferenced code here, and
its copy is byte-identical to DrosoClimb's, so removing it is a two-repo decision.

| # | Function | Lines |
|---|---|---|
| 30 | `average_list` | 15 |
| 31 | `chambertracking` | 52 |
| 32 | `individualpos` | 69 |
| 33 | `yposmean` | 171 |
| 34 | `individualspeed` | 70 |
| 35 | `speedmeangraph` | 168 |
| 36 | `fallingraph` | 224 |
| 37 | `violinfallgraph` | 47 |

Caveat on the whole queue: this measures *notebook and script* callers. A function only ever
run interactively, or used by an analysis whose notebook was never committed, reads as stale
here. That is the reason for going through them individually rather than bulk-deleting.

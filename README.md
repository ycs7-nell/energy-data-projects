# GRIDCHECK
A small, auditable energy-generator data quality pipeline built with Codex assistance.

## Status: validated against a historical official workbook
Ran on 26,010 EIA-860 2023 Operable generator records. One zero-capacity record flagged and retained. Eleven records (66 fields) independently compared to the original workbook by Codex. See VERIFICATION.md. The synthetic demo remains separate. Real output is in output-real/. This is not a current-year market snapshot. AI assisted development; no runtime LLM is used.

## Quick start (Mac Terminal, from this folder)
```sh
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
python3 gridcheck.py data/demo.csv --demo --source-url synthetic:test-fixture
python3 -m unittest -v
open output/report.html
```
Python 3.10+ recommended. Demo requires only the standard library. The openpyxl dependency is needed for XLSX inputs.

## Run official data
Visit https://www.eia.gov/electricity/data/eia860/ and download an annual EIA-860 ZIP. Extract it on your computer. Select the generator workbook (not the plant or utility workbook). Inspect its worksheet names, reporting year, and headers. Then run, substituting your actual file path:
```sh
python3 gridcheck.py /path/to/generator.xlsx --sheet Operable --source-url https://www.eia.gov/electricity/data/eia860/ --out output-real
open output-real/report.html
```
The workbook adapter searches the first 20 rows for Plant Code and Generator ID and requires Plant Name, State, Nameplate Capacity (MW), and Energy Source 1. It fails if required columns are missing. This adapter was validated against the included 2023 workbook; other years may differ. Record the exact download URL, reporting year, and retrieval date in your source notes; use the exact ZIP or workbook URL in --source-url when available. Input bytes are hashed in manifest.json.

## Outputs
- report.html: local review report, no server needed.
- normalized.csv: whitespace-trimmed records; every row retained.
- issues.csv: review queue with original spreadsheet row / CSV record line for simple single-line CSVs.
- gridcheck.sqlite: SQL table `generators` with all records and lineage.
- manifest.json: source label, filename, worksheet, SHA-256 and counts.

Checks: required values, duplicate plant + generator keys, state codes, nonnumeric/nonfinite/nonpositive capacity, and >2,000 MW generator review threshold. Flags are not proof of errors. Do not total duplicate rows or assume large generators are erroneous. Capacity is MW; generation is MWh. Fuel codes are retained, not validated. No fuzzy matching, cross-source reconciliation, predictive model, or API ingestion is implemented yet. Re-running overwrites outputs in the chosen output directory. Input files are not modified.

Example SQL:
```sql
SELECT state, COUNT(*) AS records FROM generators GROUP BY state;
```
Capacity is deliberately stored as source text to preserve invalid evidence; filter and validate before numeric aggregation.

## Understand the code
`load`: reads CSV or a named XLSX sheet. `analyze`: applies deterministic rules and preserves rows. `main`: writes CSV, SQLite, manifest, and HTML. The duplicate key uses both plant and generator IDs because one plant can have many generators. `source_row` connects each issue back to its source. SHA-256 identifies exact input bytes.

## Before sending to Parisi
1. Run this yourself on a real EIA file.
2. Verify at least ten records manually against the workbook, including clean and flagged records; record row IDs and outcomes.
3. Explain one genuine problem and why you retained or corrected the record. Never edit raw inputs to hide problems.
4. Explain every function and test in your own words.
5. Add a short real-data findings note with reporting year, denominator, limitations, and measured counts.
6. Describe AI use honestly: Codex wrote this initial implementation and ran the demo tests; your own verification remains pending.

Suggested next milestone: reconcile a second official dataset at the correct plant/year level, keeping ambiguous matches for review. A runtime LLM is optional; do not claim one exists.

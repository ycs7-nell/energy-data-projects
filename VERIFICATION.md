# Independent source spot-checks

Reviewer: Codex assistant. These are assistant-performed checks, not user-performed checks.
Source: official EIA-860 2023 generator workbook, Operable sheet. Downloaded 2026-10-26.
Method: separate openpyxl read of original workbook, without using GRIDCHECK load/analyze; compare six fields against CSV output. Purposive sample across workbook, including flagged row; not a statistical accuracy estimate.

| Workbook row | Plant | Generator | MW | Fuel | Six fields match? |
|---|---|---|---|---|---|
| 3 | Sand Point | 1 | 0.9 | DFO | Yes |
| 4 | Sand Point | 2 | 0.9 | DFO | Yes |
| 100 | Colbert | GT9 | 231.2 | NG | Yes |
| 500 | Poe | 2 | 71.4 | WAT | Yes |
| 1000 | Edge Moor | 5 | 446 | NG | Yes |
| 5000 | Johnsonville | G15 | 68 | NG | Yes |
| 7326 | Richard M Flynn | NA2 | 0 | NG | Yes |
| 10000 | Stillwater Facility | 1-1 | 11.8 | GEO | Yes |
| 15000 | Thomson Reuters Data Center Bldg H | 4 | 2 | DFO | Yes |
| 20000 | Whitesboro Solar | GEN1 | 5 | SUN | Yes |
| 26012 | Richmond (NY) | RICH1 | 5 | SUN | Yes |

## Findings
- All 66 sampled field comparisons matched source values across 11 records. This verifies extraction for the sample, not the correctness of EIA reporting.
- Workbook row 26013 is a NOTE footer, with all other cells empty. The original importer included it. The revised importer excludes only this explicit footer pattern; rows with missing IDs are otherwise retained for review.
- Final dataset: 26,010 generator records, one flagged record (row 7326), one capacity issue. The original source itself reports 0 MW at this row; value retained, unresolved. No claim of a confirmed source error.
- Rows 3 and 4 are different generators at the same plant, correctly retained separately.
- Operable includes operating, standby and out-of-service units. It does not mean every record is currently generating electricity.
- 2023 is a historical dataset, not a current market snapshot.

## Explain it in an interview
The initial real-data run exposed a footer parsing problem. I used source-row lineage to trace it, narrowed the exclusion to a recognizable note row, and reran the pipeline. A zero-capacity generator remained; the source confirms that value, so I flagged it instead of inventing a replacement.

Before adopting that explanation as your own, reproduce the run and examine these records yourself.
# E6 — DEL02 model-generated outputs retained for DEL03

Status: observed (within the model), under E5 assumptions. The DEL02 README recorded successful Mesa 3.5.2 verification on November 6, 2026. The checked-in compact distributions and summary contain the results below. This record summarizes those existing outputs; it is not a new simulation run.

Command from the repository root: `python src/project_model/run_experiments.py`. Install dependencies from `requirements.txt` first.

Primary output files in `outputs/`:

- `baseline_raw_00_category_distribution_by_round.csv`
- `alternative_raw_00_category_distribution_by_round.csv`
- `alternative_raw_02_condition_summary.csv`
- `baseline_processed_00_category_exposure_by_round.svg`
- `alternative_processed_00_category_exposure_by_round.svg`
- `alternative_processed_01_baseline_vs_personalized.svg`

The script also generates detailed exposure and trace CSVs and PNG versions of the three SVG graphs.

| Measure | Baseline (0.0) | Alternative (0.8) |
|---|---:|---:|
| Mean distinct categories per feed | 5.00 | 1.45 |
| Mean dominant-category share | 0.300 | 0.875 |

Both conditions begin with the same category counts. Baseline remains at five categories and 30% dominant share for all 20 rounds. Alternative reaches one category (Music & dance) and 100% dominant share from round 6 through round 20.

Limit: results describe one fixed-seed comparison of synthetic model rules; they do not establish actual TikTok recommendations or viewer experience.

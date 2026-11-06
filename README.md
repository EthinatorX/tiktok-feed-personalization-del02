# Personalized Short-Form Video Feed — DEL02.2 Prototype

A small Mesa agent-based model for investigating how a personalization weight changes the category distribution of videos presented to one simulated viewer over repeated feed rounds.

> **Scope warning:** This is a synthetic, selective representation informed by public descriptions of TikTok's For You feed. It is not TikTok's algorithm, does not use TikTok user data, and does not establish how real TikTok viewers or the platform behave.

## Validation status

See [`docs/VALIDATION_STATUS.md`](docs/VALIDATION_STATUS.md) before submitting. The current outputs are provisional logic-check outputs from a test-only compatibility shim; regenerate them under the installed Mesa dependency before treating them as verified Mesa outputs.

## Requirements

- Python 3.12 or newer
- Mesa 3.5.2
- Matplotlib 3.8 or newer and below 4.0

## Setup (Windows PowerShell)

From the repository root:

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
python -m pip install --upgrade pip
python -m pip install -r requirements.txt
```

If PowerShell blocks activation, use the equivalent activation command for your shell, or run the virtual-environment Python directly.

## Run the preserved Mesa source example

```powershell
python src/boltzmann_wealth_model/run_model.py
```

This runs the preserved Mesa Boltzmann Wealth tutorial model independently of the project adaptation. Its source and attribution are documented in `src/boltzmann_wealth_model/SOURCE.md`.

## Run the project adaptation and generate outputs

```powershell
python src/project_model/run_experiments.py
```

The command runs both conditions with the same random seed and initial data:

- **Baseline:** personalization weight `λ = 0.0` (ranking uses video baseline scores only).
- **Alternative:** personalization weight `λ = 0.8` (category preferences have a stronger influence on ranking).

Both runs use 120 synthetic videos (20 in each of six categories), one simulated viewer, 10 videos per feed, and 20 recommendation rounds. The simulated viewer begins with a preference score of `0.50` for every category. A positive engagement occurs with probability `0.20 + 0.60 × category preference at the start of the round`; each positive engagement raises that category preference by `0.03`, capped at `1.0`. Preference updates are applied after all 10 videos in a round have been processed, so an interaction affects later rounds rather than later videos in the same feed. A video can reappear in later rounds but cannot appear twice in the same feed.

## Run the basic checks

```powershell
python -m unittest discover -s tests -v
```

## Output files

The experiment script writes these files to `outputs/`:

| File | Description |
|---|---|
| `baseline_raw_00_category_exposure_by_round.csv` | Per-round category counts and feed-level diversity measures for `λ = 0.0`. |
| `alternative_raw_00_category_exposure_by_round.csv` | Same measures for `λ = 0.8`. |
| `baseline_raw_01_recommendation_trace.csv` | Video-level recommendation and simulated engagement trace for the baseline. |
| `alternative_raw_01_recommendation_trace.csv` | Video-level recommendation and simulated engagement trace for the alternative. |
| `baseline_processed_00_category_exposure_by_round.svg` | Baseline graph of category counts over rounds. |
| `alternative_processed_00_category_exposure_by_round.svg` | Alternative graph of category counts over rounds. |
| `alternative_processed_01_baseline_vs_personalized.svg` | Comparison of category diversity and dominant-category share across conditions. |
| `alternative_raw_02_condition_summary.csv` | Summary measures for both conditions. |

PNG counterparts are also generated as raster previews.

## Model structure

- `src/boltzmann_wealth_model/` — preserved Mesa tutorial source example.
- `src/project_model/` — project-specific model and experiment runner.
- `outputs/` — raw CSV traces and processed graphs.
- `docs/` — project notes and provenance.

## Important modelling assumptions and limitations

1. The six categories are researcher-defined labels, not a claim that TikTok uses this exact classification.
2. The 120 videos and baseline scores are synthetic. Their equal category distribution is a controlled starting condition, not a measured sample of TikTok.
3. Engagement probability and the preference update increment are invented model rules. They are not estimates of actual TikTok user behaviour.
4. Ranking is represented by a two-part weighted score. TikTok's actual ranking uses many signals and undisclosed implementation details.
5. This first slice models one viewer and does not include creator relationships, ads, moderation, eligibility rules, or TikTok's other diversification mechanisms.
6. The initial comparison changes only `λ`; the other rules and seeded starting conditions remain fixed.

Read the DEL02.1 report for the inquiry rationale, evidence, interpretation, and next steps.

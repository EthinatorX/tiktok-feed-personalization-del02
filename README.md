# Personalized Short-Form Video Feed — DEL02.2 Prototype

A small Mesa agent-based model for investigating how a personalization weight changes the category distribution of videos presented to one simulated viewer over repeated feed rounds.

> **Scope warning:** This is a synthetic, selective representation informed by public descriptions of TikTok's For You feed. It is not TikTok's algorithm, does not use TikTok user data, and does not establish how real TikTok viewers or the platform behave.

## Verification

The `Mesa prototype checks` GitHub Actions workflow completed successfully on **2026-11-06** using Python 3.12 and Mesa 3.5.2. It installed the dependencies, passed the unit tests, ran the preserved Mesa example, and ran the baseline/alternative project experiments. See [the successful workflow run](https://github.com/EthinatorX/tiktok-feed-personalization-del02/actions/runs/42141569948). The checked-in CSV/SVG outputs were regenerated from that Mesa run.

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

## Run the preserved Mesa source example

```powershell
python src/boltzmann_wealth_model/run_model.py
```

## Run the project adaptation and generate outputs

```powershell
python src/project_model/run_experiments.py
```

The command compares:
- **Baseline:** `λ = 0.0`, ranking based on fixed video baseline scores.
- **Alternative:** `λ = 0.8`, category preferences have a stronger influence on ranking.

Both runs use 120 synthetic videos (20 per category), one simulated viewer, 10 videos per feed, 20 rounds, and random seed 42. The viewer begins with category preferences of 0.50. Positive engagement probability is `0.20 + 0.60 × category preference at the start of the round`; each positive engagement raises that category preference by 0.03, capped at 1.0. Updates occur after the full feed is processed.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Output files

The experiment script writes:
- Compact per-round distribution CSVs: `baseline_raw_00_category_distribution_by_round.csv` and `alternative_raw_00_category_distribution_by_round.csv`.
- Detailed per-category exposure CSVs and per-video recommendation traces for both conditions.
- Category exposure SVG/PNG graphs for both conditions.
- A baseline-versus-alternative comparison graph and condition summary CSV.

The checked-in compact CSVs and SVG graphs were regenerated from the successful Mesa 3.5.2 GitHub Actions run linked above. The full generated output set is also retained as the workflow artifact `del02-model-outputs`.

## Model assumptions and limitations

1. The six categories are researcher-defined labels, not TikTok's official taxonomy.
2. The 120 videos and their baseline scores are synthetic and equally distributed by design.
3. Engagement probability and preference updates are invented model rules, not estimates of actual user behaviour.
4. Ranking uses a simplified weighted score; TikTok's actual ranking uses more signals and undisclosed details.
5. The model represents one viewer and omits creator relationships, ads, moderation, eligibility rules, and other recommendation mechanisms.
6. The experiment changes only `λ`; the other rules and starting conditions remain fixed.

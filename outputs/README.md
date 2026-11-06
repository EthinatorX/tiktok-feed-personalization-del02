# Output files

The checked-in compact CSV files and SVG graphs were regenerated from a successful Mesa 3.5.2 run in GitHub Actions on 2026-11-06: https://github.com/EthinatorX/tiktok-feed-personalization-del02/actions/runs/42141569948

Run `python src/project_model/run_experiments.py` from the repository root to recreate the outputs. The compact `*_category_distribution_by_round.csv` files contain one row per round; the detailed `*_category_exposure_by_round.csv` files contain one row per category per round. The recommendation trace files record each selected video and its simulated engagement outcome. The processed SVG/PNG files visualize category exposure and the baseline/alternative comparison.

The full generated output directory is retained as the GitHub Actions artifact `del02-model-outputs`.

# Output directory

Run `python src/project_model/run_experiments.py` from the repository root to recreate the baseline and alternative CSV files and PNG/SVG figures. The compact `*_category_distribution_by_round.csv` files contain one row per round; the detailed `*_category_exposure_by_round.csv` files contain one row per category per round. The recommendation trace files record each selected video and the simulated engagement outcome. The processed SVG/PNG files visualize category exposure and the baseline/alternative comparison.

The checked-in first-pass CSV/SVG outputs are marked provisional because they were generated with a test-only compatibility shim rather than an installed Mesa package. Regenerate them using the pinned Mesa dependency before interpreting them as DEL02 model-run evidence.

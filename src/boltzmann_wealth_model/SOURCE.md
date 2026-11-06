# Preserved Mesa source example

- **Example:** Boltzmann Wealth Model (also called the Money Model in the introductory tutorial).
- **Primary source:** Mesa Team, “Creating Your First Model — The Boltzmann Wealth Model,” Mesa stable documentation: https://mesa.readthedocs.io/stable/tutorials/0_first_model.html
- **Source repository:** https://github.com/mesa/mesa
- **Accessed:** 2026-11-05.
- **Mesa dependency used by this project:** `mesa==3.5.2`.
- **License:** Mesa is distributed under the Apache License 2.0. See https://github.com/mesa/mesa/blob/main/LICENSE.

The `MoneyAgent` and `MoneyModel` core logic in `model.py` preserves the official tutorial's agent-exchange example: agents begin with one unit of wealth, and an agent with wealth can transfer one unit to a randomly selected agent. `run_model.py` is a small command-line entry point so the tutorial model can be run independently from this repository. The preserved source example is kept separate from the TikTok-feed project adaptation in `src/project_model/`.

The source example is included for provenance and comparison. The recommendation-feed model is a project-specific adaptation and does not claim that the wealth-transfer mechanism is analogous to TikTok's recommendation algorithm.

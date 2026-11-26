# E5 — Synthetic model inputs and assumptions

Status: synthetic (researcher-defined inputs and rules). This record documents the DEL02 model retained for DEL03; no actual TikTok data is used.

Source implementation: `src/project_model/model.py`; comparison driver: `src/project_model/run_experiments.py`.

- 120 synthetic video agents: 20 per category (Food & cooking, Travel & places, Fashion & beauty, Comedy & memes, Gaming, Music & dance). Each has an ID, a category and a fixed baseline score drawn uniformly from 0.25 to 0.75.
- One viewer agent: preference estimates start at 0.50 for all categories.
- Both conditions: seed 42, 20 rounds, 10 videos per feed. No removal between rounds.
- Ranking: `(1 - lambda) * baseline_score + lambda * category_preference`. The top ten unique videos in each round are selected. Baseline lambda = 0.0; alternative lambda = 0.8.
- Positive engagement: probability `0.20 + 0.60 * round_start_category_preference`, bounded to [0,1]. After processing the entire feed, each positive interaction increases that category's preference by 0.03, capped at 1.0; non-engagement does not decrease preference.
- The catalogue and starting conditions are shared between the seeded runs. The personalization weight is the only deliberately varied setting.

Limit: the category taxonomy, catalogue, scores, probability formula, starting preferences and parameter values are synthetic choices, not measured TikTok values.

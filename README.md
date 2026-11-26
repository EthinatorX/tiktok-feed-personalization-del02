# TikTok's For You Feed: How Personalization Strength Affects Video Category Distribution

EECS 4461 F26 — Cumulative Inquiry Project (DEL03)

## Inquiry question and scope

How does increasing the personalization weight in a simplified model of TikTok's For You feed change the category distribution of recommended videos presented to one simulated viewer over 20 feed rounds?

The project uses Mesa to selectively represent a repeated recommendation and engagement process. It is informed by public descriptions of TikTok's For You feed, but does not reproduce TikTok's actual recommendation algorithm, use real TikTok data, or measure real viewer behaviour.

## Requirements and setup (Windows PowerShell)

- Python 3.12 or newer
- Mesa 3.5.2
- Matplotlib >= 3.8, < 4.0

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

## Run the project comparison

```powershell
python src/project_model/run_experiments.py
```

The script generates both conditions using the original DEL02 implementation. No external dataset is required.

| Setting | Baseline | Alternative |
|---|---:|---:|
| Personalization weight | 0.0 | 0.8 |
| Simulated viewers | 1 | 1 |
| Synthetic videos | 120 | 120 |
| Categories | 6 | 6 |
| Videos per category | 20 | 20 |
| Feed size | 10 | 10 |
| Rounds | 20 | 20 |
| Seed | 42 | 42 |
| Initial category preference | 0.50 | 0.50 |
| Fixed video baseline score range | 0.25–0.75 | 0.25–0.75 |
| Engagement base | 0.20 | 0.20 |
| Engagement interest weight | 0.60 | 0.60 |
| Preference update increment | 0.03 | 0.03 |
| Maximum preference | 1.0 | 1.0 |

The six categories are Food & cooking, Travel & places, Fashion & beauty, Comedy & memes, Gaming, and Music & dance. Each video has a fixed randomly generated baseline score. The ranking score is `(1 - lambda) * baseline_score + lambda * category_preference`. The top ten videos are selected each round. Positive engagement is simulated using `0.20 + 0.60 * category_preference` at the start of the round (bounded to [0, 1]). Each positive interaction increases the corresponding category preference by 0.03, capped at 1.0. Updates take place after the full feed has been processed. Non-engagement does not decrease preference.

## Run tests

```powershell
python -m unittest discover -s tests -v
```

## Outputs

The experiment writes the following files in `outputs/`:

| File | Contents |
|---|---|
| `baseline_raw_00_category_distribution_by_round.csv` | Baseline counts and feed-level measures |
| `alternative_raw_00_category_distribution_by_round.csv` | Alternative counts and feed-level measures |
| `baseline_raw_00_category_exposure_by_round.csv` | Detailed baseline exposure and preference records |
| `alternative_raw_00_category_exposure_by_round.csv` | Detailed alternative exposure and preference records |
| `baseline_raw_01_recommendation_trace.csv` | Baseline video-level recommendations and simulated engagement |
| `alternative_raw_01_recommendation_trace.csv` | Alternative video-level recommendations and simulated engagement |
| `alternative_raw_02_condition_summary.csv` | Summary of both conditions |
| `baseline_processed_00_category_exposure_by_round.svg` and `.png` | Baseline category exposure plot |
| `alternative_processed_00_category_exposure_by_round.svg` and `.png` | Alternative category exposure plot |
| `alternative_processed_01_baseline_vs_personalized.svg` and `.png` | Comparison of distinct categories and dominant-category share |

Distinct categories per feed counts the categories present in the ten recommendations. Dominant-category share is the fraction of those recommendations belonging to the most common category.

## Results retained from DEL02

| Measure | Baseline | Alternative |
|---|---:|---:|
| Mean distinct categories per feed | 5.00 | 1.45 |
| Mean dominant-category share | 30.0% | 87.5% |

Both conditions start with the same category distribution. Under seed 42, no Food & cooking video is among the ten highest baseline scores. As the baseline scores are fixed, the baseline repeats the same ten videos and retains five distinct categories per round. The alternative reaches a feed consisting entirely of Music & dance from round 6 onward. This is a result of the specified synthetic model, not an observed pattern on TikTok.

## Limitations

The video collection, categories, starting preferences and numerical rules are synthetic choices. There is only one simulated viewer and one random seed per condition. Videos remain eligible after recommendation, and the baseline repeats individual videos even though it retains more categories per feed. The engagement and preference-update rules create a reinforcing process. The model excludes creator behaviour, moderation, advertisements, social relationships, and other recommendation signals. It does not measure viewer satisfaction, perceived relevance or discovery. The results cannot establish the effects of personalization for actual TikTok viewers.

## Evidence and supporting materials

Evidence identifiers are consistent with the final dossier:

- E1: TikTok. (n.d.). *How content is recommended across TikTok.* https://support.tiktok.com/en/using-tiktok/exploring-videos/how-tiktok-recommends-content
- E2: TikTok. (2020). *How TikTok recommends videos #ForYou.* https://newsroom.tiktok.com/how-tiktok-recommends-videos-for-you
- E3: Adomavicius et al. (2022). *Recommender systems, ground truth, and preference pollution.* https://doi.org/10.1002/aaai.12055
- E4: Mesa Team. (n.d.). *Boltzmann wealth model.* https://mesa.readthedocs.io/v3.5.2/examples/basic/boltzmann_wealth_model.html
- E5: [Synthetic model inputs and rules](docs/evidence/E5_synthetic_model_inputs.md).
- E6: [Observed outputs within the model](docs/evidence/E6_model_output_record.md).

The original Mesa example is retained under `src/boltzmann_wealth_model/`; the adapted model is under `src/project_model/`. The [final ecosystem map](docs/figures/ecosystem_map.png) shows the deployed arrangement, evidence identifiers, and the boundary of the computational representation.

See [changes since DEL02](docs/DEL03_CHANGELOG.md).

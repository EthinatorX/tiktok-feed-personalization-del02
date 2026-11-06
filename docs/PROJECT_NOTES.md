# Project notes

## Inquiry
How does changing the strength of personalization in a simplified model of TikTok's For You feed affect the distribution of video categories presented to a simulated viewer over 20 recommendation rounds?

## Targeted DEL02 slice
One simulated viewer, 120 synthetic video agents across six balanced categories, one recommendation rule, one synthetic engagement/update rule, and one parameter comparison (lambda 0.0 vs lambda 0.8). The feed contains 10 unique videos per round for 20 rounds. Videos can repeat across rounds.

## Why this slice
It isolates the personalization weight in the ranking rule while holding the video collection, initial viewer preferences, random seed, feed size, engagement rule, and number of rounds fixed.

## Model rule
ranking_score = (1 - lambda) * video_baseline_score + lambda * viewer_category_preference

Positive engagement probability = 0.20 + 0.60 * current_category_preference.

Each positive engagement adds 0.03 to that category's estimated preference, capped at 1.0.

All numeric values are synthetic modelling assumptions rather than measurements of TikTok.

"""Run fixed-seed baseline and alternative conditions; write CSV and PNG/SVG outputs."""

from __future__ import annotations

import csv
from pathlib import Path

import matplotlib.pyplot as plt

from model import (
    CATEGORIES,
    DEFAULT_FEED_SIZE,
    DEFAULT_ROUNDS,
    DEFAULT_SEED,
    RecommendationFeedModel,
    RunSettings,
)

ROOT = Path(__file__).resolve().parents[2]
OUTPUT_DIR = ROOT / "outputs"

CONDITIONS = {
    "baseline": 0.0,
    "alternative": 0.8,
}


def write_csv(path: Path, rows: list[dict]) -> None:
    if not rows:
        raise ValueError(f"No rows to write to {path}")
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)


def write_distribution_csv(label: str, rows: list[dict], weight: float) -> None:
    """Write one compact row per round with category counts and diversity measures."""
    category_columns = {
        "Food & cooking": "food_cooking",
        "Travel & places": "travel_places",
        "Fashion & beauty": "fashion_beauty",
        "Comedy & memes": "comedy_memes",
        "Gaming": "gaming",
        "Music & dance": "music_dance",
    }
    by_round: dict[int, dict] = {}
    for row in rows:
        round_number = int(row["round"])
        record = by_round.setdefault(round_number, {
            "round": round_number,
            **{column: 0 for column in category_columns.values()},
            "distinct_categories": int(row["distinct_categories_in_feed"]),
            "dominant_category_share": row["dominant_category_share"],
            "personalization_weight": weight,
        })
        record[category_columns[row["category"]]] = int(row["recommendation_count"])
    write_csv(
        OUTPUT_DIR / f"{label}_raw_00_category_distribution_by_round.csv",
        [by_round[number] for number in sorted(by_round)],
    )


def run_condition(label: str, personalization_weight: float) -> tuple[list[dict], list[dict]]:
    settings = RunSettings(
        personalization_weight=personalization_weight,
        rounds=DEFAULT_ROUNDS,
        feed_size=DEFAULT_FEED_SIZE,
        seed=DEFAULT_SEED,
    )
    model = RecommendationFeedModel(settings)
    while model.round_number < model.rounds:
        model.step()

    exposure_rows = model.history
    feed_rows = model.feed_history

    write_csv(
        OUTPUT_DIR / f"{label}_raw_00_category_exposure_by_round.csv",
        exposure_rows,
    )
    write_csv(
        OUTPUT_DIR / f"{label}_raw_01_recommendation_trace.csv",
        feed_rows,
    )
    write_distribution_csv(label, exposure_rows, personalization_weight)
    make_exposure_plot(label, exposure_rows, personalization_weight)
    return exposure_rows, feed_rows


def make_exposure_plot(label: str, rows: list[dict], weight: float) -> None:
    fig, ax = plt.subplots(figsize=(10, 5.5))
    for category in CATEGORIES:
        category_rows = [row for row in rows if row["category"] == category]
        ax.plot(
            [row["round"] for row in category_rows],
            [row["recommendation_count"] for row in category_rows],
            marker="o",
            linewidth=1.8,
            markersize=3,
            label=category,
        )
    ax.set(
        title=f"Category exposure by round — {label.title()} (λ = {weight})",
        xlabel="Recommendation round",
        ylabel="Videos from category in feed (of 10)",
        xticks=list(range(1, DEFAULT_ROUNDS + 1)),
        ylim=(0, DEFAULT_FEED_SIZE),
    )
    ax.grid(True, alpha=0.25)
    ax.legend(ncol=2, frameon=False)
    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / f"{label}_processed_00_category_exposure_by_round.png",
        dpi=180,
    )
    fig.savefig(
        OUTPUT_DIR / f"{label}_processed_00_category_exposure_by_round.svg",
    )
    plt.close(fig)


def make_comparison_plot(condition_rows: dict[str, list[dict]]) -> None:
    fig, axes = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
    for label, rows in condition_rows.items():
        # Repeated category rows hold the same feed-level diversity value.
        unique_rounds = {}
        for row in rows:
            unique_rounds[row["round"]] = row
        ordered = [unique_rounds[r] for r in sorted(unique_rounds)]
        axes[0].plot(
            [row["round"] for row in ordered],
            [row["distinct_categories_in_feed"] for row in ordered],
            marker="o",
            label=label.title(),
        )
        axes[1].plot(
            [row["round"] for row in ordered],
            [row["dominant_category_share"] for row in ordered],
            marker="o",
            label=label.title(),
        )
    axes[0].set_ylabel("Distinct categories per feed")
    axes[0].set_ylim(0, len(CATEGORIES) + 0.5)
    axes[0].set_title("Feed diversity and dominant-category share")
    axes[1].set_ylabel("Share of most common category")
    axes[1].set_xlabel("Recommendation round")
    axes[1].set_ylim(0, 1.05)
    for ax in axes:
        ax.set_xticks(list(range(1, DEFAULT_ROUNDS + 1)))
        ax.grid(True, alpha=0.25)
        ax.legend(frameon=False)
    fig.tight_layout()
    fig.savefig(
        OUTPUT_DIR / "alternative_processed_01_baseline_vs_personalized.png",
        dpi=180,
    )
    fig.savefig(
        OUTPUT_DIR / "alternative_processed_01_baseline_vs_personalized.svg",
    )
    plt.close(fig)


def write_summary(condition_rows: dict[str, list[dict]]) -> None:
    summary = []
    for label, rows in condition_rows.items():
        round_rows = {}
        for row in rows:
            round_rows[row["round"]] = row
        values = list(round_rows.values())
        summary.append({
            "condition": label,
            "personalization_weight": CONDITIONS[label],
            "rounds": len(values),
            "feed_size": DEFAULT_FEED_SIZE,
            "mean_distinct_categories": round(
                sum(row["distinct_categories_in_feed"] for row in values) / len(values), 3
            ),
            "mean_dominant_category_share": round(
                sum(row["dominant_category_share"] for row in values) / len(values), 3
            ),
        })
    write_csv(OUTPUT_DIR / "alternative_raw_02_condition_summary.csv", summary)


def main() -> None:
    OUTPUT_DIR.mkdir(parents=True, exist_ok=True)
    condition_rows: dict[str, list[dict]] = {}
    for label, weight in CONDITIONS.items():
        rows, _ = run_condition(label, weight)
        condition_rows[label] = rows
    make_comparison_plot(condition_rows)
    write_summary(condition_rows)
    print("Completed baseline and alternative recommendation-feed runs.")
    print(f"Outputs saved to: {OUTPUT_DIR}")
    print("Baseline λ=0.0; alternative λ=0.8; seed=42; rounds=20; feed size=10.")


if __name__ == "__main__":
    main()

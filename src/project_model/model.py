"""A small Mesa ABM representing a personalized short-form video feed.

This is a selective, synthetic representation. It is not TikTok's algorithm.
"""

from __future__ import annotations

from collections import Counter
from dataclasses import dataclass
from typing import Any

import mesa


CATEGORIES = (
    "Food & cooking",
    "Travel & places",
    "Fashion & beauty",
    "Comedy & memes",
    "Gaming",
    "Music & dance",
)

VIDEOS_PER_CATEGORY = 20
DEFAULT_FEED_SIZE = 10
DEFAULT_ROUNDS = 20
DEFAULT_SEED = 42
DEFAULT_LEARNING_RATE = 0.03
DEFAULT_ENGAGEMENT_BASE = 0.20
DEFAULT_ENGAGEMENT_INTEREST_WEIGHT = 0.60


class VideoAgent(mesa.Agent):
    """A synthetic video with a fixed category and baseline ranking score."""

    def __init__(self, model: "RecommendationFeedModel", video_id: str,
                 category: str, baseline_score: float):
        super().__init__(model)
        self.video_id = video_id
        self.category = category
        self.baseline_score = float(baseline_score)


class ViewerAgent(mesa.Agent):
    """One simulated viewer with an estimated interest per content category."""

    def __init__(self, model: "RecommendationFeedModel"):
        super().__init__(model)
        self.preferences = {category: 0.50 for category in CATEGORIES}

    def engagement_probability(self, category: str) -> float:
        """Synthetic engagement rule; not an empirical TikTok probability."""
        preference = self.preferences[category]
        probability = (
            self.model.engagement_base
            + self.model.engagement_interest_weight * preference
        )
        return min(1.0, max(0.0, probability))

    def engage_with(self, video: VideoAgent) -> None:
        """Increase the category estimate after a simulated positive interaction."""
        old_value = self.preferences[video.category]
        self.preferences[video.category] = min(
            1.0, old_value + self.model.learning_rate
        )


@dataclass(frozen=True)
class RunSettings:
    """Settings shared by the baseline and alternative model runs."""

    personalization_weight: float
    rounds: int = DEFAULT_ROUNDS
    feed_size: int = DEFAULT_FEED_SIZE
    seed: int = DEFAULT_SEED
    learning_rate: float = DEFAULT_LEARNING_RATE
    engagement_base: float = DEFAULT_ENGAGEMENT_BASE
    engagement_interest_weight: float = DEFAULT_ENGAGEMENT_INTEREST_WEIGHT


class RecommendationFeedModel(mesa.Model):
    """Repeated recommendation, engagement, and preference-update process."""

    def __init__(self, settings: RunSettings):
        super().__init__(seed=settings.seed)

        if not 0.0 <= settings.personalization_weight <= 1.0:
            raise ValueError("personalization_weight must be between 0 and 1")
        if settings.rounds < 1:
            raise ValueError("rounds must be at least 1")
        if not 1 <= settings.feed_size <= len(CATEGORIES) * VIDEOS_PER_CATEGORY:
            raise ValueError("feed_size must be between 1 and the number of videos")
        if not 0.0 <= settings.learning_rate <= 1.0:
            raise ValueError("learning_rate must be between 0 and 1")

        self.personalization_weight = settings.personalization_weight
        self.rounds = settings.rounds
        self.feed_size = settings.feed_size
        self.learning_rate = settings.learning_rate
        self.engagement_base = settings.engagement_base
        self.engagement_interest_weight = settings.engagement_interest_weight
        self.round_number = 0
        self.history: list[dict[str, Any]] = []
        self.feed_history: list[dict[str, Any]] = []

        # The viewer and all video entries are Mesa agents. The video collection
        # is generated once and remains identical within each seeded condition.
        self.viewer = ViewerAgent(self)
        self.videos: list[VideoAgent] = []
        video_number = 1
        for category in CATEGORIES:
            for _ in range(VIDEOS_PER_CATEGORY):
                baseline = self.random.uniform(0.25, 0.75)
                video = VideoAgent(
                    self,
                    video_id=f"V{video_number:03d}",
                    category=category,
                    baseline_score=baseline,
                )
                self.videos.append(video)
                video_number += 1

    def ranking_score(self, video: VideoAgent) -> float:
        """Combine fixed video priority with the viewer's category estimate."""
        weight = self.personalization_weight
        preference = self.viewer.preferences[video.category]
        return (
            (1.0 - weight) * video.baseline_score
            + weight * preference
        )

    def recommend(self) -> list[VideoAgent]:
        """Return the highest-ranked unique videos for the current feed."""
        ranked = sorted(
            self.videos,
            key=lambda video: (
                self.ranking_score(video),
                video.baseline_score,
                video.video_id,
            ),
            reverse=True,
        )
        return ranked[: self.feed_size]

    def step(self) -> None:
        """Present one feed, simulate engagement, update preference states."""
        if self.round_number >= self.rounds:
            self.running = False
            return

        feed = self.recommend()
        category_counts = Counter(video.category for video in feed)
        engaged_count = 0
        round_start_preferences = self.viewer.preferences.copy()
        engaged_videos: list[VideoAgent] = []

        # All recommendations and engagement probabilities use the state at
        # the start of this round. Updates are applied after the whole feed has
        # been processed, so an interaction affects later rounds, not later
        # videos in the same feed.
        for video in feed:
            preference = round_start_preferences[video.category]
            probability = (
                self.engagement_base
                + self.engagement_interest_weight * preference
            )
            probability = min(1.0, max(0.0, probability))
            engaged = self.random.random() < probability
            self.feed_history.append({
                "round": self.round_number + 1,
                "video_id": video.video_id,
                "category": video.category,
                "ranking_score": round(self.ranking_score(video), 6),
                "engaged": int(engaged),
            })
            if engaged:
                engaged_count += 1
                engaged_videos.append(video)

        for video in engaged_videos:
            self.viewer.engage_with(video)

        self.round_number += 1
        distinct_categories = len(category_counts)
        dominant_count = max(category_counts.values()) if category_counts else 0
        dominant_share = dominant_count / self.feed_size

        for category in CATEGORIES:
            self.history.append({
                "round": self.round_number,
                "category": category,
                "recommendation_count": category_counts.get(category, 0),
                "distinct_categories_in_feed": distinct_categories,
                "dominant_category_share": round(dominant_share, 4),
                "engaged_videos_in_round": engaged_count,
                "preference_after_round": round(
                    self.viewer.preferences[category], 4
                ),
            })

        if self.round_number >= self.rounds:
            self.running = False

"""Basic checks for the project model (requires requirements.txt)."""
import unittest

from src.project_model.model import (
    CATEGORIES,
    RecommendationFeedModel,
    RunSettings,
    VIDEOS_PER_CATEGORY,
)


class RecommendationFeedModelTests(unittest.TestCase):
    def setUp(self):
        self.model = RecommendationFeedModel(
            RunSettings(personalization_weight=0.8, rounds=2, seed=42)
        )

    def test_video_collection_is_balanced(self):
        self.assertEqual(len(self.model.videos), 120)
        for category in CATEGORIES:
            self.assertEqual(
                sum(video.category == category for video in self.model.videos),
                VIDEOS_PER_CATEGORY,
            )

    def test_feed_has_unique_videos_and_expected_size(self):
        feed = self.model.recommend()
        self.assertEqual(len(feed), 10)
        self.assertEqual(len({video.video_id for video in feed}), 10)

    def test_baseline_ranking_ignores_preferences(self):
        baseline = RecommendationFeedModel(
            RunSettings(personalization_weight=0.0, rounds=2, seed=42)
        )
        first = [video.video_id for video in baseline.recommend()]
        baseline.viewer.preferences["Gaming"] = 1.0
        second = [video.video_id for video in baseline.recommend()]
        self.assertEqual(first, second)

    def test_preference_update_is_capped(self):
        video = next(v for v in self.model.videos if v.category == "Gaming")
        self.model.viewer.preferences["Gaming"] = 0.99
        self.model.viewer.engage_with(video)
        self.assertEqual(self.model.viewer.preferences["Gaming"], 1.0)

    def test_step_records_six_category_rows(self):
        self.model.step()
        self.assertEqual(len(self.model.history), len(CATEGORIES))
        self.assertEqual(self.model.round_number, 1)


if __name__ == "__main__":
    unittest.main()

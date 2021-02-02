import unittest
from decimal import *

from project.utils.execute_nfl_api import ExecuteNflApi
import project.constants as const
import project.config as config


class TestExecuteNflApi(unittest.TestCase):

    def setUp(self):
        self.args = {
            "league": "NFL",
            "start_date": "2020-01-12",
            "end_date": "2020-01-19"
        }
        self.execute_nfl_api = ExecuteNflApi(self.args)

    def test_pull_event_data(self):
        res, scoreboard = self.execute_nfl_api.pull_nfl_event_data_from_api(
            const.SCOREBOARD_URL.format
            (
                self.args["league"],
                self.args["start_date"],
                self.args["end_date"],
                config.API_KEY
            )
        )

        self.assertTrue(res)
        self.assertIsInstance(scoreboard, dict)

    def test_get_scoreboard(self):
        res, scoreboard = self.execute_nfl_api.get_scoreboard()

        self.assertTrue(res)
        self.assertIsInstance(scoreboard, dict)

    def test_get_rankings(self):
        res, rankings = self.execute_nfl_api.get_rankings()

        self.assertTrue(res)
        self.assertIsInstance(rankings, dict)

    def test_combined_data(self):
        _, scoreboard = self.execute_nfl_api.get_scoreboard()
        _, rankings = self.execute_nfl_api.get_rankings()
        res = self.execute_nfl_api.combined_data(scoreboard, rankings)

        self.assertEqual(len(res[0]), 13)
        self.assertEqual(Decimal(res[0]["away_rank_points"]).as_tuple().exponent, -2)
        self.assertEqual(Decimal(res[0]["home_rank_points"]).as_tuple().exponent, -2)

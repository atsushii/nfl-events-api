import requests
import datetime

import project.constants as const
import project.config as config
from project import app


class ExecuteNflApi:

    def __init__(self, args):
        self.args = args

    def pull_nfl_event_data_from_api(self, url):

        res = requests.get(url)

        return res.status_code == 200, res.json()

    def get_scoreboard(self):
        success, scoreboard = self.pull_nfl_event_data_from_api(
            const.SCOREBOARD_URL.format
            (
                self.args["league"],
                self.args["start_date"],
                self.args["end_date"],
                config.API_KEY
            )
        )

        return success, scoreboard

    def get_rankings(self):
        success, rankings = self.pull_nfl_event_data_from_api(
            const.TEAM_RANKINGS_URL.format
            (
                self.args["league"],
                config.API_KEY
            )
        )

        return success, rankings

    def combine_rankings_to_scoreboard(self, combined_event_data, rankings):
        try:
            for v in rankings["results"]["data"]:
                if combined_event_data["away_team_id"] == v['team_id']:
                    combined_event_data["away_rank"] = v["rank"]
                    combined_event_data["away_rank_points"] = f'{float(v["adjusted_points"]):.2f}'
                elif combined_event_data["home_team_id"] == v['team_id']:
                    combined_event_data["home_rank"] = v["rank"]
                    combined_event_data["home_rank_points"] = f'{float(v["adjusted_points"]):.2f}'
        except KeyError:
            app.logger.info("rankings data doesn't contain expected key")
            return {"message": "error"}

        return combined_event_data

    def combined_data(self, scoreboard, rankings, result=None):

        if result is None:
            result = []

        try:
            for k, v in scoreboard['results'].items():
                if v:
                    for k1, v1 in v['data'].items():
                        event_date, event_time = v1["event_date"].split(' ')
                        event_date = datetime.datetime.strptime(event_date, "%Y-%m-%d").strftime("%d-%m-%Y")

                        event_data = {
                            "event_id": v1["event_id"],
                            "event_date": event_date,
                            "event_time": event_time,
                            "away_team_id": v1["away_team_id"],
                            "away_nick_name": v1["away_nick_name"],
                            "away_city": v1["away_city"],
                            "away_rank": "",
                            "away_rank_points": "",
                            "home_team_id": v1["home_team_id"],
                            "home_nick_name": v1["home_nick_name"],
                            "home_city": v1["home_city"],
                            "home_rank": "",
                            "home_rank_points": ""
                        }
                        combined_event_data = self.combine_rankings_to_scoreboard(event_data, rankings)

                        result.append(combined_event_data)
        except KeyError:
            app.logger.info("scoreboard data doesn't contain expected key")
            return {"message": "error"}

        return result

    def main(self):
        success, scoreboard = self.get_scoreboard()

        if not success:
            app.logger.info(scoreboard)

            return {"message": "error"}

        success, rankings = self.get_rankings()

        if not success:
            app.logger.info(rankings)
            return {"message": "error"}

        result = self.combined_data(scoreboard, rankings)

        return result

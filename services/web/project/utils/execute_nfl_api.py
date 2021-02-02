import requests
import datetime

import project.constants as const
import project.config as config


class ExecuteNflApi:

    def __init__(self, args):
        self.args = args

    def pull_nfl_event_data_from_api(self, url):

        res = requests.get(url)

        return res.status_code != 200, res.json()

    def combine_rankings_to_scoreboard(self, data, rankings):
        for v in rankings["results"]["data"]:
            if data["away_team_id"] == v['team_id']:
                data["away_rank"] = v["rank"]
                data["away_rank_points"] = f'{float(v["adjusted_points"]):.2f}'
            elif data["home_team_id"] == v['team_id']:
                data["home_rank"] = v["rank"]
                data["home_rank_points"] = f'{float(v["adjusted_points"]):.2f}'

        return data

    def extract_data_and_return_combined_data(self, scoreboard, rankings, result=None):

        if result is None:
            result = []

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
                    data = self.combine_rankings_to_scoreboard(event_data, rankings)

                    result.append(data)
        return result

    def main(self):
        status, scoreboard = self.pull_nfl_event_data_from_api(
            const.SCOREBOARD_URL.format
            (
                self.args.get("league", None),
                self.args.get("start_date", None),
                self.args.get("end_date", None),
                config.API_KEY
            )
        )

        if status:
            return scoreboard

        status, rankings = self.pull_nfl_event_data_from_api(
            const.TEAM_RANKINGS_URL.format
            (
                self.args.get("league", None),
                config.API_KEY
            )
        )

        if status:
            return rankings

        result = self.extract_data_and_return_combined_data(scoreboard, rankings)

        return result

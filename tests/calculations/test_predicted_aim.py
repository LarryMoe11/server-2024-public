from calculations import predicted_aim
from unittest.mock import patch
import server
import pytest
from utils import near


class TestPredictedAimCalc:
    def setup_method(self, method):
        with patch("server.Server.ask_calc_all_data", return_value=False):
            self.test_server = server.Server()
        self.test_calc = predicted_aim.PredictedAimCalc(self.test_server)
        self.aims_list = [
            {
                "match_number": 1,
                "alliance_color": "R",
                "team_list": ["1678", "254", "4414"],
            },
            {
                "match_number": 1,
                "alliance_color": "B",
                "team_list": ["125", "1323", "5940"],
            },
            {
                "match_number": 2,
                "alliance_color": "R",
                "team_list": ["1678", "1323", "125"],
            },
            {
                "match_number": 2,
                "alliance_color": "B",
                "team_list": ["254", "4414", "5940"],
            },
            {
                "match_number": 3,
                "alliance_color": "R",
                "team_list": ["1678", "5940", "4414"],
            },
            {
                "match_number": 3,
                "alliance_color": "B",
                "team_list": ["1323", "254", "125"],
            },
        ]
        self.filtered_aims_list = [
            {
                "match_number": 1,
                "alliance_color": "R",
                "team_list": ["1678", "254", "4414"],
            },
            {
                "match_number": 1,
                "alliance_color": "B",
                "team_list": ["125", "1323", "5940"],
            },
            {
                "match_number": 2,
                "alliance_color": "R",
                "team_list": ["1678", "1323", "125"],
            },
            {
                "match_number": 2,
                "alliance_color": "B",
                "team_list": ["254", "4414", "5940"],
            },
            {
                "match_number": 3,
                "alliance_color": "R",
                "team_list": ["1678", "5940", "4414"],
            },
            {
                "match_number": 3,
                "alliance_color": "B",
                "team_list": ["1323", "254", "125"],
            },
        ]
        self.expected_updates = [
            {
                "match_number": 1,
                "alliance_color_is_red": True,
                "has_actual_data": True,
                "actual_score": 320,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.167,
                "actual_rp1": 0.0,
                "actual_rp2": 1.0,
                "won_match": True,
                "predicted_score": 326.05,
                "win_chance": 0.578,
                "team_numbers": ["1678", "254", "4414"],
            },
            {
                "match_number": 1,
                "alliance_color_is_red": False,
                "has_actual_data": True,
                "actual_score": 278,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.056,
                "actual_rp1": 1.0,
                "actual_rp2": 1.0,
                "won_match": False,
                "predicted_score": 314.05,
                "win_chance": 0.42200000000000004,
                "team_numbers": ["125", "1323", "5940"],
            },
            {
                "match_number": 2,
                "alliance_color_is_red": True,
                "has_actual_data": False,
                "actual_score": 0,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.111,
                "actual_rp1": 0.0,
                "actual_rp2": 0.0,
                "won_match": False,
                "predicted_score": 320.65,
                "win_chance": 0.50,
                "team_numbers": ["1678", "1323", "125"],
            },
            {
                "match_number": 2,
                "alliance_color_is_red": False,
                "has_actual_data": False,
                "actual_score": 0,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.111,
                "actual_rp1": 0.0,
                "actual_rp2": 0.0,
                "won_match": False,
                "predicted_score": 319.45,
                "win_chance": 0.5,
                "team_numbers": ["254", "4414", "5940"],
            },
            {
                "match_number": 3,
                "alliance_color_is_red": True,
                "has_actual_data": False,
                "actual_score": 0,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.111,
                "actual_rp1": 0.0,
                "actual_rp2": 0.0,
                "won_match": False,
                "predicted_score": 319.85,
                "win_chance": 0.5,
                "team_numbers": ["1678", "5940", "4414"],
            },
            {
                "match_number": 3,
                "alliance_color_is_red": False,
                "has_actual_data": False,
                "actual_score": 0,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.111,
                "actual_rp1": 0.0,
                "actual_rp2": 0.0,
                "won_match": False,
                "predicted_score": 320.25,
                "win_chance": 0.5,
                "team_numbers": ["1323", "254", "125"],
            },
        ]
        self.expected_playoffs_updates = [
            {
                "alliance_num": 1,
                "picks": ["1678", "254", "4414"],
                "predicted_score": 326.05,
                "predicted_auto_score": 55.8,
                "predicted_tele_score": 267.0,
                "predicted_stage_score": 3.25,
            },
            {
                "alliance_num": 9,
                "picks": ["1678", "254", "4414"],
                "predicted_score": 326.05,
                "predicted_auto_score": 55.8,
                "predicted_tele_score": 267.0,
                "predicted_stage_score": 3.25,
            },
            {
                "alliance_num": 17,
                "picks": ["1678", "254", "4414"],
                "predicted_score": 326.05,
                "predicted_auto_score": 55.8,
                "predicted_tele_score": 267.0,
                "predicted_stage_score": 3.25,
            },
        ]
        self.expected_results = [
            {
                "alliance_color_is_red": False,
                "match_number": 2,
                "actual_rp1": 0.0,
                "actual_rp2": 0.0,
                "actual_score": 0,
                "has_actual_data": False,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.111,
                "predicted_score": 319.45,
                "team_numbers": ["254", "4414", "5940"],
                "win_chance": 0.5,
                "won_match": False,
            },
            {
                "alliance_color_is_red": True,
                "match_number": 1,
                "actual_rp1": 0.0,
                "actual_rp2": 1.0,
                "actual_score": 320,
                "has_actual_data": True,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.167,
                "predicted_score": 326.05,
                "team_numbers": ["1678", "254", "4414"],
                "win_chance": 0.578,
                "won_match": True,
            },
            {
                "alliance_color_is_red": False,
                "match_number": 1,
                "actual_rp1": 1.0,
                "actual_rp2": 1.0,
                "actual_score": 278,
                "has_actual_data": True,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.056,
                "predicted_score": 314.05,
                "team_numbers": ["125", "1323", "5940"],
                "win_chance": 0.42200000000000004,
                "won_match": False,
            },
            {
                "alliance_color_is_red": True,
                "match_number": 2,
                "actual_rp1": 0.0,
                "actual_rp2": 0.0,
                "actual_score": 0,
                "has_actual_data": False,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.111,
                "predicted_score": 320.65,
                "team_numbers": ["1678", "1323", "125"],
                "win_chance": 0.5,
                "won_match": False,
            },
            {
                "alliance_color_is_red": True,
                "match_number": 3,
                "actual_rp1": 0.0,
                "actual_rp2": 0.0,
                "actual_score": 0,
                "has_actual_data": False,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.111,
                "predicted_score": 319.85,
                "team_numbers": ["1678", "5940", "4414"],
                "win_chance": 0.5,
                "won_match": False,
            },
            {
                "alliance_color_is_red": False,
                "match_number": 3,
                "actual_rp1": 0.0,
                "actual_rp2": 0.0,
                "actual_score": 0,
                "has_actual_data": False,
                "predicted_rp1": 0.25,
                "predicted_rp2": 4.111,
                "predicted_score": 320.25,
                "team_numbers": ["1323", "254", "125"],
                "win_chance": 0.5,
                "won_match": False,
            },
        ]
        self.expected_playoffs_alliances = [
            {"alliance_num": 1, "picks": ["1678", "254", "4414"]},
            {"alliance_num": 9, "picks": ["1678", "254", "4414"]},
            {"alliance_num": 17, "picks": ["1678", "254", "4414"]},
        ]
        self.full_predicted_values = predicted_aim.PredictedAimScores(
            park_successes=1.5,
            onstage_successes=0.5,
        )
        self.blank_predicted_values = predicted_aim.PredictedAimScores()
        self.obj_team = [
            {
                "team_number": "1678",
                "matches_played": 5,
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 3,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 17,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 7,
                "onstage_successes": 1,
                "onstage_attempts": 2,
                "park_successes": 0,
                "park_attempts": 0,
                "matches_climb_after": 0,
                "trap_successes": 1,
                "trap_fails": 0,
            },
            {
                "team_number": "254",
                "matches_played": 5,
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 3,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 17,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 7,
                "onstage_successes": 1,
                "onstage_attempts": 2,
                "park_successes": 0,
                "park_attempts": 0,
                "matches_climb_after": 0,
                "trap_successes": 1,
                "trap_fails": 0,
            },
            {
                "team_number": "4414",
                "matches_played": 5,
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 3,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 17,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 7,
                "onstage_successes": 1,
                "onstage_attempts": 2,
                "park_successes": 0,
                "park_attempts": 0,
                "matches_climb_after": 0,
                "trap_successes": 1,
                "trap_fails": 0,
            },
            {
                "team_number": "1323",
                "matches_played": 5,
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 3,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 17,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 7,
                "onstage_successes": 1,
                "onstage_attempts": 2,
                "park_successes": 0,
                "park_attempts": 0,
                "matches_climb_after": 0,
                "trap_successes": 1,
                "trap_fails": 0,
            },
            {
                "team_number": "125",
                "matches_played": 5,
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 2,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 17,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 7,
                "onstage_successes": 1,
                "onstage_attempts": 2,
                "park_successes": 0,
                "park_attempts": 0,
                "matches_climb_after": 0,
                "trap_successes": 1,
                "trap_fails": 0,
            },
            {
                "team_number": "5940",
                "matches_played": 5,
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 2,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 17,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 7,
                "onstage_successes": 1,
                "onstage_attempts": 2,
                "park_successes": 0,
                "park_attempts": 0,
                "matches_climb_after": 0,
                "trap_successes": 1,
                "trap_fails": 0,
            },
        ]
        self.tba_team = [
            {
                "team_number": "1678",
                "leave_successes": 5,
            },
            {
                "team_number": "254",
                "leave_successes": 4,
            },
            {
                "team_number": "4414",
                "leave_successes": 3,
            },
            {
                "team_number": "125",
                "leave_successes": 2,
            },
            {
                "team_number": "5940",
                "leave_successes": 1,
            },
            {
                "team_number": "1323",
                "leave_successes": 4,
            },
        ]
        self.tba_match_data = [
            {
                "match_number": 1,
                "comp_level": "qm",
                "score_breakdown": {
                    "blue": {
                        "melodyBonusAchieved": True,
                        "ensembleBonusAchieved": True,
                        "totalPoints": 278,
                    },
                    "red": {
                        "melodyBonusAchieved": False,
                        "ensembleBonusAchieved": True,
                        "totalPoints": 320,
                    },
                },
                "post_result_time": 182,
                "winning_alliance": "red",
            },
            {
                "match_number": 1,
                "comp_level": "qf",
                "score_breakdown": {
                    "blue": {
                        "melodyBonusAchieved": True,
                        "ensembleBonusAchieved": True,
                        "totalPoints": 300,
                    },
                    "red": {
                        "melodyBonusAchieved": True,
                        "ensembleBonusAchieved": True,
                        "totalPoints": 400,
                    },
                },
                "post_result_time": 182,
                "winning_alliance": "red",
            },
            {
                "match_number": 3,
                "comp_level": "qm",
                "score_breakdown": None,
                "post_result_time": None,
                "winning_alliance": "",
            },
        ]
        self.tba_playoffs_data = [
            {
                "name": "Alliance 1",
                "decines": [],
                "picks": ["frc1678", "frc254", "frc4414"],
                "status": {
                    "playoff_average": None,
                    "level": "f",
                    "record": {"losses": 2, "wins": 6, "ties": 1},
                    "status": "won",
                },
            }
        ]
        self.test_server.db.insert_documents("obj_team", self.obj_team)
        self.test_server.db.insert_documents("tba_team", self.tba_team)

    def test___init__(self):
        """Test if attributes are set correctly"""
        assert self.test_calc.watched_collections == ["obj_team", "tba_team"]
        assert self.test_calc.server == self.test_server

    def test_calc_alliance_score(self):
        """Test the total predicted_score is correct"""
        assert near(
            self.test_calc.calc_alliance_score(
                self.blank_predicted_values,
                self.obj_team,
                self.tba_team,
                ["1678", "254", "4414"],
            ),
            326.05,
        )
        # Make sure there are no errors with empty data
        try:
            self.test_calc.calc_alliance_score(
                self.blank_predicted_values,
                self.obj_team,
                self.tba_team,
                ["1000", "1000", "1000"],
            )
        except ZeroDivisionError as exc:
            assert False, f"calculate_predicted_alliance_score has a {exc}"

    def test_get_playoffs_alliances(self):
        # TODO: need more tests for this, might break
        with patch(
            "data_transfer.tba_communicator.tba_request", return_value=self.tba_playoffs_data
        ):
            assert self.test_calc.get_playoffs_alliances() == self.expected_playoffs_alliances

    def test_calculate_predicted_ensemble_rp(self):
        obj_teams = [
            {
                "team_number": "1678",
                "onstage_successes": 5,
                "onstage_attempts": 6,
                "park_successes": 0,
                "park_attempts": 0,
                "matches_climb_after": 1,
                "trap_successes": 5,
                "trap_fails": 0,
            },
            {
                "team_number": "254",
                "onstage_successes": 1,
                "onstage_attempts": 2,
                "park_successes": 0,
                "park_attempts": 0,
                "matches_climb_after": 0,
                "trap_successes": 1,
                "trap_fails": 0,
            },
            {
                "team_number": "4414",
                "onstage_successes": 6,
                "onstage_attempts": 7,
                "park_successes": 0,
                "park_attempts": 0,
                "matches_climb_after": 4,
                "trap_successes": 3,
                "trap_fails": 0,
            },
        ]
        assert self.test_calc.calc_ensemble_rp(obj_teams, ["1678", "254", "4414"]) == 0.714

    def test_calculate_predicted_melody_rp(self):
        sample_predicted_values = self.blank_predicted_values
        sample_predicted_values.auto_amp = 2
        sample_predicted_values.tele_speaker = 12
        assert self.test_calc.calc_melody_rp(sample_predicted_values) == 0.778

        sample_predicted_values.tele_speaker_amped = 6
        assert self.test_calc.calc_melody_rp(sample_predicted_values) == 1.111

    def test_get_actual_values(self):
        """Test getting actual values from TBA"""
        assert self.test_calc.get_actual_values(
            {
                "match_number": 1,
                "alliance_color": "R",
                "team_list": ["1678", "1533", "7229"],
            },
            self.tba_match_data,
        ) == {
            "has_actual_data": True,
            "actual_score": 320,
            "actual_rp1": 0.0,
            "actual_rp2": 1.0,
            "won_match": True,
        }
        assert self.test_calc.get_actual_values(
            {
                "match_number": 1,
                "alliance_color": "B",
                "team_list": ["1678", "1533", "2468"],
            },
            self.tba_match_data,
        ) == {
            "has_actual_data": True,
            "actual_score": 278,
            "actual_rp1": 1.0,
            "actual_rp2": 1.0,
            "won_match": False,
        }
        assert self.test_calc.get_actual_values(
            {
                "match_number": 3,
                "alliance_color": "B",
                "team_list": ["1678", "1533", "7229"],
            },
            self.tba_match_data,
        ) == {
            "has_actual_data": False,
            "actual_score": 0,
            "actual_rp1": 0.0,
            "actual_rp2": 0.0,
            "won_match": False,
        }
        assert self.test_calc.get_actual_values(
            {
                "match_number": 3,
                "alliance_color": "R",
                "team_list": ["1678", "1533", "2468"],
            },
            self.tba_match_data,
        ) == {
            "has_actual_data": False,
            "actual_score": 0,
            "actual_rp1": 0.0,
            "actual_rp2": 0.0,
            "won_match": False,
        }

    def test_filter_aims_list(self):
        assert (
            self.test_calc.filter_aims_list(self.obj_team, self.tba_team, self.aims_list)
            == self.filtered_aims_list
        )

    def test_update_predicted_aim(self):
        self.test_server.db.delete_data("predicted_aim")
        with patch(
            "data_transfer.tba_communicator.tba_request",
            return_value=self.tba_match_data,
        ):
            assert self.test_calc.update_predicted_aim(self.aims_list) == self.expected_updates

    def test_update_playoffs_alliances(self):
        """Test that we correctly calculate data for each of the playoff alliances"""
        self.test_server.db.delete_data("predicted_aim")
        with patch(
            "calculations.predicted_aim.PredictedAimCalc.get_playoffs_alliances",
            return_value=self.expected_playoffs_alliances,
        ):
            playoff_update = self.test_calc.update_playoffs_alliances()

        assert playoff_update == self.expected_playoffs_updates

    def test_calc_win_chance(self):
        obj_teams1 = [
            {
                "team_number": "1678",
                "auto_avg_amp": 0,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 6,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 1,
                "tele_sd_speaker": 1,
                "tele_avg_speaker_amped": 15,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 6,
            },
            {
                "team_number": "254",
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 6,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 17,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 7,
            },
            {
                "team_number": "4414",
                "auto_avg_amp": 0,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 7,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 6,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 1,
                "tele_sd_speaker": 1,
                "tele_avg_speaker_amped": 20,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 6,
            },
            {
                "team_number": "125",
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 4,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 16,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 8,
            },
            {
                "team_number": "126",
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 4,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 16,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 8,
            },
            {
                "team_number": "127",
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 4,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 16,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 8,
            },
        ]
        obj_teams2 = [
            {
                "team_number": "125",
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 4,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 16,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 8,
            },
            {
                "team_number": "126",
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 4,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 16,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 8,
            },
            {
                "team_number": "127",
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 4,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 16,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 8,
            },
            {
                "team_number": "225",
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 4,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 16,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 8,
            },
            {
                "team_number": "226",
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 4,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 16,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 8,
            },
            {
                "team_number": "227",
                "auto_avg_amp": 1,
                "auto_sd_amp": 0,
                "auto_avg_speaker": 4,
                "auto_sd_speaker": 1,
                "tele_avg_amp": 4,
                "tele_sd_amp": 2,
                "tele_avg_speaker": 0,
                "tele_sd_speaker": 0,
                "tele_avg_speaker_amped": 16,
                "tele_sd_speaker_amped": 4,
                "avg_endgame_points": 8,
            },
        ]

        assert (
            self.test_calc.calc_win_chance(
                obj_teams1, {"R": ["1678", "254", "4414"], "B": ["125", "126", "127"]}, "R"
            )
            == 0.847
        )
        assert (
            self.test_calc.calc_win_chance(
                obj_teams2, {"R": ["225", "226", "227"], "B": ["125", "126", "127"]}, "R"
            )
            == 0.5
        )

    def test_run(self):
        self.test_server.db.delete_data("obj_team")
        self.test_server.db.delete_data("tba_team")
        self.test_server.db.delete_data("predicted_aim")
        self.test_server.db.insert_documents("obj_team", self.obj_team)
        self.test_server.db.insert_documents("tba_team", self.tba_team)

        with patch(
            "calculations.predicted_aim.PredictedAimCalc.get_aim_list",
            return_value=self.aims_list,
        ), patch(
            "data_transfer.tba_communicator.tba_request",
            side_effect=[self.tba_match_data, self.tba_playoffs_data],
        ):
            self.test_calc.run()

        result = self.test_server.db.find("predicted_aim")
        assert len(result) == 6

        for ind, document in enumerate(result):
            del document["_id"]
            assert document in self.expected_results

        result2 = self.test_server.db.find("predicted_alliances")
        assert len(result2) == 3

        for document in result2:
            del document["_id"]
            assert document in self.expected_playoffs_updates

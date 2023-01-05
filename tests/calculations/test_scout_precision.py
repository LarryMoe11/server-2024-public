from unittest.mock import patch

from calculations import scout_precision
import server


class TestScoutPrecisionCalc:
    def setup_method(self):
        self.tba_test_data = [
            {
                "match_number": 1,
                "actual_time": 1100291640,
                "comp_level": "qm",
                "score_breakdown": {
                    "blue": {
                        "foulPoints": 8,
                        "autoTaxiPoints": 15,
                        "totalPoints": 278,
                        "endgamePoints": 6,
                    },
                    "red": {
                        "foulPoints": 10,
                        "autoTaxiPoints": 0,
                        "totalPoints": 130,
                        "endgamePoints": 15,
                    },
                },
            },
            {
                "match_number": 2,
                "actual_time": 1087511040,
                "comp_level": "qm",
                "score_breakdown": {
                    "blue": {
                        "foulPoints": 0,
                        "autoTaxiPoints": 0,
                        "totalPoints": 100,
                        "endgamePoints": 25,
                    },
                    "red": {
                        "foulPoints": 10,
                        "autoTaxiPoints": 0,
                        "totalPoints": 130,
                        "endgamePoints": 4,
                    },
                },
            },
            {
                "match_number": 3,
                "actual_time": None,
                "comp_level": "qm",
                "score_breakdown": None,
            },
        ]
        self.scout_tim_test_data = [
            # Match 1
            {
                "scout_name": "ALISON LIN",
                "team_number": "1678",
                "match_number": 1,
                "alliance_color_is_red": True,
                "auto_high_balls": 5,
                "auto_low_balls": 0,
                "tele_high_balls": 9,
                "tele_low_balls": 2,
            },
            {
                "scout_name": "NATHAN MILLS",
                "team_number": "1678",
                "match_number": 1,
                "alliance_color_is_red": True,
                "auto_high_balls": 4,
                "auto_low_balls": 0,
                "tele_high_balls": 10,
                "tele_low_balls": 2,
            },
            {
                "scout_name": "KATHY LI",
                "team_number": "4414",
                "match_number": 1,
                "alliance_color_is_red": True,
                "auto_high_balls": 3,
                "auto_low_balls": 1,
                "tele_high_balls": 8,
                "tele_low_balls": 4,
            },
            {
                "scout_name": "KATE UNGER",
                "team_number": "589",
                "match_number": 1,
                "alliance_color_is_red": True,
                "auto_high_balls": 0,
                "auto_low_balls": 0,
                "tele_high_balls": 1,
                "tele_low_balls": 2,
            },
            {
                "scout_name": "NITHMI JAYASUNDARA",
                "team_number": "589",
                "match_number": 1,
                "alliance_color_is_red": True,
                "auto_high_balls": 0,
                "auto_low_balls": 0,
                "tele_high_balls": 2,
                "tele_low_balls": 2,
            },
            {
                "scout_name": "RAY FABIONAR",
                "team_number": "589",
                "match_number": 1,
                "alliance_color_is_red": True,
                "auto_high_balls": 0,
                "auto_low_balls": 0,
                "tele_high_balls": 0,
                "tele_low_balls": 3,
            },
            # Match 2
            {
                "scout_name": "NATHAN MILLS",
                "team_number": "1678",
                "match_number": 2,
                "alliance_color_is_red": False,
                "auto_high_balls": 3,
                "auto_low_balls": 0,
                "tele_high_balls": 14,
                "tele_low_balls": 0,
            },
            {
                "scout_name": "KATHY LI",
                "team_number": "4414",
                "match_number": 2,
                "alliance_color_is_red": False,
                "auto_high_balls": 4,
                "auto_low_balls": 1,
                "tele_high_balls": 8,
                "tele_low_balls": 3,
            },
            {
                "scout_name": "KATE UNGER",
                "team_number": "589",
                "match_number": 2,
                "alliance_color_is_red": False,
                "auto_high_balls": 0,
                "auto_low_balls": 0,
                "tele_high_balls": 1,
                "tele_low_balls": 2,
            },
        ]

        with patch("server.Server.ask_calc_all_data", return_value=False):
            self.test_server = server.Server()
        self.test_calc = scout_precision.ScoutPrecisionCalc(self.test_server)

    def test___init__(self):
        assert self.test_calc.watched_collections == ["unconsolidated_totals"]
        assert self.test_calc.server == self.test_server

    def test_find_updated_scouts(self):
        self.test_server.db.delete_data("unconsolidated_totals")
        self.test_calc.update_timestamp()
        self.test_server.db.insert_documents(
            "unconsolidated_totals",
            [{"scout_name": "REED WANG", "other": 9}, {"scout_name": "NATHAN MILLS"}],
        )
        assert sorted(self.test_calc.find_updated_scouts()) == sorted(["REED WANG", "NATHAN MILLS"])
        self.test_calc.update_timestamp()
        self.test_server.db.update_document(
            "unconsolidated_totals", {"other": 1}, {"scout_name": "NATHAN MILLS"}
        )
        assert self.test_calc.find_updated_scouts() == ["NATHAN MILLS"]

    def test_calc_scout_precision(self):
        assert self.test_calc.calc_scout_precision([{"scout_name": "REED WANG"}]) == {}
        test_data = [
            {"scout_name": "KATHY LI", "sim_precision": 0.5, "match_number": 1},
            {"scout_name": "KATHY LI", "sim_precision": 0, "match_number": 2},
            {"scout_name": "KATHY LI", "sim_precision": -1, "match_number": 3},
            {"scout_name": "KATHY LI", "sim_precision": 0.7243, "match_number": 4},
            {"scout_name": "KATHY LI", "sim_precision": 5, "match_number": 5},
        ]
        assert self.test_calc.calc_scout_precision(test_data) == {
            "scout_precision": 1.0448600000000001
        }

    def test_update_scout_precision_calcs(self):
        with patch(
            "calculations.scout_precision.ScoutPrecisionCalc.calc_scout_precision",
            return_value={"scout_precision": 0.39},
        ):
            assert self.test_calc.update_scout_precision_calcs(["REED WANG"]) == [
                {"scout_name": "REED WANG", "scout_precision": 0.39}
            ]

    def test_run(self):

        expected_scout_precision = [
            {"scout_name": "ALISON LIN", "scout_precision": 8.222222222222221},
            {"scout_name": "NATHAN MILLS", "scout_precision": 4.111111111111111},
            {"scout_name": "KATHY LI", "scout_precision": 3.61111111111111},
            {"scout_name": "KATE UNGER", "scout_precision": 3.7777777777777777},
            {"scout_name": "NITHMI JAYASUNDARA", "scout_precision": 7.555555555555555},
            {"scout_name": "RAY FABIONAR", "scout_precision": 10.555555555555555},
        ]
        self.test_server.db.delete_data("unconsolidated_totals")
        self.test_calc.update_timestamp()
        self.test_server.db.insert_documents("unconsolidated_totals", self.scout_tim_test_data)
        with patch(
            "data_transfer.tba_communicator.tba_request",
            return_value=self.tba_test_data,
        ):
            self.test_calc.run()
        scout_precision_result = self.test_server.db.find("sim_precision")
        for document in scout_precision_result:
            document.pop("_id")
            assert document in expected_scout_precision

import unittest
import os
import json
import app
class StubHamburgRailExchangeScheduler(app.HamburgRailExchangeScheduler):
    def get_city_data(self):
        file_path = os.path.dirname(os.path.realpath(__file__))
        os.chdir(file_path)
        os.chdir("../data")
        folder_content = os.listdir()
        cities_data = {}
        for file in folder_content:
            city = file.split(".")[0]
            with open(file) as city_data:
                cities_data[city] = json.load(city_data)
        return cities_data
class SchedulerTest(unittest.TestCase):
    def setUp(self):
        self.exchange = StubHamburgRailExchangeScheduler()
    def test_schedule_train_from_leipzig_at_night(self):
        # Schedule a train from Leipzig at 23:51.
        departure_time, arrival_time = self.exchange.schedule_train_from_hamburg(
            "leipzig", "23:51")
        # Assert that the real departure time is after 00 hours (due to the above-mentioned 15 minute minimum allowed break between trains).
        self.assertGreater(arrival_time, "00:00")
    def test_city_data_present(self):
        # Assert that the city data for all five cities is present.
        for city in ["berlin", "bremen", "kiel", "leipzig", "munich"]:
            self.assertIn(city, self.exchange.city_data)
            self.assertIsNotNone(self.exchange.city_data[city])
    def test_run(self):
        self.exchange.schedule_train_to_hamburg("bremen", "01:11")
if __name__ == "__main__":
    unittest.main()

# ❯❯ src git:(main)  13:19 python3 -m unittest -v
# test_city_data_present (test_app.SchedulerTest.test_city_data_present) ... ok
# test_run (test_app.SchedulerTest.test_run) ... WARNING! Sending message to exchange in bremen.
# ok
# test_schedule_train_from_leipzig_at_night (test_app.SchedulerTest.test_schedule_train_from_leipzig_at_night) ... WARNING! Sending message to exchange in leipzig.
# ok

# ----------------------------------------------------------------------
# Ran 3 tests in 0.001s

# OK
#!/usr/bin/env python
import urllib.request
import json

from tools import time_to_minutes, minutes_to_time

EXTERNAL_URL = "http://localhost:7000/data/"


class HamburgRailExchangeScheduler:
    def __init__(self):
        self.city_data = self.get_city_data()

    def get_city_data(self):
        """Download data from other cities. WARNING: This method makes an external API call!"""
        data = {}
        for city in ["berlin", "bremen", "kiel", "leipzig", "munich"]:
            print(f"WARNING! Downloading data for {city}.")
            with urllib.request.urlopen(f"{EXTERNAL_URL}{city}.json") as f:
                data[city] = json.loads(f.read().decode("utf-8"))
        return data

    def notify_city(self, city, message):
        """Send message about change to another city. WARNING: This method makes an external API call!"""
        print(f"WARNING! Sending message to exchange in {city}.")
        urllib.request.Request(f"{EXTERNAL_URL}{city}/", data=json.dumps(message))

    def schedule_train_to_hamburg(self, city: str, desired_time: str):
        """
        Schedule a train to Hamburg around desired time. Make sure that no other train leaves to Hamburg
        within 15 minutes of this time, otherwise move the time.
        """
        scheduled_minutes = time_to_minutes(desired_time)
        time_found = False
        while not time_found:
            for time in self.city_data[city]["trains_to_hamburg"]:
                minutes = time_to_minutes(time)
                delta = minutes - scheduled_minutes
                if delta < 15 and delta > -15:
                    if delta < 0:
                        scheduled_minutes = minutes + 15
                    else:
                        scheduled_minutes = minutes - 15
                    if scheduled_minutes > 1439:
                        scheduled_minutes -= 1440
                    elif scheduled_minutes < 0:
                        scheduled_minutes += 1440
                    continue
            time_found = True
        departure_time = minutes_to_time(scheduled_minutes)
        self.notify_city(city, {"new_train_to_hamburg": departure_time})
        self.city_data[city]["trains_to_hamburg"].append(departure_time)
        arrival_minutes = scheduled_minutes + self.city_data[city]["minutes_to_hamburg"]
        if arrival_minutes > 1440:
            arrival_minutes -= 1440
        arrival_time = minutes_to_time(arrival_minutes)
        return (departure_time, arrival_time)

    def schedule_train_from_hamburg(self, city: str, desired_time: str):
        """
        Schedule a train from Hamburg around desired time. Make sure that no train leaves to Hamburg
        from that same city at the same time as that will confuse passengers. Move the train 1 minute
        into the future if that should happen.
        """
        scheduled_minutes = time_to_minutes(desired_time)
        time_found = False
        while not time_found:
            for time in self.city_data[city]["trains_to_hamburg"]:
                minutes = time_to_minutes(time)
                delta = minutes - scheduled_minutes
                if delta == 0:
                    scheduled_minutes += 1
                    if scheduled_minutes > 1439:
                        scheduled_minutes -= 1440
                    continue
            time_found = True
        departure_time = minutes_to_time(scheduled_minutes)
        arrival_minutes = scheduled_minutes + self.city_data[city]["minutes_to_hamburg"]
        if arrival_minutes > 1440:
            arrival_minutes -= 1440
        arrival_time = minutes_to_time(arrival_minutes)
        self.notify_city(city, {"new_train_from_hamburg": arrival_time})
        return (departure_time, arrival_time)


if __name__ == "__main__":
    exchange = HamburgRailExchangeScheduler()

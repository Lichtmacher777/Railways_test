# Python-testing-stub

In this exercise, you will be working with testing a class by stubbing out calls to external data.

You are working at the German Railways company. The railway company is ready to launch a new railway interchange
in Hamburg. The code has been written and everyone thinks is ready. The president of the company is on his way
to Hamburg in an express ICE train to cut the ribbon this afternoon for what will be Hamburg's largest
infrastructure upgrade in 40 years.

While browsing through the code that controls the interchange one last time, you suddenly realize that you forgot
to add test! And there is a problem with writing tests now: part of the code makes API calls to other exchanges
in other cities. If your tests cause these calls to be made, you might crash all railway traffic in cities like
Kiel, Berlin or Munich!

You therefore need to prevent those functions that make these API calls for the tests from running for your test suite.

-------

**What do you need to do:**

* Within `src/test_app.py` create an instance of `HamburgRailExchangeScheduler` that does not make API calls for getting or posting data. Do **NOT** modify the file `src/app.py` to achieve this.
* You can replace the `HamburgRailExchangeScheduler.get_city_data` method with one that reads the data from the files in the `data` directory.
* Write a test to try to schedule a train to Bremen at 15:33. Test that the departure time will be 15:34  and the arrival time 16:30.
* Write a test trying to schedule 4 trains from Bremen at 16:15. Test that the scheduler does not schedule all the trains at the same time and that the departure time is at least 15 minutes from other departures on the same route.
* Write a test trying to schedule a train from Leipzig at 23:51, testing that the real departure time is after 00 hours (due to the above-mentioned 15 minute minimum allowed break between trains).
* Write a test ensuring that the city data for all five cities is present.

# from abc import ABC, abstractmethod
import argparse
import pandas as pd
# import time
import sched
from datetime import datetime, timedelta
# from collections import defaultdict
import requests

class Website:
    def __init__(self, url, interval):
        self.url = url
        self.interval = interval
        self.data = pd.DataFrame(columns=['code','elapsed'])
        self.is_being_tracked = False
        return
    
    # We need alerter object here because each ping is a timestep in our application
    # and at each timestep we need to go through our monitored alerts
    def start_pinging(self, scheduler, alerter):
        """
        Method to ping and reschedule next ping of self.website based on self.interval

        :param alerter: Alerter object, because we need it to check alerts on each ping 
        """
        self.is_being_tracked = True
        # At each ping we are on a specific timestamp ( used for indexing )
        ts = pd.Timestamp(datetime.now())
        print("f(x) start_pinging")
        print("pinging.. ", self.url)
        try:
            response = requests.get(self.url, timeout=5)
            row = pd.DataFrame([[response.status_code, response.elapsed]], index=[ts], columns=['code','elapsed'])
            print(f"ts {ts}, url {self.url}, code {response.status_code}, elapsed {response.elapsed}")
        except:
            #TODO: change -1,None so that it doesn't look the same as others code
            row = pd.DataFrame([[-1, None]], index=[ts], columns=['code','elapsed'])
        self.data = self.data.append(row)
        print("\tdf: ", self.data)

        print(f"ts: {ts} for {self.url} next in {self.interval}")
        print()
        # schedule before we check all alerts
        scheduler.enter(self.interval, 1, self.start_pinging, argument=(scheduler, alerter))
        # Only if there are alerts to be tracked on this website check them, check_alerts
        if self.url in alerter.alerts:
            alerter.check_alerts(self.url,ts) # check alerts based on current_ts
        return


if __name__ == "__main__":
    pass
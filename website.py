# from abc import ABC, abstractmethod
import pandas as pd
import numpy as np
# import time
import sched
from datetime import datetime
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

        :param scheduler : Scheduler used to reschedule the next ping
        :param alerter   : Alerter used to check if any alerts need to be raised
        """
        self.is_being_tracked = True
        # At each ping we are on a specific timestamp ( used for indexing )
        ts = pd.Timestamp(datetime.now())
        # print("f(x) start_pinging")
        # print("pinging.. ", self.url)
        try:
            response = requests.get(self.url, timeout=5)
            row = pd.DataFrame([[response.status_code, response.elapsed]], index=[ts], columns=['code','elapsed'])
            # print(f"ts {ts}, url {self.url}, code {response.status_code}, elapsed {response.elapsed}")
        except:
            #TODO: Test that np.NaN works as intended
            row = pd.DataFrame([[np.NaN, np.NaN]], index=[ts], columns=['code','elapsed'])
        self.data = self.data.append(row)
        # reschedule next ping
        scheduler.enter(self.interval, 1, self.start_pinging, argument=(scheduler, alerter))

        # print("\tdf: ", self.data)
        #TODO: Remove below just for testing
        # self.data.to_pickle(f"./df_{self.url[8:]}.pkl")


        # print(f"ts: {ts} for {self.url} next in {self.interval}")
        # Check if alerts need to be raised
        if self.url in alerter.alerts:
            alerter.check_alerts(self.url, ts) 
        return

    def __str__(self):
        return self.url

if __name__ == "__main__":
    pass
import pandas as pd
import numpy as np
import sched
from datetime import datetime
import requests


class Website:
    """Website object keeping track of relevant intervals and data"""

    def __init__(self, url, interval):
        self.url = url
        self.interval = interval
        self.data = pd.DataFrame(columns=["code", "elapsed"])
        self.is_being_tracked = False
        return

    def start_pinging(self, scheduler, alerter):
        """
        Method used to (1) ping and (2) reschedule the next ping and (3) check if any alerts need to be send.


        :param scheduler : Scheduler used to reschedule the next ping
        :param alerter   : Alerter used to check if any alerts need o be raised
        """
        self.is_being_tracked = True
        ts = pd.Timestamp(datetime.now())
        try:
            response = requests.get(self.url, timeout=3)
            row = pd.DataFrame(
                [[response.status_code, response.elapsed]],
                index=[ts],
                columns=["code", "elapsed"],
            )
        except:
            # network error can be identified by missing status code and elapsed
            row = pd.DataFrame(
                [[np.NaN, np.NaN]], index=[ts], columns=["code", "elapsed"]
            )
        self.data = self.data.append(row)
        scheduler.enter(
            self.interval, 1, self.start_pinging, argument=(scheduler, alerter)
        )
        if self.url in alerter.alerts:
            alerter.check_alerts(self.url, ts)
        return

    def __str__(self):
        return self.url


if __name__ == "__main__":
    pass

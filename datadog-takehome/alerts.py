# from abc import ABC, abstractmethod
# import argparse
# import pandas as pd
# import time
# import sched
from datetime import timedelta
from collections import defaultdict
# import requests

class Alerter:

    def __init__(self, websites):
        self.site_idx = websites #url: Website object
        self.alerts = defaultdict(list) # dick me key " urls " : alerts sto sugkekrimeno url
        return

    #TODO: change this
    def __str__(self):
        return f"{self.alerts.items()}, \nAlerter sites: {self.site_idx}"

    def track(self, alert):
        """ 
        Start tracking a specific alert 
        
        :param alert : Alert object
        """
        self.alerts[alert.url].append(alert)
        return

    def check_alerts(self, url, ts):
        """ 
        Check alerts of website up to timestamp

        :param url : website's url, used to find alerts specific to that website
        :param ts  : current timestamp
        """
        print("f(x) check_alerts")
        if url in self.alerts:
            [alert.check_threshold(data=self.site_idx[url].data, ts=ts) for alert in self.alerts[url]]
        #TODO: Des otan exeis xrono an to website_obj me to site_idx na einai mesa sto Alert
                # Nomize einai alla double check
        #TODO: oxi to data slicing mesa ston Alerter, thelw mesa sta metrics na ginetai
        return

class Alert:
    def __init__(self, url, severity, metric, aggr_interval, threshold, threshold_type, message_upper, message_lower):
        self.url = url
        self.severity = severity
        #TODO: Prepei na perasw metric object se kathe alert?
        self.metric_name = metric # pros to paron einai metric name
        # Aggregation interval for specific alerts != reporting interval of specific stats
        self.aggr_interval = aggr_interval 
        self.threshold = threshold
        self.threshold_type = threshold_type
        self.message_upper = message_upper
        self.message_lower = message_lower
        self.has_crossed_threshold = False

    def __str__(self):
        return f"ALERT: {self.url}, {self.severity}, {self.metric_name}, {self.aggr_interval}, {self.threshold}, {self.threshold_type}, {self.message_upper}, {self.message_lower}\n"


    #TODO: To data den prepei na ginetai edw mesa
    def check_threshold(self, data, ts):
        """ 
        :param data: pandas DataFram with index the ts. so we need to get the data only for the interval we care about
        :param ts: is current timestamp
        """
        #TODO: Where do I get the val from? (some global dataframe that keeps track of ts,statuscode,elapsed)
        current_data_slice = data.loc[ts-timedelta(seconds=self.aggr_interval):ts]
#TODO: TEST IF THIS IS CORRECT
        
        #TODO: Create metric value based on correct slice of data
        # isws to data_slice prepei na to kanei calculate to metric internally tha doume
        # kai na tou pernaw 3erw gw to website_object apo to opoio to kanei calculate

        metric = self.metric_name
#TODO: We want AGGREGATE TO COMPUT current_data_slice not here 
        
        #TODO: REMOVE THESE SO THAT THE FUNCTIONS RUNS
        print("f(x) check_threshold")
        print("check_threshold of ", self.url, self.metric_name)
        return

        metric_value = self.metric.aggregate(ts=ts)

        # we use .has_crossed_threshold to define "danger zone" above or below threshold and "safe zone" on the other side
        # when in danger zone we want to keep warning
        # when in safe zone we want to say that we have recovered
        if metric_value < self.threshold:
            if self.threshold_type == "upper" and self.has_crossed_threshold:
                # print once that we recovered
                _send_alert(self.message_lower, metric_value, ts)
                self.has_crossed_threshold = False 
            if self.threshold_type == "lower":
                # sunexeia prints
                # WARNING always
                _send_alert(self.message_lower, metric_value, ts)
                self.has_crossed_threshold = True
        elif metric_value > self.threshold:
            if self.threshold_type == "lower" and self.has_crossed_threshold:
                # print once that we recovered
                _send_alert(self.message_upper, metric_value, ts)
                self.has_crossed_threshold = False 
            if self.threshold_type == "upper":
                # sunexeia prints
                # WARNING always
                _send_alert(self.message_upper, metric_value, ts)
                self.has_crossed_threshold = True
                # tsekareis an prin itan 
             

    def _send_alert(self, message, metric_value, ts):
        #TODO: logging levels WARNING DEBUG kai mlkies?
        print(f"{message} " + f"{self.metric_name}= {str(metric_value)}, time={str(ts)}")
        if self.severity == 1:
            pass
        if self.severity == 2:
            pass
        if self.severity == 3:
            pass
        if self.severity == 4:
            pass
        if self.severity == 5:
            pass
        return
        
    
        #TODO: Add some save here gia historical reasons opws lene oi idioi?
        return
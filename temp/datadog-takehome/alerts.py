from datetime import timedelta
from collections import defaultdict

class Alerter:

    def __init__(self, websites):
        # dick me key " urls " : alerts sto sugkekrimeno url
        self.alerts = defaultdict(list) 
        return

    #TODO: change this
    def __str__(self):
        return f"{self.alerts.items()}"

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
            [alert.check_threshold(ts) for alert in self.alerts[url]]
        return

class Alert:
    def __init__(self, url, severity, metric, aggr_interval, threshold, threshold_type, message_upper, message_lower):
        self.url = url
        self.severity = severity
        #TODO: Prepei na perasw metric object se kathe alert?
        self.metric = metric # pros to paron einai metric name
        # Aggregation interval for specific alerts != reporting interval of specific stats
        self.aggr_interval = aggr_interval 
        self.threshold = threshold
        self.threshold_type = threshold_type
        self.message_upper = message_upper
        self.message_lower = message_lower
        self.has_crossed_threshold = False

    def __str__(self):
        return f"ALERT: {self.url}, {self.severity}, {self.metric}, {self.aggr_interval}, {self.threshold}, {self.threshold_type}, {self.message_upper}, {self.message_lower}\n"


    #TODO: To data den prepei na ginetai edw mesa
    def check_threshold(self, ts):
        """ 
        :param data: pandas DataFram with index the ts. so we need to get the data only for the interval we care about
        :param ts: is current timestamp
        """
        #TODO: Check if these are done correctly
        metric_value = self.metric.aggregate(self.url, self.aggr_interval, ts)

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
        print(f"{message} " + f"{self.metric}= {str(metric_value)}, time={str(ts)}")
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
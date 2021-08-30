from datetime import timedelta
from collections import defaultdict
import logging
from logging_formatter import CustomLoggingFormatter

# Run this code on import, don't add "if __name__"
# create logger
logger = logging.getLogger('alerter')
logger.setLevel(logging.DEBUG)
# create console handler
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomLoggingFormatter())
logger.addHandler(ch)

class Alerter:

    def __init__(self):
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
        if url in self.alerts:
            [alert.check_threshold(ts) for alert in self.alerts[url]]
        return

class Alert:
    def __init__(self, url, severity, metric, aggr_interval, threshold, threshold_type, message_upper, message_lower):
        self.url = url
        self.severity = severity
        self.metric = metric
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
        # we use .has_crossed_threshold to define "danger zone" above or below threshold and "safe zone" on the other side
        # when in danger zone we want to keep warning
        # when in safe zone we want to say that we have recovered
        
        
        :param data: pandas DataFram with index the ts. so we need to get the data only for the interval we care about
        :param ts: is current timestamp
        """
        #TODO: Check if these are done correctly
        metric_value = self.metric.aggregate(self.url, self.aggr_interval, ts)
        
        if metric_value < self.threshold:
            if self.threshold_type == "upper" and self.has_crossed_threshold:
                # print once that we recovered
                self.has_crossed_threshold = False 
                self._send_alert(self.message_lower, metric_value, ts)
            elif self.threshold_type == "lower":
                # sunexeia prints
                # WARNING always
                self.has_crossed_threshold = True
                self._send_alert(self.message_lower, metric_value, ts)
        elif metric_value > self.threshold:
            if self.threshold_type == "lower" and self.has_crossed_threshold:
                # print once that we recovered
                self.has_crossed_threshold = False 
                self._send_alert(self.message_upper, metric_value, ts)
            elif self.threshold_type == "upper":
                # sunexeia prints
                self.has_crossed_threshold = True
                self._send_alert(self.message_upper, metric_value, ts)
             
    def _send_alert(self, message, metric_value, ts):
        """
        Sends alert through logger on appropriate level based on alert severity
        """
        if self.severity == 1:
            logger.debug(f"{message} {self.metric.name}={metric_value}, time={str(ts)}")
        if self.severity == 2:
            logger.info(f"{message} {self.metric.name}={metric_value}, time={str(ts)}")
        if self.severity == 3:
            logger.warning(f"{message} {self.metric.name}={metric_value}, time={str(ts)}")
        if self.severity == 4:
            logger.error(f"{message} {self.metric.name}={metric_value}, time={str(ts)}")
        if self.severity == 5:
            logger.critical(f"{message} {self.metric.name}={metric_value}, time={str(ts)}")
        return
        


# general python
from datetime import timedelta
from collections import defaultdict
import logging

# my classes
from logging_formatter import CustomLoggingFormatter

# Run this code on import, don't add "if __name__"
logger = logging.getLogger("alerter")
logger.setLevel(logging.DEBUG)
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)
ch.setFormatter(CustomLoggingFormatter())
logger.addHandler(ch)


class Alerter:
    """
    Alerter object used to track and check all different alerts.
    """

    def __init__(self):
        self.alerts = defaultdict(list)
        return

    def __str__(self):
        return f"{self.alerts.items()}"

    def track(self, alert):
        """
        Start tracking a specific alert.

        :param alert : Alert object
        """
        self.alerts[alert.url].append(alert)
        return

    def check_alerts(self, url, ts):
        """
        Check alerts of specific website up timestamp ts.

        :param url : website's url, used to find alerts specific to that website
        :param ts  : current timestamp
        """
        if url in self.alerts:
            [alert.check_threshold(ts) for alert in self.alerts[url]]
        return


class Alert:
    """
    Threshold Alert object, used to check if a specific metric on a website has crossed
    over specified threshold.
    """

    def __init__(
        self,
        url,
        severity,
        metric,
        aggr_interval,
        threshold,
        threshold_type,
        message_upper,
        message_lower,
    ):
        self.url = url
        self.severity = severity
        self.metric = metric
        self.aggr_interval = aggr_interval
        self.threshold = threshold
        self.threshold_type = threshold_type
        self.message_upper = message_upper
        self.message_lower = message_lower
        # .has_crossed_threshold defines "danger zone" and "safe zone"
        # when in danger zone we want to keep alerting the user
        # when returning to safe zone we want to alert once
        self.has_crossed_threshold = False

    def check_threshold(self, ts):
        """
        Check if current alert being tracked has crossed over specified threshold.

        :param ts: is current timestamp
        """
        metric_value = self.metric.aggregate(self.url, self.aggr_interval, ts)

        if metric_value < self.threshold:
            if self.threshold_type == "upper" and self.has_crossed_threshold:
                self.has_crossed_threshold = False
                self._send_alert(self.message_lower, metric_value, ts)
            elif self.threshold_type == "lower":
                self.has_crossed_threshold = True
                self._send_alert(self.message_lower, metric_value, ts)
        elif metric_value > self.threshold:
            if self.threshold_type == "lower" and self.has_crossed_threshold:
                self.has_crossed_threshold = False
                self._send_alert(self.message_upper, metric_value, ts)
            elif self.threshold_type == "upper":
                self.has_crossed_threshold = True
                self._send_alert(self.message_upper, metric_value, ts)

    def _send_alert(self, message, metric_value, ts):
        """
        Alert user based on severity level.

        :param message      : custom message specified in alerts.txt
        :param metric_value : current metric value that has crossed over a threshold
        :param ts           : current timestamp
        """
        if self.severity == 1:
            logger.debug(f"{message} {self.metric.name}={metric_value}, time={str(ts)}")
        if self.severity == 2:
            logger.info(f"{message} {self.metric.name}={metric_value}, time={str(ts)}")
        if self.severity == 3:
            logger.warning(
                f"{message} {self.metric.name}={metric_value}, time={str(ts)}"
            )
        if self.severity == 4:
            logger.error(f"{message} {self.metric.name}={metric_value}, time={str(ts)}")
        if self.severity == 5:
            logger.critical(
                f"{message} {self.metric.name}={metric_value}, time={str(ts)}"
            )
        return

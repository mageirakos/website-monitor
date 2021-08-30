from abc import ABC, abstractclassmethod
from datetime import datetime, timedelta
import numpy as np


class Metric(ABC):
    """Metric Abstract Class"""

    def __init__(self, websites, name):
        self.name = name
        self.websites = websites

    @abstractclassmethod
    def aggregate(self, url, interval, ts):
        return

    def add_website(self, url, website_object):
        self.websites["url"] = website_object

    def __str__(self):
        return self.name


class AvailabilityMetric(Metric):
    """
    Availability Metric

    availability = #successful/#total pings over interval
    #successful = all status codes besides 5xx and network errors (np.NaN)
    """

    def __init__(self, websites, name="availability"):
        super().__init__(websites, name)

    def aggregate(self, url, interval, ts):
        if not ts:
            ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts - timedelta(seconds=interval) : ts]
        return (
            np.NaN
            if len(data_slice.index) == 0
            else len(data_slice[data_slice["code"] < 500])
            / len(data_slice.index)
        )


class MaxElapsedMetric(Metric):
    """
    Max Response Time Metric

    max_response_time = max(elapsed) over interval
    """

    def __init__(self, websites, name="max_response_time"):
        super().__init__(websites, name)

    def aggregate(self, url, interval, ts):
        if not ts:
            ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts - timedelta(seconds=interval) : ts]
        return (
            np.NaN
            if len(data_slice[data_slice["code"].notna()]) == 0
            else data_slice[data_slice["code"] != -1]["elapsed"].max().total_seconds()
        )


class AvgElapsedMetric(Metric):
    """
    Avg Response Time Metric

    avg_response_time = mean(elapsed) over interval
    """

    def __init__(self, websites, name="avg_response_time"):
        super().__init__(websites, name)

    def aggregate(self, url, interval, ts):
        if not ts:
            ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts - timedelta(seconds=interval) : ts]
        return (
            np.NaN
            if len(data_slice[data_slice["code"].notnull()]) == 0
            else data_slice[data_slice["code"] != -1]["elapsed"].mean().total_seconds()
        )


class MedianElapsedMetric(Metric):
    """
    Median Response Time Metric

    median_response_time = median(elapsed) over interval
    """

    def __init__(self, websites, name="median_response_time"):
        super().__init__(websites, name)

    def aggregate(self, url, interval, ts):
        if not ts:
            ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts - timedelta(seconds=interval) : ts]
        return (
            np.NaN
            if len(data_slice[data_slice["code"].notnull()]) == 0
            else data_slice[data_slice["code"] != -1]["elapsed"]
            .median()
            .total_seconds()
        )


class Elapsed90PrcntMetric(Metric):
    """
    90th Percentile Response Time Metric

    90_prctl_response_time = quantile(0.9) of elapsed over interval
    """

    def __init__(self, websites, name="90_prctl_response_time"):
        super().__init__(websites, name)

    def aggregate(self, url, interval, ts):
        if not ts:
            ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts - timedelta(seconds=interval) : ts]
        # TODO: sort and then print the last 90% ones
        return (
            np.NaN
            if len(data_slice[data_slice["code"].notnull()]) == 0
            else data_slice[data_slice["code"] != -1]["elapsed"]
            .quantile(0.9)
            .total_seconds()
        )


class Num100Metric(Metric):
    """
    Number of 1xx Status Codes Metric

    total_1xx_codes = count("1xx" status codes) over interval
    """

    def __init__(self, websites, name="total_1xx_codes"):
        super().__init__(websites, name)

    def aggregate(self, url, interval, ts):
        if not ts:
            ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts - timedelta(seconds=interval) : ts]
        return (
            np.NaN
            if len(data_slice.index) == 0
            else len(data_slice[data_slice["code"] == 100])
        )


class Num200Metric(Metric):
    """
    Number of 2xx Status Codes Metric

    total_2xx_codes = count("2xx" status codes) over interval
    """

    def __init__(self, websites, name="total_2xx_codes"):
        super().__init__(websites, name)

    def aggregate(self, url, interval, ts):
        if not ts:
            ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts - timedelta(seconds=interval) : ts]
        return (
            np.NaN
            if len(data_slice.index) == 0
            else len(data_slice[data_slice["code"] == 200])
        )


class Num300Metric(Metric):
    """
    Number of 3xx Status Codes Metric

    total_3xx_codes = count("3xx" status codes) over interval
    """

    def __init__(self, websites, name="total_3xx_codes"):
        super().__init__(websites, name)

    def aggregate(self, url, interval, ts):
        if not ts:
            ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts - timedelta(seconds=interval) : ts]
        return (
            np.NaN
            if len(data_slice.index) == 0
            else len(data_slice[data_slice["code"] == 300])
        )


class Num400Metric(Metric):
    """
    Number of 4xx Status Codes Metric

    total_4xx_codes = count("4xx" status codes) over interval
    """

    def __init__(self, websites, name="total_4xx_codes"):
        super().__init__(websites, name)

    def aggregate(self, url, interval, ts):
        if not ts:
            ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts - timedelta(seconds=interval) : ts]
        return (
            np.NaN
            if len(data_slice.index) == 0
            else len(data_slice[data_slice["code"] == 400])
        )


class NumErrorsMetric(Metric):
    """
    Number of Unsuccessful  Pings Metric

    total_1xx_codes = count("1xx" status codes) over interval
    """

    def __init__(self, websites, name="total_5xx_codes"):
        super().__init__(websites, name)

    def aggregate(self, url, interval, ts):
        if not ts:
            ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts - timedelta(seconds=interval) : ts]
        return (
            np.NaN
            if len(data_slice.index) == 0
            else len(data_slice[data_slice["code"] == 500])
        )


if __name__ == "__main__":
    pass

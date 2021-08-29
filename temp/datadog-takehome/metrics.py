from abc import ABC, abstractclassmethod
from datetime import datetime, timedelta

#TODO: Test all of these
class Metric(ABC):
    def __init__(self, websites, name):
        self.name = name
        self.websites = websites
    
    @abstractclassmethod
    def aggregate(self, url, interval, ts):
        return

    def add_website(self, url, website_object):
        self.websites['url'] = website_object

    def __str__(self):
        return self.name

class AvailabilityMetric(Metric):
    def __init__(self, websites, name="availability"):
        super().__init__(websites, name)
        
    def aggregate(self, url, interval, ts):
        """
        availability = #successful/#total ([0,1] range (is %))
        """
        # get the correct time slice out of the data of the correct website
        if not ts: ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts-timedelta(seconds=duration):ts]
        return 0 if len(data_slice.index) == 0 else len(data_slice[data_slice["code"] == 200])/len(data_slice.index)

class MaxElapsedMetric(Metric):
    def __init__(self, websites, name="max_response_time"):
        super().__init__(websites, name)
        
    def aggregate(self, url, interval, ts):
        if not ts: ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts-timedelta(seconds=duration):ts]
        return None if len(data_slice[data_slice["code"].notna()]) == 0 else data_slice[data_slice["code"] != -1]["elapsed"].max().total_seconds()

class AvgElapsedMetric(Metric):
    def __init__(self, websites, name="avg_response_time"):
        super().__init__(websites, name)
        
    def aggregate(self, url, interval, ts):
        if not ts: ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts-timedelta(seconds=duration):ts]
        return None if len(data_slice[data_slice["code"].notnull()]) == 0 else data_slice[data_slice["code"] != -1]["elapsed"].mean().total_seconds()

class MedianElapsedMetric(Metric):
    def __init__(self, websites, name="median_response_time"):
        super().__init__(websites, name)
        
    def aggregate(self, url, interval, ts):
        if not ts: ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts-timedelta(seconds=duration):ts]
        return None if len(data_slice[data_slice["code"].notnull()]) == 0 else data_slice[data_slice["code"] != -1]["elapsed"].median().total_seconds()
                
class Elapsed90PrcntMetric(Metric):
    def __init__(self, websites, name="90_prctl_response_time"):
        super().__init__(websites, name)
        
    def aggregate(self, url, interval, ts):
        if not ts: ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts-timedelta(seconds=duration):ts]
        #TODO: sort and then print the last 90% ones
        return None if len(data_slice[data_slice["code"].notnull()]) == 0 else data_slice[data_slice["code"] != -1]["elapsed"].quantile(0.9).total_seconds()

class Num100Metric(Metric):
    def __init__(self, websites, name="total_1xx_codes"):
        super().__init__(websites, name)
        
    def aggregate(self, url, interval, ts):
        if not ts: ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts-timedelta(seconds=duration):ts]
        return 0 if len(data_slice.index) == 0 else len(data_slice[data_slice["code"] == 100])

class NumSuccessMetric(Metric):
    def __init__(self, websites, name="total_2xx_codes"):
        super().__init__(websites, name)
        
    def aggregate(self, url, interval, ts):
        if not ts: ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts-timedelta(seconds=duration):ts]
        return 0 if len(data_slice.index) == 0 else len(data_slice[data_slice["code"] == 200])

class Num300Metric(Metric):
    def __init__(self, websites, name="total_3xx_codes"):
        super().__init__(websites, name)
        
    def aggregate(self, url, interval, ts):
        if not ts: ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts-timedelta(seconds=duration):ts]
        return 0 if len(data_slice.index) == 0 else len(data_slice[data_slice["code"] == 300])

class Num400Metric(Metric):
    def __init__(self, websites, name="total_4xx_codes"):
        super().__init__(websites, name)
        
    def aggregate(self, url, interval, ts):
        if not ts: ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts-timedelta(seconds=duration):ts]
        return 0 if len(data_slice.index) == 0 else len(data_slice[data_slice["code"] == 400])
        
class NumErrorsMetric(Metric):
    def __init__(self, websites, name="total_5xx_codes"):
        super().__init__(websites, name)
        
    def aggregate(self, url, interval, ts):
        if not ts: ts = datetime.now()
        data_slice = self.websites[url].data.loc[ts-timedelta(seconds=duration):ts]
        return 0 if len(data_slice.index) == 0 else len(data_slice[data_slice["code"] == 500])


if __name__ == "__main__":
    pass
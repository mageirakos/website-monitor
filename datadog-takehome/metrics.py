# from abc import ABC, abstractmethod
# import argparse
# import pandas as pd
# import time, sched
# from datetime import datetime, timedelta
# from collections import defaultdict
# import requests
from abc import ABC, abstractclassmethod

class Metric(ABC):
    def __init__(self, name, websites):
        self.name = name
        self.websites = websites # websites being tracked
        
        
    #TODO: Each metric should have its own aggregate method where we aggregate over a dataslice?
    @abstractclassmethod
    def aggregate(self, url, interval, ts):
        return

class AvailabilityMetric:
    def __init__(self, name, websites):
        super().__init__("availability", websites)
        
    def aggregate(self, url, interval, ts):
        return


if __name__ == "__main__":
    pass
import logging

# create logger
logger = logging.getLogger('simple_example')
logger.setLevel(logging.DEBUG)

# create console handler and set level to debug
ch = logging.StreamHandler()
ch.setLevel(logging.DEBUG)

# create formatter
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')

# add formatter to ch
ch.setFormatter(formatter)

# add ch to logger
logger.addHandler(ch)

# 'application' code
logger.debug('debug message')
logger.info('info message')
logger.warning('warn message')
logger.error('error message')
logger.critical('critical message')


from abc import abstractmethod, ABC


class MetricFactoryABC(ABC):

    def __init__(self, website):
        self.website = website
        self.

    @staticmethod
    def createMetric(metric_type, website):
        """
        WORK
        RESOURCE
        EVENT
        """
        metrics = {"WORK": WorkMetric(website), "RESOURCE": ResourceMetric(website)\
            , "EVent": EventMetric(website)}
        try:
            return metrics[metric_type]
        except KeyError as _e:
            print(_e)
        
class WorkMetric:
    def __init__(self):
        return 
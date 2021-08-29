import argparse
import time, sched

from metrics import Metric, AvailabilityMetric
from alerts import Alert, Alerter
from website import Website




def create_metrics(websites):
    metrics = {
        "availability"           : AvailabilityMetric(websites=websites),
        # "max_response_time"      : MaxElapsedMetric(websites=websites),
        # "avg_response_time"      : AvgElapsedMetric(websites=websites),
        # "90_prctl_response_time" : Elapsed90PrcntMetric(websites=websites),
        # "1xx"                    : Num300Metric(websites=websites),
        # "2xx"                    : NumSuccessMetric(websites=websites),
        # "3xx"                    : Num300Metric(websites=websites),
        # "4xx"                    : Num400Metric(websites=websites),
        # "5xx"                    : NumErrorsMetric(websites=websites),
    }

    return



# ta alerts prepei na ta xeirizetai o scheduler?
# i ta metric ta xeirizetai o scheduler?
# i kati allo xeirizetai o scheduler?

# class Alerter:

#     def __init__(self, websites):
#         self.site_idx = websites #url: Website object
#         self.alerts = defaultdict(list) # dick me key " urls " : alerts sto sugkekrimeno url
#         return

#     #TODO: change this
#     def __str__(self):
#         return f"{self.alerts.items()}, \nAlerter sites: {self.site_idx}"

#     def track(self, alert):
#         """ 
#         Start tracking a specific alert 
        
#         :param alert : Alert object
#         """
#         self.alerts[alert.url].append(alert)
#         return

#     def check_alerts(self, url, ts):
#         """ 
#         Check alerts of website up to timestamp

#         :param url : website's url, used to find alerts specific to that website
#         :param ts  : current timestamp
#         """
#         print("f(x) check_alerts")
#         if url in self.alerts:
#             [alert.check_threshold(data=self.site_idx[url].data, ts=ts) for alert in self.alerts[url]]
#         #TODO: Des otan exeis xrono an to website_obj me to site_idx na einai mesa sto Alert
#                 # Nomize einai alla double check
#         #TODO: oxi to data slicing mesa ston Alerter, thelw mesa sta metrics na ginetai
#         return

# class Alert:
#     def __init__(self, url, severity, metric, aggr_interval, threshold, threshold_type, message_upper, message_lower):
#         self.url = url
#         self.severity = severity
#         #TODO: Prepei na perasw metric object se kathe alert?
#         self.metric_name = metric # pros to paron einai metric name
#         # Aggregation interval for specific alerts != reporting interval of specific stats
#         self.aggr_interval = aggr_interval 
#         self.threshold = threshold
#         self.threshold_type = threshold_type
#         self.message_upper = message_upper
#         self.message_lower = message_lower
#         self.has_crossed_threshold = False

#     def __str__(self):
#         return f"ALERT: {self.url}, {self.severity}, {self.metric_name}, {self.aggr_interval}, {self.threshold}, {self.threshold_type}, {self.message_upper}, {self.message_lower}\n"


#     #TODO: To data den prepei na ginetai edw mesa
#     def check_threshold(self, data, ts):
#         """ 
#         :param data: pandas DataFram with index the ts. so we need to get the data only for the interval we care about
#         :param ts: is current timestamp
#         """
#         #TODO: Where do I get the val from? (some global dataframe that keeps track of ts,statuscode,elapsed)
#         current_data_slice = data.loc[ts-timedelta(seconds=self.aggr_interval):ts]
# #TODO: TEST IF THIS IS CORRECT
        
#         #TODO: Create metric value based on correct slice of data
#         # isws to data_slice prepei na to kanei calculate to metric internally tha doume
#         # kai na tou pernaw 3erw gw to website_object apo to opoio to kanei calculate

#         metric = self.metric_name
# #TODO: We want AGGREGATE TO COMPUT current_data_slice not here 
        
#         #TODO: REMOVE THESE SO THAT THE FUNCTIONS RUNS
#         print("f(x) check_threshold")
#         print("check_threshold of ", self.url, self.metric_name)
#         return

#         metric_value = self.metric.aggregate(ts=ts)

#         # we use .has_crossed_threshold to define "danger zone" above or below threshold and "safe zone" on the other side
#         # when in danger zone we want to keep warning
#         # when in safe zone we want to say that we have recovered
#         if metric_value < self.threshold:
#             if self.threshold_type == "upper" and self.has_crossed_threshold:
#                 # print once that we recovered
#                 _send_alert(self.message_lower, metric_value, ts)
#                 self.has_crossed_threshold = False 
#             if self.threshold_type == "lower":
#                 # sunexeia prints
#                 # WARNING always
#                 _send_alert(self.message_lower, metric_value, ts)
#                 self.has_crossed_threshold = True
#         elif metric_value > self.threshold:
#             if self.threshold_type == "lower" and self.has_crossed_threshold:
#                 # print once that we recovered
#                 _send_alert(self.message_upper, metric_value, ts)
#                 self.has_crossed_threshold = False 
#             if self.threshold_type == "upper":
#                 # sunexeia prints
#                 # WARNING always
#                 _send_alert(self.message_upper, metric_value, ts)
#                 self.has_crossed_threshold = True
#                 # tsekareis an prin itan 
             

#     def _send_alert(self, message, metric_value, ts):
#         #TODO: logging levels WARNING DEBUG kai mlkies?
#         print(f"{message} " + f"{self.metric_name}= {str(metric_value)}, time={str(ts)}")
#         if self.severity == 1:
#             pass
#         if self.severity == 2:
#             pass
#         if self.severity == 3:
#             pass
#         if self.severity == 4:
#             pass
#         if self.severity == 5:
#             pass
#         return
        
    
#         #TODO: Add some save here gia historical reasons opws lene oi idioi?
#         return


#TODO: figure out algorithm
# - to time step mou einai kathe fora pou stelnw request
#       - requests gia kathe website stelnw se sugkekrimeno interval pou to xeirizetai o scheduler
#       - kathe time step (request) thelw na tsekarw mesw tou Alerter gia Alerts

def parse_arguments():
    """Parce cli arguments"""
    #TODO: Add more arguments?
    parser = argparse.ArgumentParser(
        description="""Website Availability & Performance Monitoring"""
    )
    required = parser.add_argument_group("required arguments")
    optional = parser.add_argument_group("optional arguments")
    required.add_argument(
        "-w",
        "--websites",
        type=str,
        required=True,
        default="websites.txt",
        help="Path of .txt file keeping websites we want to monitor.\nline: '<website> <interval>' ",
    )
    optional.add_argument(
        "-a",
        "--alerts",
        type=str,
        required=False,
        default=None,
        help="Path of .txt file keeping alerts we want to monitor.\nline: '<url> <severity> <upper> <lower> <message_upper> <message_lower>' ",
    )
    args = parser.parse_args()
    websites_path = args.websites
    alerts_path = args.alerts
    return (websites_path, alerts_path)

def read_websites_file(filename):
    """
    Read  the websites file
    """
    lines = []
    with open(filename) as f:
        for line in f:
            #TODO: Check that urls are correct
            #TODO: Check that format <website> <interval> is correct
            url, interval = line.split(', ')
            interval = int(interval)
            lines.append((url, interval))
    return lines

def read_alerts_file(filename):
    """
    Read the alerts file
    """
    lines = []
    with open(filename) as f:
        for line in f:
            if line.startswith("#"): continue # considered a comment line
            #TODO: Check that urls are correct
            #TODO: Check that format is correct
            url, severity, metric, aggr_interval, threshold, threshold_type, message_upper, message_lower = line.split(', ')
            aggr_interval = int(aggr_interval)
            #TODO: Gia ta available metrics prepei na exw kapoio .txt pou ta leei idk i sto README.md
            threshold = float(threshold)
            lines.append((url, severity, metric, aggr_interval, threshold, threshold_type, message_upper, message_lower))
    return lines

def create_websites(lines):
    """ create website objects from lines of text file """
    websites = {}
    for url, interval in lines:
        websites[url] = Website(url,interval)

    return websites

def schedule_pings_and_alerts(websites, scheduler, alerter):
    """ 
    input list of websites, 
    schedule when websites will start pinging

    :param websites: dictionary
    """
    print("f(x) scheduling pings for websites")
    # enan scheduler gia kathe website
    # opou leei pote that kalesoume gia prwti fora tin site.start_pinging()
    [scheduler.enter(site.interval, 1, site.start_pinging, argument=(scheduler, alerter)) for url, site in websites.items()]
    return

def schedule_reporting(scheduler, interval):
    #TODO: Create metrics and alerter before scheduling this?
    scheduler.enter(PRINT_10_MINUTES_INTERVAL, 1, print_stats,argument=(websites_list, 10*60, PRINT_10_MINUTES_INTERVAL, scheduler))
    scheduler.enter(PRINT_1_HOUR_INTERVAL, 1, print_stats,argument=(websites_list, 60*60, PRINT_1_HOUR_INTERVAL, scheduler))
    return

#TODO: Test this function
def setup_alerts(alerter, lines):
    """
    1. create alert object
    2. track alert object on alerter (add to alerter dictionary [url], alert) 
    """
    for url, severity, metric, aggr_interval, threshold, threshold_type, message_upper, message_lower in lines:
        #TODO: me vasi to metric_name pou einai sto line kane attach to swsto metric object
        #TODO: Need to create Metrics before I can do the above
        alert = Alert(url, severity, metric, aggr_interval, threshold, threshold_type, message_upper, message_lower)
        alerter.track(alert)
    return

def main():
    # 1. Parse arguments
    (websites_file, alerts_file) = parse_arguments()
    # 2. Read websites.txt
    lines = read_websites_file(websites_file)
    # websites[url] = Website(url,interval)
    # 3. Create Website objects
    websites = create_websites(lines)

    #TODO: 4. Create Metric object

    # 5. Create Alerter
    alerter = Alerter(websites)
    #TODO: 6. Setup Alerts and link them to Alerter #TODO: This needs Metric objects (each alert linked to a metric)
    if alerts_file:
        lines = read_alerts_file(alerts_file)   
        setup_alerts(alerter, lines)

#TODO: TESTED UP TO HERE

    
    #7. Create scheduler:
    scheduler = sched.scheduler(time.time, time.sleep)
    #TODO: 8: The Scheduler should:
    # Schedule the pings of each website based on the interval of each website
    schedule_pings_and_alerts(websites, scheduler, alerter)
    # At every ping we need to monitor our alerts
    scheduler.run()
    return
    while True:
        pass
    exit()
    #TODO: Reporter
    #(1) Every 10s, display the stats for the past 10 minutes for each website
    #(2) Every 60s, display the stats for the past hour for each website
    #TODO: Create Reporter: which is a scheduled class/function that does (1) and (2)
            # Goes through all metrics, and computes based on intervals given
    exit()
    # TSEKARE : 
    schedule_reporting()

    #TODO: create_alerts(websites) opou vazoume o,ti alerts + message pou theloume na ginei tracked 
    #TODO: pinging websites ( kathe ping einai time step ara prepei na stelnoun kai alerts fadazomai)
    #TODO: Should it return tracked_websites (since they are just the websites, it could I guess)

    #TODO: schedule the statistic printing

#TODO: Where is the main data storage that we have?

    # start scheduler
    scheduler.run()


    return 

if __name__ == "__main__":

    main() 
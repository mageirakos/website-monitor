
import argparse
from collections import defaultdict


def parse_arguments():
    """Parce cli arguments"""
    #TODO: Add more arguments?
    parser = argparse.ArgumentParser(
        description="""Website Availability & Performance Monitoring"""
    )
    required = parser.add_argument_group("required arguments")
    required.add_argument(
        "-f",
        "--file",
        type=str,
        required=True,
        default="websites.txt",
        help="Path of txt file keeping websites we want to monitor. file line format: '<website> <interval>' ",
    )
    args = parse_arguments()
    file_path = args.file
    return file_path


# val is expected to be an int
def COUNT_bins(d, val, key):
    # its COUNTING thus we just increment bin
    d[key(val)] += 1
    return d

# val is expected to be an int
def TIMING_bins(d, val, key):
    # its timing thus d is a LIST
    d[key(val)].append(val)
    return d

# san polla filter einai borw na to kanw recursively?
# kathe ena tetoio na einai allo metric?
def COUNT_metrics(code):
    if str(code).startswith("2"): return "2xx" 
    elif str(code).startswith("3"): return "3xx"
    elif str(code).startswith("4"): return "4xx"
    elif str(code).startswith("5"): return "5xx"
    else: return "N/A"

def TIMING_metrics(elapsed):
    return
    
def read_file(filename):
    """
    Read  the websites file
    """
    lines = []
    with open(filename) as f:
        for line in f:
            #TODO: Check that urls are correct
            #TODO: Check that format <website> <interval> is correct
            url, interval = line.split(' ')
            interval = int(interval)
            lines.append((url, interval))
    return lines

def read_file(filename):
    """
    Read  the websites file
    """
    lines = []
    with open(filename) as f:
        for line in f:
            #TODO: Check that urls are correct
            #TODO: Check that format <website> <interval> is correct
            url, interval = line.split(' ')
            interval = int(interval)
            lines.append((url, interval))
    return lines


def main():
    # auta tha einai ta self.data fasi i kati tetoio
    count_bin = defaultdict(int) # COUNT -> with function metrics
    timing_bin = defaultdict(list) # 
    # for metric in metrics tha kanw to .update() pou pernaei to lambda function gia to kathena
    # ta counting exoun apla +1 kai sto aggregate tha vgazoun kati allo?
    #TODO: pws apo auta ta counting bins dimiourgw ta metric pou thelw. To aggregate ti kanei se auta?
    #TODO: to "time" pws blekei edw se auta, pws to kanoume handle
    COUNT_bins(count_bin, 200, lambda x : "success" if x == 200 else "error")
    COUNT_bins(count_bin, 200, lambda x : "success" if x == 200 else "error")
    COUNT_bins(count_bin, 500, lambda x : "success" if x == 200 else "error")
    COUNT_bins(count_bin, 200, lambda x : "success" if x == 200 else "error")
    print(count_bin)
    COUNT_bins(count_bin, 200, COUNT_metrics)
    COUNT_bins(count_bin, 300, COUNT_metrics)
    COUNT_bins(count_bin, 300, COUNT_metrics)
    COUNT_bins(count_bin, 500, COUNT_metrics)
    print(count_bin)
    
    # ta timing exoun apla append giati sto aggregate vgazoun stats klp
    TIMING_bins(timing_bin, 1, lambda x: x)
    TIMING_bins(timing_bin, 1, lambda x: x)
    TIMING_bins(timing_bin, 2, lambda x: x)
    TIMING_bins(timing_bin, 5, lambda x: x)
    TIMING_bins(timing_bin, 5, lambda x: x)
    print(timing_bin)

    # #TODO: Add more arguments?
    # file_path = parse_arguments()

    # websites = read_file(args.file)
    # for url, interval in websites:
    #     response = requests.get(url)
    #     # response here is 200 OK or something
    #     print(f"\nRESPONSE = {response}\n")

    # print(file_path)
    # print("OK")
    return 

if __name__ == "__main__":


    main() 


############################## - REDUNDANCY CODE - 


# class Website:
#     def __init__(self, url, interval):
#         self.url = url
#         self.interval = interval
#         self.data = pd.DataFrame(columns=['code','elapsed'])
#         self.is_being_tracked = False
#         return
    
#     # We need alerter object here because each ping is a timestep in our application
#     # and at each timestep we need to go through our monitored alerts
#     def start_pinging(self, scheduler, alerter):
#         """
#         Method to ping and reschedule next ping of self.website based on self.interval

#         :param alerter: Alerter object, because we need it to check alerts on each ping 
#         """
#         self.is_being_tracked = True
#         # At each ping we are on a specific timestamp ( used for indexing )
#         ts = pd.Timestamp(datetime.now())
#         print("f(x) start_pinging")
#         print("pinging.. ", self.url)
#         try:
#             response = requests.get(self.url, timeout=5)
#             row = pd.DataFrame([[response.status_code, response.elapsed]], index=[ts], columns=['code','elapsed'])
#         except:
#             #TODO: change -1,None so that it doesn't look the same as others code
#             row = pd.DataFrame([[-1, None]], index=[ts], columns=['code','elapsed'])
#         self.data = self.data.append(row)
#         print(f"ts {ts}, url {self.url}, code {response.status_code}, elapsed {response.elapsed}")
#         print("\tdf: ", self.data)

#         print(f"ts: {ts} for {self.url} next in {self.interval}")
#         print()
#         # schedule before we check all alerts
#         scheduler.enter(self.interval, 1, self.start_pinging, argument=(scheduler, alerter))
#         # Only if there are alerts to be tracked on this website check them, check_alerts
#         if self.url in alerter.alerts:
#             alerter.check_alerts(self.url,ts) # check alerts based on current_ts
#         return



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


# class Metric(ABC):
#     def __init__(self, name, websites):
#         self.name = name
#         self.websites = websites # websites being tracked
        
        
#     #TODO: Each metric should have its own aggregate method where we aggregate over a dataslice?
#     @abstractclassmethod
#     def aggregate(self, url, interval, ts):
#         return

# class AvailabilityMetric:
#     def __init__(self, name, websites):
#         super().__init__("availability", websites)
        
#     def aggregate(self, url, interval, ts):
#         return


# if __name__ == "__main__":
#     pass

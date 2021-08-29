
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

#TODO: Should be some abstract function?
#TODO: Ta data_slice mipws prepei na ta pairnei to metric 
#TODO: I na ta ftiaxnei o alerter den katalavainw
#TODO: Nomizw i check_stats (pou kanei aggregate se sugkekrimena time slice)
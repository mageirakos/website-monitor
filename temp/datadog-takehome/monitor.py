import argparse
import time, sched

from metrics import *
from alerts import Alert, Alerter
from website import Website


def create_metrics(websites):
    metrics = {
        "availability"           : AvailabilityMetric(websites=websites),
        "max_response_time"      : MaxElapsedMetric(websites=websites),
        "avg_response_time"      : AvgElapsedMetric(websites=websites),
        "median_response_time"   : MedianElapsedMetric(websites=websites),
        "90_prctl_response_time" : Elapsed90PrcntMetric(websites=websites),
        "total_1xx_codes"        : Num100Metric(websites=websites),
        "total_2xx_codes"        : NumSuccessMetric(websites=websites),
        "total_3xx_codes"        : Num300Metric(websites=websites),
        "total_4xx_codes"        : Num400Metric(websites=websites),
        "total_5xx_codes"        : NumErrorsMetric(websites=websites),
    }
    return metrics

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
def setup_alerts(alerter, lines, metrics):
    """
    1. create alert object
    2. track alert object on alerter (add to alerter dictionary [url], alert) 
    """
    for url, severity, metric_name, aggr_interval, threshold, threshold_type, message_upper, message_lower in lines:
        #TODO: me vasi to metric_name pou einai sto line kane attach to swsto metric object
        #TODO: Need to create Metrics before I can do the above

        #TODO: Check if metrics[metric_name] done correctly
        alert = Alert(url, severity, metrics[metric_name], aggr_interval, threshold, threshold_type, message_upper, message_lower)
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
    # 4. Create Metric object
    #TODO: Test all o fthese
    metrics = create_metrics(websites)

    #TODO: REMOVE - print for testing
    for key, val in metrics.items():
        print(key, val)
    exit()

    # 5. Create Alerter
    alerter = Alerter()
    #TODO: 6. Setup Alerts and link them to Alerter #TODO: This needs Metric objects (each alert linked to a metric)
    if alerts_file:
        lines = read_alerts_file(alerts_file)   
        #TODO: TEST if metrics done correctly
        setup_alerts(alerter, lines, metrics)

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
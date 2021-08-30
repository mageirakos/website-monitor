import argparse
import time, sched
from tabulate import tabulate
import pandas as pd

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
            severity = int(severity)
            message_lower = message_lower.rstrip() 
            message_upper = message_upper.rstrip() 
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
    # enan scheduler gia kathe website
    # opou leei pote that kalesoume gia prwti fora tin site.start_pinging()
    [scheduler.enter(site.interval, 1, site.start_pinging, argument=(scheduler, alerter)) for url, site in websites.items()]
    return

def start_reporting(websites, metrics, reschedule_interval, aggr_interval, scheduler):
    # schedule next and then execute the code
    scheduler.enter(reschedule_interval, 1, start_reporting,argument=(websites, metrics, reschedule_interval, aggr_interval, scheduler))
    
    output, temp = pd.DataFrame(),{}
    ts = pd.Timestamp(datetime.now())
    for url, website in websites.items():
        for metric_name, metric in metrics.items():
            temp[metric_name] = metric.aggregate(website.url, aggr_interval, ts)
        row = pd.DataFrame(temp, index=[website.url])
        output = output.append(row)
    
    print(f"\n\t\t---------------REPORTING METRICS FOR PAST {aggr_interval//60} MINUTES as of {ts}---------------")
    print(tabulate(output, headers='keys', tablefmt='psql'))
    return


# def schedule_reporting(websites, metrics, scheduler, reschedule_interval, aggr_interval):
#     scheduler.enter(reschedule_interval, 1, start_reporting,argument=(websites, metrics, aggr_interval, reschedule_interval, scheduler))
#     # scheduler.enter(60, 1, report_metrics,argument=(websites, metrics,  60*60, 60, scheduler))
#     return

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
    print("Starting monitoring service...")
    # 1. Parse arguments
    (websites_file, alerts_file) = parse_arguments()
    # 2. Read websites.txt
    lines = read_websites_file(websites_file)
    # websites[url] = Website(url,interval)
    # 3. Create Website objects
    websites = create_websites(lines)
    # 4. Create Metric object
    metrics = create_metrics(websites)
    # 5. Create Alerter
    alerter = Alerter()
    #6. Setup Alerts and link them to Alerter 
    if alerts_file:
        lines = read_alerts_file(alerts_file)   
        setup_alerts(alerter, lines, metrics)
    # 7. Create scheduler:
    scheduler = sched.scheduler(time.time, time.sleep)
    # 8: The Scheduler should:
    # Schedule the pings of each website based on the interval of each website
    schedule_pings_and_alerts(websites, scheduler, alerter)
    # 9. Schedule Reporting
    scheduler.enter(10, 1, start_reporting, argument=(websites, metrics, 10, 10*60, scheduler))
    scheduler.enter(60, 1, start_reporting, argument=(websites, metrics, 60, 60*60, scheduler))
    
    scheduler.run()

    return 

if __name__ == "__main__":

    main() 
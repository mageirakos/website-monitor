# general python
import argparse
import time, sched
from tabulate import tabulate
import pandas as pd

# my classes
from metrics import *
from alerts import Alert, Alerter
from website import Website


def create_metrics(websites):
    metrics = {
        "availability": AvailabilityMetric(websites=websites),
        "max_response_time": MaxElapsedMetric(websites=websites),
        "avg_response_time": AvgElapsedMetric(websites=websites),
        "median_response_time": MedianElapsedMetric(websites=websites),
        "90_prctl_response_time": Elapsed90PrcntMetric(websites=websites),
        "total_1xx_codes": Num100Metric(websites=websites),
        "total_2xx_codes": Num200Metric(websites=websites),
        "total_3xx_codes": Num300Metric(websites=websites),
        "total_4xx_codes": Num400Metric(websites=websites),
        "total_5xx_codes": NumErrorsMetric(websites=websites),
    }
    return metrics


def parse_arguments():
    """Parse arguments"""
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
        help="Path of .txt file keeping alerts we want to monitor.\n\
            line: '<url> <severity> <upper> <lower> <message_upper> <message_lower>' ",
    )
    args = parser.parse_args()
    websites_path = args.websites
    alerts_path = args.alerts
    return (websites_path, alerts_path)


def read_websites_file(filename):
    """Read  the websites file"""
    lines = []
    with open(filename) as f:
        for line in f:
            url, interval = line.split(", ")
            interval = int(interval)
            lines.append((url, interval))
    return lines


def read_alerts_file(filename):
    """Read the alerts file"""
    lines = []
    with open(filename) as f:
        for line in f:
            if line.startswith("#"):
                continue
            (
                url,
                severity,
                metric,
                aggr_interval,
                threshold,
                threshold_type,
                message_upper,
                message_lower,
            ) = line.split(", ")
            aggr_interval = int(aggr_interval)
            severity = int(severity)
            message_lower = message_lower.rstrip()
            message_upper = message_upper.rstrip()
            threshold = float(threshold)
            lines.append(
                (
                    url,
                    severity,
                    metric,
                    aggr_interval,
                    threshold,
                    threshold_type,
                    message_upper,
                    message_lower,
                )
            )
    return lines


def create_websites(lines):
    """Create website objects from text file lines"""
    websites = {}
    for url, interval in lines:
        websites[url] = Website(url, interval)
    return websites


def schedule_pings_and_alerts(websites, scheduler, alerter):
    """
    Initialize scheduling loop for websites and alert checks.

    :param websites  : dictionary of websites url:website_object
    :param scheduler : scheduler used to schedule website pings based on their intervals
    :param alerter   : alerter object that keeps track of all alerts and is used to check them after each ping
    """
    [
        scheduler.enter(
            site.interval, 1, site.start_pinging, argument=(scheduler, alerter)
        )
        for url, site in websites.items()
    ]
    return


def start_reporting(websites, metrics, reschedule_interval, aggr_interval, scheduler):
    """
    Report all different metrics for the websites at specific intervals

    :param websites            : dictionary of websites url:website_object
    :param metrics             : dictionary of metrics metric_name:metric_object
    :param reschedule_interval : interval upon which the reporting is scheduled to be printed
    :param aggre_interval      : aggregation interval upon which the metrics are computed
    :param scheduler           : scheduler used to schedule the reporing based on the reschedule_interval
    """
    scheduler.enter(
        reschedule_interval,
        1,
        start_reporting,
        argument=(websites, metrics, reschedule_interval, aggr_interval, scheduler),
    )

    output, temp = pd.DataFrame(), {}
    ts = pd.Timestamp(datetime.now())
    for url, website in websites.items():
        for metric_name, metric in metrics.items():
            temp[metric_name] = metric.aggregate(website.url, aggr_interval, ts)
        row = pd.DataFrame(temp, index=[website.url])
        output = output.append(row)

    print(
        f"\n\t\t---------------REPORTING METRICS FOR PAST {aggr_interval//60} MINUTES as of {ts}---------------"
    )
    print(tabulate(output, headers="keys", tablefmt="psql"))
    return


def setup_alerts(alerter, lines, metrics):
    """
    Create alert objects and link them to alerter

    :param mterics : dictionary of metrics metric_name:metric_object
    """
    for (
        url,
        severity,
        metric_name,
        aggr_interval,
        threshold,
        threshold_type,
        message_upper,
        message_lower,
    ) in lines:
        alert = Alert(
            url,
            severity,
            metrics[metric_name],
            aggr_interval,
            threshold,
            threshold_type,
            message_upper,
            message_lower,
        )
        alerter.track(alert)
    return


def main():
    print("Starting monitoring service...")
    (websites_file, alerts_file) = parse_arguments()
    lines = read_websites_file(websites_file)
    websites = create_websites(lines)
    metrics = create_metrics(websites)
    alerter = Alerter()
    if alerts_file:
        lines = read_alerts_file(alerts_file)
        setup_alerts(alerter, lines, metrics)
    scheduler = sched.scheduler(time.time, time.sleep)
    schedule_pings_and_alerts(websites, scheduler, alerter)
    scheduler.enter(
        10, 1, start_reporting, argument=(websites, metrics, 10, 10 * 60, scheduler)
    )
    scheduler.enter(
        60, 1, start_reporting, argument=(websites, metrics, 60, 60 * 60, scheduler)
    )
    scheduler.run()


if __name__ == "__main__":
    main()

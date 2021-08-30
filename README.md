


# Testing
<!-- ## Alerts

Just for testing purposes alerts_test.txt exists, to run it simply
``` bash
$ python3 monitor.py -w websites.txt -a alerts_test.txt
```
Two main types of alerts have been setup (both on `120 second interval`)
1. `Availability` alert on https://www.datadoghq.com/ with `upper` threshold of 99% on `all 5 different severity levels`
    ``` 
    https://datadoghq.com/, 5, availability, 120, 0.99, upper, Website https://www.google.com/ has recovered., Website https://datadoghq.com/ is down.
https://github.com/, 3, total_2xx_codes, 60, 10, lower, Website https://github.com/ has more than 10 successful pings!, Website https://github.com/ has less than 10 successful pings!.
    ```

2. `Number of Successfull pings` alert on https://github.com/ with `lower` threshold of 10 pings on `severity level 4` -->

# Setup
To run the 


# Metrics
Each different metric belongs to the Metric abstract class, and it has to be specified under `metrics.py`

# Website
Website class in which attributes such as url, interval, and data is kept.
Data is a DataFrame of the history of status_codes and elapsed response times for each ping.

# Alerts
All alerts need to be specified on a text file (default alerts.txt) and passed as an argument to the `monitor.py` script

### Text file format:
- lines starting with `#` are considered comments and skipped
- each line is a single alert holding values: `url, severity, metric, aggr_interval, threshold, threshold_type, message_upper, message_lower`
- make sure that values are comma and single space seperated as above
- no empty lines should exist

### Attributes explanation:
- `url`      : url of a website we want to setup the alert for
- `severity` : severity level of an alert
    - possible values = (`1,2,3,4,5`) equivalent to (DEBUG, INFO, WARNING, ERROR, CRITICAL).  
    - The logic behind severity is that not all alerts are equal, and I used different logging levels to represent how we would handle the different alerts as mentioned on : https://www.datadoghq.com/blog/monitoring-101-alerting/
- `metric`   : metric that we want to track
    - possible values = (`availability`, `max_response_time`, `avg_response_time`, `median_response_time`, `90_prctl_response_time`, `total_1xx_codes`, `total_2xx_codes`, `total_3xx_codes`, `total_4xx_codes`, `total_5xx_codes` )
- `aggr_interval`: interval upon which the metric will aggregate saved values and be computed (in seconds)
- `threshold` : threshold which if crossed the alert will be sent (float)
- `threshold_type` : type of the threshold do determine alerting frequency
    - possible values = (`upper`, `lower`)
        - `upper`: As long as metric value > threshold *we keep on printing* `message_upper`.  
        If the metric value was above the threshold and falls below it we print `message_lower` *once*
        - `lower`: vice versa 
- `message_upper` : message printed when metric value > threshold
- `message_lower` : message printed when metric value < threshold

### Examples
1) Setup an alert on https://www.datadoghq.com/ so that when availability drops below 80% for the past 2 minutes, we keep on alerting the user, at severity level 5 (CRITICAL) that "Website https://www.datadoghq.com/ is down. availability={availability}, time={time}". If the availability resumes we alert once that the website recovered

    ```
    # url, severity, metric, aggr_interval, threshold, threshold_type, message_upper, message_lower
    https://datadoghq.com/, 5, availability, 120, 0.8, lower, Website https://datadoghq.com/ has recovered., Website https://datadoghq.com/ is down.
    ```
    *lines starting with #are considered comments and skipped
2) Setup an alert on https://github.com/ so that if the number of successfull pings are less 10 for the past 1 minute, we keep on alerting the user, at severity level 3 (WARNING) that "Website https://github.com/ has less than 10 successful pings! total_2xx_codes={total_2xx_codes}, time={time}". Vise versa when we have more than 10 successfull pings alert the user *once*
    ```
    https://github.com/, 3, total_2xx_codes, 60, 10, lower, Website https://github.com/ has more than 10 successful pings!, Website https://github.com/ has less than 10 successful pings :(
    ```



### Improvements:
1) Add regex handling to assert and/or clean up url and .txt file formats
2) Have multiple Alert classes, not just the threshold one as I have now.  
For example Change alerts, Outlier alerts, Anomaly alerts, Event alerts Composite alerts, as specified on https://www.datadoghq.com/blog/alerting-101-metric-checks/
3) Add persistant storage so that data is saved between runs (InfluxDB could be used since its a timeseries database)
4) Dynamically resize the reporting output based on terminal size (currently if terminal not wide enough, output might appear off)
5) Add better logic to message_upper, message_lower in alerts.tx handling. For example instead of typing in the url, we can have Website $url is down! and the alerter can identify re.replace() the pattern with website.url
6) logging level configuration on startup, currently I have set it to DEBUG so that all mesages regardless of alert severity are printed in the output
































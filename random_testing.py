import pandas as pd
from metrics import *
from website import Website
from datetime import datetime


def create_metrics(websites):
    metrics = {
        "availability": AvailabilityMetric(websites=websites),
        "max_response_time": MaxElapsedMetric(websites=websites),
        "avg_response_time": AvgElapsedMetric(websites=websites),
        "median_response_time": MedianElapsedMetric(websites=websites),
        "90_prctl_response_time": Elapsed90PrcntMetric(websites=websites),
        "total_1xx_codes": Num100Metric(websites=websites),
        "total_2xx_codes": NumSuccessMetric(websites=websites),
        "total_3xx_codes": Num300Metric(websites=websites),
        "total_4xx_codes": Num400Metric(websites=websites),
        "total_5xx_codes": NumErrorsMetric(websites=websites),
    }
    return metrics


# TODO: This is how testing is done for this
website = Website("https://datadoghq.com/", 5)
df = pd.read_pickle("./df_datado.pkl")
website.data = df
metrics = create_metrics({website.url: website})
print(df)

# "2021-08-30 11:30:43.538594"
# element = datetime.datetime.strptime("2021-08-30 11:30:43.538594")
ts = pd.Timestamp(datetime.now())
ts = pd.Timestamp("2021-08-30 11:30:43.538594")

# dummy alerts.txt gia na testarei to output kai to lower/upper?

df = pd.DataFrame()
output = {}
for metric_name, metric in metrics.items():
    output[metric_name] = metric.aggregate(website.url, 60, ts)
    print(f"{metric_name} = {output[metric_name]}")

row = pd.DataFrame(output, index=[website.url])
df = df.append(row)

for metric_name, metric in metrics.items():
    output[metric_name] = metric.aggregate(website.url, 10, ts)
    print(f"{metric_name} = {output[metric_name]}")

row = pd.DataFrame(output, index=[website.url])
df = df.append(row)

from tabulate import tabulate

print(tabulate(df, headers="keys", tablefmt="psql"))

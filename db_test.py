
from datetime import datetime
import certifi
import urllib3
from influxdb_client import InfluxDBClient, Point, WritePrecision
from influxdb_client.client.write_api import SYNCHRONOUS
import numpy as np

# You can generate an API token from the "API Tokens Tab" in the UI
token = "WG-tdJhI8ldQdZiX_OLGSlhoc3XjXbKgX1WSUjgYgFRXJ_NxWVllNjzjFwyp1qB9ShPrjK8iJXQdwGv--ZNZxg=="
org = "martinrovang@gmail.com"
bucket = "test"



with InfluxDBClient(url="https://europe-west1-1.gcp.cloud2.influxdata.com", token=token, org=org, ssl_ca_cert=certifi.where()) as client:
    write_api = client.write_api(write_options=SYNCHRONOUS)
    data = "mem,host=host1 used_percent=23.43234543"
    write_api.write(bucket, org, data)

    point = Point("mem") \
    .tag("host", "host1") \
    .field("used_percent",  3424234) \
    .time(datetime.utcnow(), WritePrecision.NS)
    write_api.write(bucket, org, point)
    sequence = ["mem,host=host1 used_percent=23.43234543",
            "mem,host=host1 available_percent=15.856523"]
    write_api.write(bucket, org, sequence)
    query = 'from(bucket: "test") |> range(start: -1h)'
    tables = client.query_api().query(query, org=org)
    for table in tables:
        for record in table.records:
            print(record)
    

    client.close()



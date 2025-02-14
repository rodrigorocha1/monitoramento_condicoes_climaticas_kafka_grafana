from datetime import datetime
import influxdb_client
from influxdb_client.client.write_api import SYNCHRONOUS
import os
from dotenv import load_dotenv
load_dotenv()

url = os.environ['INFLUXDB_URL']
token = os.environ['INFLUXDB_TOKEN']
org = os.environ['INFLUXDB_ORG']
bucket = os.environ['INFLUXDB_BUCKET']

client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)

write_api = client.write_api(write_options=SYNCHRONOUS)

p = influxdb_client.Point("my_measurement").tag(
    "location", "Prague").field("temperature", 25.3).field('teste_campo', 1)
write_api.write(bucket=bucket, org=org, record=p)


client = influxdb_client.InfluxDBClient(
    url=url,
    token=token,
    org=org
)


query_api = client.query_api()
query = f'from(bucket:"{bucket}")\
|> range(start: -10m)\
|> filter(fn:(r) => r._measurement == "my_measurement")\
|> filter(fn:(r) => r.location == "Prague")\
|> filter(fn:(r) => r._field == "teste_campo")'
result = query_api.query(org=org, query=query)
results = []
for table in result:
    for record in table.records:
        results.append((record.get_field(), record.get_value()))

print(results)

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


data_hora = datetime.now()
data_hora_formatada = data_hora.strftime('%Y-%m-%d %H:%M:%S')

data_str = data_hora_formatada
data_obj = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
print(data_str)
timestamp = int(data_obj.timestamp() * 1_000_000_000)

dados = {
    'cidade': 'cidade_teste',
    'temperatura': 27.6,
    'icone': '11d',
}

p = influxdb_client.Point("teste_json_v3").tag(
    "location", dados['cidade']
).field(
    "temperatura", dados['temperatura']
).field('icone', dados['icone']).time(timestamp, write_precision='ns')

write_api.write(bucket=bucket, org=org, record=p)

query_api = client.query_api()

query = f'from(bucket:"{bucket}")\
|> range(start: -1d)\
|> filter(fn:(r) => r._measurement == "teste_json_v3")\
|> filter(fn:(r) => r.location == "{dados["cidade"]}")'

result = query_api.query(org=org, query=query)

results = []
for table in result:
    for record in table.records:
        results.append(
            (record.get_field(), record.get_value(), record.get_time()))

print(results)

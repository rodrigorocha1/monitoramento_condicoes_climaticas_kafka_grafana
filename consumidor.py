from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from src.servico.kafka_consumidor_clima import KafkaConsumidorClima
from dotenv import load_dotenv
import os
from dateutil import parser
load_dotenv()


class Consumidor:

    def __init__(self):

        self.__INFLUXDB_URL = os.environ['INFLUXDB_URL']
        self.__INFLUXDB_TOKEN = os.environ['INFLUXDB_TOKEN']
        self.__INFLUXDB_ORG = os.environ['INFLUXDB_ORG']
        self.__INFLUXDB_BUCKET = os.environ['INFLUXDB_BUCKET']
        self.__cliente = InfluxDBClient(
            url=self.__INFLUXDB_URL,
            token=self.__INFLUXDB_TOKEN,
            org=self.__INFLUXDB_ORG
        )

        self.__kafka_consumer = KafkaConsumidorClima(
            bootstrap_servers='kafka:9092',
            group_id='weather_grupo',
            topico=os.environ['TOPICO']
        )
        try:
            self.__cliente.ping()
            print("Conectado ao InfluxDB com sucesso!")

        except Exception as e:
            print(f"Falha na conexão com o InfluxDB: {e}")

    def gerar_mensagens(self):
        for dados in self.__kafka_consumer.consumidor_mensagens():
            escrever_api = self.__cliente.write_api(write_options=SYNCHRONOUS)

            print('=' * 20)
            print(dados)
            data_hora_atual = parser.parse(
                dados['data_hora_atual']).replace(tzinfo=None)

            angulo_vento = float(
                dados['angulo_vento']) if dados['angulo_vento'] is not None else 0.0

            data_point = Point('dados_climaticos') \
                .tag('cidade', dados['cidade']) \
                .field('temperatura', round(float(dados['temperatura']), 2)) \
                .time(data_hora_atual)

            try:
                escrever_api.write(
                    bucket=self.__INFLUXDB_BUCKET,
                    record=data_point
                )
                print('Dados gravados no InfluxDB')
            except Exception as e:
                print(f'Erro ao gravar no InfluxDB: {e}')


if __name__ == '__main__':
    c = Consumidor()
    c.gerar_mensagens()

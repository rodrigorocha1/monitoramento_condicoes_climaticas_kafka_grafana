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
            topico='historico_tempo_v2'
        )

    def gerar_mensagens(self):
        for dados in self.__kafka_consumer.consumidor_mensagens():
            escrever_api = self.__cliente.write_api(write_options=SYNCHRONOUS)

            print('=' * 20)
            print(f'Partição: {dados["particao"]}')
            print(f"Cidade: {dados['cidade']}")
            print(f"Temperatura: {dados['temperatura']}°C")
            print(f"Data/Hora_api: {dados['data_hora_api']}")
            print(f"Data/Hora: {dados['data_hora_atual']}")

            data_hora_api = parser.parse(dados['data_hora_api'])
            data_hora_atual = parser.parse(dados['data_hora_atual'])
            data_point = Point('dados_climaticos') \
                .tag('cidade', dados['cidade']) \
                .field('clima', dados['clima']) \
                .field('icone', dados['icone']) \
                .field('umidade', dados['umidade']) \
                .field('velocidade_vento', dados['velocidade_vento']) \
                .field('angulo_vento', dados['angulo_vento']) \
                .field('probabilidade_chuva', dados['probabilidade_chuva']) \
                .field('temperatura', round(float(dados['temperatura']), 2)) \
                .time(data_hora_api) \
                .time(data_hora_atual)

            escrever_api.write(
                bucket=self.__INFLUXDB_BUCKET,
                record=data_point
            )

            print('=' * 20)


if __name__ == '__main__':
    c = Consumidor()
    c.gerar_mensagens()

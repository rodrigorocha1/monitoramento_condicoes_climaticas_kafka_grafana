from typing import Dict
from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from src.servico.kafka_consumidor_clima import KafkaConsumidorClima
from dotenv import load_dotenv
from datetime import datetime
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

    def __converter_data(self, data_hora: str) -> int:
        data_obj = datetime.strptime(data_hora, '%Y-%m-%d %H:%M:%S')

        timestamp = int(data_obj.timestamp() * 1_000_000_000)
        return timestamp

    def __realizar_tratamento_valores(self, dados: Dict, chave: str):
        return float(
            dados[chave]) if dados[chave] is not None else 0.0

    def gerar_mensagens(self):
        for dados in self.__kafka_consumer.consumidor_mensagens():
            escrever_api = self.__cliente.write_api(write_options=SYNCHRONOUS)

            print('=' * 20)
            print(dados)

            data_hora_api = self.__converter_data(
                data_hora=dados['data_hora_api'])
            probabilidade_chuva = self.__realizar_tratamento_valores(
                dados=dados,
                chave='probabilidade_chuva'
            )

            angulo_vento = self.__realizar_tratamento_valores(
                dados=dados,
                chave='angulo_vento'
            )

            velocidade_vento = self.__realizar_tratamento_valores(
                dados=dados,
                chave='velocidade_vento'
            )

            umidade = self.__realizar_tratamento_valores(
                dados=dados,
                chave='umidade'
            )

            temperatura = self.__realizar_tratamento_valores(
                dados=dados,
                chave='temperatura'
            )

            data_point = Point('dados_climaticos') \
                .tag('cidade', dados['cidade']) \
                .field('temperatura', temperatura) \
                .field('clima', dados['clima']) \
                .field('icone', dados['icone']) \
                .field('umidade', umidade) \
                .field('velocidade_vento', velocidade_vento) \
                .field('angulo_vento', angulo_vento) \
                .field('probabilidade_chuva', probabilidade_chuva) \
                .time(data_hora_api)

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

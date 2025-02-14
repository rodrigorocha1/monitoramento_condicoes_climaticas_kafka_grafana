from influxdb_client import InfluxDBClient, Point
from influxdb_client.client.write_api import SYNCHRONOUS
from src.servico.kafka_consumidor_clima import KafkaConsumidorClima


class Consumidor:

    def __init__(self):

        # self.__INFLUXDB_URL = ''
        # self.__INFLUXDB_TOKEN = ''
        # self.__INFLUXDB_ORG = ''
        # self.__INFLUXDB_BUCKET = ''
        # self.__cliente = InfluxDBClient(
        #     url=self.__INFLUXDB_URL,
        #     token=self.__INFLUXDB_TOKEN,
        #     org=self.__INFLUXDB_ORG
        # )

        self.__kafka_consumer = KafkaConsumidorClima(
            bootstrap_servers='kafka:9092',
            group_id='weather_grupo',
            topico='cidade'
        )

    def gerar_mensagens(self):
        for dados in self.__kafka_consumer.consumidor_mensagens():

            print('=' * 20)
            print(f'Partição: {dados["particao"]}')
            print(f"Cidade: {dados['cidade']}")
            print(f"Temperatura: {dados['temperatura']}°C")
            print(f"Data/Hora_api: {dados['data_hora_api']}")
            print(f"Data/Hora: {dados['data_hora_atual']}")

            print('=' * 20)


if __name__ == '__main__':
    c = Consumidor()
    c.gerar_mensagens()

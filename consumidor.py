import os
from src.servico.kafka_consumidor_clima import KafkaConsumidorClima


class KafkaConsumidorClima:

    def __init__(self):
        self.__kafka_consumer = KafkaConsumidorClima(
            bootstrap_servers='localhost:9092',
            group_id='weather_grupo',
            topico='topico_teste'
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

from src.servico.kafka_produtor_clima import KafkaProdutorClima
import json
from src.servico.iservicotempo import IservicoTempo


class Produtor:
    def __init__(self, servico_tempo: IservicoTempo):
        self.__kafka_produtor = KafkaProdutorClima(
            bootstrap_servers=''
        )

        self.__servico_tempo = servico_tempo
        self.__cidades = [
            "Barrinha",
            "Brodowski",
            "Cravinhos",
            "Dumont",
            "Guatapará",
            "Jardinópolis",
            "Pontal",
            "Pradópolis",
            "Ribeirão Preto",
            "Santa Rita do Passa Quatro",
            "São Simão",
            "Serrana",
            "Serra Azul",
            "Sertãozinho"
        ]

    def rodar_produtor(self):
        pass

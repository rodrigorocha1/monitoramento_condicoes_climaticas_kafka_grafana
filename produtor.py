from src.servico.kafka_produtor_clima import KafkaProdutorClima
from dotenv import load_dotenv
from src.servico.iservicotempo import IservicoTempo
from time import sleep
import os
load_dotenv()


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
        total_particoes = len(self.__cidades)
        topico = 'cidade'
        self.__kafka_produtor.criar_topico(
            topico=topico,
            numero_particoes=total_particoes
        )
        numero_particoes = self.__kafka_produtor.verificar_particoes(
            topico=self.__topico)

        while True:
            for particao, cidade in enumerate(self.__cidades):
                dados_tempo = self.__servico_tempo.obter_tempo_atual(
                    cidade=cidade
                )
                self.__kafka_produtor.enviar_dados_clima(
                    topico=topico,
                    dados_climaticos=dados_tempo,
                    municipio=cidade,
                    particao=particao
                )
                sleep(os.environ['TEMPO_ESPERA'])

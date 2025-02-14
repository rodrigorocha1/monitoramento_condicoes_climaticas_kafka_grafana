from src.servico.kafka_produtor_clima import KafkaProdutorClima
from dotenv import load_dotenv
from src.servico.iservicotempo import IservicoTempo
from time import sleep
from src.servico.openweater import OpenWeater
import os
import time
load_dotenv()


class Produtor:
    def __init__(self, servico_tempo: IservicoTempo):
        self.__kafka_produtor = KafkaProdutorClima(
            bootstrap_servers='kafka:9092'
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
        topico = 'historico_tempo_v2'
        self.__kafka_produtor.criar_topico(
            topico=topico,
            numero_particoes=total_particoes
        )
        time.sleep(10)
        numero_particoes = self.__kafka_produtor.verificar_particoes(
            topico=topico)
        print(f'Numero de partições: {numero_particoes}')

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
            sleep(int(os.environ['TEMPO_ESPERA']))


if __name__ == '__main__':
    p = Produtor(servico_tempo=OpenWeater())
    p.rodar_produtor()

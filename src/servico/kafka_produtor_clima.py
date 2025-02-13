import json
from typing import Dict
from kafka import KafkaProducer, KafkaAdminClient
from kafka.admin import NewTopic
from kafka.errors import TopicAlreadyExistsError


class KafkaProdutorClima:

    def __init__(self, bootstrap_servers: str):
        """Init da classe KafkaProdutorClima

        Args:
            bootstrap_servers (str): url do kafka
        """
        self.__produtor = KafkaProducer(
            bootstrap_servers=bootstrap_servers,
            value_serializer=lambda v: json.dumps(v).encode('utf-8'),
            key_serializer=lambda k: k.encode('utf-8')
        )
        self.__admin_cliente = KafkaAdminClient(
            bootstrap_servers=bootstrap_servers
        )

    def criar_topico(self, topico: str, numero_particoes: int) -> None:
        """Método para criar tótico

        Args:
            topico (str): Nome do tópico
            numero_particoes (int): número de partições a ser criada
        """

        try:
            novo_topico = NewTopic(
                name=topico,
                num_partitions=numero_particoes,
                replication_factor=1
            )
            self.__admin_cliente.create_topics([novo_topico])

        except:
            return

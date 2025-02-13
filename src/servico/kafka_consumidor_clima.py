import json
import datetime
from typing import Any, Dict, Generator
from kafka import KafkaConsumer


class KafkaConsumidorClima:
    def __init__(self, bootstrap_servers: str, group_id: str, topico: str) -> None:
        """Init do KafkaConsumidorClima

        Args:
            bootstrap_servers (str): url do servidor kafka
            group_id (str): grupo id
            topico (str): tótico a ser consumido
        """
        self.__consumer = KafkaConsumer(
            topico,
            bootstrap_servers=bootstrap_servers,
            group_id=group_id,
            value_deserializer=lambda x: json.loads(x.decode('utf-8')),
            auto_offset_reset='latest',
            enable_auto_commit=True
        )

    def consumidor_mensagens(self) -> Generator[Dict[str, Any], None, None]:
        """Método para consumir mensagens

        Yields:
            Generator[Dict[str, Any], None, None]: Um gerador com o dicionário
        """

        try:
            for mensagem in self.__consumer:
                cidade = mensagem.value["name"]
                data_hora = datetime.datetime.fromtimestamp(
                    mensagem.value["dt"]).strftime('%Y-%m-%d %H:%M:%S')
                temperatura = mensagem.value["main"]["temp"]
                velocidade_vento = mensagem.value["wind"]["speed"]
                umidade = mensagem.value["main"]["humidity"]
                angulo_vento = mensagem.value["wind"]["deg"]
                probabilidade_chuva = mensagem.value["clouds"]["all"]
                data_hora_atual = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                chave = mensagem.key
                clima = mensagem.value["weather"][0]["description"]
                particao = mensagem.partition
                offset = mensagem.offset
                icone = mensagem.value["weather"][0]["icon"]
                yield {
                    'particao': particao,
                    'cidade': cidade,
                    'data_hora_api': data_hora,
                    'temperatura': temperatura,

                    'data_hora_atual': data_hora_atual,
                    'clima': clima,
                    'icone': icone,
                    'umidade': umidade,

                    'velocidade_vento': velocidade_vento,
                    'angulo_vento': angulo_vento,
                    'probabilidade_chuva': probabilidade_chuva

                }

        except:
            print(f'Erro No municipio {mensagem.value}')

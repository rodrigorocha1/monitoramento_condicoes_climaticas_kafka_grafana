import json
from datetime import datetime
from typing import Any, Dict, Generator
from kafka import KafkaConsumer
from kafka.errors import KafkaError
import time


class KafkaConsumidorClima:
    def __init__(self, bootstrap_servers: str, group_id: str, topico: str) -> None:
        """Init do KafkaConsumidorClima

        Args:
            bootstrap_servers (str): url do servidor kafka
            group_id (str): grupo id
            topico (str): tótico a ser consumido
        """
        for i in range(11):
            try:
                self.__consumer = KafkaConsumer(
                    topico,
                    bootstrap_servers=bootstrap_servers,
                    group_id=group_id,
                    value_deserializer=lambda x: json.loads(x.decode('utf-8')),
                    auto_offset_reset='latest',
                    enable_auto_commit=True
                )
                break
            except KafkaError as e:
                print(f"Tentativa {i + 1}/5 falhou: {e}")
                time.sleep(30)
        else:
            raise RuntimeError(
                "Falha ao conectar ao Kafka após várias tentativas.")

    def consumidor_mensagens(self) -> Generator[Dict[str, Any], None, None]:
        """Método para consumir mensagens

        Yields:
            Generator[Dict[str, Any], None, None]: Um gerador com o dicionário
        """

        try:
            for mensagem in self.__consumer:
                cidade = mensagem.value["name"]
                data_hora = datetime.fromtimestamp(
                    mensagem.value["dt"]).strftime('%Y-%m-%d %H:%M:%S')
                temperatura = mensagem.value["main"]["temp"]
                velocidade_vento = mensagem.value["wind"]["speed"]
                umidade = mensagem.value["main"]["humidity"]
                angulo_vento = mensagem.value["wind"]["deg"]
                probabilidade_chuva = mensagem.value["clouds"]["all"]
                data_hora_atual = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
                chave = mensagem.key
                clima = mensagem.value["weather"][0]["description"]
                particao = mensagem.partition
                offset = mensagem.offset
                icone = mensagem.value["weather"][0]["icon"]
                pressao_atmosferica = mensagem.value['main']['pressure']
                data_hora_nascer_sol = datetime.fromtimestamp(
                    mensagem.value['sys']['sunrise']).strftime('%d/%m/%Y %H:%M:%S')

                data_hora_por_sol = datetime.fromtimestamp(
                    mensagem.value['sys']['sunset']).strftime('%d/%m/%Y %H:%M:%S')

                visibilidade = mensagem.value['visibility']
                yield {
                    'particao': particao,
                    'cidade': cidade,
                    'data_hora_api': data_hora,
                    'temperatura': temperatura,

                    'data_hora_atual': data_hora_atual,
                    'clima': clima,
                    'icone': f'https://openweathermap.org/img/wn/{icone}.png',
                    'umidade': umidade,

                    'velocidade_vento': velocidade_vento,
                    'angulo_vento': angulo_vento,
                    'probabilidade_chuva': probabilidade_chuva,
                    'pressao_atmosferica': pressao_atmosferica,
                    'data_hora_nascer_sol': data_hora_nascer_sol,
                    'data_hora_por_sol': data_hora_por_sol,
                    'visibilidade': visibilidade

                }

        except Exception as e:
            print(f'Erro No municipio {mensagem.value} - {e}')

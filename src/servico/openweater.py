import os
from dotenv import load_dotenv
import requests
from typing import Dict, Any
from src.servico.iservicotempo import IservicoTempo
load_dotenv()


class OpenWeater(IservicoTempo):

    def __init__(self) -> None:
        self.__url = os.environ['URL_OPENWEATHER']
        self.__chave = os.environ['OPENWEATHER_KEY']

    def obter_tempo_atual(self, cidade: str) -> Dict[str, Any]:
        """Método para obter os dados climáticos de umm múnicipio

        Args:
            cidade (str): cidade

        Returns:
            Dict[str, Any]: a requisição dos dados climáticos
        """
        params = {
            'appid': self.__chave,
            'units': 'metric',
            'lang': 'pt_br',
            'q': cidade
        }
        response = requests.get(
            url=self.__url + 'weather',
            params=params,
            timeout=10
        )
        response.raise_for_status()
        if response.status_code == 200:
            return response.json()
        return {}

from abc import ABC, abstractmethod
from typing import Any, Dict


class IservicoTempo(ABC):
    @abstractmethod
    def obter_tempo_atual(self, cidade: str) -> Dict[str, Any]:
        pass

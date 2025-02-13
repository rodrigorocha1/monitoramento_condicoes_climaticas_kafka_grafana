from src.servico.openweater import OpenWeater
ow = OpenWeater()

dados = ow.obter_tempo_atual(cidade='Ribeirão Preto')
print(dados)

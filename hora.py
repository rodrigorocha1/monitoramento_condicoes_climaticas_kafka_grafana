

from datetime import datetime

data_hora = datetime.now()
data_hora_formatada = data_hora.strftime('%Y-%m-%d %H:%M:%S')

print(data_hora_formatada)

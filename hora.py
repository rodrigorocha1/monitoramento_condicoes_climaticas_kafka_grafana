

from datetime import datetime
data_hora = datetime.now()
data_hora_formatada = data_hora.strftime('%Y-%m-%d %H:%M:%S')
data_str = data_hora_formatada
data_obj = datetime.strptime(data_str, '%Y-%m-%d %H:%M:%S')
timestamp = int(data_obj.timestamp() * 1_000_000_000)
print(type(timestamp))

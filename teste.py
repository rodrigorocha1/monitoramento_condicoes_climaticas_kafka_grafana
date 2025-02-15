from datetime import datetime

timestamp = 1739656138
data_formatada = datetime.fromtimestamp(
    timestamp).strftime('%d/%m/%Y %H:%M:%S')
print(data_formatada, type(data_formatada))

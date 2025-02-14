#!/bin/bash

sudo rm -rf ./influxdb_data/ ./influxdb2-config/ ./grafana_data/
mkdir -p ./influxdb_data/ ./influxdb2-config/ ./grafana_data/
sudo chmod -R 777 ./influxdb_data/ ./influxdb2-config/ ./grafana_data/
sudo chown -R 472:472 ./influxdb_data/ ./influxdb2-config/
sudo chown -R 472:472 ./grafana_data/csv

echo "Diretórios configurados com sucesso."

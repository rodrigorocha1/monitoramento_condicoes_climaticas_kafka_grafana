#!/bin/bash

sudo rm -rf influxdb2-data/ influxdb2-config/ grafana_data/
mkdir -p influxdb2-data/ influxdb2-config/ grafana_data/
sudo chmod -R 777 influxdb2-data/ influxdb2-config/ grafana_data/
sudo chown -R 472:472 influxdb2-data/ influxdb2-config/

echo "Diretórios configurados com sucesso."

# Sistema de Monitoramento Climático de Ribeirão Preto

Este projeto tem como objetivo propor um sistema de monitoramento climático para a região de Ribeirão Preto, utilizando Apache Kafka para coleta de dados e Grafana para visualização e análise em tempo real.

## Tecnologias Utilizadas

- **Apache Kafka** para coleta e distribuição de dados
- **Python** para a programação do produtor e consumidor
- **OpenWeatherAPI** para obtenção dos dados de temperatura
- **Grafana** para monitoramento e visualização dos dados coletados
- **Docker** para contêinerização dos serviços
- **Banco de dados InfluxDB** para armazenamento de dados

## Arquitetura do Sistema

### 1. Produtor Python

Um script Python coleta os dados da API OpenWeather dos seguintes municípios:

- Barrinha, Brodowski, Cravinhos, Dumont, Guatapará, Jardinópolis, Pontal, Pradópolis, Ribeirão Preto, Santa Rita do Passa Quatro, São Simão, Serrana, Serra Azul, Sertãozinho.

Esses dados são publicados em um tópico Kafka.

### 2. Consumidor Python

O consumidor (script Python) escuta o tópico Kafka e grava os dados coletados no banco de dados InfluxDB.

### 3. Grafana

O Grafana acessa o banco de dados e exibe os dados em tempo real no dashboard.

![Fluxo de dados](https://raw.githubusercontent.com/rodrigorocha1/monitoramento_condicoes_climaticas_kafka_grafana/refs/heads/main/fig/diagrama_fundo_preto.png)

## Gráficos e Métricas

### 1. Tabela com o Ângulo dos Ventos

Exibe a direção do vento junto com a sua velocidade.

### 2. Tabela com a Velocidade dos Ventos

Exibe a velocidade do vento junto com sua respectiva classificação na escala de Beaufort.

#### Escala de Beaufort para Velocidade dos Ventos

| Força | Velocidade do Vento (km/h) | Descrição             |
|-------|----------------------------|-----------------------|
| 0     | 0 – 1                      | Calmaria              |
| 1     | 2 – 5                      | Brisa muito leve      |
| 2     | 6 – 11                     | Brisa leve            |
| 3     | 12 – 19                    | Brisa fraca           |
| 4     | 20 – 28                    | Brisa moderada        |
| 5     | 29 – 38                    | Brisa forte           |
| 6     | 39 – 49                    | Vento fresco          |
| 7     | 50 – 61                    | Vento forte           |
| 8     | 62 – 74                    | Ventania              |
| 9     | 75 – 88                    | Ventania forte        |
| 10    | 89 – 102                   | Temporal              |
| 11    | 103 – 117                  | Tempestade violenta   |
| 12    | 118 ou mais                | Furacão               |

### 3. Temperatura, Umidade, Velocidade, Pressão Atmosférica e Visibilidade

Esses dados são exibidos com um card mostrando o valor no momento, junto com um gráfico de linha que representa o valor ao longo do tempo.

## Diagrama de Classe para o Produtor e Consumidor

A arquitetura do sistema é mostrada abaixo, desde o monitoramento até a gravação dos dados no banco de dados InfluxDB.

![Diagrama de Classe](https://raw.githubusercontent.com/rodrigorocha1/monitoramento_condicoes_climaticas_kafka_grafana/refs/heads/main/out/diagramas/diagrama_classe/diagrama_classe.png)

## Demonstração do Dashboard

Abaixo está uma captura de tela da interface do Grafana mostrando o dashboard com os dados em tempo real.

[![Dashboard](https://img.youtube.com/vi/G23vsXYHjIo/0.jpg)](https://youtu.be/G23vsXYHjIo)

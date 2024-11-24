#!/bin/bash

# Mensagem para indicar que o banco está pronto
echo "Banco de dados pronto! Iniciando a aplicação..."

# Comandos para iniciar a aplicação
# Exemplo para Django:
python manage.py migrate
python manage.py runserver 0.0.0.0:8000

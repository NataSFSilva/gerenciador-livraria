#!/bin/bash


host=db
port=3306
timeout=60

echo "Aguardando o banco de dados..."

until nc -z $host $port >/dev/null 2>&1; do
  timeout=$((timeout - 1))
  if [ $timeout -eq 0 ]; then
    echo "Timeout aguardando o banco de dados."
    exit 1
  fi
  sleep 1
done

echo "Banco de dados pronto! Iniciando a API..."

python app.py
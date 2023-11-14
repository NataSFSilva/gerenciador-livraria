# Use uma imagem oficial do Python como imagem base
FROM python:3.9-slim

# Configuração do ambiente
ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

# Criação e definição do diretório de trabalho
WORKDIR /app
# Instalação das dependências
COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt

# Copia o código fonte para o contêiner
COPY . /app/

# Comando para iniciar a aplicação
CMD ["python", "app.py"]
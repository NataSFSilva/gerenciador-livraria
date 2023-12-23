FROM python:3.9-slim

ENV PYTHONDONTWRITEBYTECODE 1
ENV PYTHONUNBUFFERED 1

WORKDIR /app

COPY requirements.txt /app/
RUN pip install --upgrade pip
RUN pip install -r requirements.txt
RUN apt-get update && apt-get install curl -y
RUN apt-get install wget -y
RUN apt-get install systemctl -y
RUN wget https://github.com/grafana/agent/releases/download/v0.38.1/grafana-agent-0.38.1-1.amd64.deb -O grafana-agent.deb
RUN apt install ./grafana-agent.deb

COPY grafana-agent.yaml /etc/grafana-agent.yaml

COPY . /app/
ADD https://github.com/ufoscout/docker-compose-wait/releases/download/2.11.0/wait /wait
RUN chmod +x /wait

CMD /wait && flask --app app run --debug && grafana-agent -config.file=/etc/grafana-agent.yaml
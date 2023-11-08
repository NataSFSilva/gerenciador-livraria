FROM mysql:8.1.0

COPY ./db/ /docker-entrypoint-initdb.d/

RUN docker run -d -p 3000:3000 --name=grafana grafana/grafana-enterprise
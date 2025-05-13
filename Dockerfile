FROM python:alpine

LABEL traefik.enable=true
LABEL traefik.http.routers.calendar_builder.rule=Host(`calendar.olegsklyarov.ru`)
LABEL traefik.http.routers.calendar_builder.tls=true
LABEL traefik.http.routers.calendar_builder.entrypoints=websecure
LABEL traefik.http.routers.calendar_builder.tls.certresolver=mytlschallenge
LABEL traefik.docker.network=infra_web_net

WORKDIR /usr/src/app

COPY . .
RUN pip install --no-cache-dir -r requirements.txt

EXPOSE 8000

CMD ["./run-gunicorn.sh"]


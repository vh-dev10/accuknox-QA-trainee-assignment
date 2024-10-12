FROM alpine:latest

RUN apk add --no-cache bash

WORKDIR /app


COPY . .


RUN chmod +x wisecow.sh
ENTRYPOINT ["./wisecow.sh"]
FROM --platform=amd64 ubuntu:22.04 as build

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get -y install tzdata
RUN apt-get install -y python3.10 curl
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN pip install poetry
COPY . /src
WORKDIR /src
RUN poetry build --format=wheel



FROM --platform=amd64 kitware/trame:py3.10-glvnd-2024-06 as run

COPY --from=build /src/dist /dist
COPY --chown=trame-user:trame-user dockerfiles/setup /deploy/setup

ENV TRAME_CLIENT_TYPE=vue3
ENV OAUTHLIB_INSECURE_TRANSPORT=1
RUN ls
RUN /opt/trame/entrypoint.sh build

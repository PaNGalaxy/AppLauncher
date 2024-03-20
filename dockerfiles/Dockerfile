ARG BUILD_ENV=no_conda

FROM --platform=amd64 ubuntu:22.04 as build

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get -y install tzdata
RUN apt-get install -y python3.10 curl
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN pip install poetry
COPY template_app /src/template_app
COPY pyproject.toml poetry.lock /src/
WORKDIR /src
RUN poetry build --format=wheel

FROM --platform=amd64 kitware/trame:py3.10-conda-glvnd-2024-01 as build_no_conda
ONBUILD RUN echo "skipping conda"
ONBUILD ENTRYPOINT []

FROM --platform=amd64 kitware/trame:py3.10-conda-glvnd-2024-01 as build_conda
ONBUILD RUN conda config --add channels mantid
ONBUILD RUN conda config --add channels conda-forge
ONBUILD RUN conda create -n trame python=3.10
ONBUILD RUN conda install -n trame mantid
ONBUILD SHELL ["conda", "run", "-n", "trame", "/bin/bash", "-c"]
ONBUILD ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "trame"]

FROM build_${BUILD_ENV}

COPY --from=build /src/dist /dist
RUN pip install /dist/*

RUN apt update && apt install -y nginx
RUN chmod og+rwX -R /var/lib/nginx
RUN chmod og+rwX -R /var/log/nginx
RUN chmod og+rwX -R /etc/nginx

COPY dockerfiles/nginx.conf.template /etc/nginx/nginx.conf.template
COPY dockerfiles/prepare_nginx.sh /

RUN python -m trame.tools.www --client-type vue3 --output /app/www-content


USER trame-user

FROM --platform=amd64 ubuntu:22.04 AS build

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get -y install tzdata
RUN apt-get install -y python3.10 curl
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN pip install poetry
COPY . /src
WORKDIR /src
RUN poetry build --format=wheel



FROM --platform=amd64 kitware/trame:py3.10-conda-glvnd-2024-01 AS run

RUN pip install --extra-index-url https://wheels.vtk.org vtk-egl
RUN pip install --extra-index-url https://code.ornl.gov/api/v4/projects/15758/packages/pypi/simple py-mvvm
RUN pip install --extra-index-url https://code.ornl.gov/api/v4/projects/16294/packages/pypi/simple trame-facade

COPY --from=build /src/dist /dist
RUN pip install /dist/*.whl

RUN apt update && apt install -y nginx
RUN chmod og+rwX -R /var/lib/nginx
RUN chmod og+rwX -R /var/log/nginx
RUN chmod og+rwX -R /etc/nginx

COPY dockerfiles/nginx.conf.template /etc/nginx/nginx.conf.template
COPY dockerfiles/prepare_nginx.sh /

RUN python -m trame.tools.www --client-type vue3 --output /app/www-content


USER trame-user
ENTRYPOINT []

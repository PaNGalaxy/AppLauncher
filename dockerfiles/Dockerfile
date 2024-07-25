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
ENV TRAME_AUTH_URL=https://login.microsoftonline.com/db3dbd43-4c4b-4544-9f8a-0553f9f5f25e/oauth2/v2.0/authorize
ENV TRAME_TOKEN_URL=https://login.microsoftonline.com/db3dbd43-4c4b-4544-9f8a-0553f9f5f25e/oauth2/v2.0/token
ENV TRAME_CLIENT_ID=e026ce47-b0c4-4e9f-aa7f-2b53f234685b
ENV TRAME_CLIENT_SECRET=secret
ENV TRAME_REDIRECT_URL=https://nova-test.ornl.gov/redirect
# ENV TRAME_REDIRECT_URL=http://localhost:8080/redirect
ENV TRAME_XCAMS_AUTH_URL=https://devextidp.ornl.gov/as/authorization.oauth2
ENV TRAME_XCAMS_TOKEN_URL=https://devextidp.ornl.gov/as/token.oauth2
ENV TRAME_XCAMS_CLIENT_ID=1c266db0-d7bd-45c2-9b68-4807f9bec427
ENV TRAME_XCAMS_CLIENT_SECRET=secret

RUN /opt/trame/entrypoint.sh build

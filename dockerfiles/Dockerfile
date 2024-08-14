FROM --platform=amd64 ubuntu:22.04 as build

RUN DEBIAN_FRONTEND="noninteractive" apt-get update && apt-get -y install tzdata
RUN apt-get install -y python3.10 curl
RUN curl -sS https://bootstrap.pypa.io/get-pip.py | python3.10
RUN pip install poetry
COPY . /src
WORKDIR /src
RUN poetry build --format=wheel



FROM --platform=amd64 kitware/trame:py3.10-glvnd-2024-08 as run

RUN apt update
RUN apt install -y mc && apt install -y vim

COPY --from=build /src/dist /dist
COPY --chown=trame-user:trame-user dockerfiles/setup /deploy/setup
ENV TRAME_CLIENT_TYPE=vue3

COPY launcher_app/default-launcher.json /opt/trame/default-launcher.json
RUN /opt/trame/entrypoint.sh build
COPY launcher_app/app/tools.json /config/tools.json
ENV TRAME_UCAMS_AUTH_URL="https://login.microsoftonline.com/db3dbd43-4c4b-4544-9f8a-0553f9f5f25e/oauth2/v2.0/authorize"
ENV TRAME_UCAMS_TOKEN_URL="https://login.microsoftonline.com/db3dbd43-4c4b-4544-9f8a-0553f9f5f25e/oauth2/v2.0/token"
ENV TRAME_UCAMS_CLIENT_ID="e026ce47-b0c4-4e9f-aa7f-2b53f234685b"
ENV TRAME_UCAMS_REDIRECT_URL="http://localhost:8080/redirect"

# ENV TRAME_UCAMS_AUTH_URL="http://localhost:8082/realms/master/protocol/openid-connect/auth"
# ENV TRAME_UCAMS_TOKEN_URL="http://localhost:8082/realms/master/protocol/openid-connect/token"
# ENV TRAME_UCAMS_CLIENT_ID="trame-demo"
# ENV TRAME_UCAMS_REDIRECT_URL="http://localhost:8080/redirect"

ENV TRAME_XCAMS_AUTH_URL="https://devextidp.ornl.gov/as/authorization.oauth2"
ENV TRAME_XCAMS_TOKEN_URL="https://devextidp.ornl.gov/as/token.oauth2"
ENV TRAME_XCAMS_CLIENT_ID="1c266db0-d7bd-45c2-9b68-4807f9bec427"
ENV TRAME_XCAMS_REDIRECT_URL="http://localhost:8080/authnz/pingfed/callback"
# ENV TRAME_XCAMS_REDIRECT_URL="http://localhost:8080/authnz"

ENV TRAME_UCAMS_SCOPES="email profile openid User.Read"
ENV TRAME_XCAMS_SCOPES="email profile openid https://calvera-test.ornl.gov/api:*"

ENV GALAXY_URL="https://calvera-test.ornl.gov"
ENV GALAXY_API_KEY=""
ENV GALAXY_API_KEY_ENDPOINT="/api/authenticate/baseauth"
ENV GALAXY_HISTORY_ID=""
ENV GALAXY_LAUNCHER_HISTORY_NAME="launcher_history"

ENV TRAME_LAUNCHER_TOOL_PATH="/config/tools.json"
ENV EP_PATH="/"
ENV TRAME_ROUTER_HISTORY_MODE=html5




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

# credentials for a dummy Google project. Non-sensitive so I can commit them
ENV TRAME_UCAMS_AUTH_URL="https://accounts.google.com/o/oauth2/v2/auth"
ENV TRAME_UCAMS_TOKEN_URL="https://oauth2.googleapis.com/token"
ENV TRAME_UCAMS_CLIENT_ID="317943623786-cju613t4todopb3cj9uh06hkhboofca2.apps.googleusercontent.com"
ENV TRAME_UCAMS_CLIENT_SECRET="REPLACE_ME"
ENV TRAME_UCAMS_REDIRECT_URL="http://localhost/redirect"

ENV TRAME_XCAMS_AUTH_URL=""
ENV TRAME_XCAMS_TOKEN_URL=""
ENV TRAME_XCAMS_CLIENT_ID=""
ENV TRAME_XCAMS_CLIENT_SECRET=""
ENV TRAME_XCAMS_REDIRECT_URL="http://localhost:8080/authnz/pingfed/callback"

ENV TRAME_UCAMS_SCOPES="https://www.googleapis.com/auth/userinfo.email openid https://www.googleapis.com/auth/userinfo.profile"
ENV TRAME_XCAMS_SCOPES="email profile openid https://calvera-test.ornl.gov/api:*"

ENV GALAXY_URL="https://calvera-test.ornl.gov"
ENV GALAXY_API_KEY=""
ENV GALAXY_API_KEY_ENDPOINT="/api/authenticate/baseauth"
ENV GALAXY_HISTORY_ID=""
ENV GALAXY_LAUNCHER_HISTORY_NAME="launcher_history"

ENV TRAME_LAUNCHER_TOOL_PATH="/config/tools.json"
ENV EP_PATH="/"
ENV TRAME_ROUTER_HISTORY_MODE=html5




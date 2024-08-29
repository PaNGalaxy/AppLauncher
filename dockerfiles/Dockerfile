FROM ubuntu:noble
ARG DEBIAN_FRONTEND=noninteractive

RUN apt update && apt upgrade -y && apt install -y \
    curl \
    software-properties-common \
    nginx
RUN add-apt-repository ppa:deadsnakes/ppa -y
RUN apt update && apt install -y \
    python3.10

# Install Poetry
RUN curl -fsSL https://install.python-poetry.org | POETRY_HOME=/etc/poetry python3.10 -
ENV PATH="$PATH:/etc/poetry/bin"

# Install Node.js LTS & pnpm
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash -
RUN apt install -y nodejs
ENV SHELL=bash
RUN curl -fsSL https://get.pnpm.io/install.sh | sh -

# Setup Django
ADD django /opt/run/django
WORKDIR /opt/run/django
RUN poetry install
# Install dependencies only used in production builds
RUN poetry run pip install gunicorn uvicorn-worker

# Create static client build
ADD vue /opt/run/vue
WORKDIR /opt/run/vue
RUN /root/.local/share/pnpm/pnpm install
RUN /root/.local/share/pnpm/pnpm build

ADD dockerfiles/nginx.conf /etc/nginx/nginx.conf
ADD dockerfiles/entrypoint.sh /opt/run/entrypoint.sh

RUN mkdir -p /tmp
RUN mkdir -p /run/nginx

WORKDIR /opt/run/django
ENTRYPOINT ["bash", "/opt/run/entrypoint.sh"]

# Introduction

This is a project that can be used as a template to create a new Trame application.
It has a couple of tabs with input fields, example how to interact with Galaxy instance, 
upload and download configuration.


## Install dependencies  

```
poetry install
```

## Run

```bash
poetrty start run
```

## Develop

Run `poetry env info  --path` to see the path to Poetry environment. It can then be used
to configure your IDE to select the correct Python interpreter.

## Docker
### Build the image

with conda and mantid

```bash
docker build -f dockerfiles/Dockerfile -t app .
```

### Run the container

```
docker run -p 8080:80 -it -e EP_PATH=/app app
```

then open your browser at http://localhost:8081/app/
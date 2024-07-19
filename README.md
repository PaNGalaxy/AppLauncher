# Introduction

This is a project that can be used as a template to create a new Trame application.
It has a couple of tabs with input fields, example how to interact with Galaxy instance, 
upload and download configuration.


## Install dependencies  

```
poetry install
```

## Run
In order to use the auth module locally with a non-https server, you will need to set the following envrionment variable:
```
OAUTHLIB_INSECURE_TRANSPORT=1
``` 

In order to connect to Galaxy to launch a tool, you will also need to set the following environment variables:
```
GALAXY_URL=https://calvera-test.ornl.gov
GALAXY_API_KEY={YOUR_API_KEY}
```

You will also need to provide a JSON file containing the data for all the tools that can be launched from this
application. One is provided at `"launcher_app/app/tools.json"`, however you can also set the environment variable:
`TRAME_LAUNCHER_TOOL_PATH` to point to another file if you wish. The format of the file should follow that of the provided 
example. 

Then you can run the following to start the application:
```bash
poetry start run
```

## Develop

Run `poetry env info  --path` to see the path to Poetry environment. It can then be used
to configure your IDE to select the correct Python interpreter.

## Docker
### Build the image

without conda and mantid:

```bash
docker build -f dockerfiles/Dockerfile -t app .
```

with conda and mantid

```bash
docker build --build-arg BUILD_ENV=conda -f dockerfiles/Dockerfile -t app .
```

### Run the container

```
docker run -p 8081:8081 -it -e EP_PATH=/app app bash -c "/prepare_nginx.sh && python -m template_app.app --host 0.0.0.0 --server"  
```

then open your browser at http://localhost:8081/app/
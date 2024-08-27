# Introduction

This repository is for the source code of the Trame Launcher App (running at https://nova.ornl.gov). The purpose
of this web application is to serve as a dashboard for users to launch their Trame reduction apps without going through
Calvera/Galaxy.


## Install dependencies

You will need to install [Poetry](https://python-poetry.org/) and [pnpm](https://pnpm.io/). After doing so, you can run
the following commands to build the source code.

```bash
cd django
poetry install
```

```bash
cd vue
pnpm i
```

## Run

To configure and run the app properly, a `.env` file is needed in the top level directory of this repository.
A sample file `.env.sample` is provided with all the configuration options available. Because your `.env` may contain
secrets, make sure this does not get committed to the upstream repository. You can also set the environment variables
manually in your environment or prefix them to your run command.

You will also need to provide a JSON file containing the configuration data for all the tools that can be launched from this
application. The default file is located in `vue/public/tools.json`, and it should be modified in place if you need to make
changes.

```json
{
  "imaging": {
    "name": "Imaging",
    "description": "MARS, VENUS",
    "tools": [
      {
        "id": "neutrons_ctr",
        "name": "CT Reconstruction",
        "description": "Computed Tomography Reconstruction in a Jupyter Notebook",
        "max_instances": 1
      }
    ]
  }
}
```

After your environment is configured, run the following to start the application:
```bash
bash go.sh
```

In order to use the authentication locally with a non-https server, you will need to set the following environment variable:
```
OAUTHLIB_INSECURE_TRANSPORT=1
```
This is not recommended unless you are developing locally.

In order to connect to Galaxy to launch a tool, you will also need to set the following environment variables in your
`.env` file or in your environment:
```
GALAXY_URL=https://calvera-test.ornl.gov
```

## Develop

Run `poetry env info  --path` to see the path to Poetry environment. It can then be used
to configure your IDE to select the correct Python interpreter.

## Docker
### Build the image

without conda and mantid:

```bash
docker build . -f dockerfiles/Dockerfile -t app --platform {your_build_platform}
```

### Run the container

```bash
docker run -p 8080:8080 -it --env-file {path/to/your/.env} app
```

then open your browser at http://localhost:8080

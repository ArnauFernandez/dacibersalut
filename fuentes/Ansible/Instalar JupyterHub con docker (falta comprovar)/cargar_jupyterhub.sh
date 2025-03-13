#!/bin/bash

# region Acceder al contenedor de JupyterHub para realizar la instalación y la configuración
docker exec -it jupyterhub bash

apt update && apt install -y nodejs npm python3 openssl

python3 -m pip install --upgrade pip

python3 -m pip install jupyterhub

npm install -g configurable-http-proxy

python3 -m pip install jupyterlab notebook

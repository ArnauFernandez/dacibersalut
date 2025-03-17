# Instalación de Jupyter

## Instalamos el paquete PIP de Python

sudo apt install python3-pip

## Comprobamos que está instalado

python3 -m ensurepip

## Instalamos el paquete de Jupyterhub con PIP 

python3 -m pip install jupyterhub

## Instalamos el paquete de configurable-http-proxy

npm install -g configurable-http-proxy
 
## s

python3 -m pip install jupyterlab notebook

Paso 6:
jupyterhub -h

generate default config file:
    jupyter --generate-config -f /etc/jupyterhub/jupyterhub_config.py
  spawn the server on 10.0.1.2:443 with https:
    jupyterhub --ip 10.0.1.2 --port 443 --ssl-key my_ssl.key --ssl-cert my_ssl.cert

Paso 7:
configurable-http-proxy -h

Paso 8:
sudo jupyterhub

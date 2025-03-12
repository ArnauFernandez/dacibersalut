#!/bin/bash

# region Copiar el script remove_comments.sh al contenedor de JupyterHub
docker cp remove_comments.sh jupyterhub:/srv/jupyterhub/Eliminar_comentarios.sh
# endregion

# region Acceder al contenedor de JupyterHub para realizar la instalación y la configuración
docker exec -it jupyterhub bash -c "
    # Instalar dependencias necesarias (si no están instaladas)
    command -v jupyterhub >/dev/null 2>&1 || {
        apt update && apt install -y nodejs npm python3 openssl
        python3 -m pip install --upgrade pip
        python3 -m pip install jupyterhub
        npm install -g configurable-http-proxy
        python3 -m pip install jupyterlab notebook

        # Generar certificado SSL si no existe
        if [ ! -f /srv/jupyterhub/servidor.crt ]; then
            openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
                -keyout /srv/jupyterhub/servidor.key -out /srv/jupyterhub/servidor.crt \
                -subj '/CN=jupyterhub/O=MyOrg/C=ES'
        fi

        # Crear usuario admin si no existe
        id -u admin >/dev/null 2>&1 || useradd -m -s /bin/bash -p \"$(openssl passwd -1 ciber25)\" -G sudo admin
    }

    # Generar el fichero de configuración si no existe
    if [ ! -f /srv/jupyterhub/jupyterhub_config.py ]; then
        jupyterhub --generate-config
    fi

    # Llamar al script para eliminar los comentarios en el archivo de configuración
    bash /srv/jupyterhub/Eliminar_comentarios.sh
"
# endregion

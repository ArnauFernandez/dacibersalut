# Usar una imagen base con Python y JupyterHub
FROM jupyterhub/jupyterhub:latest

# Instalar dependencias adicionales
RUN pip install --no-cache-dir jupyterlab notebook

# Crear directorio para JupyterHub
RUN mkdir -p /srv/jupyterhub

# Copiar configuración de JupyterHub
COPY jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

# Generar certificado SSL autofirmado
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /srv/jupyterhub/jupyterhub.key -out /srv/jupyterhub/jupyterhub.crt \
    -subj "/CN=localhost"

# Crear usuario admin dentro del contenedor
RUN useradd -m -s /bin/bash -U admin && echo "admin:admin" | chpasswd

# Exponer el puerto 8000 para JupyterHub
EXPOSE 8000

# Comando para iniciar JupyterHub
CMD ["jupyterhub", "--ip", "0.0.0.0", "--port", "8000", "--config", "/srv/jupyterhub/jupyterhub_config.py"]

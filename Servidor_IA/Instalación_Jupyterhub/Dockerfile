# Usar la imagen base oficial de JupyterHub
FROM jupyterhub/jupyterhub:latest

# Instal·lar dependències addicionals per JupyterLab i Notebook
RUN pip install --no-cache-dir jupyterlab notebook pydicom tensorflow

# Crear directori per a JupyterHub
RUN mkdir -p /srv/jupyterhub

# Copiar la configuració personalitzada de JupyterHub
COPY ./jupyterhub_config.py /srv/jupyterhub/jupyterhub_config.py

# Generar certificat SSL autofirmat (válid per 365 dies)
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /srv/jupyterhub/jupyterhub.key -out /srv/jupyterhub/jupyterhub.crt \
    -subj "/CN=localhost"

# Crear usuari administrador dins el contenidor
RUN useradd -m -s /bin/bash -U admin && echo "admin:admin" | chpasswd

# Exposar el port per defecte de JupyterHub
EXPOSE 8000

# Comandament per iniciar JupyterHub amb configuració específica
CMD ["jupyterhub", "--ip", "0.0.0.0", "--port", "8000", "--config", "/srv/jupyterhub/jupyterhub_config.py"]

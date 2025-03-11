# Imatge base de JupyterHub
FROM quay.io/jupyterhub/jupyterhub

# Actualitzar el sistema i instal·lar nano i openssl per generar les claus SSL
RUN apt-get update && apt-get install -y nano openssl

# Instal·lar jupyterlab i notebook
RUN pip install --upgrade jupyterlab notebook

# Generar les claus SSL autofirmades
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 \
    -keyout /srv/jupyterhub/jupyterhub.key \
    -out /srv/jupyterhub/jupyterhub.crt \
    -subj "/C=US/ST=Denial/L=Springfield/O=Dis/CN=localhost"

# Afegir les configuracions de JupyterHub al fitxer ja existent a /srv/jupyterhub
RUN echo "c.JupyterHub.admin_access = True" >> /srv/jupyterhub/jupyterhub_config.py && \
    echo "c.JupyterHub.admin_users = {'admin'}" >> /srv/jupyterhub/jupyterhub_config.py && \
    echo "c.JupyterHub.ssl_cert = '/srv/jupyterhub/jupyterhub.crt'" >> /srv/jupyterhub/jupyterhub_config.py && \
    echo "c.JupyterHub.ssl_key = '/srv/jupyterhub/jupyterhub.key'" >> /srv/jupyterhub/jupyterhub_config.py && \
    echo "c.Authenticator.allow_existing_users = True" >> /srv/jupyterhub/jupyterhub_config.py

# Expose the port JupyterHub will run on
EXPOSE 8000

# Comando per executar JupyterHub
CMD ["jupyterhub"]
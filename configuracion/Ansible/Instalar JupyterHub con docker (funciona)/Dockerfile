# Usar una imagen base con Python y JupyterHub
FROM jupyterhub/jupyterhub:latest

# Instalar dependencias adicionales
RUN pip install --no-cache-dir jupyterlab notebook

# Crear directorio para JupyterHub
RUN mkdir -p /srv/jupyterhub

# Generar el archivo de configuración predeterminado
RUN jupyterhub --generate-config -f /srv/jupyterhub/jupyterhub_config.py

# Generar certificado SSL autofirmado
RUN openssl req -x509 -nodes -days 365 -newkey rsa:2048 -keyout /srv/jupyterhub/jupyterhub.key -out /srv/jupyterhub/jupyterhub.crt -subj "/C=US/ST=State/L=City/O=Organization/CN=localhost"

# Configurar JupyterHub para autenticación con usuarios del sistema
RUN sed -i 's|^# \?c.JupyterHub.admin_access =.*|c.JupyterHub.admin_access = True|' /srv/jupyterhub/jupyterhub_config.py && \
    sed -i "s|^# \?c.JupyterHub.admin_users =.*|c.JupyterHub.admin_users = {'admin'}|" /srv/jupyterhub/jupyterhub_config.py && \
    sed -i 's|^# \?c.JupyterHub.ssl_cert =.*|c.JupyterHub.ssl_cert = "/srv/jupyterhub/jupyterhub.crt"|' /srv/jupyterhub/jupyterhub_config.py && \
    sed -i 's|^# \?c.JupyterHub.ssl_key =.*|c.JupyterHub.ssl_key = "/srv/jupyterhub/jupyterhub.key"|' /srv/jupyterhub/jupyterhub_config.py && \
    sed -i 's|^# \?c.Authenticator.allow_all =.*|c.Authenticator.allow_all = True|' /srv/jupyterhub/jupyterhub_config.py && \
    sed -i 's|^# \?c.Authenticator.allow_existing_users =.*|c.Authenticator.allow_existing_users = True|' /srv/jupyterhub/jupyterhub_config.py && \
    sed -i 's|^# \?c.LocalAuthenticator.create_system_users =.*|c.LocalAuthenticator.create_system_users = True|' /srv/jupyterhub/jupyterhub_config.py && \
    sed -i 's|^# \?c.JupyterHub.authenticator_class =.*|c.JupyterHub.authenticator_class = "jupyterhub.auth.PAMAuthenticator"|' /srv/jupyterhub/jupyterhub_config.py

# Crear usuario admin dentro del contenedor
RUN useradd -m -s /bin/bash -U admin && echo "admin:admin" | chpasswd

# Exponer el puerto 8000 para JupyterHub
EXPOSE 8000

# Variables de entorno necesarias
ENV JUPYTERHUB_CRYPT_KEY=supersecretkey

# Volúmenes para permitir autenticación con usuarios del sistema
VOLUME ["/etc/passwd", "/etc/shadow", "/etc/group", "/home"]

# Comando para iniciar JupyterHub
CMD ["jupyterhub", "--ip", "0.0.0.0", "--port", "8000", "--config", "/srv/jupyterhub/jupyterhub_config.py"]

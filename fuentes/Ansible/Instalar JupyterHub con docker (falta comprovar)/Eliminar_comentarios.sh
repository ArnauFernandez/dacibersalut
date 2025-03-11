#!/bin/bash

# Eliminar los comentarios (#) de las configuraciones requeridas
sed -i 's|^# \?c.JupyterHub.admin_access =.*|c.JupyterHub.admin_access = True|' /srv/jupyterhub/jupyterhub_config.py
sed -i "s|^# \?c.JupyterHub.admin_users =.*|c.JupyterHub.admin_users = {'admin'}|" /srv/jupyterhub/jupyterhub_config.py
sed -i 's|^# \?c.JupyterHub.ssl_cert =.*|c.JupyterHub.ssl_cert = \"/srv/jupyterhub/jupyterhub.crt\"|' /srv/jupyterhub/jupyterhub_config.py
sed -i 's|^# \?c.JupyterHub.ssl_key =.*|c.JupyterHub.ssl_key = \"/srv/jupyterhub/jupyterhub.key\"|' /srv/jupyterhub/jupyterhub_config.py
sed -i 's|^# \?c.Authenticator.allow_all =.*|c.Authenticator.allow_all = True|' /srv/jupyterhub/jupyterhub_config.py
sed -i 's|^# \?c.Authenticator.allow_existing_users =.*|c.Authenticator.allow_existing_users = True|' /srv/jupyterhub/jupyterhub_config.py
sed -i 's|^# \?c.LocalAuthenticator.create_system_users =.*|c.LocalAuthenticator.create_system_users = True|' /srv/jupyterhub/jupyterhub_config.py

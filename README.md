# Manual usuario Proyecto DaCiberSalut

## Playbooks de Ansible

### Requisitos previos
Para poder ejecutar los playbooks de anisble se debe tener en cuenta que debe haber una previa conexión por ssh.

Para obtener la contraseña cifrada se ejecuta con el siguiente comando:  
ansible-vault encrypt_string 'contrasenya' --name 'ansible_pass'

### Ansible python3
ansible-playbook -i inventory.ini Servidor IA/Instal·lació_Python3/python3_playbook.yml --ask-vault-pass --ask-become-pass

### Ansible Webmin
ansible-playbook -i inventory.ini Servidor IA/Instal·lació_Webmin/webmin_playbook.yml --ask-vault-pass --ask-become-pass

### Ansible Jupyterhub
ansible-playbook -i inventory.ini Servidor IA/Instalacion_Jupyterhub/jupyterhub_playbook.yml --ask-vault-pass --ask-become-pass

### Ansible MariaDB
Antes de ejecutar el comando del ansible-playbook se debe cifrar las contraseñas en el archivo secrets.yml.  
Pas 1: Crear el archivo secrets.yml utilizando ansible-vault:  
ansible-vault create secrets.yml  

Pas 2: Añadir las contraseñas en el archivo vault_secrets.yml de esta forma:  
MYSQL_ROOT_PASSWORD: "ciber25"
MYSQL_DATABASE: "oh"
MYSQL_USER: "isf"
MYSQL_PASSWORD: "ciber25"
DB_PASSWORD: "ciber25"

Paso 3: Despues encriptar el fichero vault_secrets.yml con la siguiente comanda:
ansible-vault encrypt vault_secrets.yml

Paso 4: Añadir variables en el .env de esta forma:
YSQL_ROOT_PASSWORD={{ MYSQL_ROOT_PASSWORD }}
MYSQL_DATABASE={{ MYSQL_DATABASE }}
MYSQL_USER={{ MYSQL_USER }}
MYSQL_PASSWORD={{ MYSQL_PASSWORD }}

DB_PASSWORD={{ DB_PASSWORD }}

Paso 5: Ejecutar el comando ansible-playbook   
ansible-playbook -i inventory.ini Servidor\ BBDD/Instalación_MariaDB\ \(En\ Revision\ encryptado\ contraseña\)/docker_mariadb_playbook.yml --ask-become-pass --ask-vault-pass

### Ansible Distribuir claves
ansible-playbook -i inventory.ini ssh_key.yml --ask-become-pass

## Gestión de Usuarios
### Usuarios de sistema 
Esta tarea, se realizará con un script en python, la cual se encuentra en el respositorio de servidor de IA, en el que para poder ejecutarlo debemos ser administradores por el simple hecho de que podemos añadir,modificar,borrar y añador al grupo de superusuario como a nosotros nos plazca, por ello esta versión actual del script solo lo debe ejecutar el superusuario y debe tener una fuerte coraza para que su accesibilidad sea exclusiva.

#### Implementación de variables de entorno
Con la reciente implementación de las variables de entorno para porteger al máximo la seguridad de nuestros scripts, para ello generamos un archivo oculto .env en el que guardamos variables que deseemos cifrar.
Para ejecutar los scripts se deberán seguir los pasos detallados en el apartado de ejecución, debemos genererar un entorno virtual con python3 ejecutaremos el siguiente comando **python3 -m venv venv** y después entramos en el entorno con el comando **source venv/bin/activate** e instalar el paquete dotenv con este comando **pip install python-dotenv** y así ejecutamos nuestro script
 
### Usuarios BBDD
Esta tarea, se realizará con un script en python, la cual se encuentra en el respositorio de configuración, en el que para poder ejecutarlo debemos ser adminisradores por el simple hecho de que podemos añadir,modificar,borrar y añador al grupo de superusuario como a nosotros nos plazca, por ello esta versión actual del script solo lo debe ejecutar el superusuario y debe tener una fuerte coraza para que su accesibilidad sea exclusiva.
En este caso al estar situado en un contenedor de docker los scripts para generar los usuarios se generarán en el servidor físico donde esté alojado nuestro servicio docker, por que el directorio en el que se almacenan estará vinculado a este

### Ejecución de los scripts
En este caso tenemos tres scripts con lo respectan la gestión de los usuarios en la BBDD **usuaris-alta.py** que permite registrar a los usuarios como su propio nombre indica, **usuaris-modifica.py** que permite modificar los usuarios y al grupo que pertenecen, **usuaris-baixa.py** que implementa la baja de los usuarios. En esta ocasión como hablábamos en la anterior se debe ser superusuario debido a que se pueden dar permisos a usuarios no autorizados y borrar usuarios que no se deben eliminar.
Y también se debe contar con el archivo .csv que permitirá al script ejecutarse con normalidad y desarollar sus tareas

## Contenedores docker,como ejecutar y descargar sus servicios

### Mirth connect
docker pull nextgenhealthcare/connect:latest

docker run -d --name mirthconnect -v /home/isard/Imatges:/opt/mirth/images -p 8080:8080 -p 8443:8443 -e MIRTH_HOME=/opt/mirth --restart always nextgenhealthcare/connect:latest

#### Instalar mirth connect
Se deberá descargar el archivo de lanzador de administrador de la interfície web ejecutarlo como root con el siguiente comando **bash mirth-administrator-launcher-latest-unix** y se ejecutará el menu de instalación cuando ya se haya instalado deberemos ejecutar el lanzador con el comando **launcher** y se nos abrirá esta pestaña ![imatge](https://github.com/user-attachments/assets/1352d72d-ee7d-4f21-ac36-e2733236c397) 

y debemos indicar que parametros tenga nuestra consola de administrador.

cuando ya se hayan configurado los parametros a nuestro gusto se nos abrirá la consola de administración

![imatge](https://github.com/user-attachments/assets/c41daac9-f457-4024-b0fb-22b187142f68)

### MariaDB
docker pull mariadb:latest

docker run -d --name openhospital_db -v ohv:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=ciber25 mariadb:latest

### Jupyterhub
sudo docker run --privileged -v ./jupyterhub_config.py:/srv/jupyterhub/jupyterhub_config.py -v /etc/passwd:/etc/passwd -v /etc/group:/etc/group -v /home:/home -v /etc/shadow:/etc/shadow -v /home/isard/Imatges:/srv/jupyterhub/Imatges  -p 8000:8000 --name jupyter   quay.io/jupyterhub/jupyterhub

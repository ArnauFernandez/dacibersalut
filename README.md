# Manual usuario Proyecto DaCiberSalut

## Playbooks de Ansible
### Requisitos previos
Para poder ejecutar los playbooks de anisble se debe tener en cuenta que debe haber una previa conexión por ssh.
### Ansible python3
ansible-playbook -i inventory.ini python3_playbook.yml --ask-vault-pass

### Ansible Webmin
ansible-playbook -i inventory.ini webmin_playbook.yml --ask-vault-pass
### Ansible Jupyterhub
ansible-playbook -i inventory.ini jupyterhub_playbook.yml --ask-vault-pass

### Ansible MariaDB
ansible-playbook -i inventory.ini docker_mariadb_playbook.yml --ask-vault-pass

### Ansible Distribuir claus
ansible-playbook -i inventory.ini ssh_key.yml

## Gestión de Usuarios
### Usuarios de sistema 
Esta tarea, se realizará con un script en python, la cual se encuentra en el respositorio de servidor de IA, en el que para poder ejecutarlo debemos ser administradores por el simple hecho de que podemos añadir,modificar,borrar y añador al grupo de superusuario como a nosotros nos plazca, por ello esta versión actual del script solo lo debe ejecutar el superusuario y debe tener una fuerte coraza para que su accesibilidad sea exclusiva.
La recien implementada version del script de gestion de usuarios permite a un usuario con privilegios limitados a su rol la funcion de crear usuarios

### Ejecución del Script
El script se ejecutará con pyhton3 ya que es el lenguaje con el que se ha realizado y se habrá instalado con anterioridad en el playbook del principio se deberá descargar y ejecutarse así **python3 gestusers.py** importante dato a tener en cuenta es tener el archivo de donde se extraen los usuarios en este caso **archivo_usuarios.csv**.
Como en el otro script se tendra en cuenta el archvio csv correspondiente y se ejecutara asi **bash users.sh archivo_usuarios.csv** 

#### Implementación de variables de entorno
Con la reciente implementación de las variables de entorno para porteger al máximo la seguridad de nuestros scripts, para ello generamos un archivo oculto .env en el que guardamos variables que deseemos cifrar.
Para ejecutar los scripts se deberán seguir los pasos detallados en el apartado de ejecución, debemos genererar un entorno virtual con python3 ejecutaremos el siguiente comando **python3 -m venv venv** y después entramos en el con el comando en el entorno con el comando **source venv/bin/activate** e instalar el paquete dotenv con este comando **pip install python-dotenv** y así ejecutamos nuestro script
 
### Usuarios BBDD
Esta tarea, se realizará con un script en python, la cual se encuentra en el respositorio de configuración, en el que para poder ejecutarlo debemos ser adminisradores por el simple hecho de que podemos añadir,modificar,borrar y añador al grupo de superusuario como a nosotros nos plazca, por ello esta versión actual del script solo lo debe ejecutar el superusuario y debe tener una fuerte coraza para que su accesibilidad sea exclusiva.
En este caso al estar situado en un contenedor de docker los scripts para generar los usuarios se generarán en el servidor físico donde esté alojado nuestro servicio docker, por que el directorio en el que se almacenan estará vinculado a este

### Ejecución de los scripts
En este caso tenemos tres scripts con lo respectan la gestión de los usuarios en la BBDD **usuaris-alta.py** que permite registrar a los usuarios como su propio nombre indica, **usuaris-modifica.py** que permite modificar los usuarios y al grupo que pertenecen, **usuaris-baixa.py** que implementa la baja de los usuarios. En esta ocasión como hablábamos en la anterior se debe ser superusuario debido a que se pueden dar permisos a usuarios no autorizados y borrar usuarios que no se deben eliminar.
Y también se debe contar con el archivo .csv que permitirá al script ejecutarse con normalidad y desarollar sus tareas

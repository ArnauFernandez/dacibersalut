# Manual usuario Proyecto DAcibersalut

## Playbooks de Ansible
### Ansible python3
ansible-playbook -i inventory.ini python3_playbook.yml

### Ansible Webmin
ansible-playbook -i inventory.ini Webmin_playbook.yml

### Ansible Jupyterhub
ansible-playbook -i inventory.ini jupyterhub_playbook.yml

### Ansible MariaDB
ansible-playbook -i inventory.ini docker_mariadb_playbook.yml

### Ansible Distribuir claus
ansible-playbook -i inventory.ini ssh_key.yml

## Gestión de Usuarios
### Usuarios de sistema 
Esta tarea, se realizará con un script en python, la cual se encuentra en el respositorio de configuración, en el que para poder ejecutarlo debemos ser adminisradores por el simple hecho de que podemos añadir,modificar,borrar y añador al grupo de superusuario como a nosotros nos plazca, por ello esta versión actual del script solo lo debe ejecutar el superusuario y debe tener una fuerte coraza para que su accesibilidad sea exclusiva.

### Ejecución del Script
El script se ejecutará con pyhton3 ya que es el lenguaje con el que se ha realizado y se habrá instalado con anterioridad en el playbook del principio se deberá descargar y ejecutarse así **python3 gestusers.py** importante dato a tener en cuenta es tener el archivo de donde se extraen los usuarios en este caso **archivo_usuarios.csv**

### Usuarios BBDD
Esta tarea, se realizará con un script en python, la cual se encuentra en el respositorio de configuración, en el que para poder ejecutarlo debemos ser adminisradores por el simple hecho de que podemos añadir,modificar,borrar y añador al grupo de superusuario como a nosotros nos plazca, por ello esta versión actual del script solo lo debe ejecutar el superusuario y debe tener una fuerte coraza para que su accesibilidad sea exclusiva.
En este caso al estar situado en un contenedor de docker los scripts para generar los usuarios se generarán en el servidor físico donde esté alojado nuestro servicio docker, por que el directorio en el que se almacenan estará vinculado a este

### Ejecución de los scripts
En este caso tenemos tres scripts con lo respectan la gestión de los usuarios en la BBDD **usuaris-alta.py** que permite registrar a los usuarios como su propio nombre indica, **usuaris-modifica.py** que permite modificar los usuarios y al grupo que pertenecen, **usuaris-baixa.py** que implementa la baja de los usuarios. En esta ocasión como hablábamos en la anterior se debe ser superusuario debido a que se pueden dar permisos a usuarios no autorizados y borrar usuarios que no se deben eliminar.
Y también se debe contar con el archivo .csv que permitirá al script ejecutarse con normalidad y desarollar sus tareas

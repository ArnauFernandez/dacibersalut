# Manual usuario Proyecto DaCiberSalut

## Playbooks de Ansible

### Requisitos previos
Para poder ejecutar los playbooks de anisble se debe tener en cuenta que debe haber una previa conexión por ssh.

Para crear el fichero vault_secrets.yml se hace con el siguinete comando:
~~~
ansible-vault create ruta_del_fichero
~~~

Para obtener la contraseña cifrada se ejecuta con el siguiente comando:
~~~
ansible-vault encrypt_string 'contrasenya' --name 'ansible_pass'
~~~

### Ansible python3
~~~
ansible-playbook -i ruta/al/archivo/inventory.ini ruta/al/archivo/python3_playbook.yml --ask-vault-pass --ask-become-pass
~~~

### Ansible Webmin
~~~
ansible-playbook -i ruta/al/archivo/inventory.ini ruta/al/archivo/webmin_playbook.yml --ask-vault-pass --ask-become-pass
~~~

### Ansible Jupyterhub
~~~
ansible-galaxy collection install community.docker
~~~

Recomendable hacer upgrade despues de instalar ansible
~~~
pip install --upgrade ansible
~~~



Antes de ejecutar el playbook se debera descargar **Imatges.zip** y hacer unzip hacia el directorio donde se encuentra el playbook.

~~~
ansible-playbook -i ruta/al/archivo/inventory.ini ruta/al/archivo/jupyterhub_playbook.yml --ask-vault-pass --ask-become-pass
~~~

### Ansible MariaDB
Antes de ejecutar el comando del ansible-playbook se debe cifrar las contraseñas en el archivo vault_secrets.yml. 
Paso 1: Crear el archivo secrets.yml utilizando ansible-vault:
~~~
ansible-vault create dacibersalut/Servidor_BBDD/Instalación_MariaDB/vault_secrets.yml 
~~~

Paso 2: Añadir las contraseñas en el archivo vault_secrets.yml de esta forma:
~~~
MYSQL_ROOT_PASSWORD: "dbpw"  
MYSQL_DATABASE: "db"  
MYSQL_USER: "dbuser"  
MYSQL_PASSWORD: "dbpw"  
DB_PASSWORD: "dbpw"
~~~

Paso 3: Despues encriptar el fichero vault_secrets.yml con la siguiente comanda:
~~~
ansible-vault encrypt ruta/al/archivo/vault_secrets.yml 
~~~

Paso 4: Añadir variables en el .env de esta forma:
~~~
MYSQL_ROOT_PASSWORD={{ MYSQL_ROOT_PASSWORD }}  
MYSQL_DATABASE={{ MYSQL_DATABASE }}  
MYSQL_USER={{ MYSQL_USER }}  
MYSQL_PASSWORD={{ MYSQL_PASSWORD }}  
  
DB_PASSWORD={{ DB_PASSWORD }}  
~~~

Paso 5: Cambiar dar permisos al vault_secrets.yml, porque en predeterminado solo tiene escritura i lectura del propio usuario que ejecuta.
~~~
sudo chmod 755 ruta/al/archivo/vault_secrets.yml
~~~

Paso 6: Ejecutar el comando ansible-playbook   
~~~
ansible-playbook -i ruta/al/archivo/inventory.ini ruta/al/archivo/docker_mariadb_playbook.yml --ask-become-pass --ask-vault-pass
~~~

### Ansible Distribuir claves
~~~
ansible-playbook -i ruta/al/archivo/inventory.ini ruta/al/archivo/ssh_key.yml --ask-become-pass --ask-vault-pass
~~~

## Gestión de Usuarios
#### Se requiere la previa instalación de python
### Usuarios de sistema 
Esta tarea, se realizará con un script en python, la cual se encuentra en el respositorio de servidor de IA, en el que para poder ejecutarlo debemos ser administradores por el simple hecho de que podemos añadir,modificar,borrar y añador al grupo de superusuario como a nosotros nos plazca, por ello esta versión actual del script solo lo debe ejecutar el superusuario y debe tener una fuerte coraza para que su accesibilidad sea exclusiva.

#### Implementación de variables de entorno
Con la reciente implementación de las variables de entorno para porteger al máximo la seguridad de nuestros scripts, para ello generamos un archivo oculto **.env** en el que guardamos variables que deseemos cifrar.
Para ejecutar los scripts se deberán seguir los pasos detallados en el apartado de ejecución, debemos genererar un entorno virtual con python3 ejecutaremos el siguiente comando **python3 -m venv venv** y después entramos en el entorno con el comando **source venv/bin/activate** e instalar el paquete dotenv con este comando **pip install python-dotenv** y así ejecutamos nuestro script

#### Archivo .env gestusers.py
~~~
CSV_FILE="archivo_usuarios.csv"
DEFAULT_PASSWORD="contraseñapordefecto"
DEFAULT_SHELL="/bin/bash"
~~~

 
### Usuarios BBDD
Esta tarea, se realizará con un script en python, la cual se encuentra en el respositorio de configuración, en el que para poder ejecutarlo debemos ser adminisradores por el simple hecho de que podemos añadir,modificar,borrar y añadir al grupo de superusuario como a nosotros nos plazca, por ello esta versión actual del script solo lo debe ejecutar el superusuario y debe tener una fuerte coraza para que su accesibilidad sea exclusiva.
En este caso al estar situado en un contenedor de docker los scripts para generar los usuarios se generarán en el servidor físico donde esté alojado nuestro servicio docker, por que el directorio en el que se almacenan estará vinculado a este

### Ejecución de los scripts
En este caso tenemos tres scripts con lo respectan la gestión de los usuarios en la BBDD **usuaris-alta.py** que permite registrar a los usuarios como su propio nombre indica, **usuaris-modifica.py** que permite modificar los usuarios y al grupo que pertenecen, **usuaris-baixa.py** que implementa la baja de los usuarios. En esta ocasión como hablábamos en la anterior se debe ser superusuario debido a que se pueden dar permisos a usuarios no autorizados y borrar usuarios que no se deben eliminar.
Y también se debe contar con el archivo .csv que permitirá al script ejecutarse con normalidad y desarollar sus tareas

## Gestión de Pacientes y Analíticas 

### Ejecución de los scripts

#### genera-carga-pacientes-fakes.py
Este script genera pacientes falsos y los carga en la base de datos

**¿Qué hace?**
- Crea datos aleatorios como nombre, apellidos, dirección, edad, telefono, alergias, etc. usando Faker.
- Se conecta a la base de datos MariaDB y añade estos pacientes a la tabla correspondiente.

**¿Cómo se ejecuta?**
Primero de todo debemos entrar en el entorno vitual con el comando **source venv/bin/activate** e instalar el paquete de Faker con el siguiente comando:
~~~
pip install Faker
~~~
Una vez descargado el paquete de faker, se ejecuta el siguiente comando para generar pacientes falsos para cargarlos en la base de datos:
~~~
python ruta/al/archivo/genera-carga-pacientes-fakes.py
~~~

#### Generar-analiticas-fake.py
Con los pacientes ya en la base de datos, el siguiente paso es generar analíticas médicas.
Para eso, se debe ejecutar el siguiente comando:
~~~
python ruta/al/archivo/Generar-analiticas.py
~~~

**¿Qué hace?**
- Asocia análisis clínicos a los pacientes existentes
- Genera datos aleatorios de pruebas de laboratorio


#### oh_laboratory.py
Finalmente, necesitamos cargar y procesar la información en el sistema de Open Hospital. Para eso, ejecutamos:
~~~
python ruta/al/archivo/oh_laboratory.py
~~~

**¿Qué hace?**
- Toma los datos de las analíticas generadas y los carga en el módulo de laboratorio de Open Hospital.
- Asegura que los registros sean visibles en la interfaz del software para su consulta y edición.
- Guarda estos valores en la base de datos para su consulta.

## Contenedores docker,como ejecutar y descargar sus servicios

### Mirth connect
~~~
docker pull nextgenhealthcare/connect:latest
~~~

~~~
docker run -d --name mirthconnect -v /home/isard/Imatges:/opt/mirth/images -p 8080:8080 -p 8443:8443 -e MIRTH_HOME=/opt/mirth --restart always nextgenhealthcare/connect:latest
~~~

#### Instalar mirth connect
Se deberá descargar el archivo de lanzador de administrador de la interfície web ejecutarlo como root con el siguiente comando **bash mirth-administrator-launcher-latest-unix** y se ejecutará el menu de instalación cuando ya se haya instalado deberemos ejecutar el lanzador con el comando **launcher** y se nos abrirá esta pestaña ![imatge](https://github.com/user-attachments/assets/1352d72d-ee7d-4f21-ac36-e2733236c397) 

y debemos indicar que parametros tenga nuestra consola de administrador.

cuando ya se hayan configurado los parametros a nuestro gusto se nos abrirá la consola de administración

![imatge](https://github.com/user-attachments/assets/c41daac9-f457-4024-b0fb-22b187142f68)

### MariaDB
~~~
docker pull mariadb:latest
~~~

~~~
docker run -d --name openhospital_db -v ohv:/var/lib/mysql -p 3306:3306 -e MYSQL_ROOT_PASSWORD=dbpw mariadb:latest
~~~

~~~
mariadb -u root -pdbpw
~~~

~~~
use oh;
~~~

### Jupyterhub
~~~
sudo docker run --privileged -v ./jupyterhub_config.py:/srv/jupyterhub/jupyterhub_config.py -v /etc/passwd:/etc/passwd -v /etc/group:/etc/group -v /home:/home -v /etc/shadow:/etc/shadow -v /home/isard/Imatges:/srv/jupyterhub/Imatges  -p 8000:8000 --name jupyter   quay.io/jupyterhub/jupyterhub
~~~

### Instalación dependencias para arrancar mirth connect en consola

### 🖥️Requisitos

Este proyecto requiere una interfaz gráfica para funcionar correctamente. Si accedes al entorno de ejecución desde una terminal remota (por ejemplo, mediante SSH), ten en cuenta lo siguiente:

### 🔁Reenvío X11 (SSH)

### Para ejecutar la aplicación gráficamente desde una sesión SSH:

#### Nos conectamos usando reenvío X11:

~~~
ssh -X usuario@servidor
~~~

#### O, si necesitamos un acceso menos restringido:

~~~
ssh -Y usuario@servidor
~~~

#### Asegurarnos de que el servidor esté configurado correctamente. Editar el archivo /etc/ssh/sshd_config y verificamos que incluya estas líneas:

~~~
X11Forwarding yes
X11UseLocalhost yes
~~~

#### Instalar xauth si aún no está presente:

~~~
sudo apt install xauth
~~~

#### Instala los paquetes necesarios para el entorno gráfico

~~~
sudo apt install xauth libgtk-3-0
~~~

#### Reinicia el servicio SSH para aplicar cambios:

~~~
sudo systemctl restart sshd

~~~

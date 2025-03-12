#!/bin/bash
# region Variables
usuario="root"
contrasenya="ciber25"
# endregion

# region Crear los contenedores del docker compose
docker-compose up -d
# endregion

# region Crear el volumen ohv
docker volume create ohv
# endregion

# region Crear i ejecutar el contenedor de docker openhospital
sudo docker run -dit --name openhospital -e MYSQL_ROOT_PASSWORD=ciber25   -v ohv:/var/lib/mysql   -p 3306:3306   mariadb:latest
# endregion

# region Entrar en el contenedor de la mariadb
docker exec -it openhospital bash
# endregion

# region Dentro del contenedor de la mariadb
# region Instalaciones necesarias
apt update
apt install unzip
apt install wget
apt install unzip
# endregion

# region Descargar zip con esquema de la base de datos
wget https://github.com/informatici/openhospital/releases/download/v1.14.2/OpenHospital-v1.14.2-multiarch-client.zip
# endregion

# region Descomprimir zip
unzip OpenHospital-v1.14.2-multiarch-client.zip
# endregion

# region agregar en el /etc/mysql/my.cnf la siguiente configuración
echo "[mysqld]
#
# Configuration to be inserted below last row of [mysqld] section
#
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION
max_allowed_packet = 4M # must match the value used on clients for DICOM_SIZE
skip-external-locking
key_buffer_size = 16M
thread_cache_size = 64
lower_case_table_names = 1
table_open_cache = 64
tmp_table_size = 16M
read_buffer_size = 256K
read_rnd_buffer_size = 512K
join_buffer_size = 2M
sort_buffer_size = 2M
myisam_sort_buffer_size = 8M
bind-address = 0.0.0.0

[mysqldump]
quick
max_allowed_packet = 16M

[mysql]
no-auto-rehash

[isamchk]
key_buffer = 16M
sort_buffer_size = 16M
read_buffer = 2M
write_buffer = 2M

[myisamchk]
key_buffer = 16M
sort_buffer_size = 16M
read_buffer = 2M
write_buffer = 2M" >> /etc/mysql/my.cnf
# endregion

# region Entrar en la base de datos con contraseña
cd OH/sql
mysql -u $usuario -p$contrasenya
# endregion

# region Crear base de datos
CREATE DATABASE oh;
CREATE USER 'isf'@'localhost' IDENTIFIED BY 'ciber25';
CREATE USER 'isf'@'%' IDENTIFIED BY 'ciber25';
GRANT ALL PRIVILEGES ON oh.* TO 'isf'@'localhost';
GRANT ALL PRIVILEGES ON oh.* TO 'isf'@'%';
FLUSH PRIVILEGES;

use oh; source create_all_en.sql

quit;
# endregion

# region I per ultim, posar en marxa el servei dins i el docker en si
service mysql start
docker restart openhospital
docker start openhospital
# endregion
# endregion





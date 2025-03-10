#!/bin/bash

# Variables
usuario="root"
password="root"

# Descargar zip con esquema de la base de datos
wget https://github.com/informatici/openhospital/releases/download/v1.14.2/OpenHospital-v1.14.2-multiarch-client.zip

# Descomprimir zip
unzip OpenHospital-v1.14.2-multiarch-client.zip

# Copiar esquema a la base de datos de docker
docker cp OpenHospital-v1.14.2-multiarch-client/OpenHospital-v1.14.2.sql mariadb:/OpenHospital-v1.14.2.sql

# Entrar en el contenedor de la mariadb
docker exec -it mariadb bash

# Ir a la carpeta donde se ha copiado el esquema
cd OpOpenHospital-v1.14.2-multiarch-client/sql

# Entrar en la base de datos con contraseña
mariadb -u $usuario -p$password

# Crear base de datos
CREATE DATABASE oh CHARACTER SET utf8;
CREATE USER 'isf'@'localhost' IDENTIFIED BY 'isf123';
CREATE USER 'isf'@'%' IDENTIFIED BY 'isf123';
GRANT ALL PRIVILEGES ON oh.* TO 'isf'@'localhost';
GRANT ALL PRIVILEGES ON oh.* TO 'isf'@'%';
FLUSH PRIVILEGES;

use oh; source create_all_en.sql


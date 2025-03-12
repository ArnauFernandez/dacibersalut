#!/bin/bash

# Variables
usuario="root"
password="root"

# Ir a la carpeta donde se ha copiado el esquema
cd /opt/openhospital/OpOpenHospital-v1.14.2-multiarch-client/sql

# Entrar en la base de datos con contraseña
mariadb -u $usuario -p$password

# Crear base de datos
CREATE DATABASE oh CHARACTER SET utf8;
CREATE USER 'isf'@'localhost' IDENTIFIED BY 'isf123';
CREATE USER 'isf'@'%' IDENTIFIED BY 'isf123';
GRANT ALL PRIVILEGES ON oh.* TO 'isf'@'localhost';
GRANT ALL PRIVILEGES ON oh.* TO 'isf'@'%';
FLUSH PRIVILEGES;

# Cargar esquema en la base de datos
use oh; source create_all_en.sql


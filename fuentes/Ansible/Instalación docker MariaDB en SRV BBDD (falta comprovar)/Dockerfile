# Utilitzar la imatge oficial de MariaDB
FROM mariadb:latest

# Variables d'entorn per a MariaDB
ENV MYSQL_ROOT_PASSWORD=ciber25
ENV MYSQL_DATABASE=oh
ENV MYSQL_USER=isf
ENV MYSQL_PASSWORD=isf123

# Actualitzar el sistema i instal·lar paquets necessaris
RUN apt update && apt install -y nano wget unzip

# Descarregar i descomprimir OpenHospital
RUN wget https://github.com/informatici/openhospital/releases/download/v1.14.2/OpenHospital-v1.14.2-multiarch-client.zip \
    && unzip OpenHospital-v1.14.2-multiarch-client.zip -d /opt/openhospital \
    && rm OpenHospital-v1.14.2-multiarch-client.zip

# Afegir la configuració de MariaDB directament al fitxer de configuració
RUN echo "[mysqld] \
sql_mode=STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_AUTO_CREATE_USER,NO_ENGINE_SUBSTITUTION \
max_allowed_packet=4M \
skip-external-locking \
key_buffer_size=16M \
thread_cache_size=64 \
lower_case_table_names=1 \
table_open_cache=64 \
tmp_table_size=16M \
read_buffer_size=256K \
read_rnd_buffer_size=512K \
join_buffer_size=2M \
sort_buffer_size=2M \
myisam_sort_buffer_size=8M \
bind-address=0.0.0.0 \
\
[mysqldump] \
quick \
max_allowed_packet=16M \
\
[mysql] \
no-auto-rehash \
\
[isamchk] \
key_buffer=16M \
sort_buffer_size=16M \
read_buffer=2M \
write_buffer=2M \
\
[myisamchk] \
key_buffer=16M \
sort_buffer_size=16M \
read_buffer=2M \
write_buffer=2M" > /etc/mysql/my.cnf

# Crear un script d'inicialització SQL dins del contenidor
RUN echo "CREATE DATABASE IF NOT EXISTS oh; \
CREATE USER 'isf'@'localhost' IDENTIFIED BY 'isf123'; \
CREATE USER 'isf'@'%' IDENTIFIED BY 'isf123'; \
GRANT ALL PRIVILEGES ON oh.* TO 'isf'@'localhost'; \
GRANT ALL PRIVILEGES ON oh.* TO 'isf'@'%'; \
FLUSH PRIVILEGES; \
USE oh; \
SOURCE /opt/openhospital/OH/sql/create_all_en.sql; \
SET PASSWORD FOR 'isf'@'%' = PASSWORD('ciber25'); \
FLUSH PRIVILEGES;" > /docker-entrypoint-initdb.d/init.sql

# Exposar el port de MariaDB
EXPOSE 3306

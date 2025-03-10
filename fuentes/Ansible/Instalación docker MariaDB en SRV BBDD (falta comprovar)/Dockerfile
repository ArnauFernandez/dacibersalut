# Imatge base de MariaDB
FROM mariadb:latest

# Definir variables d'entorn per a la configuració inicial
ENV MYSQL_ROOT_PASSWORD=root
ENV MYSQL_DATABASE=oh
ENV MYSQL_USER=isf
ENV MYSQL_PASSWORD=isf123

# Copiar un fitxer de configuració personalitzat (si cal)
COPY my.cnf /etc/mysql/my.cnf

# Exposar el port 3306 per connexions externes
EXPOSE 3306

# Llançar MariaDB
CMD ["mysqld"]

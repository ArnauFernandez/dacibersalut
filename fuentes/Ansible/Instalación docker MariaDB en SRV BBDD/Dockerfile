# Imatge base de MariaDB
FROM mariadb:latest

# Definir variables d'entorn per a la configuració inicial
ENV MYSQL_ROOT_PASSWORD=SuperSecretPassword
ENV MYSQL_DATABASE=prova_db
ENV MYSQL_USER=user
ENV MYSQL_PASSWORD=password

# Copiar un fitxer de configuració personalitzat (si cal)
COPY my.cnf /etc/mysql/my.cnf

# Exposar el port 3306 per connexions externes
EXPOSE 3306

# Llançar MariaDB
CMD ["mysqld"]

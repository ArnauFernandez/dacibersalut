FROM php:apache

# Instalar extensiones necesarias de PHP
RUN docker-php-ext-install mysqli pdo pdo_mysql && \
    a2enmod rewrite ssl

# Copiar archivos de configuración
COPY ./conf/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./ssl/server.crt /etc/apache2/ssl/server.crt
COPY ./ssl/server.key /etc/apache2/ssl/server.key

# Copiar archivos web (tu aplicación)
COPY ./www/ /var/www/html/

# Exponer puertos
EXPOSE 80 443

CMD ["apache2-foreground"]


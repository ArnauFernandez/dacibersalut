FROM php:apache

# Instalar extensiones necesarias de PHP
RUN docker-php-ext-install mysqli pdo pdo_mysql && \
    a2enmod rewrite ssl

# Copiar archivos de configuración
COPY ./conf/000-default.conf /etc/apache2/sites-available/000-default.conf
COPY ./ssl/dcs.crt /etc/apache2/ssl/dcs.crt
COPY ./ssl/dcs.key /etc/apache2/ssl/dcs.key

# Copiar archivos web (tu aplicación)
COPY ./www/ /var/www/html/

# Exponer puertos
EXPOSE 80 443

CMD ["apache2-foreground"]


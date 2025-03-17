Instalación de Webmin

Paso 1: Descargar e instalar la clave GPG de Webmin

Abre una terminal y ejecuta el siguiente comando para descargar e instalar la clave GPG de Webmin:

wget -q http://www.webmin.com/jcameron-key.asc -O- | sudo apt-key add -

Paso 2: Agregar el repositorio de Webmin

Ejecuta el siguiente comando para agregar el repositorio de Webmin al archivo de fuentes de APT:

sudo sh -c 'echo "deb https://download.webmin.com/download/repository sarge contrib" >> /etc/apt/sources.list'

Paso 3: Actualizar los repositorios

Después de agregar el repositorio, actualiza la lista de paquetes ejecutando:

sudo apt-get update

Paso 4: Instalar Webmin

Una vez agregado el repositorio, instala Webmin con el siguiente comando:

sudo apt-get install webmin

Este comando descargará e instalará todas las dependencias necesarias, configurando automáticamente el servidor web y los servicios requeridos para su correcto funcionamiento.

Acceso a Webmin

Una vez completada la instalación, puedes acceder a Webmin desde un navegador web utilizando la siguiente URL:

https://localhost:10000/

Si accedes desde otra máquina dentro de la misma red, reemplaza localhost por la dirección IP del servidor donde se ha instalado Webmin.

# Manual usuario Proyecto DAcibersalut

## Playbooks de Ansible
### Ansible python3
ansible-playbook -i inventoty.ini python3_playbook.yml

### Ansible Webmin
ansible-playbook -i inventari.ini Webmin_playbook.yml

## Gestion de Usuarios
### Usuarios de sistema 
Esta tarea, se realizará con un script en python, la cual se encuentra en el respositorio de configuración, en el que para poder ejecutarlo debemos ser adminisradores por el simple hecho de que podemos añadir,modificar,borrar y añador al grupo de superusuario como a nosotros nos plazca, por ello esta versión actual del script solo lo debe ejecutar el superusuario y debe tener una fuerte coraza para que su accesibilidad sea exclusiva.
### Ejecución del Script
El script se ejecutará con pyhton3 ya que es el lenguaje con el que se ha realizado y se habrá instalado con anterioridad en el playbook del principio se deberá descargar y ejecutarse así **_ python3 gestusers.py_**

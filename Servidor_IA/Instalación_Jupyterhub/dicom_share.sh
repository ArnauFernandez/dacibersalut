#!/bin/bash

DICOM_DIR="/var/Images/IMAGENES"
LINK="$HOME/Images"

if id -nG | grep -qw "jupyter"; then
    if [ ! -L "$LINK" ]; then
        ln -s "$DICOM_DIR" "$LINK"
    fi
fi

#Es posa en /etc/profile.d/ i mostra l'enllaç símbolic si l'usuari entra en la seva consola

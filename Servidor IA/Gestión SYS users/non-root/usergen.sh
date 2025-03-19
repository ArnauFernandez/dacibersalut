#!/bin/bash

# Verificar si se proporcionó un archivo CSV
if [ -z "$1" ]; then
    echo "Uso: $0 archivo.csv"
    exit 1
fi

CSV_FILE="$1"

# Verificar si el archivo existe
if [ ! -f "$CSV_FILE" ]; then
    echo "El archivo '$CSV_FILE' no existe."
    exit 1
fi

# Leer el archivo CSV y crear usuarios
while IFS="," read -r username password; do
    # Omitir líneas vacías o encabezados
    if [ -z "$username" ] || [ "$username" == "usuario" ]; then
        continue
    fi

    # Verificar si el usuario ya existe
    if id "$username" &>/dev/null; then
        echo "El usuario '$username' ya existe."
        continue
    fi

    # Si la contraseña está vacía, generar una aleatoria
    if [ -z "$password" ]; then
        password=$(openssl rand -base64 12)
        echo "Se generó la siguiente contraseña para '$username': $password"
    fi

    # Crear el usuario con la contraseña
    sudo useradd -m -s /bin/bash "$username"
    echo "$username:$password" | sudo chpasswd

    echo "Usuario '$username' creado con éxito."
done < "$CSV_FILE"

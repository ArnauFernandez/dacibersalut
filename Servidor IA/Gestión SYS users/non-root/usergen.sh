#!/bin/bash

# Verificar si se proporcionó un archivo CSV
if [ -z "$1" ]; then
    echo "Uso: $0 archivo.csv"
    exit 1
fi

CSV_FILE="$1"
CREDENCIALES_FILE="credenciales.txt"

# Verificar si el archivo existe
if [ ! -f "$CSV_FILE" ]; then
    echo "El archivo '$CSV_FILE' no existe."
    exit 1
fi

# Limpiar archivo de credenciales anterior
> "$CREDENCIALES_FILE"

# Leer el archivo CSV y crear usuarios
while IFS="," read -r username; do
    # Omitir líneas vacías o encabezados
    if [ -z "$username" ] || [ "$username" == "usuario" ]; then
        continue
    fi

    # Verificar si el usuario ya existe
    if id "$username" &>/dev/null; then
        echo "El usuario '$username' ya existe."
        continue
    fi

    # Usar el nombre de usuario como contraseña
    password="$username"

    # Crear el usuario con la contraseña
    sudo useradd -m -s /bin/bash "$username"
    echo "$username:$password" | sudo chpasswd

    # Guardar las credenciales en el archivo
    echo "$username,$password" >> "$CREDENCIALES_FILE"

    echo "Usuario '$username' creado con éxito."
done < "$CSV_FILE"

echo "Las credenciales han sido guardadas en '$CREDENCIALES_FILE'."

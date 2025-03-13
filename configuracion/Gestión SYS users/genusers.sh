#!/bin/bash

# Función para crear un usuario
crear_usuario() {
    username=$1
    fullname=$2

    echo "El usuario $username no existe. Procediendo a crear el usuario..."
    sudo useradd -m -c "$fullname" -s /bin/bash "$username"
    if [ $? -eq 0 ]; then
        echo "Usuario $username creado exitosamente."
        while true; do
            echo "Introduce la contraseña para el usuario $username:"
            sudo passwd "$username"
            if [ $? -eq 0 ]; then
                break
            else
                echo "Error al asignar la contraseña. Intenta de nuevo."
            fi
        done
        sudo chage -d 0 "$username"
    else
        echo "Hubo un error al crear el usuario $username."
    fi
}

# Función para procesar el archivo CSV
procesar_csv() {
    echo "Introduce el archivo CSV con los usuarios para alta (action,username,fullname):"
    read CSV_FILE

    if [ ! -f "$CSV_FILE" ]; then
        echo "Error: El archivo $CSV_FILE no existe."
        return
    fi

    if [ ! -r "$CSV_FILE" ]; then
        echo "Error: No se puede leer el archivo $CSV_FILE. Verifique permisos."
        return
    fi

    while IFS=, read -r action username fullname
    do
        # Saltar la primera línea si tiene encabezados
        if [[ "$action" == "action" ]]; then
            continue
        fi

        # Verificar si los campos están vacíos
        if [[ -z "$action" || -z "$username" || -z "$fullname" ]]; then
            echo "Error: Fila con datos incompletos, omitiendo..."
            continue
        fi

        # Si la acción es 'alta' y el usuario no existe, lo creamos
        if [[ "$action" == "alta" ]]; then
            # Verificar si el usuario ya existe
            if id "$username" &>/dev/null; then
                echo "El usuario $username ya existe, no se puede crear."
            else
                crear_usuario "$username" "$fullname"
            fi
        fi
    done < "$CSV_FILE"
}

# Llamada a la función de procesamiento del CSV
procesar_csv

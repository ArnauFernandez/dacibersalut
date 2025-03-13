#!/bin/bash

# Función para eliminar un usuario
eliminar_usuario() {
    username=$1

    echo "¿Estás seguro de que deseas eliminar al usuario $username? (s/n)"
    read confirmacion
    if [[ "$confirmacion" == "s" || "$confirmacion" == "S" ]]; then
        sudo userdel -r "$username"
        echo "Usuario $username eliminado exitosamente."
    else
        echo "No se eliminó el usuario $username."
    fi
}

# Función para procesar el archivo CSV
procesar_csv() {
    echo "Introduce el archivo CSV con los usuarios para eliminar (action,username):"
    read CSV_FILE

    if [ ! -f "$CSV_FILE" ]; then
        echo "Error: El archivo $CSV_FILE no existe."
        return
    fi

    if [ ! -r "$CSV_FILE" ]; then
        echo "Error: No se puede leer el archivo $CSV_FILE. Verifique permisos."
        return
    fi

    while IFS=, read -r action username
    do
        # Saltar la primera línea si tiene encabezados
        if [[ "$action" == "action" ]]; then
            continue
        fi

        # Verificar si los campos están vacíos
        if [[ -z "$action" || -z "$username" ]]; then
            echo "Error: Fila con datos incompletos, omitiendo..."
            continue
        fi

        # Si la acción es 'eliminar' y el usuario existe, lo eliminamos
        if [[ "$action" == "eliminar" ]]; then
            # Verificar si el usuario existe
            if id "$username" &>/dev/null; then
                eliminar_usuario "$username"
            else
                echo "El usuario $username no existe. No se puede eliminar."
            fi
        fi
    done < "$CSV_FILE"
}

# Llamada a la función de procesamiento del CSV
procesar_csv

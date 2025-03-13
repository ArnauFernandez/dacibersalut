#!/bin/bash

# Función para modificar un usuario
modificar_usuario() {
    username=$1
    fullname=$2

    echo "El usuario $username ya existe. ¿Qué deseas hacer?"
    echo "1) Modificar nombre completo"
    echo "2) Modificar contraseña"
    echo "3) Modificar ambos"
    echo "4) Cancelar"

    read opcion
    case $opcion in
        1)
            echo "Introduce el nuevo nombre completo para $username:"
            read new_fullname
            sudo usermod -c "$new_fullname" "$username"
            echo "Nombre completo de $username modificado exitosamente."
            ;;
        2)
            echo "Introduce la nueva contraseña para $username:"
            sudo passwd "$username"
            echo "Contraseña de $username modificada exitosamente."
            ;;
        3)
            echo "Introduce el nuevo nombre completo para $username:"
            read new_fullname
            sudo usermod -c "$new_fullname" "$username"
            echo "Introduce la nueva contraseña para $username:"
            sudo passwd "$username"
            echo "Nombre completo y contraseña de $username modificados exitosamente."
            ;;
        4)
            echo "No se realizaron cambios en el usuario $username."
            ;;
        *)
            echo "Opción no válida. No se realizaron cambios."
            ;;
    esac
}

# Función para procesar el archivo CSV
procesar_csv() {
    echo "Introduce el archivo CSV con los usuarios para modificar (action,username,fullname):"
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

        # Si la acción es 'modificar' y el usuario existe, lo modificamos
        if [[ "$action" == "modificar" ]]; then
            # Verificar si el usuario existe
            if id "$username" &>/dev/null; then
                modificar_usuario "$username" "$fullname"
            else
                echo "El usuario $username no existe. No se puede modificar."
            fi
        fi
    done < "$CSV_FILE"
}

# Llamada a la función de procesamiento del CSV
procesar_csv

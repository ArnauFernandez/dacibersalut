#!/usr/bin/env python3
import os
import pwd
import subprocess
import crypt
from dotenv import load_dotenv

# Cargar variables de entorno desde el archivo .env
load_dotenv()

DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD")
JUPYTER_GROUP = "jupyter"

# Verificar si el grupo jupyter existe, si no, crearlo
def ensure_group_exists(group_name):
    try:
        subprocess.run(['getent', 'group', group_name], check=True)
    except subprocess.CalledProcessError:
        subprocess.run(['groupadd', group_name])
        print(f"✅ Grupo '{group_name}' creado correctamente.")

def procesar_csv(csv_file):
    if not os.path.isfile(csv_file):
        print(f"❌ Error: El archivo {csv_file} no existe.")
        return

    ensure_group_exists(JUPYTER_GROUP)

    with open(csv_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith('username'):
            continue
        username, fullname = line.split(',')

        try:
            pwd.getpwnam(username)
            user_exists = True
        except KeyError:
            user_exists = False

        if user_exists:
            print(f"⚠️ El usuario {username} ya existe.")
            while True:
                user_choice = input(f"🔹 ¿Qué deseas hacer con {username}?\n   1) Modificar\n   2) Eliminar\n   3) Omitir\nSelecciona una opción (1-3): ")

                if user_choice == "1":
                    subprocess.run(['usermod', '-c', fullname, '-s', '/bin/bash', username])
                    print(f"✅ Usuario {username} modificado correctamente.")

                    # Cifrar la nueva contraseña
                    encrypted_password = crypt.crypt(DEFAULT_PASSWORD, crypt.mksalt(crypt.METHOD_SHA512))
                    subprocess.run(['usermod', '--password', encrypted_password, username])
                    print(f"✅ Contraseña de {username} restablecida.")

                    group_choice = input(f"¿Deseas añadir a {username} al grupo sudo o jupyter? (s/j/n): ")
                    if group_choice.lower() == 's':
                        subprocess.run(['usermod', '-aG', 'sudo', username])
                        print(f"✅ Usuario {username} añadido al grupo sudo.")
                    elif group_choice.lower() == 'j':
                        subprocess.run(['usermod', '-aG', JUPYTER_GROUP, username])
                        print(f"✅ Usuario {username} añadido al grupo jupyter.")
                    break
                elif user_choice == "2":
                    subprocess.run(['userdel', '-r', username])
                    print(f"✅ Usuario {username} eliminado correctamente.")
                    break
                elif user_choice == "3":
                    print(f"⏭️ No se realizaron cambios en {username}.")
                    break
                else:
                    print("❌ Opción no válida. Inténtalo de nuevo.")
        else:
            confirm = input(f"➕ El usuario {username} no existe. ¿Deseas crearlo? (s/n): ")
            if confirm.lower() == 's':
                subprocess.run(['useradd', '-m', '-c', fullname, '-s', '/bin/bash', username])
                print(f"✅ Usuario {username} creado correctamente.")

                # Cifrar la contraseña antes de asignarla
                encrypted_password = crypt.crypt(DEFAULT_PASSWORD, crypt.mksalt(crypt.METHOD_SHA512))
                subprocess.run(['usermod', '--password', encrypted_password, username])
                print(f"✅ Contraseña de {username} establecida a la predeterminada.")

                group_choice = input(f"¿Deseas añadir a {username} al grupo sudo o jupyter? (s/j/n): ")
                if group_choice.lower() == 's':
                    subprocess.run(['usermod', '-aG', 'sudo', username])
                    print(f"✅ Usuario {username} añadido al grupo sudo.")
                elif group_choice.lower() == 'j':
                    subprocess.run(['usermod', '-aG', JUPYTER_GROUP, username])
                    print(f"✅ Usuario {username} añadido al grupo jupyter.")
            else:
                print(f"⏭️ No se creó el usuario {username}.")

def mostrar_menu():
    while True:
        print("-------------------- Menú de Gestión de Usuarios --------------------")
        print("1) Procesar archivo CSV para dar de alta, modificar o eliminar usuarios")
        print("2) Salir")
        print("--------------------------------------------------------------------")
        opcion = input("Selecciona una opción: ")

        if opcion == "1":
            csv_file = input("Introduce el archivo CSV con los usuarios (username,fullname): ")
            procesar_csv(csv_file)
        elif opcion == "2":
            print("👋 Saliendo del programa...")
            break
        else:
            print("❌ Opción no válida. Inténtalo de nuevo.")

if __name__ == "__main__":
    mostrar_menu()
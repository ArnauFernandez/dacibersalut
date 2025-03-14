import os
import pwd
import subprocess

def procesar_csv(csv_file):
    # Verificar si el archivo existe
    if not os.path.isfile(csv_file):
        print(f"❌ Error: El archivo {csv_file} no existe.")
        return

    with open(csv_file, 'r') as file:
        lines = file.readlines()

    for line in lines:
        line = line.strip()
        if not line or line.startswith('username'):  # Omitir cabeceras
            continue
        username, fullname = line.split(',')

        # Verificar si el usuario ya existe
        try:
            pwd.getpwnam(username)
            user_exists = True
        except KeyError:
            user_exists = False

        if user_exists:
            print(f"⚠️ El usuario {username} ya existe.")
            while True:
                print(f"🔹 ¿Qué deseas hacer con {username}?")
                print("   1) Modificar")
                print("   2) Eliminar")
                print("   3) Omitir")
                user_choice = input("Selecciona una opción (1-3): ")

                if user_choice == "1":
                    # Modificar el usuario
                    subprocess.run(['usermod', '-c', fullname, username])
                    print(f"✅ Usuario {username} modificado correctamente.")
                    break
                elif user_choice == "2":
                    # Eliminar el usuario
                    subprocess.run(['userdel', '-r', username])
                    print(f"✅ Usuario {username} eliminado correctamente.")
                    break
                elif user_choice == "3":
                    print(f"⏭️ No se realizaron cambios en {username}.")
                    brea
                else:
                    print("❌ Opción no válida. Inténtalo de nuevo.")
        else:
            print(f"➕ El usuario {username} no existe.")
            confirm = input(f"¿Deseas crear el usuario {username}? (s/n): ")
            if confirm.lower() == 's':
                subprocess.run(['useradd', '-m', '-c', fullname, username])
                print(f"✅ Usuario {username} creado correctamente.")
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

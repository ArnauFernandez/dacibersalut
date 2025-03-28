import os
import pwd
import subprocess
import csv
from dotenv import load_dotenv

# Cargar las variables de entorno desde un archivo .env si está presente
load_dotenv()

# Definir las variables de entorno
CSV_FILE = os.getenv("CSV_FILE")
DEFAULT_PASSWORD = os.getenv("DEFAULT_PASSWORD")
DEFAULT_SHELL = os.getenv("DEFAULT_SHELL")

def user_exists(username):
    """Verifica si un usuario existe en el sistema."""
    try:
        pwd.getpwnam(username)
        return True
    except KeyError:
        return False

def group_exists(groupname):
    """Verifica si un grupo existe en el sistema."""
    try:
        subprocess.run(["getent", "group", groupname], check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        return True
    except subprocess.CalledProcessError:
        return False

def create_user(username, fullname, group, action):
    """Ejecuta la acción correspondiente (crear, modificar o eliminar un usuario)."""

    if action == "create":
        if user_exists(username):
            print(f"⚠️ Usuario {username} ya existe, omitiendo creación.")
            return

        # Verificar si el grupo existe; si no, crearlo
        if not group_exists(group):
            subprocess.run(["groupadd", group])
            print(f"✅ Grupo '{group}' creado.")

        # Usar '-g' si el grupo es igual al usuario, '-G' en caso contrario
        group_flag = '-g' if group == username else '-G'

        try:
            subprocess.run(["useradd", "-m", "-c", fullname, "-s", DEFAULT_SHELL, group_flag, group, username], check=True)
            subprocess.run(["bash", "-c", f"echo '{username}:{DEFAULT_PASSWORD}' | chpasswd"], check=True)
            print(f"✅ Usuario {username} creado y agregado al grupo {group}.")
        except subprocess.CalledProcessError as e:
            print(f"❌ Error al crear el usuario {username}: {e}")

    elif action == "modify":
        if user_exists(username):
            try:
                subprocess.run(["usermod", "-c", fullname, "-s", DEFAULT_SHELL, "-G", group, username], check=True)
                print(f"✅ Usuario {username} modificado con éxito.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error al modificar el usuario {username}: {e}")
        else:
            print(f"⚠️ No se puede modificar {username}, el usuario no existe.")

    elif action == "delete":
        if user_exists(username):
            try:
                subprocess.run(["userdel", "-r", username], check=True)
                print(f"✅ Usuario {username} eliminado correctamente.")
            except subprocess.CalledProcessError as e:
                print(f"❌ Error al eliminar el usuario {username}: {e}")
        else:
            print(f"⚠️ No se puede eliminar {username}, el usuario no existe.")

    else:
        print(f"❌ Acción desconocida '{action}' para el usuario {username}.")

def process_csv(file_path):
    """Procesa el archivo CSV y ejecuta las acciones de usuario."""
    if not os.path.isfile(file_path):
        print(f"❌ Error: El archivo {file_path} no existe.")
        return

    with open(file_path, "r") as file:
        reader = csv.DictReader(file)
        for row in reader:
            create_user(row["username"], row["fullname"], row["group"], row["action"])

if __name__ == "__main__":
    process_csv(CSV_FILE)
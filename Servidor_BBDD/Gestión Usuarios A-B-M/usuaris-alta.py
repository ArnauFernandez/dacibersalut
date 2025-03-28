import csv
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar variables de entorno desde el archivo .env
load_dotenv()

# Configuració de la connexió a la base de dades amb les variables d'entorn
config = {
    'user': os.getenv('DB_USER'),  # Obtenir l'usuari de la base de dades des de .env
    'password': os.getenv('DB_PASSWORD'),  # Obtenir la contrasenya de la base de dades des de .env
    'host': os.getenv('DB_HOST'),  # Obtenir l'host de la base de dades des de .env
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtenir el port de la base de dades des de .env
    'database': os.getenv('DB_NAME'),  # Obtenir el nom de la base de dades des de .env
    'raise_on_warnings': True
}

PASSWORD_HASH = os.getenv('PASSWORD_HASH')  # Obtenir el hash de la contrasenya des de .env

# Funció per comprovar si un usuari ja existeix
def usuari_existeix(cursor, nom):
    query = "SELECT COUNT(*) FROM oh_user WHERE US_ID_A = %s"
    cursor.execute(query, (nom,))
    return cursor.fetchone()[0] > 0

# Funció per crear l'usuari 'script' si no existeix
def crear_usuari_script(cursor):
    if not usuari_existeix(cursor, 'script'):
        query = """
        INSERT INTO oh_user (US_ID_A, US_UG_ID_A, US_DESC, US_PASSWD, US_CREATED_BY, US_CREATED_DATE)
        VALUES ('script', 'admin', 'Usuari per a creació automàtica', %s, 'script', NOW())
        """
        cursor.execute(query, (PASSWORD_HASH,))
        print("Usuari 'script' creat correctament.")

# Funció per inserir un usuari
def inserir_usuari(cursor, nom, grup, descripcio):
    query = """
    INSERT INTO oh_user (US_ID_A, US_UG_ID_A, US_DESC, US_PASSWD, US_CREATED_BY, US_CREATED_DATE)
    VALUES (%s, %s, %s, %s, 'script', NOW())
    """
    cursor.execute(query, (nom, grup, descripcio, PASSWORD_HASH))

# Llegir el fitxer CSV i inserir usuaris
def llegir_csv_i_inserir_usuaris(csv_file):
    try:
        # Connexió a la base de dades
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Crear l'usuari 'script' si no existeix
        crear_usuari_script(cursor)

        # Llegir el fitxer CSV
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                nom = row['nom']
                grup = row['grup']
                descripcio = row['descripcio']

                # Comprovar si l'usuari ja existeix
                if not usuari_existeix(cursor, nom):
                    inserir_usuari(cursor, nom, grup, descripcio)
                    print(f"Usuari {nom} inserit correctament.")
                else:
                    print(f"L'usuari {nom} ja existeix i s'ha omès.")

        # Confirmar els canvis a la base de dades
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        # Tancar la connexió
        if conn.is_connected():
            cursor.close()
            conn.close()

# Executar el script
if __name__ == "__main__":
    csv_file = 'usuaris-alta.csv'  # Camí al fitxer CSV
    llegir_csv_i_inserir_usuaris(csv_file)

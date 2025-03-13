import csv
import mysql.connector
from mysql.connector import Error

# Configuració de la connexió a la base de dades
config = {
    'user': 'root',  # Substituïu pel vostre usuari de MariaDB
    'password': 'ciber25',  # Substituïu per la vostra contrasenya de MariaDB
    'host': 'localhost',  # O la IP del contenidor Docker
    'port': 3306,  # Port exposat del contenidor
    'database': 'oh',  # Nom de la base de dades
    'raise_on_warnings': True
}

# Funció per comprovar si un usuari ja existeix
def usuari_existeix(cursor, nom):
    query = "SELECT COUNT(*) FROM oh_user WHERE US_ID_A = %s"
    cursor.execute(query, (nom,))
    return cursor.fetchone()[0] > 0

# Funció per crear l'usuari 'script' si no existeix
def crear_usuari_script(cursor):
    if not usuari_existeix(cursor, 'script'):
        query = """
        INSERT INTO oh_user (US_ID_A, US_UG_ID_A, US_DESC, US_CREATED_BY, US_CREATED_DATE)
        VALUES ('script', 'admin', 'Usuari per a creació automàtica', 'script', NOW())
        """
        cursor.execute(query)
        print("Usuari 'script' creat correctament.")

# Funció per inserir un usuari
def inserir_usuari(cursor, nom, grup, descripcio):
    query = """
    INSERT INTO oh_user (US_ID_A, US_UG_ID_A, US_DESC, US_CREATED_BY, US_CREATED_DATE)
    VALUES (%s, %s, %s, 'script', NOW())
    """
    cursor.execute(query, (nom, grup, descripcio))

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

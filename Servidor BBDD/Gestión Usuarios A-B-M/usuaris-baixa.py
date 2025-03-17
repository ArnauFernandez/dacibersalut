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

# Funció per comprovar si un usuari existeix
def usuari_existeix(cursor, nom):
    query = "SELECT COUNT(*) FROM oh_user WHERE US_ID_A = %s"
    cursor.execute(query, (nom,))
    return cursor.fetchone()[0] > 0

# Funció per eliminar un usuari
def eliminar_usuari(cursor, nom):
    query = "DELETE FROM oh_user WHERE US_ID_A = %s"
    cursor.execute(query, (nom,))
    print(f"Usuari {nom} eliminat correctament.")

# Llegir el fitxer CSV i eliminar usuaris
def llegir_csv_i_eliminar_usuaris(csv_file):
    try:
        # Connexió a la base de dades
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Llegir el fitxer CSV
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                nom = row['nom']

                # Comprovar si l'usuari existeix
                if usuari_existeix(cursor, nom):
                    eliminar_usuari(cursor, nom)
                else:
                    print(f"L'usuari {nom} no existeix i s'ha omès.")

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
    csv_file = 'usuaris-baixa.csv'  # Camí al fitxer CSV
    llegir_csv_i_eliminar_usuaris(csv_file)

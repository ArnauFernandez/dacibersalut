import csv
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Carregar variables d'entorn des del fitxer .env
load_dotenv()

# Configuració de la connexió a la base de dades amb les variables d'entorn
config = {
    'user': os.getenv('DB_USER'),  # Obtenir l'usuari de la base de dades des de .env
    'password': os.getenv('DB_PASSWORD'),  # Obtenir la contrasenya de la base de dades des de .env
    'host': os.getenv('DB_HOST'),  # Obtenir l'host de la base de dades des de .env
    'port': int(os.getenv('DB_PORT', 3306)),  # Obtenir el port de la base de dades des de .env
    'database': os.getenv('DB_NAME'),  # Obtenir el nom de la base de dades des de .env
}

# Funció per verificar si el pacient existeix a la base de dades
def pacient_existeix(cursor, pacient_name):
    cursor.execute("SELECT COUNT(*) FROM oh_patient WHERE PAT_NAME = %s", (pacient_name,))
    result = cursor.fetchone()
    return result[0] > 0

# Funció per llegir el CSV i inserir pacients
def llegir_csv_i_inserir_pacients(csv_file):
    try:
        # Connexió a la base de dades
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Obrir el fitxer CSV
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)

            for pacient in reader:
                # Comprovar si el pacient ja existeix
                if not pacient_existeix(cursor, pacient['PAT_NAME']):
                    # Convertir els valors buits a NULL per a les columnes d'enters (com PAT_PROFILE_PHOTO_ID)
                    if pacient['PAT_PROFILE_PHOTO_ID'] == '':
                        pacient['PAT_PROFILE_PHOTO_ID'] = None  # NULL per MySQL

                    # Si no existeix, inserir el nou pacient (sense PAT_ID)
                    insert_query = """
                        INSERT INTO oh_patient (PAT_FNAME, PAT_SNAME, PAT_NAME, PAT_BDATE, PAT_AGE, 
                                                 PAT_SEX, PAT_ADDR, PAT_CITY, PAT_NEXT_KIN, PAT_TELE, 
                                                 PAT_MOTH_NAME, PAT_MOTH, PAT_FATH_NAME, PAT_FATH, 
                                                 PAT_LEDU, PAT_ESTA, PAT_PTOGE, PAT_NOTE, PAT_DELETED, 
                                                 PAT_LOCK, PAT_BTYPE, PAT_TAXCODE, PAT_TIMESTAMP, 
                                                 PAT_CREATED_BY, PAT_CREATED_DATE, PAT_LAST_MODIFIED_BY, 
                                                 PAT_LAST_MODIFIED_DATE, PAT_ACTIVE, PAT_PROFESSION, 
                                                 PAT_MAR_STAT, PAT_PROFILE_PHOTO_ID, PAT_ALLERGIES, 
                                                 PAT_ANAMNESIS)
                        VALUES (%(PAT_FNAME)s, %(PAT_SNAME)s, %(PAT_NAME)s, %(PAT_BDATE)s, %(PAT_AGE)s, 
                                %(PAT_SEX)s, %(PAT_ADDR)s, %(PAT_CITY)s, %(PAT_NEXT_KIN)s, %(PAT_TELE)s, 
                                %(PAT_MOTH_NAME)s, %(PAT_MOTH)s, %(PAT_FATH_NAME)s, %(PAT_FATH)s, 
                                %(PAT_LEDU)s, %(PAT_ESTA)s, %(PAT_PTOGE)s, %(PAT_NOTE)s, %(PAT_DELETED)s, 
                                %(PAT_LOCK)s, %(PAT_BTYPE)s, %(PAT_TAXCODE)s, %(PAT_TIMESTAMP)s, 
                                %(PAT_CREATED_BY)s, %(PAT_CREATED_DATE)s, %(PAT_LAST_MODIFIED_BY)s, 
                                %(PAT_LAST_MODIFIED_DATE)s, %(PAT_ACTIVE)s, %(PAT_PROFESSION)s, 
                                %(PAT_MAR_STAT)s, %(PAT_PROFILE_PHOTO_ID)s, %(PAT_ALLERGIES)s, 
                                %(PAT_ANAMNESIS)s)
                    """
                    cursor.execute(insert_query, pacient)
                    connection.commit()
                    print(f"Pacient {pacient['PAT_NAME']} inserit correctament.")
                else:
                    print(f"El pacient {pacient['PAT_NAME']} ja existeix a la base de dades.")
    except Error as e:
        print(f"Error en la connexió a la base de dades: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Exemple d'ús
csv_file = 'usuaris-pacients-alta.csv'
llegir_csv_i_inserir_pacients(csv_file)
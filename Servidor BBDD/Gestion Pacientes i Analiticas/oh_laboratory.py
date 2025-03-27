import csv
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Configuración de la conexión a la base de datos con las variables de entorno
config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME'),
}

# Función para verificar si el examen ya existe en la base de datos
def examen_existe(cursor, exa_id):
    cursor.execute("SELECT COUNT(*) FROM oh_laboratory WHERE LAB_EXA_ID_A = %s", (exa_id,))
    result = cursor.fetchone()
    return result[0] > 0

# Función para leer el CSV e insertar los datos en la base de datos
def leer_csv_e_insertar_laboratorios(csv_file):
    try:
        # Conexión a la base de datos
        connection = mysql.connector.connect(**config)
        cursor = connection.cursor()

        # Abrir el archivo CSV
        with open(csv_file, mode='r') as file:
            reader = csv.DictReader(file)

            for lab in reader:
                # Comprobar si el examen ya existe
                if not examen_existe(cursor, lab['LAB_EXA_ID_A']):
                    # Si no existe, insertar el nuevo examen
                    insert_query = """
                        INSERT INTO oh_laboratory (LAB_EXA_ID_A, LAB_DATE, LAB_RES, LAB_NOTE, LAB_PAT_ID, 
                                                   LAB_PAT_NAME, LAB_CROSS1, LAB_CROSS2, LAB_CROSS3, LAB_CROSS4, 
                                                   LAB_CROSS5, LAB_CROSS6, LAB_CROSS7, LAB_CROSS8, LAB_CROSS9, 
                                                   LAB_CROSS10, LAB_CROSS11, LAB_CROSS12, LAB_CROSS13, LAB_LOCK, 
                                                   LAB_AGE, LAB_SEX, LAB_MATERIAL, LAB_PAT_INOUT, LAB_CREATED_BY, 
                                                   LAB_CREATED_DATE, LAB_LAST_MODIFIED_BY, LAB_LAST_MODIFIED_DATE, 
                                                   LAB_ACTIVE, LAB_STATUS)
                        VALUES (%(LAB_EXA_ID_A)s, %(LAB_DATE)s, %(LAB_RES)s, %(LAB_NOTE)s, %(LAB_PAT_ID)s, 
                                %(LAB_PAT_NAME)s, %(LAB_CROSS1)s, %(LAB_CROSS2)s, %(LAB_CROSS3)s, %(LAB_CROSS4)s, 
                                %(LAB_CROSS5)s, %(LAB_CROSS6)s, %(LAB_CROSS7)s, %(LAB_CROSS8)s, %(LAB_CROSS9)s, 
                                %(LAB_CROSS10)s, %(LAB_CROSS11)s, %(LAB_CROSS12)s, %(LAB_CROSS13)s, %(LAB_LOCK)s, 
                                %(LAB_AGE)s, %(LAB_SEX)s, %(LAB_MATERIAL)s, %(LAB_PAT_INOUT)s, %(LAB_CREATED_BY)s, 
                                %(LAB_CREATED_DATE)s, %(LAB_LAST_MODIFIED_BY)s, %(LAB_LAST_MODIFIED_DATE)s, 
                                %(LAB_ACTIVE)s, %(LAB_STATUS)s)
                    """
                    cursor.execute(insert_query, lab)
                    connection.commit()
                    print(f"Examen {lab['LAB_EXA_ID_A']} insertado correctamente.")
                else:
                    print(f"El examen {lab['LAB_EXA_ID_A']} ya existe en la base de datos.")
    except Error as e:
        print(f"Error en la conexión a la base de datos: {e}")
    finally:
        if connection.is_connected():
            cursor.close()
            connection.close()

# Ejemplo de uso
csv_file = 'oh_laboratory.csv'  # El archivo CSV con los datos de los laboratorios
leer_csv_e_insertar_laboratorios(csv_file)
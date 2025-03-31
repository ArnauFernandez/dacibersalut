import csv
import mysql.connector
from mysql.connector import Error
from dotenv import load_dotenv
import os

# Cargar variables de entorno
load_dotenv()

# Configuración de conexión a la base de datos
config = {
    'user': os.getenv('DB_USER'),
    'password': os.getenv('DB_PASSWORD'),
    'host': os.getenv('DB_HOST'),
    'port': int(os.getenv('DB_PORT', 3306)),
    'database': os.getenv('DB_NAME')
}

def validar_fila(row):
    """Validar los datos antes de la inserción."""
    if len(row[5]) > 1:
        raise ValueError(f"Error: PAT_SEX demasiado largo ({row[5]}). Debe ser 'M' o 'F'.")
    return True

def insertar_paciente_y_consenso(cursor, row):
    """Insertar datos en oh_patient y oh_patient_consensus."""
    validar_fila(row)  # Validar fila antes de insertar

    # Inserción en oh_patient
    insert_patient_query = """
        INSERT INTO oh_patient (
            PAT_FNAME, PAT_SNAME, PAT_NAME, PAT_BDATE, PAT_AGE,
            PAT_AGETYPE, PAT_SEX, PAT_ADDR, PAT_CITY, PAT_NEXT_KIN,
            PAT_TELE, PAT_MOTH_NAME, PAT_MOTH, PAT_FATH_NAME, PAT_FATH,
            PAT_NOTE, PAT_DELETED, PAT_LOCK, PAT_BTYPE, PAT_TAXCODE,
            PAT_TIMESTAMP, PAT_CREATED_BY, PAT_CREATED_DATE,
            PAT_LAST_MODIFIED_BY, PAT_LAST_MODIFIED_DATE, PAT_ACTIVE,
            PAT_PROFESSION, PAT_MAR_STAT, PAT_PROFILE_PHOTO_ID
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                  %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_patient_query, row[:29])
    connection.commit()

    # Obtener el ID del paciente insertado
    patient_id = cursor.lastrowid

    # Inserción en oh_patient_consensus
    insert_consensus_query = """
        INSERT INTO oh_patient_consensus (
            PTC_PAT_ID, PTC_CONSENSUS, PTC_SERVICE, PTC_CREATED_BY,
            PTC_CREATED_DATE, PTC_LAST_MODIFIED_BY, PTC_LAST_MODIFIED_DATE,
            PTC_ACTIVE
        ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
    """
    cursor.execute(insert_consensus_query, (patient_id, *row[29:]))
    connection.commit()

try:
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Leer el archivo CSV
    csv_file = "usuaris-pacients-alta.csv"
    with open(csv_file, mode='r', encoding='utf-8') as file:
        reader = csv.reader(file)
        next(reader)  # Saltar encabezados

        for row in reader:
            insertar_paciente_y_consenso(cursor, row)

    print("Pacientes y consensos insertados correctamente.")

except ValueError as ve:
    print(f"Validación fallida: {ve}")
except Error as e:
    print(f"Error al conectar o insertar en la base de datos: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

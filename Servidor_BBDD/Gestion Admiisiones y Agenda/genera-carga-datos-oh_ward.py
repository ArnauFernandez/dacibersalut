from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import datetime
import csv

# Cargar variables del entorno
load_dotenv()
config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT")),
    'database': os.getenv("DB_NAME")
}

# Crear instancia de Faker
fake = Faker()

# Nombre del archivo CSV
csv_filename = "wards_data.csv"

def generate_unique_wrd_id(cursor):
    """Genera un ID único que no exista en la base de datos."""
    while True:
        wrd_id_a = fake.bothify(text="W##")  # Genera identificador único (Ej: W01, W99)
        cursor.execute("SELECT COUNT(*) FROM oh_ward WHERE WRD_ID_A = %s", (wrd_id_a,))
        if cursor.fetchone()[0] == 0:  # Si no existe en la BD, lo usamos
            return wrd_id_a

try:
    # Conectar a la base de datos
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Definir cuántos registros se desean insertar
    num_records = 5

    # Abrir archivo CSV para escritura
    with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)

        # Escribir la cabecera
        writer.writerow([
            "WRD_ID_A", "WRD_NAME", "WRD_TELE", "WRD_FAX", "WRD_EMAIL", "WRD_NBEDS",
            "WRD_NQUA_NURS", "WRD_NDOC", "WRD_IS_OPD", "WRD_IS_PHARMACY", "WRD_IS_MALE",
            "WRD_IS_FEMALE", "WRD_VISIT_DURATION", "WRD_LOCK", "WRD_CREATED_BY",
            "WRD_CREATED_DATE", "WRD_ACTIVE"
        ])

        for _ in range(num_records):
            wrd_id_a = generate_unique_wrd_id(cursor)
            wrd_name = fake.company()[:20]
            wrd_tele = fake.phone_number()[:15]
            wrd_fax = fake.phone_number()[:15]
            wrd_email = fake.company_email()[:50]
            wrd_nbeds = random.randint(5, 50)
            wrd_nqua_nurs = random.randint(1, 10)
            wrd_ndoc = random.randint(1, 5)
            wrd_is_opd = random.choice([0, 1])
            wrd_is_pharmacy = random.choice([0, 1])
            wrd_is_male = random.choice([0, 1])
            wrd_is_female = random.choice([0, 1])
            wrd_visit_duration = random.randint(15, 60)
            wrd_lock = 0
            wrd_created_by = "admin"
            wrd_created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            wrd_active = 1

            insert_query = """
                INSERT INTO oh_ward (
                    WRD_ID_A, WRD_NAME, WRD_TELE, WRD_FAX, WRD_EMAIL, WRD_NBEDS, WRD_NQUA_NURS, WRD_NDOC,
                    WRD_IS_OPD, WRD_IS_PHARMACY, WRD_IS_MALE, WRD_IS_FEMALE, WRD_VISIT_DURATION, WRD_LOCK,
                    WRD_CREATED_BY, WRD_CREATED_DATE, WRD_ACTIVE
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                wrd_id_a, wrd_name, wrd_tele, wrd_fax, wrd_email, wrd_nbeds, wrd_nqua_nurs, wrd_ndoc,
                wrd_is_opd, wrd_is_pharmacy, wrd_is_male, wrd_is_female, wrd_visit_duration, wrd_lock,
                wrd_created_by, wrd_created_date, wrd_active
            ))

            # Escribir datos en CSV
            writer.writerow([
                wrd_id_a, wrd_name, wrd_tele, wrd_fax, wrd_email, wrd_nbeds,
                wrd_nqua_nurs, wrd_ndoc, wrd_is_opd, wrd_is_pharmacy, wrd_is_male,
                wrd_is_female, wrd_visit_duration, wrd_lock, wrd_created_by,
                wrd_created_date, wrd_active
            ])

    connection.commit()
    print(f"{num_records} registros insertados en la base de datos y guardados en '{csv_filename}'.")

except Error as e:
    print(f"Error al conectar o insertar datos: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import datetime
import csv

# Cargar variables del entorno (.env)
load_dotenv()
config = {
    'user': os.getenv("DB_USER"),
    'password': os.getenv("DB_PASSWORD"),
    'host': os.getenv("DB_HOST"),
    'port': int(os.getenv("DB_PORT")),
    'database': os.getenv("DB_NAME")
}

# Crear una instancia de Faker para generar datos realistas
fake = Faker()

# Definir el nombre del archivo CSV
csv_filename = "visits_data.csv"

try:
    # Conectarse a la base de datos
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Consultar registros existentes en oh_ward y oh_patient
    cursor.execute("SELECT WRD_ID_A FROM oh_ward")
    wards = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT PAT_ID FROM oh_patient")
    patients = [row[0] for row in cursor.fetchall()]

    # Validar que existan datos esenciales
    if not wards or not patients:
        print("Error: No existen datos en oh_ward o oh_patient.")
    else:
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Escribir la cabecera
            writer.writerow([
                "VST_PAT_ID", "VST_DATE", "VST_NOTE", "VST_SMS", "VST_CREATED_BY",
                "VST_CREATED_DATE", "VST_LAST_MODIFIED_BY", "VST_LAST_MODIFIED_DATE",
                "VST_ACTIVE", "VST_WRD_ID_A", "VST_DURATION", "VST_SERVICE"
            ])

            num_visits = 10

            for _ in range(num_visits):
                vst_pat_id = random.choice(patients)
                vst_wrd_id_a = random.choice(wards)

                vst_date_obj = fake.date_time_between(start_date="-1y", end_date="now")
                vst_date = vst_date_obj.strftime("%Y-%m-%d %H:%M:%S")

                vst_note = fake.sentence(nb_words=8) if random.random() < 0.5 else None
                vst_sms = random.choice([0, 1])
                vst_created_by = "admin"
                vst_created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                vst_last_modified_by = None
                vst_last_modified_date = None
                vst_active = 1
                vst_duration = random.randint(15, 60)
                vst_service = fake.word() if random.random() < 0.7 else None

                insert_query = """
                    INSERT INTO oh_visits (
                        VST_PAT_ID, VST_DATE, VST_NOTE, VST_SMS, VST_CREATED_BY,
                        VST_CREATED_DATE, VST_LAST_MODIFIED_BY, VST_LAST_MODIFIED_DATE,
                        VST_ACTIVE, VST_WRD_ID_A, VST_DURATION, VST_SERVICE
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(insert_query, (
                    vst_pat_id, vst_date, vst_note, vst_sms, vst_created_by,
                    vst_created_date, vst_last_modified_by, vst_last_modified_date,
                    vst_active, vst_wrd_id_a, vst_duration, vst_service
                ))

                writer.writerow([
                    vst_pat_id, vst_date, vst_note, vst_sms, vst_created_by,
                    vst_created_date, vst_last_modified_by, vst_last_modified_date,
                    vst_active, vst_wrd_id_a, vst_duration, vst_service
                ])

        connection.commit()
        print(f"{num_visits} registros insertados en la base de datos y guardados en '{csv_filename}'.")

except Error as e:
    print(f"Error al conectar o insertar datos: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

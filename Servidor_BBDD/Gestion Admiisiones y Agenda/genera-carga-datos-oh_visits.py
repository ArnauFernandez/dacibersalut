from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import datetime

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

try:
    # Conectarse a la base de datos
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Consultar registros existentes en oh_ward y oh_patient
    cursor.execute("SELECT WRD_ID_A FROM oh_ward")
    wards = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT PAT_ID FROM oh_patient")
    patients = [row[0] for row in cursor.fetchall()]

    # Validamos que existan datos esenciales
    if not wards:
        print("Error: no existen datos en la tabla oh_ward.")
    elif not patients:
        print("Error: no existen datos en la tabla oh_patient.")
    else:
        num_visits = 10  # Número de registros a insertar en oh_visits

        for _ in range(num_visits):
            # Seleccionar un paciente y un ward válidos
            vst_pat_id = random.choice(patients)
            vst_wrd_id_a = random.choice(wards)

            # Generar fecha aleatoria para la visita (entre hace 1 año y ahora)
            vst_date_obj = fake.date_time_between(start_date="-1y", end_date="now")
            vst_date = vst_date_obj.strftime("%Y-%m-%d %H:%M:%S")

            # Nota de la visita (opcional)
            vst_note = fake.sentence(nb_words=8) if random.random() < 0.5 else None

            # Generar sms aleatorio (0 o 1)
            vst_sms = random.choice([0, 1])

            # Datos administrativos
            vst_created_by = "admin"
            vst_created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            vst_last_modified_by = None   # Se puede dejar en NULL
            vst_last_modified_date = None   # Se puede dejar en NULL
            vst_active = 1

            # Generar duración aleatoria de la visita (en minutos)
            vst_duration = random.randint(15, 60)

            # Servicio ofrecido (opcional)
            vst_service = fake.word() if random.random() < 0.7 else None

            insert_query = """
                INSERT INTO oh_visits (
                    VST_PAT_ID, VST_DATE, VST_NOTE, VST_SMS, VST_CREATED_BY,
                    VST_CREATED_DATE, VST_LAST_MODIFIED_BY, VST_LAST_MODIFIED_DATE,
                    VST_ACTIVE, VST_WRD_ID_A, VST_DURATION, VST_SERVICE
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_query, (
                vst_pat_id,
                vst_date,
                vst_note,
                vst_sms,
                vst_created_by,
                vst_created_date,
                vst_last_modified_by,
                vst_last_modified_date,
                vst_active,
                vst_wrd_id_a,
                vst_duration,
                vst_service
            ))

        connection.commit()
        print(f"{num_visits} registros falsos insertados en oh_visits.")

except Error as e:
    print(f"Error al conectar o insertar datos: {e}")

finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
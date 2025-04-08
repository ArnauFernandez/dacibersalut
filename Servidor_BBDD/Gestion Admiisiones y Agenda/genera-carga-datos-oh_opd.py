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

# Crear instancia de Faker para generar datos realistas
fake = Faker()

try:
    # Conectar a la base de datos
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Consultar los registros existentes en las tablas relacionadas

    # Wards
    cursor.execute("SELECT WRD_ID_A FROM oh_ward")
    wards = [row[0] for row in cursor.fetchall()]

    # Pacientes (se asume que la clave primaria es PAT_ID en oh_patient)
    cursor.execute("SELECT PAT_ID FROM oh_patient")
    patients = [row[0] for row in cursor.fetchall()]

    # Enfermedades
    cursor.execute("SELECT DIS_ID_A FROM oh_disease")
    diseases = [row[0] for row in cursor.fetchall()]

    # Visitas (si existen, se usarán para OPD_NEXT_VISIT_ID; de lo contrario se asigna NULL)
    cursor.execute("SELECT VST_ID FROM oh_visits")
    visits = [row[0] for row in cursor.fetchall()]

    # Validar que existan datos esenciales en wards, patients y diseases
    if not wards:
        print("Error: no existen datos en la tabla oh_ward.")
    elif not patients:
        print("Error: no existen datos en la tabla oh_patient.")
    elif not diseases:
        print("Error: no existen datos en la tabla oh_disease.")
    else:
        # Generar datos falsos para oh_opd
        num_opd_records = 10  # Número de registros a insertar en oh_opd

        for _ in range(num_opd_records):
            # Seleccionar un ward, paciente y diagnóstico válidos
            opd_wrd_id_a = random.choice(wards)

            # Generar fecha y hora aleatoria para OPD en el último año
            opd_date_obj = fake.date_time_between(start_date="-1y", end_date="now")
            opd_date = opd_date_obj.strftime("%Y-%m-%d %H:%M:%S")

            # Usamos el año de la fecha aleatoria para OPD_PROG_YEAR
            opd_prog_year = opd_date_obj.year

            opd_new_pat = random.choice(['Y', 'N'])
            opd_sex = random.choice(['M', 'F'])
            opd_age = random.randint(1, 99)

            opd_dis_id_a = random.choice(diseases)
            opd_dis_id_a_2 = random.choice(diseases) if random.random() < 0.5 else None
            opd_dis_id_a_3 = random.choice(diseases) if random.random() < 0.3 else None

            opd_referral_from = None  # Opcional
            opd_referral_to = None  # Opcional

            opd_note = fake.sentence(nb_words=6)[:100]
            opd_pat_id = random.choice(patients)
            opd_usr_id_a = 'admin'

            # Solo se asigna un valor si hay visitas; de lo contrario se deja en NULL
            opd_next_visit_id = random.choice(visits) if visits and random.random() < 0.4 else None

            opd_lock = 0
            opd_created_by = "admin"
            # Generar una fecha de creación aleatoria entre OPD_DATE y ahora
            opd_created_date_obj = fake.date_time_between(start_date=opd_date_obj, end_date="now")
            opd_created_date = opd_created_date_obj.strftime("%Y-%m-%d %H:%M:%S")

            opd_last_modified_by = None
            opd_last_modified_date = None
            opd_active = 1
            opd_prescription = fake.sentence(nb_words=4) if random.random() < 0.6 else None

            # Consulta de inserción para oh_opd
            insert_opd_query = """
                INSERT INTO oh_opd (
                    OPD_WRD_ID_A, OPD_DATE, OPD_NEW_PAT, OPD_PROG_YEAR, OPD_SEX, OPD_AGE,
                    OPD_DIS_ID_A, OPD_DIS_ID_A_2, OPD_DIS_ID_A_3, OPD_REFERRAL_FROM, OPD_REFERRAL_TO,
                    OPD_NOTE, OPD_PAT_ID, OPD_USR_ID_A, OPD_NEXT_VISIT_ID, OPD_LOCK, OPD_CREATED_BY,
                    OPD_CREATED_DATE, OPD_LAST_MODIFIED_BY, OPD_LAST_MODIFIED_DATE, OPD_ACTIVE, OPD_PRESCRIPTION
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """

            cursor.execute(insert_opd_query, (
                opd_wrd_id_a, opd_date, opd_new_pat, opd_prog_year, opd_sex, opd_age,
                opd_dis_id_a, opd_dis_id_a_2, opd_dis_id_a_3, opd_referral_from, opd_referral_to,
                opd_note, opd_pat_id, opd_usr_id_a, opd_next_visit_id, opd_lock, opd_created_by,
                opd_created_date, opd_last_modified_by, opd_last_modified_date, opd_active, opd_prescription
            ))
        connection.commit()
        print(f"{num_opd_records} registros falsos insertados en oh_opd.")

except Error as e:
    print(f"Error al conectar o insertar datos: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()
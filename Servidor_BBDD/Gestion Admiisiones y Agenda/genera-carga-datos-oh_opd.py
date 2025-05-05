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

# Crear instancia de Faker para generar datos realistas
fake = Faker()

# Definir el nombre del archivo CSV
csv_filename = "opd_data.csv"

try:
    # Conectar a la base de datos
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Consultar los registros existentes en las tablas relacionadas

    cursor.execute("SELECT WRD_ID_A FROM oh_ward")
    wards = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT PAT_ID FROM oh_patient")
    patients = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT DIS_ID_A FROM oh_disease")
    diseases = [row[0] for row in cursor.fetchall()]

    cursor.execute("SELECT VST_ID FROM oh_visits")
    visits = [row[0] for row in cursor.fetchall()]

    if not wards or not patients or not diseases:
        print("Error: Faltan datos en oh_ward, oh_patient o oh_disease.")
    else:
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            writer.writerow([
                "OPD_WRD_ID_A", "OPD_DATE", "OPD_NEW_PAT", "OPD_PROG_YEAR", "OPD_SEX", "OPD_AGE",
                "OPD_DIS_ID_A", "OPD_DIS_ID_A_2", "OPD_DIS_ID_A_3", "OPD_REFERRAL_FROM", "OPD_REFERRAL_TO",
                "OPD_NOTE", "OPD_PAT_ID", "OPD_USR_ID_A", "OPD_NEXT_VISIT_ID", "OPD_LOCK", "OPD_CREATED_BY",
                "OPD_CREATED_DATE", "OPD_LAST_MODIFIED_BY", "OPD_LAST_MODIFIED_DATE", "OPD_ACTIVE", "OPD_PRESCRIPTION"
            ])

            num_opd_records = 10

            for _ in range(num_opd_records):
                opd_wrd_id_a = random.choice(wards)
                opd_date_obj = fake.date_time_between(start_date="-1y", end_date="now")
                opd_date = opd_date_obj.strftime("%Y-%m-%d %H:%M:%S")
                opd_prog_year = opd_date_obj.year

                opd_new_pat = random.choice(['Y', 'N'])
                opd_sex = random.choice(['M', 'F'])
                opd_age = random.randint(1, 99)
                opd_dis_id_a = random.choice(diseases)
                opd_dis_id_a_2 = random.choice(diseases) if random.random() < 0.5 else None
                opd_dis_id_a_3 = random.choice(diseases) if random.random() < 0.3 else None

                opd_note = fake.sentence(nb_words=6)[:100]
                opd_pat_id = random.choice(patients)
                opd_usr_id_a = 'admin'
                opd_next_visit_id = random.choice(visits) if visits and random.random() < 0.4 else None

                opd_lock = 0
                opd_created_by = "admin"
                opd_created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                opd_active = 1
                opd_prescription = fake.sentence(nb_words=4) if random.random() < 0.6 else None

                insert_opd_query = """
                    INSERT INTO oh_opd (
                        OPD_WRD_ID_A, OPD_DATE, OPD_NEW_PAT, OPD_PROG_YEAR, OPD_SEX, OPD_AGE,
                        OPD_DIS_ID_A, OPD_DIS_ID_A_2, OPD_DIS_ID_A_3, OPD_REFERRAL_FROM, OPD_REFERRAL_TO,
                        OPD_NOTE, OPD_PAT_ID, OPD_USR_ID_A, OPD_NEXT_VISIT_ID, OPD_LOCK, OPD_CREATED_BY,
                        OPD_CREATED_DATE, OPD_ACTIVE, OPD_PRESCRIPTION
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(insert_opd_query, (
                    opd_wrd_id_a, opd_date, opd_new_pat, opd_prog_year, opd_sex, opd_age,
                    opd_dis_id_a, opd_dis_id_a_2, opd_dis_id_a_3, None, None,
                    opd_note, opd_pat_id, opd_usr_id_a, opd_next_visit_id, opd_lock, opd_created_by,
                    opd_created_date, opd_active, opd_prescription
                ))

                writer.writerow([
                    opd_wrd_id_a, opd_date, opd_new_pat, opd_prog_year, opd_sex, opd_age,
                    opd_dis_id_a, opd_dis_id_a_2, opd_dis_id_a_3, None, None,
                    opd_note, opd_pat_id, opd_usr_id_a, opd_next_visit_id, opd_lock, opd_created_by,
                    opd_created_date, None, None, opd_active, opd_prescription
                ])

        connection.commit()
        print(f"{num_opd_records} registros falsos insertados en oh_opd y guardados en '{csv_filename}'.")

except Error as e:
    print(f"Error al conectar o insertar datos: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

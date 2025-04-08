from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import datetime

# Cargar variables del archivo .env
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

# Número de pacientes a insertar
num_records = 300

try:
    # Conexión a la base de datos
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    for _ in range(num_records):
        # Generar datos falsos para oh_patient
        fname = fake.first_name()[:50]
        sname = fake.last_name()[:50]
        name = f"{fname} {sname}"[:100]
        bdate = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d")
        age = random.randint(18, 90)
        sex = random.choice(['M', 'F'])
        addr = fake.street_address()[:50]
        city = fake.city()[:50]
        next_kin = fake.name()[:50]
        tele = fake.phone_number()[:50]
        moth_name = fake.first_name()[:50]
        moth = random.choice(['M', 'F'])
        fath_name = fake.first_name()[:50]
        fath = random.choice(['M', 'F'])
        ledu = random.choice(['Y', 'N'])
        esta = random.choice(['Y', 'N'])
        ptoge = random.choice(['Y', 'N'])
        note = "Paciente generado automáticamente"
        deleted = 'N'
        lock = 0
        btype = random.choice(['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'])
        taxcode = fake.ssn()
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_by = 'admin'
        created_date = timestamp
        last_modified_by = 'admin'
        last_modified_date = timestamp
        active = 1
        profession = "farming"
        mar_stat = "married"
        profile_photo_id = 0
        allergies = None
        anamnesis = None

        # Insertar en la tabla oh_patient
        insert_patient_query = """
            INSERT INTO oh_patient (
                PAT_FNAME, PAT_SNAME, PAT_NAME, PAT_BDATE, PAT_AGE,
                PAT_AGETYPE, PAT_SEX, PAT_ADDR, PAT_CITY, PAT_NEXT_KIN,
                PAT_TELE, PAT_MOTH_NAME, PAT_MOTH, PAT_FATH_NAME, PAT_FATH,
                PAT_LEDU, PAT_ESTA, PAT_PTOGE, PAT_NOTE, PAT_DELETED, PAT_LOCK,
                PAT_BTYPE, PAT_TAXCODE, PAT_TIMESTAMP, PAT_CREATED_BY,
                PAT_CREATED_DATE, PAT_LAST_MODIFIED_BY, PAT_LAST_MODIFIED_DATE,
                PAT_ACTIVE, PAT_PROFESSION, PAT_MAR_STAT, PAT_PROFILE_PHOTO_ID,
                PAT_ALLERGIES, PAT_ANAMNESIS
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s,
                %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        patient_values = (
            fname, sname, name, bdate, age, "",
            sex, addr, city, next_kin, tele, moth_name, moth, fath_name, fath,
            ledu, esta, ptoge, note, deleted, lock, btype, taxcode, timestamp,
            created_by, created_date, last_modified_by, last_modified_date,
            active, profession, mar_stat, profile_photo_id, allergies, anamnesis
        )

        cursor.execute(insert_patient_query, patient_values)
        connection.commit()

        # Obtener el ID del paciente recién insertado
        patient_id = cursor.lastrowid

        # Insertar en la tabla oh_patient_consensus
        insert_consensus_query = """
            INSERT INTO oh_patient_consensus (
                PTC_PAT_ID, PTC_CONSENSUS, PTC_SERVICE, PTC_CREATED_BY,
                PTC_CREATED_DATE, PTC_LAST_MODIFIED_BY, PTC_LAST_MODIFIED_DATE, PTC_ACTIVE
            ) VALUES (
                %s, %s, %s, %s, %s, %s, %s, %s
            )
        """

        consensus_values = (
            patient_id, 0, 0, created_by, created_date, last_modified_by,
            last_modified_date, active
        )

        cursor.execute(insert_consensus_query, consensus_values)
        connection.commit()

    print(f"{num_records} pacientes y sus consensos insertados correctamente.")

except Error as e:
    print(f"Error al conectar o insertar en la base de datos: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

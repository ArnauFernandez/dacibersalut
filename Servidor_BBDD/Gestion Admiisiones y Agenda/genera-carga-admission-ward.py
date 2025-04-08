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

try:
    # Conexión a la base de datos
    connection = mysql.connector.connect(**config)
    if connection.is_connected():
        cursor = connection.cursor()

        # 1. Crear wards ficticios respetando tipos de datos
        for i in range(1, 4):  # Crear 3 wards
            ward_id = f"FW{i}"  # Asegurarse de cumplir el límite de 3 caracteres
            ward_name = fake.company()[:50]
            nbeds = random.randint(5, 50)
            nqu_nurs = random.randint(2, 10)
            ndoc = random.randint(1, 5)
            is_opd = random.choice([0, 1])
            is_pharmacy = random.choice([0, 1])
            is_male = random.choice([0, 1])
            is_female = random.choice([0, 1])
            visit_duration = random.randint(15, 60)
            created_by = "admin"
            created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            active = 1

            cursor.execute("""
                INSERT INTO oh_ward (
                    WRD_ID_A, WRD_NAME, WRD_NBEDS, WRD_NQUA_NURS, WRD_NDOC, WRD_IS_OPD, WRD_IS_PHARMACY,
                    WRD_IS_MALE, WRD_IS_FEMALE, WRD_VISIT_DURATION, WRD_CREATED_BY, WRD_CREATED_DATE, WRD_ACTIVE
                ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
            """, (ward_id, ward_name, nbeds, nqu_nurs, ndoc, is_opd, is_pharmacy, is_male, is_female, visit_duration, created_by, created_date, active))
            connection.commit()

        # 2. Crear tipos de admisión ficticios respetando tipos de datos
        for i in range(1, 4):  # Crear 3 tipos de admisión
            adm_type_id = f"FAKE{i}"  # Asegurarse de cumplir el límite de 10 caracteres
            adm_desc = fake.catch_phrase()[:50]
            created_by = "admin"
            created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            active = 1

            cursor.execute("""
                INSERT INTO oh_admissiontype (
                    ADMT_ID_A, ADMT_DESC, ADMT_CREATED_BY, ADMT_CREATED_DATE, ADMT_ACTIVE
                ) VALUES (%s, %s, %s, %s, %s)
            """, (adm_type_id, adm_desc, created_by, created_date, active))
            connection.commit()

        # 3. Insertar admisiones ficticias respetando tipos de datos
        cursor.execute("SELECT PAT_ID FROM oh_patient")
        patients = cursor.fetchall()

        for patient in patients:
            patient_id = patient[0]  # Asegurarse de que este ID sea válido
            ward_id = random.choice(['FW1', 'FW2', 'FW3'])  # Relación válida con oh_ward
            adm_type_id = random.choice(['FAKE1', 'FAKE2', 'FAKE3'])  # Relación válida con oh_admissiontype
            note = fake.text(max_nb_chars=100)[:100]  # Limitar a 100 caracteres
            created_by = "admin"
            created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
            active = 1

            try:
                cursor.execute("""
                    INSERT INTO oh_admission (
                        ADM_IN, ADM_TYPE, ADM_WRD_ID_A, ADM_PAT_ID, ADM_DATE_ADM, ADM_ADMT_ID_A_ADM, ADM_NOTE,
                        ADM_USR_ID_A, ADM_CREATED_BY, ADM_CREATED_DATE, ADM_ACTIVE
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """, (1, 'A', ward_id, patient_id, created_date, adm_type_id, note, 'admin', created_by, created_date, active))
                connection.commit()
            except Error as e:
                print(f"Error al insertar en oh_admission: {e}")

        print("Datos ficticios insertados correctamente en todas las tablas.")

except Error as e:
    print(f"Error al conectar con la base de datos: {e}")
finally:
    if 'connection' in locals() and connection.is_connected():
        cursor.close()
        connection.close()

from dotenv import load_dotenv
import os
import mysql.connector
from mysql.connector import Error
from faker import Faker
import random
from datetime import datetime
import csv

# Cargar variables de entorno
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

# Definir el nombre del archivo CSV
csv_filename = "disease_data.csv"

try:
    # Conectarse a la base de datos
    connection = mysql.connector.connect(**config)
    cursor = connection.cursor()

    # Obtener los tipos de enfermedades existentes en oh_diseasetype
    cursor.execute("SELECT DCL_ID_A FROM oh_diseasetype")
    disease_types = [row[0] for row in cursor.fetchall()]

    if not disease_types:
        print("Error: No hay tipos de enfermedad en oh_diseasetype.")
    else:
        # Abrir archivo CSV para escritura
        with open(csv_filename, mode='w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)

            # Escribir la cabecera
            writer.writerow([
                "DIS_ID_A", "DIS_DESC", "DIS_DCL_ID_A", "DIS_LOCK", "DIS_OPD_INCLUDE",
                "DIS_IPD_IN_INCLUDE", "DIS_IPD_OUT_INCLUDE", "DIS_CREATED_BY",
                "DIS_CREATED_DATE", "DIS_ACTIVE"
            ])

            # Insertar datos falsos en oh_disease y guardarlos en CSV
            num_records = 10
            for _ in range(num_records):
                dis_id_a = f"D{random.randint(1000, 9999)}"
                dis_desc = fake.sentence(nb_words=3)[:160]
                dis_dcl_id_a = random.choice(disease_types)
                dis_lock = 0
                dis_opd_include = random.choice([0, 1])
                dis_ipd_in_include = random.choice([0, 1])
                dis_ipd_out_include = random.choice([0, 1])
                dis_created_by = "admin"
                dis_created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                dis_active = 1

                insert_query = """
                    INSERT INTO oh_disease (
                        DIS_ID_A, DIS_DESC, DIS_DCL_ID_A, DIS_LOCK, DIS_OPD_INCLUDE,
                        DIS_IPD_IN_INCLUDE, DIS_IPD_OUT_INCLUDE, DIS_CREATED_BY,
                        DIS_CREATED_DATE, DIS_ACTIVE
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
                """

                cursor.execute(insert_query, (
                    dis_id_a, dis_desc, dis_dcl_id_a, dis_lock, dis_opd_include,
                    dis_ipd_in_include, dis_ipd_out_include, dis_created_by,
                    dis_created_date, dis_active
                ))

                # Escribir en el CSV
                writer.writerow([
                    dis_id_a, dis_desc, dis_dcl_id_a, dis_lock, dis_opd_include,
                    dis_ipd_in_include, dis_ipd_out_include, dis_created_by,
                    dis_created_date, dis_active
                ])

        connection.commit()
        print(f"{num_records} registros falsos insertados en oh_disease.")
        print(f"Datos guardados en '{csv_filename}'.")

except Error as e:
    print(f"Error al conectar o insertar datos en la base de datos: {e}")
finally:
    if connection.is_connected():
        cursor.close()
        connection.close()

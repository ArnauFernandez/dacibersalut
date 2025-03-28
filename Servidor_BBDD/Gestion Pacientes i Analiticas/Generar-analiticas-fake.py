import csv
from faker import Faker
import random
from datetime import datetime
import mysql.connector
from dotenv import load_dotenv
import os

# Cargar las variables de entorno desde el archivo .env
load_dotenv()

# Obtener las variables de entorno
DB_USER = os.getenv("DB_USER")
DB_PASSWORD = os.getenv("DB_PASSWORD")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Crear instancia de Faker
fake = Faker()

# Conectar a la base de datos MySQL
try:
    connection = mysql.connector.connect(
        host=DB_HOST,
        user=DB_USER,
        password=DB_PASSWORD,
        database=DB_NAME,
        port=DB_PORT
    )
    cursor = connection.cursor()

    # Consultar las ID de examen válidas
    cursor.execute("SELECT EXA_ID_A FROM oh_exam")
    valid_exa_ids = [row[0] for row in cursor.fetchall()]

    # Consultar las ID de pacientes válidas
    cursor.execute("SELECT PAT_ID FROM oh_patient")
    valid_pat_ids = [row[0] for row in cursor.fetchall()]

except mysql.connector.Error as err:
    print(f"Error en la conexión a la base de datos: {err}")
    exit(1)

# Nombre del archivo CSV
output_file = "oh_laboratory.csv"

# Número de registros
num_records = 300
records_created = 0  # Contador de registros creados

# Abrir el archivo CSV para escribir
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Escribir cabeceras al CSV
    writer.writerow([
        "LAB_EXA_ID_A", "LAB_DATE", "LAB_RES", "LAB_NOTE", "LAB_PAT_ID", "LAB_PAT_NAME",
        "LAB_CROSS1", "LAB_CROSS2", "LAB_CROSS3", "LAB_CROSS4", "LAB_CROSS5", "LAB_CROSS6",
        "LAB_CROSS7", "LAB_CROSS8", "LAB_CROSS9", "LAB_CROSS10", "LAB_CROSS11", "LAB_CROSS12",
        "LAB_CROSS13", "LAB_LOCK", "LAB_AGE", "LAB_SEX", "LAB_MATERIAL", "LAB_PAT_INOUT",
        "LAB_CREATED_BY", "LAB_CREATED_DATE", "LAB_LAST_MODIFIED_BY", "LAB_LAST_MODIFIED_DATE",
        "LAB_ACTIVE", "LAB_STATUS"
    ])

    # Generar registros
    for _ in range(num_records):
        # Verificar si la lista de EXA_ID_A está vacía
        if not valid_exa_ids:
            print("No hay más EXA_ID_A disponibles para generar registros.")
            break

        # Generar datos falsos
        exa_id_a = random.choice(valid_exa_ids)  # Seleccionar un ID válido de examen
        valid_exa_ids.remove(exa_id_a)  # Eliminar el EXA_ID_A seleccionado de la lista

        lab_date = fake.date_this_year().strftime("%Y-%m-%d %H:%M:%S")
        lab_res = random.choice(["Positiu", "Negatiu", "Inconclusive"])
        lab_note = f"Prova de laboratori {random.randint(1, 100)}"
        lab_pat_id = random.choice(valid_pat_ids)  # Seleccionar un ID válido de paciente
        lab_pat_name = fake.name()[:100]  # Limitar a 100 caracteres
        lab_cross = [random.randint(1, 13) for _ in range(13)]  # Generar 13 valores aleatorios
        lab_lock = random.choice([0, 1])
        lab_age = random.randint(18, 80)
        lab_sex = random.choice(['M', 'F'])
        lab_material = random.choice(['Material1', 'Material2', 'Material3'])[:25]  # Limitar a 25 caracteres
        lab_pat_inout = random.choice(['I', 'O'])  # Inpatient or Outpatient
        created_by = 'admin'[:50]  # Limitar a 50 caracteres
        created_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        last_modified_by = 'admin'[:50]  # Limitar a 50 caracteres
        last_modified_date = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        lab_active = 1
        lab_status = random.choice(['draft', 'completed', 'pending'])[:7]  # Limitar a 7 caracteres

        # Escribir una fila al archivo CSV
        writer.writerow([
            exa_id_a, lab_date, lab_res, lab_note, lab_pat_id, lab_pat_name,
            *lab_cross, lab_lock, lab_age, lab_sex, lab_material, lab_pat_inout,
            created_by, created_date, last_modified_by, last_modified_date,
            lab_active, lab_status
        ])

        records_created += 1

# Cerrar la conexión
cursor.close()
connection.close()

# Mensaje final dependiendo de los registros creados
if records_created > 0:
    print(f"Se han generado {records_created} registros en el archivo {output_file}")
else:
    print("No se han generado registros debido a la falta de EXA_ID_A disponibles.")

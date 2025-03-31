import csv
from faker import Faker
import random
from datetime import datetime

# Crear instancia de Faker
fake = Faker()

# Nombre del archivo CSV
output_file = "patient.csv"

# Número de registros
num_records = 300

# Abrir el archivo CSV para escribir
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Escribir encabezados en el CSV
    writer.writerow([
        "PAT_FNAME", "PAT_SNAME", "PAT_NAME", "PAT_BDATE", "PAT_AGE",
        "PAT_SEX", "PAT_ADDR", "PAT_CITY", "PAT_NEXT_KIN", "PAT_TELE",
        "PAT_MOTH_NAME", "PAT_MOTH", "PAT_FATH_NAME", "PAT_FATH", "PAT_NOTE",
        "PAT_DELETED", "PAT_LOCK", "PAT_BTYPE", "PAT_TAXCODE", "PAT_TIMESTAMP",
        "PAT_CREATED_BY", "PAT_CREATED_DATE", "PAT_LAST_MODIFIED_BY",
        "PAT_LAST_MODIFIED_DATE", "PAT_ACTIVE", "PAT_PROFESSION", "PAT_MAR_STAT",
        "PAT_PROFILE_PHOTO_ID", "PTC_CONSENSUS", "PTC_SERVICE", "PTC_CREATED_BY",
        "PTC_CREATED_DATE", "PTC_LAST_MODIFIED_BY", "PTC_LAST_MODIFIED_DATE",
        "PTC_ACTIVE"
    ])

    # Generar registros
    for _ in range(num_records):
        # Generar datos falsos
        fname = fake.first_name()[:50]
        sname = fake.last_name()[:50]
        name = f"{fname} {sname}"[:100]
        bdate = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d")
        age = random.randint(18, 90)
        sex = random.choice(['M', 'F'])  # Asegurar 1 carácter para PAT_SEX
        addr = fake.street_address()[:50]
        city = fake.city()[:50]
        next_kin = fake.name()[:50]
        tele = fake.phone_number()[:50]
        moth_name = fake.first_name()[:50]
        moth = random.choice(['M', 'F'])
        fath_name = fake.first_name()[:50]
        fath = random.choice(['M', 'F'])
        note = "Paciente generado automáticamente"
        deleted = 'N'
        lock = 0
        btype = random.choice(['O+', 'O-', 'A+', 'A-', 'B+', 'B-', 'AB+', 'AB-'])
        taxcode = fake.ssn()[:30]
        timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        created_by = 'admin'
        created_date = timestamp
        last_modified_by = 'admin'
        last_modified_date = timestamp
        active = 1
        profession = "farming"
        mar_stat = "married"
        profile_photo_id = 0

        # Datos para consensus
        ptc_consensus = 0
        ptc_service = 0
        ptc_created_by = 'admin'
        ptc_created_date = created_date
        ptc_last_modified_by = last_modified_by
        ptc_last_modified_date = last_modified_date
        ptc_active = 1

        # Escribir fila en el CSV
        writer.writerow([
            fname, sname, name, bdate, age, sex, addr, city, next_kin, tele,
            moth_name, moth, fath_name, fath, note, deleted, lock, btype,
            taxcode, timestamp, created_by, created_date, last_modified_by,
            last_modified_date, active, profession, mar_stat, profile_photo_id,
            ptc_consensus, ptc_service, ptc_created_by, ptc_created_date,
            ptc_last_modified_by, ptc_last_modified_date, ptc_active
        ])

print(f"Archivo {output_file} generado correctamente con {num_records} registros.")

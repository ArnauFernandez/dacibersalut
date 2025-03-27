import csv
from faker import Faker
import random
from datetime import datetime

# Crear instància de Faker
fake = Faker()

# Nom del fitxer CSV
output_file = "usuaris-pacients-alta.csv"

# Número de registres
num_records = 300

# Longitud màxima per a cada columna, segons la definició de la taula
MAX_FNAME_LENGTH = 50
MAX_SNAME_LENGTH = 50
MAX_NAME_LENGTH = 100
MAX_ADDR_LENGTH = 50
MAX_CITY_LENGTH = 50
MAX_NEXT_KIN_LENGTH = 50
MAX_TELE_LENGTH = 50
MAX_MOTH_NAME_LENGTH = 50
MAX_FATH_NAME_LENGTH = 50
MAX_PROFESSION_LENGTH = 50
MAX_MAR_STAT_LENGTH = 50
MAX_ALLERGIES_LENGTH = 255
MAX_ANAMNESIS_LENGTH = 255

# Obrir fitxer CSV per escriure
with open(output_file, mode='w', newline='', encoding='utf-8') as file:
    writer = csv.writer(file)

    # Escriure capçaleres al CSV
    writer.writerow([
        "PAT_FNAME", "PAT_SNAME", "PAT_NAME", "PAT_BDATE", "PAT_AGE", "PAT_SEX",
        "PAT_ADDR", "PAT_CITY", "PAT_NEXT_KIN", "PAT_TELE", "PAT_MOTH_NAME", "PAT_MOTH",
        "PAT_FATH_NAME", "PAT_FATH", "PAT_LEDU", "PAT_ESTA", "PAT_PTOGE", "PAT_NOTE",
        "PAT_DELETED", "PAT_LOCK", "PAT_BTYPE", "PAT_TAXCODE", "PAT_TIMESTAMP",
        "PAT_CREATED_BY", "PAT_CREATED_DATE", "PAT_LAST_MODIFIED_BY",
        "PAT_LAST_MODIFIED_DATE", "PAT_ACTIVE", "PAT_PROFESSION", "PAT_MAR_STAT",
        "PAT_PROFILE_PHOTO_ID", "PAT_ALLERGIES", "PAT_ANAMNESIS"
    ])

    # Generar registres
    for _ in range(num_records):
        # Generar dades falses
        fname = fake.first_name()[:MAX_FNAME_LENGTH]
        sname = fake.last_name()[:MAX_SNAME_LENGTH]
        name = f"{fname} {sname}"[:MAX_NAME_LENGTH]
        bdate = fake.date_of_birth(minimum_age=18, maximum_age=90).strftime("%Y-%m-%d")
        age = random.randint(18, 90)
        sex = random.choice(['M', 'F'])
        addr = fake.street_address()[:MAX_ADDR_LENGTH]
        city = fake.city()[:MAX_CITY_LENGTH]
        next_kin = fake.name()[:MAX_NEXT_KIN_LENGTH]
        tele = fake.phone_number()[:MAX_TELE_LENGTH]
        moth_name = fake.first_name()[:MAX_MOTH_NAME_LENGTH]
        moth = random.choice(['M', 'F'])
        fath_name = fake.first_name()[:MAX_FATH_NAME_LENGTH]
        fath = random.choice(['M', 'F'])
        ledu = random.choice(['Y', 'N'])
        esta = random.choice(['Y', 'N'])
        ptoge = random.choice(['Y', 'N'])
        note = fake.text(max_nb_chars=255)
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
        profession = fake.job()[:MAX_PROFESSION_LENGTH]
        mar_stat = random.choice(['single', 'married', 'divorced', 'widowed'])[:MAX_MAR_STAT_LENGTH]
        profile_photo_id = None  # Ajusta segons les teves necessitats
        allergies = fake.text(max_nb_chars=MAX_ALLERGIES_LENGTH)
        anamnesis = fake.text(max_nb_chars=MAX_ANAMNESIS_LENGTH)

        # Escriure una fila al fitxer CSV
        writer.writerow([
            fname, sname, name, bdate, age, sex, addr, city, next_kin, tele,
            moth_name, moth, fath_name, fath, ledu, esta, ptoge, note, deleted,
            lock, btype, taxcode, timestamp, created_by, created_date,
            last_modified_by, last_modified_date, active, profession, mar_stat,
            profile_photo_id, allergies, anamnesis
        ])

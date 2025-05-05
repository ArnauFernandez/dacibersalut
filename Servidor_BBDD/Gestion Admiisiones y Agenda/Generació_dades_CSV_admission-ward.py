from dotenv import load_dotenv
import os
import csv
from faker import Faker
import random
from datetime import datetime

# Càrrega de variables del fitxer .env
load_dotenv()

# Crear instància de Faker
fake = Faker()

# Rutes per guardar els fitxers CSV
ward_csv = "oh_ward.csv"
admissiontype_csv = "oh_admissiontype.csv"
admission_csv = "oh_admission.csv"

# Generar dades fictícies i escriure-les a fitxers CSV
try:
    # 1. Crear wards fictícies
    with open(ward_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escriure capçalera
        writer.writerow([
            "WRD_ID_A", "WRD_NAME", "WRD_NBEDS", "WRD_NQUA_NURS", "WRD_NDOC",
            "WRD_IS_OPD", "WRD_IS_PHARMACY", "WRD_IS_MALE", "WRD_IS_FEMALE",
            "WRD_VISIT_DURATION", "WRD_CREATED_BY", "WRD_CREATED_DATE", "WRD_ACTIVE"
        ])
        for i in range(1, 4):
            writer.writerow([
                f"FW{i}", fake.company()[:50], random.randint(5, 50),
                random.randint(2, 10), random.randint(1, 5), random.choice([0, 1]),
                random.choice([0, 1]), random.choice([0, 1]), random.choice([0, 1]),
                random.randint(15, 60), "admin",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1
            ])

    # 2. Crear tipus d'admissió ficticis
    with open(admissiontype_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escriure capçalera
        writer.writerow([
            "ADMT_ID_A", "ADMT_DESC", "ADMT_CREATED_BY", "ADMT_CREATED_DATE", "ADMT_ACTIVE"
        ])
        for i in range(1, 4):
            writer.writerow([
                f"FAKE{i}", fake.catch_phrase()[:50], "admin",
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1
            ])

    # 3. Crear admisions fictícies
    # Per aquest cas, assumirem un conjunt fictici de pacients amb IDs PAT1, PAT2, PAT3
    patients = ["PAT1", "PAT2", "PAT3"]
    with open(admission_csv, mode='w', newline='', encoding='utf-8') as file:
        writer = csv.writer(file)
        # Escriure capçalera
        writer.writerow([
            "ADM_IN", "ADM_TYPE", "ADM_WRD_ID_A", "ADM_PAT_ID", "ADM_DATE_ADM",
            "ADM_ADMT_ID_A_ADM", "ADM_NOTE", "ADM_USR_ID_A", "ADM_CREATED_BY",
            "ADM_CREATED_DATE", "ADM_ACTIVE"
        ])
        for patient_id in patients:
            writer.writerow([
                1, 'A', random.choice(['FW1', 'FW2', 'FW3']), patient_id,
                datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                random.choice(['FAKE1', 'FAKE2', 'FAKE3']), fake.text(max_nb_chars=100)[:100],
                'admin', "admin", datetime.now().strftime("%Y-%m-%d %H:%M:%S"), 1
            ])

    print("Dades fictícies generades correctament en fitxers CSV.")

except Exception as e:
    print(f"Error al generar dades: {e}")

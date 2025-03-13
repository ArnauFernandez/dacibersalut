import csv
import mysql.connector
from mysql.connector import Error

# Configuració de la connexió a la base de dades
config = {
    'user': 'root',  # Substituïu pel vostre usuari de MariaDB
    'password': 'ciber25',  # Substituïu per la vostra contrasenya de MariaDB
    'host': 'localhost',  # O la IP del contenidor Docker
    'port': 3306,  # Port exposat del contenidor
    'database': 'oh',  # Nom de la base de dades
    'raise_on_warnings': True
}

# Funció per comprovar si un usuari existeix
def usuari_existeix(cursor, nom):
    query = "SELECT COUNT(*) FROM oh_user WHERE US_ID_A = %s"
    cursor.execute(query, (nom,))
    return cursor.fetchone()[0] > 0

# Funció per comprovar si un grup existeix
def grup_existeix(cursor, grup):
    query = "SELECT COUNT(*) FROM oh_user_group WHERE UG_ID_A = %s"  # Assumim que la taula de grups es diu oh_user_group
    cursor.execute(query, (grup,))
    return cursor.fetchone()[0] > 0

# Funció per mostrar el menú i obtenir l'opció
def mostrar_menu():
    print("\nQuè vols modificar?")
    print("1. Canviar el nom")
    print("2. Canviar el grup")
    print("3. Canviar la descripció")
    print("4. Continuar al següent usuari")
    opcio = input("Selecciona una opció (1-4): ")
    return opcio

# Funció per preguntar si es vol continuar modificant el mateix usuari
def preguntar_continuar():
    resposta = input("Vols modificar alguna cosa més per a aquest usuari? (s/n): ").strip().lower()
    return resposta == 's'

# Funció per modificar un usuari
def modificar_usuari(cursor, nom_actual):
    while True:
        opcio = mostrar_menu()

        if opcio == '1':  # Canviar el nom
            nou_nom = input("Introdueix el nou nom: ")
            if usuari_existeix(cursor, nou_nom):
                print("Error: El nom ja existeix.")
            else:
                query = "UPDATE oh_user SET US_ID_A = %s WHERE US_ID_A = %s"
                cursor.execute(query, (nou_nom, nom_actual))
                print("Nom canviat correctament.")
                if not preguntar_continuar():
                    break

        elif opcio == '2':  # Canviar el grup
            nou_grup = input("Introdueix el nou grup: ")
            if not grup_existeix(cursor, nou_grup):
                print("Error: El grup no existeix.")
            else:
                query = "UPDATE oh_user SET US_UG_ID_A = %s WHERE US_ID_A = %s"
                cursor.execute(query, (nou_grup, nom_actual))
                print("Grup canviat correctament.")
                if not preguntar_continuar():
                    break

        elif opcio == '3':  # Canviar la descripció
            nova_descripcio = input("Introdueix la nova descripció: ")
            query = "UPDATE oh_user SET US_DESC = %s WHERE US_ID_A = %s"
            cursor.execute(query, (nova_descripcio, nom_actual))
            print("Descripció canviat correctament.")
            if not preguntar_continuar():
                break

        elif opcio == '4':  # Continuar al següent usuari
            print("Continuant al següent usuari.")
            break

        else:
            print("Opció no vàlida. Torna a intentar.")

# Llegir el fitxer CSV i modificar usuaris
def llegir_csv_i_modificar_usuaris(csv_file):
    try:
        # Connexió a la base de dades
        conn = mysql.connector.connect(**config)
        cursor = conn.cursor()

        # Llegir el fitxer CSV
        with open(csv_file, mode='r') as file:
            csv_reader = csv.DictReader(file)
            for row in csv_reader:
                nom_actual = row['nom']

                # Comprovar si l'usuari existeix
                if usuari_existeix(cursor, nom_actual):
                    print(f"\nModificant usuari: {nom_actual}")
                    modificar_usuari(cursor, nom_actual)
                else:
                    print(f"L'usuari {nom_actual} no existeix i s'ha omès.")

        # Confirmar els canvis a la base de dades
        conn.commit()
    except Error as e:
        print(f"Error: {e}")
    finally:
        # Tancar la connexió
        if conn.is_connected():
            cursor.close()
            conn.close()

# Executar el script
if __name__ == "__main__":
    csv_file = 'usuaris-modificar.csv'  # Camí al fitxer CSV
    llegir_csv_i_modificar_usuaris(csv_file)

#Es guarda en el dataset d'Imatges (/var/Images/)

import nbformat
import os
import pydicom
import matplotlib.pyplot as plt

# Crear un nou notebook en format JSON
nb = nbformat.v4.new_notebook()

# Codi Python dins una cel·la del notebook
codigo_python = """import os
import pydicom
import matplotlib.pyplot as plt

dicom_dir = "/var/Images/IMAGENES"

def get_dicom_files(directory):
    dicom_files = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.lower().endswith(".dcm"):
                dicom_files.append(os.path.join(root, file))
    return dicom_files

dicom_files = get_dicom_files(dicom_dir)
for dicom_file in dicom_files:
    try:
        dicom_data = pydicom.dcmread(dicom_file, force=True)
        print(dicom_data)
        if hasattr(dicom_data, "pixel_array"):
            plt.figure(figsize=(6, 6))
            plt.imshow(dicom_data.pixel_array, cmap="gray")
            plt.title(f"Fitxer DICOM: {os.path.basename(dicom_file)}")
            plt.axis("off")
            plt.show()
            plt.close()
    except Exception as e:
        print(f"Error: {e}")
"""

nb.cells.append(nbformat.v4.new_code_cell(codigo_python))

notebook_path = "/var/Images/IMAGENES/dicom_viewer.ipynb"

with open(notebook_path, "w", encoding="utf-8") as f:
    nbformat.write(nb, f)

print(f"Notebook creat correctament: {notebook_path}")

# Gestión de Sensores con Tkinter y Excel

Este proyecto consiste en una aplicación de escritorio en Python que permite:

1. **Cargar** un archivo Excel con datos de sensores.  
2. **Visualizar** y **filtrar** sensores vigentes.  
3. **Actualizar** la información de un sensor, inactivando su registro anterior y creando uno nuevo (manteniendo un historial).  
4. **Crear** sensores completamente nuevos.  
5. **Guardar** los cambios nuevamente en el mismo archivo Excel.

La aplicación se desarrolla con **Tkinter** como interfaz gráfica y utiliza **Pandas** para la manipulación de datos en Excel.

---

## Tabla de contenidos

- [Requisitos](#requisitos)
- [Estructura del proyecto](#estructura-del-proyecto)
- [Uso de la aplicación](#uso-de-la-aplicación)
  - [Instalación](#instalación)
  - [Ejecución](#ejecución)
- [Cómo crear un ejecutable con PyInstaller](#cómo-crear-un-ejecutable-con-pyinstaller)
- [Notas adicionales](#notas-adicionales)

---

## Requisitos

- **Python 3.7+**  
- Bibliotecas de Python:
  - `pandas`
  - `openpyxl`
  - `tkinter` (viene por defecto en la mayoría de instalaciones de Python)
  - `pyinstaller` (solo si deseas crear un ejecutable)

Puedes instalar las dependencias con:

```bash
pip install pandas openpyxl pyinstaller

# GestorSensores/
├─ README.md                  # Este archivo
├─ main.py                    # Código principal de la aplicación
└─ requirements.txt           # Requerimientos (opcional)


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
```
pip install pandas openpyxl pyinstaller
```
#estructura-del-proyecto
```bash


# GestorSensores/
├─ README.md                  # Este archivo
├─ main.py                    # Código principal de la aplicación
└─ requirements.txt           # Requerimientos (opcional)

```
# Uso de la aplicación
## Instalación
Clonar o descargar este repositorio.

Asegurarte de tener las librerías necesarias instaladas:


Copiar código
pip install -r requirements.txt
Si no tienes un requirements.txt, instala manualmente:

Copiar código
pip install pandas openpyxl
Verifica que Python esté en tu PATH. Para comprobarlo, abre una terminal y ejecuta:

bash
Copiar código
python --version
Debería mostrar tu versión de Python.

# Ejecución
Navega a la carpeta donde se encuentra main.py.
Ejecuta:
bash
Copiar código
python main.py
Se abrirá la ventana de la aplicación.
Dentro de la aplicación:

Pulsa “Cargar Excel” para cargar un archivo .xlsx o .xls.
Para filtrar sensores, ingresa texto en el campo “Buscar”.
Selecciona un sensor en la tabla para ver y/o editar su información.
Actualizar Sensor:
Se inactiva el sensor seleccionado (poniendo ESTADOSENSOR = 0 y estableciendo su FECHA FIN en la fecha elegida).
Se crea un nuevo registro como sensor vigente, preservando el historial.
Crear Sensor:
Se crea un sensor completamente nuevo (sin inactivar ningún otro).
Guardar Cambios:
Escribe el DataFrame de vuelta en el archivo Excel.
Si el archivo está abierto en otro programa, asegúrate de cerrarlo antes de guardar.


Cómo crear un ejecutable con PyInstaller
Si deseas distribuir la aplicación como un archivo ejecutable (por ejemplo, en Windows), puedes usar PyInstaller.

Instala PyInstaller (si aún no lo tienes):

´´´bash

pip install pyinstaller
Navega a la carpeta que contiene main.py.

Ejecuta:

´´´bash
Copiar código
pyinstaller --onefile main.py
--onefile creará un único archivo ejecutable en la carpeta dist.
Puedes agregar --windowed (en Windows) para ocultar la consola.
Una vez que finalice el proceso, encontrarás un ejecutable en la carpeta dist/ llamado main.exe (o simplemente main en otros sistemas).

Para ejecutar:

En Windows:
bash
Copiar código
dist\main.exe
En Linux:
´´´bash
Copiar código
./dist/main
Nota: Asegúrate de incluir cualquier archivo adicional (como íconos o archivos de configuración) si tu aplicación los requiere. Puedes personalizar el spec file que genera PyInstaller para agregar otros recursos.

# Notas adicionales
Recalcular SENSOR_ID:

El código ilustra cómo SENSOR_ID se construye concatenando columnas (p.ej. SERIE, CAMPO, GRUPO_CAMPO, SENSOR, CENTRO_COSTO).
Ajusta esta lógica según tu necesidad de identificar un sensor de forma unívoca.
Historial:

Cada vez que actualizas un sensor vigente, se inactiva la fila anterior y se crea una nueva. Así mantienes un log de cambios a lo largo del tiempo.
DateTime:

Asegúrate de que las columnas de fecha (FECHA INICIO, FECHA FIN) sean de tipo datetime en tu Excel para evitar problemas de formato.

---
¡Listo! Con esto tu proyecto de Gestión de Sensores está preparado para su uso y/o para generar un ejecutable distribuible con PyInstaller. Si tienes dudas o deseas modificar la lógica interna, revisa y adapta el contenido de main.py. ¡Éxito!

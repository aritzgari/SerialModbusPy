# Imports
from itsdangerous import json
import pandas as pd
import matplotlib.pyplot as plt

# Lectura y comprobación de datos
datos = pd.read_csv(
    "/Users/aritzgaritano/Desktop/Pruebas rodion/Data/Pruebas.csv", sep=";", engine="python")

# Renombrar columnas
dict = {'Europe/Madrid_datetime': 'datetime', 'Rodion 1, tachometer pulses': 'tachometer1', 'Rodion 1, temperature': 'temperature1',
        'Rodion 2, tachometer pulses': 'tachometer2', 'Rodion 2, temperature': 'temperature2', 'Rodion 3, tachometer pulses': 'tachometer3', 'Rodion 3, temperature': 'temperature3'}
datos.rename(columns=dict, inplace=True)

# cambiar tipo de dato object a datetime
datos['datetime'] = pd.to_datetime(
    datos['datetime'], format='%d/%m/%Y %H:%M:%S')

# set timestamp as index
datos = datos.set_index('timestamp')

# Eliminación de datos vacios
datos = datos.dropna()

# Dropear minutos duplicados
datos['datetime'] = datos['datetime'].dt.floor('Min')
datos = datos.drop_duplicates(subset=['datetime'])

# dropear datos de 0
datos = datos[datos.tachometer1 != 0.0]


exportar = datos.iloc[:3].to_json(
    '/Users/aritzgaritano/AppData/Roaming/npm/angular/src/app/components/json/export.json', orient='index')
#exportar = datos.to_json('/Users/aritzgaritano/AppData/Roaming/npm/angular/export.json', orient='index')

# Haciendo grafiquillos. Para coger varios en el datetime: df['StartDate'].dt.strftime('%m/%Y')
# Enlace cheatsheet: https://strftime.org/

# Datos para el plot
fig, ax = plt.subplots()
ax.plot(datos["datetime"].dt.hour, datos["temperature1"])
ax.plot(datos["datetime"].dt.hour, datos["temperature2"])
ax.plot(datos["datetime"].dt.hour, datos["temperature3"])

# Customization
ax.set_xlabel("Time (Hours)")
ax.set_ylabel("Temperature (ºC)")
ax.set_title("Temperaturas de los Rodiones")

# Mostrar plot
plt.show()

# Pruebas de graficos dobles con figure
histograma = datos["temperature1"]
plt.figure(0)
plt.hist(histograma, bins=10)
plt.show()

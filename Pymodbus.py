import pandas as pd
import time
import os
from datetime import datetime,timedelta
from pymodbus.client.sync import ModbusSerialClient

while True:
    #Crear un cliente en este caso a través de USB pero permite la conexión Ethernet/TCP
    client = ModbusSerialClient(method='rtu', port='COM3', stopbits=1,
                                bytesize=8, baudrate=115200, timeout=1, parity='N', strict=False)
    #Establecer la conexión                            
    client.connect()

    #Lectura 
    read = client.read_holding_registers(address=0x00, count=38, unit=20)
    
    #Obtención de valores de registros
    data = read.registers

    #Mostrar datos obtenidos esta iteración
    print(data)

    #Eliminar valores no importantes
    data.pop(0)
    data.pop(0)

    #Iterador
    i = 0

    #Coge el tiempo actual y le resta los microsegundos
    now=datetime.now()-timedelta(microseconds=now.microsecond)

    #Leer lo de los tres sensores y almacenarlo en un csv temporal
    while i != 3:
        j = i*12
        dict = {now: [data[0+j], data[1+j], data[2+j], data[3+j], data[4+j], data[5+j], data[6+j], data[7+j], data[8+j],
                         data[9+j], data[10+j], data[11+j]]}
        df = pd.DataFrame.from_dict(dict, orient='index')
        i = i+1
        df.to_csv('temp.csv', mode='a', sep=';')
 
    #Cerrar la conexión
    client.close()

    datos = pd.read_csv(
        "/Users/aritzgaritano/Desktop/Pruebas rodion/temp.csv", sep=";", engine="python")
    #Setear index
    datos=datos.set_index('Timestamp')

    #rename la 
    datos.rename(columns = {'Unnamed: 0':'ID'}, inplace = True)

    #dropear las anteriores index
    datos = datos.dropna()

    #change type to int
    datos = datos.astype({"ID": int})

    #Generar el csv adaptado
    datos.to_csv('adaptado.csv', mode='a', sep=';')

    #Eliminamos el sobrante
    file = '/Users/aritzgaritano/Desktop/Pruebas rodion/temp.csv'

    #Si el archivo existe lo elimina
    if(os.path.exists(file) and os.path.isfile(file)):
        os.remove(file)
        print("file deleted")
    else:
        print("file not found")

    #Los datos cada 10 segundos
    time.sleep(10)


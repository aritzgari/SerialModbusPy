import tkinter
from typing import Text
import pandas as pd
from pymodbus.client.sync import ModbusSerialClient


def datos():
    completo=pd.DataFrame()
    client = ModbusSerialClient(method='rtu', port='COM3', stopbits=1,
                                bytesize=8, baudrate=115200, timeout=1, parity='N')
    client.connect()
    read = client.read_holding_registers(address=0x00, count=38, unit=20)
    data = read.registers  
    data.pop(0)
    data.pop(0)
    i = 0
    while i != 3:
        j = i*12
        dict = {data[0+j]:  [data[1+j], data[2+j], data[3+j], data[4+j], data[5+j], data[6+j], data[7+j], data[8+j],
                             data[9+j], data[10+j], data[11+j]]}
        df = pd.DataFrame.from_dict(dict, orient='index',columns=[
            'Estado', 'Cobertura', 'Tension(mV)', 'Temperatura(x10)', 'RPM', 'RMS', 'STD', 'Cres.Vib.', 'RMS Des.', 'STD Des.', 'Cre.Des.'])
        completo=completo.append(df)
        i = i+1
    etiqueta1["text"] = str(completo)
    client.close()

ventana = tkinter.Tk()

ventana.geometry("1000x600")

boton1 = tkinter.Button(ventana, text="Tomar datos", padx=20, pady=20, command=datos)
boton1.pack()

etiqueta1 = tkinter.Label(
    ventana)
etiqueta1.pack()

ventana.mainloop()

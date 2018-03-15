from multiprocessing.connection import Client
from array import array
import sqlite3
import cPickle 

	# Conexion
conexiondb= sqlite3.connect('cliente.db')
	# creamos un cursor por el 
	# cual podremos ejecutar comandos 
	# SQL via el metodo execute
c= conexiondb.cursor()
c.execute('''CREATE TABLE IF NOT EXISTS yahoo(symbol text, last text, fecha text, change text, high text, low text, vol text)''')
direccion = ('0.0.0.0',6000) # Utilizamos 0.0.0.0 para tener la identidad local
conn = Client(direccion)
conn.send('close')
msg = conn.recv()

aceptado= 1

c.execute('INSERT INTO yahoo values(:symbol, :last, :fecha, :change, :high, :low, :vol)', msg)
c.execute('SELECT * FROM yahoo')
resultado = c.fetchall()
print (resultado)
conexiondb.commit()# Guardar cambios
conexiondb.close()



conn.close()
print ("Conexion exitosa")

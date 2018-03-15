from multiprocessing.connection import Listener
from array import array
import urllib2
import sqlite3
import cPickle 

conexiondb= sqlite3.connect('servidor.db')

def getYahooStockQuote(symbol):
    url = "http://download.finance.yahoo.com/d/quotes.csv?s=%s&f=sl1d1c1hgv" % symbol
    f = urllib2.urlopen(url)
    s = f.read()
    f.close()
    s = s.strip()
    L = s.split(',')
    D = {}
    D['symbol'] = L[0].replace('"','')
    D['last'] = L[1]
    D['fecha'] = L[2]
    D['change'] = L[3]
    D['high'] = L[4]
    D['low'] = L[5]
    D['vol'] = L[6]
    return D


# creamos un cursor por el 
    # cual podremos ejecutar comandos 
    # SQL via el metodo execute
c= conexiondb.cursor()


direccion = ('127.0.0.1',6000)
listener =Listener(direccion)
conn = listener.accept()
print (('connection accepted from', listener.last_accepted))
while True:
    msg = conn.recv()
    valores= getYahooStockQuote('GOOG')
    conn.send(valores)
    eschuchado= 1
    c.execute('''CREATE TABLE IF NOT EXISTS yahoo(symbol text, last text, fecha text, change text, high text, low text, vol text)''')
    c.execute("INSERT INTO yahoo values(:symbol, :last, :fecha, :change, :high, :low, :vol)", valores)
    c.execute("SELECT * from yahoo")
    resultado=c.fetchall()
    print (resultado)
    conexiondb.commit()#Guardar cambios
    conexiondb.close()


    if msg =='close':
        packed = cPickle.dumps(valores) # Crea un string de valores del objeto
        conn.close()
        break
listener.close()

import random
#NIF
letras = ['T', 'R', 'W', 'A', 'G', 'M', 'Y', 'F', 'P', 'D', 'X', 'B', 'N', 'J', 'Z', 'S', 'Q', 'V', 'H', 'L', 'C', 'K',
          'E']
letrasNIE = ['X', 'Y', 'Z']

#fechas
month = ["january", "february", "march", "april", "may", "june", "july", "august", "september", "october", "november",
         "december"]
def FormatoI(f):
    return f"{int(f['Año']):04d}-{int(f['Mes']):02d}-{int(f['Día']):02d} {int(f['Horas']):02d}:{int(f['Minutos']):02d}"

def FormatoII(f):
    if(int(f['Horas'])<=12):
        return f"{month[int(f['Mes'])-1]} {int(f['Día'])}, {int(f['Año'])}  {int(f['Horas'])}:{int(f['Minutos']):02d} AM"
    else:
        return f"{month[int(f['Mes']) - 1]} {int(f['Día'])}, {int(f['Año'])}  {int(f['Horas'])-12}:{int(f['Minutos']):02d} PM"

def FormatoIII(f):
    return f"{int(f['Horas']):02d}:{int(f['Minutos']):02d}:{int(f['Segundos']):02d} {int(f['Día']):02d}/{int(f['Mes']):02d}/{int(f['Año']):04d}"

#coordenadas
def Decimal(c):
    latitud = c["latitud"]
    longitud = c["longitud"]
    #si es positivo le ponemos un '+', aunque no siempre tiene que llevarlo, por normalizarlo
    if latitud > 0:
        latitud = '+' + str(latitud)
    if longitud > 0:
        longitud = '+' + str(longitud)

    return f"{latitud}, {longitud}" #IMPORTANTE: Devuelve string

def Sexagesimal(c):
    lat = c["latitud"]
    lon = c["longitud"]

    lat_grados = int(lat)
    lon_grados = int(lon)

    if(lat_grados >= 0):
        letra_lat = "N"
    else:
        letra_lat = "S"

    if (lon_grados >= 0):
        letra_lon = "E"
    else:
        letra_lon = "W"

    lat = abs(lat)
    lon = abs(lon)
    #conversion a sexagesimal
    lat_grados = abs(lat_grados)
    lon_grados = abs(lon_grados)

    lat_minutos = int((lat - lat_grados) * 60)
    lon_minutos = int((lon - lon_grados) * 60)

    lat_segundos = float(((lat - lat_grados) * 60) - lat_minutos)*100
    lon_segundos = float(((lon - lon_grados) * 60) - lon_minutos)*100

    return f"{lat_grados}{chr(176)} {lat_minutos}{chr(39)} {lat_segundos:00.04f}{chr(34)} {letra_lat}, {lon_grados}{chr(176)} {lon_minutos}{chr(39)} {lon_segundos:00.04f}{chr(34)} {letra_lon}"

def GPS(c):
    lat = float(c["latitud"])
    lon = float(c["longitud"])

    lat_grados = int(lat)
    lon_grados = int(lon)

    if(lat_grados >= 0):
        letra_lat = "N"
    else:
        letra_lat = "S"

    if (lon_grados >= 0):
        letra_lon = "E"
    else:
        letra_lon = "W"

    lat = abs(lat)
    lon = abs(lon)
    #conversion a sexagesimal
    lat_grados = abs(lat_grados)
    lon_grados = abs(lon_grados)

    lat_minutos = int((lat - lat_grados) * 60)
    lon_minutos = int((lon - lon_grados) * 60)

    lat_segundos = float(((lat - lat_grados) * 60) - lat_minutos)*100
    lon_segundos = float(((lon - lon_grados) * 60) - lon_minutos)*100

    return f"{lat_grados:03d}{lat_minutos:02d}{lat_segundos:07.4f}{letra_lat}{lon_grados:03d}{lon_minutos:02d}{lon_segundos:07.4f}{letra_lon}"
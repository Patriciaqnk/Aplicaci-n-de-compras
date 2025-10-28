import regex as re
from Formatos import *

# NIF
def nifCorrecto(nif):
    # comprueba si es un dni
    if nif[0] not in letrasNIE:
        letra = nif[-1]
        numdni = "".join(nif[0:8])
        n = int(numdni) % 23
        if letra == letras[n]:
            return True
        return False
    # si no es un dni, comprueba el nie
    letra = nif[-1]
    numnie = letrasNIE.index(nif[0])
    numnie *= 10000000
    numnie += int(nif[1:8])
    n = int(numnie) % 23
    if letra == letras[n]:
        return True
    return False


# FECHA
def bisiesto(anho):
    return anho % 4 == 0 and (anho % 100 != 0 or anho % 400 == 0)


def fechaCorrecta(dia, mes, anho):
    if (dia >= 1 and dia <= 31) and (
            mes == 1 or mes == 3 or mes == 5 or mes == 7 or mes == 8 or mes == 10 or mes == 12):
        return True
    elif (dia >= 1 and dia <= 30) and (mes == 4 or mes == 6 or mes == 9 or mes == 11):
        return True
    elif (dia >= 1 and dia <= 28) and (mes == 2):
        return True
    elif (dia == 29) and (mes == 2 and bisiesto(anho)):
        return True
    else:
        return False


def horaCorrecta(hora, minuto, segundo):
    if (hora >= 0 and hora <= 23) and (minuto >= 0 and minuto <= 59) and (segundo >= 0 and segundo <= 59):
        return True
    else:
        return False


# COORDENADAS
def coordenadasCorrectas(latitud, longitud):
    if (float(latitud) >= -90.00 and float(latitud) <= 90.00 and float(longitud) >= -180.00 and float(
            longitud) <= 180.00):
        return True
    return False


# EXPRESIONES REGULARES
def comprobarNumero(cadena):
    R = r"^\d{3} \d{3} \d{3}\s*$|\+(\d+\s*)+"
    p = re.compile(R)
    elem = p.search(cadena)
    if elem == None:
        return False
    tlf = str(elem.group(0))
    tlf2 = tlf.replace(" ", "")

    #si no tiene el símbolo +, se asume que es español y se añade +34
    if tlf2[0] != "+":
        tlf2 = "+34"+tlf2
    #la longitud de la cadena puede llegar hasta 16 porque se incluye el +
    if (elem and len(tlf2) <= 16 and len(tlf2) >= 11):
        tlf = {"Número": tlf2}
        return tlf
    return False


def comprobarNIF(cadena):
    R = r"(?P<num>\d{8}|[X-Z]\d{7})(?P<letra>[A-Z])"
    p = re.compile(R)
    elem = p.search(cadena)
    if (elem):
        NIF = elem.group(0)
        if (nifCorrecto(NIF)):
            numeros = elem.group(1)
            letra = elem.group(2)
            NIF = {"Números": numeros, "Letra": letra}
            return NIF
        return False
    return False


def comprobarFecha(cadena):
    R = r"(?P<anho>\d{4})-(?P<mes>[0-1]\d)-(?P<dia>[0-3]\d)\s+(?P<hora>[0-2]\d):(?P<minutos>[0-5]\d)(?P<segundos>)(?P<am>)|" \
        r"(?i)(?P<mes>January|February|March|April|May|June|July|August|September|October|November|December)\s+(?P<dia>[1-3]\d|\d),\s+(?P<anho>\d|\d{2}|\d{3}|\d{4})\s+(?P<hora>[1]\d|\d):(?P<minutos>[0-5]*\d)\s+(?i)(?P<am>AM|PM)(?P<segundos>)|" \
        r"(?P<hora>[0-2]\d):(?P<minutos>[0-5]\d):(?P<segundos>[0-5]\d)\s+(?P<dia>[0-3]\d)/(?P<mes>[0-1]\d)/(?P<anho>\d{4})(?P<am>)"  # formato iii

    p = re.compile(R)
    elem = p.search(cadena)
    if (elem):
        Fecha = elem.group(0)
        dia = elem.group(3)
        mes = elem.group(2)
        anho = elem.group(1)
        hora = elem.group(4)
        min = elem.group(5)
        seg = elem.group(6)
        am = elem.group(7)
        #convertimos el mes a minuscula para compararlo con nuestro array
        if mes.lower() in month:
            mes = month.index(mes.lower()) + 1      #convertimos letra a número para comprobar que sea válido
        #si el formato no tiene segundos, asumimos que es 0
        if seg == '':
            seg = 0
        #al igual que con los meses, lo pasamos a minúscula para comparar
        if (am.lower() == 'pm'):
            if not int(hora) == 12:
                hora = int(hora) + 12
        #comprobamos que el día, mes, año , hora, minutos y segundos sean coherentes
        if (fechaCorrecta(int(dia), int(mes), int(anho)) and horaCorrecta(int(hora), int(min), int(seg))):
            fecha = {"Año": int(anho), "Mes": int(mes), "Día": int(dia), "Horas": int(hora), "Minutos": int(min),
                     "Segundos": int(seg)}
            return fecha
        return False

    return False


def comprobarCoordenadas(cadena):
    R = "(?P<latitud>[+,-]?[0-1]*\d+.\d+),\s*(?P<longitud>[+,-]?[0-1]*\d+.\d+)|" \
        "(?P<latitudg>\d+)°\s*(?P<latitudmin>[0-5]*\d)'\s*(?P<latituds>[0-5]*\d.\d+)\"\s*(?P<n>N|S),\s*(?P<longitudg>1?\d*)°\s*(?P<longitudmin>[0-5]*\d)'\s*(?P<longituds>[0-5]*\d.\d+)\"\s*(?P<e>E|W)|" \
        "(?P<latitudg>[0-1]\d{2})(?P<latitudmin>[0-5]\d)(?P<latituds>[0-5]\d.\d{4})(?P<n>N|S)(?P<longitudg>[0-1]\d{2})(?P<longitudmin>[0-5])(?P<longituds>\d[0-5]\d.\d{4})(?P<e>E|W)"
    p = re.compile(R)
    elem = p.search(cadena)
    if (elem):
        Coordenadas = elem.group(0)
        longitud = elem.group(2)
        latitud = elem.group(1)

        if (latitud == None and longitud == None):
            latgrados = elem.group(3)
            latminutos = elem.group(4)
            latsegundos = elem.group(5)
            longrados = elem.group(7)
            lonminutos = elem.group(8)
            lonsegundos = elem.group(9)
            n = elem.group(6)
            e = elem.group(10)
            #conversión a decimal para guardarlo normalizado
            if n == 'S':
                latitud = - float(latgrados) - float(latminutos) / 60 - float(latsegundos) / 3600
            else:
                latitud = float(latgrados) + float(latminutos) / 60 + float(latsegundos) / 3600

            if e == 'W':
                longitud = - float(longrados) - float(lonminutos) / 60 - float(lonsegundos) / 3600
            else:
                longitud = float(longrados) + float(lonminutos) / 60 + float(lonsegundos) / 3600

        #comprobamos que la latitud y longitud están dentro de su rango de valores
        if (coordenadasCorrectas(latitud, longitud)):
            coordenadas = {"latitud": latitud, "longitud": longitud}
            return coordenadas
    return False


def comprobarPrecio(cadena):
    R = "(?P<Precio>[\d]+(?:\.\d+)?[€])"
    p = re.compile(R)
    elem = p.search(cadena)
    if elem == None:
        return False
    return elem.group(0)
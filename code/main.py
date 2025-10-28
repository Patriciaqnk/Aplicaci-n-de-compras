import sys
from math import *
from Comprobar import *


def validaFormato(linea):
    listlinea = linea.split(sep=";", maxsplit=6)
    if len(listlinea) < 6:  #si la línea no contiene todos los campos
        return None

    #comprueba que la línea cumple con los formatos
    tlf = comprobarNumero(listlinea[0])
    nif = comprobarNIF(listlinea[1])
    fecha = comprobarFecha(listlinea[2])
    coords = comprobarCoordenadas(listlinea[3])
    prod = listlinea[4]
    prec = comprobarPrecio(listlinea[5])

    if tlf == False:
        return None
    if nif == False:
        return None
    if fecha == False:
        return None
    if coords == False:
        return None
    if prec == False:
        return None
    #si todos los campos son correctos, devuelve un diccionario con los mismos campos, sin cambiar el formato
    d = {"Numero": listlinea[0], "NIF": listlinea[1], "Fecha": listlinea[2], "Coordenadas": listlinea[3],
         "Producto": prod, "Precio": listlinea[5]}

    return d


def n(linea):
    d = validaFormato(linea)

    if d == None:
        return None
    # modifica la fecha y las coordenadas
    print(str(d["Numero"]) + ";" + str(d["NIF"]) + ";" + FormatoI(comprobarFecha(d["Fecha"])) + ";" + GPS(
        comprobarCoordenadas(d["Coordenadas"])) + ";" + str(d["Producto"]) + ";" + str(d["Precio"]), end="")


def sPhone(telefono, linea):
    d = validaFormato(linea)

    if d == None:
        return None
    telefono.join("")
    # si los teléfonos coinciden imprime la línea
    if (comprobarNumero(telefono) == comprobarNumero(d["Numero"].strip())):
        print(str(d["Numero"]) + ";" + str(d["NIF"]) + ";" + str(d["Fecha"]) + ";" + str(d["Coordenadas"]) + ";" + str(
            d["Producto"]) + ";" + str(d["Precio"]), end="")


def sNIF(NIF, linea):
    d = validaFormato(linea)
    # si los nif coinciden imprime la línea
    if (d != None and NIF == d["NIF"].strip()):
        print(str(d["Numero"]) + ";" + str(d["NIF"]) + ";" + str(d["Fecha"]) + ";" + str(d["Coordenadas"]) + ";" + str(
            d["Producto"]) + ";" + str(d["Precio"]), end="")


def comparacionFechas(fecha1, fecha2):  # devuelve True si fecha1 es mayor (después)
    if (fecha1["Año"] > fecha2["Año"]):
        return True
    elif fecha1["Año"] == fecha2["Año"]:
        if (fecha1["Mes"] > fecha2["Mes"]):
            return True
        elif fecha1["Mes"] == fecha2["Mes"]:
            if (fecha1["Día"] > fecha2["Día"]):
                return True
            elif fecha1["Día"] == fecha2["Día"]:
                if (fecha1["Horas"] > fecha2["Horas"]):
                    return True
                elif fecha1["Horas"] == fecha2["Horas"]:
                    if (fecha1["Minutos"] > fecha2["Minutos"]):
                        return True
                    elif fecha1["Minutos"] == fecha2["Minutos"]:
                        if (fecha1["Segundos"] > fecha2["Segundos"]):
                            return True

    return False


def sTime(fecha1, fecha2, linea):
    d = validaFormato(linea)

    if d == None:
        return None
    # compara las fechas del fichero con las que le pasan al programa
    if (comparacionFechas(comprobarFecha(d["Fecha"]), fecha1) and comparacionFechas(fecha2,comprobarFecha(d["Fecha"]))):
        print(str(d["Numero"]) + ";" + str(d["NIF"]) + ";" + str(d["Fecha"]) + ";" + str(d["Coordenadas"]) + ";" + str(
            d["Producto"]) + ";" + str(d["Precio"]), end="")


def comparacionCoords(coords1, coords2):
    # latitud
    lat1 = float(coords1["latitud"])
    lat2 = float(coords2["latitud"])
    # longitud
    long1 = float(coords1["longitud"])
    long2 = float(coords2["longitud"])

    r = 6371000  # radio terrestre
    c = pi / 180  # constante para transformar grados en radianes
    # Fórmula de haversine
    d = 2 * r * asin(sqrt(sin(c * (lat2 - lat1) / 2) ** 2 + cos(c * lat1) * cos(c * lat2) * sin(
        c * (long2 - long1) / 2) ** 2))  # el resultado está en metros
    d = d / 1000  # lo pasamos a kilómetros
    return d


def sLocation(coord1, hasta, linea):
    d = validaFormato(linea)

    if d == None:
        return None

    coord1 = comprobarCoordenadas(coord1)
    #comprobamos que la distancia es menor que la introducida como parámetro
    if comparacionCoords(comprobarCoordenadas(d["Coordenadas"]), coord1) < int(hasta):
        print(str(d["Numero"]) + ";" + str(d["NIF"]) + ";" + str(d["Fecha"]) + ";" + str(d["Coordenadas"]) + ";" + str(
            d["Producto"]) + ";" + str(d["Precio"]), end="")


def error(a):
    # función para los errores
    if a == "tlf":
        print("El télefono introducido no es válido", file=sys.stderr)
        exit(1)
    if a == "nif":
        print("El NIF introducido no es válido", file=sys.stderr)
        exit(1)
    if a == "fecha":
        print("La fecha introducida no es válida", file=sys.stderr)
        exit(1)
    if a == "coords":
        print("Las coordenadas introducidas no son válidas", file=sys.stderr)
        exit(1)
    if a == "params":
        print("El número de parámetros no es correcto", file=sys.stderr)
        exit(1)
    if a == "file":
        print("El fichero no existe", file=sys.stderr)
        exit(1)
    if a == "error":
        print("El fichero no se puede leer", file=sys.stderr)
        exit(1)
    if a == "comando":
        print("El comando es incorrecto", file=sys.stderr)
        exit(1)
    return 1


def main():
    #Intérprete de comandos
    if sys.argv[1] == "-n":
        if not len(sys.argv) == 3:
            error("params")
        try:
            f = open(sys.argv[2], "r")
        except FileNotFoundError:
            error("file")
        except:
            error("error")

        while True:
            linea = f.readline()
            if not linea:
                break
            else:
                n(linea)
        f.close()

    elif sys.argv[1] == "-sphone":
        if not len(sys.argv) == 4:
            error("params")
        if (comprobarNumero(sys.argv[2]) == False):
            error("tlf")
        try:
            f = open(sys.argv[3], "r")
        except FileNotFoundError:
            error("file")
        except:
            error("error")
        while True:
            linea = f.readline()
            if not linea:
                break
            else:
                sPhone(sys.argv[2], linea)
        f.close()


    elif sys.argv[1] == "-snif":
        if not len(sys.argv) == 4:
            error("params")
        try:
            f = open(sys.argv[3], "r")
        except FileNotFoundError:
            error("file")
        except:
            error("error")
        if (comprobarNIF(sys.argv[2]) == False):
            error("nif")
        while True:
            linea = f.readline()
            if not linea:
                break
            else:
                sNIF(sys.argv[2], linea)
        f.close()

    elif sys.argv[1] == "-stime":
        if not len(sys.argv) == 5:
            error("params")
        try:
            f = open(sys.argv[4], "r")
        except FileNotFoundError:
            error("file")
        except:
            error("error")
        if comprobarFecha(sys.argv[2]) == False or comprobarFecha(sys.argv[3]) == False:
            error("fecha")
        while True:
            linea = f.readline()
            if not linea:
                break
            else:
                sTime(comprobarFecha(sys.argv[2]), comprobarFecha(sys.argv[3]), linea)
        f.close()

    elif sys.argv[1] == "-slocation":
        if not len(sys.argv) == 5:
            error("params")
        try:
            f = open(sys.argv[4], "r")
        except FileNotFoundError:
            error("file")
        except:
            error("error")
        if comprobarCoordenadas(sys.argv[2]) == False:
            error("coords")
        while True:
            linea = f.readline()
            if not linea:
                break
            else:
                sLocation(sys.argv[2], sys.argv[3], linea)
        f.close()
    else:
        error("comando")


if __name__ == "__main__":
    main()

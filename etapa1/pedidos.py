from os import TMP_MAX
import sqlite3
import time
######################################################################

### -----> FUNCIONES <------- ###

# Cuando se piden los nombres de los encargados


def ingreso_str(mensaje, error):
    dato = input(mensaje)
    while dato == "":
        print(error)
        dato = input(mensaje)
    return dato

# Cuando trabajamos con las cantidades de combos:


def ingreso_int(mensaje, error):
    dato = input(mensaje)
    while True:
        try:
            dato = int(dato)
            break
        except ValueError:
            print(error)
        dato = input(mensaje)
    return dato


def ingreso_float(mensaje, error):
    dato = input(mensaje)
    while True:
        try:
            dato = float(dato)
            break
        except ValueError:
            print(error)
        dato = input(mensaje)
    return dato


def ingresar_encargado():
    print("Bienvenidos a hamburgesas IT")
    nombre = input("Por favor, ingrese su nombre encargad@: ")
    return nombre


def saludar_encargado(nombre):
    print("Bienvenidos a Hamburgesa IT")
    print(f"Encargado -> {nombre}")
    print("Recuerda, siempre hay que recibir al cliente con una sonrisa :)")

# Calcular Precio Total


def calcular(precios, pedido):
    total = 0
    total += pedido["ComboSimple"] * precios["ComboSimple"]
    total += pedido["ComboDoble"] * precios["ComboDoble"]
    total += pedido["ComboTriple"] * precios["ComboTriple"]
    total += pedido["Flurby"] * precios["Flurby"]
    return total

# Confirmar Pedido


def confirmar():
    respuesta = ingreso_str("¿Confirmar pedido?(y/n)", "Error. Campo vacio.")
    while respuesta.lower() != "y" and respuesta.lower() != "n" and respuesta.lower() != "yes" and respuesta.lower() != "no":
        print("Ingrese únicamente Y o N")
        respuesta = ingreso_str(
            "¿Confirma el pedido? Y/N: ", "Error. Campo vacio.")
    if respuesta == "y" or respuesta == "yes":
        return True
    else:
        return False


def guardar_ventas(data):
    datos = tuple(data.values())
    conn = sqlite3.connect("comercio_combo.sqlite")
    cursor = conn.cursor()

    try:
        cursor.execute(
            "INSERT INTO ventas VALUES (null, ?, ?, ?, ?, ?, ?, ?)", datos)
    except sqlite3.OperationalError:
        cursor.execute("""CREATE TABLE ventas (id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            fecha TEXT,
            ComboS INT,
            ComboD INT,
            ComboT INT,
            Flurby INT,
            total REAL
         )""")
        cursor.execute("INSERT INTO ventas VALUES (null,?,?,?,?,?,?,?)", datos)
    conn.commit()
    conn.close()
    print(f"¡Se salvo el nuevo contacto! {datos[0]}")


def guardar_encargado(data):
    datosIn = (data["nombre"], data["ingreso"], "IN", 0)
    datosOut = (data["nombre"], data["egreso"], "OUT", data["facturado"])
    conn = sqlite3.connect("comercio_combo.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute(
            "INSERT INTO registro VALUES (null, ?, ?, ?, ?)", datosIn)
        cursor.execute(
            "INSERT INTO registro VALUES (null, ?, ?, ?, ?)", datosOut)
    except sqlite3.OperationalError:
        cursor.execute("""CREATE TABLE registro (id INTEGER PRIMARY KEY AUTOINCREMENT,
            encargado TEXT,
            fecha TEXT,
            evento TEXT,
            caja REAL
         )""")
        cursor.execute(
            "INSERT INTO registro VALUES (null, ?, ?, ?, ?)", datosIn)
        cursor.execute(
            "INSERT INTO registro VALUES (null, ?, ?, ?, ?)", datosOut)
    conn.commit()
    conn.close()
    print(f"¡Se salvo el nuevo contacto! ")


######################################################################

### ------> PROGRAMA EJECUTABLE <------- ###
precios = {"ComboSimple": 5, "ComboDoble": 6, "ComboTriple": 7, "Flurby": 2}

salir = True


while salir:
    datos_encargado = {"nombre": "", "ingreso": "",
                       "egreso": "", "facturado": ""}

    encargado = ingresar_encargado()
    inicio = time.asctime()
    datos_encargado["nombre"] = encargado
    datos_encargado["ingreso"] = inicio
    caja = 0

    print("\n" * 2)

    while True:
        saludar_encargado(encargado)
        print("""
        1 – Ingreso de nuevo pedido
        2 – Cambio de turno
        3 – Apagar sistema
        """)

        opcion = ingreso_str(">>>", "Error, ingreso vacio")

        if opcion == "1":
            print("\n"*2)

            pedido = {"cliente": "", "fecha": "", "ComboSimple": 0,
                      "ComboDoble": 0, "ComboTriple": 0, "Flurby": 0, "total": 0}
            pedido["cliente"] = ingreso_str(
                "Ingrese el nombre del cliente: ", "Error. No deje este campo vacio")
            pedido["ComboSimple"] = ingreso_int(
                "Ingrese cantidad Combo Simple: ", "Error, solo números")
            pedido["ComboDoble"] = ingreso_int(
                "Ingrese cantidad Combo Doble: ", "Error, solo números")
            pedido["ComboTriple"] = ingreso_int(
                "Ingrese cantidad Combo Triple: ", "Error, solo números")
            pedido["Flurby"] = ingreso_int(
                "Ingrese cantidad Flurby: ", "Error, solo números")

            costo_total = calcular(precios, pedido)
            print("Total: $", costo_total)

            recibido = ingreso_float("Abona con $ ", "Error, solo números")
            while costo_total > recibido:
                print(
                    "Ingrese un monto mayor. No alcanza para pagar el monto ingresado.")
                recibido = ingreso_float("Abona con $ ", "Error, solo números")
            print("Vuelto: $", recibido - costo_total)

            estado = confirmar()
            if estado:
                caja += costo_total
                pedido["fecha"] = time.asctime()
                pedido["total"] = costo_total
                guardar_ventas(pedido)
            else:
                print("Pedido cancelado")

        elif opcion == "2":
            datos_encargado["egreso"] = time.asctime()
            datos_encargado["facturado"] = caja
            guardar_encargado(datos_encargado)
            break

        elif opcion == "3":
            datos_encargado["egreso"] = time.asctime()
            datos_encargado["facturado"] = caja
            guardar_encargado(datos_encargado)
            print("¡Muchas gracias por usar nuestro programa!")
            salir = False
            break

        else:
            print("Opción incorrecta vuelva a intentarlo")
            print("\n" * 3)

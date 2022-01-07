import tkinter as tk
from tkinter import ttk, messagebox
import time
import sqlite3
import requests
import sys


### FUNCIONES ###


### FUNCION (ENCARGADO)
def guardarEncargado(data):
    datosIn = (data["nombre"], data["ingreso"], "IN", 0)
    datosOut = (data["nombre"], data["egreso"], "OUT", data["facturado"])
    conn = sqlite3.connect("comercio.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO registro VALUES (null, ?, ?, ?, ?)", (datosIn))
        cursor.execute("INSERT INTO registro VALUES (null, ?, ?, ?, ?)", (datosOut))
    except sqlite3.OperationalError:
        cursor.execute(
            "CREATE TABLE registro (id INTEGER PRIMARY KEY AUTOINCREMENT, encargado TEXT, fecha TEXT, evento TEXT, caja REAL)"
        )
        cursor.execute("INSERT INTO registro VALUES (null, ?, ?, ?, ?)", (datosIn))
        cursor.execute("INSERT INTO registro VALUES (null, ?, ?, ?, ?)", (datosOut))
    conn.commit()
    conn.close()


## GUARDAR VENTAS
def guardarVentas(data):
    datos = tuple(data)
    conn = sqlite3.connect("comercio.sqlite")
    cursor = conn.cursor()
    try:
        cursor.execute("INSERT INTO ventas VALUES (null, ?, ?, ?, ?, ?, ?, ?)", (datos))
    except sqlite3.OperationalError:
        cursor.execute(
            """CREATE TABLE ventas 
        ( 
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            cliente TEXT,
            fecha TEXT,
            ComboS INT,
            ComboD INT,
            ComboT INT,
            Flurby INT,
            total REAL
        )
        """
        )
        cursor.execute("INSERT INTO ventas VALUES (null,?,?,?,?,?,?,?)", datos)
    conn.commit()
    conn.close


def cotizar():
    try:
        r = requests.get("https://api-dolar-argentina.herokuapp.com/api/dolaroficial")
        valor = r.json()["venta"]
        valor = round(float(valor))
        return valor
    except:
        messagebox.showerror(
            title="Error grave", message="Sin internet para cotizar. Terminado"
        )
        sys.exit()


def validar(dato):
    try:
        dato = int(dato)
        return dato
    except ValueError:
        return -1


def pedir():
    cantComboS = combo_simple_entry.get()
    cantComboS = validar(cantComboS)

    cantComboD = combo_doble_entry.get()
    cantComboD = validar(cantComboD)

    cantComboT = combo_triple_entry.get()
    cantComboT = validar(cantComboT)

    cantPostre = postre_entry.get()
    cantPostre = validar(cantPostre)

    dolar = cotizar()

    if cantComboS >= 0 and cantComboD >= 0 and cantComboT >= 0 and cantPostre >= 0:
        cliente = nombre_cliente_entry.get()
        encargado = encargado_entry.get()

        if cliente and encargado:
            respuesta = messagebox.askyesno(
                title="Pregunta", message="¿Confirma el pedido?"
            )
            if respuesta:
                costoTotal = (
                    (cantComboS * precios["ComboSimple"])
                    + (cantComboD * precios["ComboDoble"])
                    + (cantComboT * precios["ComboTriple"])
                    + (cantPostre * precios["Flurby"])
                )
                totalPesos = costoTotal * dolar
                fecha = time.asctime()
                pedido = [
                    cliente,
                    fecha,
                    cantComboS,
                    cantComboD,
                    cantComboT,
                    cantPostre,
                    totalPesos,
                ]
                messagebox.showinfo(title="A pagar", message="$" + str(totalPesos))
                guardarVentas(pedido)
                messagebox.showinfo(title="Información", message="Pedido Exitoso")
                if (
                    datosEncargado["nombre"] != encargado
                    and datosEncargado["egreso"] == ""
                ):  # cuando inicia la app egreso es vacio
                    datosEncargado["nombre"] = encargado
                    datosEncargado[
                        "egreso"
                    ] = "SinFecha"  # es solo para que la proxima no cumpla la condición, es solo al inicio
                    datosEncargado[
                        "facturado"
                    ] += totalPesos  # voy incrementando totales
                elif datosEncargado["nombre"] == encargado:
                    datosEncargado[
                        "facturado"
                    ] += totalPesos  # voy incrementando totales
                else:
                    datosEncargado[
                        "egreso"
                    ] = fecha  # al cambiar de encargado registro la fecha
                    guardarEncargado(datosEncargado)  # guardo
                    # borramos el encargado anterior, en el diccionario ponemos el nuevo
                    datosEncargado["nombre"] = encargado  # iniciamos el nuevo encargado
                    datosEncargado["ingreso"] = fecha
                    datosEncargado["facturado"] = 0
                    datosEncargado["facturado"] += totalPesos
                borrar()
            else:
                messagebox.showinfo(title="Información", message="Pedido en pausa")
        else:
            messagebox.showwarning(
                title="Advertencia", message="Error, ingrese bien los datos"
            )
    else:
        messagebox.showwarning(
            title="Advertencia", message="Error, ingrese datos correctos"
        )


# ---> FUNCION BORRAR Y CANCELAR PEDIDO


def borrar():
    combo_simple_entry.delete(0, tk.END)
    combo_doble_entry.delete(0, tk.END)
    combo_triple_entry.delete(0, tk.END)
    postre_entry.delete(0, tk.END)
    nombre_cliente_entry.delete(0, tk.END)


def cancelar():
    respuesta = messagebox.askyesno(
        title="Cancelar Pedido?",
        message="Confirmar, en verdad quieres cancelar el pedido?...",
    )
    if respuesta:
        borrar()


## SALIR SEGURO
def salir():
    # salir seguro implica guardar el último encargado
    respuesta = messagebox.askyesno(title="Pregunta", message="¿Desea salir?")
    if respuesta:
        datosEncargado["egreso"] = time.asctime()
        guardarEncargado(datosEncargado)
        sys.exit()


### ----> DATOS ENCARGADO Y PRECIOS
##########################

precios = {"ComboSimple": 5, "ComboDoble": 6, "ComboTriple": 7, "Flurby": 2}
datosEncargado = {"nombre": "", "ingreso": time.asctime(), "egreso": "", "facturado": 0}

##########################


##### Aplicación Escritorio #####

# --> Ventana

ventana = tk.Tk()
ventana.title("Delivery")
ventana.config(width=500, height=400)


# ---> Etiqueta -> Titulo

titulo = tk.Label(text="--- Pedidos ---")
titulo.place(x=200, y=20)

## ENCARGADO ##
nombre_encargado = tk.Label(text="Nombre de Encargado:")
nombre_encargado.place(x=30, y=50)

encargado_entry = tk.Entry()
encargado_entry.place(x=200, y=50, width=200)

## COMBOS ###

combo_simple = tk.Label(text="Combo S cantidad:")
combo_simple.place(x=30, y=100)

combo_simple_entry = tk.Entry()
combo_simple_entry.place(x=200, y=100, width=200)

combo_doble = tk.Label(text="Combo D cantidad:")
combo_doble.place(x=30, y=150)

combo_doble_entry = tk.Entry()
combo_doble_entry.place(x=200, y=150, width=200)

combo_triple = tk.Label(text="Combo T cantidad:")
combo_triple.place(x=30, y=200)

combo_triple_entry = tk.Entry()
combo_triple_entry.place(x=200, y=200, width=200)

##POSTRES

postre = tk.Label(text="Postre cantidad:")
postre.place(x=30, y=250)

postre_entry = tk.Entry()
postre_entry.place(x=200, y=250, width=200)

##CLIENTE

nombre_cliente = tk.Label(text="Nombre del Cliente:")
nombre_cliente.place(x=30, y=300)

nombre_cliente_entry = tk.Entry()
nombre_cliente_entry.place(x=200, y=300, width=200)

### ---> BOTONES

boton_salir = tk.Button(text="Salir Seguro", command=salir)
boton_salir.place(x=30, y=350)

cancelar_pedido = tk.Button(text="Cancelar Pedido", command=cancelar)
cancelar_pedido.place(x=180, y=350)

hacer_pedido = tk.Button(text="Hacer Pedido", command=pedir)
hacer_pedido.place(x=350, y=350)

ventana.mainloop()

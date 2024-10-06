import random as rn
import datetime as dt
import re
from menues import menues as menu
from variables import constantes as cs
from funciones import funcionesX as fx
import json

ruta = "JSON/mensajes.json"

def obtener_datos_mensaje() -> list:
    """
    Esta funcion toma los datos del mensaje nuevo y los valida

    pre:no recive nada como parametro, toma los datos dentro de la funcion

    post: devuelve una lista con los datos
    """
    while True:
        try: 
            nuevo_mensaje = input("Ingrese nuevo mensaje: ")
            #verifico si el mensaje es valido y no es demaciado largo
            if 0 > len(nuevo_mensaje) <= 200:
                print(f"El mensaje es: {nuevo_mensaje}")
                dias = int(input("Ingrese la cantidad de días: "))
                #verifico que la cantidad de dias sea valida
                if 0 > dias <= 100:
                    print(f"La cantidad de dias ingresados es: {dias}")
                    #verificación de que el mensaje ingresado es correcto
                    ok = input("¿Los datos ingresados son correctos? (y/n): ").lower()
                    if ok == "y":
                        mensaje = [dias, nuevo_mensaje]
                        return mensaje
        except ValueError:
            print("Datos ingresados son incorrectos")
    
    

def crear_mensaje(mensaje: list) -> None:
    """
    Esta funcion toma los datos, comprueba si son validos y los agrega al json
    
    pre: recive una lista con los datos del mensaje nuevo y la cantidad de dias

    post: agrega los datos como par clave valor al diccionario del json
    """
    #leo el json y lo guardo en la variable mansajes
    mensajes = fx.leer_JSON(ruta)
    #recorro los mensajes para ver si esta la key ya existe
    for key in mensajes.keys():
        if key != mensaje[0]:
            mensajes[mensaje[0]] = mensaje[1]
    with open(ruta, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    print("Mensaje cargado.")
    menu.menu_mensajes()
    return None


def actualizar_mensaje() -> None:
    """
    Obtine el mensaje nuevo a travez de la funcion obtener_datos_mensaje, busca la clave
    que es la cantidad de dias, y si está modifica el mensaje

    pre: toma los datos dentro de la funcion

    port: carga el nuevo mensaje, no devuelve nada
    """
    #obtengo el menssaje nuevo
    mensaje_nuevo = obtener_datos_mensaje()
    #defino los dias desde la lista devuelta en la linea anterior
    dias = mensaje_nuevo[0]
    #defino los mensajes de la misma manera
    mensaje = mensaje_nuevo[1]
    #leo el json
    mensajes = fx.leer_JSON(ruta)
    #comparo para ver si la clave(los dias) existen en el json
    for key in mensajes.keys():
        if key == dias:
            mensajes[dias] = [mensaje]
    #vuelvo a cargar todo en el json
    with open(ruta, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    print("Mensaje cargado.")
    menu.menu_mensajes()
    return None



def borrar_mensaje():
    """
    Borrar mensaje con ese id
    """
    #defino los dias desde la lista devuelta en la linea anterior
    dias = mensaje_nuevo[0]
    #leo el json
    mensajes = fx.leer_JSON(ruta)
    #comparo para ver si la clave(los dias) existen en el json
    for key in mensajes.keys():
        if key == dias:
            print(mensajes[dias])
            ok = input("Este es  el mensaje que queres eliminar? (y/n): ").lower()
            if ok == "y":
                del mensajes[dias]
                menu.menu_mensajes()
            else:
                print("Mensaje no eliminado")
                menu.menu_mensajes()
    #vuelvo a cargar todo en el json
    with open(ruta, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    print("Mensaje cargado.")
    menu.menu_mensajes()
    return None

def mostrar_mensajes():
    """
    Ver todos los mensajes disponibles
    """
    mensajes = fx.leer_JSON(ruta)
    for key, value in mensajes:
        print(f"Dias: {key}- mensaje: {value}")
    return None

def ver_mensaje():
    """
    Ver un mensaje por id
    """
    mensajes = fx.leer_JSON(ruta)
    dias =
    for key, value in mensajes:
        print(f"Dias: {key}- mensaje: {value}")
    pass


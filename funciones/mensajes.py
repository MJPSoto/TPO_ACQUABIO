import random as rn
import datetime as dt
from variables import constantes as cs


def crear_mensaje():
    """
    Se repíte lo mismo de arriba 
    id mensaje --> generado aleatoriamente  
    cantidad de dias 
    mensaje 
    """
    #variables de fecha
    fecha_actual = dt.datetime.now()
    fecha_compra = dt.
    #verificar la cantidad de dias desdepues de la venta
    cantidad_dias = 0
    #generar el id del mensaje con un nuemero aleatorio
    id_mensaje = rn.randint(1000, 9999)
    #ingresar el mensaje
    while True:
        nuevo_mensaje = input("Ingrese nuevo mensaje: ")
        print(nuevo_mensaje)
        #verificación de que el mensaje ingresado es correcto
        ok = input("¿El mensaje es correcto? (y/n): ").lower()
        if ok == "y":
            break
    #verifico si el id ya esta cargado en el diccionario
    if id_mensaje not in cs.mensajes:


    pass

def actualizar_mensaje():
    """
    Actualizar mensaje con ese id
    """
    pass

def borrar_mensaje():
    """
    Borrar mensaje con ese id
    """
    pass

def ver_mensajes():
    """
    Ver todos los mensajes disponibles
    """
    pass

def ver_mensaje():
    """
    Ver un mensaje por id
    """
    pass
from menues import menues as menu
from funciones import funcionesX as fx
import json
import re

RUTA = "JSON/mensajes.json"


def mensaje_valido(texto):
    # Patrón: al menos cuatro caracteres, contiene letras, no es solo números ni solo espacios
    patron = r"^(?=.*[A-Za-z])(?=.{4,})(?!^\d+$).*$"
    return bool(re.match(patron, texto.strip()))

def obtener_datos_mensaje() -> list[str]:
    """
    Esta funcion toma los datos del mensaje nuevo y los valida

    pre: no recive nada

    post: devuelve una lista con los datos
    """
    while True:
        mensaje = [""]
        nuevo_mensaje = input("Ingrese nuevo mensaje: ")
        #verifico si el mensaje es valido y no es demasiado largo
        if mensaje_valido(nuevo_mensaje):
            try:
                dias = input("Ingrese la cantidad de días: ")
                #verifico que la cantidad de dias sea valida
                if int(dias) > 0 and int(dias) <= 100:
                    print(f"El mensaje es: {nuevo_mensaje}")
                    print(f"La cantidad de dias ingresados es: {dias}")
                    #verificación de que el mensaje ingresado es correcto
                    ok = input("¿Los datos ingresados son correctos? (y/n): ").lower()
                    if ok == "y":
                        mensaje = [dias, nuevo_mensaje]
            except ValueError:
                print("Datos ingresados son incorrectos")
        return mensaje
    
    

def crear_mensaje() -> None:
    """
    Esta funcion toma los datos, comprueba si son validos y los agrega al json
    
    pre: no recibe nada

    post: no devuelve nada
    """
    #leo el json y lo guardo en la variable mansajes
    mensajes = fx.leer_JSON(RUTA)
    print(mensajes)
    nuevo_mensaje = obtener_datos_mensaje()
    #defino los dias desde la lista devuelta en la linea anterior
    dias = nuevo_mensaje[0]
    #defino los mensajes de la misma manera
    mensaje = nuevo_mensaje[1]
    #copruebo si el mensaje ya existe
    if mensajes[0].get(dias) is None:
        #creo el mensaje nuevo
        mensajes[0][dias] = mensaje
        print("Mensaje cargado.")
    else:
        #compruebo si quiere reescribir el mensaje
        ok = input("El ID de mensaje ya existe quiere reemplazarlo (y/n): ").lower()
        if ok == "y":
            mensajes[0][dias] = mensaje
            print("Mensaje cargado.")
        else:
            #esto no se si dejarlo asi o volver a la carga de mensajes
            print("No se creó ningun mensaje...")
    #reescribo el json
    with open(RUTA, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    menu.menu_mensajes()
    return None


def actualizar_mensaje() -> None:
    """
    Obtine el mensaje nuevo a travez de la funcion obtener_datos_mensaje, busca la clave
    que es la cantidad de dias, y si está modifica el mensaje

    pre: no recive nada

    port: no devuelve nada
    """
    #obtengo el menssaje nuevo
    nuevo_mensaje = obtener_datos_mensaje()
    #defino los dias desde la lista devuelta en la linea anterior
    dias = nuevo_mensaje[0]
    #defino los mensajes de la misma manera
    mensaje = nuevo_mensaje[1]
    #leo el json
    mensajes = fx.leer_JSON(RUTA)
    #comparo para ver si la clave(los dias) existen en el json
    if mensajes[0].get(dias) is None:
        #si no encuentra el mensaje solo imprime un aviso
        print("Mensaje no encotrado")
    else:
        #creo el mensaje nuevo
        mensajes[0][dias] = mensaje
        print("Mensaje cargado.")
    #vuelvo a cargar todo en el json
    with open(RUTA, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    menu.menu_mensajes()
    return None



def borrar_mensaje() -> None:
    """
    Lee el json encontrando el mensaje que se quiere borrar mediante el Id, vuelve a cargar
    el json con los mensajes excepto el eliminado.

    pre: no recive nada

    prost: no devuelve nada
    """
    #defino los dias desde la lista devuelta en la linea anterior
    try:
        dias = input("Ingrese la cantidad de días: ")
        #verifico que la cantidad de dias sea valida
        if int(dias) > 0 and int(dias) <= 100:
            #leo el json
            mensajes = fx.leer_JSON(RUTA)
            #comparo para ver si la clave(los dias) existen en el json
            if mensajes[0].get(dias) is None:
                #si no encuentra ningun mensaje
                print("Mensaje no encontrado")
            else:
                #creo el mensaje nuevo
                print(mensajes[0][dias])
                ok = input("Este es  el mensaje que queres eliminar? (y/n): ").lower()
                if ok == "y":
                    del mensajes[0][dias]
                    # Vuelvo a cargar todo en el JSON
                    with open(RUTA, "w") as archivo:
                        json.dump(mensajes, archivo, indent=4)
                    print("Mensaje eliminado.")
                    menu.menu_mensajes()
                else:
                    print("Mensaje no eliminado")
                    menu.menu_mensajes()
        else:
            print("Número ingresado fuera de rango")
    except ValueError:
        print("El valor ingresado es invalido")
    return None

def ver_mensajes() -> None:
    """
    Lee el json para imprimirlas en pantalla

    pre: no recive nada

    post: no devuelve nada
    """
    mensajes = fx.leer_JSON(RUTA)
    for key, value in mensajes[0].items():
        print(f"Dias: {key}- mensaje: {value}")
    return None

def ver_mensaje() -> None:
    """
    Busca un mensaje mediante el id, si lo encuentra lo mustra en pantalla

    pre: no recive nada

    post: no devuelve nada
    """
    mensajes = fx.leer_JSON(RUTA)
    try:
        dias = input("Ingrese la cantidad de días: ")
        #verifico que la cantidad de dias sea valida
        if int(dias) > 0 and int(dias) <= 100:
            #comparo para ver si la clave(los dias) existen en el json
            try:
                if mensajes[0].get(dias) is None:
                    print("Mensaje no encontrado")
                else:
                    print(f"Dias: {dias}- mensaje: {mensajes[0][dias]}")
            except KeyError as e:
                print(f"Error: {e}")
        else:
            print("Cantidad de dias ingresada no valida.")
    except ValueError:
        print("El valor ingresado es invalido")

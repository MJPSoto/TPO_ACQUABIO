from menues import menues as menu
from funciones import funcionesX as fx
import json

RUTA = "JSON/mensajes.json"

def obtener_datos_mensaje() -> list:
    """
    Esta funcion toma los datos del mensaje nuevo y los valida

    pre: no recive nada

    post: devuelve una lista con los datos
    """
    while True:
        try: 
            nuevo_mensaje = input("Ingrese nuevo mensaje: ")
            #verifico si el mensaje es valido y no es demasiado largo
            if 0 > len(nuevo_mensaje) <= 200: ################### expresiones regulares
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
    
def obtener_mensaje()->str:
    return input("Ingrese el mensaje: ")

def obtener_cantidad_dias()->int:
    while True:
        try:
            cantidad_dias = int(input("Ingrese la cantidad de dias: "))
            return cantidad_dias
        except ValueError as e:
            print("La cantidad de dias tiene que ser un numero.")

def crear_mensaje() -> None:
    """
    Esta funcion toma los datos, comprueba si son validos y los agrega al json
    
    pre: recive una lista con los datos del mensaje nuevo y la cantidad de dias

    post: agrega los datos como par clave valor al diccionario del json
    """
    #leo el json y lo guardo en la variable mansajes
    mensajes = fx.leer_JSON(RUTA)
    mensaje = obtener_mensaje()
    cantidad_dias = obtener_cantidad_dias()

    #recorro los mensajes para ver si esta la key ya existe
    for key in mensajes.keys():
        if key != mensaje:
            mensajes[mensaje[0]] = mensaje[1]
    with open(RUTA, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    print("Mensaje cargado.")
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
    mensaje_nuevo = obtener_datos_mensaje()
    #defino los dias desde la lista devuelta en la linea anterior
    dias = mensaje_nuevo[0]
    #defino los mensajes de la misma manera
    mensaje = mensaje_nuevo[1]
    #leo el json
    mensajes = fx.leer_JSON(RUTA)
    #comparo para ver si la clave(los dias) existen en el json
    for key in mensajes.keys():
        if key == dias:
            mensajes[dias] = [mensaje]
    #vuelvo a cargar todo en el json
    with open(RUTA, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    print("Mensaje cargado.")
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
        dias = int(input("Ingrese la cantidad de días: "))
        #verifico que la cantidad de dias sea valida
    except ValueError:
        print("El valor ingresado es invalido")
    if 0 > dias <= 100:
        #leo el json
        mensajes = fx.leer_JSON(RUTA)
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
        with open(RUTA, "w") as archivo:
            json.dump(mensajes, archivo, indent=4)
        print("Mensaje cargado.")
        menu.menu_mensajes()
    else:
        print("Número ingresado fuera de rango")
    return None

def mostrar_mensajes() -> None:
    """
    Lee el json para imprimirlas en pantalla

    pre: no recive nada

    post: no devuelve nada, solo imprime en pantalla
    """
    mensajes = fx.leer_JSON(RUTA)
    for key, value in mensajes:
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
        dias = int(input("Ingrese la cantidad de días: "))
        #verifico que la cantidad de dias sea valida
        if 0 > dias <= 100:
            for key, value in mensajes:
                if key == dias: 
                    print(f"Dias: {key}- mensaje: {value}")
        else:
            print("Cantidad de dias ingresada no valida.")
    except ValueError:
        print("El valor ingresado es invalido")
    return None

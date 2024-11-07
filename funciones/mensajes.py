from menues import menues as menu
from funciones import funcionesX as fx
import json
import re

RUTA = "JSON/mensajes.json"


def mensaje_valido(texto) -> bool:
    """
    Recibe un texto y comprueba si es valido o no

    pre: recibe un string

    post: devuelve un booleno
    """
    #al menos cuatro caracteres, contiene letras, no es solo números ni solo espacios
    patron = r"^(?=.*[A-Za-z])(?=.{4,})(?!^\d+$).*$"
    return bool(re.match(patron, texto.strip()))


def volver_menu()-> None:
    """
    Pregunta si quiere volver al menú. Te lleva al menú principal si ingresa "y" y te lleva al menu mensajes
    si ingresa "n".

    pre: no recibe nada

    post: no devuelve nada
    """
    ok = input("¿Desea volver al menú principal? (y/n): ").lower()
    
    #si es "n" vuelve a mensajes
    if ok == "n":
        menu.menu_mensajes()

    #si no es ni "n" ni "y", vuelve a ejecutar la funcion
    if ok != "y":
        volver_menu()
    
    #si no es ninguna de las anteriores se toma como "y" y vuelve a menu principal
    menu.menu_principal()
    return None


def obtener_datos_mensaje() -> list[str]:
    """
    Esta funcion toma los datos del mensaje nuevo y los valida

    pre: no recibe nada

    post: devuelve una lista con los datos
    """
    while True:
        mensaje = []
        nuevo_mensaje = input("Ingrese nuevo mensaje: ")
        #verifico si el mensaje es valido y no es demasiado largo
        if not mensaje_valido(nuevo_mensaje):
            continue

        dias = input("Ingrese la cantidad de días: ")
        #verifico que la cantidad de dias sea valida
        if not re.match("\b([1-9][0-9]{0,2})\b", dias):
            continue
        
        #guardo lo que quiero imprimir
        descripcion = f"Dias: {dias}- Mensaje: {nuevo_mensaje}\n"

        #verificación de que el mensaje ingresado es correcto
        ok = input(f"{descripcion}¿Los datos ingresados son correctos? (y/n): ").lower()
        if ok == "n":
            continue
        if ok != "y":
            continue
        
        mensaje = [dias, nuevo_mensaje]
        return mensaje
    
    

def crear_mensaje() -> str:
    """
    Esta funcion toma los datos, comprueba si son validos y los agrega al json
    
    pre: no recibe nada

    post: no devuelve nada
    """
    #leo el json y lo guardo en la variable mansajes
    mensajes = fx.leer_JSON(RUTA)
    nuevo_mensaje = obtener_datos_mensaje()
    #defino los dias desde la lista devuelta en la linea anterior
    
    try:    
        dias = nuevo_mensaje[0]
        #defino los mensajes de la misma manera
        mensaje = nuevo_mensaje[1]
        #copruebo si el mensaje ya existe
    except IndexError as e:
        crear_mensaje()
        return f"Error: {e}"

    if mensajes[0].get(dias) is None:
        #creo el mensaje nuevo
        mensajes[0][dias] = mensaje
        with open(RUTA, "w") as archivo:
            json.dump(mensajes, archivo, indent=4)
        return "Mensaje cargado."

    #compruebo si quiere reescribir el mensaje
    ok = input("El ID de mensaje ya existe quiere reemplazarlo (y/n): ").lower()
    if ok == "n":
        return "No se cargó ningun mensaje"
    if ok != "y":
        return "Valor ingresado ingorrecto"

    #reescribo el json
    with open(RUTA, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    
    return "Mensaje cargado"


def actualizar_mensaje() -> str:
    """
    Obtine el mensaje nuevo a travez de la funcion obtener_datos_mensaje, busca la dias
    que es la cantidad de dias, y si está modifica el mensaje

    pre: no recibe nada

    port: no devuelve nada
    """
    ver_mensajes()
    #leo el json
    mensajes = fx.leer_JSON(RUTA)
    #obtengo el mensaje nuevo
    nuevo_mensaje = obtener_datos_mensaje()

    try: ############# verifica el uso del try, los try van donde sabes que va a fallar tu codigo 
        #defino los dias desde la lista devuelta en la linea anterior
        dias = nuevo_mensaje[0]
        #defino los mensajes de la misma manera
        mensaje = nuevo_mensaje[1]
    except IndexError as e:
        return f"Error: {e}"

    #comparo para ver si la dias(los dias) existen en el json
    while True:
        #busco el mensaje
        if mensajes[0].get(dias) is None:
            #al no encontrarse, pregunto si quiere crear el mensaje############ 
            ok = input("El ID de mensaje no existe, desea crearlo (y/n): ").lower()
            if ok == "n":
                continue        
            if ok != "y":
                continue
            mensajes[0][dias] = mensaje
            with open(RUTA, "w") as archivo:
                json.dump(mensajes, archivo, indent=4)
            return "Mensaje cargado"

    
        #actualizo el valor del mensaje
        mensajes[0][dias] = mensaje
    
        #vuelvo a cargar todo en el json
        with open(RUTA, "w") as archivo:
            json.dump(mensajes, archivo, indent=4)
        menu.menu_mensajes()
        return "mensaje cargado."



def borrar_mensaje() -> str:
    """
    Lee el json encontrando el mensaje que se quiere borrar mediante el Id, vuelve a cargar
    el json con los mensajes excepto el eliminado.

    pre: no recibe nada

    prost: no devuelve nada
    """
    ver_mensajes()
    #defino los dias desde la lista devuelta en la linea anterior
    dias = input("Ingrese la cantidad de días: ") ######################## upa acá no puede dar error, cuando se castea un input y ese casteo no se puede hacer, eso genera un error
    #verifico que la cantidad de dias sea valida
    if not re.match("\b([1-9][0-9]{0,2})\b", dias):####################### trata de usar retorno rapido y no usar los ifs en flecha ######cambie el >1 <100 por una expresion regular
        return "Candidad de dias invalida"    
        
    #leo el json
    mensajes = fx.leer_JSON(RUTA)

    mensaje = mensajes[0].get(dias)
            
    #comparo para ver si la dias(los dias) existen en el json
    if mensaje is None:
    #si no encuentra ningun mensaje
        volver_menu()
        return "Mensaje no encontrado" ### tenemos que devolver cosas no printear cosas 

    print(mensaje)
    ok = input("Es este el mensaje que desea eliminar? (y/n): ").lower()
    if ok == "n":
        return "No se modificó ningun mensaje"        

    if ok != "y":
        volver_menu()
        return "Valor incorrecto"

    #borro el mensaje
    del mensajes[0][dias]
        
    # Vuelvo a cargar todo en el JSON
    with open(RUTA, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    return "Mensaje eliminado."
        

def ver_mensajes() -> None:
    """
    Lee el json, e imprime los mensajes en pantalla

    pre: no recibe nada

    post: no devuelve nada
    """
    try:
        mensajes = fx.leer_JSON(RUTA)
        for key, value in mensajes[0].items():
            print(f"Dias: {key}- mensaje: {value}")
        volver_menu()
    except IndexError as e:
        print(f"Error: {e}")
    return None


def ver_mensaje() -> str:
    """
    Busca un mensaje mediante el id, si lo encuentra lo mustra en pantalla

    pre: no recibe nada

    post: no devuelve nada
    """
    mensajes = fx.leer_JSON(RUTA)
    dias = input("Ingrese la cantidad de días: ") ############ lo mismo acá que en la anterior función 
    #verifico que la cantidad de dias sea valida
    if not re.match("\b([1-9][0-9]{0,2})\b", dias):
        return "El nomero ingresado no es válido"
    
    if mensajes[0].get(dias) is None:
        return "Mensaje no encontrado"

    return f"Dias: {dias}- mensaje: {mensajes[0][dias]}"

from menues import menues as menu
from funciones import funcionesX as fx
import json
import re


RUTA = "JSON/mensajes.json"


def mensaje_valido(texto) -> bool:
    """
    Recibe un texto y comprueba si es válido o no.

    pre: recibe un string.

    post: devuelve un booleano.
    """
    # al menos cuatro caracteres, contiene letras, no es solo números ni solo espacios
    patron = r"^(?=.*[A-Za-z])(?=.{4,})(?!^\d+$).*$"
    return bool(re.match(patron, texto.strip()))


def volver_menu() -> None:
    """
    Pregunta si desea volver al menú. Te lleva al menú principal si ingresas "y" y al menú mensajes si ingresas "n".

    pre: no recibe nada.

    post: no devuelve nada.
    """
    ok = input("¿Desea volver al menú principal? (y/n): ").lower()
    
    # si es "n", vuelve a mensajes
    if ok == "n":
        menu.menu_mensajes()

    # si no es ni "n" ni "y", vuelve a ejecutar la función
    if ok != "y":
        volver_menu()
    
    # si no es ninguna de las anteriores, se toma como "y" y vuelve al menú principal
    menu.menu_principal()
    return None


def obtener_datos_mensaje() -> list[str]:
    """
    Esta función toma los datos del mensaje nuevo y los valida.

    pre: no recibe nada.

    post: devuelve una lista con los datos.
    """
    while True:
        mensaje = []
        nuevo_mensaje = input("Ingrese nuevo mensaje: ")
        # verifica si el mensaje es válido y no es demasiado largo
        if not mensaje_valido(nuevo_mensaje):
            continue

        dias = input("Ingrese la cantidad de días: ")
        # verifica que la cantidad de días sea válida
        if not re.match(r"\b([1-9][0-9]{0,2})\b", dias):
            continue
        
        # guarda lo que quiere imprimir
        descripcion = f"Días: {dias} - Mensaje: {nuevo_mensaje}\n"

        # verificación de que el mensaje ingresado es correcto
        ok = input(f"{descripcion}¿Los datos ingresados son correctos? (y/n): ").lower()
        if ok == "n":
            continue
        if ok != "y":
            continue
        
        mensaje = [dias, nuevo_mensaje]
        return mensaje
    

def crear_mensaje() -> str:
    """
    Esta función toma los datos, comprueba si son válidos y los agrega al JSON.
    
    pre: no recibe nada.

    post: no devuelve nada.
    """
    # lee el JSON y lo guarda en la variable mensajes
    mensajes = fx.leer_JSON(RUTA)
    nuevo_mensaje = obtener_datos_mensaje()
    # define los días desde la lista devuelta en la línea anterior
    
    try:    
        dias = nuevo_mensaje[0]
        # define los mensajes de la misma manera
        mensaje = nuevo_mensaje[1]
    except IndexError as e:
        crear_mensaje()
        return f"Error: {e}"

    # comprueba si el mensaje ya existe
    if mensajes[0].get(dias) is None:
        # crea el mensaje nuevo
        mensajes[0][dias] = mensaje
        with open(RUTA, "w") as archivo:
            json.dump(mensajes, archivo, indent=4)
        return "Mensaje cargado."

    # comprueba si desea reemplazar el mensaje
    ok = input("El ID del mensaje ya existe, ¿quiere reemplazarlo? (y/n): ").lower()
    if ok == "n":
        return "No se cargó ningún mensaje."
    if ok != "y":
        return "Valor ingresado incorrecto."
    
    # crea el mensaje nuevo
    mensajes[0][dias] = mensaje

    # reescribe el JSON
    with open(RUTA, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    
    return "Mensaje cargado."


def actualizar_mensaje() -> str:
    """
    Obtiene el mensaje nuevo a través de la función obtener_datos_mensaje, busca el ID 
    que es la cantidad de días, y si está, modifica el mensaje.

    pre: no recibe nada.

    post: no devuelve nada.
    """
    ver_mensajes()
    # lee el JSON
    mensajes = fx.leer_JSON(RUTA)
    # obtiene el mensaje nuevo
    nuevo_mensaje = obtener_datos_mensaje()

    try: 
        # define los días desde la lista devuelta en la línea anterior
        dias = nuevo_mensaje[0]
        # define los mensajes de la misma manera
        mensaje = nuevo_mensaje[1]
    except IndexError as e:
        return f"Error: {e}"

    # compara para ver si el ID (los días) existe en el JSON
    while True:
        # busca el mensaje
        if mensajes[0].get(dias) is None:
            # al no encontrarse, pregunta si desea crear el mensaje
            ok = input("El ID del mensaje no existe, ¿desea crearlo? (y/n): ").lower()
            if ok == "n":
                continue        
            if ok != "y":
                continue
            mensajes[0][dias] = mensaje
            with open(RUTA, "w") as archivo:
                json.dump(mensajes, archivo, indent=4)
            return "Mensaje cargado."

        # actualiza el valor del mensaje
        mensajes[0][dias] = mensaje
    
        # vuelve a cargar todo en el JSON
        with open(RUTA, "w") as archivo:
            json.dump(mensajes, archivo, indent=4)
        menu.menu_mensajes()
        return "Mensaje cargado."


def borrar_mensaje() -> str:
    """
    Lee el JSON encontrando el mensaje que se quiere borrar mediante el ID, y vuelve a cargar
    el JSON con los mensajes excepto el eliminado.

    pre: no recibe nada.

    post: no devuelve nada.
    """
    ver_mensajes()
    # define los días desde la lista devuelta en la línea anterior
    dias = input("Ingrese la cantidad de días: ") 
    # verifica que la cantidad de días sea válida
    if not re.match(r"\b([1-9][0-9]{0,2})\b", dias):
        return "Cantidad de días inválida."
        
    # lee el JSON
    mensajes = fx.leer_JSON(RUTA)

    mensaje = mensajes[0].get(dias)
            
    # compara para ver si el ID (los días) existe en el JSON
    if mensaje is None:
        volver_menu()
        return "Mensaje no encontrado." 

    ok = input(f"{mensajes[dias]}\n¿Es este el mensaje que desea eliminar? (y/n): ").lower()
    if ok == "n":
        volver_menu()
        return "No se modificó ningún mensaje."        

    if ok != "y":
        volver_menu()
        return "Valor incorrecto."

    # borra el mensaje
    del mensajes[0][dias]
        
    # vuelve a cargar todo en el JSON
    with open(RUTA, "w") as archivo:
        json.dump(mensajes, archivo, indent=4)
    return "Mensaje eliminado."
        

def ver_mensajes() -> None:
    """
    Lee el JSON e imprime los mensajes en pantalla.

    pre: no recibe nada.

    post: no devuelve nada.
    """
    try:
        # lee el JSON
        mensajes = fx.leer_JSON(RUTA)
        # recorre el diccionario e imprime por clave y valor
        for key, value in mensajes[0].items():
            print(f"Días: {key} - Mensaje: {value}")
        # pregunta si desea volver al menú
        volver_menu()
    except IndexError as e:
        print(f"Error: {e}")
    return None


def ver_mensaje() -> str:
    """
    Busca un mensaje mediante el ID. Si lo encuentra, lo muestra en pantalla.

    pre: no recibe nada.

    post: no devuelve nada.
    """
    mensajes = fx.leer_JSON(RUTA)
    dias = input("Ingrese la cantidad de días: ")  
    # verifica que la cantidad de días sea válida
    if not re.match(r"\b([1-9][0-9]{0,2})\b", dias):
        return "El número ingresado no es válido."
    
    if mensajes[0].get(dias) is None:
        return "Mensaje no encontrado."

    return f"Días: {dias} - Mensaje: {mensajes[0][dias]}"


from menues import menues as menu
from funciones import funcionesX as fx
import json
import re
from tabulate import tabulate

RUTA = "JSON/mensajes.json"


def obtener_datos_mensaje() -> dict:
    """
    Esta funcion toma los datos del mensaje nuevo y los valida
    pre: no recibe nada
    post: devuelve una lista con los datos
    """
    nuevo_mensaje = fx.validacion_datos(
        "Ingrese nuevo mensaje: ",
        "Ingrese nuevamente el mensaje",
        r"^(?=.*[A-Za-z])(?=.{4,})(?!^\d+$).*$",
    )
    cantidad_dias = fx.validacion_datos(
        "Ingrese la cantidad de días: ",
        "Ingrese nuevamente la cantidad de dias",
        r"\b([1-9][0-9]{0,2})\b",
    )
    mensaje = {cantidad_dias: nuevo_mensaje}
    # verificación de que el mensaje ingresado es correcto
    print(tabulate(mensaje.items(), headers=["Dias", "Mensaje"], stralign="center"))
    fx.volver_menu(
        "¿Los datos ingresados son correctos? (y/n): ", obtener_datos_mensaje
    )
    return mensaje


def validar_existencia(mensaje: list, mensajes: list) -> None:
    if mensaje in mensajes:
        fx.volver_menu(
            "¿El mensaje ya existe, quiere cargar otro mensaje? (y/n): ",
            menu.menu_mensajes,
            crear_mensaje,
        )


def cargar_archivo(datos_cargar, mensaje_excep: str, mensaje_success: str) -> None:
    try:
        with open(RUTA, "w") as archivo:
            json.dump(datos_cargar, archivo, indent=4)
    except Exception:
        print(mensaje_excep)
    print(mensaje_success)


def crear_mensaje() -> None:
    """
    Esta funcion toma los datos, comprueba si son validos y los agrega al json
    pre: no recibe nada
    post: no devuelve nada
    """
    # leo el json y lo guardo en la variable mansajes
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
    Obtine el mensaje nuevo a travez de la funcion obtener_datos_mensaje, busca la dias
    que es la cantidad de dias, y si está modifica el mensaje
    pre: no recibe nada
    port: no devuelve nada
    """
    mensajes = fx.leer_JSON(RUTA)
    # Solicitar el ID del mensaje en días
    id_mensaje = fx.validacion_datos(
        "Ingrese la cantidad de días: ",
        "Ingrese nuevamente la cantidad de dias",
        r"\b([1-9][0-9]{0,2})\b",
    )

    mensaje = mensajes[0].get(id_mensaje, None)

    # Si el mensaje no existe, preguntar si se desea crearlo
    if mensaje is None:
        fx.volver_menu(
            "¿El mensaje no existe, desea crearlo? (y/n): ",
            menu.menu_mensajes,
            crear_mensaje,
        )
    else:
        # Mostrar el mensaje en formato de tabla
        print(
            tabulate(
                [[id_mensaje, mensaje]], headers=["Días", "Mensaje"], stralign="center"
            )
        )
        nuevo_mensaje = obtener_datos_mensaje()
        mensajes[0][list(nuevo_mensaje.keys())[0]] = list(nuevo_mensaje.values())[0]
        cargar_archivo(
            mensajes,
            "No se ha podido cargar el archivo",
            "El mensaje se actualizó correctamente",
        )
    fx.volver_menu(
        "¿Quiere actualizar otro mensaje? (y/n): ",
        menu.menu_mensajes,
        actualizar_mensaje,
    )


def obtener_mensaje_x_id(mensajes: list) -> dict:
    id_mensaje = fx.validacion_datos(
        "Ingrese la cantidad de días: ",
        "Ingrese nuevamente la cantidad de dias",
        r"\b([1-9][0-9]{0,2})\b",
    )

    mensaje = mensajes[0].get(id_mensaje, None)

    # Si el mensaje no existe, preguntar si se desea crearlo
    if mensaje is None:
        fx.volver_menu(
            "¿El mensaje no existe, desea crearlo? (y/n): ",
            menu.menu_mensajes,
            crear_mensaje,
        )
    else:
        return {id_mensaje: mensaje}


def borrar_mensaje() -> str:
    """
    Lee el json encontrando el mensaje que se quiere borrar mediante el Id, vuelve a cargar
    el json con los mensajes excepto el eliminado.
    pre: no recibe nada
    prost: no devuelve nada
    """
    # leo el json
    mensajes = fx.leer_JSON(RUTA)
    mensaje = obtener_mensaje_x_id(mensajes)
    print(
        tabulate(
            mensaje.items(),
            headers=["Dias", "Mensaje"],
            tablefmt="fancy_grid",
            stralign="center",
        )
    )

    # confirmar eliminación del mensaje
    fx.volver_menu(
        "¿Está seguro que quiere eliminar el mensaje? (y/n): ",
        menu.menu_mensajes,
    )
    # borro el mensaje
    del mensajes[0][list(mensaje.keys())[0]]

    # Vuelvo a cargar todo en el JSON
    cargar_archivo(
        mensajes,
        "No se ha podido cargar el archivo",
        "El mensaje se borró correctamente",
    )
    fx.volver_menu(
        "¿Quiere borrar otro mensaje? (y/n): ",
        menu.menu_mensajes,
        borrar_mensaje,
    )


def ver_mensajes() -> None:
    """
    Lee el json, e imprime los mensajes en pantalla
    pre: no recibe nada
    post: no devuelve nada
    """
    mensajes = fx.leer_JSON(RUTA)

    # Verificar si se encontraron mensajes
    if not mensajes:
        print("No se encontraron mensajes.")
        return menu.menu_mensajes()

    # Muestro los mensajes existentes
    print(
        tabulate(
            list(mensajes[0].items()),
            headers=["Dias", "Mensaje"],
            tablefmt="fancy_grid",
            stralign="center",
        )
    )
    fx.volver_menu(
        "Quiere volver al menu (Y/N): ",
        menu.menu_mensajes,
        menu.menu_principal,
    )


def ver_mensaje() -> None:
    """
    Busca un mensaje mediante el id, si lo encuentra lo mustra en pantalla
    pre: no recibe nada
    post: no devuelve nada
    """
    mensajes = fx.leer_JSON(RUTA)
    id_mensaje = fx.validacion_datos(
        "Ingrese la cantidad de días: ",
        "Ingrese nuevamente la cantidad de dias",
        r"\b([1-9][0-9]{0,2})\b",
    )

    mensaje = mensajes[0].get(id_mensaje, None)
    if mensaje:
        mensaje = {id_mensaje: mensaje}
        print(
            tabulate(
                mensaje.items(),
                headers=["Dias", "Mensaje"],
                tablefmt="fancy_grid",
                stralign="center",
            )
        )
    else:
        print("No se ha encontrado el mensaje")
    fx.volver_menu(
        "Quiere volver al menu (Y/N): ",
        menu.menu_mensajes,
        menu.menu_principal,
    )
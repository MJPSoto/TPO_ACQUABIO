from menues import menues as menu
from funciones import funcionesX as fx
import json
from tabulate import tabulate
import datetime

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
    mensaje = {"cantidad_dias": cantidad_dias, "mensaje": nuevo_mensaje}
    # verificación de que el mensaje ingresado es correcto
    print(
        f"\n{tabulate([mensaje.values()], headers=mensaje.keys(), tablefmt="fancy_grid", stralign="center")}\n"
    )
    fx.volver_menu(
        "¿Los datos ingresados son correctos? (y/n): ", obtener_datos_mensaje
    )
    """
        Esta función retorna 
        {
            "cantidad_dias" : 31,
            "mensaje": "prueba 123"
        }
    """
    return mensaje


def validar_existencia(mensaje: list, mensajes: list) -> None:
    if mensaje in mensajes:
        fx.volver_menu(
            "¿El mensaje ya existe, quiere cargar otro mensaje? (y/n): ",
            menu.menu_mensajes,
            crear_mensaje,
        )


def cargar_archivo(datos_cambiar, access_mode: str):
    try:
        with open(RUTA, access_mode, encoding="utf-8") as archivo:
            json.dump(datos_cambiar, archivo, indent=4, ensure_ascii=False)
    except Exception:
        print("Error al escribir el archivo mensajes.")


def crear_mensaje() -> None:
    """
    Esta funcion toma los datos, comprueba si son validos y los agrega al json
    pre: no recibe nada
    post: no devuelve nada
    """
    # leo el json y lo guardo en la variable mansajes
    dict_mensajes = {key: value for key, value in fx.leer_JSON(RUTA).items()}

    """
        dict_mensajes
        "1": {
            "cantidad_dias": "31",
            "mensaje": "holaaa"
        },
        "2": {
            "cantidad_dias": "31",
            "mensaje": "holaaaa"
        },
        "3": {
            "cantidad_dias": "12",
            "mensaje": "prueba beto"
        }
    """
    mensaje = obtener_datos_mensaje()
    id_mensaje = fx.crear_id(RUTA)
    dict_mensajes[id_mensaje] = mensaje
    cargar_archivo(dict_mensajes, "wt")
    print("Mensaje agregado exitosamente.\n")

    fx.volver_menu(
        "¿Quiere volver a cargar otro mensaje? (y/n): ",
        menu.menu_mensajes,
        crear_mensaje,
    )


def obtener_id_mensaje() -> int:
    while True:
        try:
            id_cliente = int(input("Ingrese el numero del mensaje: "))
            break
        except (ValueError, KeyboardInterrupt) as e:
            print("\nError al ingresar el codigo del usuario...")
    return id_cliente


def actualizar_mensaje() -> None:
    """
    Obtine el mensaje nuevo a travez de la funcion obtener_datos_mensaje, busca la dias
    que es la cantidad de dias, y si está modifica el mensaje
    pre: no recibe nada
    port: no devuelve nada
    """
    if not(fx.leer_JSON(RUTA)):
        fx.volver_menu(
            "¿No se cargaron mensajes, quiere cargar un mensaje? (y/n): ",
            menu.menu_mensajes,
            crear_mensaje,
        )
    mensajes = {key: value for key, value in fx.leer_JSON(RUTA).items()}
    
    """
        mensajes
        {
            "1": {
                "12": "Holaaa"
            },
            "2": {
                "12": "holaaa"
            }
        }
    """
    tabla = [[key, list(value.values())[1]] for key, value in mensajes.items()]
    #muestro los mensajes 
    print("\nMensajes disponibles")
    print(tabulate(tabla, headers=["Nro", "Mensaje"], tablefmt="fancy_grid", stralign="center"))
    # Solicito el id del mensaje
    id_mensaje = obtener_id_mensaje()

    mensaje = mensajes.get(str(id_mensaje), None)
    # Si el mensaje no existe, preguntar si se desea crearlo
    if mensaje is None:
        fx.volver_menu(
            "¿El mensaje no existe, desea crearlo? (y/n): ",
            menu.menu_mensajes,
            crear_mensaje,
        )
    print(tabulate([mensaje.values()], headers=mensaje.keys(), tablefmt="fancy_grid", stralign="center"))
    fx.volver_menu("¿Esta bien el mensaje encontrado? (y/n): ", actualizar_mensaje)

    nuevo_mensaje = obtener_datos_mensaje()

    mensajes[str(id_mensaje)] = nuevo_mensaje

    cargar_archivo(mensajes, "w")
    print("Se actualizo correctamente el mensaje")

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

    mensaje = mensajes.get(id_mensaje, None)

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
    del mensajes[list(mensaje.keys())[0]]

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
            list(mensajes.items()),
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

    mensaje = mensajes.get(id_mensaje, None)
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

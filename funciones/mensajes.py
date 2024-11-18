from menues import menues as menu
from funciones import funcionesX as fx
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
        "^(?=.*[A-Za-z])(?=.{4,})(?!^\d+$).*$",
    )
    cantidad_dias = fx.validacion_datos(
        "Ingrese la cantidad de días: ",
        "Ingrese nuevamente la cantidad de dias",
        "^[1-9][0-9]{0,2}$",
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
    fx.cargar_archivo(
        dict_mensajes, "wt", RUTA, "El mensaje no se pudo insertar en el archivo"
    )
    print("Mensaje agregado exitosamente.\n")

    fx.volver_menu(
        "¿Quiere volver a cargar otro mensaje? (y/n): ",
        menu.menu_mensajes,
        crear_mensaje,
    )


def actualizar_mensaje() -> None:
    """
    Obtine el mensaje nuevo a travez de la funcion obtener_datos_mensaje, busca la dias
    que es la cantidad de dias, y si está modifica el mensaje
    pre: no recibe nada
    port: no devuelve nada
    """
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
    # muestro los mensajes
    print("\nMensajes disponibles")
    print(
        tabulate(
            tabla, headers=["Nro", "Mensaje"], tablefmt="fancy_grid", stralign="center"
        )
    )
    # Solicito el id del mensaje
    id_mensaje = fx.obtener_id(
        "Ingrese el ID del mensaje: ", "El ID ingresado no es valido."
    )

    mensaje = mensajes.get(str(id_mensaje), None)
    # Si el mensaje no existe, preguntar si se desea crearlo
    if mensaje is None:
        fx.volver_menu(
            "¿El mensaje no existe, desea crearlo? (y/n): ",
            menu.menu_mensajes,
            crear_mensaje,
        )
    print(
        tabulate(
            [mensaje.values()],
            headers=mensaje.keys(),
            tablefmt="fancy_grid",
            stralign="center",
        )
    )
    fx.volver_menu("¿Esta bien el mensaje encontrado? (y/n): ", actualizar_mensaje)

    nuevo_mensaje = obtener_datos_mensaje()

    mensajes[str(id_mensaje)] = nuevo_mensaje

    fx.cargar_archivo(mensajes, "w", RUTA, "No se pudo cargar el mensaje en el archivo")
    print("Se actualizo correctamente el mensaje")

    fx.volver_menu(
        "¿Quiere actualizar otro mensaje? (y/n): ",
        menu.menu_mensajes,
        actualizar_mensaje,
    )


def borrar_mensaje() -> str:
    """
    Lee el json encontrando el mensaje que se quiere borrar mediante el Id, vuelve a cargar
    el json con los mensajes excepto el eliminado.
    pre: no recibe nada
    prost: no devuelve nada
    """
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
    if not mensajes:
        fx.volver_menu(
            "¿No se encontraron mensajes, quiere cargar un mensaje? (y/n): ",
            menu.menu_mensajes,
            crear_mensaje,
        )

    tabla = [[key, list(value.values())[1]] for key, value in mensajes.items()]
    # muestro los mensajes
    print("\nMensajes disponibles")
    print(
        tabulate(
            tabla, headers=["Nro", "Mensaje"], tablefmt="fancy_grid", stralign="center"
        )
    )
    # Solicito el id del mensaje
    id_mensaje = fx.obtener_id(
        "Ingrese el ID del mensaje: ", "El ID ingresado no es valido."
    )
    mensaje = mensajes.get(str(id_mensaje), None)

    # Si el mensaje no existe, preguntar si se desea crearlo
    if mensaje is None:
        fx.volver_menu(
            "¿El mensaje no existe, desea crearlo? (y/n): ",
            menu.menu_mensajes,
            crear_mensaje,
        )
    print(
        tabulate(
            [mensaje.values()],
            headers=mensaje.keys(),
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
    del mensajes[str(id_mensaje)]

    # Vuelvo a cargar todo en el JSON
    fx.cargar_archivo(
        mensajes,
        "w",
        RUTA,
        "El mensaje no se pudo cargar en el archivo",
    )
    print("Se elimino el mensaje correctamente")
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
    if not mensajes:
        fx.volver_menu(
            "¿No se encontraron mensajes, quiere cargar un mensaje? (y/n): ",
            menu.menu_mensajes,
            crear_mensaje,
        )

    # Muestro los mensajes existentes
    tabla = [[key, list(value.values())[1]] for key, value in mensajes.items()]
    print(
        tabulate(
            tabla,
            headers=["Nro", "Mensaje"],
            tablefmt="fancy_grid",
            stralign="center",
        )
    )
    fx.volver_menu(
        "Quiere volver al menu (y/n): ",
        menu.menu_mensajes,
        menu.menu_principal,
    )


def ver_mensaje() -> None:
    """
    Busca un mensaje mediante el id, si lo encuentra lo mustra en pantalla
    pre: no recibe nada
    post: no devuelve nada
    """
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
    if not mensajes:
        fx.volver_menu(
            "¿No se encontraron mensajes, quiere cargar un mensaje? (y/n): ",
            menu.menu_mensajes,
            crear_mensaje,
        )
    id_mensaje = fx.obtener_id(
        "Ingrese el ID del mensaje: ", "El ID ingresado no es valido."
    )
    mensaje = mensajes.get(str(id_mensaje), None)
    if mensaje:
        print(
            tabulate(
                [mensaje.values()],
                headers=["Nro", "Mensaje"],
                tablefmt="fancy_grid",
                stralign="center",
            )
        )
    else:
        print("No se ha encontrado el mensaje")
    fx.volver_menu(
        "Quiere volver al menu (y/n): ",
        menu.menu_mensajes,
        menu.menu_principal,
    )

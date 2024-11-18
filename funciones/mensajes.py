from menues import menues as menu
from funciones import funcionesX as fx
from tabulate import tabulate
import textwrap

RUTA = "JSON/mensajes.json"


def obtener_datos_mensaje() -> dict:
    """Esta funcion obtiene los datos del mensaje nuevo, los valida y se almacena como un diccionario de diccionarios
    La primer clave es referente al mensaje N1, su valor contiene la cantidad de días y el mensaje a emitir.
    No recibe parámetros

    Returns:
        dict: Retorna un diccionario
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
    confirmacion = fx.volver_menu(
        "¿Los datos ingresados son correctos? (y/n): ", obtener_datos_mensaje
    )
    """
        Esta función retorna 
        {
        "1": {
            "cantidad_dias": "60",
            "mensaje": "Hola ¿como estas? Te dejamos este recordatorio para cambiar tu filtro"
            }
        }
    """
    if confirmacion:
        return confirmacion
    return mensaje


def crear_mensaje() -> None:
    """Esta función lee todo el JSON mensajes, luego se obtienen los datos para crear el mensaje, se almacenan
    en el JSON y se sobreescriben los datos.

    No recibe parámetros
    Returns:
        None: Retorna None
    """
    # leo el json y lo guardo en la variable mansajes

    dict_mensajes = {key: value for key, value in fx.leer_JSON(RUTA).items()}

    """
        dict_mensajes
        {
            "1": {
                "cantidad_dias": "60",
                "mensaje": "Hola ¿como estas? Te dejamos este recordatorio para cambiar tu filtro"
            },
            "2": {
                "cantidad_dias": "30",
                "mensaje": "Hola como andas? Pasaron 30 días esto es un recordatorio para colocarle sal a su ablandador"
            }
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
    return None


def actualizar_mensaje() -> None:
    """
    Esta función actualiza un mensaje en específico ingresado por el usuario.
    Toma todos los datos del JSON y el usuario ingresa el número del ID para ingresar al mensaje y actualizarlo

    No recibe parámetros
    Returns:
        None: Retorna None
    """
    mensajes = {key: value for key, value in fx.leer_JSON(RUTA).items()}
    """
        mensajes
        {
            "1": {
                "cantidad_dias": "60",
                "mensaje": "Hola ¿como estas? Te dejamos este recordatorio para cambiar tu filtro"
            },
            "2": {
                "cantidad_dias": "30",
                "mensaje": "Hola como andas? Pasaron 30 días esto es un recordatorio para colocarle sal a su ablandador"
            }
        }   
    """
    tabla = [[key, list(value.values())[1]] for key, value in mensajes.items()]
    # muestro los mensajes
    print("\nMensajes disponibles")
    print(
        tabulate(
            tabla, headers=["ID", "Mensaje"], tablefmt="fancy_grid", stralign="center"
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
    fx.volver_menu("¿El mensaje es el que estas buscando? (y/n): ", actualizar_mensaje)

    nuevo_mensaje = obtener_datos_mensaje()

    mensajes[str(id_mensaje)] = nuevo_mensaje

    fx.cargar_archivo(
        mensajes, "wt", RUTA, "No se pudo cargar el mensaje en el archivo"
    )
    print("Se actualizó correctamente el mensaje")

    fx.volver_menu(
        "¿Quiere actualizar otro mensaje? (y/n): ",
        menu.menu_mensajes,
        actualizar_mensaje,
    )
    return None


def borrar_mensaje() -> None:
    """
    Esta función borra un mensaje en específico. Muestra en pantalla todos los datos del JSON, luego se selecciona un ID
    para ingresar a un mensaje determinado. Al seleccionar, se pregunta si se quiere o no borrar ese mensaje.

    No recibe parámetros
    Returns:
        None: Retorna None
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
            tabla, headers=["Días", "Mensaje"], tablefmt="fancy_grid", stralign="center"
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
    return None


def ver_mensajes() -> None:
    """
    Esta función toma todos los datos del JSON e imprime en pantala todos los mensajes que haya cargados.
    En el caso de que no haya, se muestra en pantalla un mensaje informando que no hay mensajes.

    No recibe parámetros
    Returns:
        None: Retorna None
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
            headers=["ID", "Mensaje"],
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
    Esta función toma todos los datos por el JSON, se le pide un ID al usuario para ingresar a un mensaje en específico.
    Al ingresar el ID, se imprime en pantalla el mensaje.

    No recibe parámetros
    Returns:
        None: Retorna None
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
                headers=["Días", "Mensaje"],
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
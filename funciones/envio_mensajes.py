from menues import menues as menu
from funciones import funcionesX as fx
from tabulate import tabulate
from datetime import datetime


CLIENTE_RUTA = "JSON/clientes.json"
MENSAJE_RUTA = "JSON/mensajes.json"


def calcular_dias(fecha_compra) -> int:
    """
    Esta función calcula la diferencia entre la fecha de compra y la fecha actual

    Args:
        fecha_compra (type): Este parámetro tiene como dato la fecha de compra 

    Returns:
        int: Esto devuelve un entero con la diferencia entre ambas fechas
    """
    fecha_compra = datetime.strptime(fecha_compra, "%Y/%m/%d")
    return abs((datetime.now() - fecha_compra).days)


def enviar_mensajes() -> None:
    """ 
    Esta función almacena el numero de celular, nombre y apellido y un mensaje del JSON mensajes dependiendo la fecha que transcurrió para
    poder enviar ese mensaje.
    Se tiene que utilizar librerías como PyWhatKit y PyAutoGUI para poder enviar los mensajes por WhatsApp
    
    No recibe parámetros
    
    Returns:
        None: Retorna None
    """
    dict_mensajes = {key: value for key, value in fx.leer_JSON(MENSAJE_RUTA).items()}
    dict_clientes = {key: value for key, value in fx.leer_JSON(CLIENTE_RUTA).items()}

    # Diccionario final con el número de teléfono como clave
    mensajes_por_cliente = {}

    if not dict_clientes or not dict_mensajes:
        pass  # Manejar casos donde los datos sean vacíos

    for cliente in dict_clientes.values():
        fecha_compra = cliente["fecha_compra"]
        dias_transcurridos = calcular_dias(fecha_compra)
        mensajes = []

        for mensaje in dict_mensajes.values():
            cantidad_dias = int(mensaje["cantidad_dias"])
            if dias_transcurridos >= cantidad_dias:
                mensajes.append(mensaje["mensaje"])
        if mensajes:
            # Crear entrada en el diccionario para este cliente
            numero_telefono = cliente["telefono"]
            mensajes_por_cliente[numero_telefono] = {
                "nombre": cliente["nombre"],
                "mensajes": mensajes,
            }
    if not mensajes_por_cliente:
        fx.volver_menu(
            "Ningun cliente cumple con las condiciones para el envio del mensajes, desea volver al menu? (y/n): ",
            exit,
            menu.menu_principal,
        )
    # Convertir el diccionario a una lista de listas para tabular
    tabla = [
        [telefono, datos["nombre"], "\n".join(datos["mensajes"])]
        for telefono, datos in mensajes_por_cliente.items()
    ]
    print("\nEstos son los mensajes a enviar\n")
    # Mostrar la tabla
    print(
        tabulate(
            tabla,
            headers=["Teléfono", "Nombre", "Mensajes"],
            tablefmt="fancy_grid",
            stralign="center",
        )
    )
    fx.volver_menu(
        "Desea volver al menu? (y/n): ",
        exit,
        menu.menu_principal,
    )
    return None
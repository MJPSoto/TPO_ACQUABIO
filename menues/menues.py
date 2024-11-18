from variables import constantes as cs
from funciones import funcionesX as fx, mensajes as fm, productos as fp, clientes as fc, envio_mensajes as em
from termcolor import colored
import time


def menu_opciones(menu_desplegar: int) -> int:
    """
    Está función muestra las opciones del menu que haya seleccionado el usuario y devuelve el siguiente menu
    Pre: Está función recibe como parametro en formato entero que representa el menu seleccionado
    Post: Está funcion devuelve un entero que representa el siguiente menu
    """
    while True:
        fx.clear_console()
        fx.mostrar_logo()
        fx.mostrar_opciones(cs.dict_opciones, menu_desplegar)
        try:
            option = int(input("Seleccione una de las opciones: "))
            if not (option in cs.dict_opciones[menu_desplegar].keys()):
                raise ValueError()
            break
        except (ValueError, KeyboardInterrupt):
            print(colored("Opción ingresada no valida...", "red"))
            time.sleep(1)
    return option



def menu_clientes() -> None:
    """
    Está función muestra las opciones para un crud (crear un cliente, leer datos del cliente, modificar un cliente y borrar cliente)
    Pre: Está función no recibe ningun parametro
    Post: Está función no devuelve nada
    """
    option_select = menu_opciones(1)
    match option_select:
        case 1:
            fc.crear_nuevo_cliente()
        case 2:
            fc.actualizar_datos_cliente()
        case 3:
            fc.borrar_cliente()
        case 4:
            fc.ver_datos_cliente()
        case 5:
            fc.mostrar_clientes()
        case 6:
            menu_principal()


def menu_producto() -> None:
    """
    Está función muestra las opciones para un crud (crear un producto, leer datos de un producto,
    modificar un producto y borrar producto)
    Pre: Está función no recibe ningun parametro
    Post: Está función no devuelve nada
    """
    option_select = menu_opciones(2)
    match option_select:
        case 1:
            fp.crear_producto()
        case 2:
            fp.actualizar_producto()
        case 3:
            fp.borrar_producto()
        case 4:
            fp.ver_producto()
        case 5:
            fp.ver_productos()
        case 6:
            menu_principal()


def menu_mensajes() -> None:
    """
    Está función muestra las opciones para un crud (crear un mensaje, leer datos de un mensaje,
    modificar un mensaje y borrar mensaje)
    Pre: Está función no recibe ningun parametro
    Post: Está función no devuelve nada
    """
    option_select = menu_opciones(3)
    match option_select:
        case 1:
            fm.crear_mensaje()
        case 2:
            fm.actualizar_mensaje()
        case 3:
            fm.borrar_mensaje()
        case 4:
            fm.ver_mensaje()
        case 5:
            fm.ver_mensajes()
        case 6:
            menu_principal()


def menu_principal() -> None:
    """
    Está función es el menu principal donde se inicia el programa, desde aca pasa a los siguientes menues
    Pre: Está función no recibe ningun parametro
    Post: Está función no devuelve nada
    """
    option_select = menu_opciones(0)
    match option_select:
        case 1:
            menu_clientes()
        case 2:
            menu_mensajes()
        case 3:
            menu_producto()
        case 4:
            em.enviar_mensajes()
        case 5:
            exit()

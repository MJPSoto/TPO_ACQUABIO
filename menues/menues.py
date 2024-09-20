from tabulate import tabulate
from variables import constantes as cs
from funciones import funcionesX as fx, mensajes as fm, productos as fp, clientes as fc


def menu_opciones(menu_desplegar: int) -> int:
    fx.clear_console()
    while True:
        try:
            print(
                tabulate(
                    [["Sistema de avisos ACQUABIO"], ["by Cocucha"]],
                    tablefmt="fancy_grid",
                    colalign=("center",),
                )
            )
            fx.mostrar_opciones(cs.dict_opciones, menu_desplegar)
            option = int(input("Seleccione una de las opciones: "))
            if not (option in cs.dict_opciones[menu_desplegar].keys()):
                raise ValueError("Opción ingresada no valida")
            break
        except ValueError as e:
            print(f"{e}")
            fx.clear_console()
    return option


def menu_principal():
    option_select = menu_opciones(0)
    match option_select:
        case 1:
            menu_clientes()
        case 2:
            menu_mensajes()
        case 3:
            menu_producto()
        case 4:
            exit()
        case _:
            print("Opción no valida")
    return None


def menu_clientes():
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
        case _:
            print("Opción no valida")
    return None


def menu_producto():
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
        case _:
            print("Opción no valida")
    return None


def menu_mensajes():
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
        case _:
            print("Opción no valida")
    return None

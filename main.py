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
            if not (option in cs.dict_opciones.keys()):
                print(cs.dict_opciones[menu_desplegar].values())
                raise ValueError("Opción ingresada no valida")
            break
        except ValueError as e:
            print(f"{e}")
            fx.clear_console()
    return option


def menu_options_recursivo(op: int) -> None:
    if op in cs.dict_opciones[op].keys():
        option = menu_opciones(op)
    return option


def main():
    option = menu_opciones(0)
    option = menu_options_recursivo(option)

if __name__ == "__main__":
    main()

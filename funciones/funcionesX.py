from tabulate import tabulate
from collections.abc import Sequence
import json
import os


def clear_console() -> None:
    """
    Está función limpia la consola 
    pre: esta función no recibe ningun parametro
    post: esta función no devuelve nada
    """
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_opciones(dict_opciones: dict[int, str], option: int) -> None:
    """
    Está función muestra las opciones disponibles de cada menu
    Pre: Está función no recibe 2 parametros, uno es un diccionario que contiene las opciones y
    el otro es el que muestra el diccionario
    Post: Está función no devuelve nada
    """
    data = [[key, value] for key, value in dict_opciones[option].items()]
    print(
        tabulate(
            data, headers=["N°1", "Opción"], tablefmt="fancy_grid", stralign="center"
        )
    )

def mostrar_logo() -> None:
    """
    Está función muestra el logo del programa
    Pre: Está función no recibe ningun parametro
    Post: Está función no devuelve nada
    """
    print(
        tabulate(
            [["Sistema de avisos ACQUABIO"], ["by Cocucha"]],
            colalign=("center",),
        )
    )

def leer_JSON(path: str) -> None:
    try:
        with open(path, "r") as archivo:
            clientes = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        clientes = []
    return clientes
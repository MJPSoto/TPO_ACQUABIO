from tabulate import tabulate
import os

def clear_console() -> None:
    """
    contrato: esta función limpia la consola
    pre: esta función no obtiene ningun parametro
    post: esta función no devuelve nada None
    """
    os.system("cls" if os.name == "nt" else "clear")


def mostrar_menu(key: int, dict_opciones: dict) -> None:
    for i, value in enumerate(dict_opciones[key]):
        print(f"{i+1}. {value}")
    return None


def mostrar_opciones(dict_opciones: dict, option: int) -> None:
    print(
        tabulate(
            [[f"{i+1}. {valor}" for i, valor in enumerate(dict_opciones[option].values())]],
            tablefmt="fancy_grid",
        )
    )
    return None

#aca paso la funcion leer json para hacer los llamados en general
def leer_JSON(ruta):
    """
    esta funcion lee la el archivo dela ruta y genera una lista con los datos

    pre: esta funcion recive como parametro una ruta de archivo de json

    post: si en cuentra el archivo devuelve una lista de diccionarios 
    y sino devielve una lista vacia
    """
    archivo_path = ruta
    try:
        with open(archivo_path, "r") as archivo:
            datos = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        datos = []
    return datos



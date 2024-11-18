from tabulate import tabulate
from collections.abc import Sequence
import json
import re
import os
from menues import menues as menu


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
            data, headers=["N°", "Opción"], tablefmt="fancy_grid", stralign="center"
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

def escribir_archivo_vacio(path: str):
    with open(path, "w", encoding="utf-8") as archivo:
        archivo.write("{}")

def leer_JSON(path: str) -> dict:
    try:
        with open(path, "rt", encoding="utf-8") as archivo:
            clientes = json.load(archivo)
    except FileNotFoundError:
        escribir_archivo_vacio(path)
        clientes = {}
    if not clientes:
        escribir_archivo_vacio(path)
    return clientes


def volver_menu(mensaje: str, funtion_no, funtion_si=None) -> None:
    """
    Pregunta si quiere volver al menú. Te lleva al menú principal si ingresa "y" y te lleva al menu mensajes
    si ingresa "n".
    pre: Esta función recibe como parametro una función y un mensaje en formato str
    post: no devuelve nada
    """
    opciones = {
        "y": funtion_si,
        "n": funtion_no,
    }
    try:
        option = input(mensaje).strip().lower()
    except KeyboardInterrupt:
        print("\nno se permite interrupciones")
        volver_menu("Quiere volver al menu principal? (Y/N): ", funtion_no, funtion_si)
    seleccion = opciones.get(option, funtion_no)
    if seleccion:
        seleccion()


def validacion_datos(mensaje: str, mensaje_error: str, expretion: str):
    while True:
        try:
            dato_verificar = input(mensaje)
            if re.match(expretion, dato_verificar):
                break
            else:
                print(mensaje_error)
        except KeyboardInterrupt:
            print("\nNo se permite interrupciones")
    return dato_verificar

def crear_id(ruta: str) -> int:
    """Esta funcion lee el JSON y guarda los datos en una lista. Verifica si hay algun valor en "id"
    Si no lo hay, guardamos 0 en la lista, caso contrario, el mayor dato encontrado en "id".
    Retornamos
    Returns:
        bool: Retorna una tupla con el id
    """
    return max(list(map(int, list(leer_JSON(ruta).keys()))), default=0) + 1

def cargar_archivo(datos_cambiar, access_mode: str, ruta: str, mensaje: str):
    try:
        with open(ruta, access_mode, encoding="utf-8") as archivo:
            json.dump(datos_cambiar, archivo, indent=4, ensure_ascii=False)
    except Exception:
        print(mensaje)

def obtener_id(msj_input: str, msj_error: str) -> int:
    try:
        id = int(input(msj_input))
    except (ValueError, KeyboardInterrupt) as e:
        print(f"\n{msj_error}")
        obtener_id(msj_input, msj_error)
    return id

from tabulate import tabulate
from collections.abc import Sequence
import json
import re
import os
from menues import menues as menu


def clear_console() -> None:
    """
    Está función limpia la consola
    Esta función no recibe ningun parametro
    Returns:
        None: Retorna None
    """
    os.system("cls" if os.name == "nt" else "clear")
    return None


def mostrar_opciones(dict_opciones: dict[int, str], option: int) -> None:
    """Esta funcion muestra las opciones disponibles

    Args:
        dict_opciones (dict[int, str]): Se le pasa como parámetro un diccionario con datos enteros como key y str de valores_
        option (int): El segundo parámetro son las opciones
        
    Returns:
        None: Retorna None
    """
    data = [[key, value] for key, value in dict_opciones[option].items()]
    print(
        tabulate(
            data, headers=["N°", "Opción"], tablefmt="fancy_grid", stralign="center"
        )
    )
    return None


def mostrar_logo() -> None:
    """
    Esta función muestra el logo del programa
    No recibe parámetros
    Returns:
        None: Retorna None
    """
    print(
        tabulate(
            [["Sistema de avisos ACQUABIO"], ["by Cocucha"]],
            colalign=("center",),
        )
    )
    return None


def escribir_archivo_vacio(path: str) -> None:
    """Esta función crea diccionarios vacíos en los archivos JSON si es que estos están vacíos.

    Args:
        path (str): Recibe como parámetro una ruta

    Returns:
        None: Retorna None
    """
    with open(path, "w", encoding="utf-8") as archivo:
        archivo.write("{}")
    return None


def leer_JSON(path: str) -> dict:
    """Esta función es la encargada de leer los archivo JSON cuando se la llame

    Args:
        path (str): Se pasa como argumento una ruta donde se encuentre el archivo

    Returns:
        dict: Retorna un diccionario con datos o vacío
    """
    try:
        with open(path, "r", encoding="utf-8") as archivo:
            clientes = json.load(archivo)
    except FileNotFoundError:
        escribir_archivo_vacio(path)
        clientes = {}
    except json.JSONDecodeError as e:
        escribir_archivo_vacio(path)
        clientes = {}
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
        volver_menu("¿Quiere volver al menu principal? (Y/N): ", funtion_no, funtion_si)
    seleccion = opciones.get(option, funtion_no)
    if seleccion:
        seleccion()
    return None


def validacion_datos(mensaje: str, mensaje_error: str, expretion: str) -> str:
    """Esta funcion verifica un dato ingresado por teclado.

    Args:
        mensaje (str): Mensaje muestra el dato que el usuario tiene que cargar
        Ejemplo: "Ingrese su nombre y apellido"

        mensaje_error (str): Este se muestra si el mensaje ingresado es incorrecto
        "Ingrese nuevamente el nombre y apellido"

        expretion (str): Por cada funcion que se utilice, la expresion regular va cambiando
        "[A-Za-z\s]{3,}$"

    Returns:
        str: Retorna el dato ya verificado
    """
    while True:
        try:
            dato_verificar = input(mensaje)
            if re.match(expretion, dato_verificar):
                break
            else:
                print(mensaje_error)
        except KeyboardInterrupt:
            print("\nNo se permite interrupciones")
        # esto retorna por ejemplo un nombre: Agustin Villavicencio
    return dato_verificar


def crear_id(ruta: str) -> int:
    """Esta funcion lee el JSON y guarda los datos en una lista. Verifica si hay algun valor en "id"
    Si no lo hay, guardamos 1 en la lista, caso contrario, el mayor dato encontrado en "id".
    
    Returns:
        int: Retorna un entero como valor del ID
    """
    return max(list(map(int, list(leer_JSON(ruta).keys()))), default=0) + 1


def cargar_archivo(
    datos_cambiar: dict, access_mode: str, ruta: str, mensaje: str
) -> None:
    """Esta función carga o sobre escribe archivos JSON

    Args:
        datos_cambiar (dict): Se pasa como primer parámetro un diccionario con los datos que se quieren cambiar
        access_mode (str): Se pasa como access mode "wt" para cargar o sobreescribir el json
        ruta (str): Se pasa la ruta donde está el JSON
        mensaje (str): Se muestra un mensaje si el archivo no se pudo cargar

    Returns:
        None: Retorna None
    """
    try:
        with open(ruta, access_mode, encoding="utf-8") as archivo:
            json.dump(datos_cambiar, archivo, indent=4, ensure_ascii=False)
    except Exception:
        print(mensaje)
    return None


def obtener_id(msj_input: str, msj_error: str) -> int:
    """En esta función se obtiene el ID de un cliente en particular ingresado por teclado.
    Args:
        msj_input (str): Se muestra lo que se le pide al usuario
        msj_error (str): Se muestra un mensaje de error

    Returns:
        int: Se retorna un int correspondiente al id del cliente
    """
    try:
        id = int(input(msj_input))
    except (ValueError, KeyboardInterrupt) as e:
        print(f"\n{msj_error}")
        return obtener_id(msj_input, msj_error)
    return id

from random import randint
from menues import menues as menu
from tabulate import tabulate
import re
import json
import datetime


def verificar_nombre(nombre_completo:str) -> bool:
    """En esta funcion verificamos si el nombre del cliente es valido

    Args:
        nombre (str): Ingreso nombre y apellido del cliente

    Returns:
        bool: retorno true si se cumplen las condiciones
    """
    nombre_valido = "[A-Za-z\s]+$"
    while True:
        verificacion = re.match(nombre_valido, nombre_completo)
        if verificacion:
            return True
        else:
            print("Nombre invalido, ingrese solo caracteres alfabeticos y no termine con espacios")
            
            
def verificar_telefono(telefono:int) ->bool:
    """Esta funcion verifica si un numero es valido

    Args:
        telefono (int): le paso como parametro un numero que por lo menos tenga 10 digitos y sea positivo

    Returns:
        bool: retorna true si se cumple y false si no
    """
    if len(telefono) == 10 and telefono > 0:
        return True
    return False


def verificar_direccion(direccion:str)-> bool:
    """Esta funcion verifica si la direccion tiene algun dato

    Args:
        direccion (str): Recibo datos tipo string

    Returns:
        bool: retorno true si la longitud tiene al menos cuatro caracteres
    """
    if len(direccion) >= 4:
        return True
    return False
    pass


def fecha_compra() ->bool:
    """En esta funcion verifico si la fecha ingresada es valida

    Args:
        No recibe argumentos

    Returns:
        bool: retorno true si es valida
    """
    while True:
        anio = int(input("Ingrese el anio de la compra: "))
        mes = int(input("Ingrese el mes de la compra: "))
        dia = int(input("Ingrese el dia de la compra: "))
        fecha_compra = datetime.date(anio, mes, dia)
        if fecha_compra:
            return True
        else:
            print("Fecha invalida, ingrese nuevamente los datos")


def verificar_id_cliente(id_cliente:str) ->bool:
    """_summary_

    Args:
        id_cliente (str): _description_

    Returns:
        bool: _description_
    """
    clientes = leer_JSON()
    if id_cliente != clientes["id"]:
        return True
    return False
    
    
    
def leer_JSON():
    archivo_path = "JSON/clientes.json"

    try:
        with open(archivo_path, "r") as archivo:
            clientes = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        clientes = []
    return clientes

def verificar_celular(celular: str) -> bool:
    patron = r"^\d{2}\s\d{4}-\d{4}$"
    return bool(re.match(patron, celular))


def obtener_datos_cliente():
    """
    Está función obtiene los datos del cliente por consola

    pre: Está función no necesita parametros

    post: Esta función devuelve un diccionario con los datos del cliente
    """
    nombre = input("Ingrese el nombre del cliente: ")
    while True:
        telefono = input("Ingrese el teléfono del cliente (Ej: 11 1234-5678): ")
        if verificar_celular(telefono):
            break
        else:
            print("Teléfono no válido. Intente de nuevo.")
    direccion = input("Ingrese la dirección del cliente: ")
    localidad = input("Ingrese la localidad del cliente: ")
    fecha_compra = fecha_compra()
    id_cliente = randint(10000, 99999)
    nuevo_cliente = {
        "id": id_cliente,
        "nombre": nombre,
        "telefono": telefono,
        "direccion": direccion,
        "localidad": localidad,
        "fecha_compra": fecha_compra,
    }
    return nuevo_cliente
from random import randint
from menues import menues as menu
from tabulate import tabulate
import re
import json
import datetime


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
    if len(direccion) > 4:
        return True
    return False
    pass

def verificar_fecha_compra(fecha_compra:str) ->bool:
    pass


def verificar_id_cliente(id_cliente:str) ->bool:
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
    fecha_compra = datetime.datetime.now().strftime("%Y-%m-%d")
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
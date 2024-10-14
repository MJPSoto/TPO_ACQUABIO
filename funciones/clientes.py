from menues import menues as menu
from tabulate import tabulate
import re
import json
from datetime import date


def ingresar_nombre() -> str:
    while True:
        try:
            nombre = input("Ingrese su nombre y apellido: ")
            if verificar_nombre(nombre):
                print("Nombre valido")
        except ValueError:
            print("Ingrese correctamente el nombre y apellido")
        return nombre

def verificar_nombre(nombre:str) -> bool:
    """En esta funcion verificamos si el nombre del cliente es valido

    Args:
        No recibe argumentos

    Returns:
        retorno el nombre y apellido del cliente
    """
    flag = False
    nombre_valido = r'^(?=.{3,})[A-Za-z\s]+$'
    while True:
        try:
            if re.match(nombre_valido, nombre):
                flag = True
        except ValueError:
            print("Ingrese un nombre valido")
        return flag


def ingresar_telefono()-> str:
    while True:
        try:
            telefono = input("Ingrese su numero de telefono. Ejemplo 1122334455: ")
            if verificar_telefono(telefono):
                print("Numero valido")
        except ValueError:
            print("Ingrese un numero valido")
        return telefono


def verificar_telefono(telefono: str) -> bool:
    """Esta funcion verifica si un numero es valido

    Args:
        telefono (int): le paso como parametro un numero que por lo menos tenga 10 digitos y sea positivo

    Returns:
        bool: retorna true si se cumple y false si no
    """
    flag = False
    telefono_valido = r'^(?=.{10})\d{10}$'
    while True:
        try:
            if re.fullmatch(telefono_valido, telefono):
                flag = True
        except Exception as e:
            print("Ingrese un telefono valido, ejemplo: 1122334455")
        return flag
    

def ingresar_direccion() -> str:
    while True:
        try:
            direccion = input("Ingrese su direccion: ")
            if verificar_direccion(direccion):
                print("Direccion valida")
        except ValueError:
            print("Ingrese una direccion valida")
        return direccion


def verificar_direccion(direccion: str) -> bool:
    """Esta funcion verifica si la direccion tiene algun dato

    Args:
        direccion (str): Recibo datos tipo string

    Returns:
        bool: retorno true si la longitud tiene al menos cuatro caracteres
    """
    flag = False
    direccion_valida = "[A-Za-z\s]+$"
    while True:
        try:
            if re.match(direccion_valida, direccion):
                flag = True
        except ValueError: 
            print("Ingrese datos validos")
        return flag


def ingresar_fecha_compra():
    while True:
        try:
            anio = int(input("Ingrese el anio: "))
            if anio > 0:
                mes = int(input("Ingrese el mes: "))
                if mes > 0 and mes < 13:
                    dia = int(input("Ingrese el dia: "))
                    fecha_compra = verificar_fecha_compra(anio, mes, dia)
                    if fecha_compra:
                        print("Fecha valida")
                        break
        except ValueError:
            print("Ingrese una fecha valida")
        return fecha_compra


def verificar_fecha_compra(a:int, b:int, c:int) -> bool:
    flag = False
    while True:
        try:
            fecha = date(a, b, c)
            if fecha:
                print("Fecha valida")
                flag = True
        except ValueError:
            print("Ingrese bien los datos")
        return flag


def id_cliente() -> tuple:
    """
    En esta funcion se genera el id de los clientes
    En el caso de no tener datos en el archivo json, el id se inicializa en 1
    Sino se lee el archivo json, se guardan en una lista, se busca el máximo y se le suma 1 para el próximo cliente
    
    Args:
        No recibe argumentos
    
    Returns:
        Tuple: retorna una tupla con el dato del id del cliente

    """
    leer_json = leer_JSON()
    ids = []
    if len(leer_json) > 0: 
        for i in leer_json:
            ids.append(i["id"])
    else:
        ids.append(0)
    maximo = max(ids)
    nuevo_id = maximo + 1
    return (nuevo_id)


def obtener_datos_cliente():
    """
    Está función obtiene los datos del cliente por consola

    pre: Está función no necesita parametros

    post: Esta función devuelve un diccionario con los datos del cliente
    """
    nombre = ingresar_nombre()
    telefono = ingresar_telefono()
    direccion = ingresar_direccion()
    localidad = "holis"
    fecha = ingresar_fecha_compra()
    ide = id_cliente()
    
    nuevo_cliente = {
        "id": ide,
        "nombre": nombre,
        "telefono": telefono,
        "direccion": direccion,
        "localidad": localidad,
        "fecha_compra": fecha,
    }
    return nuevo_cliente



def leer_JSON():
    archivo_path = "JSON/clientes.json"

    try:
        with open(archivo_path, "r") as archivo:
            clientes = json.load(archivo)
    except (FileNotFoundError, json.JSONDecodeError):
        clientes = []
    return clientes


def crear_nuevo_cliente() -> None:
    """
    Está función carga un nuevo cliente al json de clientes

    pre: Está función no necesita parametros

    post: Esta función Guarda un nuevo cliente en el archivo clientes.json.
    """

    # Solicitar datos del cliente
    clientes = leer_JSON()
    clientes.append(obtener_datos_cliente())

    with open("JSON/clientes.json", "w") as archivo:
        json.dump(clientes, archivo, indent=4)
    print("Cliente agregado exitosamente.")
    menu.menu_clientes()
    return None


def actualizar_datos_cliente():
    """
    Está función actualiza los datos de un cliente en particular

    pre: Está función no necesita parametros

    post: Esta función actualiza los datos de un cliente en el archivo json
    """

    while True:
        try:
            id_cliente = int(input("Ingrese el ID del cliente: "))
            break
        except ValueError as e:
            print(f"Error{e}")
    clientes = leer_JSON()
    if not clientes:
        print("No se encontraron clientes")
        menu.menu_clientes()
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            nuevos_datos = obtener_datos_cliente()
            for key, value in nuevos_datos.items():
                if key != "id":
                    cliente[key] = value
            with open("JSON/clientes.json", "w") as archivo:
                json.dump(clientes, archivo, indent=4)
            print("Cliente actualizado correctamente.")
            menu.menu_clientes()
    return None


def borrar_cliente():
    """
    Está función borra un cliente del la lista de clientes

    pre: Está función no necesita parametros

    post: Esta función borra un cliente del archivo json de clientes
    """
    while True:
        try:
            id_cliente = int(input("Ingrese el ID del cliente: "))
            break
        except ValueError as e:
            print(f"Error{e}")
    clientes = leer_JSON()
    if not clientes:
        print("No se encontraron clientes")
        menu.menu_clientes()
    clientes_actualizados = [
        cliente for cliente in clientes if cliente["id"] != id_cliente
    ]

    if len(clientes) == len(clientes_actualizados):
        print("Cliente no encontrado.")
    else:
        with open("JSON/clientes.json", "w") as archivo:
            json.dump(clientes_actualizados, archivo, indent=4)
        print("Cliente borrado correctamente.")

    menu.menu_clientes()
    return None


def mostrar_clientes():
    """
    Está función muestra todos los clientes

    pre: Está función no necesita parametros

    post: Esta función lista todos los clientes que existen en el archivo json clientes
    """
    clientes = leer_JSON()
    if not clientes:
        print("No se encontraron clientes")
        menu.menu_clientes()
    print(tabulate(clientes, headers="keys"))
    return None


def ver_datos_cliente():
    """
    Mostrar datos del cliente con ese id
    """
    pass

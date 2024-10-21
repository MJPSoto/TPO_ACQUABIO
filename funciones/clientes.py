from random import randint
from menues import menues as menu
from tabulate import tabulate
import re
import json
import datetime


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


def ver_datos_cliente() -> None:
    """
    Mostrar datos del cliente con ese id

    pre:esta funcion no recibe parametros

    post: esta funcion muestra en pantalla los datos de un cliente segun el id soliciado
    """
    clientes = leer_JSON()
    while True:
        #se solicita el id del cliente
        id_cliente = input("Ingrese el ID del cliente:")

        # Usar re para verificar que el ID tenga exactamente 5 dígitos
        if re.fullmatch(r'\d{5}', id_cliente):
            break
        else:
            print("ID invalido")
    #se busca en la lista de clientes el ID del cliente
    cliente = next((c for c in clientes if c['id'] == int(id_cliente)), None)
    #en caso de encontrarlo, lo muestra en pantalla, en el contrario, avisa al usuario que no existe
    if cliente:
        print(tabulate([cliente], headers="keys", tablefmt="grid"))
    else:
        print(f"no existe un cliente con el ID {id_cliente}.")
    menu.menu_clientes()
    return None

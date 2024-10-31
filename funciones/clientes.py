from menues import menues as menu
from funciones import funcionesX as fx
from tabulate import tabulate
import re
import json
import datetime

# declaro la ruta que voy a usar para la funcion leer json
ruta = "JSON/clientes.json"


def validacion_datos(mensaje: str, mensaje_error: str, expretion: str):
    while True:
        dato_verificar = input(mensaje)
        if re.match(expretion, dato_verificar):
            break
        else:
            print(mensaje_error)
    return dato_verificar


def ingresar_fecha_compra() -> None:
    patron_date = "^(?:\\d{4})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$"
    while True:
        date = input("Ingrese la fecha. Ejemplo: 20240608: ")
        if re.match(patron_date, date):
            date = datetime.date(
                int(date[:4]), int(date[4:6]), int(date[6:8])
            ).strftime("%Y/%m/%d")
            return date
        else:
            print("Fecha no valida.")


def verificar_ciudades_disponibles(codigo_postal: str) -> str:
    localidades = fx.leer_JSON("TPO_ACQUABIO/JSON/ciudades.json")
    key_value = {"100100": "Otro"}
    for key, valor in localidades.items():
        if key == codigo_postal:
            key_value = {key: valor}
    return key_value


def crear_id_cliente() -> tuple:
    """Esta funcion lee el JSON y guarda los datos en una lista. Verifica si hay algun valor en "id"
    Si no lo hay, guardamos 0 en la lista, caso contrario, el mayor dato encontrado en "id".
    Retornamos

    Returns:
        bool: Retorna una tupla con el id
    """
    return max(list(cliente["id"] for cliente in fx.leer_JSON(ruta))) + 1


def obtener_datos_cliente() -> dict:
    """
    Está función obtiene los datos del cliente por consola

    pre: Está función no necesita parametros

    post: Esta función devuelve un diccionario con los datos del cliente
    """
    ide = crear_id_cliente()
    nombre = validacion_datos(
        "Ingrese su nombre y apellido: ",
        "Ingrese nuevamente el nombre",
        "[A-Za-z\s]{3,}$",
    )
    telefono = validacion_datos(
        "Ingrese su numero de telefono. Ejemplo: 1122334455: ",
        "Ingrese nuevamente el telefono.",
        "[0-9\s]{10}$",
    )
    codigo_postal = validacion_datos(
        "Ingrese su codigo postal: ",
        "Ingrese nuevamente su codigo postal.",
        "[0-9\s]{4}$",
    )
    direccion = validacion_datos(
        "Ingrese su direccion: ",
        "Ingrese nuevamente su direccion.",
        "^[a-zA-Z0-9\s]+$",
    )

    fecha_compra = ingresar_fecha_compra()

    codigo_postal = verificar_ciudades_disponibles(codigo_postal)

    nuevo_cliente = {
        "id": ide,
        "nombre": nombre,
        "telefono": telefono,
        "ciudad": codigo_postal,
        "direccion": direccion,
        "fecha_compra": fecha_compra,
    }
    return nuevo_cliente


def crear_nuevo_cliente() -> None:
    """
    Está función carga un nuevo cliente al json de clientes

    pre: Está función no necesita parametros

    post: Esta función Guarda un nuevo cliente en el archivo clientes.json.
    """
    # Solicitar datos del cliente
    clientes = fx.leer_JSON(ruta)
    """
    Ejemplo de lo que devuelve la funcion leer_JSON
    [
        {
            "id": 5,
            "nombre": "Mateo",
            "telefono": "1122334455",
            "ciudad": {
                "7167": "Pinamar"
            },
            "direccion": "Casa de mateo",
            "fecha_compra": "2024/08/06"
        }
    ]
    """
    clientes.append(obtener_datos_cliente())
    try:
        with open(ruta, "w") as archivo:
            json.dump(clientes, archivo, indent=4)
    except Exception:
        print("Error al escribir el archivo clientes.")
    print("Cliente agregado exitosamente.")
    menu.menu_clientes()


def actualizar_datos_cliente() -> None:
    """
    Está función actualiza los datos de un cliente en particular

    pre: Está función no necesita parametros

    post: Esta función actualiza los datos de un cliente en el archivo json
    """
    id_cliente = obtener_id_cliente()
    clientes = fx.leer_JSON(ruta)
    if not clientes:
        print("No se encontraron clientes")
        menu.menu_clientes()
    datos_cliente = encontrar_cliente(id_cliente)
    print(tabulate(datos_cliente.items()))
    nuevos_datos = obtener_datos_cliente()
    """
    for key, value in nuevos_datos.items():
        if key != "id":
            cliente[key] = value
    with open(ruta, "w") as archivo:
        json.dump(clientes, archivo, indent=4)
    print("Cliente actualizado correctamente.")
    menu.menu_clientes()
    """


def mostrar_clientes() -> None:
    """
    Está función muestra todos los clientes

    pre: Está función no necesita parametros

    post: Esta función lista todos los clientes que existen en el archivo json clientes
    """
    clientes = fx.leer_JSON(ruta)
    if not clientes:
        print("No se encontraron clientes")
        menu.menu_clientes()
    print(tabulate(clientes, headers="keys"))


def obtener_id_cliente() -> int:
    while True:
        try:
            id_cliente = int(input("Ingrese el numero del usuario: "))
            return id_cliente
        except ValueError as e:
            print("El numero de usuario no existe.")


def borrar_cliente() -> None:
    """
    Está función borra un cliente del la lista de clientes

    pre: Está función no necesita parametros

    post: Esta función borra un cliente del archivo json de clientes
    """
    id_cliente = obtener_id_cliente()
    clientes = fx.leer_JSON(ruta)
    if not clientes:
        print("No se encontraron clientes")
        menu.menu_clientes()
    clientes_actualizados = [
        cliente for cliente in clientes if cliente["id"] != id_cliente
    ]

    if len(clientes) == len(clientes_actualizados):
        print("Cliente no encontrado.")
    else:
        try:
            with open(ruta, "w") as archivo:
                json.dump(clientes_actualizados, archivo, indent=4)
        except Exception:
            print("Error al escribir el archivo clientes.")
        print("Cliente borrado correctamente.")


def encontrar_cliente(id_cliente: int):
    clientes = fx.leer_JSON(ruta)
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            return cliente
    return []


def ver_datos_cliente() -> None:
    """
    Mostrar datos del cliente con ese id
    """
    id_cliente = obtener_id_cliente()
    datos_cliente = encontrar_cliente(id_cliente)
    if datos_cliente:
        tabla = [list(datos_cliente.values())]
        # Mostrar la tabla con claves como encabezados
        print(
            tabulate(
                tabla,
                headers=datos_cliente.keys(),
                tablefmt="fancy_grid",
                stralign="center",
            )
        )
    else:
        print("No se ha encontrado el cliente.")

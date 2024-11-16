from menues import menues as menu
from funciones import funcionesX as fx
from tabulate import tabulate
import re
import json
import datetime

# declaro la ruta que voy a usar para la funcion leer json
RUTA = "JSON/clientes.json"


def validacion_datos(mensaje: str, mensaje_error: str, expretion: str):
    while True:
        dato_verificar = input(mensaje)
        if re.match(expretion, dato_verificar):
            break
        else:
            print(mensaje_error)
    return dato_verificar


def ingresar_fecha_compra() -> str:
    patron_date = "^(?:\\d{4})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$"
    while True:
        date = input("Ingrese la fecha. Ejemplo: 20240608: ")
        if re.match(patron_date, date):
            date = datetime.date(
                int(date[:4]), int(date[4:6]), int(date[6:8])
            ).strftime("%Y/%m/%d")
            break
    return date

def verificar_ciudades_disponibles(codigo_postal: str) -> str:
    localidades = fx.leer_JSON("JSON/ciudades.json")
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
    return max(list(map(int, list(fx.leer_JSON(RUTA).keys()))), default=0) + 1


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
        "[0-9\s]{3,}$",
    )
    direccion = validacion_datos(
        "Ingrese su direccion: ",
        "Ingrese nuevamente su direccion.",
        "^[a-zA-Z0-9\s]{4,}$",
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

def cargar_archivo(datos_cambiar, access_mode: str):
    try:
        with open(RUTA, access_mode, encoding='utf-8') as archivo:
            json.dump(datos_cambiar, archivo, indent=4, ensure_ascii=False)
    except Exception:
        print("Error al escribir el archivo clientes.")

def crear_nuevo_cliente() -> None:
    """
    Está función carga un nuevo cliente al json de clientes

    pre: Está función no necesita parametros

    post: Esta función Guarda un nuevo cliente en el archivo clientes.json.
    """
    # Solicitar datos del cliente
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
    dict_clientes = {key: value for key, value in fx.leer_JSON(RUTA).items()}
    datos_cliente = obtener_datos_cliente()
    id_cliente = datos_cliente.get('id', 0)
    del(datos_cliente['id'])
    dict_clientes[id_cliente] = datos_cliente
    cargar_archivo(dict_clientes, "wt")
    print("Cliente agregado exitosamente.")
    fx.volver_menu(
        "Quiere cargar otro cliente? (Y/N): ", menu.menu_clientes, crear_nuevo_cliente
    )


def actualizar_datos_cliente() -> None:
    """
    Está función actualiza los datos de un cliente en particular
    pre: Está función no necesita parametros
    post: Esta función actualiza los datos de un cliente en el archivo json
    """
    id_cliente = obtener_id_cliente()
    dict_clientes = {key: value for key, value in fx.leer_JSON(RUTA).items()}

    # Verificar si se encontraron clientes
    if not dict_clientes:
        print("No se encontraron clientes.")
        fx.volver_menu(
            "Quiere volver al menu (Y/N): ",
            menu.menu_clientes,
            menu.menu_principal,
        )

    # Buscar el cliente específico
    datos_cliente = encontrar_cliente(id_cliente)
    mostrar_datos(datos_cliente)
    fx.volver_menu(
        "El cliente encontrado es correcto? (Y/N): ",
        menu.menu_clientes,
    )

    datos_cliente = obtener_datos_cliente()
    del(datos_cliente['id'])
    mostrar_datos(datos_cliente)
    fx.volver_menu(
        "Estan bien los datos? (Y/N): ",
        obtener_datos_cliente,
    )
    
    dict_clientes[str(id_cliente)] = datos_cliente

    # Guardar los datos actualizados en el archivo
    cargar_archivo(dict_clientes, "w")
    print("Cliente actualizado correctamente.")
    fx.volver_menu(
        "Quiere actualizar otro cliente? (Y/N): ",
        menu.menu_clientes,
        actualizar_datos_cliente,
    )

def mostrar_clientes() -> None:
    """
    Está función muestra todos los clientes
    pre: Está función no necesita parametros
    post: Esta función lista todos los clientes que existen en el archivo json clientes
    """
    clientes = fx.leer_JSON(RUTA)

    # Verificar si se encontraron clientes
    if not clientes:
        print("No se encontraron clientes.")
        fx.volver_menu(
            "Quiere volver al menu (Y/N): ",
            menu.menu_clientes,
            menu.menu_principal,
        )
    # Mostrar la tabla con claves como encabezados
    print(
        tabulate(
            [clientes.values()],
            headers=clientes.keys(),
            tablefmt="fancy_grid",
            stralign="center",
        )
    )
    fx.volver_menu(
        "Quiere volver al menu (Y/N): ",
        menu.menu_clientes,
        menu.menu_principal,
    )


def obtener_id_cliente() -> int:
    while True:
        try:
            id_cliente = int(input("Ingrese el numero del usuario: "))
            break
        except (ValueError, KeyboardInterrupt) as e:
            print("\nError al ingresar el codigo del usuario...")
    return id_cliente
def mostrar_datos(datos_cliente):
    print(
        tabulate(
            [datos_cliente.values()],
            headers=datos_cliente.keys(),
            tablefmt="fancy_grid",
            stralign="center",
        )
    )

def borrar_cliente() -> None:
    """
    Está función borra un cliente del la lista de clientes
    pre: Está función no necesita parametros
    post: Esta función borra un cliente del archivo json de clientes
    """
    id_cliente = obtener_id_cliente()
    dict_clientes = {key: value for key, value in fx.leer_JSON(RUTA).items()}

    # Verificar si se encontraron clientes
    if not dict_clientes:
        print("No se encontraron clientes.")
        fx.volver_menu(
            "Quiere agregar un cliente? (Y/N): ",
            menu.menu_clientes,
            crear_nuevo_cliente,
        )

    # Buscar el cliente específico
    datos_cliente = encontrar_cliente(id_cliente)
    if not datos_cliente:
        print("Cliente no encontrado.")
        fx.volver_menu(
            "Quiere buscar otro cliente? (Y/N): ",
            menu.menu_clientes,
            borrar_cliente,
        )

    # Mostrar la tabla con claves como encabezados
    mostrar_datos(datos_cliente)
    fx.volver_menu(
        "Esta seguro que quiere borrar el cliente? (Y/N): ",
        menu.menu_clientes,
    )
    # Creo una lista con los clientes que no sean ese cliente
    print(dict_clientes)
    del(dict_clientes[str(id_cliente)])

    # Guardar los datos actualizados en el archivo
    cargar_archivo(dict_clientes, "w")
    print("Cliente borro correctamente el cliente.")
    fx.volver_menu(
        "Quiere borrar otro cliente? (Y/N): ",
        menu.menu_clientes,
        borrar_cliente,
    )

def encontrar_cliente(id_cliente: int):
    clientes = fx.leer_JSON(RUTA)
    return clientes.get(str(id_cliente), {})


def ver_datos_cliente() -> None:
    """
    Mostrar datos del cliente con ese id
    """
    id_cliente = obtener_id_cliente()
    datos_cliente = encontrar_cliente(id_cliente)
    if not (datos_cliente):
        print("No se ha encontrado el cliente.")
        fx.volver_menu(
            "Quiere agregar un cliente? (Y/N): ",
            menu.menu_principal,
            crear_nuevo_cliente,
        )
    mostrar_datos(datos_cliente)
    fx.volver_menu(
        "Quiere volver al menu? (Y/N): ",
        menu.menu_principal,
        menu.menu_clientes,
    )

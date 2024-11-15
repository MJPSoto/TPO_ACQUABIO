from menues import menues as menu
from funciones import funcionesX as fx
from tabulate import tabulate
import re
import json
import datetime

# declaro la ruta que voy a usar para la funcion leer json
RUTA = "JSON/clientes.json"

def ingresar_fecha_compra() -> None:
    patron_date = "^(?:\\d{4})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$"
    while True:
        try:
            date = input("Ingrese la fecha. Ejemplo: 20240608: ")
            if re.match(patron_date, date):
                date = datetime.date(
                    int(date[:4]), int(date[4:6]), int(date[6:8])
                ).strftime("%Y/%m/%d")
                break
            else:
                print("Fecha no valida.")
        except KeyboardInterrupt:
            print("\nNo se permite interrupciones")
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
    return max(list(cliente["id"] for cliente in fx.leer_JSON(RUTA))) + 1


def obtener_datos_cliente() -> dict:
    """
    Está función obtiene los datos del cliente por consola

    pre: Está función no necesita parametros

    post: Esta función devuelve un diccionario con los datos del cliente
    """
    ide = crear_id_cliente()
    nombre = fx.validacion_datos(
        "Ingrese su nombre y apellido: ",
        "Ingrese nuevamente el nombre",
        "[A-Za-z\s]{3,}$",
    )
    telefono = fx.validacion_datos(
        "Ingrese su numero de telefono. Ejemplo: 1122334455: ",
        "Ingrese nuevamente el telefono.",
        "[0-9\s]{10}$",
    )
    codigo_postal = fx.validacion_datos(
        "Ingrese su codigo postal: ",
        "Ingrese nuevamente su codigo postal.",
        "[0-9\s]{4}$",
    )
    direccion = fx.validacion_datos(
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
    clientes = fx.leer_JSON(RUTA)
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
        with open(RUTA, "w") as archivo:
            json.dump(clientes, archivo, indent=4)
    except Exception:
        print("Error al escribir el archivo clientes.")
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
    clientes = fx.leer_JSON(RUTA)

    # Verificar si se encontraron clientes
    if not clientes:
        print("No se encontraron clientes.")
        return menu.menu_clientes()

    # Buscar el cliente específico
    datos_cliente = encontrar_cliente(id_cliente)
    if not datos_cliente:
        print("Cliente no encontrado.")
        return menu.menu_clientes()

    # Mostrar los datos del cliente y solicitar los nuevos datos
    print(tabulate(datos_cliente.items()))
    nuevos_datos = obtener_datos_cliente()

    # Actualizar los datos del cliente sin modificar el ID
    for key, value in nuevos_datos.items():
        if key != "id":
            datos_cliente[key] = value
    # Creo una lista con los clientes que no sean ese cliente
    clientes_actualizados = [
        cliente for cliente in clientes if cliente["id"] != id_cliente
    ]
    # Agrego el nuevo cliente con los datos actualizados
    clientes_actualizados.append(datos_cliente)

    # Guardar los datos actualizados en el archivo
    try:
        with open(RUTA, "w") as archivo:
            json.dump(clientes_actualizados, archivo, indent=4)
    except Exception:
        print("Error al intentar actualizar los datos del cliente")
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
        return menu.menu_clientes()

    tabla = [
        {
            key: (value if not isinstance(value, dict) else list(value.values())[0])
            for key, value in cliente.items()
        }
        for cliente in clientes
    ]

    # Mostrar la tabla con claves como encabezados
    print(
        tabulate(
            tabla,
            headers="keys",
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


def borrar_cliente() -> None:
    """
    Está función borra un cliente del la lista de clientes
    pre: Está función no necesita parametros
    post: Esta función borra un cliente del archivo json de clientes
    """
    id_cliente = obtener_id_cliente()
    clientes = fx.leer_JSON(RUTA)

    # Verificar si se encontraron clientes
    if not clientes:
        print("No se encontraron clientes.")
        return menu.menu_clientes()

    # Buscar el cliente específico
    datos_cliente = encontrar_cliente(id_cliente)
    if not datos_cliente:
        print("Cliente no encontrado.")
        return menu.menu_clientes()

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
    fx.volver_menu(
        "Esta seguro que quiere borrar el cliente? (Y/N): ",
        menu.menu_clientes,
    )
    # Creo una lista con los clientes que no sean ese cliente
    lista_clientes_actualizada = [
        cliente for cliente in clientes if cliente["id"] != id_cliente
    ]

    # Guardar los datos actualizados en el archivo
    try:
        with open(RUTA, "w") as archivo:
            json.dump(lista_clientes_actualizada, archivo, indent=4)
    except Exception:
        print("Error al intentar actualizar los datos del cliente")
    print("Cliente actualizado correctamente.")
    fx.volver_menu(
        "Quiere borrar otro cliente? (Y/N): ",
        menu.menu_clientes,
        borrar_cliente,
    )


def encontrar_cliente(id_cliente: int):
    clientes = fx.leer_JSON(RUTA)
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
    fx.volver_menu(
        "Quiere volver al menu? (Y/N): ",
        menu.menu_principal,
        menu.menu_clientes,
    )

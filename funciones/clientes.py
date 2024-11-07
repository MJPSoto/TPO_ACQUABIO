from menues import menues as menu
from funciones import funcionesX as fx
from tabulate import tabulate
import re
import json
import datetime

# declaro la ruta que voy a usar para la funcion leer json
ruta = "JSON/clientes.json"


def validacion_datos(mensaje: str, mensaje_error: str, expretion: str) -> str:
    """Es una función genérica para validar distintos datos

    Args:
        mensaje (str): Mensaje inicial según el dato a pedir
        mensaje_error (str): Mensaje de error en el caso de que no se valide la entrada
        expretion (str): Expresión regular para validar el dato

    Returns:
        str: Retorna un string con el dato validado
    """
    while True:
        dato_verificar = input(mensaje)
        if re.match(expretion, dato_verificar):
            break
        else:
            print(mensaje_error)
    return dato_verificar


def ingresar_fecha_compra() -> str:
    """En esta funcion se ingresa el año, mes y dia de la instalación del ablandador

    Returns:
        str: Retorna en formato string la fecha de la instalación tipo 20240208
    """
    patron_date = "^(?:\\d{4})(0[1-9]|1[0-2])(0[1-9]|[12]\d|3[01])$"
    while True:
        date = input("Ingrese la fecha. Ejemplo: AAAAMMDD: ")
        if re.match(patron_date, date):
            date = datetime.date(
                int(date[:4]), int(date[4:6]), int(date[6:8])
            ).strftime("%Y/%m/%d")
            return date
        else:
            ingresar_fecha_compra()


def verificar_ciudades_disponibles(codigo_postal: str) -> str:
    """Esta funcion verifica si el dato ingresado está dentro de las ciudades en el JSON ciudades

    Args:
        codigo_postal (str): Dato tipo string, tiene que ser 1 numero de 4 digitos

    Returns:
        str: Si encuentra el codigo postal en el JSON, retorna el CP, sino retorna "Otro"
    """
    localidades = fx.leer_JSON("JSON/ciudades.json")
    key_value = {"100100": "Otro"}
    for localidad in localidades:
        for key, valor in localidad.items():
            if key == codigo_postal:
                key_value = {key: valor}
    return key_value


def crear_id_cliente() -> int:
    """Esta función verifica en clientes.JSON el "id". En el caso de que haya datos, verifica cliente por cliente
    y se selecciona el valor máximo de los id. Se le añade 1 para que este sea el valor del próximo cliente
    En el caso de que no haya datos, se le asigna por default 0 y se le suma 1 para asignarselo al primer cliente

    Returns:
        bool: Retorna un valor entero
    """
    return (
        int(max(list(cliente["id"] for cliente in fx.leer_JSON(ruta)), default=0)) + 1
    )


def verificar_celular_repetido(numero_telefono: str) -> bool:
    """Se verifica si un numero está repetido o no en el dato "telefono" en clientes.JSON

    Args:
        numero_telefono (str):  Se ingresa el numero de telefono del cliente

    Returns:
        bool: Retorna True si ese numero de telefono ya está en el JSON, caso contrario, retorna False
    """
    clientes = fx.leer_JSON(ruta)
    if clientes:
        for cliente in clientes:
            if cliente["telefono"] == numero_telefono:
                return True
        return False


def obtener_datos_cliente() -> dict:
    """
    Está función obtiene los datos del cliente por consola

    Args:
        Está función no necesita parametros

    Returns:
        Esta función devuelve un diccionario con los datos del cliente
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
    while verificar_celular_repetido(telefono):
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

    Args:
        Está función no necesita parametros

    Returns:
        Retorna None
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
        with open(ruta, "wt") as archivo:
            json.dump(clientes, archivo, indent=4)
    except Exception:
        print("Error al escribir el archivo clientes.")
    print("Cliente agregado exitosamente.")
    volver_al_menu()
    return None


def actualizar_datos_cliente() -> None:
    """
    Está función actualiza los datos de un cliente en particular

    Args:
        Está función no necesita parametros

    Return:
        Esta función actualiza los datos de un cliente en el archivo json
    """
    id_cliente = obtener_id_cliente()
    clientes = fx.leer_JSON(ruta)
    if not clientes:
        menu.menu_clientes()
        print("No se encontraron clientes")
    datos_cliente = encontrar_cliente(id_cliente)
    print(tabulate(datos_cliente.items()))
    """
    for key, value in nuevos_datos.items():
        if key != "id":
            cliente[key] = value
    with open(ruta, "w") as archivo:
        json.dump(clientes, archivo, indent=4)
    print("Cliente actualizado correctamente.")
    menu.menu_clientes()
    """
    volver_al_menu()
    return None


def mostrar_clientes() -> None:
    """
    Está función muestra todos los clientes
    Esta función lista todos los clientes que existen en el archivo json clientes

    Args:
        Está función no necesita parametros

    Return:
        Retorna None
    """
    clientes = fx.leer_JSON(ruta)
    if not clientes:
        print("No se encontraron clientes")
        menu.menu_clientes()
    print(tabulate(clientes, headers="keys"))
    volver_al_menu()
    return None


def obtener_id_cliente() -> int:
    """Esta funcion obtiene el id del cliente

    Returns:
        int: Retorna un dato entero con el id del cliente
    """
    while True:
        try:
            id_cliente = int(input("Ingrese el numero del usuario: "))
            return id_cliente
        except ValueError as e:
            print("El numero de usuario no existe.")


def borrar_cliente() -> None:
    """
    Está función borra un cliente del la lista de clientes

    Args:
        Está función no necesita parametros

    Return:
        Esta funcion retorna None
    """
    id_cliente = obtener_id_cliente()
    clientes = fx.leer_JSON(ruta)
    if not clientes:
        menu.menu_clientes()
        print("No se encontraron clientes")
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
    volver_al_menu()
    return None


def encontrar_cliente(id_cliente: int) -> list:
    """Esta funcion verifica si un cliente se encuentra en JSON clientes

    Args:
        id_cliente (int): Se ingresa como parametro el ID del cliente

    Returns:
        list: Retorna los datos del cliente en una lista en caso de encontrarlo
        Caso contrario, retorna una lista vacia
    """
    clientes = fx.leer_JSON(ruta)
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            return cliente
    return []


def ver_datos_cliente() -> None:
    """
    Mostrar datos del cliente con ese id

    Args:
        No recibe argumentos

    Returns:
        Retorna None
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
    volver_al_menu()
    return None


def volver_al_menu() -> None:
    """Esta funcion te retorna al menú principal o menú clientes

    Returns:
        _type_: Retorna None
    """
    mensaje = input("Desea salir del menu cliente? S/N")

    if mensaje == "n":
        menu.menu_clientes()

    if mensaje != "s":
        volver_al_menu()

    menu.menu_principal()
    return None

from menues import menues as menu
from funciones import funcionesX as fx
from tabulate import tabulate
import re
import json
import datetime

# declaro la ruta que voy a usar para la funcion leer json
ruta = "JSON/clientes.json"


def ingresar_direccion() -> str:
    while True:
        try:
            direccion = input("Ingrese su direccion: ")
            if verificar_direccion(direccion):
                return direccion
        except Exception:
            print("Ingrese nuevamente su direccion.")


def verificar_direccion(direccion: str) -> bool:
    patron = r"^[a-zA-Z0-9\s]+$"
    return bool(re.match(patron, direccion))


def ingresar_nombre() -> str:
    """En esta funcion verificamos si el nombre del cliente es valido

    Args:
        nombre (str): Ingreso nombre y apellido del cliente

    Returns:
        bool: retorno true si se cumplen las condiciones
    """
    while True:
        try:
            nombre = input("Ingrese su nombre y apellido: ")
            if verificar_nombre(nombre):
                return nombre
        except Exception:
            print("Error")


def verificar_nombre(nombre):
    nombre_valido = r"[A-Za-z\s]{3,}$"
    return bool(re.match(nombre_valido, nombre))


def ingresar_telefono() -> str:
    """

    Returns:
        _type_: _description_
    """
    while True:
        try:
            telefono = input("Ingrese su numero de telefono. Ejemplo: 1122334455: ")
            if verificar_telefono(telefono):
                return telefono
        except ValueError:
            print("Error")


def verificar_telefono(telefono: str) -> bool:
    """Esta funcion verifica si un numero es valido

    Args:
        telefono (int): le paso como parametro un numero que por lo menos tenga 10 digitos y sea positivo

    Returns:
        bool: retorna true si se cumple y false si no
    """
    if telefono.isdigit() and len(telefono) == 10:
        return True
    return False


def ingresar_fecha_compra() -> None:
    patron_anio = r"^20[0-9]{2}$"
    patron_mes = r"^(0[1-9]|1[0-2])$"
    patron_dia = r"^(0[1-9]|[12][0-9]|3[01])$"
    while True:
        try:
            anio = input("Ingrese su el anio de la compra: ")
            if not (re.match(patron_anio, anio)):
                raise ValueError("El año no es valido")
            mes = input("Ingrese el mes de la compra: ")
            if not (re.match(patron_mes, mes)):
                raise ValueError("El mes no es valido")
            dia = input("Ingrese el dia de la compra: ")
            if not (re.match(patron_dia, dia)):
                raise ValueError("El dia no es valido")
            fecha = anio, mes, dia
            fecha_final = "/".join(fecha)
            if verificar_fecha_compra(anio, mes, dia):
                return fecha_final
        except ValueError as e:
            print(f"Error: {e}")


def verificar_fecha_compra(anio, mes, dia) -> bool:
    """En esta funcion verifico si la fecha ingresada es valida

    Args:
        No recibe argumentos

    Returns:
        bool: retorno true si es valida
    """
    anio, mes, dia = int(anio), int(mes), int(dia)
    while True:
        fecha_compra = datetime.date(anio, mes, dia)
        if fecha_compra:
            return True
        else:
            print("Fecha invalida, ingrese nuevamente los datos")


def ingresar_ciudad() -> int:
    while True:
        try:
            codigo_postal = input("Ingrese su codigo postal: ")
            if verificar_ciudad(codigo_postal):
                print("Codigo postal valido")
                return codigo_postal
        except ValueError:
            print("Ingrese nuevamente su codigo postal")


def verificar_ciudad(codigo_postal: str) -> bool:
    codigo_postal_valido = r"[0-9\s]{4}$"
    return bool(re.match(codigo_postal_valido, codigo_postal))


def verificar_ciudades_disponibles(codigo_postal: str) -> str:
    while True:
        try:
            if verificar_ciudad(codigo_postal):
                localidades = fx.leer_JSON("JSON/ciudades.json")
                localidad = localidades.get(codigo_postal)
                if localidad:
                    return codigo_postal
                else:
                    return localidades.get("", "100100")
        except Exception as e:
            print("Error")


def crear_id_cliente() -> tuple:
    """Esta funcion lee el JSON y guarda los datos en una lista. Verifica si hay algun valor en "id"
    Si no lo hay, guardamos 0 en la lista, caso contrario, el mayor dato encontrado en "id".
    Retornamos

    Returns:
        bool: Retorna una tupla con el id
    """
    maximo = 0
    clientes = fx.leer_JSON(ruta)
    lista_id = []
    for cliente in clientes:
        ide = cliente["id"]
        lista_id.append(ide)
    if lista_id:
        maximo = max(lista_id)
    else:
        maximo = 0
    return maximo + 1


def obtener_datos_cliente() -> None:
    """
    Está función obtiene los datos del cliente por consola

    pre: Está función no necesita parametros

    post: Esta función devuelve un diccionario con los datos del cliente
    """

    ide = crear_id_cliente()
    nombre = ingresar_nombre()
    telefono = ingresar_telefono()
    ciudad = ingresar_ciudad()
    direccion = ingresar_direccion()
    fecha_compra = ingresar_fecha_compra()

    # ciudades = fx.leer_JSON_ciudades()
    ciudades = fx.leer_JSON("JSON/ciudades.json")
    for valor in ciudades:
        if list(valor.keys())[0] == ciudad:
            ciudad = valor
            break
    if isinstance(ciudad, str):
        ciudad = {"100100": "Otro"}

    nuevo_cliente = {
        "id": ide,
        "nombre": nombre,
        "telefono": telefono,
        "ciudad": ciudad,
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
    clientes.append(obtener_datos_cliente())

    with open("JSON/clientes.json", "w") as archivo:
        json.dump(clientes, archivo, indent=4)
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
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            nuevos_datos = obtener_datos_cliente()
            for key, value in nuevos_datos.items():
                if key != "id":
                    cliente[key] = value
            with open(ruta, "w") as archivo:
                json.dump(clientes, archivo, indent=4)
            print("Cliente actualizado correctamente.")
            menu.menu_clientes()


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
        with open(ruta, "w") as archivo:
            json.dump(clientes_actualizados, archivo, indent=4)
        print("Cliente borrado correctamente.")


def ver_datos_cliente() -> None:
    """
    Mostrar datos del cliente con ese id
    """
    id_cliente = obtener_id_cliente()
    clientes = fx.leer_JSON("JSON/clientes.json")
    for cliente in clientes:
        if cliente["id"] == id_cliente:
            print(tabulate(cliente.items()))

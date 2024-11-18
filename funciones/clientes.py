from menues import menues as menu
from funciones import funcionesX as fx
from tabulate import tabulate
import re
import datetime

# declaro la ruta que voy a usar para la funcion leer json
RUTA = "JSON/clientes.json"


def ingresar_fecha_compra() -> str:
    """Esta funcion pide por teclado que el usuario ingrese la fecha de compra del ablandador
    Utilizamos la libreria datetime para asegurarnos que sea una fecha real
    Se espera que el usuario ingrese fechas a partir del 2022

    Returns:
        str: Se retora la fecha de compra
    """
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
    """Esta funcion verifica si el codigo postal ingresado por el usuario se encuentra en el JSON.
    En el caso de que no esté, se le asigna "Otro"

    Args:
        codigo_postal (str): Recibe como parámetro un código postal de 4 digitos numéricos en formato string

    Returns:
        str: Retorna un diccionario con el codigo postal como key y la ciudad como valor
    """
    localidades = fx.leer_JSON("JSON/ciudades.json")
    key_value = {"100100": "Otro"}
    for key, valor in localidades.items():
        if key == codigo_postal:
            key_value = {key: valor}
    return key_value


def verificar_celular_repetido() -> str:
    """En esta funcion se verifica si el numero de telefono igresado por teclado está repetido en el JSON clientes.
    Returns:
        str: Retorna el número de teléfono si no está repetido.
    """
    clientes = fx.leer_JSON(RUTA)
    telefono_cliente = fx.validacion_datos(
        "Ingrese su número de teléfono. Ejemplo: 1122334455: ",
        "Ingrese nuevamente el teléfono.",
        "[0-9\s]{10}$",
    )

    if clientes:
        for cliente in clientes.values():
            if cliente["telefono"] == telefono_cliente:
                print("El número ingresado ya está cargado a otro cliente.")
                return verificar_celular_repetido()
    return telefono_cliente


def obtener_datos_cliente() -> dict:
    """En esta función se obtienen todos los datos del cliente

    Returns:
        dict: Se retorna un diccionario con todos los datos
    """
    ide = fx.crear_id(RUTA)
    nombre = fx.validacion_datos(
        "Ingrese su nombre y apellido: ",
        "Ingrese nuevamente el nombre",
        "[A-Za-z\s]{3,}$",
    )

    telefono = verificar_celular_repetido()

    codigo_postal = fx.validacion_datos(
        "Ingrese su codigo postal: ",
        "Ingrese nuevamente su codigo postal.",
        "[0-9\s]{3,}$",
    )
    direccion = fx.validacion_datos(
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

    """
    Ejemplo del return
    {
        "1": {
            "nombre": "Agustin Villavicencio",
            "telefono": "2233445566",
            "ciudad": {
                "7167": "Pinamar"
            },
            "direccion": "Foca 25",
            "fecha_compra": "2024/12/20"
        }
    }
    """
    return nuevo_cliente


def crear_nuevo_cliente() -> None:
    """Esta función crea un nuevo cliente y lo añade al JSON clientes
    No recibe parámetros

    Returns:
        None: Retorna None
    """
    # Solicitar datos del cliente
    dict_clientes = {key: value for key, value in fx.leer_JSON(RUTA).items()}
    datos_cliente = obtener_datos_cliente()
    id_cliente = datos_cliente.get("id", 0)
    del datos_cliente["id"]
    dict_clientes[id_cliente] = datos_cliente
    fx.cargar_archivo(dict_clientes, "wt", RUTA, "El cliente no se pudo cargar")
    print("Cliente agregado exitosamente.")
    fx.volver_menu(
        "¿Quiere cargar otro cliente? (Y/N): ", menu.menu_clientes, crear_nuevo_cliente
    )
    return None


def actualizar_datos_cliente() -> None:
    """En esta funcion se actualizan los datos de un cliente en particular
    No recibe parámetros

    Returns:
        None: Retorna None
    """
    id_cliente = obtener_id_cliente()
    dict_clientes = {key: value for key, value in fx.leer_JSON(RUTA).items()}

    # Verificar si se encontraron clientes
    if not dict_clientes:
        print("No se encontraron clientes.")
        fx.volver_menu(
            "¿Quiere volver al menú principal? (Y/N): ",
            menu.menu_clientes,
            menu.menu_principal,
        )

    # Buscar el cliente específico
    datos_cliente = encontrar_cliente(id_cliente)
    mostrar_datos(datos_cliente)
    fx.volver_menu(
        "¿El cliente encontrado es el que desea modificar? (Y/N): ",
        menu.menu_clientes,
    )
    # generamos un diccionario con el índice de cada clave como key y cada key como valor
    keys = {i + 1: key for i, key in enumerate(datos_cliente.keys())}

    print(
        tabulate(
            keys.items(),
            headers=["Número", "Opción"],
            tablefmt="fancy_grid",
            stralign="center",
        )
    )

    while True:
        try:
            option = int(input("Seleccione una de las siguiente opciones: "))
            if option in keys.keys():
                break
        except ValueError as e:
            print(e)
    # Opción ingresada y validada
    value_keys = keys[option]

    dato_modificar = validations[value_keys]()

    datos_cliente[value_keys] = dato_modificar
    mostrar_datos(datos_cliente)
    fx.volver_menu(
        "El cambio es correcto? (Y/N): ",
        menu.menu_clientes,
    )

    dict_clientes[str(id_cliente)] = datos_cliente

    # Guardar los datos actualizados en el archivo
    fx.cargar_archivo(dict_clientes, "w", RUTA, "El cliente no se pudo cargar")
    print("Cliente actualizado correctamente.")
    fx.volver_menu(
        "Quiere actualizar otro cliente? (Y/N): ",
        menu.menu_clientes,
        actualizar_datos_cliente,
    )
    return None


def mostrar_clientes() -> None:
    """Esta función muestra a todos los clientes que hay en el JSON clientes.
    En el caso de no haberlos, muestra un mensaje en pantalla informandoló.
    No recibe parámetros.
    Returns:
        None: Retorna None.
    """
    clientes = fx.leer_JSON(RUTA)
    # Verificar si se encontraron clientes
    if not clientes:
        print("No se encontraron clientes.")
        fx.volver_menu(
            "¿Quiere volver al menu principal? (Y/N): ",
            menu.menu_clientes,
            menu.menu_principal,
        )
    # Mostrar la tabla con claves como encabezados
    rows = [list(cliente.values()) for cliente in clientes.values()]
    headers = list(next(iter(clientes.values())).keys())
    print(
        tabulate(
            rows,
            headers=headers,
            tablefmt="fancy_grid",
            stralign="center",
        )
    )
    fx.volver_menu(
        "Quiere volver al menu (Y/N): ",
        menu.menu_clientes,
        menu.menu_principal,
    )
    return None


def obtener_id_cliente() -> int:
    """En esta función se obtiene el ID de un cliente en particular ingresado por teclado.
    No recibe parámetros

    Returns:
        int: Retorna un número entero
    """
    while True:
        try:
            id_cliente = int(input("Ingrese el ID del usuario: "))
            break
        except (ValueError, KeyboardInterrupt) as e:
            print("\nError al ingresar el codigo del usuario...")
    return id_cliente


def mostrar_datos(datos_cliente: dict) -> None:
    """Esta función está creada para mostrar en pantalla datos de un diccionario

    Args:
        datos_cliente (_type_): Recibe como parámetro un diccionario con datos

    Returns:
        None: Retorna None
    """
    print(
        tabulate(
            [datos_cliente.values()],
            headers=datos_cliente.keys(),
            tablefmt="fancy_grid",
            stralign="center",
        )
    )
    return None


def borrar_cliente() -> None:
    """Esta función borra a un cliente del JSON clientes
    No recibe parámetros
    Retorna None
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
    del dict_clientes[str(id_cliente)]

    # Guardar los datos actualizados en el archivo
    fx.cargar_archivo(dict_clientes, "w", RUTA, "El cliente no se pudo cargar.")
    print("Cliente borro correctamente el cliente.")
    fx.volver_menu(
        "Quiere borrar otro cliente? (Y/N): ",
        menu.menu_clientes,
        borrar_cliente,
    )


def encontrar_cliente(id_cliente: int) -> str:
    """Esta función se encarga de encontrar a un cliente en específico
    Se cargan todos los datos del JSON clientes

    Args:
        id_cliente (int): Se ingresa como parámetro el id del cliente en formato int

    Returns:
        str: Si se encuentra el cliente, se retorna la key con el id del cliente
        Caso contrario, se retorna un string vacío
    """
    clientes = fx.leer_JSON(RUTA)
    return clientes.get(str(id_cliente), "")


def ver_datos_cliente() -> None:
    """Esta función muestra en pantalla el dato de un cliente en específico
    Se pide el dato del ID del cliente y luego muestra todos los datos
    No recibe parámetros

    Returns:
        None: Retorna None
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
    return None


# validaciones para función actualizar_datos_cliente()
validations = {
    "nombre": lambda: fx.validacion_datos(
        "Ingrese su nombre y apellido: ",
        "Ingrese nuevamente el nombre",
        "[A-Za-z\s]{3,}$",
    ),
    "telefono": lambda: verificar_celular_repetido(),
    "direccion": lambda: fx.validacion_datos(
        "Ingrese su direccion: ",
        "Ingrese nuevamente su direccion.",
        "^[a-zA-Z0-9\s]{4,}$",
    ),
    "fecha_compra": lambda: ingresar_fecha_compra(),
    "ciudad": lambda: verificar_ciudades_disponibles(validations["codigo_postal"]()),
    "codigo_postal": lambda: fx.validacion_datos(
        "Ingrese su codigo postal: ",
        "Ingrese nuevamente su codigo postal.",
        "[0-9\s]{3,}$",
    ),
}

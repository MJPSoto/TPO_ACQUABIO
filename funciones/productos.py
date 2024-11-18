from menues import menues as menu
from funciones import funcionesX as fx
import json
import re
from tabulate import tabulate

RUTA = "JSON/productos.json"


def obtener_datos_producto() -> str:
    """
    En esta función se obtiene el producto ingresado por el usuario.
    Se validan los datos y se almacenan en una variable

    No recibe parámetros
    Returns:
        str: Retorna el nuevo producto en formato string
    """
    nuevo_producto = fx.validacion_datos(
        "Ingrese nuevo producto: ",
        "Ingrese nuevamente el producto: ",
        r"^(?=.*[A-Za-z])(?=.{4,})(?!^\d+$).*$",
    )
    # verificación de que el producto ingresado es correcto
    print(tabulate([[nuevo_producto]], headers=["producto"], stralign="center"))
    confirmacion = fx.volver_menu(
        "¿Los datos ingresados son correctos? (y/n): ", obtener_datos_producto
    )

    if confirmacion:
        return confirmacion
    return nuevo_producto


def crear_producto() -> None:
    """
    En esta función primero se cargan todos los datos del JSON productos si los hay.
    Luego se obtienen los datos del producto
    Se crea un ID correspondiente
    Se carga el producto al JSON productos

    No recibe parámetros
    Returns:
        None: Retorna None
    """
    # leo el json y lo guardo en la variable mansajes
    productos = fx.leer_JSON(RUTA)
    #Obtengo el nombre del producto
    producto = obtener_datos_producto()
    #Creo un nuevo id
    id_mensaje = fx.crear_id(RUTA)
    #Lo cargo la variable de productos
    productos[id_mensaje] = producto

    #Lo cargo en el JSON de productos
    fx.cargar_archivo(productos, "wt", RUTA, "No se pudo cargar el producto")

    fx.volver_menu(
        "¿Quiere volver a cargar otro producto? (y/n): ",
        menu.menu_producto,
        crear_producto,
    )
    return None


def actualizar_producto() -> None:
    """
    Esta función actualiza un producto en específico ingresado por el usuario.
    Toma todos los datos del JSON y el usuario ingresa el número del ID para ingresar al producto y actualizarlo
    
    No recibe parámetros
    Returns:
        None: Retorna None
    """
    # Se lee el json de los productos
    productos = fx.leer_JSON(RUTA)
    if not productos:
        fx.volver_menu(
            "¿No hay productos, desea crear uno? (y/n): ",
            menu.menu_producto,
            crear_producto,
        )
    print("\n Productos disponibles")
    print(
        tabulate(
            productos.items(),
            headers=["ID", "Producto"],
            tablefmt="fancy_grid",
            stralign="center",
        )
    )

    # solicito el id del producto
    id_producto = fx.obtener_id(
        "Ingrese el ID del producto: ", "El ID ingresado no es valido."
    )

    # se almacena el producto encontrado en el diccionario según al id que corresponda
    producto = productos.get(str(id_producto), None)
    if not producto:
        fx.volver_menu(
            "¿El producto no existe, desea crearlo? (y/n): ",
            menu.menu_producto,
            crear_producto,
        )
    print(
        tabulate(
            [[id_producto, producto]],
            headers=["ID", "Producto"],
            tablefmt="fancy_grid",
            stralign="center",
        )
    )
    fx.volver_menu("¿Es el producto que busca modificar? (Y/N): ", actualizar_producto)

    nuevo_producto = fx.validacion_datos(
        "Ingrese el nuevo producto: ",
        "Ingrese nuevamente el producto",
        "[A-Za-z\s]{3,}$",
    )

    productos[str(id_producto)] = nuevo_producto

    fx.cargar_archivo(
        productos, "w", RUTA, "No se pudo cargar el producto en el archivo"
    )
    print("Se actualizó correctamente el producto")

    fx.volver_menu(
        "¿Quiere actualizar otro producto? (y/n): ",
        menu.menu_producto,
        actualizar_producto,
    )
    return None


def borrar_producto() -> str:
    """
    Esta función borra un producto en específico. Muestra en pantalla todos los datos del JSON, luego se selecciona un ID
    para ingresar a un producto determinado. Al seleccionar, se pregunta si se quiere o no borrar ese mensaje.

    No recibe parámetros
    Returns:
        None: Retorna None
    """
    # leo el json
    productos = fx.leer_JSON(RUTA)
    """
        productos
        {
            "1": sarasa,
            "2": prueba
        }
    """
    id_producto = fx.obtener_id(
        "Ingrese el ID del mensaje: ", "El ID ingresado no es valido."
    )
    producto = productos.get(str(id_producto), None)
    if not producto:
        fx.volver_menu(
            "El ID ingresado no existe, quiere crearlo? (y/n): ",
            menu.menu_producto,
            crear_producto,
        )
    print(
        tabulate(
            [[id_producto, producto]],
            headers=["ID", "producto"],
            tablefmt="fancy_grid",
            stralign="center",
        )
    )

    # confirmar eliminación del producto
    fx.volver_menu(
        "¿Está seguro que quiere eliminar el producto? (y/n): ",
        menu.menu_producto,
    )
    # borro el producto
    del productos[str(id_producto)]

    # Vuelvo a cargar todo en el JSON
    fx.cargar_archivo(
        productos, "w", RUTA, "No se pudo escribir en el archivo de productos"
    )
    print("El productos se elimino correctamente")
    fx.volver_menu(
        "¿Quiere borrar otro producto? (y/n): ",
        menu.menu_producto,
        borrar_producto,
    )


def ver_productos() -> None:
    """
    Esta función toma todos los datos del JSON e imprime en pantala todos los productos que haya cargados.
    En el caso de que no haya, se muestra en pantalla un mensaje informando que no hay productos.

    No recibe parámetros
    Returns:
        None: Retorna None
    """
    productos = fx.leer_JSON(RUTA)
    """
        productos
        {
            "1": sarasa,
            "2": prueba
        }
    """
    # Verificar si se encontraron productos
    if not productos:
        fx.volver_menu(
            "No se encontraron productos, quiere cargar un producto? (y/n): ",
            menu.menu_producto,
            crear_producto,
        )

    # Muestro los productos existentes
    print(
        tabulate(
            list(productos.items()),
            headers=["clave", "producto"],
            tablefmt="fancy_grid",
            stralign="center",
        )
    )
    fx.volver_menu(
        "Quiere volver al menu (Y/N): ",
        menu.menu_producto,
        menu.menu_principal,
    )


def ver_producto() -> None:
    """
    Esta función toma todos los datos por el JSON, se le pide un ID al usuario para ingresar a un mensaje en específico.
    Al ingresar el ID, se imprime en pantalla el mensaje.

    No recibe parámetros
    Returns:
        None: Retorna None
    """
    productos = fx.leer_JSON(RUTA)
    """
        productos
        {
            "1": "filtro de carbón activado",
            "2": "filtro de sedimentos"
        }
    """
    id_producto = fx.obtener_id(
        "Ingrese el ID del producto: ", "El ID ingresado no es valido."
    )
    producto = productos.get(str(id_producto), None)
    if producto:
        producto = {id_producto: producto}
        print(
            tabulate(
                producto.items(),
                headers=["ID", "Producto"],
                tablefmt="fancy_grid",
                stralign="center",
            )
        )
    else:
        print("No se ha encontrado el producto")
    fx.volver_menu(
        "Quiere volver al menu (Y/N): ",
        menu.menu_producto,
        menu.menu_principal,
    )
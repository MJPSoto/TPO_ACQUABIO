from menues import menues as menu
from funciones import funcionesX as fx
import json
import re
from tabulate import tabulate

RUTA = "JSON/productos.json"


def obtener_datos_producto() -> dict:
    """
    Esta funcion toma los datos del producto nuevo y los valida
    pre: no recibe nada
    post: devuelve una lista con los datos
    """
    nuevo_producto = fx.validacion_datos(
        "Ingrese nuevo producto: ",
        "Ingrese nuevamente el producto: ",
        r"^(?=.*[A-Za-z])(?=.{4,})(?!^\d+$).*$",
    )
    clave = int(max((producto for producto in fx.leer_JSON(RUTA)), default=0)) + 1
    producto = {clave: nuevo_producto}
    # verificación de que el producto ingresado es correcto
    print(tabulate(producto.items(), headers=["clave", "producto"], stralign="center"))
    fx.volver_menu(
        "¿Los datos ingresados son correctos? (y/n): ", obtener_datos_producto
    )
    return producto


def validar_existencia(producto: list, productos: list) -> None:
    if producto in productos:
        fx.volver_menu(
            "¿El producto ya existe, quiere cargar otro producto? (y/n): ",
            menu.menu_producto,
            crear_producto,
        )


def cargar_archivo(datos_cargar, producto_excep: str, producto_success: str) -> None:
    try:
        with open(RUTA, "w") as archivo:
            json.dump(datos_cargar, archivo, indent=4)
    except Exception:
        print(producto_excep)
    print(producto_success)


def crear_producto() -> None:
    """
    Esta funcion toma los datos, comprueba si son validos y los agrega al json
    pre: no recibe nada
    post: no devuelve nada
    """
    # leo el json y lo guardo en la variable mansajes
    productos = fx.leer_JSON(RUTA)
    producto = obtener_datos_producto()
    key, value = list(producto.keys())[0], list(producto.values())[0]
    validar_existencia(key, list(productos.keys()))
    productos[key] = value

    cargar_archivo(
        productos,
        "No se ha podido cargar el archivo",
        "El producto se cargo correctamente",
    )

    fx.volver_menu(
        "¿Quiere volver a cargar otro producto? (y/n): ",
        menu.menu_producto,
        crear_producto,
    )


def actualizar_producto() -> None:
    """
    Obtine el producto nuevo a travez de la funcion obtener_datos_producto, busca la clave
    que es la clave, y si está modifica el producto
    pre: no recibe nada
    port: no devuelve nada
    """
    productos = fx.leer_JSON(RUTA)
    # Solicitar el ID del producto en días
    id_producto = fx.validacion_datos(
        "Ingrese la clave: ",
        "Ingrese nuevamente la clave",
        r"\b([1-9][0-9]{0,2})\b",
    )

    producto = productos.get(id_producto, None)

    # Si el producto no existe, preguntar si se desea crearlo
    if producto is None:
        fx.volver_menu(
            "¿El producto no existe, desea crearlo? (y/n): ",
            menu.menu_producto,
            crear_producto,
        )
    else:
        # Mostrar el producto en formato de tabla
        print(
            tabulate(
                [[id_producto, producto]], headers=["Días", "producto"], stralign="center"
            )
        )
        nuevo_producto = obtener_datos_producto()
        productos[list(nuevo_producto.keys())[0]] = list(nuevo_producto.values())[0]
        cargar_archivo(
            productos,
            "No se ha podido cargar el archivo",
            "El producto se actualizó correctamente",
        )
    fx.volver_menu(
        "¿Quiere actualizar otro producto? (y/n): ",
        menu.menu_producto,
        actualizar_producto,
    )


def obtener_producto_x_id(productos: list) -> dict:
    id_producto = fx.validacion_datos(
        "Ingrese la clave: ",
        "Ingrese nuevamente la clave",
        r"\b([1-9][0-9]{0,2})\b",
    )

    producto = productos.get(id_producto, None)

    # Si el producto no existe, preguntar si se desea crearlo
    if producto is None:
        fx.volver_menu(
            "¿El producto no existe, desea crearlo? (y/n): ",
            menu.menu_producto,
            crear_producto,
        )
    else:
        return {id_producto: producto}


def borrar_producto() -> str:
    """
    Lee el json encontrando el producto que se quiere borrar mediante el Id, vuelve a cargar
    el json con los productos excepto el eliminado.
    pre: no recibe nada
    prost: no devuelve nada
    """
    # leo el json
    productos = fx.leer_JSON(RUTA)
    producto = obtener_producto_x_id(productos)
    print(
        tabulate(
            producto.items(),
            headers=["clave", "producto"],
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
    del productos[list(producto.keys())[0]]

    # Vuelvo a cargar todo en el JSON
    cargar_archivo(
        productos,
        "No se ha podido cargar el archivo",
        "El producto se borró correctamente",
    )
    fx.volver_menu(
        "¿Quiere borrar otro producto? (y/n): ",
        menu.menu_producto,
        borrar_producto,
    )


def ver_productos() -> None:
    """
    Lee el json, e imprime los productos en pantalla
    pre: no recibe nada
    post: no devuelve nada
    """
    productos = fx.leer_JSON(RUTA)

    # Verificar si se encontraron productos
    if not productos:
        print("No se encontraron productos.")
        return menu.menu_producto()

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
    Busca un producto mediante el id, si lo encuentra lo mustra en pantalla
    pre: no recibe nada
    post: no devuelve nada
    """
    productos = fx.leer_JSON(RUTA)
    id_producto = fx.validacion_datos(
        "Ingrese la clave: ",
        "Ingrese nuevamente la clave",
        r"\b([1-9][0-9]{0,2})\b",
    )

    producto = productos.get(id_producto, None)
    if producto:
        producto = {id_producto: producto}
        print(
            tabulate(
                producto.items(),
                headers=["clave", "producto"],
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
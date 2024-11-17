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
    clave = max(list(map(int, list(fx.leer_JSON(RUTA).keys()))), default=0) + 1
    producto = {clave: nuevo_producto}
    # verificación de que el producto ingresado es correcto
    print(tabulate(producto.items(), headers=["clave", "producto"], stralign="center"))
    fx.volver_menu(
        "¿Los datos ingresados son correctos? (y/n): ", obtener_datos_producto
    )
    return producto


def validar_existencia(producto: list, productos: list) -> None:
    """Esta funcion verifica si el producto existe. Caso contrario, se le pregunta al usuario si quiere crearlo.

    Args:
        producto (list): recibe una lista con 2 datos, una clave y un valor, como primer parametro
        productos (list): recibe una lista con todos los datos del json productos como segundo parametro

    Returns:
        _type_: No retorna nada
    """
    if producto in productos:
        fx.volver_menu(
            "¿El producto ya existe, quiere cargar otro producto? (y/n): ",
            menu.menu_producto,
            crear_producto,
        )
    return None


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
    
    
def obtener_id_producto() -> int:
    while True:
        try:
            id_cliente = int(input("Ingrese el ID del producto: "))
            break
        except (ValueError, KeyboardInterrupt) as e:
            print("\nError al ingresar el codigo del usuario...")
    return id_cliente


def actualizar_producto() -> None:
    """
    Obtine el producto nuevo a travez de la funcion obtener_datos_producto, busca la clave
    que es la clave, y si está modifica el producto
    pre: no recibe nada
    port: no devuelve nada
    """
    #en productos está el diccionario con las claves y el nombre del producto
    productos = {key: value for key, value in fx.leer_JSON(RUTA).items()}
    # en tabla almaceno en una lista llave y valor por cada producto
    tabla = [[key, value] for key, value in productos.items()]
    print(tabla)
    print("\n Productos disponibles")
    print(tabulate(tabla, headers=["ID", "Producto"], tablefmt="fancy_grid", stralign="center"))
    
    # solicito el id del producto
    id_producto = obtener_id_producto()
    
    # se almacena el producto encontrado en el diccionario según al id que corresponda
    producto = productos.get(str(id_producto), None)
    
    if not productos:
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
    
    fx.cargar_archivo(productos, "w", RUTA, "No se pudo cargar el producto en el archivo")
    print("Se actualizó correctamente el producto")

    fx.volver_menu(
        "¿Quiere actualizar otro producto? (y/n): ",
        menu.menu_producto,
        actualizar_producto,
    )
    return None
    


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
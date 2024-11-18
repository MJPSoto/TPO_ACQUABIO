from menues import menues as menu
from funciones import funcionesX as fx
from tabulate import tabulate

RUTA = "JSON/productos.json"


def obtener_datos_producto() -> str:
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
    # verificación de que el producto ingresado es correcto
    print(tabulate([[nuevo_producto]], headers=["producto"], stralign="center"))
    fx.volver_menu(
        "¿Los datos ingresados son correctos? (y/n): ", obtener_datos_producto
    )
    return nuevo_producto


def crear_producto() -> None:
    """
    Esta funcion toma los datos, comprueba si son validos y los agrega al json
    pre: no recibe nada
    post: no devuelve nada
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


def actualizar_producto() -> None:
    """
    Obtine el producto nuevo a travez de la funcion obtener_datos_producto, busca la clave
    que es la clave, y si está modifica el producto
    pre: no recibe nada
    port: no devuelve nada
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
    Lee el json encontrando el producto que se quiere borrar mediante el Id, vuelve a cargar
    el json con los productos excepto el eliminado.
    pre: no recibe nada
    prost: no devuelve nada
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
    Lee el json, e imprime los productos en pantalla
    pre: no recibe nada
    post: no devuelve nada
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
    Busca un producto mediante el id, si lo encuentra lo mustra en pantalla
    pre: no recibe nada
    post: no devuelve nada
    """
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

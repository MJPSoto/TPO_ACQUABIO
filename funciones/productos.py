from funciones import funcionesX as fx
from menues import menues as menu
import json
import re

RUTA = "JSON/productos.json"

def producto_valido(texto) -> bool:
    """
    Recibe un texto y comprueba si es válido o no.

    pre: recibe un string.

    post: devuelve un booleano.
    """
    # Patrón: al menos cuatro caracteres, contiene letras, no es solo números ni solo espacios
    patron = r"^(?=.*[A-Za-z])(?=.{4,})(?!^\d+$).*$"
    return bool(re.match(patron, texto.strip()))

def volver_menu()-> None:
    """
    Pregunta si desea volver al menú. Te lleva al menú principal si ingresa "y" y al menú de productos
    si ingresa "n".

    pre: no recibe nada.

    post: no devuelve nada.
    """
    ok = input("¿Desea volver al menú principal? (y/n): ").lower()
    
    # Si es "n", vuelve al menú de productos
    if ok == "n":
        menu.menu_producto()

    # Si no es ni "n" ni "y", vuelve a ejecutar la función
    if ok != "y":
        volver_menu()
    
    # Si no es ninguna de las anteriores, se toma como "y" y vuelve al menú principal
    menu.menu_principal()
    return None


def obtener_datos_producto() -> list[str]:
    """
    Pide los datos del producto, los valida y los devuelve como una lista.

    pre: no recibe nada.

    post: devuelve una lista con los datos.
    """
    while True:
        producto = []
        nuevo_producto = input("Ingrese nuevo producto: ")
        # Verifico si el producto es válido y no es demasiado largo
        if not producto_valido(nuevo_producto):
            continue

        clave = input("Ingrese la cantidad de días: ")
        # Verifico que la clave sea válida
        if not re.match("\b([1-9][0-9]{0,2})\b", clave):
            continue
    
        # Verificación de que el producto ingresado es correcto
        ok = input("¿Los datos ingresados son correctos? (y/n): ").lower()
        if ok == "n":
            continue
        if ok != "y":
            continue
        
        producto = [clave, nuevo_producto]
        return producto


def datos_producto_nuevo() -> list[str]:
    """
    Pide la descripción del producto, genera un ID según el que tiene el máximo, valida los datos
    y devuelve los datos como una lista.

    pre: no recibe nada.

    post: devuelve una lista con los datos.
    """
    while True:
        # Leo el JSON y lo guardo en productos
        productos = fx.leer_JSON(RUTA)
        producto = []
        nuevo_producto = input("Ingrese descripción de nuevo producto: ")
        # Verifico si el texto de nuevo_producto es válido
        if not producto_valido(nuevo_producto):
            continue
        
        # Busco el ID con el valor más alto, lo casteo y le sumo 1; si no hay ningún valor toma 0 como default
        clave = int(max((producto for producto in productos[0]), default=0)) + 1

        # Guardo la descripción que quiero imprimir
        descripcion = f"El producto es: {nuevo_producto}\n"
        
        # Verificación de que el producto ingresado es correcto
        ok = input(f"{descripcion}¿Los datos ingresados son correctos? (y/n): ").lower()
        if ok == "n":
            continue
        if ok != "y":
            continue
        
        # Guardo los datos validados en la lista
        producto = [clave, nuevo_producto]
        return producto


def crear_producto() -> str:
    """
    Toma los datos anteriores y los agrega al JSON.
    
    pre: no recibe nada.

    post: devuelve un mensaje con el resultado de la operación.
    """
    # Leo el JSON y lo guardo en la variable productos
    productos = fx.leer_JSON(RUTA)
    nuevo_producto = obtener_datos_producto()
    
    try:
        # Defino la clave desde la lista devuelta en la línea anterior
        clave = nuevo_producto[0]
        # Defino el producto de la misma manera
        producto = nuevo_producto[1]
    except IndexError as e:
        crear_producto()
        return f"Error: {e}"

    # Compruebo si el producto ya existe
    if productos[0].get(clave) is None:
        # Creo el producto nuevo
        productos[0][clave] = producto
        # Reescribo el JSON
        with open(RUTA, "w") as archivo:
            json.dump(productos, archivo, indent=4)
        return "Producto cargado."

    # Compruebo si desea reescribir el producto
    ok = input("El ID de producto ya existe, ¿quiere reemplazarlo? (y/n): ").lower()
    if ok == "n":
        return "No se cargó ningún producto."
    if ok != "y":
        return "Valor ingresado incorrecto."
    
    # Creo el producto nuevo
    productos[0][clave] = producto

    # Reescribo el JSON
    with open(RUTA, "w") as archivo:
        json.dump(productos, archivo, indent=4)
    return "Producto cargado."


def actualizar_producto() -> None:
    """
    Recibe el diccionario con el stock de los productos y una lista referencial con los productos disponibles
    y sus respectivas claves.

    pre: no recibe nada.

    post: devuelve un mensaje con el resultado de la operación.
    """
    ver_productos()
    # Leo el JSON
    productos = fx.leer_JSON(RUTA)
    # Obtengo el producto nuevo
    nuevo_producto = obtener_datos_producto()

    try:  
        # Defino la clave desde la lista devuelta en la línea anterior
        clave = nuevo_producto[0]
        # Defino el producto de la misma manera
        producto = nuevo_producto[1]
    except IndexError as e:
        return f"Error: {e}"

    # Comparo para ver si la clave existe en el JSON
    while True:
        # Busco el producto
        if productos[0].get(clave) is None:
            # Al no encontrarse, pregunto si desea crear el producto
            ok = input("El ID de producto no existe, ¿desea crearlo? (y/n): ").lower()
            if ok == "n":
                continue        
            if ok != "y":
                continue
            productos[0][clave] = producto
            with open(RUTA, "w") as archivo:
                json.dump(productos, archivo, indent=4)
            return "Producto cargado."

        # Actualizo el valor del producto
        productos[0][clave] = producto
    
        # Vuelvo a cargar todo en el JSON
        with open(RUTA, "w") as archivo:
            json.dump(productos, archivo, indent=4)
        return "Producto cargado."


def borrar_producto():
    """
    Busca el producto por el ID ingresado por el usuario y lo elimina.

    pre: no recibe nada.

    post: devuelve un mensaje con el resultado de la operación.
    """
    ver_productos()
    # Defino la clave desde la lista devuelta en la línea anterior
    clave = input("Ingrese la cantidad de días: ") 
    # Verifico que la clave sea válida
    if not re.match("\b([1-9][0-9]{0,2})\b", clave):
        return "Clave inválida."    
        
    # Leo el JSON
    productos = fx.leer_JSON(RUTA)

    producto = productos[0].get(clave)
            
    # Comparo para ver si la clave existe en el JSON
    if producto is None:
        # Si no se encuentra ningún producto
        volver_menu()
        return "Producto no encontrado."
    
    ok = input(f"{productos[clave]}\n¿Es este el producto que desea eliminar? (y/n): ").lower()
    if ok == "n":
        return "No se modificó ningún producto."        

    if ok != "y":
        volver_menu()
        return "Valor incorrecto."

    # Borro el producto
    del productos[0][clave]
        
    # Vuelvo a cargar todo en el JSON
    with open(RUTA, "w") as archivo:
        json.dump(productos, archivo, indent=4)
        return "Producto eliminado."
    return None


def ver_productos():
    """
    Muestra todos los productos con sus respectivas claves.
    """
    try:
        productos = fx.leer_JSON(RUTA)
        for key, value in productos[0].items():
            print(f"Clave: {key} - Producto: {value}")
    except IndexError as e:
        print(f"Error: {e}")
    return None


def ver_producto() -> str:
    """
    Muestra en pantalla el producto con el ID ingresado por teclado.

    pre: no recibe nada.

    post: devuelve una cadena con la información del producto.
    """
    productos = fx.leer_JSON(RUTA)
    clave = input("Ingrese la cantidad de días: ")  
    # Verifico que la clave sea válida
    if not re.match("\b([1-9][0-9]{0,2})\b", clave):
        return "El nomero ingresado no es válido"
    
    if productos[0].get(clave) is None:
        return "Producto no encontrado"

    return f"clave: {clave}- producto: {productos[0][clave]}"

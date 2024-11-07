from funciones import funcionesX as fx
from menues import menues as menu
import json
import re

RUTA = "JSON/productos.json"

def producto_valido(texto) -> bool:
    """
    Recibe un texto y comprueba si es valido o no

    pre: recibe un string

    post: devuelve un booleno
    """
    # Patrón: al menos cuatro caracteres, contiene letras, no es solo números ni solo espacios
    patron = r"^(?=.*[A-Za-z])(?=.{4,})(?!^\d+$).*$"
    return bool(re.match(patron, texto.strip()))

def volver_menu()-> None:
    """
    Pregunta si quiere volver al menú. Te lleva al menú principal si ingresa "y" y te lleva al menu producto
    si ingresa "n".############

    pre: no recibe nada

    post: no devuelve nada
    """
    ok = input("¿Desea volver al menú principal? (y/n): ").lower()
    
    #si es "n" vuelve a producto
    if ok == "n":
        menu.menu_producto()

    #si no es ni "n" ni "y", vuelve a ejecutar la funcion
    if ok != "y":
        volver_menu()
    
    #si no es ninguna de las anteriores se toma como "y" y vuelve a menu principal
    menu.menu_principal()
    return None


def obtener_datos_producto() -> list[str]:
    """
    Pide los datos del producto, los valida y los devuelve como una lista

    pre: no recibe nada

    post: devuelve una lista con los datos
    """
    while True:
        producto = []
        nuevo_producto = input("Ingrese nuevo producto: ")
        #verifico si el producto es valido y no es demasiado largo
        if not producto_valido(nuevo_producto):
            continue

        clave = input("Ingrese la cantidad de días: ")
        #verifico que la cantidad de clave sea valida
        if not re.match("\b([1-9][0-9]{0,2})\b", clave):
            continue
    
        #verificación de que el producto ingresado es correcto
        ok = input("¿Los datos ingresados son correctos? (y/n): ").lower()
        if ok == "n":
            continue
        if ok != "y":
            continue
        
        producto = [clave, nuevo_producto]
        return producto


def datos_producto_nuevo() -> list[str]:
    """
    Pide la descripcion del producto, los valida, genera un ID segun el que tiene el maximo
    y devuelve los datos como una lista.

    pre: no recibe nada

    post: devuelve una lista con los datos
    """
    while True:
        productos = fx.leer_JSON(RUTA)
        producto = []
        nuevo_producto = input("Ingrese descripcion de nuevo producto: ")
        #verifico si el texto de producto es valido
        if not producto_valido(nuevo_producto):
            continue
        
        #busco el ID con el valor mas alto lo casteo y le sumo 1, si no tiene ningun valor toma 0 como default
        clave = int(max((producto for producto in productos[0]), default=0)) +1

        #guardo lo que quiero imprimir
        descripcion = f"El producto es: {nuevo_producto}\n"
        
        #verificación de que el producto ingresado es correcto
        ok = input(f"{descripcion}¿Los datos ingresados son correctos? (y/n): ").lower()
        if ok == "n":
            continue
        if ok != "y":
            continue
        
        #guardo los datos validados en la lista
        producto = [clave, nuevo_producto]
        return producto


def crear_producto() -> None:
    """
    Toma los datos anteriores y los agrega al json
    
    pre: no recibe nada

    post: no devuelve nada
    """
    #leo el json y lo guardo en la variable mansajes
    productos = fx.leer_JSON(RUTA)
    nuevo_producto = obtener_datos_producto()
    #defino los clave desde la lista devuelta en la linea anterior
    
    try:    
        clave = nuevo_producto[0]
        #defino los productos de la misma manera
        producto = nuevo_producto[1]
        #copruebo si el producto ya existe
    except IndexError as e:
        crear_producto()
        return f"Error: {e}"

    if productos[0].get(clave) is None:
        #creo el producto nuevo
        productos[0][clave] = producto
        with open(RUTA, "w") as archivo:
            json.dump(productos, archivo, indent=4)
        return "Producto cargado."

    #compruebo si quiere reescribir el producto
    ok = input("El ID de producto ya existe quiere reemplazarlo (y/n): ").lower()
    if ok == "n":
        return "No se cargó ningun producto"
    if ok != "y":
        return "Valor ingresado ingorrecto"

    #reescribo el json
    with open(RUTA, "w") as archivo:
        json.dump(productos, archivo, indent=4) 
    return "Producto cargado."

    

def actualizar_producto() -> None:
    """
    Recibe el diccionario con el stock de los productos y una lista referencial con los productos disponibles
    y sus respecticas claves.

    pre: no recibe nada

    post: devuelve un dicccionario
    """
    ver_productos()
    #leo el json
    productos = fx.leer_JSON(RUTA)
    #obtengo el producto nuevo
    nuevo_producto = obtener_datos_producto()

    try: ############# verifica el uso del try, los try van donde sabes que va a fallar tu codigo 
        #defino los clave desde la lista devuelta en la linea anterior
        clave = nuevo_producto[0]
        #defino los productos de la misma manera
        producto = nuevo_producto[1]
    except IndexError as e:
        return f"Error: {e}"

    #comparo para ver si la clave(los clave) existen en el json
    while True:
        #busco el producto
        if productos[0].get(clave) is None:
            #al no encontrarse, pregunto si quiere crear el producto############ 
            ok = input("El ID de producto no existe, desea crearlo (y/n): ").lower()
            if ok == "n":
                continue        
            if ok != "y":
                continue
            productos[0][clave] = producto
            with open(RUTA, "w") as archivo:
                json.dump(productos, archivo, indent=4)
            return "Producto cargado"

    
        #actualizo el valor del producto
        productos[0][clave] = producto
    
        #vuelvo a cargar todo en el json
        with open(RUTA, "w") as archivo:
            json.dump(productos, archivo, indent=4)
        return "Producto cargado."


def borrar_producto():
    """
    Busca el producto por el Id ingresado por el usuario y lo elimina

    pre: no recibe nada

    prost: no devuelve nada
    """
    ver_productos()
    #defino los clave desde la lista devuelta en la linea anterior
    clave = input("Ingrese la cantidad de días: ") ######################## upa acá no puede dar error, cuando se castea un input y ese casteo no se puede hacer, eso genera un error
    #verifico que la cantidad de clave sea valida
    if not re.match("\b([1-9][0-9]{0,2})\b", clave):####################### trata de usar retorno rapido y no usar los ifs en flecha ######cambie el >1 <100 por una expresion regular
        return "Clave invalida"    
        
    #leo el json
    productos = fx.leer_JSON(RUTA)

    producto = productos[0].get(clave)
            
    #comparo para ver si la clave(los clave) existen en el json
    if producto is None:
    #si no encuentra ningun producto
        volver_menu()
        return "Producto no encontrado" ### tenemos que devolver cosas no printear cosas 

    print(producto)
    ok = input("Es este el producto que desea eliminar? (y/n): ").lower()
    if ok == "n":
        return "No se modificó ningun producto"        

    if ok != "y":
        volver_menu()
        return "Valor incorrecto"

    #borro el producto
    del productos[0][clave]
        
    # Vuelvo a cargar todo en el JSON
    with open(RUTA, "w") as archivo:
        json.dump(productos, archivo, indent=4)
        return "Producto eliminado."
    return None



def ver_productos():
    """
    Actualizar producto con ese id
    """
    try:
        productos = fx.leer_JSON(RUTA)
        for key, value in productos[0].items():
            print(f"clave: {key}- producto: {value}")
    except IndexError as e:
        print(f"Error: {e}")
    return None



def ver_producto() -> str:
    """
    Muestra en pantalla el producto con el id ingresado por teclado

    pre: no recibe nada

    post: no devuelve nada
    """
    productos = fx.leer_JSON(RUTA)
    clave = input("Ingrese la cantidad de días: ") ############ lo mismo acá que en la anterior función 
    #verifico que la cantidad de clave sea valida
    if not re.match("\b([1-9][0-9]{0,2})\b", clave):
        return "El nomero ingresado no es válido"
    
    if productos[0].get(clave) is None:
        return "Producto no encontrado"

    return f"clave: {clave}- producto: {productos[0][clave]}"

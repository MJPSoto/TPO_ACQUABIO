from variables import constantes as cs
from funciones import funcionesX as fx
from menues import menues as menu
import random as rn
import json
import re

RUTA = "JSON/productos.json"

def producto_valido(texto) -> bool:
    """
    Recibe un texto y comprueba si es valido o no

    pre: recive un string

    post: devuelve un booleno
    """
    # Patrón: al menos cuatro caracteres, contiene letras, no es solo números ni solo espacios
    patron = r"^(?=.*[A-Za-z])(?=.{4,})(?!^\d+$).*$"
    return bool(re.match(patron, texto.strip()))


def obtener_datos_producto() -> list[str]:
    """
    Esta funcion toma los datos del producto y los valida

    pre: no recive nada

    post: devuelve una lista con los datos
    """
    while True:
        producto = []
        nuevo_producto = input("Ingrese nuevo producto: ")
        #verifico si el producto es valido y no es demasiado largo
        if producto_valido(nuevo_producto):
            try:
                clave = input("Ingrese la cantidad de días: ")
                #verifico que la cantidad de clave sea valida
                if int(clave) > 0 and int(clave) <= 100:
                    print(f"El producto es: {nuevo_producto}")
                    #verificación de que el producto ingresado es correcto
                    ok = input("¿Los datos ingresados son correctos? (y/n): ").lower()
                    if ok == "y":
                        producto = [clave, nuevo_producto]
                        return producto
                    elif ok == "n":
                        continue
                    else:
                        print("Valor ingresado incorrecto")
            except ValueError:
                print("Datos ingresados son incorrectos")
        else:
            print("El producto ingresado no es valido")
        return producto


def datos_producto_nuevo() -> list[str]:
    """
    Esta funcion toma los datos del producto nuevo y los valida

    pre: no recive nada

    post: devuelve una lista con los datos
    """
    while True:
        productos = fx.leer_JSON(RUTA)
        producto = []
        nuevo_producto = input("Ingrese descripcion de nuevo producto: ")
        #verifico si el texto de producto es valido
        if producto_valido(nuevo_producto):
            clave = int(max((producto for producto in productos[0]), default=0)) +1
            print(f"La descripcion del producto es: {nuevo_producto}")
            #verificación de que el producto ingresado es correcto
            ok = input("¿Los datos ingresados son correctos? (y/n): ").lower()
            if ok == "y":
                producto = [clave, nuevo_producto]
                return producto
            elif ok == "n":
                continue
            else:
                print("Valor ingresado incorrecto")
        else:
            print("Datos ingresados son incorrectos")
            return producto


def crear_producto() -> None:
    """
    Esta funcion toma los datos, comprueba si son validos y los agrega al json
    
    pre: no recibe nada

    post: no devuelve nada
    """
    #leo el json y lo guardo en la variable productos
    productos = fx.leer_JSON(RUTA)
    nuevo_producto = datos_producto_nuevo()
    #defino la clave de la lista devuelta en la linea anterior
    try:    
        clave = nuevo_producto[0]
        #defino los productos de la misma manera
        producto = nuevo_producto[1]
        #copruebo si el producto ya existe
        if productos[0].get(clave) is None:
            #creo el producto nuevo
            productos[0][clave] = producto
            print("producto cargado.")
        else:
            #compruebo si quiere reescribir el producto
            ok = input("El ID de producto ya existe desea reemplazarlo (y/n): ").lower()
            if ok == "y":
                productos[0][clave] = producto
                print("producto cargado.")
            else:
                #esto no se si dejarlo asi o volver a la carga de productos##############
                print("No se creó ningun producto...")
        #reescribo el json
        with open(RUTA, "w") as archivo:
            json.dump(productos, archivo, indent=4)
        menu.menu_producto()
    except IndexError as e:
        print(f"Error: {e}")
        menu.menu_producto()
    except FileNotFoundError:
        print("No se encontró el archivo")
        menu.menu_producto()
    except KeyboardInterrupt:
        print("Se interrumpio el proceso")
        menu.menu_producto()
    return None
    

def actualizar_producto() -> None:
    """
    Recibe el diccionario con el stock de los productos y una lista referencial con los productos disponibles
    y sus respecticas claves.

    pre: no recive nada

    post: devuelve un dicccionario
    """
    ver_productos()
    #obtengo el menssaje nuevo
    nuevo_producto = obtener_datos_producto()
    try:    
        #defino los clave desde la lista devuelta en la linea anterior
        clave = nuevo_producto[0]
        #defino los productos de la misma manera
        producto = nuevo_producto[1]
        #leo el json
        productos = fx.leer_JSON(RUTA)
        #compruebo que la clave existe
        while True:    
            if productos[0].get(clave) is None:
                #compruebo si quiere crear el producto
                ok = input("El ID de producto no existe, desea crearlo (y/n): ").lower()
                if ok == "y":
                    productos[0][clave] = producto
                    print("producto cargado.")
                    break
                elif ok == "n":
                    #esto no se si dejarlo asi o volver a la carga de productos##############
                    print("No se creó ningun producto...")
                    break
                else:
                    print("Opcion incorrecta")
            else:
                #actualizo el valor del producto
                productos[0][clave] = producto
                print("producto cargado.")
                break
        #vuelvo a cargar todo en el json
        with open(RUTA, "w") as archivo:
            json.dump(productos, archivo, indent=4)
        menu.menu_producto()
    except IndexError as e:
        print(f"Error: {e}")
        actualizar_producto()
    except FileNotFoundError:
        print("No se encontró el archivo")
        menu.menu_producto()
    except KeyboardInterrupt:
        print("Se interrumpio el proceso")
        menu.menu_producto()
    return None


def borrar_producto():
    """
    Busca el producto por el Id ingresado por el usuario y lo elimina

    pre: no recive nada

    prost: no devuelve nada
    """
    ver_productos()
    try:
        clave = input("Ingrese la clave de producto: ")
        #verifico que la clave sea valida
        if int(clave) > 0 and int(clave) <= 1000:
            #leo el json
            productos = fx.leer_JSON(RUTA)
            #obtengo la clave y verifico que existen en el json
            if productos[0].get(clave) is None:
                print("Producto no encontrado")
            else:
                #imprimo para verificar si es correcto
                print(productos[0][clave])
                ok = input("Este es el producto que desea eliminar? (y/n): ").lower()
                if ok == "y":
                    del productos[0][clave]
                    # Vuelvo a cargar todo en el JSON
                    with open(RUTA, "w") as archivo:
                        json.dump(productos, archivo, indent=4)
                    print("producto eliminado.")
                    menu.menu_producto()
                else:
                    print("producto no eliminado")
                    menu.menu_producto()
        else:
            print("Número ingresado fuera de rango")
    except ValueError:
        print("El valor ingresado es invalido")
    except IndexError as e:
        print(f"Error: {e}")
        menu.menu_producto()
    except FileNotFoundError:
        print("No se encontró el archivo")
        menu.menu_producto()
    except KeyboardInterrupt:
        print("Se interrumpio el proceso")
        menu.menu_producto()
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



def ver_producto() -> None:
    """
    Muestra en pantalla el producto con el id ingresado por teclado

    pre: no recibe nada

    post: no devuelve nada
    """
    productos = fx.leer_JSON(RUTA)
    try:
        clave = input("Ingrese la clave de producto: ")
        #verifico que la clave de producto sea valida
        if int(clave) > 0 and int(clave) <= 1000:
            #obtengo la clave y verifico que existen en el json
            try:
                if productos[0].get(clave) is None:
                    print("Clave de producto no encontrada")
                else:
                    print(f"clave: {clave}- producto: {productos[0][clave]}")
            except KeyError as e:
                print(f"Error: {e}")
        else:
            print("La clave ingresada no es valida.")
    except ValueError:
        print("El valor ingresado es invalido")
    return None

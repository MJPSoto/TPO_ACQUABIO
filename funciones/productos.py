from variables import constantes as cs
<<<<<<< HEAD
from verificaciones import verificaciones as vf
=======
>>>>>>> origin

def crear_producto():
    """
    Actualizar mensaje con ese id
    """
    pass

def actualizar_producto():
    """
    recibe el diccionario con el stock de los productos y una lista referencial con los productos disponibles
    y sus respecticas claves.

    pre: recibe un diccionario y una lista

    post: devuelve un dicccionario
    """
    #imprime lista de claves de productos
    [print(producto) for producto in cs.lista_claves]
    #ingresa una clade de producto
    clave_producto = input("\nIngrese clave producto: ")
    #comprueba si la clave esta en el diccionario 
    if clave_producto in cs.stock_productos:
        #ingresa valor a cambiar como entero
        cantidad_stock = int(input("Ingrese el stock actual: "))
        #compueba que sea valido el stock
        if 0 <= cantidad_stock <= 200:
            #convierte el valor a string y lo cambia por el nuevo
            cs.stock_productos[clave_producto] = str(cantidad_stock)
        else:
            print("Valor de stock incorrecto")
    else:
        print("La clave ingresada no pertenece a ningun producto")
    return cs.stock_productos


def borrar_producto():
    """
    Actualizar mensaje con ese id
    """
    pass

def ver_productos():
    """
    Actualizar mensaje con ese id
    """
    pass

def ver_producto():
    """
    Actualizar mensaje con ese id
    """
    pass

def crear_archivo_productos(dict_productos: dict):
    file = open("../CSV/archivo_productos.csv", "a+", encoding="utf-8")
    for value in dict_productos.values():
        cadena = ",".join(value) + "\n"
        file.write(cadena)
    return None

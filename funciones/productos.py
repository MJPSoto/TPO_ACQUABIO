from variables import constantes as cs

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
    esta funcion elimina un producto del stock

    pre:esta funcion no recibe parametros externos

    post: esta funcion no retorna nada
    """
    with open("../CSV/archivo_productos.csv", "r", encoding="utf-8") as file:
        reader = csv.DictReader(file)
        productos = list(reader)

    while True:
        #se solicitar el ID del producto
        id_producto = input("Ingrese el ID del producto (3 dígitos): ")
        #se usa re para verificar el id correctamente
        if re.fullmatch(r'\d{3}', id_producto):
            break
        else:
            print("ID de producto inválido.")
    #se crea una nueva lista con todos los productos menos el que se va eliminar
    productos_actualizados = [
        producto for producto in productos if producto['id'] != id_producto
    ]

    #si no se encuentra el producto se notifica
    if len(productos_actualizados) == len(productos):
        print(f"No existe un producto con el ID {id_producto}.")
        return

    #se sobreescribe el archivo con los productos actualizados
    with open(archivo_csv, "w", newline='', encoding="utf-8") as file:
        fieldnames = productos[0].keys()  # Obtener los nombres de las columnas
        writer = csv.DictWriter(file, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(productos_actualizados)

    print("producto eliminado correctamente")
    return None

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

def crear_producto(id_producto: int):
    """
    Actualizar mensaje con ese id
    """
    pass

def actualizar_producto(id_producto: int):
    """
    Actualizar mensaje con ese id
    """
    pass

def borrar_producto(id_producto: int):
    """
    Actualizar mensaje con ese id
    """
    pass

def ver_productos():
    """
    Actualizar mensaje con ese id
    """
    pass

def ver_producto(id_producto: int):
    """
    Actualizar mensaje con ese id
    """
    pass

def crear_archivo_productos(dict_productos: dict):
    file = open("archivo_productos.csv", "a+", encoding="utf-8")
    for value in dict_productos.values():
        cadena = ",".join(value) + "\n"
        file.write(cadena)
    return None

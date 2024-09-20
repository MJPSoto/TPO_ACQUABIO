def crear_producto():
    """
    Actualizar mensaje con ese id
    """
    pass

def actualizar_producto():
    """
    Actualizar mensaje con ese id
    """
    pass

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

# para encontrar si un elemento se repite las veces deseadas en la lista
def find_n(elements, needle, n):
    """
    Devuelve True si en elements hay n o más ocurrencias de needle en una lista
    :param elements: lista de elementos
    :param needle: valor a buscar
    :param n: ocurrencias deseadas
    :return: bool
    """
    if n >= 0:
        index = 0
        count = 0
        while count < n and index < len(elements):
            if needle == elements[index]:
                count += 1
            index += 1
        return count >= n
    else:
        return False

# Para buscar un elemento en una lista usando find_n
def find_one(elements, needle):
    """
    Busca si un elemento existe en una lista 
    :param elements: lista de elementos
    :param needle: valor a buscar
    :return: True si el elemento estála lista
    """
    return find_n(elements, needle, 1)
    
# para encontrar si hay una cantidad continua de elementos iguales en una lista
# así detectar victorias
def find_strike(elements, needle, n):
    """
    Encuentra si hay una cantidad n continua de elementos iguales en una lista
    :param elements: lista de elementos
    :param needle: el valor buscado
    :param n: la cantidad de veces que buscamos que aparezca el valor
    :return: True si hay n o más ocurrencias CONTINUAS de needle
    """
    if n >= 0:
        index = 0
        count = 0
        #strike = False
        while count < n and index < len(elements):
            if needle == elements[index]:
                #strike = True
                count += 1
            else:
                #strike = False
                count = 0
            index += 1
        return count >= n #and strike
    else:
        return False

# crea una lista y la llena de filler (Nones) para hacer filas de un tablero vacío
def make_list(length, filler):
    """
    Crea una lista de longitud length llenándola con el elemento filler
    :param length: longitud de la lista
    :param filler: elemento con el que se llena la lista
    :return: lista creada
    """
    result = []
    index = 0
    while index < length:
        result.append(filler)
        index += 1
    return result

# para encontrar el primer elemento deseado, se usa con un None para saber
# donde coloca la próxima ficha
def index_first_element(elements, needle):
    """
    Encuentra el primer elemento que coincide con needle
    :param elements: lista de elementos
    :param needle: valor a buscar
    :return: índice del primer elemento que coincide con needle o None si no está
    """
    index = 0
    while index < len(elements):
        if needle == elements[index]:
            return index
        else:
            index += 1
    return None

# se construye una lista nueva aplicando transform a cada elemento, lo usamos para
# transformar cada lista (columna del tablero) dentro de la lista en objetos
# para que en vez de lista tengamos objetos
def map_list(elements, transform):
    """
    Crea una lista nueva aplicando transform a cada elemento
    :param elements: lista de elementos
    :param transform: función que se aplica a cada elemento
    :return: lista creada
    """
    result = []
    for element in elements:
        result.append(transform(element))
    return result

# crea una matriz llamando la veces deseadas a factory(LinearBoard) para hacer un tablero con esas propiedades
def make_list_from_factory(length, factory):
    """
    Crea una lista con la cantidad de listas en su interior creadas por la fábrica escogida
    :param length: cantidad de columnas
    :param factory: la fábrica que se escoge
    :return: lista de objetos LinearBoard
    """
    result = []
    index = 0
    while index < length:
        result.append(factory())
        index += 1
    return result

# transpose es como si girara el tablero 90 grados afectando a filas y columnas
def transpose(matrix):
    """
    Intercambia filas y columnas. Funciona con matrices no cuadradas
    :param matrix: matriz a transponer
    :return: matriz transpuesta
    """
    if not matrix:
        return []
    height = len(matrix[0])
    result = []
    for i in range(height):
        sub_result = []
        for j in range(len(matrix)):
            sub_result.append(matrix[j][i])
        result.append(sub_result)
    return result


# desplaza cada elemento de la lista segun la distancia que se le pase (l)
# es variable, la pasa displace_matrix que varía segun la columna para poder trazar diagonales
# el filler por defecto es None ya que segun como la dsplaza, los huecos los rellena con None
def displace(l, distancia, filler = None):
    """
    Devuelve una lista resultante de desplazar cada elemento de la lista segun la distancia que se le pase (l),
    rellena con Nones los huecos que quedan vacíos tras desplazar.

    ejemplo de este ejercicio: 
            l = [a,b,c,d], distancia = -1, filler = None, resultado = [b,c,d,None]
            l = [a,b,c,d], distancia = 0, filler = None, resultado = [a, b, c, d]
            l = [a,b,c,d], distancia = 1, filler = None, resultado = [None, a, b, c]
            l = [a,b,c,d], distancia = 2, filler = None, resultado = [None,None,a,b]
            
    :param l: lista a desplazar
    :param distancia: distancia a desplazar
    :param filler: elemento con el que se rellena la lista
    :return: lista desplazada
    """
    # n va a ser la longitud de la lista
    n = len(l) # en este ejercicio es 4
    result = []
    # bucle que va de 0 a n - 1, es decir de 0 a 3
    for i in range(n):
        index = i - distancia # index es la posicion original de la que viene el valor que va en result[i]
        if 0 <= index < n: # si la posicion original es valida (entre 0 y n - 1)
            result.append(l[index]) # anade el valor a la lista resultante
        else:
            result.append(filler) # si la posicion original no es valida, añade el None
    return result

# hace un bucle llamando a displace la cantidad de veces que hay columnas en la matriz, 
# y entrega la matriz nueva con cada columna desplazada segun la distancia que le 
# corresponde a su posicion
def displace_matrix(matrix, filler = None):
    """
    Crea una matriz resultante de desplazar cada columna,
    rellena con Nones los huecos que quedan vacíos tras desplazar.
      
    :param matrix: matriz a desplazar
    :param filler: elemento con el que se rellena la matriz
    :return: matriz desplazada
    """
    d = []
    # para cada columna llama a la funcion displace y le pasa la distancia segun la posicion de la columna
    for i in range(len(matrix)): 
        d.append(displace(matrix[i], i - 1, filler))
    return d




# le hace el reverse a una lista (columna del tablero)
def reverse_list(elements):
    """
    Le da la vuelta a una lista, por ejemplo: [a,b,c,d] -> [d,c,b,a]
    :param elements: lista a invertir
    :return: lista invertida
    """
    return elements[::-1]

# llama a reverse_list para cada columna del tablero y asi le da la vuelta
# la columna mantiene su posicion pero su interior esta invertido, es decir
# la columna 2 sigue siento la columna 2 pero su interior esta invertido.
def reverse_matrix(matrix):
    """
    Le da la vuelta a cada columna de la matriz
    :param matrix: matriz a invertir
    :return: matriz invertida
    """
    result = []
    for col in matrix:
        result.append(reverse_list(col))
    return result


def all_the_same_score(elements):
    """
    Comprueba si todos los elementos de una lista son exactamente iguales entre sí
    :param elements: lista de elementos
    :return: True si todos los elementos son iguales y False si no lo son
    """
    # si la lista esta vacia, devuelve True
    if not elements:
        return True
    # coge el primer elemento para comparar con el resto
    first_element = elements[0]
    result = True
    # para cada elemento en la lista
    for element in elements:
        if element != first_element:
            result = False
    return result

# hace un bucle llamando a colapse_list para cada columna de la matriz y 
# al final retorna un string de toda la matriz separando las columnas con el separador
def colpase_matrix(matrix, empty = '.', sep = '|'):
    """
    Convierte una matriz en una única línea de texto, separando las columnas con un delimitador "|".
    :param matrix: matriz a convertir
    :param empty: elemento que representa un hueco
    :param sep: separador entre columnas
    :return: cadena de texto continua
    """
    result = ''
    # por cada columna
    for elt in matrix:
        # llama al colapse para obtener el string de la columna y separa cada columna con "|"
        result = result + sep + colapse_list(elt, empty)
    # retorna el resultado quitandole el primer separador
    return result[1:]

def colapse_list(elements, empty = '.'):
    """
    Convierte una lista de elementos en una sola cadena de texto continua
    :param elements: lista de elementos
    :param empty: elemento que representa un hueco
    :return: cadena de texto continua
    """
    result = ''
    # por cada elemento en la lista
    for elt in elements:
        if elt is None:
            # si el elemento es None, se añade el empty a la cadena, es decir un .
            result = result + empty
        else:
            # si el elemento no es None, se añade el elemento a la cadena
            result = result + elt
    return result


# para poder reconstruir una matriz a partir de un texto 
def explode_list(list_of_strings):
    """
    Convierte una lista de cadenas de texto en una lista de listas de caracteres
    ejemplo: ['x..o', 'oxoo'] -> [['x','.','.','o'], ['o','x','o','o']]

    :param list_of_strings: lista de cadenas de texto
    :return: lista de listas de caracteres
    """
    result = []
    # por cada cadena de texto
    for element in list_of_strings:
        # convierte la cadena en una lista de caracteres
        result.append(list(element))
    return result

# para cambiar algun valor por otro en toda una matriz
def replace_all(matrix, old, new):
    """
    Reemplaza todos los elementos 'old' por elementos 'new' en una matriz
    :param matrix: matriz
    :param old: valor a reemplazar
    :param new: valor por el que se reemplaza
    :return: matriz nueva con el valor reemplazado
    """
    new_matrix = []
    # recorre cada columna
    for element in matrix:
        # llama a replace_in_list para reemplazar el valor en la columna actual
        new_matrix.append(replace_in_list(element, old, new))
    return new_matrix

def replace_in_list(elements, old, new):
    """
    Reemplaza todos los elementos 'old' por elementos 'new' en una lista
    :param elements: lista
    :param old: valor a reemplazar
    :param new: valor por el que se reemplaza
    :return: lista nueva con el valor reemplazado
    """
    result = []
    # elemento por elemento
    for elt in elements:
        # si el elemento es igual a old se añade el new a la nueva lista
        if elt == old:
            result.append(new)
        else:
            # si el elemento no es igual a old se añade el mismo elemento a la nueva lista
            result.append(elt)
    return result










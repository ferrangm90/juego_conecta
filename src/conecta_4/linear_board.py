from conecta_4.settings import BOARD_LENGTH, VICTORY_STRIKE
from conecta_4.list_utils import find_strike, make_list, index_first_element

class LinearBoard:
    """
    Representamos una sola columna.
    Los jugadores son:
    - Jugador 1 : x
    - Jugador 2 : o
    - Las posiciones vacías van a ser None
    """
    # ---------------------------------------------------
    #           CONSTRUCTORES / MÉTODOS DE CLASE
    # ---------------------------------------------------

    # creo una nueva linea a partir de una lista de datos que existe
    @classmethod
    def from_list(cls, data):
        """
        Clase para crear una nueva linea a partir de una lista de datos
        :param data: lista de datos
        :return: nueva linea del tablero
        """
        board = cls()
        #aquí estoy insertando los datos en la columna
        board._columns = data
        return board

    # ---------------------------------------------------
    #              DUNDERS / MÉTODOS MÁGICOS
    # ---------------------------------------------------

    # inicializo un objeto linea vacio (con Nones)
    def __init__(self):
        """
        Crea una sola columna y es como inicializamos el linear board
        return: nueva lista con Nones
        """
        self._columns = make_list(BOARD_LENGTH, None)
    
    # miro que sean de la misma clase y si es así comparo si la columna es igual a la otra columna
    def __eq__(self, other):
        """
        Me sirve para poder usar la equivalencia entre linear boards (==)
        :param other: otro linear board
        :return: True si son iguales, False si no
        """
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._columns == other._columns

    # convierto la lista a tupla porque las tuplas son hasheables y las listas no
    def __hash__(self):
        """
        No se usa pero es indispensable para el __eq__ para comparar objetos
        Sirve para ver si dos objetos comparten la misma memoria con is
        return: hash del objeto
        """
        return hash(tuple(self._columns))


    # ---------------------------------------------------
    #         MÉTODOS PÚBLICOS
    # ---------------------------------------------------

    # es un getter para obtener el contenido de la columna fuera de la clase
    def get_columns(self):
        """
        Obtengo la lista, es decir la columna
        return: lista
        """
        return self._columns

    # pregunto si la última posición es None para saber si la columna está llena
    def is_full(self):
        """
        Pregunto si el último valor es un None para saber si la lista esta llena
        return: True si esta llena, False si no
        """
        # -1 es la última posición
        return self._columns[-1] is not None

    # añado el valor 'o' o 'x' en la primera posición que sea None
    def add(self, char):
        """
        Añado el valor 'o' o 'x' en la primera posición que sea None
        :param char: valor a añadir
        :return: 
        """
        if not self.is_full():
            # busca el primer elemento vacío de la columna
            i = index_first_element(self._columns, None)
            # lo sustituye por el char
            self._columns[i] = char

    # mira si algun jugador cumple la racha y gana
    def is_victory(self, char):
        """
        Comprueba si hay victoria
        :param char: ficha del jugador
        :return: True si hay victoria, False si no
        """
        #llama a la funcion pasandole la columna, la ficha y la racha
        return find_strike(self._columns, char, VICTORY_STRIKE)

    # mira si el jugador 1 o el jugador 2 ha ganado, si ninguna ha ganado devuelve True
    def is_tie(self, char_1, char_2):
        """
        Comprueba si hay empate
        :param char_1: ficha del jugador 1
        :param char_2: ficha del jugador 2
        :return: True si hay empate, False si no
        """
        return ((self.is_victory(char_1) == False) and
                (self.is_victory(char_2) == False))
from conecta_4.linear_board import LinearBoard
from conecta_4.settings import BOARD_LENGTH
from conecta_4.list_utils import *

class SquareBoard:

    # ---------------------------------------------------
    #           CONSTRUCTORES / MÉTODOS DE CLASE
    # ---------------------------------------------------

    @classmethod
    def from_list(cls, list_of_list):
        """
        Crea un tablero de SquareBoard a partir de una lista de listas
        Transforma cada sublista en un LinearBoard con LinearBoard.from_list
        :param list_of_list: Lista de listas de fichas
        :return: Un objeto SquareBoard
        """
        board = cls()
        # Convierte cada sublista de datos en un objeto LinearBoard
        board._columns = map_list(list_of_list, LinearBoard.from_list)
        return board


    @classmethod
    def from_str_board(cls, str_board):
        """
        Reconstruye un SquareBoard a partir de un string
        :param str_board: matriz en texto
        :return: Un objeto SquareBoard
        """
        # Divide el texto por cada "|"en una lista de strings, cada elemento es una columna
        list_of_strings = str_board.split('|')
        # Transforma la lista de strings en una matriz
        matrix = explode_list(list_of_strings)
        # Convierte los puntos en None
        matrix = replace_all(matrix, '.', None)
        # Convierte la matriz en un SquareBoard
        return cls.from_list(matrix) 
        # el from_list de SquareBoard que en la funcion anterior usa LinearBoard.from_list


    @classmethod
    def from_board_code(cls, board_code):
        """
        Crea un SquareBoard a partir de un BoardCode (texto)
        Extrae la string almacenada en board_code.str_board y la pasa a from_str_board

        :param board_code: Un objeto de la clase BoardCode
        :return: Un objeto SquareBoard
        """
        return cls.from_str_board(board_code.str_board)

    # ---------------------------------------------------
    #              DUNDERS / MÉTODOS MÁGICOS
    # ---------------------------------------------------

    def __init__(self):
        """
        Crea el tablero con sus columnas vacias
        :return: Un objeto SquareBoard
        """
        #genera una lista de 4 columnas vacias usando la factoria LinearBoard
        self._columns = make_list_from_factory(BOARD_LENGTH, LinearBoard)
    

    def __repr__(self):
        """
        Define como se imprime el objeto
        :return: string
        """
        # imprime la clase y las columnas
        return f'{self.__class__}:{self._columns}'
    
    def __len__(self):
        """
        Devuelve el número total de columnas que tiene el tablero
        :return: el número de columnas
        """
        return len(self._columns)

    # Compara que sean de la misma clase y que sean iguales
    def __eq__(self, other):
        """
        Compara dos tableros
        :param other: tablero
        :return: True si son iguales, False si no
        """
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._columns == other._columns

    # convierto la lista a tupla porque las tuplas son hasheables y las listas no
    def __hash__(self):
        """
        Convierte la lista de columnas en una tupla y obtiene su hash, se necesita
        para el __eq__
        :return: hash del objeto
        """
        return hash(tuple(self._columns))
        
    # ---------------------------------------------------
    #                  MÉTODOS PÚBLICOS
    # ---------------------------------------------------

    def is_full(self):
        """
        Devuelve si el tablero esta lleno
        :return: True si el tablero esta lleno, False si no
        """
        result = True
        # pasamos por cada columna
        for linear_board in self._columns:
            # si result que es true y la columna esta llena, devuelve true
            # si result que es true y la columna no está llena devuelve False
            # el is.full es de linear_board no de esta misma función, obvio
            result = result and linear_board.is_full()
        return result


    def add(self, char, column):
        """
        Añade una ficha en la columna especificada
        :param char: la ficha 'x' o 'o'
        :param column: La columna donde se quiere jugar
        """
        # el add es de LinearBoard, no de SquareBoard
        result = self._columns[column].add(char)
        return result

    def as_matrix(self):
        """
        Convierte la estructura del objeto en una lista de listas
        :return: lista de listas
        """
        result = []
        # por cada columna de la estructura del objeto
        for column in self._columns:
            # añade la lista de fichas _columns de esa columna
            result.append(column._columns)
        return result

    def as_code(self):
        """
        Devuelve el tablero en objeto BoardCode
        :return: un objeto BoardCode
        """
        return BoardCode(self)

    def is_victory(self, char):
        """
        Da el resultado de si la ficha char ha conseguido hace linea
        :param char: caracter 'x' u 'o'
        :return: True si hay victoria, False en caso contrario
        """
        # esta hecho para que de true si se cumple cualquiera de las 4 condiciones
        return (self._any_vertical_victory(char) or
                self._any_descending_diagonal(char) or
                self._any_ascending_diagonal(char) or
                self._any_horizontal_victory(char))

    # ---------------------------------------------------
    #                 MÉTODOS PRIVADOS
    # ---------------------------------------------------

    def _any_vertical_victory(self, char):
        """
        Comprueba si existe un 4 en raya en alguna de las columnas
        :param char: caracter 'x' u 'o'
        :return: True si hay victoria, sino False
        """
        result = False
        #por cada columna del objeto
        for linear_board in self._columns:
            # el resultado solo es true si alguna columna da true
            result = result or linear_board.is_victory(char)
        return result

    def _any_horizontal_victory(self, char):
        """
        Comprueba si existe un 4 en raya en alguna de las filas
        :param char: caracter 'x' u 'o'
        :return: True si hay victoria, sino False
        """
        # transpone la matriz para pasar de columnas a filas y usar la función anterior
        transpose_matrix = transpose(self.as_matrix())
        #crea un tablero a partir de la matriz transpuesta
        transpose_board = SquareBoard.from_list(transpose_matrix)
        # comprueba con la función anterior si hay 4 en raya
        return transpose_board._any_vertical_victory(char)

    def _any_descending_diagonal(self, char):
        """
        Comprueba si existe un 4 en raya en alguna de las diagonales descendentes
        :param char: caracter 'x' u 'o'
        :return: True si hay victoria, sino False
        """
        # coge la matriz del tablero
        matrix = self.as_matrix()
        # desplaza la matriz para que las diagonales se conviertan en filas
        dm = displace_matrix(matrix)
        # crea un tablero a partir de la matriz desplazada
        displace_board = SquareBoard.from_list(dm)
        # comprueba con la función anterior si hay 4 en raya
        return displace_board._any_horizontal_victory(char)

    def _any_ascending_diagonal(self, char):
        """
        Comprueba si existe un 4 en raya en alguna de las diagonales ascendentes
        :param char: caracter 'x' u 'o'
        :return: True si hay victoria, sino False
        """
        # coge la matriz del tablero
        matrix = self.as_matrix()
        # invierte la matriz para que las diagonales ascendentes se conviertan en descendentes
        rm = reverse_matrix(matrix)
        # crea un tablero a partir de la matriz invertida
        reverse_board = SquareBoard.from_list(rm)
        # comprueba con la función anterior si hay 4 en raya, que ya hemos visto que llama a
        # las funciones anteriores y se aprovecha el mismo codigo
        return reverse_board._any_descending_diagonal(char)


class BoardCode:

    # ---------------------------------------------------
    #              DUNDERS / MÉTODOS MÁGICOS
    # ---------------------------------------------------

    def __init__(self, board):
        """
        Coge la matriz del tablero con as_matrix() y usa colpase_matrix para guardarla 
        en la variable privada _str_board como un string
        :param board: tablero
        """
        # la matriz se convierte en un string
        self._str_board = colpase_matrix(board.as_matrix())

    # es para comparar si son iguales pero averiguando antes si los dos son de la clase BoardCode
    def __eq__(self, other):
        """
        Compara dos tableros
        :param other: tablero
        :return: True si son iguales, False si no
        """
        if not isinstance(other, self.__class__):
            return False
        else:
            return self._str_board == other.str_board

    #nos permite que un objeto BoardCode se pueda usar como clave de un diccionario
    def __hash__(self):
        """
        Genera el hash del tablero
        :return: hash
        """
        return hash(self._str_board)
    
    # define como se imprime este objeto cuando hago print
    def __repr__(self):
        """
        Devuelve el string del tablero
        :return: string
        """
        return f'{self._str_board}:{self.__class__}'

    # ---------------------------------------------------
    #                     PROPIEDADES
    # ---------------------------------------------------
    @property
    def str_board(self):
        """
        Devuelve el string del tablero
        :return: string
        """
        # lee el string de la matriz del tablero
        return self._str_board





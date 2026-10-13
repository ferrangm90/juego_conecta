from random import choice

from conecta_4.oracle import *
from conecta_4.square_board import *
from conecta_4.move import *
from conecta_4.settings import BOARD_LENGTH

class Player:

    # ---------------------------------------------------
    #              DUNDERS / MÉTODOS MÁGICOS
    # ---------------------------------------------------

    def __init__(self, name, char = None, oracle = BaseOracle(), opponent = None):
        self.name = name
        self.char = char
        # una vez que el jugador entra a la partida, el tipo de "cerebro" no debería cambiar desde fuera
        # por eso lo de _
        self._oracle = oracle
        self.opponent = opponent
        self.last_moves = []

    # ---------------------------------------------------
    #                     PROPIEDADES
    # ---------------------------------------------------

    # PROPIEDAD: opponent es el enlace bidireccional entre jugadores
    #
    # dos variables:
    #   - self._opponent --> almacén privado en memoria que guarda al rival
    #   - self.opponent  --> es pública que activa el getter y el setter


    @property
    def opponent(self):
        """
        GETTER--> permite leer el oponente privado "(self._opponent)" 
        desde fuera escribiendo 'jugador.opponent'
        """
        return self._opponent
    @opponent.setter
    def opponent(self, other):
        """
        SETTER--> se activa automáticamente al hacer 'jugador1.opponent = jugador2'
        Guarda a 'jugador2' en el almacén privado de 'jugador1' y, para evitar
        hacerlo manualmente, enlaza automáticamente a 'jugador1' dentro del 
        almacén privado de 'jugador2', es decir en ambos sentidos

        Si no entraría en un bucle infinito ya que si yo le pongo el oponente y lo
        hago publico en el setter, el setter lo vuelve a poner como mi oponente por eso hay
        2 variables (private y public) para poder guardar el oponente
        """
        self._opponent = other
        if other is not None:
            other._opponent = self

    # ---------------------------------------------------
    #                  MÉTODOS PÚBLICOS
    # ---------------------------------------------------

    def play(self, board):
        """
        Elige la mejor columna donde jugar. Estas me las recomienda el oráculo
        :param board:
        :return:
        """
        (best, recommendations) = self._ask_oracle(board) # consultar al oraculo
        self._play_on(board, best.index, recommendations) # jugar


    # ---------------------------------------------------
    #                 MÉTODOS PRIVADOS
    # ---------------------------------------------------

    def _play_on(self, board, position, recommendations ):
        """
        Jugamos en la pocisión elegida de las jugadas recomendadas
        :param board:
        :param position:
        :param recommendation:
        :return:
        """
        board.add(self.char, position) # pone la ficha
        # guardo la jugada para tener un registro de movimientos hechos y así consultarlo y ver qué pasó
        self.last_moves.insert(0, Move(position, board.as_code(),recommendations, self)) 

    def _ask_oracle(self, board):
        """
        Pregunto al oráculo para que me de las posibles jugadas
        :param board:
        :return:
        """
        recommendations = self._oracle._get_recommendation(board, self) #consulto al oraculo
        best = self._choose_a_recommendation(recommendations) # Elijo la mejor jugada
        return (best, recommendations)

    # coge todas las recomendaciones del oráculo, columnas llenas y las ordena por prioridad y elige una
    def _choose_a_recommendation(self, recommendations):
        """
        Elijo una de las recomendaciones que me da el oráculo
        :param board:
        :return:
        """
        valid_recommendations = list(filter(lambda x:
                                            x.classification != ColumnClassification.FULL,
                                            recommendations)) # Usa filter para descartar las columnas que estén llenas
        # ordenamos la lista de mayor a menor porque en ColumnClassification los mejores valores son mas grandes
        valid_recommendations = sorted(valid_recommendations, key = lambda x : x.classification.value, reverse = True)
        if all_the_same_score(valid_recommendations): # si todos los valores son iguales
            return choice(valid_recommendations) # elige una al azar
        else:
            return valid_recommendations[0] # si no, elige la mejor

    # ---------------------------------------------------
    #                 MÉTODOS HOOK
    # ---------------------------------------------------

    def _on_lose(self):
        pass

class HumanPlayer(Player):
    """
    Esta clase no se testea porque son valores introducidos por el usuario
    Testeamos los valores que introduce el usuario
    """
    # ---------------------------------------------------
    #              DUNDERS / MÉTODOS MÁGICOS
    # ---------------------------------------------------

    def __init__(self, name, char = None): # iniciamos
        """
        Inicializa al jugador humano llamando al constructor de la clase padre
        :param name: nombre del jugador para el init del padre y para usarlo en el tablero y en el match
        :param char: ficha asignada ('x' u 'o')
        """
        super().__init__(name, char)

    # ---------------------------------------------------
    #                 MÉTODOS PRIVADOS
    # ---------------------------------------------------

    def _ask_oracle(self, board):
        """
        Mi oráculo es el jugador humano. Le pido que me de la posición a través de pantalla
        :param board:
        :return:
        """
        while True:
            position = input("Tu turno! Selecciona una columna: ")
            # comprobaciones de entrada correcta, que sea un entero, este dentro del rango
            # y la columna no este llena
            if (HumanEntryVerifications._is_int(position) and
                HumanEntryVerifications._is_in_range(board,int(position)) and
                HumanEntryVerifications._is_not_full(board, int(position))):
                position = int(position)
                # reotrna la recomendacion en tupla para el metodo play
                return (ColumnRecommendations(position,None), None)


class HumanEntryVerifications:
    """
    Clase auxiliar con métodos estáticos para validar la entrada de texto
    del usuario antes de ser procesada por el tablero.
    """

    # ---------------------------------------------------
    #                 MÉTODOS PRIVADOS
    # ---------------------------------------------------

    @staticmethod
    def _is_int(cadena):
        """
        Mira si el texto ingresado se puede convertir a número entero
        y evita que el programa falle si el usuario escribe letras o caracteres inválidos.
        :param cadena: string introducido por el usuario
        :return: True si es convertible a int, False si da error
        """
        try:
            num = int(cadena)
            return True
        except:
            return False

    @staticmethod
    def _is_not_full(board, col):
        """
        Mira que la columna elegida no esté completamente llena
        :param board: tablero en juego
        :param col: columna a comprobar
        :return: True si hay espacio, False si la columna esta llena
        """
        return not board._columns[col].is_full()

    @staticmethod
    def _is_in_range(board, col):
        """
        Mira que el número de columna esté dentro de los 
        límites del tablero
        :param board: tablero en juego
        :param col: columna a comprobar
        :return: True si el index existe en el tablero, sino False
        """
        return 0 <= col < len(board)



class ReportingPlayer(Player):
    """
    Le pide al oraculo la mejor recomendación de su base de datos de recomendaciones
    """
    # ---------------------------------------------------
    #                 MÉTODOS PRIVADOS
    # ---------------------------------------------------
    def _on_lose(self):
        """
        Sobrescribe el metodo vacío de la clase Player, see activa automáticamente 
        cuando el juego detecta que este jugador ha perdido entregando la lista de 
        movimientos (self.last_moves) al oráculo para ejecutar backtrack
        """
        self._oracle.back_track(self.last_moves)





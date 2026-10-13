from enum import Enum
from conecta_4.square_board import *
from conecta_4.settings import BOARD_LENGTH
from copy import deepcopy

class ColumnClassification(Enum):
    """
    Enumeracion que le da un valor numérico a cada columna segun
    la situacion de la columna
    """
    FULL = -1
    MAYBE = 10
    WIN = 100
    LOSE = 1
    BAD = 5

class ColumnRecommendations:

    # para las recomendaciones de la columna

    # ---------------------------------------------------
    #              DUNDERS / MÉTODOS MÁGICOS
    # ---------------------------------------------------


    def __init__(self, index, classification):
        """
        Guarda el index de la columna evaluada y la calificación asignada.
        :param index: número de la columna
        :param classification: Enum de ColumnClassification
        """
        self.index = index
        self.classification = classification

    # si quiero comparar dos 
    def __eq__(self, other):
        """
        Compara dos recomendaciones y devuelve True si son de la misma clase
        y tienen la misma clasificación
        :param other: un objeto ColumnRecommendations a comparar
        :return: True si tienen la misma clasificación, sino False
        """
        if not isinstance(other, self.__class__):
            return False
        else:
            return self.classification == other.classification

    def __hash__(self):
        """
        Genera el hash del objeto y permite guardar las recomendaciones en 
        claves de diccionarios
        :return: hash
        """
        return hash ((self.index, self.classification))


    #Si quiero imprimir las recomendaciones que me está dando necesito un __repr__
    def __repr__(self):
        """
        Representación legible en consola para depuración y visualización de recomendaciones.
        :return: string de la clase y la clasificación
        """
        return f'{self.__class__}: {self.classification}'

class BaseOracle:

    # Obtener las recomendaciones de las 4 columnas en una lista

    # ---------------------------------------------------
    #                 MÉTODOS PRIVADOS
    # ---------------------------------------------------
    
    def _get_recommendation(self, board, player):
        """
        Obtenemos recomenciones por column y las guardamos en una lista
        :param board:
        :param player:
        :return:
        """
        result = []
        for i in range(len(board)):
            # iteramos por columna y guardamos en una lista la recomendacion
            result.append(self._get_columns_recommendations(board, i, player))
        return result
    

    def _get_columns_recommendations(self, board, i, player):
        """
        Analiza una columna y calcula su puntuación
        Inicializa con MAYBE y actualiza a FULL si la columna está llena.

        :param board: el tablero
        :param i: index de la columna a analizar
        :param player: el jugador 'x' u 'o'
        :return: ColumnRecommendations con el índice y la clasificación
        """
        classification = ColumnClassification.MAYBE # inicializo en maybe
        if board._columns[i].is_full(): # compruebo si está llena
            classification = ColumnClassification.FULL # si está llena la marco como full
        return ColumnRecommendations(i, classification)

    # ---------------------------------------------------
    #                  MÉTODOS PÚBLICOS
    # ---------------------------------------------------

    # Comprueba si alguien ha ganado o el talbero está completo
    # revisa las recomendaciones obtenidas y si hay algun MAYBE o WIN avisa
    # de que hay resultados validos con un result = False y si no hay jugadas
    # devuelve un result = True
    def full_or_win(self, board, player):
        """
        Comprueba si hay alguna columna llena o si si alguien a ganado

        :param board: el tablero
        :param player: el jugador 'x' u 'o'
        :return: True si NO quedan alternativ (MAYBE o WIN), 
                 False si todavía hay al menos una columna jugable
        """
        recomendaciones = self._get_recommendation(board, player)
        result = True
        for recomendacion in recomendaciones:
            # si encuentra al menos una columna donde se puede ganar--> WIN
            # o que todavía es jugable--> MAYBE
            if(recomendacion.classification == ColumnClassification.WIN) or (recomendacion.classification == ColumnClassification.MAYBE):
                result = False
                break
        return result

    # ---------------------------------------------------
    #                 MÉTODOS HOOK
    # ---------------------------------------------------
    # Los hooks son métodos que se pueden sobreescribir en las clases hijas, abajo,
    # para modificar el comportamiento de la clase padre
    # sin romper la compatibilidad con las clases hijas
    def back_track(self, list_of_moves):
        pass
    def to_bad(self, move):
        pass



class SmartOracle(BaseOracle):
    """
    Hereda de BaseOracle (clase padre) y le da un poco de inteligencia
    Ahora no solo mira si la columna está llena, también mira si al poner una ficha gana o pierde
    """

    # ---------------------------------------------------
    #                 MÉTODOS PRIVADOS
    # ---------------------------------------------------

    #Ver si estamos si al poner en el MAYBE se gana o se pierde
    def _get_columns_recommendations(self, board, i, player):
        """
        Analiza una columna y calcula su puntuación, de las dudosas MAYBE comprueba
        si tira ahi y hay victora la reclasifica a WIN si no hay victoria comprueba
        si pierde la reclasifica a LOSE de lo contrario se queda en MAYBE  

        :param board: el tablero actual
        :param i: el index de la columna a analizar
        :param player: el jugador que va a mover 'x' u 'o'
        :return: ColumnRecommendations con la puntuación calculada
        """
        # llama a BaseOracle con super() para obtener la puntuacion de la columna i
        recommendations = super()._get_columns_recommendations(board, i, player)
        # de las columnas dudosas
        if recommendations.classification == ColumnClassification.MAYBE:
            # si mueve aqui y gana la reclasifica a WIN
            if self._is_winning_bet(board, i, player):
                recommendations.classification = ColumnClassification.WIN
            # si mueve aqui y pierde la reclasifica a LOSE
            elif self._is_losing_bet(board, i, player):
                recommendations.classification = ColumnClassification.LOSE
        
        return recommendations

    #Para verlo, vamos a crear un tablero temporal con deepcopy y jugar en el
    def _play_on_temporal_board(self, board, index, player):
        """
        Crea una copia temporal del tablero y agrega una ficha en la esa posición

        :param board: el tablero original
        :param index: el índice de la columna donde agregar la ficha
        :param player: el jugador que va a mover
        :return: una copia del tablero con la ficha agregada
        """
        # copia para no alterar el tablero original
        temporal_board = deepcopy(board)
        # agregamos la ficha en esa columna
        temporal_board.add(player.char, index)
        # devolvemos el tablero temporal
        return temporal_board

    #vamos a ver si gana la jugada en el tablero temporal
    def _is_winning_bet(self, board, index, player):
        """
        Comprueba si la jugada en la posición especificada será una victoria

        :param board: el tablero actual
        :param index: el índice de la columna donde se agregó la ficha
        :param player: el jugador que va a mover
        :return: True si hay victoria, si no False
        """
        # crea una copia temporal del tablero
        temporal_bet = self._play_on_temporal_board(board, index, player)
        # devuelve True si hay victoria
        return temporal_bet.is_victory(player.char)

    #vamos a ver si pierde la jugada en el tablero temporal
    def _is_losing_bet(self, board, index, player):
        """
        Comprueba si la jugada en la posición especificada será una derrota

        :param board: el tablero actual
        :param index: el índice de la columna donde se agregó la ficha
        :param player: el jugador que va a mover
        :return: True si hay derrota, si no False
        """
        # simula el tablero si el jugador mueve en index
        temporal_bet = self._play_on_temporal_board(board, index, player)
        losing_bet = False
        # recorre todas las columnas posibles del tablero resultante
        for i in range(0, BOARD_LENGTH):
            # comprueba si player.opponent tendría una jugada ganadora en la columna i 
            # inmediatamente después de nuestro movimiento
            if self._is_winning_bet(temporal_bet, i, player.opponent):
                #si es asi la marca como True
                losing_bet = True
                break
        # devuelve True si hay derrota, si no False
        return losing_bet



class MemoizationOracle(SmartOracle):
    """
    Para memorizar el get_recommendation
    """

    # ---------------------------------------------------
    #              DUNDERS / MÉTODOS MÁGICOS
    # ---------------------------------------------------

    def __init__(self):
        """
        Inicia el oráculo heredando todo lo de SmartOracle y crea un diccionario vacío 
        donde la clave será el estado del tablero y el valor será la lista de 
        recomendaciones calculadas
        """
        super().__init__()
        self.memo_recommendations = {}

    # ---------------------------------------------------
    #                 MÉTODOS PRIVADOS
    # ---------------------------------------------------

    def _make_key(self, board_code, player):
        """
        Genera una clave en texto único combinando el estado del tablero
        y el char del jugador actual porque un mismo estado del tablero puede ser 
        bueno o malo según a quién le toque mover, por eso combina el estado del 
        tablero con el jugador actual

        :param board_code: objeto BoardCode del tablero
        :param player: objeto Player 
        :return: cadena de texto identificadora (ej. "x..o|xx.o|....@o")
        """
        return f'{board_code.str_board}@{player.char}' # x..o|xx.o|....@o


    def _get_recommendation(self, board, player):
        """
        Mira si la posición actual ya existe en la memoria y si no existe, 
        la calcula llamando a SmartOracle y la guarda
        :param board: Tablero actual
        :param player: Jugador actual
        :return: Objeto con las recomendaciones del tablero
        """
        # genera la clave única para la posición actual
        key = self._make_key(board.as_code(), player)
        # pregunta si la posición NO está guardada en la caché
        if key not in self.memo_recommendations:
            # si es la primera vez que ve esa posición, llama a SmartOracle
            # para que haga el análisis simulado y guarda el resultado en el diccionario
            self.memo_recommendations[key] = super()._get_recommendation(board, player)
        # devuelve el resultado calculado o recuperado de la memoria
        return self.memo_recommendations[key]



class LearningOracle(MemoizationOracle):
    """
    Va a hacer dos cosas: Reclasificar y mirar hacia atrás (back_track)
    Aprende de sus propios errores. Si comete un error, lo guarda en memoria
    """
    # cuando pierde una partida:
    # coge el historial de todos los movimientos realizados en la partida (last_moves)
    # recorre las jugadas de la última a la primera --> backtrack
    # reclasifica la columna jugada cambiando su estado a BAD dentro del diccionario de memoria
    # aprende para que la próxima vez que se encuentre exactamente en esa misma situación elegirá otra opción

    # ---------------------------------------------------
    #                  MÉTODOS PÚBLICOS
    # ---------------------------------------------------

    def to_bad(self, move):
        """
        Reclasifica la columna jugada cambiando su estado a BAD en la memoria
        de recomendaciones
        :param move: objeto Move con los datos de la jugada realizada
        """
        # genera la clave única para la posición actual
        key = self._make_key(move.board_code, move.player)
        # recupera las recomendaciones para ese estado del tablero
        recomendaciones = self._get_recommendation(
            SquareBoard.from_board_code(move.board_code), move.player)
        # la marca como mala jugada
        recomendaciones[move.position] = ColumnRecommendations(move.position, ColumnClassification.BAD)
        # sustituimos el registro en la memoria del oráculo
        self.memo_recommendations[key] = recomendaciones

    

    def back_track(self, list_of_moves):
        """
        Recorre el historial de movimientos de una partida perdida y castiga 
        las decisiones tomadas con 'to_bad'
        :param list_of_moves: lista de objetos Move guardados
        """
        for move in list_of_moves:
            # castiga la jugada actual marcándola como mala
            self.to_bad(move)
            # reconstruye el tablero de esa jugada para ver las alternativas
            board = SquareBoard.from_board_code(move.board_code)
            #   comprueba si en este tablero todavía existian alternativas
            #   si NO todas las columnas eran derrotas inevitables, aquí fue donde se tomó
            #   la mala decisión teniendo opciones buenas. Se para el rastreo para no castigar 
            #   jugadas anteriores que fueron correctas.
            #   si la derrota ya era inevitable hiciera lo que hiciera, el bucle continúa 
            #   hacia atrás para castigar el error original que la llevó a este estado
            if not self.full_or_win(board, move.player):
                break





























class Move:

    # crea un objeto con la posicion, eltablero en ese momento, las recomendaciones y el jugador
    # se hace para pasar todo a la vez de una manera mas ordenada y si se quiere guardar un
    # registro de manera sencilla y si el dia de mañana quiero guardar otra propiedad mas
    # la añado aqui, haciendo ese proceso muy fácil
    def __init__(self, position, board_code, recommendation, player ):
        """
        Guarda la posicion, el tablero, las recomendaciones y el jugador
        :param position: posicion
        :param board_code: codigo del tablero
        :param recommendation: recomendaciones
        :param player: jugador
        """
        self.position = position
        self.board_code = board_code
        self.recommendation = recommendation
        self.player = player

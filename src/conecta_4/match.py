
# esta clase gestiona las reglas del juego, quien es quien, a quien le toca tirar
# y quien es cada ficha, y si se quiere jugar otra partida
class Match:

    # ---------------------------------------------------
    #              DUNDERS / MÉTODOS MÁGICOS
    # ---------------------------------------------------

    def __init__(self, player1, player2):
        """
        Guardamos los jugadores y asignamos a cada uno su ficha y su oponente
        :param player1: objeto de la clase player
        :param player2: objeto de la clase player
        """
        #Asignamos los char a mano. Después se elegiran al azar.
        player1.char = 'o'
        player2.char = 'x'
        # fijamos al oponente activando el oponent.setter
        player1.opponent = player2
        # crea un diccionario siendo la key la ficha y el valor el jugador
        # así el árbitro puede consultar que ficha tiene cada jugador de manera rápida
        self._players = {'o': player1, 'x': player2}
        # es una lista con los dos jugadores para el orden de cada turno
        self._round = [player1, player2]


    # ---------------------------------------------------
    #                     PROPIEDADES
    # ---------------------------------------------------

    # usa el decorador property porque queremos que sea una propiedad
    # del objeto aunque hace modificaciones y lleva el nombre "get" entonces no debería ser un property
    # al usar @property para poder acceder como 'match.get_next_player' sin paréntesis
    @property
    def get_next_player(self):
        """
        Mira el jugador de la lista (_round) para saber a quien le toca tirar.
        :return: El jugador al que le toca tirar
        """
        # el siguiente jugador es el primer elemento de la lista (_round)
        next_player = self._round[0]
        # despues invertimos la lista para que el siguiente jugador sea el siguiente en tirar
        # y asi sucesivamente cada vez
        self._round.reverse()
        return next_player

    # ---------------------------------------------------
    #         MÉTODOS PÚBLICOS
    # ---------------------------------------------------

    def get_player(self, char):
        """
        Devuelve que jugador tiene la ficha que se le pasa
        :param char: el valor 'x' o 'o' del jugador
        :return: el jugador que tiene ese valor
        """
        # accede al diccionario del creado en el __init__ y devuelve el valor que tiene esa key
        return self._players[char]

    def get_winner(self, board):
        """
        Mira en el tablero si la ficha que le pasa por parámetro ha ganado y devuelve el jugador ganador en
        caso de que no haya ganador devuelve None
        :param board:el tablero en juego
        :return:el jugador que ha ganado o None si no hay ganador
        """
        # pregunta al tablero si ha ganado o no la ficha 'x' y luego otro pregunta si ha ganado la ficha 'o'
        if board.is_victory('x'):
            # si ha ganado devuelve el jugador con esa ficha
            return self.get_player('x')
        if board.is_victory('o'):
            return self.get_player('o')
        else:
            return None # si no ha ganado ningun jugador devuelve none


    # igual que la de get_winner pero no tiene la opcion de retornar un NONE porque 
    # solo se la llama cuando ya sabemos que alguien ha ganado y obligatoriamente hay un perdedor
    def get_loser(self, board):
        """
        Mira en el tablero si la ficha ha perdido y devuelve el jugador
        :param board:el tablero en juego
        :return:el jugador que ha perdido
        """
        if board.is_victory('x'):
            return self.get_player('o')
        if board.is_victory('o'):
            return self.get_player('x')


    # pregunta al jugador en un bucle infinito hasta que responda con 's' o 'n' y devuelve ese
    # resultado
    def play_more(self):
        """
        Pregunta al usuario si quiere jugar una partida más
        :return: la respuesta si quiere jugar mas o no
        """
        result = True
        while True:
            answer = input('¿Quieres volver a jugar una partida más? S/N')
            if answer.lower() == 's':
                result = True
                break
            elif answer.lower() == 'n':
                result = False
                break
        return result
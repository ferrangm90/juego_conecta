import pyfiglet
from beautifultable import BeautifulTable

from enum import auto
from conecta_4.match import *
from conecta_4.player import *
from conecta_4.list_utils import *

class RoundType(Enum):
    """
    Define los tipos que se pueden jugar:
    - Humano contra Máquina
    - Máquina contra Máquina
    """
    Human_vs_Computer = auto()
    Computer_vs_Computer = auto()

class Level(Enum):
    """
    Define los niveles de dificultad para la Máquina:
    """
    LOW = auto()
    MEDIUM = auto()
    HIGH = auto()


class Game:

    # ---------------------------------------------------
    #              DUNDERS / MÉTODOS MÁGICOS
    # ---------------------------------------------------
    def __init__(self):
        """
        Iniciamos el tablero con un SquareBoard
        """
        self.board = SquareBoard()

    # ---------------------------------------------------
    #                  MÉTODOS PÚBLICOS
    # ---------------------------------------------------

    def start_game(self):
        """
        Iniciamos el juego
        """
        self._print_logo()
        self._configuration()
        self._game_loop()

    # ---------------------------------------------------
    #                 MÉTODOS PRIVADOS
    # ---------------------------------------------------

    def _print_logo(self):
        """
        Imprime logo del juego
        """
        logo = pyfiglet.Figlet(font = "swamp_land") # lo imprime utilizando pyfiglet para que sea mas chulo
        print(logo.renderText("Conecta 4"))

    def _configuration(self):
        """
        Configuración pedida al usuario
        """
        #Pedimos un tipo de ronda
        self.round_type = self._get_round_type()
        #Pedimos un nivel de dificultad
        if self.round_type == RoundType.Human_vs_Computer:
            self._difficulty_level = self._get_level()
        # creamos la partida
        self.match = self._match()


    def _get_round_type(self):
        """
        Usuario setea las opciones disponibles de rondas
        :return: tipo de partida
        """
        print("""
        Selecciona las opciones de juego:
        
        1) Humano vs Computadora
        2) Computer vs Computadora
        """)
        respuesta = ""
        while respuesta != '1' and respuesta != '2':# se queda en este bucle hasta que no ponga 1 o 2
            respuesta = input('Selecciona 1 ó 2: ')
        if respuesta == '1':
            return RoundType.Human_vs_Computer# juega el humano
        else:
            return RoundType.Computer_vs_Computer # juegan los ordenadores

    def _get_level(self):
        """
        Usuario setea las opciones disponibles de dificultad
        :return:
        """
        print("""
        Selecciona las opciones disponibles:

        1) Fácil
        2) Intermedio
        3) Difícil
        """)
        while True:# se queda en este bucle hasta que no ponga 1, 2 o 3
            repuesta = input("Selecciona entre 1, 2 ó 3: ")
            if repuesta == '1':
                level = Level.LOW
                break
            elif repuesta == '2':
                level = Level.MEDIUM
                break
            elif repuesta == '3':
                level = Level.HIGH
                break
        return level

    def _match(self):
        """
        Creamos los dos jugadores y la partida segun la dificultad elegida,
        El primero siempre va a ser ordenador
        :return: partida con los 2 jugadores
        """
        # se crea un diccionario con las dificultades
        _levels = {Level.LOW: BaseOracle(),
                   Level.MEDIUM : SmartOracle(),
                   Level.HIGH : LearningOracle()}
        # comprueba la modalidad de juego si hay humano o no
        if self.round_type == RoundType.Computer_vs_Computer:
            # se instancian dos jugadores automáticos
            player1 = ReportingPlayer('Ordenador 1', oracle=LearningOracle())
            player2 = ReportingPlayer('Ordenador 2', oracle=LearningOracle())
        else:
            # si hay un humano se instancia un jugador humano y un jugador automatico
            player1 = ReportingPlayer('Computer', oracle=_levels[self._difficulty_level]) #Posible bug # Resolución bug: Es _difficulty_level
            player2 = HumanPlayer(name = input('Ingrese su nombre: '))
        return Match(player1, player2)


    def _game_loop(self):
        """
        Es el bucle de eventos
        Mantiene el juego en marcha continuamente y la única forma de salir 
        de este bucle es mediante break
        :return:
        """
        while True:
            #Seleccionamos el jugador
            jugador_actual = self.match.get_next_player
            #Una vez con el juagador lo mandamos a jugar
            jugador_actual.play(self.board)
            #Muestro la jugada
            self._print_move(jugador_actual)
            #Muestro el tablero
            self._print_board()
            # Evaluamos el tablero. ¿Algún vencedor? ¿Empate?
            if self._winner_or_tie():
                #Muestro resultado
                self._print_result()
                #Pregunto si le apetece otra partida
                if self.match.play_more():
                    # reinicia el tablero a un estado vacío para la nueva ronda
                    self.board = SquareBoard()
                    self._print_board()
                else:
                    # sale del bucle infinito y finaliza la aplicación
                    break

    def _print_board(self):
        """
        Imprime tablero usando BeatifulTable
        :return:
        """
        #Covertimos tablero en una matriz y le damos la vuelta
        board_matrix = reverse_matrix(self.board.as_matrix())
        bt = BeautifulTable()   
        # Agrega las columnas a la tabla
        for col in board_matrix:
            bt.columns.append(col)
        # Establece los encabezados de las columnas
        bt.columns.header = [str(i) for i in range(BOARD_LENGTH)]
        #Imprimimos la tabla
        print(bt)

    def _print_result(self):
        """
        Muestra por pantalla el resultado final de la partida.
        Si hay un ganador, lo muestra junto a su rival,
        si es un empate muestra EMPATE
        """
        ganador = self.match.get_winner(self.board)
        perdedor = self.match.get_loser(self.board)
        if ganador is not None:
            print(f'{ganador.name} ({ganador.char}) GANA VS {perdedor.name} ({perdedor.char})')
        else:
            print('EMPATE')

    def _print_move(self, player):
        """
        Muestra por pantalla la ultima juagada de player
        """
        print(f'{player.name} ({player.char} ha movido en {player.last_moves[0].position})')

    def _winner_or_tie(self):
        """
        Comprueba si la partida ha finalizado por victoria o empate
        si es victoria notifica al perdedor con el hook '_on_lose'
        para activar el aprendizaje
        :return: True si la partida terminó, False si debe continuar
        """
        ganador = self. match.get_winner(self.board)
        if ganador is not None:
            # notifica la derrota al oponente para activar el backtrack _on_lose
            ganador.opponent._on_lose()
            return True
        elif self.board.is_full():
            return True
        else:
            return False






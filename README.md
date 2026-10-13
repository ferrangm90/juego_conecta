# Conecta 4

Este repositorio contiene una implementación del clásico juego Conecta 4 desarrollada íntegramente en Python. 
El proyecto está diseñado con un enfoque en la **Programación Orientada a Objetos (POO)**, 
la aplicación de buenas prácticas y el diseño de una Inteligencia Artificial para la toma de decisiones."

## Características Principales

* **Arquitectura Escalable:** El tamaño del tablero es paramétrico (definido por `BOARD_LENGTH`).
* **Patrón Estrategia (Strategy Pattern):** Desacoplamiento total entre `Player`y `Oracle`
* **Sistema de Clasificación Táctica:** Uso de enumeraciones (`Enum`) con valor numérico (`WIN = 100`, `MAYBE = 10`, `BAD = 5`, `LOSE = 1`) para priorizar decisiones.
* **Mecanismos de Optimización (Memoización):** Implementación de un sistema de caché que convierte el estado de los objetos del tablero en cadenas de texto inmutables (`BoardCode`) para almacenar y recuperar evaluaciones previas, reduciendo la complejidad temporal.
* **Aprendizaje por Refuerzo Negativo:** Desarrollo de un oráculo adaptativo (`LearningOracle`) que ejecuta un rastreo hacia atrás (*backtracking*) al perder una partida, reclasificando las jugadas defectuosas para no repetir errores en el futuro.

## Arquitectura de la Inteligencia Artificial

El proyecto cuenta con una jerarquía de "oráculos" (motores de IA) heredados:

1. **`BaseOracle`:** Analiza las posibles jugadas clonando el tablero en entornos temporales (`deepcopy`) para simular las respuestas inmediatas del rival.
2. **`MemoizationOracle`:** Resuelve el cuello de botella del coste computacional. Guarda en memoria el resultado del análisis de cada tablero (asociado al turno actual) para ofrecer respuestas instantáneas si se vuelve a llegar a la misma posición.
3. **`LearningOracle`:** Modifica el comportamiento de la IA basándose en el historial de la partida (`last_moves`). Cuando el sistema detecta una derrota, recorre el historial a la inversa y penaliza la decisión que provocó el fallo, alterando la caché para futuras partidas.

## Estructura del Proyecto

```text
conecta_4/
├── conecta4.py        # Punto de entrada y orquestador ejecutable del juego.
├── game.py            # Gestión del bucle principal (game loop), turnos y renderizado visual.
├── match.py           # Lógica de emparejamiento y control del estado global del enfrentamiento.
├── square_board.py    # Representación matricial 2D, límites y físicas de gravedad para la caída de fichas.
├── linear_board.py    # Comprobación de secuencias y victorias en líneas individuales (filas, columnas, diagonales).
├── player.py          # Definición de clases para jugadores (HumanPlayer y ReportingPlayer para la IA).
├── oracle.py          # Heurística, simulación temporales de estados, caché y aprendizaje tras derrota.
├── move.py            # Registro inmutable del historial de movimientos.
├── list_utils.py      # Utilidades algorítmicas para análisis y verificación de listas de fichas.
└── settings.py        # Configuración global del proyecto (dimensiones del tablero, caracteres y constantes).
```
## 🛠️ Requisitos e Instalación

Este proyecto requiere **Python 3.12** y las siguientes bibliotecas externas para la interfaz visual:

* `beautifultable`: Para la renderización gráfica del tablero en la terminal.
* `pyfiglet`: Para la generación de títulos y banners en arte ASCII.

### Instalación de dependencias:
```bash
pip install beautifultable pyfiglet
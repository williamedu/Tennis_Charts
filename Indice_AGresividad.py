import csv
import pandas as pd
from tkinter import Tk
from tkinter.filedialog import askopenfilename
import matplotlib.pyplot as plt
import numpy as np


# Crear una ventana principal de Tkinter (se cerrará inmediatamente)
root = Tk()
root.withdraw()

# Mostrar el cuadro de diálogo de selección de archivo
file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])

# Verificar si se seleccionó un archivo
if file_path:

    # Diccionario para almacenar las acciones agresivas y totales de cada jugador
    player_stats = {}

    # Leer el archivo CSV usando pandas
    data = pd.read_csv(file_path)

    # Iterar sobre cada fila del DataFrame
    for _, row in data.iterrows():
        player = row[' player'].strip()
        opponent = row[' opponent'].strip()
        action = row[' action'].strip()
        action_type = row[' actiontype'].strip()

        # Inicializar el diccionario para cada jugador si no existe
        if player not in player_stats:
            player_stats[player] = {'aggressive_actions': 0, 'total_actions': 0, 'winners': 0, 'forced_errors_caused': 0, 'approach_dropshots': 0, 'forced_errors_committed': 0}
        if opponent not in player_stats:
            player_stats[opponent] = {'aggressive_actions': 0, 'total_actions': 0, 'winners': 0, 'forced_errors_caused': 0, 'approach_dropshots': 0, 'forced_errors_committed': 0}

        # Contar acciones agresivas
        if action_type == 'WINNER':
            player_stats[player]['aggressive_actions'] += 1
            player_stats[player]['winners'] += 1
            player_stats[player]['total_actions'] += 1
        elif action_type == 'APPROACH_DROP':
            player_stats[player]['aggressive_actions'] += 1
            player_stats[player]['approach_dropshots'] += 1
            player_stats[player]['total_actions'] += 1

        # Contar forced errors causados y cometidos
        if action == 'FORCED_ERROR':
            player_stats[player]['forced_errors_committed'] += 1
            player_stats[opponent]['forced_errors_caused'] += 1
            player_stats[player]['total_actions'] += 1

        # Contar acciones totales para acciones no agresivas y no forzadas
        if action_type not in ['undefined', 'SERVICE_FAULT', 'WINNER', 'APPROACH_DROP'] and action != 'FORCED_ERROR':
            player_stats[player]['total_actions'] += 1

    # Mostrar estadísticas para cada jugador
    player_names = []
    aggressiveness_percentages = []
    winners_counts = []
    forced_errors_caused_counts = []
    approach_dropshots_counts = []
    forced_errors_committed_counts = []

    for player, stats in player_stats.items():
        aggressive_actions = stats['aggressive_actions']
        total_actions = stats['total_actions']
        winners = stats['winners']
        forced_errors_caused = stats['forced_errors_caused']
        approach_dropshots = stats['approach_dropshots']
        forced_errors_committed = stats['forced_errors_committed']

        if total_actions == 0:
            aggressiveness_percentage = 0.0
        else:
            aggressiveness_percentage = (aggressive_actions / total_actions) * 100

        player_names.append(player)
        aggressiveness_percentages.append(aggressiveness_percentage)
        winners_counts.append(winners)
        forced_errors_caused_counts.append(forced_errors_caused)
        approach_dropshots_counts.append(approach_dropshots)
        forced_errors_committed_counts.append(forced_errors_committed)

    # Obtener los nombres de los jugadores
    player1 = player_names[0]
    player2 = player_names[1]

    # Crear el gráfico de barras agrupadas
    fig, ax = plt.subplots(figsize=(10, 6))

    bar_width = 0.15
    opacity = 0.8

    index = pd.Index(player_names)
    bar_positions = np.arange(len(player_names))

    # Agresividad (%)
    aggressiveness_bars = ax.bar(bar_positions - 2 * bar_width, aggressiveness_percentages, bar_width, alpha=opacity,
                                 color='b', label='Agresividad (%)')
    for bar in aggressiveness_bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{height:.1f}%', ha='center', va='bottom')

    # Winners
    winners_bars = ax.bar(bar_positions - bar_width, winners_counts, bar_width, alpha=opacity, color='g',
                          label='Winners')
    for bar in winners_bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom')

    # Forced Errors Causados
    forced_errors_caused_bars = ax.bar(bar_positions, forced_errors_caused_counts, bar_width, alpha=opacity, color='r',
                                       label='Forced Errors Causados')
    for bar in forced_errors_caused_bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom')

    # Approach Dropshots
    approach_dropshots_bars = ax.bar(bar_positions + bar_width, approach_dropshots_counts, bar_width, alpha=opacity,
                                     color='c', label='Approach Dropshots')
    for bar in approach_dropshots_bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom')

    # Forced Errors Cometidos
    forced_errors_committed_bars = ax.bar(bar_positions + 2 * bar_width, forced_errors_committed_counts, bar_width,
                                          alpha=opacity, color='m', label='Forced Errors Cometidos')
    for bar in forced_errors_committed_bars:
        height = bar.get_height()
        ax.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}', ha='center', va='bottom')

    ax.set_xlabel('Jugador')
    ax.set_ylabel('Cantidad')
    ax.set_title(f'Estadísticas de los Jugadores: {player1} vs {player2}')
    ax.set_xticks(bar_positions)
    ax.set_xticklabels(player_names)
    ax.legend()

    plt.tight_layout()
    plt.show()
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk
from tkinter.filedialog import askopenfilename

# Crear una ventana principal de Tkinter (se cerrará inmediatamente)
root = Tk()
root.withdraw()

# Mostrar el cuadro de diálogo de selección de archivo
file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])

# Verificar si se seleccionó un archivo
if file_path:
    data = pd.read_csv(file_path)

    # Obtener los nombres de los jugadores
    jugador2 = data.iloc[0][' serving']
    jugador1 = data.iloc[0][' opponent']

    # Convertir la columna 'date' a tipo datetime
    data[' date'] = pd.to_datetime(data[' date'])

    # Agrupar los datos por game y calcular la duración en minutos
    game_duration = data.groupby(' game').agg({' date': ['min', 'max']})
    game_duration.columns = ['start_time', 'end_time']
    game_duration['duration_minutes'] = (game_duration['end_time'] - game_duration['start_time']).dt.total_seconds() / 60

    # Convertir la duración a formato "minutos:segundos"
    game_duration['duration_label'] = game_duration['duration_minutes'].apply(lambda x: f"{int(x)}:{int((x - int(x)) * 60):02d} min")

    # Calcular el tiempo total transcurrido y la mediana de tiempo por game
    total_duration = game_duration['duration_minutes'].sum()
    total_label = f"Tiempo total del juego: {int(total_duration)}:{int((total_duration - int(total_duration)) * 60):02d} min"
    median_duration = game_duration['duration_minutes'].median()
    median_label = f"Mediana de tiempo por game: {int(median_duration)}:{int((median_duration - int(median_duration)) * 60):02d} min"

    # Crear el gráfico de barras
    plt.figure(figsize=(10, 6))
    colors = ['#1f77b4', '#ff7f0e', '#2ca02c', '#d62728', '#9467bd', '#8c564b', '#e377c2', '#7f7f7f', '#bcbd22', '#17becf', '#9edae5', '#aec7e8']
    bars = plt.bar(game_duration.index, game_duration['duration_minutes'], color=colors[:len(game_duration)])

    # Personalizar el gráfico
    plt.xlabel('Game')
    plt.ylabel('Duration (minutes)')
    plt.title(f"{jugador1} vs {jugador2}")
    plt.xticks(game_duration.index)
    plt.ylim(0, 6)  # Establecer el límite superior del eje y en 15 minutos

    # Mostrar el valor de cada barra en formato "minutos:segundos min"
    for bar, label in zip(bars, game_duration['duration_label']):
        height = bar.get_height()
        plt.text(bar.get_x() + bar.get_width() / 2, height, label, ha='center', va='bottom')

    # Mostrar la leyenda con el tiempo total transcurrido y la mediana de tiempo por game
    legend_text = f"{total_label}\n{median_label}"
    plt.text(0.02, 0.95, legend_text, ha='left', va='top', transform=plt.gca().transAxes, fontsize=10, bbox=dict(facecolor='white', edgecolor='gray', boxstyle='round', alpha=0.8))

    # Guardar el gráfico con los nombres de los jugadores
    filename = f"{jugador1}_vs_{jugador2}_Mediana_de_tiempo.png"
    plt.savefig(filename)

    plt.tight_layout()
    plt.show()
else:
    print("No se seleccionó ningún archivo.")
import pandas as pd
import matplotlib.pyplot as plt
from tkinter import Tk, Label
from tkinter.filedialog import askopenfilename

# Crear una ventana principal de Tkinter (se cerrará inmediatamente)
root = Tk()
root.withdraw()

# Mostrar el cuadro de diálogo de selección de archivo
file_path = askopenfilename(filetypes=[("CSV Files", "*.csv")])

# Leer el archivo CSV
data = pd.read_csv(file_path)

# Eliminar espacios al inicio de los nombres de las columnas
data.columns = data.columns.str.strip()

# Obtener los nombres de los jugadores de las columnas "serving" y "opponent"
player1 = data['serving'].iloc[0].strip()
player2 = data['opponent'].iloc[0].strip()

# Función para contar las acciones de un jugador
def count_actions(player):
    actions = data[data['player'].str.strip() == player]['action'].value_counts()
    return actions

# Contar las acciones para cada jugador
player1_actions = count_actions(player1)
player2_actions = count_actions(player2)

# Imprimir las estadísticas de cada jugador
print(f"{player1}:")
for action, count in player1_actions.items():
    print(f"{action}: {count}")

print(f"\n{player2}:")
for action, count in player2_actions.items():
    print(f"{action}: {count}")

# Obtener todas las acciones únicas
all_actions = set(player1_actions.index) | set(player2_actions.index)

# Crear el gráfico de barras agrupado
fig, ax = plt.subplots(figsize=(10, 6))

# Definir la posición de las barras en el eje x
bar_width = 0.35
x = range(len(all_actions))

# Graficar las barras para el jugador 1
player1_counts = [player1_actions.get(action, 0) for action in all_actions]
player1_bars = ax.bar([i - bar_width/2 for i in x], player1_counts, width=bar_width, label=player1)

# Agregar los valores encima de las barras del jugador 1
for bar in player1_bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height, str(height), ha='center', va='bottom')

# Graficar las barras para el jugador 2
player2_counts = [player2_actions.get(action, 0) for action in all_actions]
player2_bars = ax.bar([i + bar_width/2 for i in x], player2_counts, width=bar_width, label=player2)

# Agregar los valores encima de las barras del jugador 2
for bar in player2_bars:
    height = bar.get_height()
    ax.text(bar.get_x() + bar.get_width()/2, height, str(height), ha='center', va='bottom')

# Configurar las etiquetas del eje x
ax.set_xticks(x)
ax.set_xticklabels(all_actions, rotation=45, ha='right')

# Configurar el título y las etiquetas de los ejes
ax.set_title("Acciones por Jugador")
ax.set_xlabel("Acción")
ax.set_ylabel("Cantidad")

# Mostrar la leyenda
ax.legend()

# Ajustar el espaciado entre las barras
fig.tight_layout()

# Mostrar el gráfico
plt.show()

# Crear una ventana de Tkinter para mostrar los datos en formato de tabla
data_window = Tk()
data_window.title("Datos de los Jugadores")

# Crear las etiquetas de encabezado
header_labels = ["Player"] + list(all_actions)
for col, header in enumerate(header_labels):
    label = Label(data_window, text=header, font=("Arial", 12, "bold"), padx=10, pady=5)
    label.grid(row=0, column=col, sticky="nsew")

# Mostrar los datos del jugador 1
player1_labels = [player1] + [str(player1_actions.get(action, 0)) for action in all_actions]
for col, value in enumerate(player1_labels):
    label = Label(data_window, text=value, font=("Arial", 12), padx=10, pady=5)
    label.grid(row=1, column=col, sticky="nsew")

# Mostrar los datos del jugador 2
player2_labels = [player2] + [str(player2_actions.get(action, 0)) for action in all_actions]
for col, value in enumerate(player2_labels):
    label = Label(data_window, text=value, font=("Arial", 12), padx=10, pady=5)
    label.grid(row=2, column=col, sticky="nsew")

# Iniciar el bucle principal de la ventana de datos
data_window.mainloop()
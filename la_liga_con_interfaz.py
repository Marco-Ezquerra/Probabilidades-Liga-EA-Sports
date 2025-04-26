# simulador_laliga_gui_final.py

import random
import math
import copy
from collections import defaultdict
import ttkbootstrap as ttk
from ttkbootstrap.constants import *
from tkinter import StringVar, filedialog
from tkinter.scrolledtext import ScrolledText
import csv
from tqdm import tqdm

# ─── PARTE DE DATOS ─────────────────────────────────────────────────
clasificacion_actual = {
    "Barcelona": 76, "Real Madrid": 72, "Atlético de Madrid": 66,
    "Athletic Club": 60, "Real Betis": 54, "Villarreal": 52,
    "Celta de Vigo": 46, "Osasuna": 44, "Mallorca": 44,
    "Real Sociedad": 42, "Rayo Vallecano": 41, "Getafe": 39,
    "Espanyol": 39, "Valencia": 39, "Sevilla": 37,
    "Girona": 35, "Alavés": 34, "Las Palmas": 32,
    "Leganés": 30, "Real Valladolid": 16
}

jornadas = {
    26: [('Villarreal', 'Espanyol')],
    34: [('Rayo Vallecano', 'Getafe'), ('Alavés', 'Atlético de Madrid'), ('Villarreal', 'Osasuna'),
         ('Las Palmas', 'Valencia'), ('Real Valladolid', 'Barcelona'), ('Real Madrid', 'Celta de Vigo'),
         ('Sevilla', 'Leganés'), ('Espanyol', 'Real Betis'), ('Real Sociedad', 'Athletic Club'),
         ('Girona', 'Mallorca')],
    35: [('Las Palmas', 'Rayo Vallecano'), ('Valencia', 'Getafe'), ('Celta de Vigo', 'Sevilla'),
         ('Girona', 'Villarreal'), ('Mallorca', 'Real Valladolid'), ('Atlético de Madrid', 'Real Sociedad'),
         ('Leganés', 'Espanyol'), ('Barcelona', 'Real Madrid'), ('Athletic Club', 'Alavés'),
         ('Real Betis', 'Osasuna')],
    36: [('Real Valladolid', 'Girona'), ('Real Sociedad', 'Celta de Vigo'), ('Sevilla', 'Las Palmas'),
         ('Alavés', 'Valencia'), ('Villarreal', 'Leganés'), ('Real Madrid', 'Mallorca'),
         ('Osasuna', 'Atlético de Madrid'), ('Rayo Vallecano', 'Real Betis'), ('Espanyol', 'Barcelona'),
         ('Getafe', 'Athletic Club')],
    37: [('Atlético de Madrid', 'Real Betis'), ('Barcelona', 'Villarreal'), ('Celta de Vigo', 'Rayo Vallecano'),
         ('Las Palmas', 'Leganés'), ('Mallorca', 'Getafe'), ('Osasuna', 'Espanyol'), ('Real Sociedad', 'Girona'),
         ('Real Valladolid', 'Alavés'), ('Sevilla', 'Real Madrid'), ('Valencia', 'Athletic Club')],
    38: [('Alavés', 'Osasuna'), ('Athletic Club', 'Barcelona'), ('Espanyol', 'Las Palmas'),
         ('Getafe', 'Celta de Vigo'), ('Girona', 'Atlético de Madrid'), ('Leganés', 'Real Valladolid'),
         ('Rayo Vallecano', 'Mallorca'), ('Real Betis', 'Valencia'), ('Real Madrid', 'Real Sociedad'),
         ('Villarreal', 'Sevilla')]
}

# ─── PARÁMETROS DEL MODELO ELO ───────────────────────────────────────
K = 30
H = 50
P_EMPATE = 0.25
S = 50
media_pts = sum(clasificacion_actual.values()) / len(clasificacion_actual)
elo_inicial = {team: 1200 + ((pts - media_pts) / 10) * S for team, pts in clasificacion_actual.items()}


def prob_local_gana(elo_local, elo_visit):
    return 1 / (1 + 10 ** (-(elo_local + H - elo_visit) / 400))

def simular_partido(local, visit, elo):
    p_win_local = prob_local_gana(elo[local], elo[visit])
    p_local = (1 - P_EMPATE) * p_win_local
    p_visit = (1 - P_EMPATE) * (1 - p_win_local)

    r = random.random()
    if r < p_local:
        res = 'L'
    elif r < p_local + P_EMPATE:
        res = 'E'
    else:
        res = 'V'

    s_local = {'L': 1, 'E': 0.5, 'V': 0}[res]
    s_visit = 1 - s_local
    e_local = p_local + 0.5 * P_EMPATE
    e_visit = 1 - e_local

    elo[local] += K * (s_local - e_local)
    elo[visit] += K * (s_visit - e_visit)
    return res

def simular_jornada(partidos, puntos, elo):
    for local, visit in partidos:
        resultado = simular_partido(local, visit, elo)
        if resultado == 'L':
            puntos[local] += 3
        elif resultado == 'V':
            puntos[visit] += 3
        else:
            puntos[local] += 1
            puntos[visit] += 1

def simular_liga():
    puntos = copy.deepcopy(clasificacion_actual)
    elo = copy.deepcopy(elo_inicial)
    for j in sorted(jornadas.keys()):
        simular_jornada(jornadas[j], puntos, elo)
    return puntos

# ─── FUNCIÓN DE SIMULACIÓN COMPLETA ────────────────────────────────
def run_simulacion():
    try:
        N = int(entry_nsim.get())
    except:
        text_resultados.delete(1.0, "end")
        text_resultados.insert("end", "Error: Número inválido")
        return

    campeones = defaultdict(int)
    champions=defaultdict(int)
    europa    = defaultdict(int)
    conference=defaultdict(int)
    descenso  = defaultdict(int)
    puntos_descenso = []

    for _ in tqdm(range(N), desc="Simulando ligas", leave=False):
        puntos = simular_liga()
        tabla = sorted(puntos.items(), key=lambda x: x[1], reverse=True)

        campeones[tabla[0][0]] += 1
        for team, _ in tabla[0:5]:
            champions[team] += 1
        for team, _ in tabla[5:7]:
            europa[team] +=1
        conference[tabla[7][0]] += 1
       
        for team, _ in tabla[-3:]:
            descenso[team] += 1
        
        puntos_descenso.append(tabla[-3][1])
    
    salida = f"Simulaciones realizadas: {N}\n"
    salida += "\n───────────── CAMPEONES ─────────────\n"
    for t in clasificacion_actual:
        salida += f"{t:20s}: {campeones[t]/N:6.2%}\n"

    salida += "\n───────────── Champions (TOP-5) ─────────────\n"
    for t in clasificacion_actual:
        salida += f"{t:20s}: {champions[t]/N:6.2%}\n"
     
    salida += "\n───────────── Europa (6 y 7)) ─────────────\n"
    for t in clasificacion_actual:
        salida += f"{t:20s}: {europa[t]/N:6.2%}\n"
    
    salida += "\n───────────── Conference (8) ─────────────\n"
    for t in clasificacion_actual:
        salida += f"{t:20s}: {conference[t]/N:6.2%}\n"


    salida += "\n───────────── DESCENSO ─────────────\n"
    for t in clasificacion_actual:
        salida += f"{t:20s}: {descenso[t]/N:6.2%}\n"
    
    salida += "\n───────────── PUNTOS PROMEDIO PARA SALVARSE ─────────────\n"
    salida += f"Puntos promedio para evitar el descenso: {sum(puntos_descenso) / len(puntos_descenso):.2f}\n"
     
    text_resultados.delete(1.0, "end")
    text_resultados.insert("end", salida)

# ─── FUNCIÓN GUARDAR CSV ─────────────────────────────────────────────
def guardar_resultados():
    fichero = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if fichero:
        with open(fichero, mode='w', newline='', encoding='utf-8') as f:
            f.write(text_resultados.get(1.0, "end"))

# ─── INTERFAZ GRÁFICA ────────────────────────────────────────────────
app = ttk.Window(themename="darkly")
app.title("Simulador LaLiga MonteCarlo + ELO")
app.geometry("1000x1000")

label_title = ttk.Label(app, text="Simulador LaLiga EA Sports 2025", font=("Helvetica", 20))
label_title.pack(pady=20)

frame_inputs = ttk.Frame(app)
frame_inputs.pack(pady=10)

label_nsim = ttk.Label(frame_inputs, text="Número de simulaciones:")
label_nsim.grid(row=0, column=0, padx=10)

entry_nsim = ttk.Entry(frame_inputs, width=15)
entry_nsim.insert(0, "100000")
entry_nsim.grid(row=0, column=1, padx=10)

btn_start = ttk.Button(frame_inputs, text="Iniciar simulación", command=run_simulacion, bootstyle="success")
btn_start.grid(row=0, column=2, padx=10)

btn_save = ttk.Button(frame_inputs, text="Guardar resultados", command=guardar_resultados, bootstyle="info")
btn_save.grid(row=0, column=3, padx=10)

frame_resultados = ttk.Frame(app)
frame_resultados.pack(pady=10, fill="both", expand=True)

text_resultados = ScrolledText(frame_resultados, font=("Courier", 10))
text_resultados.pack(fill="both", expand=True)

app.mainloop()

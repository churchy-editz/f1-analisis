from pathlib import Path

import fastf1
import pandas as pd

# --- Configuración (ya hecha) --------------------------------------------
# La caché se busca junto a este archivo, así funciona se ejecute desde donde se ejecute.
fastf1.Cache.enable_cache(Path(__file__).parent / "cache")
session = fastf1.get_session(2024, "Abu Dhabi", "R")
session.load(telemetry=False, weather=False, messages=False)

# --- TU PARTE ------------------------------------------------------------
# Elige un piloto que no sea VER (por ejemplo "NOR", "LEC" o "HAM").
piloto = "NOR"

# 1. Filtrar las vueltas de ese piloto.
# session.laps es un DataFrame con las vueltas de los 20 pilotos (una fila por vuelta).
# pick_drivers("NOR") devuelve otro objeto Laps con solo las filas de Norris.

laps_piloto = session.laps.pick_drivers(piloto)

# len() cuenta las filas, es decir, las vueltas: 58 en esta carrera.

print(len(laps_piloto))

# 2. Vuelta más rápida: número de vuelta, tiempo y neumático.
# pick_fastest() recorre las vueltas y devuelve UNA sola fila: la de menor LapTime.

mejor = laps_piloto.pick_fastest()
print(f"Vuelta más rápida de {piloto}:")

# mejor['Columna'] saca un dato de esa fila por el nombre de la columna.
# LapTime es un Timedelta (duración), por eso se imprime como "0 days 00:01:27.438".

print(f"Vuelta: {mejor['LapNumber']}, Tiempo: {mejor['LapTime']}, Neumático: {mejor['Compound']}")

# 3. Tiempo medio por compuesto, sin contar las vueltas de boxes.
# isna() es True donde el valor está vacío (NaT). En una vuelta normal ni se entra
# ni se sale de boxes, así que PitInTime y PitOutTime están vacíos. El "&" exige que
# se cumplan las dos condiciones a la vez, y así descartamos las vueltas de entrada
# a boxes y de salida de boxes, que son lentísimas y falsearían la media.

vueltas_limpias = laps_piloto[laps_piloto['PitOutTime'].isna() & laps_piloto['PitInTime'].isna()]

# groupby('Compound') agrupa las vueltas por neumático (HARD, MEDIUM...).
# ['LapTime'].mean() calcula, dentro de cada grupo, la media de los tiempos.
# El resultado es una Series con un valor por compuesto.

tiempo_medio_por_compuesto = vueltas_limpias.groupby('Compound')['LapTime'].mean()
print("Tiempo medio por compuesto:")

for compuesto, tiempo in tiempo_medio_por_compuesto.items():
    print(f"{compuesto}: {tiempo}")

# Mediana: el valor central al ordenar las vueltas. Casi no le afectan las vueltas raras.
# Con MEDIUM sale 1:29.139, bastante menos que su media (1:30.551): señal de que hay
# vueltas muy lentas (por ejemplo la 1 por la salida, o vueltas con coche de seguridad)
# que inflan la media. Qué vueltas son exactamente es algo que puedes comprobar tú.
tiempo_mediana_por_compuesto = vueltas_limpias.groupby('Compound')['LapTime'].median()
print("Tiempo mediana por compuesto:")

# .items() recorre la Series devolviendo pares (nombre del compuesto, valor).
for compuesto, tiempo in tiempo_mediana_por_compuesto.items():
    print(f"{compuesto}: {tiempo}")

# Mínimo: la mejor vuelta de cada compuesto (ritmo punta, no ritmo de carrera).
tiempo_minimo_por_compuesto = vueltas_limpias.groupby('Compound')['LapTime'].min()
print("Tiempo mínimo por compuesto:")

for compuesto, tiempo in tiempo_minimo_por_compuesto.items():
    print(f"{compuesto}: {tiempo}")

# 4. Respuesta: ¿con qué compuesto fue más rápido de media?
# Con el HARD: 1:28.079 de media frente a 1:30.551 con el MEDIUM, unos 2,5 s por vuelta
# más rápido. Aun así la comparación no es justa, porque los compuestos se usaron en
# momentos distintos de la carrera. El MEDIUM se usó al principio, con el depósito
# lleno (coche más pesado y por tanto más lento) y la pista todavía poco "gomada".
# El HARD se usó al final, con el coche mucho más ligero y la pista con más agarre.
# Por eso esta media no demuestra que el HARD sea mejor neumático: mezcla el efecto
# del compuesto con el del combustible y el estado de la pista.


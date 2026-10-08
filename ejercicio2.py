from pathlib import Path

import fastf1
import matplotlib.pyplot as plt
import pandas as pd

# --- Configuración (ya hecha) --------------------------------------------
fastf1.Cache.enable_cache(Path(__file__).parent / "cache")
session = fastf1.get_session(2024, "Abu Dhabi", "R")
session.load(telemetry=False, weather=False, messages=False)

# --- TU PARTE ------------------------------------------------------------
# Objetivo: comparar el ritmo REAL de dos pilotos, quitando las vueltas "raras".

# 1. Elige dos pilotos (por ejemplo "NOR" y "LEC") y guarda sus vueltas en dos variables.
# TODO

piloto1 = "NOR"
piloto2 = "LEC"

# 2. Convierte LapTime a segundos en una columna nueva llamada "Segundos".
#    Pista: .dt.total_seconds()
# TODO

vueltas_piloto1 = session.laps.pick_drivers(piloto1).copy()
vueltas_piloto1["Segundos"] = vueltas_piloto1["LapTime"].dt.total_seconds()

vueltas_piloto2 = session.laps.pick_drivers(piloto2).copy()
vueltas_piloto2["Segundos"] = vueltas_piloto2["LapTime"].dt.total_seconds() 

print(vueltas_piloto1)
print(vueltas_piloto2)

# 3. Quédate solo con las vueltas limpias de cada piloto:
#    - sin entrada ni salida de boxes (como en el ejercicio 1)
#    - sin la vuelta 1 (la salida es más lenta)
#    - sin vueltas más de un 107 % más lentas que su mediana (coche de seguridad, errores...)
#    Pista: calcula la mediana de "Segundos" y úsala en un filtro.
# TODO

vueltas_limpias_piloto1 = vueltas_piloto1[(vueltas_piloto1['PitOutTime'].isna() & vueltas_piloto1['PitInTime'].isna()) & 
                                          (vueltas_piloto1['LapNumber'] != 1) & (vueltas_piloto1['Segundos'] <= 1.07 * vueltas_piloto1['Segundos'].median())]

vueltas_limpias_piloto2 = vueltas_piloto2[(vueltas_piloto2['PitOutTime'].isna() & vueltas_piloto2['PitInTime'].isna()) & 
                                          (vueltas_piloto2['LapNumber'] != 1) & (vueltas_piloto2['Segundos'] <= 1.07 * vueltas_piloto2['Segundos'].median())]

print(vueltas_limpias_piloto1)
print(vueltas_limpias_piloto2)

# 4. Para cada piloto, imprime en una tabla: nº de vueltas limpias,
#    media y mediana de "Segundos". Pista: .agg([...]) o un DataFrame hecho a mano.
# TODO

tabla_piloto1 = pd.DataFrame({
    "Piloto": [piloto1],
    "Vueltas limpias": [len(vueltas_limpias_piloto1)],
    "Media Segundos": [vueltas_limpias_piloto1['Segundos'].mean()],
    "Mediana Segundos": [vueltas_limpias_piloto1['Segundos'].median()]
})

tabla_piloto2 = pd.DataFrame({
    "Piloto": [piloto2],
    "Vueltas limpias": [len(vueltas_limpias_piloto2)],
    "Media Segundos": [vueltas_limpias_piloto2['Segundos'].mean()],
    "Mediana Segundos": [vueltas_limpias_piloto2['Segundos'].median()]
})

print(tabla_piloto1)
print(tabla_piloto2)

# 5. Respuesta (como comentario): ¿quién tuvo mejor ritmo? ¿Cambia la conclusión si
#    usas la media o la mediana? ¿Por qué?
# TODO

# El mejor ritmo lo tuvo NOR (piloto 1): media 88.517 s y mediana 88.362 s, frente a
# LEC con 88.944 s y 88.565 s. El sentido de la conclusión no cambia con la media o la
# mediana, pero la magnitud sí: la ventaja es de 0.43 s con la media y solo 0.20 s con
# la mediana. Es decir, LEC tiene algunas vueltas lentas que le suben la media y su
# ritmo "normal" está más cerca del de NOR de lo que parece. Además, son coches
# distintos y han rodado en tráfico distinto, así que no mide solo al piloto.

# BONUS: dibuja con matplotlib los "Segundos" de ambos pilotos frente a "LapNumber"
#        (una línea por piloto) y guarda la imagen en una carpeta nueva "graficos".

# Carpeta de salida junto a este archivo; exist_ok=True evita error si ya existe.
carpeta_graficos = Path(__file__).parent / "graficos"
carpeta_graficos.mkdir(exist_ok=True)

# plt.subplots() crea la figura (el lienzo) y los ejes (donde se dibuja).
fig, ax = plt.subplots(figsize=(10, 5))

# Una línea por piloto: eje X = número de vuelta, eje Y = segundos.
# label= es el texto que saldrá en la leyenda.
ax.plot(vueltas_limpias_piloto1["LapNumber"], vueltas_limpias_piloto1["Segundos"],
        label=piloto1)
ax.plot(vueltas_limpias_piloto2["LapNumber"], vueltas_limpias_piloto2["Segundos"],
        label=piloto2)
ax.set_title(f"Ritmo de {piloto1} y {piloto2} en {session.event['EventName']} {session.event.year}")
ax.set_xlabel("Número de Vuelta")
ax.set_ylabel("Segundos")
ax.legend()


# TODO (tuyo): ponle título con ax.set_title(...), nombres a los ejes con
#              ax.set_xlabel(...) y ax.set_ylabel(...), y la leyenda con ax.legend().
#              Opcional: ax.grid(True), colores con color="...", marcadores con marker="o".

# Guarda la imagen. bbox_inches="tight" evita que se recorten los bordes.
fig.savefig(carpeta_graficos / "ritmo.png", dpi=150, bbox_inches="tight")
plt.show()


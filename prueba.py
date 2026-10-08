from pathlib import Path

import fastf1
import pandas as pd

# --- 1. Caché -----------------------------------------------------------
# FastF1 descarga los datos de internet; la caché los guarda en disco para
# que la próxima ejecución sea mucho más rápida y no repita descargas.
fastf1.Cache.enable_cache(Path(__file__).parent / "cache")

# --- 2. Cargar la sesión ------------------------------------------------
# Año 2024, Gran Premio de Abu Dabi, sesión "R" (Race = carrera).
session = fastf1.get_session(2024, "Abu Dhabi", "R")
# load() descarga/lee los datos. Desactivamos telemetría y meteo porque
# solo necesitamos los tiempos por vuelta (así carga más rápido).
session.load(telemetry=False, weather=False, messages=False)

# --- 3. Filtrar las vueltas de Verstappen -------------------------------
# session.laps es un DataFrame con todas las vueltas de todos los pilotos.
# "VER" es la abreviatura de tres letras de Max Verstappen.
laps_ver = session.laps.pick_drivers("VER")

# --- 4. Preparar una tabla limpia ---------------------------------------
# Nos quedamos solo con las columnas útiles y las renombramos.
tabla = laps_ver[["LapNumber", "LapTime", "Compound", "TyreLife", "Stint"]].copy()
tabla.columns = ["Vuelta", "Tiempo", "Neumático", "Edad neum.", "Stint"]

# LapTime es un Timedelta (duración). Lo convertimos a texto mm:ss.mmm.
def formatear(td):
    if pd.isna(td):  # vueltas sin tiempo registrado
        return "-"
    total = td.total_seconds()
    minutos = int(total // 60)
    return f"{minutos}:{total - minutos * 60:06.3f}"

tabla["Tiempo"] = tabla["Tiempo"].apply(formatear)
tabla["Vuelta"] = tabla["Vuelta"].astype(int)

# --- 5. Mostrar el resultado --------------------------------------------
print(f"{session.event['EventName']} {session.event.year} - Verstappen")
print(tabla.to_string(index=False))

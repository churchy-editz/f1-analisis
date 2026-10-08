# f1-analisis

Analisis de datos de Formula 1 con [FastF1](https://docs.fastf1.dev/), pandas y matplotlib.

## Puesta en marcha (Windows / PowerShell)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

## Cache de FastF1

Los datos descargados se guardan en la carpeta `cache/` (ignorada por Git).
Activala al inicio de tu script o notebook:

```python
import fastf1
fastf1.Cache.enable_cache("cache")
```

## Estructura

- `cache/`: cache local de FastF1
- `requirements.txt`: dependencias con versiones fijadas
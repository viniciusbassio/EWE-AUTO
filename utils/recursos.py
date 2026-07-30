import sys
from pathlib import Path


def caminho_recurso(relativo: str) -> str:
    if getattr(sys, "frozen", False):
        base = Path(sys._MEIPASS)
    else:
        base = Path(__file__).resolve().parent.parent

    return str(base / relativo)
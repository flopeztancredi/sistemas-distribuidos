#!/usr/bin/env python3
"""Une autoev-a/b/c en una sola seccion, detectando preguntas duplicadas.

Salida: sintesis/autoevaluacion.html (la consume ensamblar.py).
"""
import re
import sys
import unicodedata
from pathlib import Path

S = Path("/home/lopez/fiuba/distribuidos/apunte/fuentes/sintesis")
PARTES = ["autoev-a.html", "autoev-b.html", "autoev-c.html"]

CAB = """<section class="unidad" id="autoev" data-titulo="Autoevaluacion">
  <h2>Autoevaluación: preguntas de finales resueltas</h2>
  <p class="intro">Banco de preguntas tomadas en finales de la materia entre 2022 y 2025,
  agrupadas por tema y con la respuesta desplegable. La fecha entre paréntesis indica
  en qué final apareció. Conviene intentar responder antes de abrir, y usar los enlaces
  del final de cada respuesta para volver a la sección del apunte donde se estudia el tema.</p>
"""


def clave(s: str) -> str:
    """Normaliza un enunciado para comparar: sin tildes, sin puntuacion, minusculas."""
    s = re.sub(r"<[^>]+>", " ", s)
    s = unicodedata.normalize("NFKD", s).encode("ascii", "ignore").decode().lower()
    s = re.sub(r"[^a-z0-9 ]", " ", s)
    return " ".join(s.split())


def main() -> int:
    cuerpos, faltan = [], []
    for p in PARTES:
        f = S / p
        if f.exists():
            cuerpos.append((p, f.read_text(encoding="utf-8").strip()))
        else:
            faltan.append(p)
    if faltan:
        print(f"!! faltan partes: {faltan}", file=sys.stderr)
        return 1

    todo = "\n\n".join(c for _, c in cuerpos)

    # duplicados por enunciado (aviso, no borra: el criterio es humano)
    sums = re.findall(r"<summary>(.*?)</summary>", todo, re.S)
    vistos, dups = {}, []
    for s in sums:
        k = clave(s)[:90]
        if k in vistos:
            dups.append(clave(s)[:70])
        vistos[k] = True

    salida = CAB + "\n" + todo + "\n</section>\n"
    (S / "autoevaluacion.html").write_text(salida, encoding="utf-8")

    n_preg = len(re.findall(r'<details class="preg">', salida))
    n_h3 = len(re.findall(r"<h3 ", salida))
    print(f"autoevaluacion.html: {n_h3} bloques, {n_preg} preguntas, "
          f"{len(salida)//1024} KB")
    for p, c in cuerpos:
        print(f"   {p}: {len(re.findall(r'<details class=.preg.>', c))} preguntas")
    if dups:
        print(f"!! {len(dups)} enunciado(s) posiblemente duplicados:")
        for d in dups:
            print("      -", d)
    return 0


if __name__ == "__main__":
    sys.exit(main())

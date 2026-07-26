#!/usr/bin/env python3
"""Genera el glosario del apunte a partir de los bloques .def de cada unidad.

No inventa contenido: toma el termino en negrita y la primera oracion de cada
definicion, y las indexa alfabeticamente con enlace a la seccion donde se
estudia. Salida: sintesis/glosario.html
"""
import html
import re
import sys
import unicodedata
from pathlib import Path

S = Path("/home/lopez/fiuba/distribuidos/apunte/fuentes/sintesis")
ORDEN = ["u01", "u02", "u03", "u04", "u05", "u06", "u07", "u09", "u10",
         "u11", "u13", "u15", "u16", "u17", "u19", "u20", "u21"]

CAB = """<section class="unidad" id="glosario" data-titulo="Glosario">
  <h2>Glosario</h2>
  <p class="intro">Índice alfabético de los términos definidos en el apunte, con
  la unidad donde se estudia cada uno. Sirve para repasar antes del final o para
  ubicar rápido un concepto que aparece citado en otra sección.</p>
"""

TITULOS = {}


def clave_orden(t: str) -> str:
    t = unicodedata.normalize("NFKD", t).encode("ascii", "ignore").decode()
    return re.sub(r"[^a-zA-Z0-9 ]", "", t).lower().strip()


def main() -> int:
    entradas = []
    for uid in ORDEN:
        f = S / f"{uid}.html"
        if not f.exists():
            print(f"!! falta {f.name}", file=sys.stderr)
            return 1
        txt = f.read_text(encoding="utf-8")
        m = re.search(r"<h2[^>]*>(.*?)</h2>", txt, re.S)
        TITULOS[uid] = re.sub(r"<[^>]+>", "", m.group(1)).strip() if m else uid

        # recorrer el archivo llevando cuenta del ultimo h3/h4 con id, para
        # que cada definicion apunte a su seccion y no solo a la unidad
        pos_sec = [(mm.start(), mm.group(1))
                   for mm in re.finditer(r'<h[34][^>]*\sid="([^"]+)"', txt)]
        for d in re.finditer(r'<div class="def">\s*<b>(.*?)</b>(.*?)</div>',
                             txt, re.S):
            termino = re.sub(r"<[^>]+>", "", d.group(1)).strip().rstrip(".")
            cuerpo = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", d.group(2)))
            # primera oracion, sin cortar en abreviaturas obvias
            frase = re.split(r"(?<=[a-zá-ú0-9\)])\.\s", cuerpo.strip())[0]
            frase = frase.strip().rstrip(".")
            if len(frase) > 320:
                frase = frase[:317].rsplit(" ", 1)[0] + "..."
            ancla = uid
            for p, i in pos_sec:
                if p < d.start():
                    ancla = i
                else:
                    break
            if termino:
                entradas.append((termino, frase, uid, ancla))

    entradas.sort(key=lambda e: clave_orden(e[0]))

    partes = [CAB]
    letra_actual = None
    for termino, frase, uid, ancla in entradas:
        letra = clave_orden(termino)[:1].upper() or "#"
        if letra != letra_actual:
            if letra_actual is not None:
                partes.append("  </dl>\n")
            partes.append(f'  <h3 id="glo-{letra}">{letra}</h3>\n  <dl class="glo">\n')
            letra_actual = letra
        num = uid[1:].lstrip("0")
        partes.append(
            f"    <dt>{html.escape(termino)}</dt>\n"
            f"    <dd>{html.escape(frase)} "
            f'<a href="#{ancla}">U{num}</a></dd>\n')
    partes.append("  </dl>\n</section>\n")

    (S / "glosario.html").write_text("".join(partes), encoding="utf-8")
    print(f"glosario.html: {len(entradas)} terminos, "
          f"{len(set(clave_orden(e[0])[:1] for e in entradas))} letras")
    por_u = {}
    for _, _, uid, _ in entradas:
        por_u[uid] = por_u.get(uid, 0) + 1
    print("  " + "  ".join(f"{u}:{n}" for u, n in sorted(por_u.items())))
    return 0


if __name__ == "__main__":
    sys.exit(main())

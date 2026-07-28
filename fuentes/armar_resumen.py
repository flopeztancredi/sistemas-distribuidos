#!/usr/bin/env python3
"""Ensambla la subpagina conceptual de repaso en resumen/index.html."""

import re
import sys
from pathlib import Path

import adaptar_estetica as base


BASE = Path(__file__).resolve().parent
OUT = BASE.parent / "resumen" / "index.html"

GRUPOS = [
    ("Fundamentos", [
        ("r01", "01", "Modelo distribuido y diseño"),
        ("r02", "02", "Concurrencia y comunicación local"),
        ("r03", "03", "Paralelización y arquitectura física"),
    ]),
    ("Comunicación", [
        ("r04", "04", "Protocolos e invocación remota"),
        ("r05", "05", "Patrones, middleware y mensajería"),
        ("r06", "06", "Cómputo distribuido"),
    ]),
    ("Escala y datos", [
        ("r07", "07", "Escala, disponibilidad y cloud"),
        ("r08", "08", "Datos distribuidos"),
        ("r09", "09", "App Engine y BigTable"),
        ("r10", "10", "Diseño de gran escala"),
    ]),
    ("Corrección distribuida", [
        ("r11", "11", "Fallos, coordinación y transacciones"),
        ("r12", "12", "Tiempo, orden y snapshots"),
        ("r13", "13", "Consenso y elección de líder"),
        ("r14", "14", "Sistemas de tiempo real"),
    ]),
]


def main() -> int:
    OUT.parent.mkdir(parents=True, exist_ok=True)
    base.SINT = BASE / "resumen"
    base.OUT = OUT
    base.GRUPOS = GRUPOS

    resultado = base.main()
    if resultado:
        return resultado

    doc = OUT.read_text(encoding="utf-8")
    doc = re.sub(
        r"<title>.*?</title>",
        "<title>Resumen conceptual | Sistemas Distribuidos (75.74)</title>",
        doc,
        flags=re.S,
    )
    doc = re.sub(
        r'<meta name="description" content="[^"]*"',
        '<meta name="description" content="Resumen conceptual y autocontenido de '
        'Sistemas Distribuidos (75.74, FIUBA)"',
        doc,
    )
    doc = re.sub(
        r'<header class="hero">.*?</header>',
        '<header class="hero">\n'
        '        <h1>Resumen conceptual de Sistemas Distribuidos</h1>\n'
        '        <p>Una explicación autocontenida, ordenada por problemas y '
        'decisiones de diseño. <a href="../">Abrir el apunte completo</a>.</p>\n'
        '      </header>',
        doc,
        flags=re.S,
    )
    doc = doc.replace("'sd-", "'sd-resumen-")
    doc = re.sub(
        r'<a class="icon-button wide" href="resumen/">.*?</a>',
        '<a class="icon-button wide" href="../">Apunte completo</a>',
        doc,
        flags=re.S,
    )
    doc = "\n".join(line.rstrip() for line in doc.splitlines()) + "\n"
    OUT.write_text(doc, encoding="utf-8")
    print(f"ajustada identidad del resumen: {OUT}")
    return 0


if __name__ == "__main__":
    sys.exit(main())

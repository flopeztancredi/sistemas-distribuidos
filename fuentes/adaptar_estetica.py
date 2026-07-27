#!/usr/bin/env python3
"""Ensambla el apunte usando el shell de flopeztancredi/aprendizaje-automatico.

Reusa el CSS y el JS de ese repo tal cual (sidebar, buscador, resaltado, notas,
progreso, checkboxes de tema preparado) y transforma los fragmentos propios al
markup que ese shell espera.

Entrada:  fuentes/shell-aa.html  (index.html del repo de referencia)
          fuentes/sintesis/*.html
Salida:   index.html (asi lo sirve GitHub Pages)
"""
import html
import re
import sys
import unicodedata
from pathlib import Path

BASE = Path("/home/lopez/fiuba/distribuidos/apunte/fuentes")
SHELL = BASE / "shell-aa.html"
# El modulo de sincronizacion es el mismo para todos los apuntes. La copia que
# manda es la del repo de la portada; aca hay un duplicado porque los repos son
# independientes, y el build avisa si se separaron.
SYNC = BASE / "sync.html"
SYNC_CANONICO = Path("/home/lopez/fiuba/flopeztancredi.github.io/fuentes/sync.html")
SINT = BASE / "sintesis"
OUT = Path("/home/lopez/fiuba/distribuidos/apunte/index.html")

# (id, numero para la insignia, titulo corto para la sidebar)
GRUPOS = [
    ("Fundamentos", [
        ("u01", "01", "Introducción a Sistemas Distribuidos"),
        ("u02", "02", "Multitasking y comunicaciones"),
        ("u03", "03", "Paralelización, nombres y documentación"),
    ]),
    ("Diseño y comunicación", [
        ("u04", "04", "Layers, interfaces, protocolos y REST"),
        ("u05", "05", "Mensajes, grupos, middlewares y MOMs"),
        ("u06", "06", "Práctica de diseño multicomputing"),
        ("u07", "07", "Patrones de comunicación y ZeroMQ"),
    ]),
    ("Arquitecturas y datos", [
        ("u09", "09", "Arquitecturas distribuidas simples"),
        ("u10", "10", "Distribución y coordinación de procesos"),
        ("u11", "11", "Sistemas elásticos y alta disponibilidad"),
        ("u13", "13", "Data intensive applications"),
    ]),
    ("Escala y cloud", [
        ("u15", "15", "Arquitecturas de gran escala"),
        ("u16", "16", "SOA, cloud, PaaS y BigTable"),
    ]),
    ("Fallos, consenso y tiempo", [
        ("u17", "17", "Tolerancia a fallos"),
        ("u19", "19", "Algoritmos de consenso"),
        ("u20", "20", "Tiempo, relojes, orden y estado"),
        ("u21", "21", "Sistemas de tiempo real"),
    ]),
    ("Para el final", [
        ("autoev", "P", "Autoevaluación: finales resueltos"),
        ("glosario", "G", "Glosario"),
    ]),
]

CLASES = {
    "def": "callout",
    "idea": "callout blue",
    "ej": "callout example",
    "warn": "callout warning",
    "examen": "callout exam",
}

# CSS propio, escrito con los tokens del shell de referencia
CSS_EXTRA = """
    /* ---- agregados para este apunte ---- */
    .callout.example { border-color: var(--ok); background: var(--ok-bg); color: var(--ok); }
    .callout.exam { border-color: var(--exam); background: var(--exam-bg); color: var(--exam); }
    .callout > b:first-child, .callout > strong:first-child { color: inherit; }
    .callout.blue::before { content: "Intuición"; }
    .callout.example::before { content: "Ejemplo"; }
    .callout.warning::before { content: "Ojo"; }
    .callout.exam::before { content: "Tomado en finales"; }
    .callout.blue::before, .callout.example::before,
    .callout.warning::before, .callout.exam::before {
      display: block;
      margin-bottom: 6px;
      font-size: 10px;
      font-weight: 800;
      letter-spacing: .1em;
      text-transform: uppercase;
      opacity: .85;
    }
    p.intro {
      margin: 0 0 26px;
      color: var(--muted);
      font-size: 18px;
      line-height: 1.6;
    }
    pre {
      margin: 16px 0 22px;
      padding: 16px 18px;
      overflow-x: auto;
      border: 1px solid var(--line);
      border-radius: 14px;
      background: var(--surface-2);
      font-size: 13.5px;
      line-height: 1.55;
    }
    pre code { font-size: inherit; }
    :not(pre) > code {
      padding: 1px 6px;
      border-radius: 6px;
      background: var(--surface-2);
    }
    figure.diag {
      margin: 22px 0;
      padding: 18px 16px 12px;
      border: 1px solid var(--line);
      border-radius: 16px;
      background: var(--surface);
      text-align: center;
    }
    /* Alias que usan los SVG de los fragmentos (ver contrato-fragmento.md).
       Van en :root, no en figure.diag, porque hay diagramas fuera de figure.
       --linea no apunta a --line: ese token es un borde decorativo de 1.2:1 y
       como trazo de diagrama no se vería. Las flechas necesitan --muted. */
    :root, html[data-theme="dark"] {
      --linea: var(--muted);
      --acc: var(--accent);
      --acc2: var(--blue);
    }
    figure.diag svg { max-width: 100%; height: auto; color: var(--ink); }
    figure.diag figcaption {
      margin-top: 12px;
      color: var(--muted);
      font-size: 13px;
      line-height: 1.5;
      text-align: left;
    }
    p.nota {
      margin: 14px 0;
      padding-left: 14px;
      border-left: 3px solid var(--line);
      color: var(--muted);
      font-size: 14.5px;
    }
    p.ref {
      margin: 14px 0 0;
      padding-top: 10px;
      border-top: 1px dashed var(--line);
      color: var(--muted);
      font-size: 13.5px;
    }
    dl.glo {
      display: grid;
      grid-template-columns: minmax(170px, auto) 1fr;
      gap: 9px 22px;
      margin: 12px 0 26px;
      align-items: baseline;
    }
    dl.glo dt { font-weight: 700; }
    dl.glo dd { margin: 0; color: var(--muted); font-size: 15px; }
    dl.glo dd a {
      margin-left: 4px;
      padding: 1px 6px;
      border: 1px solid var(--line);
      border-radius: 6px;
      color: var(--accent);
      font-size: 12px;
      font-weight: 700;
      text-decoration: none;
      white-space: nowrap;
    }
    dl.glo dd a:hover { border-color: var(--accent); background: var(--accent-2); }
    @media (max-width: 640px) {
      dl.glo { grid-template-columns: 1fr; gap: 2px; }
      dl.glo dt { margin-top: 12px; }
    }
"""

# Paleta propia: lavanda, para que esta materia se distinga a simple vista de
# Aprendizaje Automatico (que usa turquesa). Se mantienen los nombres de token,
# asi que todo el CSS del shell sigue funcionando sin tocarlo.
PALETA_LIGHT = """:root {
      color-scheme: light;
      --bg: #faf8ff;
      --surface: #ffffff;
      --surface-2: #f2eefc;
      --ink: #241f33;
      --muted: #6f6885;
      --line: #e5dff5;
      --accent: #7455d8;
      --accent-2: #eee9fd;
      --accent-ink: #4e35a3;
      --warm: #96591c;
      --warm-bg: #fdf2e1;
      --danger: #a63a56;
      --danger-bg: #fdebf0;
      --blue: #276b93;
      --blue-bg: #e6f2f8;
      --ok: #35704a;
      --ok-bg: #e9f5ec;
      --exam: #a83a7d;
      --exam-bg: #fceaf4;
      --hl-yellow: #ffe08a;
      --hl-mint: #a8e6c8;
      --hl-pink: #ffc1d2;
      --hl-blue: #cdc4ff;
      --shadow: 0 18px 55px rgba(56, 38, 88, .08);
      --radius: 18px;
      --sidebar: 292px;
    }"""

PALETA_DARK = """html[data-theme="dark"] {
      color-scheme: dark;
      --bg: #16121f;
      --surface: #201a2d;
      --surface-2: #2b2340;
      --ink: #f2eefa;
      --muted: #aca3bd;
      --line: #3a2f52;
      --accent: #c0a5fb;
      --accent-2: #322449;
      --accent-ink: #e9deff;
      --warm: #f0b766;
      --warm-bg: #3b2c19;
      --danger: #f097ad;
      --danger-bg: #3f2029;
      --blue: #7ec8e8;
      --blue-bg: #16323f;
      --ok: #86cf9b;
      --ok-bg: #1a2f21;
      --exam: #e79ac9;
      --exam-bg: #3a1f31;
      --hl-yellow: #6f5a18;
      --hl-mint: #1f5c40;
      --hl-pink: #6e3549;
      --hl-blue: #443577;
      --shadow: 0 18px 55px rgba(0, 0, 0, .3);
    }"""

# sombras y overlay con tinte azulado que quedaban fuera de los tokens
SOMBRAS = {
    "rgba(18, 44, 58, .1)": "rgba(56, 38, 88, .12)",
    "rgba(15, 25, 22, .2)": "rgba(40, 26, 66, .22)",
    "rgba(7, 23, 31, .36)": "rgba(26, 18, 44, .42)",
}


def slug_kw(texto: str) -> str:
    t = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode().lower()
    t = re.sub(r"[^a-z0-9 ]", " ", t)
    palabras = [w for w in t.split() if len(w) > 2]
    vistas, out = set(), []
    for w in palabras:
        if w not in vistas:
            vistas.add(w)
            out.append(w)
    return " ".join(out)


def transformar(frag: str, uid: str, numero: str) -> str:
    # cabecera de capitulo
    m = re.search(r"<h2[^>]*>(.*?)</h2>", frag, re.S)
    titulo = re.sub(r"\s+", " ", re.sub(r"<[^>]+>", "", m.group(1))).strip()
    titulo = re.sub(r"^U\d+\.\s*", "", titulo)

    # palabras clave para el buscador: titulo + h3 + h4
    heads = [re.sub(r"<[^>]+>", "", h) for h in
             re.findall(r"<h[34][^>]*>(.*?)</h[34]>", frag, re.S)]
    kw = slug_kw(titulo + " " + " ".join(heads))

    cuerpo = frag[m.end():]
    cuerpo = cuerpo.rstrip()
    if cuerpo.endswith("</section>"):
        cuerpo = cuerpo[: -len("</section>")]

    # bloques propios -> callouts del shell
    for viejo, nuevo in CLASES.items():
        cuerpo = cuerpo.replace(f'<div class="{viejo}">', f'<div class="{nuevo}">')

    # details: envolver el cuerpo en .details-body
    def fix_details(mm):
        interior = mm.group(2)
        s = re.search(r"<summary>(.*?)</summary>", interior, re.S)
        if not s:
            return mm.group(0)
        resto = interior[s.end():]
        return (f"<details><summary>{s.group(1)}</summary>"
                f'<div class="details-body">{resto}</div></details>')

    cuerpo = re.sub(r'<details class="(mas|preg)">(.*?)</details>',
                    fix_details, cuerpo, flags=re.S)

    # tablas: envolver en .table-wrap si no lo estan
    cuerpo = re.sub(r'<div class="tablewrap">\s*(<table>.*?</table>)\s*</div>',
                    r'<div class="table-wrap">\1</div>', cuerpo, flags=re.S)
    cuerpo = re.sub(r'(?<!<div class="table-wrap">)(<table>.*?</table>)',
                    lambda mm: f'<div class="table-wrap">{mm.group(1)}</div>'
                    if 'table-wrap">' + mm.group(1) not in cuerpo else mm.group(1),
                    cuerpo, flags=re.S)
    # listas de terminos -> study-list
    cuerpo = cuerpo.replace("<ul>\n    <li><b>", '<ul class="study-list">\n    <li><b>')

    cabecera = (f'    <section class="chapter" id="{uid}" data-title="{kw}">\n'
                f'      <div class="chapter-head">\n'
                f'        <div class="chapter-number">{numero}</div>\n'
                f'        <div><h2>{titulo}</h2></div>\n'
                f'      </div>')
    return cabecera + cuerpo + "\n    </section>\n"


def sidebar() -> str:
    partes = []
    for titulo, items in GRUPOS:
        partes.append(f'    <div class="nav-title">{titulo}</div>')
        partes.append('    <nav class="toc" aria-label="' + titulo + '">')
        for uid, num, nombre in items:
            partes.append(f'      <a href="#{uid}"><span>{num}</span>{nombre}</a>')
        partes.append("    </nav>")
    return "\n".join(partes)


def main() -> int:
    if not SHELL.exists():
        print(f"!! falta {SHELL} (bajar index.html del repo de referencia)",
              file=sys.stderr)
        return 1
    doc = SHELL.read_text(encoding="utf-8")

    # 1. contenido: reemplazar los capitulos del apunte de referencia
    ini = doc.find('<section class="chapter"')
    fin = doc.rfind("</section>") + len("</section>")
    if ini < 0 or fin < ini:
        print("!! no se encontraron los capitulos en el shell", file=sys.stderr)
        return 1

    capitulos, faltan = [], []
    for _, items in GRUPOS:
        for uid, num, _ in items:
            f = SINT / f"{uid if uid not in ('autoev', 'glosario') else uid}.html"
            if uid == "autoev":
                f = SINT / "autoevaluacion.html"
            if uid == "glosario":
                f = SINT / "glosario.html"
            if not f.exists():
                faltan.append(f.name)
                continue
            capitulos.append(transformar(f.read_text(encoding="utf-8"), uid, num))
    if faltan:
        print(f"!! faltan fragmentos: {faltan}", file=sys.stderr)
        return 1

    doc = doc[:ini] + "\n".join(capitulos).lstrip() + doc[fin:]

    # 2. sidebar
    s_ini = doc.find('<div class="nav-title">')
    s_fin = doc.rfind("</nav>", 0, doc.find('class="side-actions"')) + len("</nav>")
    doc = doc[:s_ini] + sidebar().lstrip() + doc[s_fin:]

    # 3. identidad
    doc = re.sub(r"<title>.*?</title>",
                 "<title>Sistemas Distribuidos (75.74) - Apunte completo</title>",
                 doc, flags=re.S)
    doc = doc.replace("<strong>Aprendizaje Automático</strong>",
                      "<strong>Sistemas Distribuidos</strong>")
    doc = re.sub(r'<header class="hero">.*?</header>',
                 '<header class="hero">\n        <h1>Sistemas Distribuidos</h1>\n'
                 '        <p>Apunte completo de la materia 75.74 (FIUBA), armado sobre las '
                 'diapositivas de la cátedra, las clases grabadas, la bibliografía y '
                 '12 finales reales.</p>\n      </header>',
                 doc, flags=re.S)
    doc = re.sub(r'<meta name="description" content="[^"]*"',
                 '<meta name="description" content="Apunte completo de Sistemas '
                 'Distribuidos (75.74, FIUBA)"', doc)

    # 4. estado propio en localStorage (no compartir con el otro apunte)
    doc = re.sub(r"'aa-([a-z0-9-]+)'", r"'sd-\1'", doc)

    # 5. tokens y CSS propios
    # paleta propia: se reemplazan los dos bloques de tokens completos
    doc, n_light = re.subn(r":root\s*\{[^}]*\}", lambda _: PALETA_LIGHT, doc, count=1)
    doc, n_dark = re.subn(r'html\[data-theme="dark"\]\s*\{[^}]*\}',
                          lambda _: PALETA_DARK, doc, count=1)
    if not (n_light and n_dark):
        print(f"!! no se pudo reemplazar la paleta (light={n_light}, dark={n_dark})",
              file=sys.stderr)
        return 1
    for viejo, nuevo in SOMBRAS.items():
        doc = doc.replace(viejo, nuevo)
    doc = doc.replace('content="#167e9e"', 'content="#7455d8"')
    doc = doc.replace("</style>", CSS_EXTRA + "  </style>", 1)

    # 6. PWA de la otra materia: sacar lo que no aplica
    doc = re.sub(r'\s*<link rel="manifest"[^>]*>', "", doc)
    doc = re.sub(r'\s*<link rel="apple-touch-icon"[^>]*>', "", doc)
    doc = re.sub(r"\s*<script>[^<]*serviceWorker.*?</script>", "", doc, flags=re.S)

    # 7. el boton de resumen apunta a un archivo que este apunte no tiene
    doc = re.sub(r'\s*<a class="icon-button wide" href="resumen\.html">.*?</a>', "",
                 doc, flags=re.S)

    # 8. identidad que quedaba de la otra materia: favicon e icono de app
    favicon = (
        "data:image/svg+xml,"
        "%3Csvg xmlns='http://www.w3.org/2000/svg' viewBox='0 0 64 64'%3E"
        "%3Crect width='64' height='64' rx='14' fill='%237455d8'/%3E"
        "%3Cg stroke='white' stroke-width='3' fill='white'%3E"
        "%3Cline x1='32' y1='32' x2='32' y2='14' /%3E"
        "%3Cline x1='32' y1='32' x2='16' y2='44' /%3E"
        "%3Cline x1='32' y1='32' x2='48' y2='44' /%3E"
        "%3Ccircle cx='32' cy='32' r='6'/%3E"
        "%3Ccircle cx='32' cy='13' r='5'/%3E"
        "%3Ccircle cx='15' cy='45' r='5'/%3E"
        "%3Ccircle cx='49' cy='45' r='5'/%3E"
        "%3C/g%3E%3C/svg%3E")
    doc = re.sub(r'<link rel="icon" href="data:image/png;base64,[^"]+"',
                 f'<link rel="icon" href="{favicon}"', doc)
    doc = doc.replace('content="Aprendizaje Automático"',
                      'content="Sistemas Distribuidos"')

    # 9. sincronizacion entre dispositivos
    # El reemplazo va como lambda: re.sub interpreta los escapes del string de
    # reemplazo y convertiria los \n del JavaScript en saltos de linea reales,
    # partiendo los literales al medio.
    if not SYNC.exists():
        print(f"!! falta {SYNC}", file=sys.stderr)
        return 1
    sync = SYNC.read_text(encoding="utf-8")
    if SYNC_CANONICO.exists() and SYNC_CANONICO.read_text(encoding="utf-8") != sync:
        print(f"  !! {SYNC.name} difiere del canonico en {SYNC_CANONICO}")
    # Si el shell ya lo trae (paso, por ejemplo, cuando se refresca
    # shell-aa.html desde el apunte de Aprendizaje Automatico, que ya lo tiene
    # inyectado), no se duplica.
    n_sync = 1 if "sync-dialog" in doc else 0
    if not n_sync:
        doc, n_sync = re.subn(r"</body>", lambda _: sync + "</body>", doc, count=1)
    if not n_sync:
        print("!! no se encontro </body> para inyectar sync.html", file=sys.stderr)
        return 1

    OUT.write_text(doc, encoding="utf-8")

    ids = re.findall(r'\sid="([^"]+)"', doc)
    dup = sorted({i for i in ids if ids.count(i) > 1})
    hrefs = {h for h in re.findall(r'href="#([^"]+)"', doc)}
    rotos = sorted(hrefs - set(ids))
    print(f"escrito: {OUT}  ({len(doc.encode())//1024} KB, "
          f"{len(capitulos)} capitulos)")
    print(f"  h2={len(re.findall(r'<h2', doc))} h3={len(re.findall(r'<h3', doc))} "
          f"callouts={len(re.findall(r'class=.callout', doc))} "
          f"svg={doc.count('<svg')} tablas={doc.count('<table')}")
    # Un var() sin definir no da error: en stroke computa a none y la flecha
    # desaparece sin dejar rastro. Por eso se valida aca.
    usados = set(re.findall(r"var\(\s*(--[a-z0-9-]+)", doc))
    definidos = set(re.findall(r"(--[a-z0-9-]+)\s*:", doc))
    huerfanos = sorted(usados - definidos)

    if dup:
        print(f"!! ids duplicados: {dup[:10]}")
    if rotos:
        print(f"!! anclas rotas ({len(rotos)}): {rotos[:12]}")
    if huerfanos:
        print(f"!! tokens CSS usados y no definidos: {huerfanos}")
        print("   (definilos como alias en CSS_EXTRA, ver contrato-fragmento.md)")
    if not dup and not rotos and not huerfanos:
        print("  ids unicos, anclas resuelven, tokens CSS definidos")
    return 1 if (dup or rotos or huerfanos) else 0


if __name__ == "__main__":
    sys.exit(main())

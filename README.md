# Apunte de Sistemas Distribuidos (75.74, FIUBA)

**Se lee en https://flopeztancredi.github.io/sistemas-distribuidos/**

`index.html` es el apunte completo. `resumen/index.html` es una segunda
presentación autocontenida, organizada por conceptos y con mayor densidad. Los
dos archivos funcionan sin recursos externos y también se abren con doble clic.

## Cómo se construye

El contenido vive partido en fragmentos, uno por unidad, y el HTML final se
ensambla con scripts. Nunca se edita `index.html` a mano: se edita el
fragmento y se reconstruye.

```
fuentes/sintesis/uNN.html        contenido de cada unidad (17)
fuentes/sintesis/autoev-a|b|c    partes de la autoevaluación
fuentes/sintesis/glosario.html   generado, no editar a mano
fuentes/resumen/rNN.html         capítulos del resumen conceptual
fuentes/shell-aa.html            shell de diseño (ver abajo)
```

Orden de los scripts:

```bash
cd fuentes
python3 lint_fragmentos.py        # valida los fragmentos antes de ensamblar
python3 armar_autoevaluacion.py   # autoev-a|b|c  ->  autoevaluacion.html
python3 armar_glosario.py         # los .callout de definición  ->  glosario.html
python3 adaptar_estetica.py       # todo + shell  ->  ../index.html
python3 armar_resumen.py          # resumen/* + shell -> ../resumen/index.html
```

`adaptar_estetica.py` es el que manda: valida ids únicos, anclas y tokens CSS
al terminar, y devuelve código de salida distinto de cero si algo falla.

`lint_fragmentos.py` chequea, fragmento por fragmento, lo que el contrato pide y
lo que ya rompió alguna vez: tags balanceados, tokens de color permitidos, `<` y
`>` escapados dentro de `pre/code`, SVG con `viewBox` y `aria-label`, figuras con
`figcaption`, clases del vocabulario, ids repetidos entre fragmentos, guiones
largos y middle dots, y palabras del castellano escritas sin tilde.

## Sobre el diseño

El CSS y el JS salen de `flopeztancredi/aprendizaje-automatico` (el apunte de
Aprendizaje Automático), para que las dos materias se lean igual. `shell-aa.html`
es una copia del `index.html` de ese repo, y `adaptar_estetica.py` le reemplaza
el contenido, la sidebar y la identidad, y le agrega el CSS que ese shell no
traía (bloques de pseudocódigo, figuras con diagramas SVG, glosario y dos
variantes de callout).

De ahí vienen, sin reimplementar nada: sidebar con búsqueda, checkboxes de tema
preparado, resaltador de texto en cuatro colores, panel de notas en Markdown,
barra de progreso de lectura, tema claro y oscuro, y exportación a PDF.

**La paleta sí es propia.** Aprendizaje Automático usa turquesa; esta materia usa
lavanda (`#7455d8` en claro, `#c0a5fb` en oscuro), para que se distingan de un
vistazo cuando están deployadas juntas.

Los nombres de los tokens son los mismos que los del shell, así que su CSS
funciona sin tocarlo: el adaptador reemplaza los dos bloques de tokens (`:root` y
`html[data-theme="dark"]`) por `PALETA_LIGHT` y `PALETA_DARK`, más las tres
sombras con tinte azulado que estaban fuera de los tokens, el `theme-color` y el
favicon. Cambiar la paleta es editar esas dos constantes y reconstruir.

Los secundarios se eligieron para no competir con el lavanda: intuiciones en
azul petróleo, ejemplos en verde, avisos en ámbar y "tomado en finales" en
magenta.

Los SVG de los fragmentos no usan los tokens del shell directamente, sino tres
alias que `CSS_EXTRA` define: `--acc` (acento), `--acc2` (secundario, para
anotaciones y líneas punteadas) y `--linea` (trazo neutro de cajas y flechas).
`--linea` apunta a `--muted`, no a `--line`: ese token es un borde decorativo de
1,2:1 y como trazo de diagrama no se vería. Si se agrega un token al vocabulario
de los fragmentos hay que definir el alias, porque un `var()` sin definir en
`stroke` computa a `none` y la flecha desaparece sin error. El build lo valida.

Contrastes verificados contra WCAG AA (4.5:1) en los dos temas. El par más justo
es el texto atenuado sobre el fondo, con 4.99:1 en claro; el resto va de 5.07:1 a
16:1. El borde sobre el fondo queda en 1.23:1, igual que en el shell original
(1.20:1): es un borde decorativo y la separación real la da el blanco de las
tarjetas sobre el fondo tintado.

Para actualizar el diseño cuando cambie el apunte de la otra materia:

```bash
curl -sL https://raw.githubusercontent.com/flopeztancredi/aprendizaje-automatico/main/index.html \
  -o fuentes/shell-aa.html
cd fuentes && python3 adaptar_estetica.py
```

Dos cosas que el adaptador ajusta a propósito y conviene no perder:

- Las claves de `localStorage` pasan de `aa-` a `sd-`. Si no, los dos apuntes
  comparten notas y resaltados cuando se sirven del mismo dominio.
- Se saca el botón "Resumen" (apunta a un `resumen.html` que este apunte no
  tiene), el manifest y el service worker de la otra materia, y el favicon y el
  título de app se reemplazan por los de esta.

## Vocabulario de contenido

Está documentado en `fuentes/contrato-fragmento.md`. En los fragmentos se
escriben las clases propias (`def`, `idea`, `ej`, `warn`, `examen`) y el
adaptador las traduce a los callouts del shell:

| en el fragmento | en el HTML final | se ve como |
|---|---|---|
| `div.def` | `div.callout` | definición formal, color de acento |
| `div.idea` | `div.callout.blue` | intuición |
| `div.ej` | `div.callout.example` | ejemplo |
| `div.warn` | `div.callout.warning` | error común |
| `div.examen` | `div.callout.exam` | tomado en finales |
| `details.mas` / `details.preg` | `details` + `div.details-body` | desplegable |

## Trazabilidad

- `AUDITORIA-FIGURAS.md`: qué contenido visual de las diapositivas no había
  llegado al apunte, cuánto se cerró y los errores de contenido que aparecieron
  en el camino. Los reportes por unidad, en `fuentes/auditoria-figuras/`.
- `fuentes/manifiesto.json`: qué fuentes alimentaron cada unidad.
- `fuentes/plan.md`: mapeo de unidades a clases, videos y bibliografía.
- `DIFF-vs-apunte-viejo.md`: comparación contra el apunte anterior y resultado de
  la auditoría contra los 12 finales, con los 15 defectos corregidos.

Las fuentes de terceros que alimentaron el apunte (diapositivas de la cátedra,
bibliografía, finales transcriptos y la clase en Notion) quedan fuera del repo,
en `.gitignore`: el apunte las cita y las sintetiza, pero no las redistribuye.
Los scripts las esperan en `fuentes/diapositivas/`, `fuentes/bibliografia/`,
`fuentes/repo/` y `fuentes/notion/` si se quiere rehacer el trabajo desde cero,
aunque para reconstruir el HTML alcanza con los fragmentos versionados.

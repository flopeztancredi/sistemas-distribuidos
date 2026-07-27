# Auditoría de figuras: qué se perdió al pasar de las diapositivas al apunte

## Por qué se hizo

El apunte se escribió a partir de extracciones de **texto** de las diapositivas
(`fuentes/manifiesto.json` lo muestra: cada unidad se alimentó de archivos
`.txt`). Quien redactó nunca vio las figuras. La pregunta era cuánto contenido
puramente visual se había perdido.

El disparador fue otro: en los diagramas del apunte había flechas que no se
veían. Resultó ser un bug distinto y peor, descrito al final.

## Método

Un auditor por unidad, mirando las páginas del PDF renderizadas, no el texto.
Cada elemento visual con contenido técnico (se excluyen logos, portadas, fotos
decorativas) se clasificó en cuatro categorías:

| veredicto | significa |
|---|---|
| OK-DIAGRAMA | el apunte tiene un diagrama propio equivalente |
| OK-PROSA | no hay diagrama, pero el texto transmite la misma información completa |
| PARCIAL | el tema está, pero falta lo que específicamente aportaba la figura |
| FALTA | la información de la figura no está en ninguna forma |

Los reportes por unidad están en `fuentes/auditoria-figuras/`.

## Resultado del relevamiento

**647 diapositivas, 359 figuras técnicas.**

| | figuras | OK-DIAGRAMA | OK-PROSA | PARCIAL | FALTA |
|---|---|---|---|---|---|
| total | 359 | 53 | 201 | 95 | 10 |

El **71%** ya estaba cubierto. La conclusión importante: el contenido conceptual
no se había perdido (201 figuras estaban bien explicadas en prosa, porque el
texto de la diapositiva sí llegó), pero se perdió de forma sistemática **lo que
solo vivía en el dibujo**: topologías, líneas de tiempo, arquitecturas de
referencia y notación.

Las unidades más golpeadas:

- **u03** (diagramas y documentación técnica): 17 PARCIAL y 2 FALTA sobre 35. Es
  la unidad donde las figuras *son* el contenido: el apunte explicaba para qué
  sirve cada diagrama UML pero no mostraba la notación.
- **u21** (tiempo real): 4 FALTA y 3 PARCIAL sobre 12. Faltaban los diagramas de
  scheduling, que en tiempo real es casi todo.
- **u20** (tiempo y relojes): los diagramas espacio-tiempo importantes ya estaban
  y sus números coincidían con el deck; el hueco eran las slides 26 a 31
  (sigma/tau y los protocolos unsteady, delta y TDMA), que en el deck son
  figuras sin una línea de texto.

En el otro extremo, **u06** y **u15** no perdieron nada: sus decks son de puro
enunciado, sin un solo diagrama.

## Qué se hizo

Se cerraron los 10 FALTA y la mayoría de los PARCIAL, priorizando por valor para
un final. Los diagramas nuevos son SVG propios, con los mismos tokens de color
del resto y verificados contra la diapositiva antes de escribirse.

El apunte quedó con **101 diagramas propios** (94 en las unidades y 7 en la
autoevaluación) y pasó de 1055 a 1306 KB.

El criterio de conteo es `figure.diag`: un `<figure class="diag">` con su `<svg>`
y su `<figcaption>`. Los tres números coinciden exactamente (101 figuras, 101 SVG
con `aria-label`, 101 figcaptions). El build reporta `svg=117` porque además
cuenta 16 iconos `aria-hidden` de la interfaz, que no son diagramas.

Antes de esta auditoría `DIFF-vs-apunte-viejo.md` registraba 49 diagramas. Ese
número quedó sin poder re-verificarse, porque no se conservó una copia completa
del archivo previo.

Figuras por unidad después del cierre:

```
u01  4   u02  8   u03 15   u04  3   u05  7   u06  1
u07  9   u09  6   u10  4   u11  4   u13  5   u15  1
u16  6   u17  2   u19  3   u20 10   u21  6
autoevaluación 7
```

## Errores de contenido encontrados

La auditoría no buscaba errores, pero al comparar contra la fuente aparecieron
cuatro. Los tres primeros se verificaron contra la diapositiva y se corrigieron.

1. **u04, reparto de layers sobre tiers.** El apunte ubicaba `Services` en el
   Application Tier. La slide 11 del deck de Clase 04 lo ubica en el Business
   Logic Tier, junto a Core Business y Persistence. Corregido, con figura nueva
   del reparto completo y un aviso, porque es el error clásico del ejercicio.
2. **u01, docker-compose.** El texto decía "cuatro containers" y el YAML tenía
   tres. La slide 36 tiene cuatro: faltaba `phpmyadmin`. Completado.
3. **u21, Mars Pathfinder.** La explicación de la inversión de prioridades
   hablaba de una interrupción. El diagrama de la slide 17 muestra el mecanismo
   real: una tarea de baja prioridad retiene el lock S, la de alta se bloquea
   esperándolo y las de prioridad media la preemptan. Reescrito en esos
   términos. También se eliminó una afirmación sobre el resguardo de energía que
   no está en la diapositiva.
4. **Descartado.** Un auditor marcó como inventados los ejemplos de JobHandler y
   de los updaters en la sección de diagramas de actividades de u03. No lo son:
   salen de la transcripción del video de la cátedra, que es fuente legítima de
   esa unidad. No se tocaron; sí se agregó el ejemplo del propio deck (SerCom en
   tres iteraciones).

También se documentó una discrepancia que **no** es error del apunte: la slide
21 del deck de Clase 20 inicializa el reloj vectorial con `v[i] := 1`, pero su
propio diagrama da `(1,0)` al primer evento, que solo sale arrancando en ceros.
El apunte usa ceros, y ahora avisa qué hacer si en un final aparece la otra
convención.

## El bug de las flechas invisibles

Los SVG usaban `var(--linea)`, `var(--acc)` y `var(--acc2)`, y esos tres tokens
**no estaban definidos en ninguna parte**: 403 usos apuntando al vacío. El
contrato afirmaba que el shell los definía, y nunca fue cierto.

Un `var()` sin definir no produce ningún error: en `stroke` computa a `none` y la
flecha desaparece en silencio. Medido sobre los estilos computados en Chrome,
había **89 elementos completamente invisibles**, y todos eran del mismo tipo,
`fill="none"` más `stroke="var(...)"`, es decir líneas y flechas, mientras las
cajas con relleno seguían visibles.

Se corrigió definiendo los tres alias en `CSS_EXTRA` con criterio semántico, no
literal: `--linea` apunta a `--muted` y no a `--line`, porque `--line` es un
borde decorativo de 1,2:1 que como trazo de diagrama tampoco se habría visto.
Hoy quedan 0 elementos invisibles sobre 3781 (el único que no pinta es una banda
de título intencional en u01).

## Punto ciego de las tildes

Al revisar los renders apareció otro problema sistemático: **el texto dentro de
los SVG nunca había recibido tildes**. `acentuar.py` saltea por diseño los
bloques `<svg>`, así que todas las etiquetas de los diagramas quedaron sin
acentos desde el principio ("cola anonima", "Particion 3", "vista unica del
sistema").

Se corrigieron los 20 casos, dejando sin tilde lo que es identificador y no
prosa (el nombre de mensaje `eleccion(45)`, el campo `{numero, precio}`).

## Prevención

Para que ninguna de estas dos clases de defecto vuelva a pasar en silencio:

- `adaptar_estetica.py` ahora valida que todo `var(--token)` usado esté definido,
  y termina con código de salida distinto de cero si no lo está.
- `fuentes/lint_fragmentos.py` (nuevo) valida cada fragmento contra el contrato:
  tags balanceados, tokens de color permitidos, `<` escapado dentro de
  `pre/code`, SVG con `viewBox` y `aria-label`, figuras con `figcaption`, clases
  del vocabulario, ids repetidos entre fragmentos, guiones largos, y palabras sin
  tilde **tanto en la prosa como en las etiquetas de los SVG**.
- El contrato (`fuentes/contrato-fragmento.md`) explica que los tres tokens de
  color son alias definidos por el adaptador, y qué pasa si se agrega uno nuevo
  sin definirlo.

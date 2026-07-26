# Contrato para fragmentos de unidad del apunte

Cada agente de sintesis produce UN archivo `apunte/fuentes/sintesis/uNN.html` que
contiene exactamente un `<section>` y nada mas (sin doctype, html, head, body,
sin `<style>` ni `<script>` propios, sin recursos externos de ningun tipo).

## Estructura

```html
<section class="unidad" id="uNN" data-titulo="Titulo corto">
  <h2>UNN. Titulo de la unidad</h2>
  <p class="intro">2-4 oraciones: que cubre la unidad y por que importa.</p>

  <h3 id="uNN-tema-slug">Tema</h3>
  ...contenido...
</section>
```

- Encabezados: h2 solo el titulo de unidad, h3 temas, h4 subtemas. Todos los h3/h4
  con id prefijado `uNN-` (el indice y la busqueda se generan de ahi).
- Idioma: espanol rioplatense neutro, tecnico. Terminos en ingles cuando son de
  uso universal (commit, quorum, broker), sin traducciones forzadas.
- ORTOGRAFIA: el texto visible va con TILDES correctas (comunicación, función,
  también, está, qué). La regla de abajo prohibe guiones largos, NO prohibe
  acentos: un apunte en espanol sin tildes esta mal escrito. Los identificadores
  (id, href) y el codigo van sin acentos.
- Sin guiones largos ni middle dots en el texto: comas, dos puntos o parentesis.

## Vocabulario de clases (usar estas, no inventar)

- `<div class="def">` definicion formal de un concepto. Primer elemento interno:
  `<b>Termino.</b>` seguido de la definicion.
- `<div class="idea">` intuicion o forma de pensar un concepto (complementa def).
- `<div class="ej">` ejemplo concreto desarrollado.
- `<div class="warn">` error comun o distincion sutil que confunde en examenes.
- `<div class="examen">` senal de final: indica que esto fue preguntado en finales,
  citando la forma tipica de la pregunta. Ej: "Preguntado en finales: 'Compare X
  con Y' (2025-07, 2024-12)".
- `<details class="mas"><summary>...</summary>...</details>` para profundizaciones
  opcionales (demostraciones, casos borde, material de biblio que excede la clase).
- `<table>` para comparaciones (protocolos, modelos, garantias). Siempre con
  `<thead>`.
- `<figure class="diag">` para diagramas: SVG inline simple (cajas, flechas,
  texto) + `<figcaption>`. Paleta del SVG: solo `currentColor` y los tokens
  `var(--acc)` (acento), `var(--acc2)` (secundario, anotaciones y lineas
  punteadas) y `var(--linea)` (trazo neutro, cajas y flechas). Nada de colores
  hardcodeados.
  Esos tres nombres NO son tokens del shell: `adaptar_estetica.py` los define
  como alias en `CSS_EXTRA`, apuntando a tokens reales que se ven en los dos
  temas. Si se agrega un token nuevo al vocabulario hay que definir el alias
  ahi, o el SVG se rompe en silencio: un `var()` no definido en `stroke` computa
  a `none` y la flecha se vuelve invisible sin ningun error.
- `<code>` inline y `<pre><code>` para pseudocodigo. Pseudocodigo en estilo
  python simplificado, como usa la catedra.
- `<p class="nota">` acotacion de contexto sobre un bloque (por ejemplo, que un
  ejercicio se repite en todos los finales con la misma forma).
- `<p class="ref">` cierre de una respuesta de autoevaluacion con los enlaces a
  las secciones del apunte donde se estudia el tema.
- `<dl class="glo">` solo en el glosario, que se genera automaticamente con
  `armar_glosario.py` a partir de los bloques `.def`: no se escribe a mano.

## Contenido

- El hilo conductor es el deck de diapositivas de la unidad: cubrir TODOS sus
  temas, en su orden salvo que el orden pedagogico claramente mejore.
- Los transcripts aportan las explicaciones habladas: incorporar la intuicion y
  los ejemplos del docente (sin citar "el profesor dice": integrado al texto).
- El deck alternativo de CLASES/ complementa donde el principal es escueto.
- Notion aporta enfasis de cursada y (en Final) que se pregunta: usar para
  calibrar profundidad y para los bloques `.examen`.
- Kleppmann (unidad 13): usar caps 1/5/6 para dar profundidad real a
  replicacion y particionamiento.
- Autocontenido: el lector NO tiene las diapositivas. Nada de "como se ve en la
  filmina". Todo concepto usado se define antes o se linkea con
  `<a href="#uNN-slug">`.
- Densidad: esto es un apunte de estudio, no un libro. Parrafos cortos, listas,
  tablas. Cada afirmacion tiene que ganarse el lugar.

## Prohibido

- Recursos externos (fonts, imagenes, CDNs). Todo inline.
- Datos personales de alumnos que aparezcan en las fuentes (nombres, padrones).
- Inventar contenido que no este respaldado por alguna fuente. Ante duda, el
  bloque `.warn` puede decir "la catedra no lo cubre en profundidad".

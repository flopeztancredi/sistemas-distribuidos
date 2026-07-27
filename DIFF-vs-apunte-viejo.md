# Diff: apunte nuevo vs SD_Apunte_Distribuidos.html

Comparación del apunte generado (`apunte/index.html`) contra el que venías
armando durante la cursada. Hecha después de cerrar los huecos que detectó la
auditoría contra finales.

## Números

La columna "Nuevo" está remedida después de la auditoría de figuras, que agregó
diagramas y texto. Método: palabras de texto visible con `html.parser`
descartando `script`, `style` y `svg`; el resto contando ocurrencias del tag.

| Métrica | Viejo | Nuevo |
|---|---:|---:|
| Palabras de texto | 33.050 | 126.460 |
| Tamaño del archivo | 5.642 KB | 1.306 KB |
| Secciones de primer nivel | 21 | 19 |
| Subsecciones (h3) | 156 | 166 |
| Sub-subsecciones (h4) | 85 | 207 |
| Diagramas SVG | 4 | 101 |
| Capturas de filminas (JPEG embebido) | 70 | 0 |
| Tablas | 22 | 67 |
| Bloques desplegables | 109 | 88 |

El nuevo tiene casi 4 veces más texto en un archivo 4 veces más liviano: el peso
del viejo son las 70 capturas de filminas en JPEG. El nuevo usa diagramas SVG
propios, que además se adaptan al tema claro u oscuro y escalan sin pixelarse.

Los números del viejo no se pueden re-verificar: no se conservó una copia
completa de ese archivo.

## Contenido que el viejo no tiene

Verificado buscando el término y su contexto en ambos documentos:

- **Unidad completa de Sistemas de Tiempo Real (U21).** El viejo termina en
  relojes y cortes de estado. "Tiempo real" aparece en el viejo solo dos veces
  y de pasada ("juegos en tiempo real", "carga en tiempo real"), sin sección.
  El nuevo cubre la unidad entera: hard y soft RT, sistemas de control,
  sensores y actuadores, y los casos de estudio Therac-25, Ariane 5 y Mt. Gox.
- **Raft.** En el viejo aparece cinco veces, siempre como referencia cruzada
  ("Paxos/Raft"), sin desarrollo. En el nuevo tiene subsección propia, con la
  aclaración de que la cátedra solo lo deja en bibliografía.
- **Teorema FLP de imposibilidad** y **Terraform**, ausentes en el viejo.
- **Autoevaluación con finales reales.** El viejo tiene ~103 ítems de práctica
  inventados, uno por clase. El nuevo tiene 71 preguntas tomadas de finales
  reales 2022-2025, con la fecha del examen donde apareció cada una, y 33 de
  ellas son ejercicios prácticos resueltos con desarrollo completo (cálculos de
  volumen con unidades, endpoints, pseudocódigo, arquitecturas).
- **75 marcas de "tomado en finales"** repartidas por el cuerpo del apunte, con
  la forma textual de la pregunta. 66 traen además la fecha del examen; las 9
  restantes son preguntas recurrentes que se citan sin atarlas a una fecha
  puntual. El viejo no las tiene.

## Contenido del viejo que el nuevo también cubre

Se compararon los 96 temas de contenido del viejo (sus h3, descontando "Mapa de
la clase", "Glosario", "Autoevaluación" y "Guía de lectura", que son
estructurales) más los 182 términos de sus glosarios. Resultado: **no quedó
ningún tema del viejo sin cobertura en el nuevo**.

Se verificaron explícitamente los que más riesgo tenían de haberse perdido, por
estar en unidades que el nuevo organiza distinto:

- Shared Code Snippets (segundo caso de NALSD): está en U15.
- Evolución de las arquitecturas: está en U11 y U16.
- Catálogo de diagramas UML: el nuevo cubre ocho tipos (casos de uso, paquetes,
  actividades, componentes, secuencia, despliegue, robustez y topología de red).
- De los 182 términos de glosario, 38 no matchearon por texto literal. Se
  revisaron los 20 más sospechosos uno por uno (back-pressure, hot shard,
  atomic broadcast, wait-for graph, variable de condición, ORB de CORBA, VFS y
  NFS, colectivas de MPI, shuffle, read-your-writes, principio de Miller,
  quorum 2f+1, entre otros) y **los 20 están cubiertos**, escritos con otra
  redacción. Los 18 restantes son etiquetas compuestas del mismo estilo.

## Diferencias de formato

El viejo tenía tres features que el nuevo no replicaba:

1. **Glosario consolidado por clase** (20 bloques, 182 términos). El contenido
   ya estaba cubierto en los 118 bloques de definición del nuevo, pero faltaba
   el índice. **Cerrado**: se agregó una sección de glosario con los 118
   términos ordenados alfabéticamente, cada uno con su definición y un enlace
   a la sección donde se estudia. Se genera con `armar_glosario.py` a partir de
   las definiciones existentes, así que no se desincroniza del cuerpo.
2. **Ruta de lectura y dependencias** (mapa de qué leer antes de qué, con un
   núcleo secuencial y pistas temáticas). No se replicó a propósito: el nuevo
   está ordenado para leerse de arriba hacia abajo, que es como se pidió.
3. **Guía de lectura por clase**, que indica qué mirar en cada filmina del PDF
   original ("1-2 portada y agenda, 3-5 tendencias..."). No aplica: el nuevo es
   autocontenido y no asume que tengas las diapositivas al lado.

## Huecos de la auditoría, cerrados

Los tres que había dejado pendientes la auditoría contra finales:

- **U07: mapeo de pipes y filters a artefactos de programación.** Lo pide
  literalmente el final del 2025-07-03. Se agregó la subsección con el mapeo
  explícito (filter como proceso, worker o función de transformación; pipe como
  pipe del SO, cola de MOM, socket PUSH/PULL de ZeroMQ o stream de Flink), una
  tabla de concepto, artefacto, ejemplo y garantías, un ejemplo desarrollado de
  punta a punta y un diagrama del pipeline.
- **U09: diagrama de objetos distribuidos con el estado de las instancias.** El
  final del 2025-07-03 pide el gráfico y el estado después de la operación. Se
  agregó el diagrama con el proceso cliente y su proxy, el dispatcher del
  servidor y las dos cuentas mostrando saldo antes y después de la
  transferencia (1000 a 800 y 500 a 700).
- **U09: atomicidad y RPC asincrónico.** Se agregó el aviso de que una
  transferencia toca dos objetos y por lo tanto exige atomicidad, enlazando a
  two-phase commit, y una subsección de RPC asincrónico (one-way, callback
  stub, futures, y encolar con ID de request más polling) con el diagrama de
  secuencia del caso de la consulta que demora minutos.

Los otros dos huecos que la auditoría había marcado (pseudocódigo del ejercicio
publisher-subscriber y el DAG aplicado con top-N distribuido) ya habían quedado
cubiertos por la sección de ejercicios prácticos, que se escribió después de
que corriera la auditoría.

## Auditoría completa: 10 finales, 100 preguntas

| Final | Respondibles | Parciales | Ausentes |
|---|---:|---:|---:|
| 2022-08-02 y 2022-08-09 | 18/20 | 2 | 0 |
| 2023-07-25 y 2024-07-08 | 19/20 | 1 | 0 |
| 2024-07-16 y 2024-12-19 | 19/20 | 1 | 0 |
| 2025-02-20 y 2025-02-27 | 18/20 | 2 | 0 |
| 2025-03-06 y 2025-07-03 | 19/20 | 1 | 0 |
| **Total** | **93/100** | **7** | **0** |

Ningún tema de ningún final quedó ausente del apunte. Los 7 parciales se
corrigieron todos (ver abajo).

Donde existe resolución corregida por la cátedra (los finales de agosto 2022 y
febrero 2025) el apunte está al nivel exigido o por encima. En el ejercicio de
diseño de febrero 2025 el material ya incorpora las correcciones que el docente
marcó en rojo sobre la hoja de la alumna: el orden de magnitud del peso de la
imagen, el factor de eventos por entrada y salida, el pasaje de unidades, que la
impresión horaria es un job y no un endpoint, y que en un GET va retorno y no
body.

## Defectos de contenido que encontró la auditoría

Los tres primeros no eran material faltante sino **material incorrecto**, que es
peor: un alumno que lo copiara al examen contestaba mal. Verificados uno por uno
antes de corregir.

1. **Barrera con una sola blocking queue (autoevaluación).** Proponía una cola
   de capacidad N donde cada worker hace `put` y después `take`, afirmando que
   "nadie puede sacar hasta que la cola esté llena", y la presentaba como "la
   que suele esperarse porque es más elegante". Es falso: `take` bloquea cuando
   la cola está **vacía**, no hasta que se llene, así que el primer worker cruza
   la barrera sin esperar a nadie y no hay barrera. **Corregido**: ahora es un
   bloque de aviso que explica por qué el atajo no funciona (es justo el que se
   le ocurre a cualquiera bajo presión) y a continuación va una variante
   descentralizada que sí funciona, con una cola por worker y conteo de las N
   llegadas numerando la ronda.
2. **Orden total contra orden causal (U20).** Afirmaba que el ejemplo dado
   mostraba orden total respetado con causalidad violada. No: en ese ejemplo los
   dos emisores son independientes, así que los mensajes son **concurrentes** y
   el orden causal no dice nada sobre ellos. El texto además se contradecía,
   porque tres líneas más abajo señalaba correctamente que entre emisores que no
   se comunican el "antes" ni siquiera está bien definido. **Corregido**: se
   arregló la afirmación y se agregó la traza que el final pide de verdad, con
   mensajes causalmente relacionados (P1 emite m1, P2 lo recibe y por eso emite
   m2, y todos entregan m2 antes de m1), más el ejemplo del chat donde se lee la
   respuesta antes de la pregunta.
3. **Pseudocódigo del XOR distribuido (autoevaluación).** Tenía tres defectos
   encadenados: usaba el acumulador antes de inicializarlo, después lo
   reinicializaba a cero borrando lo acumulado en el loop, y como no sacaba el
   futuro de la lista de pendientes, el reduce final volvía a XORear parciales ya
   sumados, que en XOR se cancelan. El resultado impreso era incorrecto.
   **Corregido**.

Los otros cuatro eran material incompleto:

4. **U17: ventajas y desventajas de replicación activa contra pasiva.** Estaban
   las diferencias estructurales pero no las ventajas, que son la mitad de la
   consigna del final de agosto 2022. **Agregado**: tabla con ventajas y
   desventajas de los tres esquemas (costo de cómputo, exigencia de determinismo
   y de orden total, tiempo de failover, detección de réplicas divergentes por
   comparación de respuestas) y el criterio para elegir entre ellos.
5. **U05: tolerancia a fallos del broker.** El apunte cubría ACK (caída del
   consumidor) y durabilidad (reinicio del broker), pero no el caso en que el
   broker queda caído, que es el punto único de falla de un MOM centralizado.
   **Agregado**: clustering, colas replicadas con quorum queues basadas en Raft,
   reconexión del cliente, y el trade-off de latencia que implica replicar.
6. **Autoevaluación: cuarta consulta del caso Smart TV.** El enunciado de agosto
   2022 pide los usuarios con más de una visualización por día, y la resolución
   tenía otra cuarta consulta. **Agregado** el endpoint con la explicación de que
   se materializa con clave compuesta y umbral en el reduce, no con un scan.
7. **Autoevaluación: vista física sin diagrama** en el caso del reporte
   ciudadano de infracciones. Los casos análogos sí tienen diagrama y la unidad
   15 señala que la vista física puntúa. **Corregido**: se agregó el diagrama
   con el flujo completo (subida directa al object storage con URL prefirmada,
   cola de ingesta, pipeline de OCR y join replicado, router por tipo de
   infracción, derivación a revisión manual por umbral de confianza, emisión y
   servicio de email externo, base particionada por año y log de auditoría).

## Segunda ronda: los dos finales restantes (12 finales, 120 preguntas)

Los finales 2025-07-17 y 2025-07-24 se habían reservado como control, pero
**el control no resultó ciego**: el apunte cita explícitamente el 17-07 en U10 y
los agentes de síntesis habían buscado en todo el directorio de finales para
marcar los bloques de examen, así que estos dos también alimentaron el
contenido. La auditoría mide cobertura, no generalización a exámenes no vistos.

Resultado: **19 de 20 respondibles, 1 parcial, 0 ausentes**. Total acumulado
sobre los 12 finales: **112 de 120 respondibles**.

A este auditor se le pidió además un segundo objetivo: buscar **errores de
contenido**, no solo huecos, verificando los pseudocódigos paso a paso y
recalculando los números. Encontró cinco, todos verificados antes de corregir:

1. **U19, pseudocódigo del consenso sincrónico por rondas: off-by-one.** El loop
   escribe `values[r+1]`, así que después de las f+1 rondas el conocimiento
   acumulado está en `values[f+2]`, pero la decisión se toma sobre
   `values[f+1]`, que es el estado previo a la última ronda: justo la que
   garantiza agreement. Contradice al ejemplo de la propia sección.
   **Particularidad importante**: el error no lo introdujo el apunte, viene de la
   diapositiva 44 de la cátedra, que lo copia de Coulouris. Por eso no se
   cambió el pseudocódigo (en el final conviene reproducir la notación que
   enseñan) sino que se agregó una nota que explica la trampa del índice y
   aclara que la agregación va sobre todo lo acumulado.
2. **U20, inicialización de los relojes vectoriales.** El pseudocódigo hacía
   `v = [0] * N` y después `v[i] = 1`, con lo cual el primer evento daba (2,0)
   mientras la figura y todos los ejercicios de la misma unidad usan (1,0). La
   línea sobraba y además rompía el invariante que el propio texto enuncia.
   **Corregido**: arranca en ceros.
3. **Autoevaluación, ejercicio de consenso del riego: el caso de divergencia no
   divergía.** Decía que con P1 = NO_REGAR el resultado divergiría, pero con la
   regla de desempate declarada arriba (empate, no regar) los tres procesos
   deciden NO_REGAR igual. **Corregido**: se reemplazó por el caso que sí
   diverge, que es que el proceso caído hubiera propuesto NO_REGAR (P1 ve empate
   y decide no regar, P2 y P3 ven 2 a 1 y deciden regar), que es justamente lo
   que justifica la segunda ronda.
4. **Autoevaluación, ejercicio de relojes: número mal calculado.** Decía
   `L(g) = 4`. En P1 el evento previo a g es a (L=1) y f llega con L=4, así que
   L(g) = max(1, 4) + 1 = **5**. La conclusión se sostiene igual (3 < 5), pero
   el número estaba mal. **Corregido**.
5. **U09, celda equivocada en la tabla de call semantics.** La fila "sin
   control" tenía "no implementable" en la columna de filtro de duplicados,
   donde corresponde "no aplica": sin reintentos no hay duplicados que filtrar.
   La tabla equivalente de U07 ya lo tenía bien. **Corregido**.

Más una inconsistencia menor, también corregida: en el ejercicio del promedio de
ventas se atribuía al worker el problema de acumular un millón de valores en
memoria, cuando en el pseudocódigo mostrado el que acumula (y el cuello de
botella) es el dispatcher.

Y el único hueco de cobertura: **U01 no daba ninguna situación concreta donde
centralizar sea preferible**, que es la segunda mitad de la pregunta 1 del final
de julio 2025. **Agregado**: escala acotada, consistencia fuerte como requisito
duro, auditoría y regulación, y previsibilidad temporal en sistemas de tiempo
real, más el criterio de cuándo distribuir no se justifica.

## Nota sobre el método

De los 8 defectos que encontró esta última ronda, 6 eran **material incorrecto**
y no material faltante. Eso es lo más valioso de haber auditado los 12 finales:
un hueco se nota al estudiar, pero una afirmación falsa se copia con confianza.
El pedido explícito de "verificá los pseudocódigos ejecutándolos mentalmente y
recalculá los números" fue lo que los destapó, y conviene repetirlo si se agrega
contenido nuevo al apunte.

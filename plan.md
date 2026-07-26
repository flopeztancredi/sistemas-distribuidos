# Plan del apunte - mapeo de fuentes por unidad

Numeracion canonica = diapositivas de la catedra (1-21, sin 8/12/14/18).
"CLASES/" = decks alternativos del repo (numeracion propia). "videos" = numeracion
de los mp4/transcripts (distinta de la de diapositivas).

| U | Tema | Diapositivas | CLASES (repo) | Transcripts (videos) | Notion | Biblio |
|---|------|--------------|---------------|----------------------|--------|--------|
| 1 | Introduccion a Sist. Distribuidos | Clase 01 | 1 | - | 19/08 | Coulouris c1-2, Tanenbaum c1 |
| 2 | Multitasking y comunicaciones | Clase 02 | 2 | - (videos clase 2 faltan) | 21/08 | - |
| 3 | Paralelizacion, multiprocessors, nombres; diagramas y doc tecnica | Clase 03 (x2) | 3, 6.1 | clase-4: doc-tecnica, diagramas | 26/08 | UML/C4 refs |
| 4 | Layers/tiers, interfaces, protocolos, REST | Clase 04 | 4 | clase-5 x4 | - | Tanenbaum c2.1, c4 |
| 5 | Mensajes, grupos, middlewares, MOMs; RabbitMQ | Clase 05 (x2) | 5.1, 6.2 | clase-4: middlewares; clase-10: rabbitmq | 02/09 | Verissimo c2.1/2.4, Tanenbaum c4.3 |
| 6 | Practica de disenio multicomputing | Clase 06 (x2) | 5.2, 7.2 | - | 09/09 | - |
| 7 | Patrones de comunicacion; ZeroMQ | Clase 07 (x2) | 7.1, 7.3 | clase-11 x3; clase-10: zeromq | 09/09 | Coulouris c5.2/6.3 |
| 9 | Arquitecturas distribuidas simples: C/S, P2P, RPC, RMI | Clase 09 | 8 | clase-9 x4 | - | Coulouris c5/c8, Verissimo c3.6/4.4 |
| 10 | Distribucion y coordinacion: MapReduce, MPI, Flink/Beam | Clase 10 | 9 | clase-12 x2 | MPI-Flink-Beam | MapReduce paper refs |
| 11 | Sistemas elasticos y alta disponibilidad | Clase 11 | 14 | - | 23/09 | Coulouris c18, Tanenbaum c8.1 |
| 13 | Data intensive: particion, replicacion, DSM, DFS | Clase 13 | 13 | clase-14 v1-v4 | 30/09 | KLEPPMANN c1/5/6, Verissimo c3.8, Coulouris c12 |
| 15 | Disenio de arquitecturas de gran escala | Clase 15 | 18.2 | clase-17: traffic-violation (caso) | - | NALSD (SRE) |
| 16 | SOA, Cloud, PaaS, App Engine, BigTable | Clase 16 | 15, 18.1 | clase-16 x4; clase-14 v5: bigtable | - | - |
| 17 | Tolerancia a fallos, confiabilidad, acuerdo | Clase 17 | 16 | clase-18 x3 | - | Verissimo c6-8, Coulouris c15/17 |
| 19 | Consenso: lider, bizantinos, Paxos, Raft | Clase 19 | 17 | clase-19 x4 | - | Paxos Simple, Raft |
| 20 | Tiempo, relojes, sincronismo, orden, cortes | Clase 20 | 10, 12 | clase-8 x3 | - | Verissimo c2.5-2.7, Coulouris c14.5 |
| 21 | Sistemas de tiempo real | Clase 21 | 19 | clase-20 x2 | - | Verissimo c11-12 |

Transversal:
- TP1 - Disenio y TP Paper (Notion): contexto de practica, mencionar en unidades 6 y 15.
- Notion "Final": preguntas de finales -> seccion autoevaluacion.
- RESUELTOS.pdf (70p) + INTEGRADOR.pdf (93p) + fotos transcriptas -> banco de
  preguntas para autoevaluacion y auditoria de cobertura.

Fases restantes:
1. [en curso] Extraccion Notion + transcripcion fotos finales.
2. Sintesis por unidad (agentes paralelos, 1 por unidad, reciben todas sus fuentes).
3. Ensamblado HTML unico autocontenido (nav lateral, busqueda, colapsables, dark mode).
4. Auditoria: agentes rinden cada final solo con el apunte; huecos -> se corrigen.
   Diff de cobertura contra SD_Apunte_Distribuidos.html (el viejo del usuario).
5. Seccion autoevaluacion: preguntas de finales agrupadas por tema con respuesta
   desplegable.

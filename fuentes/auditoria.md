# Fase de auditoria del apunte

Criterio del usuario: alguien que lea SOLO este apunte tiene que poder rendir
cualquiera de los finales 2022-2025 y sacarse una nota excelente.

## Metodo

No sirve preguntarle a un agente "esta completo?". El apunte pesa 560 KB y no
entra comodo en contexto. En cambio, cada auditor toma finales concretos y, por
cada pregunta, busca en los fragmentos el material que la responde. Reporta:

- `RESPONDIBLE`: el apunte tiene todo lo necesario (cita el ancla).
- `PARCIAL`: hay material pero falta algo puntual para contestar bien (dice que).
- `AUSENTE`: el tema no esta.

El output es una lista de huecos accionables, no una opinion global.

## Reparto (5 auditores, 2 finales cada uno)

| Auditor | Finales |
|---|---|
| 1 | 2022-08-02, 2022-08-09 |
| 2 | 2023-07-25, 2024-07-08 |
| 3 | 2024-07-16, 2024-12-19 |
| 4 | 2025-02-20, 2025-02-27 |
| 5 | 2025-03-06, 2025-07-03 |

(2025-07-17 y 2025-07-24 quedan como control: si los huecos de los otros diez
se corrigen, estos dos deberian pasar sin cambios. Se auditan al final.)

## Despues de la auditoria

1. Consolidar los huecos por unidad.
2. Un agente por unidad con huecos: los completa sobre el fragmento existente.
3. Re-ensamblar y re-validar.
4. Diff de cobertura contra SD_Apunte_Distribuidos.html (el apunte viejo del
   usuario): listar los temas que el viejo trata y el nuevo no, para decidir si
   son huecos reales o material que el viejo tenia de mas.

# Informe de estado del proyecto — Sprint 3

**Nombre del Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

**Sprint:** 3 — Usuarios y propuesta de ruta

**Inicio:** 2026-10-09. **Cierre informado:** 2026-11-05.

**Versión:** 1.0.0. **Fecha de actualización documental:** 2026-11-05.

[Volver al README principal](../../../README.md)

## Historias de Usuario completadas en este Sprint

El periodo de dos semanas cerraba el 22 de octubre. El incremento se publicó el 5 de noviembre. Se cerraron dos historias. El mapa no entra en este cierre.

| Historia | Backlog | Funcionalidad completada | Estado |
|---|---|---|---|
| US-002 | EP-01 | El administrador registra un usuario y actualiza su nombre y estado | Finalizada |
| US-006 | EP-03 | Con pedidos pendientes y un vehículo disponible, el sistema propone una ruta en lista y respeta la capacidad | Finalizada |

## Demostración del trabajo completado

La demostración usa http://127.0.0.1:8765.

| Historia | Funcionalidad terminada | Recorrido de presentación | Evidencia |
|---|---|---|---|
| US-002 | Alta y modificación de usuarios | Entrar como `administrador@ecologistica.test` / `admin123`. Registrar un contratante. Cambiar su nombre o pasarlo a INACTIVO. El operador no puede crear usuarios | `src/backend/ecologistica/servicio.py` y `tests.test_reglas` |
| US-006 | Propuesta de ruta | Entrar como `operador@ecologistica.test` / `operador123`. Registrar vehículo, puntos y un pedido general. Pulsar Generar ruta. Sin vehículo disponible, la propuesta no se crea | API `/api/rutas` |

La lista ordena las paradas de norte a sur dentro de El Tambo, Huancayo y Chilca. El pedido que no cabe queda PENDIENTE. El que entra a la propuesta pasa a EN_RUTA.

## Pendientes

1. **US-007:** dibujar la ruta en el mapa. Este sprint solo muestra la lista.
2. **US-008:** reoptimizar una ruta ya generada.
3. **US-009:** filtrar el listado de pedidos. El contratante ya puede ver el listado, sin filtro.
4. Pasar la API a FastAPI y el almacén en memoria a PostgreSQL.
5. Adjuntar las capturas recortadas de Jira.

## Historial de versiones

| Versión | Fecha de edición | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-05 | Informe del Sprint 3 con usuarios y propuesta de ruta. |

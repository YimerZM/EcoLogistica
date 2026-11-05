# Revisión del sprint — Sprint 3

**Nombre del Proyecto:** EcoLogística — Sistema de Optimización de Rutas Sostenibles

**Líder del Proyecto:** ZEVALLOS MELENDRES YIMER EDYSON

**Sprint:** 3 — Usuarios y propuesta de ruta

**Inicio:** 2026-10-09. **Cierre informado:** 2026-11-05.

**Versión:** 1.0.0. **Fecha de actualización documental:** 2026-11-05.

[Volver al README principal](../../../README.md)

## Historias de Usuario completadas en este Sprint

Se aceptan US-002 y US-006. US-007 no se presenta como terminada.

| Historia | Backlog | Funcionalidad completada | Estado |
|---|---|---|---|
| US-002 | EP-01 | Registrar usuario y modificar nombre y estado | Finalizada |
| US-006 | EP-03 | Generar una propuesta de ruta o informar que no hay vehículo disponible | Finalizada |

## Demostración del trabajo completado

Participaron ZEVALLOS MELENDRES YIMER EDYSON, POMACHAGUA YAPIAS BRYAN ANTONY y CAJAMALQUI DAVILA JOSEMARIA PIERO.

| Historia | Funcionalidad terminada | Recorrido de presentación | Evidencia |
|---|---|---|---|
| US-002 | Usuarios | El administrador crea al contratante. Una cuenta INACTIVA no inicia sesión. El operador recibe autorización denegada | `POST /api/usuarios` y `PUT /api/usuarios` |
| US-006 | Ruta | El operador genera la ruta del pedido general. La parada muestra distrito y peso. Un pedido que supera la capacidad no entra | `POST /api/rutas` |
| Consulta | Listado del contratante | El contratante inicia sesión y ve los pedidos. No puede registrar operaciones ni filtrar | Pantalla de consulta |

## Pendientes

1. Cambiar el mapa esquemático por cartografía externa si la revisión lo pide.
2. FastAPI, PostgreSQL y las capturas recortadas de Jira.

## Historial de versiones

| Versión | Fecha de edición | Cambio |
|---|---|---|
| 1.0.0 | 2026-11-05 | Revisión del Sprint 3. |
